ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.4.0-devel-centos8 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 8.2.4.15-1
ENV NV_CUDNN_PACKAGE libcudnn8-devel-${NV_CUDNN_VERSION}.cuda11.4

FROM base as base-arm64

ENV NV_CUDNN_VERSION 8.2.4.15-1
ENV NV_CUDNN_PACKAGE libcudnn8-devel-${NV_CUDNN_VERSION}.cuda11.4

FROM base as base-ppc64le

ENV NV_CUDNN_VERSION 8.2.4.15-1
ENV NV_CUDNN_PACKAGE libcudnn8-devel-${NV_CUDNN_VERSION}.cuda11.4

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

LABEL com.nvidia.cudnn.version="${NV_CUDNN_VERSION}"

RUN yum install -y ${NV_CUDNN_PACKAGE} \
    && yum clean all \
    && rm -rf /var/cache/yum/*