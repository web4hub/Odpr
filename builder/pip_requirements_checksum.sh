#!/bin/bash
set -eo pipefail

sha256sum "${BACKEND_DIRECTORY}/requirements.txt"
