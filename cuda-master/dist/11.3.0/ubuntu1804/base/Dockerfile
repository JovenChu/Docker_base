FROM ubuntu:18.04 as base

FROM base as base-amd64

ENV NVARCH x86_64
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.3 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 driver>=450"
ENV NV_CUDA_CUDART_VERSION 11.3.58-1
ENV NV_CUDA_COMPAT_PACKAGE cuda-compat-11-3

ENV NV_ML_REPO_ENABLED 1
ENV NV_ML_REPO_URL https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/${NVARCH}

FROM base as base-arm64

ENV NVARCH sbsa
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.3"
ENV NV_CUDA_CUDART_VERSION 11.3.58-1
ENV NV_ML_REPO_ENABLED 1
ENV NV_ML_REPO_URL https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/${NVARCH}

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/${NVARCH}/7fa2af80.pub | apt-key add - && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/${NVARCH} /" > /etc/apt/sources.list.d/cuda.list && \
    if [ ! -z ${NV_ML_REPO_ENABLED} ]; then echo "deb ${NV_ML_REPO_URL} /" > /etc/apt/sources.list.d/nvidia-ml.list; fi && \
    apt-get purge --autoremove -y curl \
    && rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 11.3.0

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-11-3=${NV_CUDA_CUDART_VERSION} \
    ${NV_CUDA_COMPAT_PACKAGE} \
    && ln -s cuda-11.3 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

# Required for nvidia-docker v1
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf \
    && echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

COPY NGC-DL-CONTAINER-LICENSE /

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility