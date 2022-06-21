FROM ubuntu
# this is needed to make sure we can see the log output

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update
RUN apt install -y python3-dev python3-pip
#RUN apt-get py3-pip

RUN apt-get install -y mosquitto
RUN pip3 install paho-mqtt

COPY message_forward.py ./
CMD ["python3", "message_forward.py"]