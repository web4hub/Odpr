FROM docker.gitlab.electrocnic.com/dood/app/debian-dind:latest

ARG REPO_COPY_DIRECTORY
ARG CLIENT_DIRECTORY
ARG BACKEND_DIRECTORY
ARG BUILDER_VERSION_SCRIPTS_SRC_DIRECTORY
ARG BUILDER_VERSION_SCRIPTS_DIRECTORY
ARG BUILDER_VENV_DIRECTORY
ARG BUILDER_NODE_MODULES_SRC_DIRECTORY

ENV REPO_COPY_DIRECTORY "${REPO_COPY_DIRECTORY}"
ENV CLIENT_DIRECTORY "${CLIENT_DIRECTORY}"
ENV BACKEND_DIRECTORY "${BACKEND_DIRECTORY}"
ENV BUILDER_VERSION_SCRIPTS_SRC_DIRECTORY "${BUILDER_VERSION_SCRIPTS_SRC_DIRECTORY}"
ENV BUILDER_VERSION_SCRIPTS_DIRECTORY "${BUILDER_VERSION_SCRIPTS_DIRECTORY}"
ENV BUILDER_VENV_DIRECTORY "${BUILDER_VENV_DIRECTORY}"
ENV BUILDER_NODE_MODULES_SRC_DIRECTORY "${BUILDER_NODE_MODULES_SRC_DIRECTORY}"

WORKDIR ${REPO_COPY_DIRECTORY}

COPY ${CLIENT_DIRECTORY}/package.json ${CLIENT_DIRECTORY}/
COPY ${CLIENT_DIRECTORY}/package.json ${BUILDER_VERSION_SCRIPTS_DIRECTORY}/
COPY ${BACKEND_DIRECTORY}/requirements.txt ${BACKEND_DIRECTORY}/
COPY ${BACKEND_DIRECTORY}/requirements.txt ${BUILDER_VERSION_SCRIPTS_DIRECTORY}/
COPY ${BUILDER_VERSION_SCRIPTS_SRC_DIRECTORY}/node_modules_checksum.sh ${BUILDER_VERSION_SCRIPTS_DIRECTORY}/
COPY ${BUILDER_VERSION_SCRIPTS_SRC_DIRECTORY}/pip_requirements_checksum.sh ${BUILDER_VERSION_SCRIPTS_DIRECTORY}/
COPY ${BUILDER_VERSION_SCRIPTS_SRC_DIRECTORY}/dockerfile_checksum.sh ${BUILDER_VERSION_SCRIPTS_DIRECTORY}/
COPY ${BUILDER_VERSION_SCRIPTS_SRC_DIRECTORY}/Dockerfile ${BUILDER_VERSION_SCRIPTS_DIRECTORY}/

RUN apt-get update \
	&& apt-get install -y \
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
	&& curl -sL https://deb.nodesource.com/setup_12.x | bash - \
	&& apt-get install -y nodejs \
	&& npm install -g npm \
	&& npm install -g lighthouse \
	&& node -v \
	&& npm -v \
	&& wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
	&& apt install -y ./google-chrome-stable_current_amd64.deb \
	&& cd "${REPO_COPY_DIRECTORY}/${BACKEND_DIRECTORY}" \
        && pip3 install anybadge \
	&& python3 -m venv "${BUILDER_VENV_DIRECTORY}" \
	&& . "${BUILDER_VENV_DIRECTORY}/bin/activate" \
	&& pip3 install --upgrade pip \
	&& pip3 install -r requirements.txt \
	&& pip3 install docker-compose \
	&& mkdir -p ~/.ssh \
	&& [ -f /.dockerenv ] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config

RUN cd ${REPO_COPY_DIRECTORY}/${CLIENT_DIRECTORY} \
	&& npm set progress=false \
	&& npm install -s --no-progress \
	&& npm audit fix \
	&& node_modules/.bin/cypress verify \
	&& mv node_modules "${BUILDER_NODE_MODULES_SRC_DIRECTORY}"

RUN chmod 755 ${BUILDER_VERSION_SCRIPTS_DIRECTORY}/*.sh
