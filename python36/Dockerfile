# 设置基础镜像
FROM nvidia/cuda:11.0.3-cudnn8-runtime-centos7
MAINTAINER jovenchu

# 安装 openssh 和 openssl
RUN set -ex \
	&& yum install -y openssh-clients openssh-server openssl \
	&& mkdir -p /var/run/sshd \
	&& /usr/bin/ssh-keygen -A
    
# 允许 OpenSSH 在不要求确认的情况下与容器通信
RUN set -ex \
	&& cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new \
	&& echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new \
	&& cat /etc/ssh/sshd_config | grep -v  PermitRootLogin> /etc/ssh/sshd_config.new \
	&& echo "PermitRootLogin yes" >> /etc/ssh/sshd_config.new \
	&& mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config \
	&& mv /etc/ssh/sshd_config.new /etc/ssh/sshd_config

# 开始安装python3
## 设定python版本
ARG python=3.6.10
ENV PYTHON_VERSION=${python} 

RUN yum clean packages \
	&& yum -y install wget make zlib zlib-devel bzip2-devel openssl-devel sqlite-devel readline-devel gdbm-devel  gcc libffi-devel \ 
	&& cd /home \
	&& wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
	&& tar -zxvf Python-${PYTHON_VERSION}.tgz \
	&& cd Python-${PYTHON_VERSION} \
	&& ./configure \
	&& make \
	&& make install \
	&& make clean \
	&& rm -rf Python-${PYTHON_VERSION}

## 安装 python3
RUN set -ex \
	&& if [ -e /usr/bin/python ]; then mv /usr/bin/python /usr/bin/python27; fi \
    && if [ -e /usr/bin/pip ]; then mv /usr/bin/pip /usr/bin/pip-python27; fi \
    && ln -s /usr/local/bin/python3 /usr/bin/python \
    && ln -s /usr/local/bin/pip3 /usr/bin/pip \
    # 修改pip默认镜像源
	&& mkdir -p ~/.pip \
	&& echo '[global]' > ~/.pip/pip.conf \
	&& echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >> ~/.pip/pip.conf \
	&& echo 'trusted-host = pypi.tuna.tsinghua.edu.cn' >> ~/.pip/pip.conf \
	&& echo 'timeout = 120' >> ~/.pip/pip.conf \
	# 更新pip
	&& pip3 install --upgrade pip \
	# 安装wheel
	&& pip3 install wheel

# 验证环境信息，修改环境配置
RUN set -ex \
    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/bin/yum \
    && if [ -e /usr/libexec/urlgrabber-ext-down ]; then sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/libexec/urlgrabber-ext-down; fi
# 完成 python3 安装工作

# 安装jupyterlab
RUN set -ex \
	&& pip install --upgrade pip \
	&& pip --no-cache-dir install jupyterlab \
	&& rm -rf /root/.cache/pip/http/*  

## 确认jupyterlab安装完成
RUN set -ex \
	&& mkdir /etc/jupyter/ \
	&& wget -P /etc/jupyter/  https://raw.githubusercontent.com/Winowang/jupyter_gpu/master/jupyter_notebook_config.py \
	&& wget -P /etc/jupyter/ https://raw.githubusercontent.com/Winowang/jupyter_gpu/master/custom.js 

## 安装tini，使得容器可被集群K8s调用：https://blog.csdn.net/M2l0ZgSsVc7r69eFdTj/article/details/104765016
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
# 解决 net/http: TLS handshake timeout的错误需要添加镜像源，中间报错可删除第二行，再次运行。
RUN set -ex \
    && curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://d1d9aef0.m.daocloud.io \
    && chmod +x /tini