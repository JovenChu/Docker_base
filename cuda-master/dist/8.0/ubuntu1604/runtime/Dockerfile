FROM ubuntu:16.04 as base

FROM base as base-amd64

ENV NVARCH x86_64
ENV NVIDIA_REQUIRE_CUDA "cuda>=8.0"
ENV NV_CUDA_CUDART_VERSION 8.0.61-1

ENV NV_ML_REPO_ENABLED 1
ENV NV_ML_REPO_URL https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/${NVARCH}

ENV NV_CUDA_NVRTC_VERSION 8.0.61-1
ENV NV_CUDA_NVRTC_PACKAGE cuda-nvrtc-8-0=${NV_CUDA_NVRTC_VERSION}
ENV NV_CUDA_NVGRAPH_VERSION 8.0.61-1
ENV NV_CUDA_NVGRAPH_PACKAGE cuda-nvgraph-8-0=${NV_CUDA_NVGRAPH_VERSION}
ENV NV_LIBCUSOLVER_VERSION 8.0.61-1
ENV NV_LIBCUSOLVER_PACKAGE cuda-cusolver-8-0=${NV_LIBCUSOLVER_VERSION}
ENV NV_LIBCUBLAS_VERSION 8.0.61.2-1
ENV NV_LIBCUBLAS_PACKAGE cuda-cublas-8-0=${NV_LIBCUBLAS_VERSION}
ENV NV_LIBCUFFT_VERSION 8.0.61-1
ENV NV_LIBCUFFT_PACKAGE cuda-cufft-8-0=${NV_LIBCUFFT_VERSION}
ENV NV_LIBCURAND_VERSION 8.0.61-1
ENV NV_LIBCURAND_PACKAGE cuda-curand-8-0=${NV_LIBCURAND_VERSION}
ENV NV_LIBCUSPARSE_VERSION 8.0.61-1
ENV NV_LIBCUSPARSE_PACKAGE cuda-cusparse-8-0=${NV_LIBCUSPARSE_VERSION}
ENV NV_LIBNPP_VERSION 8.0.61-1
ENV NV_LIBNPP_PACKAGE cuda-npp-8-0=${NV_LIBNPP_VERSION}
FROM base as base-ppc64le

ENV NVARCH ppc64el
ENV NVIDIA_REQUIRE_CUDA "cuda>=8.0"
ENV NV_CUDA_CUDART_VERSION 8.0.61-1

ENV NV_ML_REPO_ENABLED 1
ENV NV_ML_REPO_URL https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/${NVARCH}

ENV NV_CUDA_NVRTC_VERSION 8.0.61-1
ENV NV_CUDA_NVRTC_PACKAGE cuda-nvrtc-8-0=${NV_CUDA_NVRTC_VERSION}
ENV NV_CUDA_NVGRAPH_VERSION 8.0.61-1
ENV NV_CUDA_NVGRAPH_PACKAGE cuda-nvgraph-8-0=${NV_CUDA_NVGRAPH_VERSION}
ENV NV_LIBCUSOLVER_VERSION 8.0.61-1
ENV NV_LIBCUSOLVER_PACKAGE cuda-cusolver-8-0=${NV_LIBCUSOLVER_VERSION}
ENV NV_LIBCUBLAS_VERSION 8.0.61.2-1
ENV NV_LIBCUBLAS_PACKAGE cuda-cublas-8-0=${NV_LIBCUBLAS_VERSION}
ENV NV_LIBCUFFT_VERSION 8.0.61-1
ENV NV_LIBCUFFT_PACKAGE cuda-cufft-8-0=${NV_LIBCUFFT_VERSION}
ENV NV_LIBCURAND_VERSION 8.0.61-1
ENV NV_LIBCURAND_PACKAGE cuda-curand-8-0=${NV_LIBCURAND_VERSION}
ENV NV_LIBCUSPARSE_VERSION 8.0.61-1
ENV NV_LIBCUSPARSE_PACKAGE cuda-cusparse-8-0=${NV_LIBCUSPARSE_VERSION}
ENV NV_LIBNPP_VERSION 8.0.61-1
ENV NV_LIBNPP_PACKAGE cuda-npp-8-0=${NV_LIBNPP_VERSION}
FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates apt-transport-https gnupg-curl && \
    NVIDIA_GPGKEY_SUM=d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5 && \
    NVIDIA_GPGKEY_FPR=ae09fe4bbd223a84b2ccfce3f60f4b3d7fa2af80 && \
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/${NVARCH}/7fa2af80.pub && \
    apt-key adv --export --no-emit-version -a $NVIDIA_GPGKEY_FPR | tail -n +5 > cudasign.pub && \
    echo "$NVIDIA_GPGKEY_SUM  cudasign.pub" | sha256sum -c --strict - && rm cudasign.pub && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/${NVARCH} /" > /etc/apt/sources.list.d/cuda.list && \
    if [ ! -z ${NV_ML_REPO_ENABLED} ]; then echo "deb ${NV_ML_REPO_URL} /" > /etc/apt/sources.list.d/nvidia-ml.list; fi && \
    apt-get purge --auto-remove -y gnupg-curl \
    && rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 8.0.61

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-8-0=${NV_CUDA_CUDART_VERSION} \
    ${NV_CUDA_NVRTC_PACKAGE} \
    ${NV_CUDA_NVGRAPH_PACKAGE} \
    ${NV_CUSOLVER_PACKAGE} \
    ${NV_LIBCUBLAS_PACKAGE} \
    ${NV_LIBCUFFT_PACKAGE} \
    ${NV_LIBCURAND_PACKAGE} \
    ${NV_LIBCUSPARSE_PACKAGE} \
    ${NV_LIBNPP_PACKAGE} \
    && ln -s cuda-8.0 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

# Required for nvidia-docker v1
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

COPY NGC-DL-CONTAINER-LICENSE /

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility