#!/bin/bash

docker build -t processor --no-cache .
docker tag processor seankoval/processor:v3
docker push seankoval/processor:v3