#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    docker pull ${image}
    check_runtime
}

# TODO (jesusa): re-enable this test once we have the a better way to detect which nccl version should be installed
# @test "check_libnccl_installed" {
#     unsupported=('11.2.0-devel-ubuntu16.04', '11.2.1-devel-ubuntu16.04', '11.2.2-devel-ubuntu16.04')
#     image_name=$(echo "${image}" | cut -d: -f3)
#     if printf '%s' "${unsupported[@]}" | grep -q "${image_name}"; then
#         skip "libnccl2 not supported for this platform"
#     fi
#     local CMD="dpkg --get-selections | grep nccl"
#     if [[ "${OS_NAME}" == "centos" ]] || [[ "${OS_NAME}" == "centos" ]]; then
#         local CMD="rpm -qa | grep nccl"
#     fi
#     docker_run --rm --gpus 0 ${image} bash -c "$CMD"
#     [ "$status" -eq 0 ]
# }
