ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.0-runtime-ubi7 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 7.6.5.32
ENV NV_CUDNN_PACKAGE libcudnn7-${NV_CUDNN_VERSION}.cuda9.0

ENV NV_CUDNN_DL_SHA256SUM bd0a4c0090d5b02feec3f195738968690cc2470b9bc6026e6fe8ff245cd261c8
ENV NV_CUDNN_DL_BASENAME cudnn-9.0-linux-x64-v7.6.5.32.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.5/${NV_CUDNN_DL_BASENAME}

FROM base as base-ppc64le

ENV NV_CUDNN_VERSION 7.2.1.38
ENV NV_CUDNN_PACKAGE libcudnn7-${NV_CUDNN_VERSION}.cuda9.0

ENV NV_CUDNN_DL_SHA256SUM 4c0937b5618cb0d1d7eed195b3a4ba6a49e061f9e734f5702b030c8522cdfc9c
ENV NV_CUDNN_DL_BASENAME cudnn-9.0-linux-ppc64le-v7.2.1.38.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v7.2.1/${NV_CUDNN_DL_BASENAME}

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
