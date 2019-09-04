#!/bin/bash
set -eo pipefail

lighthouse "https://${TEST_PRODUCTION_DOMAIN}" --quiet --chrome-flags="--headless --no-sandbox" --no-enable-error-reporting --output-path=./report.html

performance=$(cat report.html | sed -rn 's~^.*("id":"performance","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')
accessibility=$(cat report.html | sed -rn 's~^.*("id":"accessibility","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')
best_practices=$(cat report.html | sed -rn 's~^.*("id":"best-practices","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')
seo=$(cat report.html | sed -rn 's~^.*("id":"seo","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')

nginx_version=$(docker run -t --entrypoint nginx "${NGINX_IMAGE_DEBUG}" -v | sed -rn 's~^.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')
postgres_version=$(docker run -t --entrypoint postgres "${POSTGRES_IMAGE_DEBUG}" -V | sed -rn 's~^.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')

webpack_version=$(cat "${CLIENT_DIRECTORY}/package.json" | sed -rn 's~^.*"webpack":.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')
vue_version=$(cat "${CLIENT_DIRECTORY}/package.json" | sed -rn 's~^.*"vue":.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')
django_version=$(cat "${BACKEND_DIRECTORY}/requirements.txt" | sed -rn 's~^.*Django==.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')

anybadge -l version -v ${CI_BUILD_TAG} -f latest_release_tag.svg -c '#00FF00'
anybadge -l nginx -v ${nginx_version} -f nginx_version.svg -c '#008080'
anybadge -l postgres -v ${postgres_version} -f postgres_version.svg -c '#008080'
anybadge -l webpack -v ${webpack_version} -f webpack_version.svg -c '#008080'
anybadge -l vue -v ${vue_version} -f vue_version.svg -c '#008080'
anybadge -l django -v ${django_version} -f django_version.svg -c '#008080'
anybadge -l "lighthouse performance" -v ${performance} -f performance.svg 0.4=red 0.6=orange 0.8=yellow 1.01=green
anybadge -l "lighthouse accessibility" -v ${accessibility} -f accessibility.svg 0.4=red 0.6=orange 0.8=yellow 1.01=green
anybadge -l "lighthouse best practices" -v ${best_practices} -f best_practices.svg 0.4=red 0.6=orange 0.8=yellow 1.01=green
anybadge -l "lighthouse search engine results ranking" -v ${seo} -f search_engine_results_ranking.svg 0.4=red 0.6=orange 0.8=yellow 1.01=green
