ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.2-base-ubuntu16.04 as base

FROM base as base-amd64

ENV NV_CUDA_LIB_VERSION 9.2.148-1
ENV NV_NVTX_VERSION 9.2.148-1
ENV NV_LIBNPP_VERSION 9.2.148-1
ENV NV_LIBCUSPARSE_VERSION 9.2.148-1


ENV NV_LIBCUBLAS_PACKAGE_NAME cuda-cublas-9-2

ENV NV_LIBCUBLAS_VERSION 9.2.148-1
ENV NV_LIBCUBLAS_PACKAGE ${NV_LIBCUBLAS_PACKAGE_NAME}=${NV_LIBCUBLAS_VERSION}


ENV NV_LIBNCCL_PACKAGE_NAME "libnccl2"
ENV NV_LIBNCCL_PACKAGE_VERSION 2.4.8-1
ENV NCCL_VERSION 2.4.8
ENV NV_LIBNCCL_PACKAGE ${NV_LIBNCCL_PACKAGE_NAME}=${NV_LIBNCCL_PACKAGE_VERSION}+cuda9.2
FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-9-2=${NV_CUDA_LIB_VERSION} \
    cuda-npp-9-2=${NV_LIBNPP_VERSION} \
    cuda-nvtx-9-2=${NV_NVTX_VERSION} \
    cuda-cusparse-9-2=${NV_LIBCUSPARSE_VERSION} \
    ${NV_LIBCUBLAS_PACKAGE} \
    ${NV_LIBNCCL_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBNCCL_PACKAGE_NAME} ${NV_LIBCUBLAS_PACKAGE_NAME}