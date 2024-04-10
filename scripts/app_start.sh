#!/bin/sh

if [ -z "$FLASK_APP" ]; then
    echo "FLASK_APP is not set"
    exit 1
fi

if [ "$RUN_TASKS" = "True" ]; then
    echo "Running tasks"
    python3 app.py
    exit 0
fi

gunicorn --chdir . ${FLASK_APP} -w 2 --threads 32 -b 0.0.0.0:80 --log-level=info --log-file=-
