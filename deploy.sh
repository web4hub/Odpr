#!/bin/bash
set -eo pipefail

source ./resolve_os.sh
source ./backend/.venv/"${VBIN}"/activate

if [ "$1" != "run" ]; then
	./build.sh
fi

export PORT=8000
echo 'Server runnning on port ' $PORT
python manage.py runserver
