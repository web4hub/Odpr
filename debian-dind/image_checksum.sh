#!/bin/bash
set -eo pipefail

SUM_1=$(sha256sum "${BUILDER_VERSION_SCRIPTS_DIRECTORY}/Dockerfile" | awk '{printf $1}')
SUM_2=$(sha256sum "${BUILDER_VERSION_SCRIPTS_DIRECTORY}/dind_script.sh" | awk '{printf $1}')
SUM_3=$(sha256sum "${BUILDER_VERSION_SCRIPTS_DIRECTORY}/entrypoint.sh" | awk '{printf $1}')

echo "${SUM_1}${SUM_2}${SUM_3}"
