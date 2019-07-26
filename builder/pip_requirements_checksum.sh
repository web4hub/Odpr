#!/bin/bash
set -eo pipefail

sha256sum "${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}/requirements.txt"
