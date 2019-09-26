#!/bin/bash
set -eo pipefail

/inject_env_into_file.sh GUNICORN_PORT /etc/nginx/conf.d/local.conf

/inject_env_into_file.sh NGINX_SERVER_NAME /etc/nginx/sites-customizations/local.80.conf
/inject_env_into_file.sh NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY /etc/nginx/sites-customizations/local.80.conf
/inject_env_into_file.sh NGINX_IMAGE_MEDIAFILES_DESTINATION_DIRECTORY /etc/nginx/sites-customizations/local.80.conf
/inject_env_into_file.sh NGINX_PERMANENT_REDIRECT_INSTRUCTION /etc/nginx/sites-customizations/local.80.conf --force

/inject_env_into_file.sh NGINX_SERVER_NAME /etc/nginx/sites-customizations/local.443.conf --force
/inject_env_into_file.sh NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY /etc/nginx/sites-customizations/local.443.conf --force
/inject_env_into_file.sh NGINX_IMAGE_MEDIAFILES_DESTINATION_DIRECTORY /etc/nginx/sites-customizations/local.443.conf --force

/inject_env_into_file.sh NGINX_SERVER_NAME /etc/nginx/sites-customizations/www.80.conf --force
/inject_env_into_file.sh NGINX_PERMANENT_REDIRECT_INSTRUCTION /etc/nginx/sites-customizations/www.80.conf --force

/inject_env_into_file.sh NGINX_SERVER_NAME /etc/nginx/sites-customizations/www.443.conf --force
/inject_env_into_file.sh NGINX_PERMANENT_REDIRECT_INSTRUCTION /etc/nginx/sites-customizations/www.443.conf --force
