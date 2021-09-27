ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.2-runtime-ubuntu18.04 as base

FROM base as base-amd64

ENV NV_CUDA_LIB_VERSION 9.2.148-1
ENV NV_CUDA_CUDART_DEV_VERSION 9.2.148-1
ENV NV_NVML_DEV_VERSION 9.2.148-1
ENV NV_LIBCUSPARSE_DEV_VERSION 9.2.148-1
ENV NV_LIBNPP_DEV_VERSION 9.2.148-1
ENV NV_LIBCUBLAS_DEV_PACKAGE_NAME cuda-cublas-dev-9-2

ENV NV_LIBCUBLAS_DEV_VERSION 9.2.148-1
ENV NV_LIBCUBLAS_DEV_PACKAGE ${NV_LIBCUBLAS_DEV_PACKAGE_NAME}=${NV_LIBCUBLAS_DEV_VERSION}

ENV NV_LIBNCCL_DEV_PACKAGE_NAME libnccl-dev
ENV NV_LIBNCCL_DEV_VERSION 2.4.8-1
ENV NCCL_VERSION ${NV_LIBNCCL_DEV_VERSION}
ENV NV_LIBNCCL_DEV_PACKAGE ${NV_LIBNCCL_DEV_PACKAGE_NAME}=${NV_LIBNCCL_DEV_VERSION}+cuda9.2


FROM base-${TARGETARCH}

ARG TARGETARCH
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-nvml-dev-9-2=${NV_NVML_DEV_VERSION} \
    cuda-command-line-tools-9-2=${NV_CUDA_LIB_VERSION} \
    cuda-nvprof-9-2=${NV_CUDA_LIB_VERSION} \
    cuda-npp-dev-9-2=${NV_LIBNPP_DEV_VERSION} \
    cuda-libraries-dev-9-2=${NV_CUDA_LIB_VERSION} \
    cuda-minimal-build-9-2=${NV_CUDA_LIB_VERSION} \
    ${NV_LIBCUBLAS_DEV_PACKAGE} \
    ${NV_LIBNCCL_DEV_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_DEV_PACKAGE_NAME} ${NV_LIBNCCL_DEV_PACKAGE_NAME}

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs