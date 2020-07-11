FROM debian:buster

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		curl \
		git \
		gnupg2 \
		openssh-client \
		software-properties-common \
		wget \
	&& wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
	&& wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
	&& apt install -y ./google-chrome-stable_current_amd64.deb \
	&& curl -sL https://deb.nodesource.com/setup_14.x | bash - \
	&& apt-get install -y --no-install-recommends \
		nodejs \
	&& npm install -g npm \
	&& git clone https://github.com/prerender/prerender.git \
	&& cd prerender \
	&& npm install \
	&& npm audit fix

RUN echo 'alias google-chrome="google-chrome --no-sandbox"' >> ~/.bashrc

WORKDIR /prerender
RUN sed -i "s~scrollbars'~scrollbars', '--no-sandbox'~g" lib/browsers/chrome.js

EXPOSE 3000

CMD node server.js
