ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-runtime-ubi7 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 8.0.5.39-1
ENV NV_CUDNN_PACKAGE libcudnn8-${NV_CUDNN_VERSION}.cuda10.1


FROM base as base-ppc64le

ENV NV_CUDNN_VERSION 8.0.5.39-1
ENV NV_CUDNN_PACKAGE libcudnn8-${NV_CUDNN_VERSION}.cuda10.1


FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION ${NV_CUDNN_VERSION}
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN yum install -y \
    ${NV_CUDNN_PACKAGE} \
    && yum clean all \
    && rm -rf /var/cache/yum/*

