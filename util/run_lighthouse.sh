#!/bin/bash
set -eo pipefail

lighthouse "https://${TEST_PRODUCTION_DOMAIN}" --quiet --chrome-flags="--headless --no-sandbox" --no-enable-error-reporting --output-path=./report.html

export performance=$(cat report.html | sed -rn 's~^.*("id":"performance","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')
export accessibility=$(cat report.html | sed -rn 's~^.*("id":"accessibility","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')
export best_practices=$(cat report.html | sed -rn 's~^.*("id":"best-practices","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')
export seo=$(cat report.html | sed -rn 's~^.*("id":"seo","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')

export nginx_version=$(docker run -ti --entrypoint nginx "${NGINX_IMAGE_DEBUG}" -v | sed -rn 's~^.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+)$~\1~p')
export postgres_version=$(docker run -ti --entrypoint postgres "${POSTGRES_IMAGE_DEBUG}" -V | sed -rn 's~^.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+)$~\1~p')

export webpack_version=$(cat "${CLIENT_DIRECTORY}/package.json" | sed -rn 's~^.*"webpack":.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')
export vue_version=$(cat "${CLIENT_DIRECTORY}/package.json" | sed -rn 's~^.*"vue":.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')
export django_version=$(cat "${BACKEND_DIRECTORY}/requirements.txt" | sed -rn 's~^.*Django==.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')
