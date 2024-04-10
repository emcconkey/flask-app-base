#!/bin/bash

APP_NAME=sample-app

if [ -z "$DEPLOY_ENV" ]; then
  echo "DEPLOY_ENV not set"
  exit 1
fi

echo "******************************************"
echo "BUILDING FOR ${DEPLOY_ENV}"
docker build -t ${APP_NAME}-${DEPLOY_ENV} .
echo "BUILD COMPLETE"
echo "******************************************"

echo "******************************************"
echo "RUNNING POST BUILD SCRIPTS"
  # Do something here
echo "POST BUILD SCRIPTS COMPLETE"
echo "******************************************"

