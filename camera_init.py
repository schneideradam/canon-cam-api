#!/usr/bin/env python
import logging
import paho.mqtt.client as mqtt
from camera_controller import CameraActions
import os

logger = logging.getLogger(__name__)

if os.environ.get('DOCKER'):
    MQTT_HOSTNAME = os.environ.get('MQTT_HOSTNAME', "localhost")
else:
    MQTT_HOSTNAME = 'localhost'

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("camera_comms/")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    action = CameraActions()
    if payload == 'capture':
        try:
            image = action.capture_image()
            client.publish('camera_comms/', payload=image)
        except Exception as e:
            logger.error(
                'Could not access camera {}'.format(str(e))
            )
    elif payload == 'status':
        try:
            summary = action.get_summary()
            client.publish('camera_comms/', payload=summary)
        except Exception as e:
            logger.error(
                'Could not access camera {}'.format(str(e))
            )
    else:
        logger.error('Unknown command {}'.format(payload))


client = mqtt.Client(client_id='camera_status')
# client.username_pw_set(settings.MQTT_USERNAME, password=settings.MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOSTNAME, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
