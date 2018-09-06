#!/usr/bin/env python
import logging
import paho.mqtt.client as mqtt
from camera_controller import CameraActions
import os

logger = logging.getLogger(__name__)

MQTT_HOSTNAME = os.environ.get('MQTT_HOSTNAME', "localhost")

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("camera_comms/")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(payload)
    try:
        action = CameraActions()
        summary = action.get_summary()
        logger.info(payload)
        action.capture_image()
        print(summary)
    except Exception as e:
        logger.error(
            'Could not trigger camera. {}'.format(str(e))
        )
        return
    logger.info('Image captured')

client = mqtt.Client(client_id='camera_status')
# client.username_pw_set(settings.MQTT_USERNAME, password=settings.MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
# import pdb; pdb.set_trace()
client.connect(MQTT_HOSTNAME, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
