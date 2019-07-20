#!/bin/bash
set -eo pipefail


source ./resolve_os.sh
source ./backend/.venv/"${VBIN}"/activate

cd client

echo 'Run npm build'
npm install
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
