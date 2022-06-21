#!/bin/bash

docker build -t forwarder --no-cache .
docker tag forwarder seankoval/forwarder:v1
docker push seankoval/forwarder:v1