FROM nginx:latest

ARG NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY
ARG NGINX_IMAGE_MEDIAFILES_DESTINATION_DIRECTORY
ARG NGINX_PERMANENT_REDIRECT_INSTRUCTION
ARG NGINX_PRODUCTION_CONFIG
ARG CERTBOT_EMAIL
ARG GUNICORN_PORT
ARG NGINX_SERVER_NAME

ENV NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY "${NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY}"
ENV CERTBOT_EMAIL "${CERTBOT_EMAIL}"

# Provide a default debug config embedded in the image.
RUN rm "/etc/nginx/conf.d/default.conf"
COPY "nginx/conf.d/local.conf" "/etc/nginx/conf.d"
COPY "nginx/sites-customizations" "/etc/nginx/sites-customizations"
COPY "util/inject_env_into_file.sh" "/"
COPY "nginx/inject_config_values.sh" "/"
RUN chmod 755 "/inject_config_values.sh"
RUN "/inject_config_values.sh"
RUN cat "/etc/nginx/conf.d/*"
RUN cat "/etc/nginx/sites-customizations/*"
RUN rm "/inject_config_values.sh"
RUN rm "/inject_env_into_file.sh"
RUN [ -z $NGINX_PRODUCTION_CONFIG ] && rm /etc/nginx/sites-customizations/local.443.conf

# Frontend
COPY "${NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY}/static" "${NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY}"

# EXPOSE port to be used
EXPOSE 80
EXPOSE 443
