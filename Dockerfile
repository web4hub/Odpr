FROM python:buster

COPY /backend /backend
COPY docker-entrypoint.sh /
# staticfiles are not copied here because the nginx-container will contain them and serve them directly

# EXPOSE port to be used
EXPOSE 80
EXPOSE 443
EXPOSE 8000

# Set command to run as soon as container is up
CMD ["/docker-entrypoint.sh"]
