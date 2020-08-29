FROM alpine:latest

# Installs latest Chromium package.
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/v3.11/main" >> /etc/apk/repositories \
    && apk upgrade -U -a \
    && apk add --no-cache \
      libstdc++ \
      chromium \
      harfbuzz \
      nss \
      freetype \
      ttf-freefont \
      wqy-zenhei \
    && rm -rf /var/cache/* \
    && mkdir /var/cache/apk \
    && mkdir -p /usr/src/app \
    && adduser -D chrome \
    && chown -R chrome:chrome /usr/src/app \
    && cd /usr/src/app \
    && apk add --no-cache git nodejs nodejs-npm \
    && git clone https://github.com/prerender/prerender.git \
    && cd prerender \
    && npm install \
    && npm install prerender-memory-cache \
    && npm audit fix \
    && apk del nodejs-npm \
    && apk del $(apk info | grep -v node | grep -v chrom) \
    && rm -rf /var/lib/apt/lists/* \
          /var/cache/apk/* \
          /usr/share/man \
          /tmp/* \
    && sed -i "s~scrollbars'~scrollbars', '--no-sandbox'~g" lib/browsers/chrome.js \
    && sed -i "s~google-chrome~chromium-browser~g" lib/browsers/chrome.js \
    && sed -i "s~require('./lib');~require('./lib');\nconst cache = require('prerender-memory-cache');~g" server.js \
    && sed -i "s~httpHeaders());~httpHeaders());\nserver.use(cache);~g" server.js

ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_PATH=/usr/lib/chromium/ \
    CACHE_MAXSIZE=10000 \
    CACHE_TTL=604800

EXPOSE 3000

WORKDIR /usr/src/app/prerender

ENTRYPOINT node server.js
