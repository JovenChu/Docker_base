# 基于的基础镜像
FROM centosjoven:latest
 
ENV PATH $PATH:/usr/local/python3/bin/
ENV PYTHONIOENCODING utf-8

# 代码添加到code文件夹
ADD . /code

# 设置code文件夹是工作目录
WORKDIR /code

# 安装支持
RUN pip install -r requirements.txt