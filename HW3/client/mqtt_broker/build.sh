#!/bin/bash

docker build -t mosquitto-broker-device .
docker tag mosquitto-broker-device seankoval/mosquitto-broker-device:v1
docker push seankoval/mosquitto-broker-device:v1