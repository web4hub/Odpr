#!/bin/bash
#set -eo pipefail


. ./resolve_os.sh
pwd
ls -la
ls -la ./backend
ls -la ./backend/.venv
ls -la ./backend/.venv/bin
. ./backend/.venv/"${VBIN}"/activate

cd client

echo 'Run npm build'
npm set progress=false
npm install -s --no-progress
npm audit fix
npm run build
echo 'Done...'

echo 'Format index.html as Jinja template'
python format_index_html.py
echo 'Done...'

cd ../backend

echo 'Install python modules'
python -m pip install --upgrade pip
pip install -r requirements.txt
echo 'Done...'

echo 'Collect static'
python manage.py collectstatic --noinput
echo 'Done...'

echo 'Run migrations'
python manage.py migrate
echo 'Done...'
