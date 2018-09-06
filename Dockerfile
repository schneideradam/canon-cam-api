FROM sellpy/python3-gphoto2

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ADD . /src
WORKDIR /src

RUN apt-get update
RUN apt-get install -y libgphoto2*

RUN pip install -r requirements.txt

EXPOSE 8080
