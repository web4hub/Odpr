FROM nginx:latest

ARG NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY
ARG NGINX_PRODUCTION_CONFIG

ENV NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY "${NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY}"

# Provide a default debug config embedded in the image.
RUN rm "/etc/nginx/conf.d/default.conf"
COPY "nginx/conf.d/local.conf" "/etc/nginx/conf.d"
COPY "nginx/sites-customizations" "/etc/nginx/sites-customizations"
RUN [ -z $NGINX_PRODUCTION_CONFIG ] && rm /etc/nginx/sites-customizations/local.443.conf

# Frontend
COPY "${NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY}/static" "${NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY}"

# EXPOSE port to be used
EXPOSE 80
EXPOSE 443
EXPOSE 8000
