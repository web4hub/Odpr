#!/bin/bash
set -eo pipefail

source util/resolve_os.sh
set +e
source ./backend/.venv/"${VBIN}"/activate 2>/dev/null
if [ ! $? -eq 0 ]; then
	MAKE_VENV=1
fi
set -e

if [ 0$MAKE_VENV -eq 1 ]; then
	echo "No .venv found, thus python3 -m venv .venv..."
	python3 -m venv backend/.venv
fi

