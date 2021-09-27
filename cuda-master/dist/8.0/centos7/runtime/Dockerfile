FROM centos:7 as base

FROM base as base-amd64

ENV NVARCH x86_64
ENV NVIDIA_REQUIRE_CUDA cuda>=8.0
ENV NV_CUDA_CUDART_VERSION 8.0.61-1

COPY cuda.repo-x86_64 /etc/yum.repos.d/cuda.repo
ENV NV_CUDA_NVRTC_VERSION 8.0.61-1
ENV NV_CUDA_NVRTC_PACKAGE cuda-nvrtc-8-0-${NV_CUDA_NVRTC_VERSION}
ENV NV_CUDA_NVGRAPH_VERSION 8.0.61-1
ENV NV_CUDA_NVGRAPH_PACKAGE cuda-nvgraph-8-0-${NV_CUDA_NVGRAPH_VERSION}
ENV NV_LIBCUSOLVER_VERSION 8.0.61-1
ENV NV_LIBCUSOLVER_PACKAGE cuda-cusolver-8-0-${NV_LIBCUSOLVER_VERSION}
ENV NV_LIBCUBLAS_VERSION 8.0.61.2-1
ENV NV_LIBCUBLAS_PACKAGE cuda-libcublas-8-0-${NV_LIBCUBLAS_VERSION}
ENV NV_LIBCUFFT_VERSION 8.0.61-1
ENV NV_LIBCUFFT_PACKAGE cuda-cufft-8-0-${NV_LIBCUFFT_VERSION}
ENV NV_LIBCURAND_VERSION 8.0.61-1
ENV NV_LIBCURAND_PACKAGE cuda-curand-8-0-${NV_LIBCURAND_VERSION}
ENV NV_LIBCUSPARSE_VERSION 8.0.61-1
ENV NV_LIBCUSPARSE_PACKAGE cuda-cusparse-8-0-${NV_LIBCUSPARSE_VERSION}
ENV NV_LIBNPP_VERSION 8.0.61-1
ENV NV_LIBNPP_PACKAGE cuda-npp-8-0-${NV_LIBNPP_VERSION}

FROM base as base-ppc64le

ENV NVARCH ppc64le
ENV NVIDIA_REQUIRE_CUDA cuda>=8.0
ENV NV_CUDA_CUDART_VERSION 8.0.61-1

COPY cuda.repo-ppc64le /etc/yum.repos.d/cuda.repo
ENV NV_CUDA_NVRTC_VERSION 8.0.61-1
ENV NV_CUDA_NVRTC_PACKAGE cuda-nvrtc-8-0-${NV_CUDA_NVRTC_VERSION}
ENV NV_CUDA_NVGRAPH_VERSION 8.0.61-1
ENV NV_CUDA_NVGRAPH_PACKAGE cuda-nvgraph-8-0-${NV_CUDA_NVGRAPH_VERSION}
ENV NV_LIBCUSOLVER_VERSION 8.0.61-1
ENV NV_LIBCUSOLVER_PACKAGE cuda-cusolver-8-0-${NV_LIBCUSOLVER_VERSION}
ENV NV_LIBCUBLAS_VERSION 8.0.61.2-1
ENV NV_LIBCUBLAS_PACKAGE cuda-libcublas-8-0-${NV_LIBCUBLAS_VERSION}
ENV NV_LIBCUFFT_VERSION 8.0.61-1
ENV NV_LIBCUFFT_PACKAGE cuda-cufft-8-0-${NV_LIBCUFFT_VERSION}
ENV NV_LIBCURAND_VERSION 8.0.61-1
ENV NV_LIBCURAND_PACKAGE cuda-curand-8-0-${NV_LIBCURAND_VERSION}
ENV NV_LIBCUSPARSE_VERSION 8.0.61-1
ENV NV_LIBCUSPARSE_PACKAGE cuda-cusparse-8-0-${NV_LIBCUSPARSE_VERSION}
ENV NV_LIBNPP_VERSION 8.0.61-1
ENV NV_LIBNPP_PACKAGE cuda-npp-8-0-${NV_LIBNPP_VERSION}

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN NVIDIA_GPGKEY_SUM=d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5 && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/rhel7/${NVARCH}/7fa2af80.pub | sed '/^Version/d' > /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA && \
    echo "$NVIDIA_GPGKEY_SUM  /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA" | sha256sum -c --strict  -

ENV CUDA_VERSION 8.0
ENV CUDA_PKG_VERSION 8-0-$CUDA_VERSION-1

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN yum upgrade -y && yum install -y \
    ${NV_CUDA_NVRTC_PACKAGE} \
    ${NV_CUDA_NVGRAPH_PACKAGE} \
    ${NV_LIBCUSOLVER_PACKAGE} \
    ${NV_LIBCUBLAS_PACKAGE} \
    ${NV_LIBCUFFT_PACKAGE} \
    ${NV_LIBCURAND_PACKAGE} \
    ${NV_LIBCUSPARSE_PACKAGE} \
    ${NV_LIBNPP_PACKAGE} \
    ${NV_CUDA_CUDART_PACKAGE} \
    && ln -s cuda-8.0 /usr/local/cuda \
    && yum clean all \
    && rm -rf /var/cache/yum/*

# nvidia-docker 1.0
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