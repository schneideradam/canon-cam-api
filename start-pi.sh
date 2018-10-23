#!bin/bash
if [ ! -f .env ]; then
    touch .env
    touch .mqtt_env
fi
docker-compose up -d
