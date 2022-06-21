import paho.mqtt.client as mqtt
import sys


LOCAL_MQTT_HOST = "mosquitto-service"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC ="face_capture" 

print(f'{LOCAL_MQTT_HOST} {LOCAL_MQTT_PORT}')
print(type(LOCAL_MQTT_HOST), type(LOCAL_MQTT_PORT))

def on_connect_local(client, userdata, flags, rc):
    '''
    Subscribe to the topic on the MQTT broker.
    '''
    print(f'connected to local broker with rc: {str(rc)}')
    client.subscribe(LOCAL_MQTT_TOPIC)
    print(f'Subscribed to topic: {LOCAL_MQTT_TOPIC}')
	
def on_message(client, userdata, msg):
    '''
    Prints the decoded message from the broker topic.
    '''
    try:
        print('Message Received...')
        print(f'Message Size (bytes): {len(msg.payload)}')
        #print(f'Message Info:\t {str(msg.payload.decode("utf-8"))}')

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




# import paho.mqtt.client as mqtt

# LOCAL_MQTT_HOST="mosquitto-service"
# LOCAL_MQTT_PORT=1883
# LOCAL_MQTT_TOPIC="faces"

# def on_connect_local(client, userdata, flags, rc):
#     print("connected to local broker with rc: " + str(rc))
#     client.subscribe(LOCAL_MQTT_TOPIC)

# def on_message(client,userdata, msg):
#   print('See message received here!')
#   try:
#     print("message received! {} bytes ".format(len(msg.payload)))
#   except:
#     print("Unexpected error:", sys.exc_info()[0])

# print("Create new instance")
# local_mqttclient = mqtt.Client()

# print("Bind call back function")
# local_mqttclient.on_connect = on_connect_local

# print("Connect to broker")
# local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

# print("Receiving message...")
# local_mqttclient.on_message = on_message

# local_mqttclient.loop_forever()