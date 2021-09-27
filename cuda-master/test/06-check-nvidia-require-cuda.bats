#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    docker pull --platform linux/${ARCH} ${image}
    check_runtime
}

@test "check_NVIDIA_REQUIRES_CUDA" {
    # The devel images for x86_64 should always contain "brand=tesla"
    if [ ${ARCH} != "x86_64" ]; then
       skip "Only needed on x86_64."
    fi
    unsupported=('8.0', '9.0', '9.1', '9.2')
    debug "cuda_version: ${CUDA_VERSION}"
    debug "unsupported: $(printf '%s' \"${unsupported[@]}\")"
    if printf '%s' "${unsupported[@]}" | grep -q "${CUDA_VERSION}"; then
        skip "NVIDIA_REQUIRE_CUDA not supported for this CUDA version"
    fi
    docker_run --rm --gpus 0 --platform linux/${ARCH} ${image} bash -c "printenv | grep -q 'brand=tesla'"
    [ "$status" -eq 0 ]
}
