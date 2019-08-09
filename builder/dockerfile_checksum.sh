#!/bin/bash
set -eo pipefail

sha256sum "${BUILDER_VERSION_SCRIPTS_DIRECTORY}/Dockerfile" | awk '{printf $1}'
