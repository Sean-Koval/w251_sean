# import libraries
import os
import sys

import cv2
import numpy as np

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

import paho.mqtt.client as mqtt
from datetime import datetime
from cred import AWS_ACCESS_KEY_ID, AWS_SECRET_KEY

# set global vars for MQTT Broker
LOCAL_MQTT_HOST = "serv-mosquitto-service"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC ="face_capture" 

print(f'{LOCAL_MQTT_HOST} {LOCAL_MQTT_PORT}')
print(type(LOCAL_MQTT_HOST), type(LOCAL_MQTT_PORT))

#K3s Cred from Secret
#ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
#SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY'] # AWS_SECRET_KEY

# # name of S3 bucket
BUCKET = 'seanimagebucket'
CONFIG = Config(
    read_timeout=200,
    connect_timeout=200,
    retries={"max_attempts": 5})


s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_KEY,
                  config=CONFIG)

def upload_file(file_name, bucket, object_name=None):
    '''
    Uploads file object to s3 bucket.
    '''
    if object_name is None:
        print('Object name not set...')
        object_name = os.path.basename(file_name)
        #s3_client = boto3.client('s3')
        print('Connected to client within upload')
    try:
        #s3_client = 
        print(f'Uploading file:\t{file_name} to {bucket}')
        ### TODO: THIS IS WHERE THE FILE HAS ERROR: <class 'attribute error'>
        response = s3.upload_file(file_name, bucket, object_name)

    except ClientError as e:
        print(e)



def on_connect_local(client, userdata, flags, rc):
    '''
    Subscribe to the topic on the MQTT broker.
    '''
    print(f'connected to local broker with rc: {str(rc)}')
    client.subscribe(LOCAL_MQTT_TOPIC)
    print(f'Subscribed to topic: {LOCAL_MQTT_TOPIC}')
    print(f'AWS ACCESS: {AWS_ACCESS_KEY_ID}')
	
def on_message(client, userdata, msg):
    '''
    Prints the decoded message from the broker topic.
    '''
    try:
        print('Message Received...')
        print(f'Message Size (bytes): {len(msg.payload)}')
        # # get payload
        #img = msg.payload.decode

        # Generate File Name
        id = 'sean_koval'
        date_time = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
        file_name = str(date_time) + str(id) + '_image.png'

        
        # # Save Image
        #nparr = np.frombuffer(img, np.uint8)
        #img = cv2.imdecode(nparr, 0) #cv2.IMREAD_COLOR)
        #cv2.imwrite(file_name, img)
        #print(f'uploading to s3 {img}')
        
        # write the payload to a file
    
        #print("messae received: ",str(len(msg.payload.decode))
        # "images" + id + ".png"
        print('Processing image...')
        f = open(file_name, "wb")
        f.write(msg.payload)
        f.close()
        print(f'Uploading: {id} file size: {len(msg.payload)}')
        upload_file(file_name, BUCKET)

        print('Upload Successful!')
        print(f'Ending Upload Process')
    except:
        print(f'Unexpected error:\t {sys.exc_info()[0]}')

print('1/4:\tSetting up logger client...')
local_mqttclient = mqtt.Client()
print('2/4:\tBind call back function...')
local_mqttclient.on_connect = on_connect_local
print(f'3/4:\tConnect to |\tLocal host: {LOCAL_MQTT_HOST} |\tPort: {LOCAL_MQTT_PORT}')
local_mqttclient.connect(LOCAL_MQTT_HOST, port=LOCAL_MQTT_PORT, keepalive=60)
print('4/4:\tListening to Broker...')
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()




