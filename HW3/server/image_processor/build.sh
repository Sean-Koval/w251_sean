#!/bin/bash

docker build -t logger-list .
docker tag logger-list seankoval/logger_list:v1
docker push seankoval/logger_list:v1