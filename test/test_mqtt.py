#!/usr/bin/env python
import time
import sys
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
    print(msg.payload)
    print(msg.topic)


def on_image(client, userdata, msg):
    print("hello")
    print(msg.payload.decode())
    # filename = "image_{}.jpg".format(uuid.uuid1())
    # with open(filename, 'wb') as img:
    #     img.write(msg.payload)

def main(action='test'):
    if os.environ.get('DOCKER'):
        MQTT_HOST = 'mqtt'
        MQTT_PORT = '1883'
    else:
        MQTT_HOST = '34.219.224.47'
        MQTT_PORT = 1883
    TIMEOUT = 120
    CALLBACK = 0

    client = mqtt.Client(client_id='test_client')
    # client.username_pw_set(settings.MQTT_USERNAME, password=settings.MQTT_PASSWORD)
    client.on_connect = on_connect
    # client.on_message = on_message
    client.on_message = on_message
    client.message_callback_add('camera_comms/image/', on_image)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    if action == 'capture':
        client.publish('camera_comms/capture/', payload='capture')
    elif action == 'test':
        client.publish('camera_comms/test/', payload='a')

    client.loop_start()
    while CALLBACK < TIMEOUT:
        time.sleep(.01)
        CALLBACK += 1
    client.disconnect()
    client.loop_stop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
