#!/bin/bash
set -eo pipefail

apt-get update -qq
'which ssh-agent || ( apt-get install -qq openssh-client )'
eval $(ssh-agent -s)
ssh-add <(cat "$DEPLOY_SERVER_PRIVATE_KEY")
mkdir -p ~/.ssh
'[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config'
