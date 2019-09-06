#!/bin/bash
set -eo pipefail

echo "Get outdated pip dependencies through running app docker container..."
outdated_pip_dependencies=$(docker run -t --entrypoint pip "${APP_IMAGE_DEBUG}" list -o --format freeze | wc -l)
echo "Get list of outdated pip dependencies in pretty format..."
outdated_pip_dependencies_list=$(docker run -t --entrypoint pip "${APP_IMAGE_DEBUG}" list -o | awk '{ if(NR > 2) { printf "<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n", $1, $2, $3 } }')
echo "Get list of all pip dependencies..."
all_pip_dependencies_list=$(docker run -t --entrypoint pip "${APP_IMAGE_DEBUG}" list | awk '{ if(NR > 2) { printf "<tr><td>%s</td><td>%s</td></tr>\n", $1, $2 } }')

dir=$(pwd)
cd "${CLIENT_DIRECTORY}"
echo "Get outdated npm package count through npm outdated in client directory..."
set +e # npm outdated returns 1 if found outdated packages
outdated_npm_packages=$(($(npm outdated | wc -l)-1))
echo "Get list of outdated npm packages in pretty format..."
outdated_npm_packages_list=$(npm outdated | awk '{ if(NR > 1) { printf "<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n", $1, $2, $4 } }')
set -e
cd "${dir}"

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
echo '<table>' >> outdated.html
echo '<tr><th>Package</th><th>Current</th><th>Latest</th></tr>' >> outdated.html
echo "${outdated_npm_packages_list}" >> outdated.html
echo '</table>' >> outdated.html
echo '</div>' >> outdated.html
echo '<div>' >> outdated.html
echo '<h1>Outdated pip dependencies</h1>' >> outdated.html
echo '<table>' >> outdated.html
echo '<tr><th>Package</th><th>Current</th><th>Latest</th></tr>' >> outdated.html
echo "${outdated_pip_dependencies_list}" >> outdated.html
echo '</table>' >> outdated.html
echo '</div>' >> outdated.html
echo '<div>' >> outdated.html
echo '<h1>List of all pip dependencies</h1>' >> outdated.html
echo '<table>' >> outdated.html
echo '<tr><th>Package</th><th>Version</th></tr>' >> outdated.html
echo "${all_pip_dependencies_list}" >> outdated.html
echo '</table>' >> outdated.html
echo '</div>' >> outdated.html
echo '</body>' >> outdated.html

if [ $outdated_pip_dependencies -le 0 ]; then
	pip_color="green"
	outdated_pip_dependencies="up to date"
else
	if [ $outdated_pip_dependencies -le 2 ]; then
		pip_color="yellow"
	elif [ $outdated_pip_dependencies -le 7 ]; then
		pip_color="orange"
	else
		pip_color="red"
	fi
	outdated_pip_dependencies="${outdated_pip_dependencies} newer available"
fi

if [ $outdated_npm_packages -le 0 ]; then
	npm_color="green"
	outdated_npm_packages="up to date"
else
	if [ $outdated_npm_packages -le 4 ]; then
		npm_color="yellow"
	elif [ $outdated_npm_packages -le 9 ]; then
		npm_color="orange"
	else
		npm_color="red"
	fi
	outdated_npm_packages="${outdated_npm_packages} newer available"
fi

echo "Creating badge for outdated pip dependencies with value=\"${outdated_pip_dependencies}\""
anybadge -l "pip dependencies" -v "${outdated_pip_dependencies}" -f outdated_pip.svg -c "${pip_color}"
echo "Creating badge for outdated npm dependencies with value=\"${outdated_npm_packages}\""
anybadge -l "npm dependencies" -v "${outdated_npm_packages}" -f outdated_npm.svg -c "${npm_color}"

