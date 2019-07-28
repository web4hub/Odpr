FROM postgres:latest

ARG DJANGO_DATABASE_NAME
ARG DJANGO_DATABASE_USERNAME
ARG DJANGO_DATABASE_PASSWORD

ENV POSTGRES_DB "${DJANGO_DATABASE_NAME}"
ENV POSTGRES_USER "${DJANGO_DATABASE_USERNAME}"
ENV POSTGRES_PASSWORD "${DJANGO_DATABASE_PASSWORD}"

COPY ./docker-entrypoint.sh /usr/local/bin/
RUN rm /docker-entrypoint.sh \
	&& chmod 755 usr/local/bin/docker-entrypoint.sh \
	&& ln -s usr/local/bin/docker-entrypoint.sh /
