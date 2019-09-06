#!/bin/bash
set -eo pipefail

echo "apt-get update -qq"
apt-get update -qq
echo "which ssh-agent || ( apt-get install -qq openssh-client )"
which ssh-agent || ( apt-get install -qq openssh-client )
echo "eval (ssh-agent -s)"
eval $(ssh-agent -s)
echo "ssh-add <(cat \"DEPLOY_SERVER_PRIVATE_KEY\")"
ssh-add <(cat "$DEPLOY_SERVER_PRIVATE_KEY")
echo "mkdir -p ~/.ssh"
mkdir -p ~/.ssh
echo "[[ -f /.dockerenv ]] && echo -e \"Host *\\n\\tStrictHostKeyChecking no\\n\\n\" > ~/.ssh/config"
[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
