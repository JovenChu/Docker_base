ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.2.1-base-ubuntu16.04 as base

ENV NV_CUDA_LIB_VERSION 11.2.1-1

FROM base as base-amd64

ENV NV_NVTX_VERSION 11.2.67-1
ENV NV_LIBNPP_VERSION 11.3.2.139-1
ENV NV_LIBNPP_PACKAGE libnpp-11-2=${NV_LIBNPP_VERSION}
ENV NV_LIBCUSPARSE_VERSION 11.4.0.135-1

ENV NV_LIBCUBLAS_PACKAGE_NAME libcublas-11-2
ENV NV_LIBCUBLAS_VERSION 11.4.1.1026-1
ENV NV_LIBCUBLAS_PACKAGE ${NV_LIBCUBLAS_PACKAGE_NAME}=${NV_LIBCUBLAS_VERSION}

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-2=${NV_CUDA_LIB_VERSION} \
    ${NV_LIBNPP_PACKAGE} \
    cuda-nvtx-11-2=${NV_NVTX_VERSION} \
    libcusparse-11-2=${NV_LIBCUSPARSE_VERSION} \
    ${NV_LIBCUBLAS_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_PACKAGE_NAME}