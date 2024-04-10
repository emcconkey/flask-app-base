#!/bin/bash

# The first augument is the task to run
# Example: ./run_tasks.sh task_name
# This is passet into app/app.py as an environment variable: task_name=True
TASK=$1
APP_NAME=sample-app

if [ -z "$DEPLOY_ENV" ]; then
  echo "DEPLOY_ENV not set"
  exit 1
fi

# Example task running script for the container
echo "******************************************"
echo "RUNNING ${TASK} FOR ${DEPLOY_ENV}"
docker run --rm \
  -e RUN_TASKS=True -e \
  "$TASK"=True \
  --name ${APP_NAME}-${DEPLOY_ENV} \
  -e RUN_MODE=${DEPLOY_ENV} \
  -v /app/${APP_NAME}-${DEPLOY_ENV}/logs:/app/logs \
  ${APP_NAME}-${DEPLOY_ENV}
echo "TASK RUN COMPLETE"
echo "******************************************"
