#!/bin/bash

docker build -t logger .
docker tag logger seankoval/logger:v1
docker push seankoval/logger:v1