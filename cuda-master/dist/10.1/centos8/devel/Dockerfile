ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-runtime-centos8 as base

FROM base as base-amd64

ENV NV_CUDA_LIB_VERSION 10.1.243-1
ENV NV_NVPROF_VERSION 10.1.243-1
ENV NV_CUDA_CUDART_DEV_VERSION 10.1.243-1
ENV NV_NVML_DEV_VERSION 10.1.243-1

ENV NV_LIBNPP_DEV_VERSION 10.1.243-1

ENV NV_LIBCUBLAS_DEV_PACKAGE_NAME libcublas-devel
ENV NV_LIBCUBLAS_DEV_VERSION 10.2.1.243-1
ENV NV_LIBCUBLAS_DEV_PACKAGE ${NV_LIBCUBLAS_DEV_PACKAGE_NAME}-${NV_LIBCUBLAS_DEV_VERSION}

ENV NV_LIBNCCL_DL_BASENAME nccl_2.8.4-1+cuda10.1_x86_64.txz
ENV NV_LIBNCCL_DL_SHA256SUM bcff1cf98e4b24d7ca189577a9d909980d8df88075223d70dc4638e428c53f84
ENV NV_LIBNCCL_DL_SOURCE https://developer.download.nvidia.com/compute/redist/nccl/v2.8/nccl_2.8.4-1+cuda10.1_x86_64.txz


LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"


# setopt flag prevents yum from auto upgrading. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN yum install --setopt=obsoletes=0 -y \
    make \
    cuda-nvml-dev-10-1-${NV_NVML_DEV_VERSION} \
    cuda-command-line-tools-10-1-${NV_CUDA_LIB_VERSION} \
    cuda-cudart-dev-10-1-${NV_CUDA_CUDART_DEV_VERSION} \
    cuda-libraries-dev-10-1-${NV_CUDA_LIB_VERSION} \
    cuda-minimal-build-10-1-${NV_CUDA_LIB_VERSION} \
    cuda-nvprof-10-1-${NV_NVPROF_VERSION} \
    cuda-npp-dev-10-1-${NV_LIBNPP_DEV_VERSION} \
    ${NV_LIBCUBLAS_DEV_PACKAGE} \
    && yum clean all \
    && rm -rf /var/cache/yum/*

RUN yum install -y yum-plugin-versionlock && yum versionlock ${NV_LIBCUBLAS_PACKAGE_NAME_DEV}

RUN yum install -y xz && NCCL_DOWNLOAD_SUM=${NV_LIBNCCL_DL_SHA256SUM} && \
    curl -fsSL ${NV_LIBNCCL_DL_SOURCE} -O && \
    echo "$NCCL_DOWNLOAD_SUM  ${NV_LIBNCCL_DL_BASENAME}" | sha256sum -c - && \
    unxz ${NV_LIBNCCL_DL_BASENAME} && \
    tar --no-same-owner --keep-old-files -xvf "${NV_LIBNCCL_DL_BASENAME:0:-4}.tar" -C /usr/local/cuda/include/ --strip-components=2 --wildcards '*/include/*' && \
    tar --no-same-owner --keep-old-files -xvf "${NV_LIBNCCL_DL_BASENAME:0:-4}.tar" -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so' && \
    rm -f "${NV_LIBNCCL_DL_BASENAME:0:-4}.tar" && \
    ldconfig

