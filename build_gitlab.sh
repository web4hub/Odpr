#!/bin/bash
#set -eo pipefail

. "${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}"/.venv/bin/activate

cd "${WORKING_DIRECTORY}/${CLIENT_DIRECTORY}"

echo 'Run npm build'
npm set progress=false
npm install -s --no-progress
npm audit fix
npm run build
echo 'Done...'

echo 'Format index.html as Jinja template'
python3 format_index_html.py
echo 'Done...'

cd "${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}"

echo 'Install python modules'
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
echo 'Done...'

echo 'Collect static'
python3 manage.py collectstatic --noinput
echo 'Done...'

echo 'Run migrations'
python3 manage.py migrate
echo 'Done...'
