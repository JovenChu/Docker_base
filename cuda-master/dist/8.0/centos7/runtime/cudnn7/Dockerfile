ARG IMAGE_NAME
FROM ${IMAGE_NAME}:8.0-runtime-centos7 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 7.1.2.21
ENV NV_CUDNN_PACKAGE libcudnn7-${NV_CUDNN_VERSION}.cuda8.0

ENV NV_CUDNN_DL_SHA256SUM a5dfd656811fe9c43d87c40338cec5e1a85ad5a9cd3b5f1e95dd67d5e126aacc
ENV NV_CUDNN_DL_BASENAME cudnn-8.0-linux-x64-v7.1.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v7.1.2/${NV_CUDNN_DL_BASENAME}

FROM base as base-ppc64le

ENV NV_CUDNN_VERSION 7.0.2.38
ENV NV_CUDNN_PACKAGE libcudnn7-${NV_CUDNN_VERSION}.cuda8.0

ENV NV_CUDNN_DL_SHA256SUM 7bc1452c9ac5ab4fda03e3226c83202c6c85431e2a3a51dce67ac0da6ffa45a8
ENV NV_CUDNN_DL_BASENAME cudnn-8.0-linux-ppc64le-v7.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v7.0.2/${NV_CUDNN_DL_BASENAME}

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
