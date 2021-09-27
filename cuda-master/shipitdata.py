from config import *
from dotdict import *
from retry import retry
from error import *
import utils

import requests
import pathlib
import re
import sys
import json
import yaml

from plumbum.cmd import rm


class ShipitData:
    """Class to wrap shipit data.
    """

    data = DotDict()

    shipit_uuid = ""
    shipit_manifest = DotDict()

    product_name = ""
    candidate_number = 0
    release_label = ""
    distros = None

    l4t_base_image = ""

    push_repo_logged_in = ""

    def __init__(self, shipit_uuid):
        self.shipit_uuid = shipit_uuid
        self.data = DotDict(self.get_shipit_global_json())

    def get_shipit_funnel_json(self, distro, distro_version, arch):
        funnel_distro = distro
        if any(distro in funnel_distro for distro in ["centos", "ubi"]):
            funnel_distro = "rhel"
        self.arch = arch
        modified_distro_version = distro_version.replace(".", "")
        modified_arch = self.arch.replace("_", "-")
        if modified_arch == "arm64":
            log.debug(f"Converting arch '{arch}' into 'arm64' for container images")
            modified_arch = "sbsa"
        shipit_distro = f"{funnel_distro}{modified_distro_version}"
        if "tegra" in self.data.product_name:
            shipit_distro = "l4t"
            modified_arch = "aarch64"

        platform_name = (
            f"{shipit_distro}-{self.data.product_name}-linux-{modified_arch}.json"
        )
        shipit_json = (
            f"http://cuda-internal.nvidia.com/funnel/{self.shipit_uuid}/{platform_name}"
        )
        log.info(f"Retrieving funnel json from: {shipit_json}")
        return self.get_http_json(shipit_json)

    def get_shipit_global_json(self):
        global_json = (
            f"http://cuda-internal.nvidia.com/funnel/{self.shipit_uuid}/global.json"
        )
        log.info(f"Retrieving global json from: {global_json}")
        ldata = self.get_http_json(global_json)
        if ldata:
            #  pp(ldata)
            return ldata

    # Returns a unmarshalled json object
    @retry(
        (RequestsRetry),
        tries=HTTP_RETRY_ATTEMPTS,
        delay=HTTP_RETRY_WAIT_SECS,
        logger=log,
    )
    def get_http_json(self, url):
        r = requests.get(url)
        log.debug("response status code %s", r.status_code)
        #  log.debug("response body %s", r.json())
        if r.status_code == 200:
            log.info("http json get successful")
        else:
            raise RequestsRetry()
        return r.json()

    def pkg_rel_from_package_name(self, name, version):
        log.debug(f"have name: {name} version: {version}")
        rgx = re.search(fr"[\w\d-]*{version}-(\d)_?", name)
        if rgx:
            log.debug(f"found match: {rgx.group(1)}")
            return rgx.group(1)
        log.debug("Could not match pkgrel from package name!")

    def shipit_components(self, shipit_json, packages):
        components = {}

        fragments = shipit_json["fragments"]

        def fragment_by_name(name):
            name_with_hyphens = name.replace("_", "-")
            for k, v in fragments.items():
                for k2, v2 in v.items():
                    if any(x in v2["name"] for x in [name, name_with_hyphens]):
                        return v2

        for pkg in packages:
            #  log.debug(f"package: {pkg}")
            fragment = fragment_by_name(pkg)
            if not fragment:
                log.warning(f"{pkg} was not found in the fragments json!")
                continue

            name = fragment["name"]
            version = fragment["version"]

            pkg_rel = self.pkg_rel_from_package_name(name, version)
            if not pkg_rel:
                raise Exception(
                    f"Could not get package release version from package name '{name}' using version '{version}'. Perhaps there is an issue in the RC data?"
                )

            pkg_no_prefix = pkg[len("cuda_") :] if pkg.startswith("cuda_") else pkg

            # rename "devel" to "dev" to keep things consistant with ubuntu
            if "_devel" in pkg_no_prefix:
                pkg_no_prefix = pkg_no_prefix.replace("_devel", "_dev")

            log.debug(
                f"component: {pkg_no_prefix} version: {version} pkg_rel: {pkg_rel}"
            )

            components.update({f"{pkg_no_prefix}": {"version": f"{version}-{pkg_rel}"}})

        return components

    def supported_distros(self):
        """Returns a set of supported distro names for a shipit manifest."""
        distros = set()
        #  pp(self.data)

        # FIXME: hacky WAR, need a better way to define container "flavors"
        if "tegra" in self.data.product_name:
            log.debug("TEGRA DETECTED")
            distros.add("ubuntu1804")
            return distros

        for platform in self.data.targets.items():
            for os in platform[1]:
                if any(x in os for x in SUPPORTED_DISTRO_LIST):
                    distros.add(os)
        return distros

    def supported_distros_by_arch(self, arch):
        sdistros = set()
        larch = arch
        #  log.debug(f"arch: {arch}")
        if "ppc64el" in arch:
            log.debug(f"Setting key '{arch}' to 'ppc64le' for images")
            larch = "ppc64le"
        elif "arm64" in arch:
            # There are three different names for arm64 at nvidia...
            larch = "aarch64"
            if not f"linux-{larch}" in self.data.targets:
                larch = "sbsa"
        #  elif any(f in arch for f in ["arm64", "aarch64"]):
        #      log.debug(f"Setting key '{arch}' to 'sbsa' for images")
        #      larch = "sbsa"
        #  pp(self.data.targets)
        if not f"linux-{larch}" in self.data.targets:
            log.debug(f"'linux-{larch}' not found in shipit data!")
            return
        for distro in self.data.targets[f"linux-{larch}"]:
            if "wsl" in distro:
                continue
            for sdistro in SUPPORTED_DISTRO_LIST:
                if sdistro in ["ubi", "centos"] and "rhel" in distro:
                    sdistros.add("ubi" + distro[len(distro) - 1 :])
                    sdistros.add("centos" + distro[len(distro) - 1 :])
                elif sdistro in distro:
                    sdistros.add(distro)
        return sdistros

    def kitpick_repo_url(self, global_json):
        repo_distro = self.distro
        if any(x in repo_distro for x in ["ubi", "centos"]):
            repo_distro = "rhel"
        clean_distro = "{}{}".format(repo_distro, self.distro_version.replace(".", ""))
        return f"http://cuda-internal.nvidia.com/release-candidates/kitpicks/{self.product_name}/{self.release_label}/{self.candidate_number}/repos/{clean_distro}"

    def generate_shipit_manifest(self, output_path, cudnn_json_path=None):
        # 22:31 Tue Jul 13 2021 FIXME: (jesusa) this function is way too long to be considered good practice in python
        log.debug("Building the shipit manifest")

        self.product_name = self.data["product_name"]
        self.candidate_number = self.data["cand_number"]
        self.release_label = self.data["rel_label"]
        self.distros = self.supported_distros()

        log.info(f"Product Name: '{self.product_name}'")
        log.info(f"Candidate Number: '{self.candidate_number}'")
        log.info(f"Release label: {self.release_label}")

        reldata = {}
        for plat, distros in self.data["targets"].items():
            if "windows" in plat:
                continue
            log.debug(f"platform: {plat}")
            splat = plat.split("-")
            if len(splat) > 2 or len(splat) <= 1:
                # At the moment, platforms needed by cuda image only contain a name and arch separated by a single hyphen
                continue
            os, arch = splat[0], splat[1]
            if any(a in arch for a in ["aarch64", "sbsa"]):
                log.debug(f"Converting arch '{arch}' into 'arm64' for container images")
                arch = "arm64"
            if not os in reldata:
                reldata[os] = {}
            if not arch in reldata[os]:
                reldata[os][arch] = {}
            reldata[os][arch]["distros"] = self.supported_distros_by_arch(arch)

        if output_path.exists:
            log.warning(f"Removing path '{output_path}'")
            rm["-rf", output_path]()

        output_path.mkdir(parents=True, exist_ok=False)
        self.output_manifest_path = pathlib.Path(f"{output_path}/manifest.yml")

        release_key = f"cuda_v{self.release_label}"
        self.shipit_manifest = {
            release_key: {
                "dist_base_path": output_path.as_posix(),
                "push_repos": ["artifactory"],
            }
        }

        #  pp(self.data.targets)
        #  pp(reldata)
        #  log.debug(f"reldata: {pp(reldata)}")

        #
        # FIXME: find a better way to do this!
        #
        #        Move this function to the parent class!
        #
        def nested_keys(data):
            for k, v in data.items():
                if isinstance(v, dict):
                    for pair in nested_keys(v):
                        yield (k, *pair)
                else:
                    if "distros" in k:
                        yield ([v])
                    else:
                        yield (k, v)

        manifest = DotDict()
        for platform in nested_keys(reldata):
            log.info(f"Inspecting global.json platform: {platform}")
            #  continue
            os = platform[0]
            self.arch = platform[1]
            distros = platform[2]
            if "tegra" in self.product_name and not "arm64" in self.arch:
                log.warning(
                    f"Skipping platform! '{self.arch}' is not supported for L4T Cuda Container Images (yet)"
                )
                continue

            for distro in distros:
                rgx = re.search(r"(\D*)(\d*)", distro)
                if rgx:
                    self.distro = rgx.group(1)
                    self.distro_version = rgx.group(2).replace("04", ".04")
                else:
                    raise UnknownCudaRCDistro("Distro '{distro}' has an unknown format")

                platform = f"{self.distro}{self.distro_version}"
                if "tegra" in self.product_name:
                    platform = "l4t"
                    if not cudnn_json_path:
                        log.error("Argument `--cudnn-json-path` is not set!")
                        sys.exit(1)

                #  print(platform)
                #  continue
                #  self.set_output_path(platform)

                #  if delete and output_path.exists:
                #      #  raise
                #      log.warning(f"Removing path '{output_path}'")
                #      rm["-rf", output_path]()
                #  platform = f"{target}-{self.arch}"

                if "tegra" in self.product_name:
                    platform = f"{platform}-cuda"
                self.output_path = pathlib.Path(f"{output_path}/{platform}")

                sjson = self.get_shipit_funnel_json(
                    self.distro, self.distro_version, self.arch
                )

                pkgs = utils.template_packages(self.distro)

                log.debug(f"template packages: {pkgs}")
                components = self.shipit_components(sjson, pkgs)

                # TEMP WAR: populate cudnn component for L4T
                if "l4t" in platform:
                    cudnn_comp = {
                        "cudnn8": {
                            "version": "",
                            "source": "",
                            "dev": {"source": "", "md5sum": ""},
                        }
                    }
                    log.debug(f"cudnn_json_path: {cudnn_json_path}")
                    with open(pathlib.Path(cudnn_json_path), "r") as f:
                        cudnn = json.loads(f.read())
                    for x in cudnn:
                        artpath = f"https://urm.nvidia.com/artifactory/{x['repo']}/{x['path']}/{x['name']}"
                        if "arm64" in x["name"]:
                            if "-dev_" in x["name"]:
                                #  cudnn_comp["cudnn8"]["dev"]["version"] = x["version"]
                                cudnn_comp["cudnn8"]["dev"]["source"] = artpath
                                cudnn_comp["cudnn8"]["dev"]["md5sum"] = x["actual_md5"]
                            else:
                                cudnn_comp["cudnn8"]["version"] = x["version"]
                                cudnn_comp["cudnn8"]["source"] = artpath
                                cudnn_comp["cudnn8"]["md5sum"] = x["actual_md5"]
                    if cudnn_comp:
                        #  print(cudnn_comp)
                        components.update(cudnn_comp)

                image_name = "gitlab-master.nvidia.com:5005/cuda-installer/cuda/release-candidate/cuda"
                template_path = "templates/ubuntu"
                if "ubuntu" not in self.distro:
                    template_path = "templates/redhat"
                #  if all(x in self.product_name for x in ["tegra", "10-2"]):
                #      template_path = "templates/ubuntu/legacy"
                #  if not "x86_64" in self.arch:
                #      image_name = f"gitlab-master.nvidia.com:5005/cuda-installer/cuda/release-candidate/cuda"
                base_image = f"{self.distro}:{self.distro_version}"
                if "ubi" in self.distro:
                    base_image = f"registry.access.redhat.com/ubi{self.distro_version}/ubi:latest"
                requires = ""

                key = "push_repos"
                if "tegra" in self.product_name:
                    key = "l4t_push_repos"
                prepos = utils.load_rc_push_repos_manifest_yaml()[key]
                if not self.push_repo_logged_in:
                    # only need to do this once
                    utils.auth_registries(prepos)
                    self.push_repo_logged_in = True

                if "tegra" in self.product_name:
                    if not self.l4t_base_image:
                        self.l4t_base_image = utils.latest_l4t_base_image()
                    base_image = self.l4t_base_image
                    requires = "cuda>=10.2"
                    image_name = (
                        f"gitlab-master.nvidia.com:5005/cuda-installer/cuda/l4t-cuda"
                    )

                self.shipit_manifest["push_repos"] = prepos
                manifest = self.shipit_manifest[release_key]
                manifest["image_name"] = image_name
                if not platform in manifest:
                    manifest[platform] = {
                        "base_image": base_image,
                        "image_tag_suffix": f"-{self.data['cand_number']}",
                        "template_path": template_path,
                        "repo_url": self.kitpick_repo_url(self.data),
                    }

                manifest[platform][f"{self.arch}"] = {
                    "requires": requires,
                    "components": components,
                }

        if not manifest:
            log.warning(
                "No manifest to write after parsing Shipit data. Unsupported kitpick as it doesn't contain anything useful for Cuda Image!"
            )
            sys.exit(155)

        self.shipit_manifest[release_key] = manifest
        log.info(f"Writing shipit manifest: {self.output_manifest_path}")
        self.generate_shipit_manifest_from_manifest(self.shipit_manifest)
        #  pp(self.shipit_manifest)
        #  sys.exit(1)

    def generate_shipit_manifest_from_manifest(self, manifest):
        yaml_str = yaml.dump(manifest)
        with open(self.output_manifest_path, "w") as f:
            f.write(yaml_str)
