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

logger = logging.getLogger('Camera-Controller')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

if LOGSTASH_HOST:
    logger.addHandler(logstash.LogstashHandler(LOGSTASH_HOST, 5001, version=1))

if SENTRY_DSN:
    sentry = SentryHandler(SENTRY_DSN)
    sentry.setLevel(logging.ERROR)
    setup_logging(sentry)

# If we are running in a docker stack, we will look to the local MQTT broker
if os.environ.get('DOCKER'):
    MQTT_HOSTNAME = 'mqtt'
else:
    MQTT_HOSTNAME = 'localhost'

DIR = os.path.dirname(os.path.realpath(__file__))

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
            image, target = action.capture_image()
            client.publish('camera_comms/', payload=image)
            logger.info('Image captured - {}'.format(target))
        except Exception as e:
            logger.error(
                'Could not access camera {}'.format(str(e))
            )
            client.publish('camera_comms/', payload=str(e))
    elif payload == 'status':
        try:
            summary = action.get_summary()
            client.publish('camera_comms/status/', payload=summary)
            logger.info(summary)
        except Exception as e:
            logger.error(
                'Could not access camera {}'.format(str(e))
            )
            client.publish('camera_comms/status/', payload=str(e))
            client.disconnect()
    elif payload == 'test':
        with open('test_photo.jpg', 'rb') as test_img:
            img = test_img.read()
        client.publish('camera_comms/', payload=img)
        logger.info('Sending test image')
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
