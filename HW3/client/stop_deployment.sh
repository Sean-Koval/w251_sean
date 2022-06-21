#!/bin/bash

# shuts down the kube deployments and services on the client
kubectl delete deployment mosquitto-broker-device
kubectl delete deployment client-deployments
kubectl delete service mosquitto-service

sudo systemctl stop k3s

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
