FROM docker.gitlab.electrocnic.com/dood/app/debian-dind:latest

ARG WORKING_DIRECTORY
ARG CLIENT_DIRECTORY
ARG BACKEND_DIRECTORY
ARG VERSION_DIRECTORY
ENV WORKING_DIRECTORY "${WORKING_DIRECTORY}"
ENV CLIENT_DIRECTORY "${CLIENT_DIRECTORY}"
ENV BACKEND_DIRECTORY "${BACKEND_DIRECTORY}"
ENV VERSION_DIRECTORY "${VERSION_DIRECTORY}"

RUN pwd
RUN ls -la
COPY ${CLIENT_DIRECTORY}/package.json ${WORKING_DIRECTORY}/${CLIENT_DIRECTORY}/
COPY ${BACKEND_DIRECTORY}/requirements.txt ${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}/
RUN ls -la
RUN echo "${WORKING_DIRECTORY}"
RUN ls -la ${WORKING_DIRECTORY}
RUN find / -iname "*backend*"
RUN find / -iname "*client*"

WORKDIR ${WORKING_DIRECTORY}
RUN pwd
RUN ls -la

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
	&& cd "${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}" \
	&& python3 -m venv .venv \
	&& . .venv/bin/activate \
	&& pip3 install --upgrade pip \
	&& pip3 install -r requirements.txt

RUN cd ${WORKING_DIRECTORY}/${CLIENT_DIRECTORY} \
	&& npm set progress=false \
	&& npm install -s --no-progress \
	&& npm audit fix \
	&& node_modules/.bin/cypress verify \
	&& mkdir -p "${WORKING_DIRECTORY}/${CLIENT_DIRECTORY}/static"

RUN chmod 755 ${WORKING_DIRECTORY}/${VERSION_DIRECTORY}/node_modules_checksum.sh ${WORKING_DIRECTORY}/${VERSION_DIRECTORY}/pip_requirements_checksum.sh
