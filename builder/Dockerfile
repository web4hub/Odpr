FROM node:12.6-stretch

COPY builder/node_modules_checksum.sh .
COPY builder/pip_requirements_checksum.sh .

COPY client /client
COPY backend /backend

RUN apt update \
	&& apt install python3-pip \
	&& pip3 install --upgrade pip \
	&& cd backend \
	&& python3 -m venv .venv \
	&& pip3 install -r requirements.txt

RUN cd /client && npm install

