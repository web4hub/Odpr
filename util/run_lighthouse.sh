#!/bin/bash
set -eo pipefail

echo "Running lighthouse analysis..."
lighthouse "https://${TEST_PRODUCTION_DOMAIN}" --quiet --chrome-flags="--headless --no-sandbox" --no-enable-error-reporting --output-path=./report.html

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

echo "Get outdated pip dependencies through running app docker container..."
outdated_pip_dependencies=$(docker run -t --entrypoint pip "${APP_IMAGE_DEBUG}" list -o --format freeze | wc -l)
echo "Get list of outdated pip dependencies in pretty format..."
outdated_pip_dependencies_list=$(docker run -t --entrypoint pip "${APP_IMAGE_DEBUG}" list -o)
echo "Get list of all pip dependencies..."
all_pip_dependencies_list=$(docker run -t --entrypoint pip "${APP_IMAGE_DEBUG}" list)

dir=$(pwd)
echo "${dir}"
cd "${CLIENT_DIRECTORY}"
echo "cd to $(pwd)"
ls -la
echo "npm -v"
npm -v
echo "npm outdated"
echo "Get outdated npm package count through npm outdated in client directory..."
set +e # npm outdated returns 1 if found outdated packages
npm outdated
outdated_npm_packages=$(($(npm outdated | wc -l)-1))
echo "Get list of outdated npm packages in pretty format..."
outdated_npm_packages_list=$(npm outdated)
set -e
cd "${dir}"
echo "back in $(pwd)"

echo "Generate outdated report html..."
echo '<!doctype html>' > outdated.html
echo '<html lang="en">' >> outdated.html
echo '<head>' >> outdated.html
echo '<meta charset="utf-8">' >> outdated.html
echo '<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1">' >> outdated.html
echo '<title>Outdated Packages</title>' >> outdated.html
echo '</head>' >> outdated.html
echo '<body>' >> outdated.html
echo '<div>' >> outdated.html
echo '<h1>Outdated NPM Packages</h1>' >> outdated.html
echo '<p>' >> outdated.html
echo "${outdated_npm_packages_list}" >> outdated.html
echo '</p>' >> outdated.html
echo '</div>' >> outdated.html
echo '<div>' >> outdated.html
echo '<h1>Outdated pip dependencies</h1>' >> outdated.html
echo '<p>' >> outdated.html
echo "${outdated_pip_dependencies_list}" >> outdated.html
echo '</p>' >> outdated.html
echo '</div>' >> outdated.html
echo '<div>' >> outdated.html
echo '<h1>List of all pip dependencies</h1>' >> outdated.html
echo '<p>' >> outdated.html
echo "${all_pip_dependencies_list}" >> outdated.html
echo '</p>' >> outdated.html
echo '</div>' >> outdated.html
echo '</body>' >> outdated.html

echo "Prepare results for badge creation..."
if [ $performance -eq 1 ] || [ $performance -eq 0 ]; then
	performance="${performance}.0"
fi

if [ $accessibility -eq 1 ] || [ $accessibility -eq 0 ]; then
	accessibility="${accessibility}.0"
fi

if [ $best_practices -eq 1 ] || [ $best_practices -eq 0 ]; then
	best_practices="${best_practices}.0"
fi

if [ $seo -eq 1 ] || [ $seo -eq 0 ]; then
	seo="${seo}.0"
fi

if [ $outdated_pip_dependencies -le 0 ]; then
	outdated_pip_dependencies="up to date"
else
	outdated_pip_dependencies="${outdated_pip_dependencies} newer available"
fi

if [ $outdated_npm_packages -le 0 ]; then
	outdated_npm_packages="up to date"
else
	outdated_npm_packages="${outdated_npm_packages} newer available"
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
echo "Creating badge for outdated pip dependencies with value=\"${outdated_pip_dependencies}\""
anybadge -l "pip dependencies" -v "${outdated_pip_dependencies}" -f outdated_pip.svg 1=green 3=yellow 8=orange 1000=red
echo "Creating badge for outdated npm dependencies with value=\"${outdated_npm_packages}\""
anybadge -l "npm dependencies" -v "${outdated_npm_packages}" -f outdated_npm.svg 1=green 5=yellow 10=orange 1000=red

echo "in dir: $(pwd)"
ls -la
