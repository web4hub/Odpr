FROM python:buster

ARG WORKING_DIRECTORY
ARG CLIENT_DIRECTORY
ARG BACKEND_DIRECTORY
ARG VERSION_DIRECTORY
ARG GUNICORN_PORT
ENV WORKING_DIRECTORY "${WORKING_DIRECTORY}"
ENV CLIENT_DIRECTORY "${CLIENT_DIRECTORY}"
ENV BACKEND_DIRECTORY "${BACKEND_DIRECTORY}"
ENV VERSION_DIRECTORY "${VERSION_DIRECTORY}"
ENV GUNICORN_PORT "${GUNICORN_PORT}"

COPY "${BACKEND_DIRECTORY}" "${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}"
COPY docker-entrypoint.sh /
RUN chmod 755 /docker-entrypoint.sh
# staticfiles are not copied here because the nginx-container will contain them and serve them directly


# EXPOSE port to be used
EXPOSE 80
EXPOSE 443
EXPOSE 8000

# Set command to run as soon as container is up
CMD ["/docker-entrypoint.sh"]
