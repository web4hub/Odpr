#!/bin/bash
set -Eeo pipefail

sleep 5

cd /backend
python3 manage.py migrate

gunicorn --chdir /backend --bind :8000 vuedj.wsgi:application
