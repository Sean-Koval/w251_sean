#!/bin/bash

docker build -t serv-logger .
docker tag serv-logger seankoval/serv_logger:v1
docker push seankoval/serv_logger:v1