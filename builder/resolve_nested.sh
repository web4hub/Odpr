#!/bin/bash
set -eo pipefail
# $1 = input variable with nested variables
# the nested variables need to be exported to be visible for this script!!

if [[ "${1}" =~ '$' ]]; then
  current="${1}"
else
  eval current="\$${1}"
fi

while [[ "${current}" =~ '$' ]]; do
  eval current="${current}"
done

echo "${current}"
