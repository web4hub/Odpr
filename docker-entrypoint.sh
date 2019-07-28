#!/bin/bash
set -Eeo pipefail

sleep 5

cd "${APP_IMAGE_BACKEND_DIRECTORY}"
. "${APP_IMAGE_VENV_DIRECTORY}/bin/activate"
python3 manage.py migrate

gunicorn --chdir "${APP_IMAGE_BACKEND_DIRECTORY}" --bind :${GUNICORN_PORT} vuedj.wsgi:application
