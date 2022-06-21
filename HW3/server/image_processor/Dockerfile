### Dockerfile: sets up python env and runs receiver python code
FROM ubuntu:latest
# FROM alpine:latest
  
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /app

RUN apt-get update
RUN apt install -y python3-pip python3 python3-opencv mosquitto-clients libopencv-dev x11-xserver-utils libcanberra-gtk-module libcanberra-gtk3-module

RUN pip3 install numpy

RUN pip3 install paho-mqtt
RUN pip3 install boto3
RUN pip3 install DateTime
RUN pip3 install botocore

#WORKDIR /app

COPY processor2.py ./ 
# COPY processor.py processor.py
CMD ["python3", "processor2.py"]
