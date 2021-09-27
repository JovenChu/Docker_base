ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.2-devel-centos7 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 7.6.5.32
ENV NV_CUDNN_PACKAGE libcudnn7-devel-${NV_CUDNN_VERSION}.cuda9.2

ENV NV_CUDNN_DL_SHA256SUM a2a2c7a8ba7b16d323b651766ee37dcfdbc2b50d920f73f8fde85005424960e4
ENV NV_CUDNN_DL_BASENAME cudnn-9.2-linux-x64-v7.6.5.32.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.5/${NV_CUDNN_DL_BASENAME}

FROM base as base-ppc64le

ENV NV_CUDNN_VERSION 7.6.5.32
ENV NV_CUDNN_PACKAGE libcudnn7-devel-${NV_CUDNN_VERSION}.cuda9.2

ENV NV_CUDNN_DL_SHA256SUM a11f44f9a827b7e69f527a9d260f1637694ff7c1674a3e46bd9ec054a08f9a76
ENV NV_CUDNN_DL_BASENAME cudnn-9.2-linux-ppc64le-v7.6.5.32.tgz
ENV NV_CUDNN_DL_URL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.5/${NV_CUDNN_DL_BASENAME}

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
