FROM debian:buster

############
## Docker ##
############
ARG DOCKER_CHANNEL=stable
ARG DOCKER_VERSION=18.09.8

ARG DIND_VERSION_SCRIPTS_SRC_DIRECTORY
ARG DIND_VERSION_SCRIPTS_DIRECTORY

ENV DIND_VERSION_SCRIPTS_SRC_DIRECTORY "${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}"
ENV DIND_VERSION_SCRIPTS_DIRECTORY "${DIND_VERSION_SCRIPTS_DIRECTORY}"

COPY ${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}/Dockerfile ${DIND_VERSION_SCRIPTS_DIRECTORY}/
COPY ${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}/dind_script.sh ${DIND_VERSION_SCRIPTS_DIRECTORY}/
COPY ${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}/entrypoint.sh ${DIND_VERSION_SCRIPTS_DIRECTORY}/
COPY ${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}/image_checksum.sh ${DIND_VERSION_SCRIPTS_DIRECTORY}/
RUN chmod 755 ${DIND_VERSION_SCRIPTS_DIRECTORY}/image_checksum.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg2 \
  software-properties-common

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   ${DOCKER_CHANNEL}"

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash docker-ce \
  && docker -v \
  && dockerd -v

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    libgtk2.0-0 \
    libnotify-dev \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    libpq-dev \
    xvfb \
    curl \
    software-properties-common \
    wget \
    openssh-client \
    git \
  && curl -sL https://deb.nodesource.com/setup_12.x | bash - \
  && apt-get install -y nodejs \
  && npm install -g npm \
  && npm install -g lighthouse \
  && node -v \
  && npm -v \
  && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt install -y ./google-chrome-stable_current_amd64.deb


#################
## DIND Script ##
#################
ENV DOCKER_EXTRA_OPTS '--storage-driver=overlay'
COPY ${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}/dind_script.sh /usr/local/bin/dind
RUN chmod +x /usr/local/bin/dind


################
## Entrypoint ##
################
COPY ${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh


VOLUME /var/lib/docker
EXPOSE 2375
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
