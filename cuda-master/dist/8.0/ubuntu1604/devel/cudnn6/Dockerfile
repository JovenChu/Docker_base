ARG IMAGE_NAME
FROM ${IMAGE_NAME}:8.0-devel-ubuntu16.04 as base

FROM base as base-amd64

ENV NV_CUDNN_PACKAGE_VERSION 6.0.21-1
ENV NV_CUDNN_VERSION 6.0.21

ENV NV_CUDNN_PACKAGE_NAME libcudnn6
ENV NV_CUDNN_PACKAGE ${NV_CUDNN_PACKAGE_NAME}=${NV_CUDNN_PACKAGE_VERSION}+cuda8.0
ENV NV_CUDNN_PACKAGE_DEV ${NV_CUDNN_PACKAGE_NAME}-dev=${NV_CUDNN_PACKAGE_VERSION}+cuda8.0

FROM base as base-ppc64le

ENV NV_CUDNN_PACKAGE_VERSION 6.0.21-1
ENV NV_CUDNN_VERSION 6.0.21

ENV NV_CUDNN_PACKAGE_NAME libcudnn6
ENV NV_CUDNN_PACKAGE ${NV_CUDNN_PACKAGE_NAME}=${NV_CUDNN_PACKAGE_VERSION}+cuda8.0
ENV NV_CUDNN_PACKAGE_DEV ${NV_CUDNN_PACKAGE_NAME}-dev=${NV_CUDNN_PACKAGE_VERSION}+cuda8.0

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/${NVARCH} /" > /etc/apt/sources.list.d/nvidia-ml.list

ENV CUDNN_VERSION ${NV_CUDNN_VERSION}

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ${NV_CUDNN_PACKAGE} \
    ${NV_CUDNN_PACKAGE_DEV} \
    && apt-mark hold ${NV_CUDNN_PACKAGE_NAME} && \
    rm -rf /var/lib/apt/lists/*