#!/bin/bash
set -eo pipefail

sha256sum "${BUILDER_VERSION_SCRIPTS_DIRECTORY}/requirements.txt" | awk '{printf $1}'
