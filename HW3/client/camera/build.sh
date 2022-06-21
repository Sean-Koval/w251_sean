#!/bin/bash

docker build -t detector --no-cache .
docker tag detector seankoval/detector:v1
docker push seankoval/detector:v1