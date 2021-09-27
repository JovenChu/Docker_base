ARG IMAGE_NAME
FROM ${IMAGE_NAME}:8.0-runtime-ubi7 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 6.0.21
ENV NV_CUDNN_PACKAGE libcudnn6-${NV_CUDNN_VERSION}.cuda8.0

ENV NV_CUDNN_DL_SHA256SUM 9b09110af48c9a4d7b6344eb4b3e344daa84987ed6177d5c44319732f3bb7f9c
ENV NV_CUDNN_DL_BASENAME cudnn-8.0-linux-x64-v6.0.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v6.0/${NV_CUDNN_DL_BASENAME}

FROM base as base-ppc64le

ENV NV_CUDNN_VERSION 6.0.21
ENV NV_CUDNN_PACKAGE libcudnn6-${NV_CUDNN_VERSION}.cuda8.0

ENV NV_CUDNN_DL_SHA256SUM bb32b7eb8bd1edfd63b39fb8239bba2e9b4d0b3b262043a5c6b41fa1ea1c1472
ENV NV_CUDNN_DL_BASENAME cudnn-8.0-linux-ppc64le-v6.0.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v6.0/${NV_CUDNN_DL_BASENAME}

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
