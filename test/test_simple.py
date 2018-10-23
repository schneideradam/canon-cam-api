#!/usr/bin/env python
import time
import os
import uuid
import paho.mqtt.client as mqtt

DIR = os.path.dirname(os.path.realpath(__file__))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("camera_comms/#")


def on_message(client, userdata, msg):
    client.loop_stop()


def on_image(client, userdata, msg):
    filename = "{}/photos/image_{}.jpg".format(DIR, uuid.uuid1())
    with open(filename, 'wb') as img:
        img.write(msg.payload)



def main():
    MQTT_HOST = '34.219.224.47'
    MQTT_PORT = 1883
    TIMEOUT = 120
    CALLBACK = 0

    client = mqtt.Client(client_id='test_client')
    client.on_connect = on_connect
    client.message_callback_add('camera_comms/image/', on_image)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.subscribe('camera_comms/image/')
    client.publish('camera_comms/test/', payload="a", qos=2)
    client.loop_start()
    time.sleep(1)

if __name__ == '__main__':
    main()
