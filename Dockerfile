FROM lakerfield/dotnet-gphoto2

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ADD . /src
WORKDIR /src

RUN apt-get update
RUN apt-get install libgphoto2* -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN pip3 install -r requirements.txt

EXPOSE 8080
