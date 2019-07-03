FROM python:3.6 AS build-env

WORKDIR /usr/src/

RUN apt-get update &&\
  apt-get -y install apache2 apache2-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY django.conf /etc/apache2/sites-available

RUN a2ensite django && \
  a2dissite 000-default && \
  perl -i.bk -wpe 's/Timeout 300/Timeout 30000/g' /etc/apache2/apache2.conf

RUN mkdir -p /var/www/django && \
  chmod -R 777 /var/www/django

VOLUME ["/var/www/django", "/var/log/apache2"]
EXPOSE 80


