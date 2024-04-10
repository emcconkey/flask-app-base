#!/bin/bash

APP_NAME=sample-app
LISTEN_PORT=8000

if [ -z "$DEPLOY_ENV" ]; then
  echo "DEPLOY_ENV not set"
  exit 1
fi


echo "******************************************"
echo "DEPLOYING TO ${DEPLOY_ENV}"
docker stop -t0 ${APP_NAME}-${DEPLOY_ENV} || true
docker rm ${APP_NAME}-${DEPLOY_ENV} || true
docker run -d \
  --restart=always \
  --name ${APP_NAME}-${DEPLOY_ENV} \
  -e RUN_MODE=${DEPLOY_ENV} \
  -p ${LISTEN_PORT}:80 \
  -v /app/${APP_NAME}-${DEPLOY_ENV}/logs:/app/logs \
  ${APP_NAME}-${DEPLOY_ENV}
echo "DEPLOY COMPLETE"
echo "******************************************"

echo "******************************************"
echo "RUNNING POST DEPLOY SCRIPTS"
  docker exec ${APP_NAME}-${DEPLOY_ENV} bash -c 'cd /app && flask db upgrade'
echo "POST DEPLOY SCRIPTS COMPLETE"
echo "******************************************"

