#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    docker pull --platform linux/${ARCH} ${image}
    check_runtime
}

@test "check_architecture" {
    narch=${ARCH}
    if [[ ${ARCH} == "arm64" ]]; then
        narch="aarch64"
    fi
    docker_run --rm --gpus 0 --env narch=${narch} --platform linux/${ARCH} ${image} bash -c '[[ "$(uname -m)" == "${narch}" ]] || false'
    [ "$status" -eq 0 ]
}
