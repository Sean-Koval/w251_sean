import os
import boto3
from botocore.config import Config

import paho.mqtt.client as mqtt
import cv2
from datetime import datetime
import numpy as np

SERV_MQTT_HOST = "serv-mosquitto-service" # remote server IP serv-mosquitto-service
#SERV_MQTT_HOST ='10.43.155.173'
SERV_MQTT_PORT = 1883
SERV_MQTT_TOPIC ="face_capture" 
print('CHECK: getting keys')
#K3s Cred from Secret
ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY'] # AWS_SECRET_KEY



print(f'AKID: {ACCESS_KEY_ID}')
print(f'ASK: {SECRET_ACCESS_KEY}')

#config = Config(
#    read_timeout=200,
#    connect_timeout=200,
#    retries={"max_attempts": 5}
#)
# name of S3 bucket
BUCKET = 'seanimagebucket'

# check if bucket exists
#s3_resource = boto3.resource('s3')

#S3 Connection
#s3 = boto3.client('s3', 
#                  aws_access_key_id=ACCESS_KEY_ID,
#                  aws_secret_access_key=SECRET_ACCESS_KEY,
#                  config=config)

#s3_bucket = s3.list_buckets()

#if s3_bucket:
#    print(f'BUCKET: {BUCKET} EXISTS')
#else:
#    print(f'BUCKET: {BUCKET} NOT DETECTED')



print('Connected to S3')
print(f'{SERV_MQTT_HOST} {SERV_MQTT_PORT}')
print(type(SERV_MQTT_HOST), type(SERV_MQTT_PORT))

def on_connect_serv(client, userdata, flags, rc):
        print("connected to SERV broker with rc: " + str(rc))
        print(f'TOPIC: {SERV_MQTT_TOPIC}')
        client.subscribe(SERV_MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        # get payload
        #img = msg.payload
        print('received message')
        # Generate File Name
        #date_time = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
        #file_name = str(date_time) + '_image.png'
        print('decoding image...')
        # Save Image
        #nparr = np.frombuffer(img, np.uint8)
        #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #cv2.imwrite(file_name, img)
        print('uploading to s3')
        # Upload Image 
        #s3.upload_file(file_name, BUCKET, str(file_name))
        print(f'wrote file name: {file_name}')

    except:
        print("Unexpected error:", sys.exc_info()[0])

serv_mqttclient = mqtt.Client()
serv_mqttclient.on_connect = on_connect_serv
serv_mqttclient.connect(SERV_MQTT_HOST, port=1883, keepalive=100)
serv_mqttclient.on_message = on_message

# go into a loop
serv_mqttclient.loop_forever()