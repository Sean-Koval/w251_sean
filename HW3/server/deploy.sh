#!/bin/bash
sudo systemctl start k3s
kubectl apply -f mqtt_service.yaml
kubectl apply -f aws_secret.yaml
kubectl apply -f mqtt_deployment.yaml
kubectl apply -f server_logger.yaml
#kubectl apply -f processor_deployment.yaml

kubectl get service

sleep 10

kubectl get pods