#!/bin/bash

export PRODUCTION_DOMAIN="localhost"
export DEBUG_URL="http://${PRODUCTION_DOMAIN}:${GUNICORN_PORT}/"

# Docker images
#
export CI_BUILD_TAG="local-build-production"
export CI_PROJECT_PATH="local-build"
export DOCKER_REGISTRY="registry.gitlab.com"
export BASE_IMAGE="docker:dind"
export DIND_IMAGE="${DOCKER_REGISTRY}/${CI_PROJECT_PATH}/debian-dind:latest"
export BUILDER_IMAGE="${DOCKER_REGISTRY}/${CI_PROJECT_PATH}/builder:latest"
export APP_IMAGE_DEBUG="${DOCKER_REGISTRY}/${CI_PROJECT_PATH}/app"
export NGINX_IMAGE_DEBUG="${DOCKER_REGISTRY}/${CI_PROJECT_PATH}/nginx"
export POSTGRES_IMAGE_DEBUG="${DOCKER_REGISTRY}/${CI_PROJECT_PATH}/postgres"
export APP_IMAGE_PRODUCTION_TEST="${APP_IMAGE_DEBUG}:${CI_BUILD_TAG}-test"
export NGINX_IMAGE_PRODUCTION_TEST="${NGINX_IMAGE_DEBUG}:${CI_BUILD_TAG}-test"
export POSTGRES_IMAGE_PRODUCTION_TEST="${POSTGRES_IMAGE_DEBUG}:${CI_BUILD_TAG}-test"
export APP_IMAGE_PRODUCTION="${APP_IMAGE_DEBUG}:${CI_BUILD_TAG}"
export NGINX_IMAGE_PRODUCTION="${NGINX_IMAGE_DEBUG}:${CI_BUILD_TAG}"
export POSTGRES_IMAGE_PRODUCTION="${POSTGRES_IMAGE_DEBUG}:${CI_BUILD_TAG}"
#
# Directories
#
export CI_PROJECT_DIR="/project"
export CLIENT_DIRECTORY="client"
export BACKEND_DIRECTORY="backend"
export DIND_VERSION_SCRIPTS_SRC_DIRECTORY="debian-dind"
export DIND_VERSION_SCRIPTS_DIRECTORY="/version"
export BUILDER_VERSION_SCRIPTS_SRC_DIRECTORY="builder"
export BUILDER_VENV_DIRECTORY="/.venv"
export BUILDER_VERSION_SCRIPTS_DIRECTORY="/version"
export BUILDER_NODE_MODULES_SRC_DIRECTORY="/node_modules"
export BUILDER_NODE_MODULES_DESTINATION_DIRECTORY="${CI_PROJECT_DIR}/${CLIENT_DIRECTORY}/node_modules"
export BUILDER_STATIC_SRC_DIRECTORY="${CI_PROJECT_DIR}/${CLIENT_DIRECTORY}/${STATICFILES_DIRNAME}/static"
export STATICFILES_DIRNAME='static'
export MEDIAFILES_DIRNAME='media'
export NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY="/${STATICFILES_DIRNAME}"
export NGINX_IMAGE_MEDIAFILES_DESTINATION_DIRECTORY="/${MEDIAFILES_DIRNAME}"
export APP_IMAGE_VENV_DIRECTORY="/.venv"
export APP_IMAGE_BACKEND_DIRECTORY="/backend"
export APP_INDEX_HTML_TEMPLATE_DIRECTORY="templates/index.html"
#
# Vue/Webpack Settings
#
export VUE_DEBUG="true" # (true or false)  (defined here and in jobs)
#
# Django Settings (some of them are defined in the gitlab variables page and are commented here)
#
export DJANGO_SECRET_KEY_DEBUG="L62VY92iganbgBaZPcx6VWK24F2MSzegTRt4f4U7yG7LwUS3UN" #  (defined in gitlab)
export DJANGO_SECRET_KEY_TEST="HUMDuifZBPGA54ADY2e3kPBCSVYLX4r6icFynn67Du9kEEJ52G" #  (defined in gitlab)
export DJANGO_SECRET_KEY="HFZAxnpvi84CSnCMiZriX4r37SCU9zNM5Z7y2DcoDQ733z56Ra" #  (defined in gitlab)
export DJANGO_DEBUG="True" # (True or False)  (defined here)
#
# Django Database settings
#
export DJANGO_DATABASE_NAME="database1" #  (e.g. 'database1')  (defined in gitlab variables)
export DJANGO_DATABASE_USERNAME="postgres_django" #  (defined in gitlab variables)
export DJANGO_DATABASE_PASSWORD_DEBUG="y55k9nC4YV7r3Uny49JiG6qYFMxZ2W5Vwx9n6BJW" #  (defined in gitlab variables)
export DJANGO_DATABASE_PASSWORD_TEST="6EeV2E9GGkZZ343MVF8iXp2MYp4qQRvYuJYQL3D5" #  (defined in gitlab variables)
export DJANGO_DATABASE_PASSWORD="4vSiJQk2RdaYWBRbY3R3E64M4jS8T65YCBZ86dG3" #  (defined in gitlab variables)
export DJANGO_DATABASE_PORT=5432
export DJANGO_DATABASE_HOST="database1" #  (must be the same name as the docker-compose service, e.g 'database1')  (defined in gitlab)
#
# Django allowed host domains (optional)
#
export DJANGO_ALLOWED_HOST_1="${PRODUCTION_DOMAIN}" #  (defined in release-job)
export DJANGO_ALLOWED_HOST_2="www.${PRODUCTION_DOMAIN}" #  (defined in release-job)
# DJANGO_ALLOWED_HOST_3  (define it in gitlab variables)
# DJANGO_ALLOWED_HOST_4  (define it in gitlab variables)
#
# Django staticfiles settings
#
export DJANGO_STATICFILES_RELATIVE_TO_BACKEND_DIRECTORY="../${CLIENT_DIRECTORY}/${STATICFILES_DIRNAME}" #  (default = '../client/static-vuedj')
export DJANGO_STATIC_ROOT_RELATIVE_TO_BACKEND_DIRECTORY="../${STATICFILES_DIRNAME}/static" #  (default = '../staticfiles/static')
export DJANGO_MEDIA_ROOT_RELATIVE_TO_BACKEND_DIRECTORY="../media" #  (default = '../staticfiles/media')
export DJANGO_STATIC_URL="/${STATICFILES_DIRNAME}/" #     (default = '/static-vuedj/')
export DJANGO_MEDIA_URL="/${MEDIAFILES_DIRNAME}/" #       (default = '/media/')
#
# Misc
#
export GUNICORN_PORT=8000 # inner port of the App-Docker-Container (exposed to nginx)
export HOST_PORT=8000 # port of gitlab-ci runner container which runs cypress to test the app on app@localhost:HOST_PORT
# NGINX_PRODUCTION_CONFIG  (defined in release-job locally).
# PRODUCTION_URL  (defined in release-job locally. If defined, will overwrite DEBUG_URL. Should be in the format="https://my.site.com/" (don't forget the trailing slash))
export NGINX_SERVER_NAME="localhost"
# NGINX_PERMANENT_REDIRECT_INSTRUCTION="" # (defined in release-job locally). Leave empty for debug builds.

