#!/bin/bash
set -eo pipefail

echo "Running lighthouse analysis..."
lighthouse "https://${PRODUCTION_DOMAIN}" --quiet --chrome-flags="--headless --no-sandbox" --no-enable-error-reporting --output-path=./report.html

echo "Parse lighthouse results from generated report.html..."
performance=$(cat report.html | sed -rn 's~^.*("id":"performance","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')
accessibility=$(cat report.html | sed -rn 's~^.*("id":"accessibility","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')
best_practices=$(cat report.html | sed -rn 's~^.*("id":"best-practices","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')
seo=$(cat report.html | sed -rn 's~^.*("id":"seo","score":)([[:digit:]]\.?[[:digit:]]{0,2}).*$~\2~p')

echo "Get nginx version by starting nginx docker container..."
nginx_version=$(docker run -t --entrypoint nginx "${NGINX_IMAGE_DEBUG}" -v | sed -rn 's~^.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')
echo "Get postgres version by starting postgres docker container..."
postgres_version=$(docker run -t --entrypoint postgres "${POSTGRES_IMAGE_DEBUG}" -V | sed -rn 's~^.*\s([[:digit:]]+\.[[:digit:]]+\.?[[:digit:]]*).*$~\1~p')

echo "Get webpack version through package.json"
webpack_version=$(cat "${CLIENT_DIRECTORY}/package.json" | sed -rn 's~^.*"webpack":.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')
echo "Get vue version through package.json"
vue_version=$(cat "${CLIENT_DIRECTORY}/package.json" | sed -rn 's~^.*"vue":.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')
echo "Get django version through requirements.txt"
django_version=$(cat "${BACKEND_DIRECTORY}/requirements.txt" | sed -rn 's~^.*Django==.*([[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+).*$~\1~p')

echo "Prepare results for badge creation..."
if [ $performance -eq 1 ] || [ $performance -eq 0 ]; then # This might produce a warning/error "Integer expression expected" - Can be ignored.
	performance="${performance}.0"
fi

if [ $accessibility -eq 1 ] || [ $accessibility -eq 0 ]; then # This might produce a warning/error "Integer expression expected" - Can be ignored.
	accessibility="${accessibility}.0"
fi

if [ $best_practices -eq 1 ] || [ $best_practices -eq 0 ]; then # This might produce a warning/error "Integer expression expected" - Can be ignored.
	best_practices="${best_practices}.0"
fi

if [ $seo -eq 1 ] || [ $seo -eq 0 ]; then # This might produce a warning/error "Integer expression expected" - Can be ignored.
	seo="${seo}.0"
fi

echo "Creating badge for project version with version=\"${CI_BUILD_TAG}\""
anybadge -l version -v ${CI_BUILD_TAG} -f latest_release_tag.svg -c '#00FF00'
echo "Creating badge for nginx version with version=\"${nginx_version}\""
anybadge -l nginx -v ${nginx_version} -f nginx_version.svg -c '#008080'
echo "Creating badge for postgres version with version=\"${postgres_version}\""
anybadge -l postgres -v ${postgres_version} -f postgres_version.svg -c '#008080'
echo "Creating badge for webpack version with version=\"${webpack_version}\""
anybadge -l webpack -v ${webpack_version} -f webpack_version.svg -c '#008080'
echo "Creating badge for vue version with version=\"${vue_version}\""
anybadge -l vue -v ${vue_version} -f vue_version.svg -c '#008080'
echo "Creating badge for django version with version=\"${django_version}\""
anybadge -l django -v ${django_version} -f django_version.svg -c '#008080'
echo "Creating badge for lighthouse performance with value=\"${performance}\""
anybadge -l "lighthouse performance" -v ${performance} -f performance.svg 0.55=red 0.8=orange 0.9=yellow 1.01=green
echo "Creating badge for lighthouse accessibility with value=\"${accessibility}\""
anybadge -l "lighthouse accessibility" -v ${accessibility} -f accessibility.svg 0.55=red 0.8=orange 0.9=yellow 1.01=green
echo "Creating badge for lighthouse best practices with value=\"${best_practices}\""
anybadge -l "lighthouse best practices" -v ${best_practices} -f best_practices.svg 0.55=red 0.8=orange 0.9=yellow 1.01=green
echo "Creating badge for lighthouse search engine results ranking with value=\"${seo}\""
anybadge -l "lighthouse search engine results ranking" -v ${seo} -f search_engine_results_ranking.svg 0.55=red 0.8=orange 0.9=yellow 1.01=green

util/update_dependency_badges.sh
