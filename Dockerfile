FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ADD . /src
WORKDIR /src

RUN apt-get update && apt-get install -y \
  v4l2loopback-utils \
  vlc

RUN pip install -r requirements.txt
