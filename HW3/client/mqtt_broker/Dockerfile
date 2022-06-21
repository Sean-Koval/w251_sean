FROM ubuntu:latest

RUN apt update
RUN apt-get install -y mosquitto
# Configure to allow remote access
RUN echo "allow_anonymous true" > /etc/mosquitto/mosquitto.conf
# Set listenet port
RUN echo "listener 1883 0.0.0.0" >> /etc/mosquitto/mosquitto.conf
CMD ["mosquitto","-c","/etc/mosquitto/mosquitto.conf"]