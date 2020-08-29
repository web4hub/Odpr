#!/bin/bash
set -eo pipefail

# if the variable TEST_DEPLOY_SERVER_IP is defined and the variable TEST_DEPLOYMENT, this script will use the variables
# TEST_DEPLOY_SERVER_IP
# TEST_DEPLOY_SERVER_USER
# TEST_DEPLOY_SERVER_PRIVATE_KEY
# and if defined:
# TEST_PROXY_SERVER_IP
# TEST_PROXY_SERVER_USER
# TEST_PROXY_SERVER_PRIVATE_KEY

ssh_production() {
	>&2 eval $(ssh-agent -s)
	>&2 ssh-add <(cat "$DEPLOY_SERVER_PRIVATE_KEY")
	if [ "${PROXY_SERVER_PRIVATE_KEY}" != "" ]; then
		>&2 ssh-add <(cat "$PROXY_SERVER_PRIVATE_KEY")
	fi
	# if all three proxy variables are set, use proxy, else use deploy directly
	if [ "${PROXY_SERVER_IP}" == "" -o "${PROXY_SERVER_USER}" == "" -o "${PROXY_SERVER_PRIVATE_KEY}" == "" ]; then
		# >&2 echo "Connecting directly to the deploy server..."
		ssh "${DEPLOY_SERVER_USER}@${DEPLOY_SERVER_IP}" "${1}"
	else
		# >&2 echo "proxy-server variable set, connecting via proxy server to deploy server..."
		ssh -o "ProxyCommand ssh ${PROXY_SERVER_USER}@${PROXY_SERVER_IP} -W ${DEPLOY_SERVER_IP}:22" "${DEPLOY_SERVER_USER}@${DEPLOY_SERVER_IP}" "${1}"
	fi
}

scp_production() {
	>&2 eval $(ssh-agent -s)
	>&2 ssh-add <(cat "$DEPLOY_SERVER_PRIVATE_KEY")
	if [ "${PROXY_SERVER_PRIVATE_KEY}" != "" ]; then
		>&2 ssh-add <(cat "$PROXY_SERVER_PRIVATE_KEY")
	fi
	# if all three proxy variables are set, use proxy, else use deploy directly
	if [ "${PROXY_SERVER_IP}" == "" -o "${PROXY_SERVER_USER}" == "" -o "${PROXY_SERVER_PRIVATE_KEY}" == "" ]; then
		# >&2 echo "Connecting directly to the deploy server..."
		scp "${1}" "${DEPLOY_SERVER_USER}@${DEPLOY_SERVER_IP}":"${2}"
	else
		# >&2 echo "proxy-server variable set, connecting via proxy server to deploy server..."
		scp -o "ProxyCommand ssh ${PROXY_SERVER_USER}@${PROXY_SERVER_IP} -W ${DEPLOY_SERVER_IP}:22" "${1}" "${DEPLOY_SERVER_USER}@${DEPLOY_SERVER_IP}:${2}"
	fi
}

ssh_testserver() {
	>&2 eval $(ssh-agent -s)
	>&2 ssh-add <(cat "$TEST_DEPLOY_SERVER_PRIVATE_KEY")
	if [ "${TEST_PROXY_SERVER_PRIVATE_KEY}" != "" ]; then
		>&2 ssh-add <(cat "$TEST_PROXY_SERVER_PRIVATE_KEY")
	fi
	# if all three proxy variables are set, use proxy, else use deploy directly
	if [ "${TEST_PROXY_SERVER_IP}" == "" -o "${TEST_PROXY_SERVER_USER}" == "" -o "${TEST_PROXY_SERVER_PRIVATE_KEY}" == "" ]; then
		# >&2 echo "Connecting directly to the deploy server..."
		ssh "${TEST_DEPLOY_SERVER_USER}@${TEST_DEPLOY_SERVER_IP}" "${1}"
	else
		# >&2 echo "proxy-server variable set, connecting via proxy server to deploy server..."
		ssh -o "ProxyCommand ssh ${TEST_PROXY_SERVER_USER}@${TEST_PROXY_SERVER_IP} -W ${TEST_DEPLOY_SERVER_IP}:22" "${TEST_DEPLOY_SERVER_USER}@${TEST_DEPLOY_SERVER_IP}" "${1}"
	fi
}

scp_testserver() {
	>&2 eval $(ssh-agent -s)
	>&2 ssh-add <(cat "$TEST_DEPLOY_SERVER_PRIVATE_KEY")
	if [ "${TEST_PROXY_SERVER_PRIVATE_KEY}" != "" ]; then
		>&2 ssh-add <(cat "$TEST_PROXY_SERVER_PRIVATE_KEY")
	fi
	# if all three proxy variables are set, use proxy, else use deploy directly
	if [ "${TEST_PROXY_SERVER_IP}" == "" -o "${TEST_PROXY_SERVER_USER}" == "" -o "${TEST_PROXY_SERVER_PRIVATE_KEY}" == "" ]; then
		# >&2 echo "Connecting directly to the deploy server..."
		scp "${1}" "${TEST_DEPLOY_SERVER_USER}@${TEST_DEPLOY_SERVER_IP}":"${2}"
	else
		# >&2 echo "proxy-server variable set, connecting via proxy server to deploy server..."
		scp -o "ProxyCommand ssh ${TEST_PROXY_SERVER_USER}@${TEST_PROXY_SERVER_IP} -W ${TEST_DEPLOY_SERVER_IP}:22" "${1}" "${TEST_DEPLOY_SERVER_USER}@${TEST_DEPLOY_SERVER_IP}:${2}"
	fi
}

# $1 = "command with args in quotes"
ssh_proxy() {
	if [ "${TEST_DEPLOY_SERVER_IP}" != "" -a "${TEST_DEPLOYMENT}" != "" ]; then
		ssh_testserver "$@"
	else
		ssh_production "$@"
	fi
}

# $1 = local file path
# $2 = remote file path
scp_proxy() {
	if [ "${TEST_DEPLOY_SERVER_IP}" != "" -a "${TEST_DEPLOYMENT}" != "" ]; then
		scp_testserver "$@"
	else
		scp_production "$@"
	fi
}
