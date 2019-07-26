FROM python:buster

ENV WORKING_DIRECTORY "${working_directory}"
ENV CLIENT_DIRECTORY "${client_directory}"
ENV BACKEND_DIRECTORY "${backend_directory}"
ENV VERSION_DIRECTORY "${version_directory}"
ENV GUNICORN_PORT "${gunicorn_port}"

COPY "${backend_directory}" "${backend_directory}"
COPY docker-entrypoint.sh /
# staticfiles are not copied here because the nginx-container will contain them and serve them directly
RUN mkdir -p /static
RUN mkdir -p /client/static

# EXPOSE port to be used
EXPOSE 80
EXPOSE 443
EXPOSE 8000

# Set command to run as soon as container is up
CMD ["/docker-entrypoint.sh"]
