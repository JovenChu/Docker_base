ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.2-devel-ubuntu18.04 as base

FROM base as base-amd64

ENV NV_CUDNN_PACKAGE_VERSION 7.6.5.32-1
ENV NV_CUDNN_VERSION 7.6.5.32

ENV NV_CUDNN_PACKAGE_NAME libcudnn7
ENV NV_CUDNN_PACKAGE ${NV_CUDNN_PACKAGE_NAME}=${NV_CUDNN_PACKAGE_VERSION}+cuda9.2
ENV NV_CUDNN_PACKAGE_DEV ${NV_CUDNN_PACKAGE_NAME}-dev=${NV_CUDNN_PACKAGE_VERSION}+cuda9.2

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION ${NV_CUDNN_VERSION}

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ${NV_CUDNN_PACKAGE} \
    ${NV_CUDNN_PACKAGE_DEV} \
    && apt-mark hold ${NV_CUDNN_PACKAGE_NAME} && \
    rm -rf /var/lib/apt/lists/*