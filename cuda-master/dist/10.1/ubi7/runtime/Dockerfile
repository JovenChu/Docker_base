ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-base-ubi7 as base

FROM base as base-amd64

ENV NV_CUDA_LIB_VERSION 10.1.243-1
ENV NV_NVTX_VERSION 10.1.243-1
ENV NV_LIBNPP_VERSION 10.1.243-1

ENV NV_LIBCUBLAS_PACKAGE_NAME libcublas10
ENV NV_LIBCUBLAS_VERSION 10.2.1.243-1
ENV NV_LIBCUBLAS_PACKAGE ${NV_LIBCUBLAS_PACKAGE_NAME}-${NV_LIBCUBLAS_VERSION}

ENV NV_LIBNCCL_DL_BASENAME nccl_2.8.4-1+cuda10.1_x86_64.txz
ENV NV_LIBNCCL_DL_SHA256SUM bcff1cf98e4b24d7ca189577a9d909980d8df88075223d70dc4638e428c53f84
ENV NV_LIBNCCL_DL_SOURCE https://developer.download.nvidia.com/compute/redist/nccl/v2.8/nccl_2.8.4-1+cuda10.1_x86_64.txz
FROM base as base-ppc64le

ENV NV_CUDA_LIB_VERSION 10.1.243-1
ENV NV_NVTX_VERSION 10.1.243-1
ENV NV_LIBNPP_VERSION 10.1.243-1

ENV NV_LIBCUBLAS_PACKAGE_NAME libcublas10
ENV NV_LIBCUBLAS_VERSION 10.2.1.243-1
ENV NV_LIBCUBLAS_PACKAGE ${NV_LIBCUBLAS_PACKAGE_NAME}-${NV_LIBCUBLAS_VERSION}

ENV NV_LIBNCCL_DL_BASENAME nccl_2.8.4-1+cuda10.1_ppc64le.txz
ENV NV_LIBNCCL_DL_SHA256SUM 72e587b4029188616c20113fae867a9d1ab50cac529640f9d4fefa55ea33a3cf
ENV NV_LIBNCCL_DL_SOURCE https://developer.download.nvidia.com/compute/redist/nccl/v2.8/nccl_2.8.4-1+cuda10.1_ppc64le.txz

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

# setopt flag prevents yum from auto upgrading. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN yum install --setopt=obsoletes=0 -y \
    cuda-libraries-10-1-${NV_CUDA_LIB_VERSION} \
    cuda-nvtx-10-1-${NV_NVTX_VERSION} \
    cuda-npp-10-1-${NV_LIBNPP_VERSION} \
    ${NV_LIBCUBLAS_PACKAGE} \
    && yum clean all \
    && rm -rf /var/cache/yum/*

RUN yum install -y xz && NCCL_DOWNLOAD_SUM=${NV_LIBNCCL_DL_SHA256SUM} \
    && curl -fsSL ${NV_LIBNCCL_DL_SOURCE} -O \
    && echo "$NCCL_DOWNLOAD_SUM  ${NV_LIBNCCL_DL_BASENAME}" | sha256sum -c - \
    && unxz ${NV_LIBNCCL_DL_BASENAME} \
    && tar --no-same-owner --keep-old-files -xvf "${NV_LIBNCCL_DL_BASENAME:0:-4}.tar" -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so.*' \
    && tar --no-same-owner --keep-old-files -xvf  "${NV_LIBNCCL_DL_BASENAME:0:-4}.tar" -C /usr/lib64/pkgconfig/ --strip-components=3 --wildcards '*/lib/pkgconfig/*' \
    && rm -f "${NV_LIBNCCL_DL_BASENAME:0:-4}.tar" \
    && ldconfig \
    && yum clean all \
    && rm -rf /var/cache/yum/*
