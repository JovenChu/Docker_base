ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.1-runtime-ubi7 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 7.1.2
ENV NV_CUDNN_PACKAGE libcudnn7-${NV_CUDNN_VERSION}.cuda9.1

ENV NV_CUDNN_DL_SHA256SUM c61000ed700bc5a009bc2e135bbdf736c9743212b2174a2fc9018a66cc0979ec
ENV NV_CUDNN_DL_BASENAME cudnn-9.1-linux-x64-v7.1.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v7.1.2/${NV_CUDNN_DL_BASENAME}

FROM base as base-ppc64le

ENV NV_CUDNN_VERSION 7.0.5
ENV NV_CUDNN_PACKAGE libcudnn7-${NV_CUDNN_VERSION}.cuda9.1

ENV NV_CUDNN_DL_SHA256SUM 68834ffe96c91fa1b13517a4b5b0358f8433ed2d30f146b7bb41dd0ea50c55ce
ENV NV_CUDNN_DL_BASENAME cudnn-9.1-linux-ppc64le-v7.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v7.0.5/${NV_CUDNN_DL_BASENAME}

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
