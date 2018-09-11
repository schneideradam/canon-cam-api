#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt

MQTT_HOST = "camera-controller.local"
TIMEOUT = 200
CALLBACK = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("camera_comms/")


def on_message(client, userdata, msg):
    filename = "photos/image_{}.jpg".format(time.strftime("%Y%m%d-%H%M%S", time.localtime()))
    image = msg.payload
    with open(filename, 'wb') as img:
        img.write(image)
    super().CALLBACK = (TIMEOUT + 1)

def on_status(client, userdata, msg):
    payload = msg.payload.decode()
    print(msg.payload.decode())
    super().CALLBACK = (TIMEOUT + 1)


client = mqtt.Client(client_id='test_client')
# client.username_pw_set(settings.MQTT_USERNAME, password=settings.MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add('camera_comms/status/', on_status)
# client.message_callback_add('camera_comms/', on_image)
client.connect(MQTT_HOST, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.publish('camera_comms/status/', payload='status')
client.publish('camera_comms/', payload='capture')
client.loop_start()
while CALLBACK < TIMEOUT:
    time.sleep(.01)
    CALLBACK += 1
client.disconnect()
client.loop_stop()
