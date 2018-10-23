#!/usr/bin/env python
import time
import os
import uuid
import sys
import paho.mqtt.client as mqtt

DIR = os.path.dirname(os.path.realpath(__file__))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(str(rc)))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("camera_comms/#")


def on_message(client, userdata, msg):
    print(msg.payload.decode())


def on_image(client, userdata, msg):
    filename = "{}/photos/image_{}.jpg".format(DIR, uuid.uuid1())
    with open(filename, 'wb') as img:
        img.write(msg.payload)
    client.disconnect()
    client.loop_stop()


def main(action='test'):
    if os.environ.get('DOCKER'):
        MQTT_HOST = 'mqtt'
        MQTT_PORT = '1883'
    else:
        MQTT_HOST = '34.219.224.47'
        MQTT_PORT = 1883

    client = mqtt.Client(client_id='test_client')
    client.on_connect = on_connect
    client.message_callback_add('camera_comms/image/', on_image)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.subscribe('camera_comms/image/')
    client.loop_start()
    if action == 'capture':
        client.publish('camera_comms/capture/', payload="capture")
    elif action == 'test':
        client.publish('camera_comms/test/', payload="test")
    else:
        client.publish('camera_comms/status/', payload="status")
    time.sleep(2)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
