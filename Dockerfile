FROM lakerfield/dotnet-gphoto2

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ADD . /src
WORKDIR /src

RUN apt-get update && apt-get install -y \
libgphoto2*
python3 -y
python3-pip -y

RUN pip3 install -r requirements.txt

EXPOSE 8080
