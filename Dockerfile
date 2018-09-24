FROM python:3.6-stretch

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ADD . /src
WORKDIR /src

RUN apt-get update
RUN apt-get install libgphoto2* -y
RUN pip3 install -r requirements.txt

EXPOSE 5000
