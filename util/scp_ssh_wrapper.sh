#!/bin/bash
set -eo pipefail

# $1 = "command with args in quotes"
ssh_proxy() {
	eval $(ssh-agent -s)
	ssh-add <(cat "$DEPLOY_SERVER_PRIVATE_KEY")
	if [ "${PROXY_SERVER_PRIVATE_KEY}" != "" ]; then
		ssh-add <(cat "$PROXY_SERVER_PRIVATE_KEY")
	fi
	# if all three proxy variables are set, use proxy, else use deploy directly
	if [ "${PROXY_SERVER_IP}" == "" -o "${PROXY_SERVER_USER}" == "" -o "${PROXY_SERVER_PRIVATE_KEY}" == "" ]; then
		echo "Connecting directly to the deploy server..."
		ssh "${DEPLOY_SERVER_USER}@${DEPLOY_SERVER_IP}" "${1}"
	else
		echo "proxy-server variable set, connecting via proxy server to deploy server..."
		ssh "${PROXY_SERVER_USER}@${PROXY_SERVER_IP}" "ssh ${DEPLOY_SERVER_USER}@${DEPLOY_SERVER_IP} ${1}"
	fi
}

# $1 = local file path
# $2 = remote file path
scp_proxy() {
	eval $(ssh-agent -s)
	ssh-add <(cat "$DEPLOY_SERVER_PRIVATE_KEY")
	if [ "${PROXY_SERVER_PRIVATE_KEY}" != "" ]; then
		ssh-add <(cat "$PROXY_SERVER_PRIVATE_KEY")
	fi
	# if all three proxy variables are set, use proxy, else use deploy directly
	if [ "${PROXY_SERVER_IP}" == "" -o "${PROXY_SERVER_USER}" == "" -o "${PROXY_SERVER_PRIVATE_KEY}" == "" ]; then
		echo "Connecting directly to the deploy server..."
		scp "${1}" "${DEPLOY_SERVER_USER}@${DEPLOY_SERVER_IP}":"${2}"
	else
		echo "proxy-server variable set, connecting via proxy server to deploy server..."
		scp -o "ProxyCommand ssh ${PROXY_SERVER_USER}@${PROXY_SERVER_IP} -W ${DEPLOY_SERVER_IP}:22" "${1}" "${DEPLOY_SERVER_USER}@${DEPLOY_SERVER_IP}:${2}"
	fi
}
