#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${IMAGE_TAG_SUFFIX}"

major=$(echo $CUDA_VERSION | cut -f1 -d.)
minor=$(echo $CUDA_VERSION | cut -f2 -d.)
rev=$(echo $CUDA_VERSION | cut -f3 -d.)

function setup() {
    check_runtime
}

@test "check_multiple_cuda_directories" {
    # There can be only one...
    # If a wrong dependency version is selected for a different cuda version, it will pull in other packages and install to a
    # different cuda version. We only want one cuda version in the images
    docker pull --platform linux/${ARCH} ${image}
    local num=2

    #
    # A different alternatives structure in /usr/local/ for cuda is used on...
    #
    # - 11.3.1 and greater for all distros
    # - 11.3.0 for ubuntu and ubi (redhat)
    #
    if ([[ "11.3.1" == "${major}.${minor}.${rev}" ]] || ([[ ${major} -eq 11 ]] && [[ ${minor} -gt 3 ]])) || \
       ([[ "11.3.0" == "${major}.${minor}.${rev}" ]] && ([[ "${OS_NAME}" == "ubuntu" ]] || [[ "${OS_NAME}" == "ubi" ]] || [[ "${OS_NAME}" == "centos" ]])); then
        num=3
    fi

    debug "num = ${num}"
    docker_run --rm --gpus 0 --platform linux/${ARCH} ${image} bash -c "[[ \$(ls -l /usr/local/ | grep cuda | wc -l) == ${num} ]] || false"
    [ "$status" -eq 0 ]
}
