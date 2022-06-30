#!/bin/bash

kubectl delete deployment processor-deployment
kubectl delete deployment serv-mosquitto-deployment
kubectl delete service aws-secret
kubectl delete service serv-mosquitto-service 
kubectl delete deployment serv-logger logger-list

sudo systemctl stop k3s

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)