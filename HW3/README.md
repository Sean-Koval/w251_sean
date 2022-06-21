## Homework Repo for W251 HW 3

This a repository for setting up the face capture application that will run on a remote linux machine and will send the message (image) to the VPC Kub cluster to process the image and store in s3.

LINK TO PUBLIC S3 BUCKET:

https://s3.console.aws.amazon.com/s3/buckets/seanimagebucket?region=us-east-1&tab=objects

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
- build docker image (or pull from dockerhub?)
- create network bridge between broker container and the forwarder container + publisher
    -- docker network create --driver bridge hw_3
- next start the broker on the jetson nano/VM with the networking bridge
    -- docker run -dit --network hw_03 --name

+-- cloud
|   +-- deploy_script.sh
|   +-- broker
|       +-- Dockerfile
|	+-- bash_script.sh
|       +-- mosquitto_deployment.yaml
|       +-- mosquittoService.yaml  
|   +-- processor
|       +-- Dockerfile
|	+-- docker_script.sh
|	+-- processor_deployment.yaml
|	+-- processor.py
+-- edge
|   +-- deploy_script.sh
|   +-- mosquitto_deployment.yaml
|   +-- other_deployments.yaml
|   +-- mosquittoService.yaml
|   +-- broker
|       +-- Dockerfile
|   +-- detector
|	+-- Dockerfile
|       +-- docker_script.sh
|	+-- haarcascade_frontalface_default.xml
|       +-- cam.py
|   +-- logger 
|       +-- Dockerfile
|       +-- docker_script.sh
|       +-- logger.py
|   +-- forwarder
|      +-- Dockerfile
|      +-- docker_script.sh
|      +-- forwarder.py    


Code:
- Camera capture python file
- MQTT python file
- Message Forwarder python file (will need to listen to MQTT broker and have TCP port for MQTT Broker on server)

Docker:
- Docker image for the camera file (download packages and run the application)
- Docker image for the MQTT broker (setup env and run broker with the port)
- Docker image for the message forwarder (setup env and list to the port of the MQTT broker)(forward to the tcp endpoint on the server side)

:: Docker file needs to be published to the registry
:: Kube will pull the Docker image from the registry and then Docker will run the files to deploy the applications to the cluster

Kubernetes: (1 shared)
- The .yaml files will be used to manage the pod of Docker files
- 1 Node hosting 1 pod of Docker images 


# Question 4 Answer

MQTT Topics: The MQTT topic that I used for the app is 'face_capture' which is utilized in multiple files where we are calling on MQTT within the broker and listner.

QoS: The QoS that I choose to use is a value of 1. This is to reduce the liklihood that an image is lost, by ensuring that we send at least 1 message.

DEBUGGING COMMANDS:

# if NoScheduling is set for master node
# this will remove that taint making it so that you do not need to add a tolerance to the .yaml deployment file
$ kubectl patch node MASTER_NAME -p "{\"spec\":{\"unschedulable\":false}}"

# if there is an issue with the port not having permission (on server)
# expose the ports 8080 and the nodeport (whatever is available) to the private instance security group

# make sure all docker images have the same name as the .yaml file describes
# make sure to build docker images for first time on different architectures
# can find an open TCP port on aws by not setting a value for the NodePort and letting kubernetes find an open port. Then you can hard code the port into the .yaml files once discovered
# if issues arise. Drain node, delete deploymentes, delete services, restart processes


# if imagePullError
# check if you have permission (login via 'docker login')

# if docker cant build image because there isn't enough space
# docker prune
# increase volume of root repo on instance
# extend from root repo to partition


# IF YOU GET A net/http timout error when calling kubectl commnands
# reset proxy issue: '$ unset http_proxt' and '$ unset https_proxy'


