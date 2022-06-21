#!/bin/bash

docker build -t mosquitto-serv  .
docker tag mosquitto-serv seankoval/mosquitto-serv:v1
docker push seankoval/mosquitto-serv:v1