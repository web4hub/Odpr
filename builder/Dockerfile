FROM docker.gitlab.electrocnic.com/dood/app/debian-dind:latest

COPY builder/node_modules_checksum.sh .
COPY builder/pip_requirements_checksum.sh .

COPY client "${CI_BUILDS_DIR}"/client
COPY backend "${CI_BUILDS_DIR}"/backend

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
	&& cd "${CI_BUILDS_DIR}"/backend \
	&& python3 -m venv .venv \
	&& . .venv/bin/activate \
	&& pip3 install --upgrade pip \
	&& pip3 install -r requirements.txt

RUN cd "${CI_BUILDS_DIR}"/client \
	&& npm set progress=false \
	&& npm install -s --no-progress \
	&& npm audit fix \
	&& node_modules/.bin/cypress verify

RUN chmod 755 node_modules_checksum.sh pip_requirements_checksum.sh
