#!/bin/bash
#set -eo pipefail

. "${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}"/.venv/bin/activate

# cd "${WORKING_DIRECTORY}/${CLIENT_DIRECTORY}"
cd "${CLIENT_DIRECTORY}"

echo "pwd:"
pwd
echo "ls -la:"
ls -la

echo 'Run npm build'
npm set progress=false
npm install -s --no-progress
npm audit fix
npm run build
echo 'Done...'

echo 'Format index.html as Jinja template'
python3 format_index_html.py
echo 'Done...'

cd "../${BACKEND_DIRECTORY}"

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

cd ..

echo "pwd:"
pwd
echo "ls -la:"
ls -la
echo "find / -iname backend:"
find / -iname "*backend*"
echo "\${WORKING_DIRECTORY}/\${BACKEND_DIRECTORY}:"
echo "${WORKING_DIRECTORY}/${BACKEND_DIRECTORY}:"
apt-get update && apt-get install -y procps
echo "ps":
ps
