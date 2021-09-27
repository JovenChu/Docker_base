ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.3.1-devel-ubuntu20.04 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 8.2.0.53

ENV NV_CUDNN_PACKAGE "libcudnn8=$NV_CUDNN_VERSION-1+cuda11.3"
ENV NV_CUDNN_PACKAGE_DEV "libcudnn8-dev=$NV_CUDNN_VERSION-1+cuda11.3"
ENV NV_CUDNN_PACKAGE_NAME "libcudnn8"

FROM base as base-arm64

ENV NV_CUDNN_VERSION 8.2.0.53

ENV NV_CUDNN_PACKAGE "libcudnn8=$NV_CUDNN_VERSION-1+cuda11.3"
ENV NV_CUDNN_PACKAGE_DEV "libcudnn8-dev=$NV_CUDNN_VERSION-1+cuda11.3"
ENV NV_CUDNN_PACKAGE_NAME "libcudnn8"

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"
LABEL com.nvidia.cudnn.version="${NV_CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ${NV_CUDNN_PACKAGE} \
    ${NV_CUDNN_PACKAGE_DEV} \
    && apt-mark hold ${NV_CUDNN_PACKAGE_NAME} && \
    rm -rf /var/lib/apt/lists/*
