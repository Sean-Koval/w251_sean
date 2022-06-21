# from ubuntu
FROM alpine:latest
# needed for logging output
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apk update 
RUN apk add python3 
RUN apk add py3-pip
RUN apk add mosquitto
RUN pip3 install paho-mqtt

COPY server_logger.py ./
CMD ["python3", "server_logger.py"]
