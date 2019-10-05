#!/bin/bash
set -eo pipefail


. util/resolve_os.sh
util/make_venv.sh
. ./backend/.venv/"${VBIN}"/activate

cd client

echo 'Run npm build'
npm install
npm audit fix
npm run build
echo 'Done...'

echo 'Format index.html as Jinja template'
PYTHON format_index_html.py
echo 'Done...'

cd ../backend

echo 'Install python modules'
PYTHON -m pip install --upgrade pip
pip install -r requirements.txt
echo 'Done...'

echo 'Collect static'
PYTHON manage.py collectstatic --noinput
echo 'Done...'

echo 'Run migrations'
PYTHON manage.py migrate
echo 'Done...'
