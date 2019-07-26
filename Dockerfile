FROM python:buster

ENV WORKING_DIRECTORY "${WORKING_DIRECTORY}"
ENV CLIENT_DIRECTORY "${CLIENT_DIRECTORY}"
ENV BACKEND_DIRECTORY "${BACKEND_DIRECTORY}"
ENV VERSION_DIRECTORY "${VERSION_DIRECTORY}"
ENV GUNICORN_PORT "${GUNICORN_PORT}"

COPY "${BACKEND_DIRECTORY}" "${BACKEND_DIRECTORY}"
COPY docker-entrypoint.sh "${WORKING_DIRECTORY}"/
# staticfiles are not copied here because the nginx-container will contain them and serve them directly
RUN mkdir -p /static
RUN mkdir -p "${CLIENT_DIRECTORY}"/static

# EXPOSE port to be used
EXPOSE 80
EXPOSE 443
EXPOSE 8000

# Set command to run as soon as container is up
CMD ["${WORKING_DIRECTORY}/docker-entrypoint.sh"]
