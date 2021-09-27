ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.1.1-runtime-centos7 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 8.0.5.39-1
ENV NV_CUDNN_PACKAGE libcudnn8-${NV_CUDNN_VERSION}.cuda11.1

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

LABEL com.nvidia.cudnn.version="${NV_CUDNN_VERSION}"

RUN yum install -y ${NV_CUDNN_PACKAGE} \
    && yum clean all \
    && rm -rf /var/cache/yum/*