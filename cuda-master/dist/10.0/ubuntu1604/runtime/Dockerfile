ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.0-base-ubuntu16.04 as base

FROM base as base-amd64

ENV NV_CUDA_LIB_VERSION 10.0.130-1
ENV NV_NVTX_VERSION 10.0.130-1
ENV NV_LIBNPP_VERSION 10.0.130-1
ENV NV_LIBCUSPARSE_VERSION 10.0.130-1


ENV NV_LIBCUBLAS_PACKAGE_NAME cuda-cublas-10-0

ENV NV_LIBCUBLAS_VERSION 10.0.130-1
ENV NV_LIBCUBLAS_PACKAGE ${NV_LIBCUBLAS_PACKAGE_NAME}=${NV_LIBCUBLAS_VERSION}


ENV NV_LIBNCCL_PACKAGE_NAME "libnccl2"
ENV NV_LIBNCCL_PACKAGE_VERSION 2.6.4-1
ENV NCCL_VERSION 2.6.4
ENV NV_LIBNCCL_PACKAGE ${NV_LIBNCCL_PACKAGE_NAME}=${NV_LIBNCCL_PACKAGE_VERSION}+cuda10.0
FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-10-0=${NV_CUDA_LIB_VERSION} \
    cuda-npp-10-0=${NV_LIBNPP_VERSION} \
    cuda-nvtx-10-0=${NV_NVTX_VERSION} \
    cuda-cusparse-10-0=${NV_LIBCUSPARSE_VERSION} \
    ${NV_LIBCUBLAS_PACKAGE} \
    ${NV_LIBNCCL_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBNCCL_PACKAGE_NAME} ${NV_LIBCUBLAS_PACKAGE_NAME}