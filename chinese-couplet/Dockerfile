# 基于的基础镜像
FROM webappflask
 
ENV PATH $PATH:/usr/local/python3/bin/
ENV PYTHONIOENCODING utf-8

# 代码添加到code文件夹
ADD . /code

# 设置code文件夹是工作目录
WORKDIR /code

# 安装支持
# RUN pip3 install -r requirements.txt
# 启动WSGI注入了一些代码
ADD chinese-couplet.wsgi /var/www/flaskapp/flaskapp.wsgi
# 在启动容器，启动apache web服务器时获取任何可能的错误信息，并将其发送至stdout
CMD service apache2 start && tail -F /var/log/apache2/error.log