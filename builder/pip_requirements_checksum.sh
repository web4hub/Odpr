#!/bin/bash
set -eo pipefail

sha256sum "requirements.txt" | awk '{printf $1}'
