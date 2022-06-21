#!/bin/bash

# starts k3s and deplys the service and application deployments
sudo systemctl start k3s

kubectl apply -f mqtt_service.yaml
kubectl apply -f broker_deployment.yaml
kubectl apply -f other_deployments.yaml

kubectl get service

sleep 10

kubectl get pods