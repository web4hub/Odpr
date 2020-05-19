#!/bin/bash

export APP_IMAGE="registry.gitlab.com/electrocnic/vue-django-ci-cd-boilerplate/app:latest"
export NGINX_IMAGE="registry.gitlab.com/electrocnic/vue-django-ci-cd-boilerplate/nginx:latest"
export POSTGRES_IMAGE="registry.gitlab.com/electrocnic/vue-django-ci-cd-boilerplate/postgres:latest"
export HOST_PORT=8000

docker-compose up
