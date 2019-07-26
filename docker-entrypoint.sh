#!/bin/bash
set -Eeo pipefail

sleep 5

cd "${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}"
python3 manage.py migrate

gunicorn --chdir "${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}" --bind :${GUNICORN_PORT} vuedj.wsgi:application
