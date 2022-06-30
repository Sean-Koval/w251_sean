#!/bin/bash
sudo systemctl start k3s
kubectl apply -f mqtt_service.yaml
kubectl apply -f aws_secret.yaml
kubectl apply -f mqtt_deployment.yaml
kubectl apply -f other_deployments.yaml
#kubectl apply -f processor_deployment.yaml
