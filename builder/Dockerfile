FROM node:12.6-stretch

COPY builder/node_modules_checksum.sh .
COPY builder/pip_requirements_checksum.sh .

COPY client /client
COPY backend /backend

RUN apt update \
	&& apt install python3-pip python3-venv -y \
	&& python3 -m venv .venv \
	&& . .venv/bin/activate \
	&& pip3 install --upgrade pip \
	&& cd backend \
	&& pip3 install -r requirements.txt

RUN cd /client \
	&& npm set progress=false \
	&& npm install -s --no-progress \
	&& npm audit fix \
	&& node_modules/.bin/cypress verify

