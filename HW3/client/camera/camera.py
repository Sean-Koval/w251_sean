import numpy as np
import cv2
import paho.mqtt.client as mqtt



# Set up MQTT
LOCAL_MQTT_HOST = 'mosquitto-service'
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = 'face_capture' 

print(f'{LOCAL_MQTT_HOST} {LOCAL_MQTT_PORT}')
print(type(LOCAL_MQTT_HOST), type(LOCAL_MQTT_PORT))


def on_connect_local(client, userdata, flags, rc):
    print('connected to local broker with rc: ' + str(rc))


local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, port=1883, keepalive=200)


# Load cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# the index depends on your camera setup and which one is your USB camera.
# you may need to change to 1 depending on your local config
# v4l2-ctl --list-devices
# HD CAMERA: 2 or 3
# FACETIME: 0 or 1
cap = cv2.VideoCapture(7)

count = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray_frame, 1.1, 4)
    print(len(faces))

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(gray_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    if len(faces) > 0:
        print(f'Found a face: {faces}')
        
        # Convert image to binary
        rc, png = cv2.imencode('.png', gray_frame)
        msg = png.tobytes()
        #print(f'Image converted to binary: {msg}')

        # Send Message
        #local_mqttclient.publish(LOCAL_MQTT_TOPIC,'Face Found')
        local_mqttclient.publish(LOCAL_MQTT_TOPIC, msg)


        #count += 1
        #if count == 10:
        #    break


    # Display the resulting frame
    #cv2.imshow('frame',gray_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()