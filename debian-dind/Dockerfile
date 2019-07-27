FROM debian:stretch

############
## Docker ##
############
ARG DOCKER_CHANNEL=stable
ARG DOCKER_VERSION=18.09.8

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
RUN apt-get update && apt-get install -y --no-install-recommends docker-ce && \
  docker -v && \
  dockerd -v


#################
## DIND Script ##
#################
ENV DOCKER_EXTRA_OPTS '--storage-driver=overlay'
COPY dind_script.sh /usr/local/bin/dind
RUN chmod +x /usr/local/bin/dind


################
## Entrypoint ##
################
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh


VOLUME /var/lib/docker
EXPOSE 2375
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
