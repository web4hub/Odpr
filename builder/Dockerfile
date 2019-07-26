FROM docker.gitlab.electrocnic.com/dood/app/debian-dind:latest

ENV WORKING_DIRECTORY "${WORKING_DIRECTORY}"
ENV CLIENT_DIRECTORY "${CLIENT_DIRECTORY}"
ENV BACKEND_DIRECTORY "${BACKEND_DIRECTORY}"
ENV VERSION_DIRECTORY "${VERSION_DIRECTORY}"

RUN echo "args in Dockerfile: ${WORKING_DIRECTORY} ${CLIENT_DIRECTORY} ${BACKEND_DIRECTORY} ${VERSION_DIRECTORY}"

COPY . ${WORKING_DIRECTORY}

WORKDIR ${WORKING_DIRECTORY}

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
	&& curl -sL https://deb.nodesource.com/setup_12.x | bash - \
	&& apt-get install -y nodejs \
	&& node -v \
	&& npm -v \
	&& cd ${BACKEND_DIRECTORY} \
	&& python3 -m venv .venv \
	&& . .venv/bin/activate \
	&& pip3 install --upgrade pip \
	&& pip3 install -r requirements.txt

RUN cd ${CLIENT_DIRECTORY} \
	&& npm set progress=false \
	&& npm install -s --no-progress \
	&& npm audit fix \
	&& node_modules/.bin/cypress verify

RUN chmod 755 ${VERSION_DIRECTORY}/node_modules_checksum.sh ${VERSION_DIRECTORY}/pip_requirements_checksum.sh
