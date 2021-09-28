FROM ubuntu:18.04

MAINTAINER jovenchu

RUN apt-get update

RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y python3.6
RUN apt-get install -y python3-pip
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y apache2
RUN apt-get install -y libapache2-mod-wsgi
RUN sed -i 's/80/5000/' /etc/apache2/ports.conf

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /var/www/public_html
ADD flaskapp.wsgi /var/www/flaskapp/flaskapp.wsgi
ADD flaskapp.cfg /etc/apache2/sites-available/flaskapp.conf
RUN a2ensite flaskapp.conf

EXPOSE 5000
