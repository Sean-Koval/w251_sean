## Homework Repo for W251 HW 3

This a repository for setting up the face capture application that will run on a remote linux machine and will send the message (image) to the VPC Kub cluster to process the image and store in s3.

LINK TO PUBLIC S3 BUCKET:


![](https://seanimagebucket.s3.amazonaws.com/06-19-2022-18-59-32sean_koval_image.png)

[https://seanimagebucket.s3.amazonaws.com/06-19-2022-18-59-32sean_koval_image.png](https://seanimagebucket.s3.amazonaws.com/06-19-2022-18-59-32sean_koval_image.png)

## Setting up Kubernetes, Docker, and OpenCV on an edge device (linux VM)

The purpose of this project is to setup a kubernetes cluster on an edge device (VM) and move data from the edge device to an EC2 instance and then to an S3 bucket. This process requires setting up multiple docker images (camera capture, MQTT broker, Message forwarder) within a kub cluster on the client machine. The message forwarder will then connect to the broker on the server side and send an image over a TCP/Websocket connection to the server side where a kub cluster is managing the pod of docker images (MQTT broker and message processer).


# Setting up Server Side

Steps to setup server side kub cluster:

Initial setup:
- The repo/kub files need to be downloaded on the server side (EC2 instance)
- Check the TCP/Websocket ports that are open so that we can connect using the client device

Code:
- MQTT broker pyton file
- Python script for storing the message received from the broker in the S3 bucket

Docker:
- Docker image for the MQTT broker (could use the same docker file code used for the broker on the client device)
- Docker image for the python script that will store the image recieved in the S3 bucket

:: The Docker files will need to be published on Docker Hub
:: The Docker file will be pulled to the server side using a Kub .yaml file with registry information
:: Kuberetes will pull the the docker image from the registry and Docker will be used to deploy the application to the Kubenetes cluster


Kubernetes: (1 Total Kubernetes cluster: Server and Client)
- 1 Node hosting 1 Pod (containing 2 docker images)
- Download .yaml file to EC2 (micro) instance and deploy usink kubectl
- This will have a TCP endpoint for MQTT broker to receive messages from the client forwarder
- The processing script within the kube pod will need to have access credentials to the S3 bucket


# Setting up Client Side

Steps to setup the kube cluster (node) on the client side:

Initial setup (node)):
- Download the repo on the VM
- Build docker images for camera, forwarder, broker, service, and logger (using bash scripts)
- Deploy application using using deploy.sh script within client folder (deploy these pods after the pods in the server are deployed)
- Check the logs of the client and ensure all pods are running
- Note: you will have to set the IP Address used by the forwarder to the IPv4 address of the AWS instance
- Note: you may have to edit the video port that the jetson nano/VM is assigning to the camera

```
+-- cloud
|   +-- deploy_script.sh
|   +-- broker
|       +-- Dockerfile
|	+-- bash_script.sh
|       +-- mosquitto_deployment.yaml
|       +-- mosquittoService.yaml  
|   +-- image_processor
|       +-- build.sh
|       +-- Dockerfile
|       +-- cred.py
|       +-- image_processor.py
|   +-- logger
|       +-- build.sh
|       +-- Dockerfile
|       +-- server_logger.py
|   +-- server_borker
|       +-- build.sh
|       +-- Dockerfile
|   +-- aws_secret.yaml
|   +-- deploy.sh
|   +-- mqtt_deployment.yaml
|   +-- mqtt_service.yaml
|	+-- other_deployments.yaml
|	+-- stop_deployment.py
+-- client
|   +-- camera
|       +-- build.sh
|       +-- camera.py
|       +-- Dockerfile
|	    +-- haarcascade_frontalface_default.xml
|   +-- mqtt_broker
|       +-- build.sh
|       +-- Dockerfile
|   +-- mqtt_forwarder
|       +-- build.sh
|       +-- Dockerfile
|       +-- message_forward.py  
|   +-- mqtt_logger
|       +-- build.sh
|       +-- Dockerfile
|       +-- logger.py
|   +-- broker_deployment.yaml
|   +-- mqtt_service.yaml
|   +-- deploy.sh
|   +-- other_deployments.yaml
|   +-- stop_deployment.sh
```

Code:
- Camera capture python file
- MQTT python file
- Message Forwarder python file (will need to listen to MQTT broker and have TCP port for MQTT Broker on server)
- logger python file
- Image processor file used to store image in s3 bucket

Docker:
- Docker image for the camera (download packages and run the application)
- Docker image for the MQTT broker (setup env and run broker with the port)
- Docker image for the message forwarder (setup env and list to the port of the MQTT broker)(forward to the tcp endpoint on the server side)
- Docker image for the logger (client/server)
- Docker image for image processor

:: Docker file needs to be published to the registry
:: Kube will pull the Docker image from the registry and then Docker will run the files to deploy the applications to the cluster

Kubernetes: (1 shared)
- The .yaml files will be used to manage the pods and deployment 


# Question 4 Answer

MQTT Topics: The MQTT topic that I used for the app is 'face_capture' which is utilized in multiple files where we are calling on MQTT within the broker and listner.

QoS: The QoS that I choose to use is a value of 1. This is to reduce the liklihood that an image is lost, by ensuring that we send at least 1 message.
