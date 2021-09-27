from config import *
from retry import retry
from error import *

import os
import yaml
import pathlib
import subprocess
import io
import collections
import sys
import json
import re

import plumbum
from plumbum import local
from plumbum.cmd import find, cut, sort


@retry(
    (ImageRegistryLoginRetry),
    tries=HTTP_RETRY_ATTEMPTS,
    delay=HTTP_RETRY_WAIT_SECS,
    logger=log,
)
def auth_registries(push_repos):
    repos = {}
    for repo, metadata in push_repos.items():
        if metadata.get("only_if", False) and not os.getenv(metadata["only_if"]):
            log.info("repo: '%s' only_if requirement not satisfied", repo)
            continue
        user = os.getenv(metadata["user"])
        if not user:
            user = metadata["user"]
        passwd = os.getenv(metadata["pass"])
        if not passwd:
            passwd = metadata["pass"]
        repos[metadata["registry"]] = {"user": user, "pass": passwd}

    if not repos:
        log.fatal("Could not retrieve registry credentials. Environment not set?")
        sys.exit(1)

    # docker login
    for repo, data in repos.items():
        log.info(f"Logging into {repo}")
        #  log.debug(f"USER: {data['user']} PASS: {data['pass']}")
        result = shellcmd(
            "docker",
            ("login", repo, f"-u" f"{data['user']}", f"-p" f"{data['pass']}",),
            printOutput=False,
            returnOut=True,
        )
        if result.returncode > 0:
            raise ImageRegistryLoginRetry()
        else:
            log.info(f"Docker login to '{repo}' was successful.")


#  def auth_registries(self):
#      for repo, metadata in self.parent.manifest[self.key].items():
#          registry = {}
#          if repo in (
#              "gitlab-master",
#              "artifactory",
#              "nvcr.io",
#          ):  # TODO: push to Nvidia Registry
#              log.debug(f"Skipping push to {repo}")
#              continue
#          if metadata.get("only_if", False) and not os.getenv(metadata["only_if"]):
#              log.info("repo: '%s' only_if requirement not satisfied", repo)
#              continue
#          user = os.getenv(metadata["user"])
#          if not user:
#              user = metadata["user"]
#          passwd = os.getenv(metadata["pass"])
#          if not passwd:
#              passwd = metadata["pass"]
#          self.repo_creds[repo] = {"user": user, "pass": passwd}
#          for arch in ("x86_64", "ppc64le", "arm64"):
#              registry[f"README-{arch}.md"] = metadata["registry"][arch]
#          self.repos_dict[repo] = registry

#      if not self.repos_dict:
#          log.fatal("Could not retrieve registry credentials. Environment not set?")
#          sys.exit(1)
#      # docker login
#      result = shellcmd(
#          "docker",
#          (
#              "login",
#              f"-u" f"{self.repo_creds['docker.io']['user']}",
#              f"-p" f"{self.repo_creds['docker.io']['pass']}",
#          ),
#          printOutput=False,
#          returnOut=True,
#      )
#      if result.returncode > 0:
#          log.error(result.stderr)
#          log.error("Docker login failed!")
#          sys.exit(1)
#      else:
#          log.info("Docker login was successful.")


def shellcmd(bin, args, printOutput=True, returnOut=False):
    """Run the shell command with specified arguments for skopeo/docker

    args        -- A tuple of arguments.
    printOutput -- If True, the output of the command will be send to the logger.
    returnOut   -- Return a tuple of the stdout, stderr, and return code. Default: returns true if the command
                 succeeded.
    """
    if "skopeo" in bin:
        bin_name = local["/usr/bin/skopeo"]
    elif "docker" in bin:
        # find docker
        if pathlib.Path("/usr/local/bin/docker").exists():
            bin_name = local["/usr/local/bin/docker"]
        elif pathlib.Path("/usr/bin/docker").exists():
            bin_name = local["/usr/bin/docker"]
        else:
            raise Exception("Can't find docker client executable!")
    else:
        log.error("%s is not supported by method - shellcmd", bin)
        sys.exit(1)
    out = ""
    err = ""
    # XXX: This can leak secrets!
    #  log.debug(f"Running command: bin: {bin} args: {args}")
    p = bin_name.popen(
        args=args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
        # do something with line
        out += line
        if printOutput:
            log.info(line)
    for line in io.TextIOWrapper(p.stderr, encoding="utf-8"):
        err += line
        if printOutput:
            log.error(line)
    p.communicate()
    if returnOut:
        Output = collections.namedtuple("output", "returncode stdout stderr")
        return Output(p.returncode, out, err)
    if p.returncode != 0:
        #  log.error("See log output...")
        return False
    return True


# Returns a list of packages used in the templates
def template_packages(distro):
    # 21:31 Tue Jul 13 2021 FIXME (jesusa): this func feels like a hack
    log.info(f"current directory: {os.getcwd()}")
    temp_dir = "ubuntu"
    if any(d in distro for d in ["centos", "ubi"]):
        temp_dir = "redhat"
    # sometimes the old ways are the best ways...
    cmd = (
        find[
            f"templates/{temp_dir}/",
            "-type",
            "f",
            "-iname",
            "*.j2",
            "-exec",
            "grep",
            r"^ENV\ NV_.*_VERSION\ .*$",
            "{}",
            ";",
        ]
        | cut["-f", "2", "-d", " "]
        | sort["-u"]
    )
    log.debug(f"command: {cmd}")
    # When docker:stable (alpine) has python 3.9...
    #  return [x.removesuffix("_component_version") for x in cmd().splitlines()]
    return [
        x[3 : -len("_VERSION")].lower()
        for x in cmd().splitlines()
        if "_VERSION" in x and not "CUDA_LIB" in x
    ]


def load_rc_push_repos_manifest_yaml():
    push_repo_path = pathlib.Path("manifests/rc-push-repos.yml")
    log.debug(f"Loading push repos manifest: {push_repo_path}")
    obj = {}
    with open(push_repo_path, "r") as f:
        obj = yaml.load(f, yaml.Loader)
    return obj


def latest_l4t_base_image():
    l4t_base_image = "nvcr.io/nvidian/nvidia-l4t-base"
    #  return f"{l4t_base_image}:r32_CUDA_10.2.460_RC_006"
    #  return f"{l4t_base_image}:r32.2"
    # bash equivalent
    #  /usr/bin/skopeo list-tags docker://nvcr.io/nvidian/nvidia-l4t-base | jq -r '.["Tags"] | .[]' | grep "^r[[:digit:]]*\." | sort -r -n | head -n 1
    out = shellcmd(
        "skopeo",
        ("list-tags", f"docker://{l4t_base_image}"),
        printOutput=False,
        returnOut=True,
    )
    #  pp(out)
    if out[0] != 0:
        log.error(
            f"Some problem occurred in getting tags from NGC (nvcr.io): {out.stderr}"
        )
        sys.exit(1)

    try:
        tag_dict = json.loads(out.stdout)
    except json.JSONDecodeError as e:
        log.error(f"Some problem occurred loading skopeo json ret: {e.msg}")
        sys.exit(1)

    tag_list = []
    # TODO: refactor
    for key in tag_dict.keys():
        if "Tags" in key:
            tag_list = list(tag_dict[key])
    tag_list2 = []
    for tag in tag_list:
        # Match r32_CUDA
        #  if re.match("^r[\d_]*CUDA", tag):
        # Match r32\.*
        if re.match("^r[\\d]*\\.", tag):
            tag_list2.append(tag)
    return f"{l4t_base_image}:{sorted(tag_list2, reverse=True)[0]}"
