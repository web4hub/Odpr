#!/bin/bash
set -eo pipefail

source util/resolve_os.sh
util/make_venv.sh
source ./backend/.venv/"${VBIN}"/activate

if [ "$1" != "run" ]; then
	./build.sh
fi

cd backend

export PORT=8000
echo 'Server running on port ' $PORT
$PYTHON manage.py runserver
