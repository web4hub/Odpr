#!/bin/bash
set -Eeo pipefail

sleep 5

cd "${BACKEND_DIRECTORY}"
python3 manage.py migrate

gunicorn --chdir "${BACKEND_DIRECTORY}" --bind :${GUNICORN_PORT} vuedj.wsgi:application
