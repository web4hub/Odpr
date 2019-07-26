FROM docker.gitlab.electrocnic.com/dood/app/debian-dind:latest

ENV WORKING_DIRECTORY "${working_directory}"
ENV CLIENT_DIRECTORY "${client_directory}"
ENV BACKEND_DIRECTORY "${backend_directory}"
ENV VERSION_DIRECTORY "${version_directory}"

COPY . ${working_directory}

WORKDIR ${working_directory}

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
	&& cd ${backend_directory} \
	&& python3 -m venv .venv \
	&& . .venv/bin/activate \
	&& pip3 install --upgrade pip \
	&& pip3 install -r requirements.txt

RUN cd ${client_directory} \
	&& npm set progress=false \
	&& npm install -s --no-progress \
	&& npm audit fix \
	&& node_modules/.bin/cypress verify

RUN chmod 755 ${version_directory}/node_modules_checksum.sh ${version_directory}/pip_requirements_checksum.sh
