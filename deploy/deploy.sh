#!/bin/bash
set -eo pipefail

cd "$(dirname "$0")"

source ../util/scp_ssh_wrapper.sh

help() {
	echo "Usage: $0"
	echo "  Remote-scp and remote-ssh to (production) deploy-server to copy the nginx-proxy files if not already there,"
	echo "  plus copy the app's docker-compose file if not already there, and the start the nginx-proxy if not"
	echo "  already running, and then start or restart the app (with updating the docker images of the app if"
	echo "  it is not the first time deploy but an update deploy)."
}

delete_old_app_images_on_server() {
	set +e
	OLD_IMAGES=$(ssh "${DEPLOY_SERVER_USER}@${DEPLOY_SERVER_IP}" "docker-compose -f apps/${NGINX_SERVER_NAME}/docker-compose.yml images -q 2>/dev/null")
	while read -r line; do
		ssh_proxy "docker image rm --force ${line} 2>/dev/null"
	done <<< "${OLD_IMAGES}"
	set -e
}

make_app_directory() {
	set -e
	ssh_proxy "mkdir -p apps/${NGINX_SERVER_NAME}/re-encrypt-certs"
	ssh_proxy "mkdir -p apps/${NGINX_SERVER_NAME}/gitlab-badges"
	ssh_proxy "mkdir -p apps/${NGINX_SERVER_NAME}/crawlers"
	set +e
}

make_nginx_proxy_directories() {
	set -e
	ssh_proxy "mkdir -p nginx-proxy/config/template"
	set +e
}

scp_start_script() {
	make_nginx_proxy_directories
	set -e
	scp_proxy "nginx-proxy/nginx-proxy.sh" "~/nginx-proxy/"
	ssh_proxy "chmod 755 nginx-proxy/nginx-proxy.sh"
	set +e
}

scp_docker_compose() {
	make_nginx_proxy_directories
	set -e
	scp_proxy "nginx-proxy/config/docker-compose.yml" "~/nginx-proxy/config/"
	set +e
}

scp_template() {
	make_nginx_proxy_directories
	set -e
	scp_proxy "nginx-proxy/config/template/nginx.tmpl" "~/nginx-proxy/config/template/"
	set +e
}

set +e
scp_start_script
scp_docker_compose
scp_template
set -e

echo "Files for nginx-proxy copied or updated, now starting nginx-proxy if not running..."

ssh_proxy "nginx-proxy/nginx-proxy.sh start"
ssh_proxy "nginx-proxy/nginx-proxy.sh status"

echo "Nginx-proxy should now be up and running. Copying app..."
make_app_directory
set -e
# Inject app name into start script/docker-compose.yml of app:
chmod 755 ../util/*.sh
../util/inject_parameter_into_file.sh APP_NAME "${NGINX_SERVER_NAME}" app/app.sh
../util/inject_env_into_file.sh DOCKER_USER app/app.sh
../util/inject_env_into_file.sh DOCKER_PW app/app.sh
../util/inject_env_into_file.sh DOCKER_REGISTRY app/app.sh
../util/inject_env_into_file.sh APP_IMAGE_NAME app/docker-compose.yml
../util/inject_env_into_file.sh NGINX_IMAGE_NAME app/docker-compose.yml
../util/inject_env_into_file.sh POSTGRES_IMAGE_NAME app/docker-compose.yml
../util/inject_env_into_file.sh PRERENDER_IMAGE_NAME app/docker-compose.yml
delete_old_app_images_on_server
scp_proxy "app/docker-compose.yml" "~/apps/${NGINX_SERVER_NAME}/"
scp_proxy "app/app.sh" "~/apps/${NGINX_SERVER_NAME}/"
for f in app/re-encrypt-certs/*; do
	scp_proxy "${f}" "~/apps/${NGINX_SERVER_NAME}/re-encrypt-certs/"
done

export CURRENT_DATE="$(date -I)"
../util/inject_env_into_file.sh CURRENT_DATE app/crawlers/sitemap.xml
for f in app/crawlers/*; do
	../util/inject_env_into_file.sh PRODUCTION_URL "${f}"
	scp_proxy "${f}" "~/apps/${NGINX_SERVER_NAME}/crawlers/"
done
ssh_proxy "chmod 755 apps/${NGINX_SERVER_NAME}/app.sh"

echo "Copied app configuration to server. Updating images and deploying now..."
ssh_proxy "apps/${NGINX_SERVER_NAME}/app.sh update"

echo "Deploy finished, your app should be reachable in a few seconds/minutes at ${NGINX_SERVER_NAME}"
