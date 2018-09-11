FROM jjanzic/docker-python3-opencv:opencv-3.3.0

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ADD . /src
WORKDIR /src

RUN apt-get update && apt-get install -y \
libgphoto2*

RUN pip install -r requirements.txt
