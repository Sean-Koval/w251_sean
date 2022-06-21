import paho.mqtt.client as mqtt
import sys

LOCAL_MQTT_HOST = "mosquitto-service"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC ="face_capture" 

REMOTE_MQTT_HOST = "54.227.71.69"
REMOTE_MQTT_PORT = 32211
REMOTE_MQTT_TOPIC = "face_capture"

# connect to remote host

print(f'{LOCAL_MQTT_HOST} {LOCAL_MQTT_PORT}')
print(type(LOCAL_MQTT_HOST), type(LOCAL_MQTT_PORT))

def on_connect_local(client, userdata, flags, rc):
    print(f'connected to local broker with rc: {str(rc)}')
    client.subscribe(LOCAL_MQTT_TOPIC)

def on_connect_remote(client, userdata, msg):
    print(f'Connected to remote broker with rc: {str(rc)}')

#def on_publish(client,userdata,result): #create function for callback
#    print("data published \n")
#    pass

def on_message(client, userdata, msg):
    try:
        # print the message received
        #print(f'message received: {len(msg)}') 

        msg = msg.payload  
        #test_message = "ARE YOU GETTING THIS"
        #remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=test_message, qos=1)
        # forward Message
        remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0)
        print(f'message sent {len(msg)}')

    except Exception as e:
        print(f"Unexpected error: {e.message}")#, sys.exc_info()[0])

print("Connecting to remote host")
remote_mqttclient = mqtt.Client()
remote_mqttclient.on_connect = on_connect_remote
remote_mqttclient.connect(REMOTE_MQTT_HOST, port=32211, keepalive=60)


local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
print('Connecting to local host...')
local_mqttclient.connect(LOCAL_MQTT_HOST, port=1883, keepalive=60)
print('Listening to Broker...')
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()