#!/usr/bin/env python
import os
import logging
import logstash
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging
import paho.mqtt.client as mqtt
from camera_controller import CameraActions

# Logging and alerts
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
LOGSTASH_HOST = os.environ.get('LOGSTASH_HOST', None)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
logger.addHandler(logstash.LogstashHandler(LOGSTASH_HOST, 5001, version=1))

sentry = SentryHandler(SENTRY_DSN)
sentry.setLevel(logging.WARNING)
setup_logging(sentry)

# If we are running in a docker stack, we will look to the local MQTT broker
if os.environ.get('DOCKER'):
    MQTT_HOSTNAME = 'mqtt'
else:
    MQTT_HOSTNAME = 'localhost'


def on_connect(client, userdata, flags, rc):
    # Successfull connection callback
    logger.info("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("camera_comms/#")


def on_message(client, userdata, msg):
    # The callback for when a PUBLISH message is received from the server
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
            client.publish('camera_comms/', payload=str(e))
    elif payload == 'status':
        try:
            summary = action.get_summary()
            client.publish('camera_comms/status/', payload=summary)
        except Exception as e:
            logger.error(
                'Could not access camera {}'.format(str(e))
            )
            client.publish('camera_comms/status/', payload=str(e))
    else:
        logger.warning('Unknown command {}'.format(payload))


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