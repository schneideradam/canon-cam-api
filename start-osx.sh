#!/bin/bash
if [ ! -f .env ]; then
    touch .env
    touch .mqtt_env
fi
docker-compose -f docker-compose-override.yml up -d
