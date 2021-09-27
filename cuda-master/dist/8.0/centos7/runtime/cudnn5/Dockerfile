ARG IMAGE_NAME
FROM ${IMAGE_NAME}:8.0-runtime-centos7 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 5.1.10
ENV NV_CUDNN_PACKAGE libcudnn5-${NV_CUDNN_VERSION}.cuda8.0

ENV NV_CUDNN_DL_SHA256SUM c10719b36f2dd6e9ddc63e3189affaa1a94d7d027e63b71c3f64d449ab0645ce
ENV NV_CUDNN_DL_BASENAME cudnn-8.0-linux-x64-v5.1.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/${NV_CUDNN_DL_BASENAME}

FROM base as base-ppc64le

ENV NV_CUDNN_VERSION 5.1.10
ENV NV_CUDNN_PACKAGE libcudnn5-${NV_CUDNN_VERSION}.cuda8.0

ENV NV_CUDNN_DL_SHA256SUM 663aac0328f821d90ae9c74ee43e90751706546c2ce769ea9c96f92864300af6
ENV NV_CUDNN_DL_BASENAME cudnn-8.0-linux-ppc64le-v5.1.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/${NV_CUDNN_DL_BASENAME}

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION ${NV_CUDNN_VERSION}
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"


# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN curl -fsSL ${NV_CUDNN_DL_URL} -O && \
    echo "${NV_CUDNN_DL_SHA256SUM}  ${NV_CUDNN_DL_BASENAME}" | sha256sum -c - && \
    gunzip ${NV_CUDNN_DL_BASENAME} && \
    tar --no-same-owner -xf ${NV_CUDNN_DL_BASENAME:0:-4}.tar -C /usr/local ${NV_CUDNN_DL_RUNTIME_EXTRACT_ARG} && \
    rm ${NV_CUDNN_DL_BASENAME:0:-4}.tar && \
    ldconfig
