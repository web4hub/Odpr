#!/bin/bash
set -eo pipefail

cd "$(dirname "$0")"

help() {
	echo "Usage: $0"
	echo "  Remote-scp and remote-ssh to (production) deploy-server to copy the nginx-proxy files if not already there,"
	echo "  plus copy the app's docker-compose file if not already there, and the start the nginx-proxy if not"
	echo "  already running, and then start or restart the app (with updating the docker images of the app if"
	echo "  it is not the first time deploy but an update deploy)."
}

delete_old_app_images_on_server() {
	set +e
	OLD_IMAGES=$(ssh gitlab@$DEPLOY_SERVER_IP "docker-compose -f apps/${NGINX_SERVER_NAME}/docker-compose.yml images -q 2>/dev/null")
	while read -r line; do
    ssh gitlab@$DEPLOY_SERVER_IP "docker image rm --force ${line} 2>/dev/null"
	done <<< "${OLD_IMAGES}"
	set -e
}

make_app_directory() {
	set -e
	ssh gitlab@$DEPLOY_SERVER_IP "mkdir -p apps/${NGINX_SERVER_NAME}/re-encrypt-certs"
	ssh gitlab@$DEPLOY_SERVER_IP "mkdir -p apps/${NGINX_SERVER_NAME}/gitlab-badges"
	ssh gitlab@$DEPLOY_SERVER_IP "mkdir -p apps/${NGINX_SERVER_NAME}/crawlers"
	set +e
}

make_nginx_proxy_directories() {
	set -e
	ssh gitlab@$DEPLOY_SERVER_IP "mkdir -p nginx-proxy/config/template"
	set +e
}

scp_start_script() {
	make_nginx_proxy_directories
	set -e
	scp nginx-proxy/nginx-proxy.sh gitlab@"${DEPLOY_SERVER_IP}":~/nginx-proxy/
	ssh gitlab@$DEPLOY_SERVER_IP "chmod 755 nginx-proxy/nginx-proxy.sh"
	set +e
}

scp_docker_compose() {
	make_nginx_proxy_directories
	set -e
	scp nginx-proxy/config/docker-compose.yml gitlab@"${DEPLOY_SERVER_IP}":~/nginx-proxy/config/
	set +e
}

scp_template() {
	make_nginx_proxy_directories
	set -e
	scp nginx-proxy/config/template/nginx.tmpl gitlab@"${DEPLOY_SERVER_IP}":~/nginx-proxy/config/template/
	set +e
}

set +e
nginx_proxy_found=$(ssh gitlab@$DEPLOY_SERVER_IP "ls -la" | grep -c "nginx-proxy")
if [ ! $nginx_proxy_found -eq 0 ]; then
	echo "Found nginx-proxy directory in home directory of gitlab user on remote server."
	start_script_found=$(ssh gitlab@$DEPLOY_SERVER_IP "ls -la nginx-proxy/" | grep -c "nginx-proxy.sh")
	if [ ! $start_script_found -eq 0 ]; then
		echo "Found nginx-proxy-start-script."
	else
		echo "Start script not found. Copying files..."
		scp_start_script
	fi

	config_folder_found=$(ssh gitlab@$DEPLOY_SERVER_IP "ls -la nginx-proxy/" | grep -c "config")
	if [ ! $config_folder_found -eq 0 ]; then
		echo "Found config folder of nginx-proxy."
		docker_compose_found=$(ssh gitlab@$DEPLOY_SERVER_IP "ls -la nginx-proxy/config/" | grep -c "docker-compose.yml")
		if [ ! $docker_compose_found -eq 0 ]; then
			echo "Found docker-compose.yml of nginx-proxy."
		else
			echo "docker-compose.yml of nginx-proxy not found. Copying files..."
			scp_docker_compose
		fi

		template_folder_found=$(ssh gitlab@$DEPLOY_SERVER_IP "ls -la nginx-proxy/config/" | grep -c "template")
		if [ ! $template_folder_found -eq 0 ]; then
			echo "Found template directory of nginx-proxy."
			template_found=$(ssh gitlab@$DEPLOY_SERVER_IP "ls -la nginx-proxy/config/template" | grep -c "nginx.tmpl")
			if [ ! $template_found -eq 0 ]; then
				echo "Found nginx.tmpl of nginx-proxy."
			else
				echo "nginx.tmpl of nginx-proxy not found. Copying files..."
				scp_template
			fi
		else
			echo "template directory of nginx-proxy not found. Copying files..."
			scp_template
		fi
	else
		echo "Config folder not found. Copying files..."
		scp_docker_compose
		scp_template
	fi
else
	echo "nginx-proxy not found on remote server in home directory of gitlab user. Copying files to server..."
	scp_start_script
	scp_docker_compose
	scp_template
fi
set -e

echo "Files copied or verified, now starting nginx-proxy if not running..."

ssh gitlab@$DEPLOY_SERVER_IP "nginx-proxy/nginx-proxy.sh start"
ssh gitlab@$DEPLOY_SERVER_IP "nginx-proxy/nginx-proxy.sh status"

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
delete_old_app_images_on_server
scp app/docker-compose.yml gitlab@"${DEPLOY_SERVER_IP}":~/apps/${NGINX_SERVER_NAME}/
scp app/app.sh gitlab@"${DEPLOY_SERVER_IP}":~/apps/${NGINX_SERVER_NAME}/
scp app/re-encrypt-certs/* gitlab@"${DEPLOY_SERVER_IP}":~/apps/${NGINX_SERVER_NAME}/re-encrypt-certs/
scp app/crawlers/* gitlab@"${DEPLOY_SERVER_IP}":~/apps/${NGINX_SERVER_NAME}/crawlers/
ssh gitlab@$DEPLOY_SERVER_IP "chmod 755 apps/${NGINX_SERVER_NAME}/app.sh"

echo "Copied app configuration to server. Updating images and deploying now..."
ssh gitlab@$DEPLOY_SERVER_IP "apps/${NGINX_SERVER_NAME}/app.sh update"

echo "Deploy finished, your app should be reachable in a few seconds/minutes at ${NGINX_SERVER_NAME}"

