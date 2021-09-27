ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-devel-centos8 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 7.6.5.32
ENV NV_CUDNN_PACKAGE libcudnn7-devel-${NV_CUDNN_VERSION}.cuda10.1

ENV NV_CUDNN_DL_SHA256SUM 7eaec8039a2c30ab0bc758d303588767693def6bf49b22485a2c00bf2e136cb3
ENV NV_CUDNN_DL_BASENAME cudnn-10.1-linux-x64-v7.6.5.32.tgz
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
