#!/bin/bash
#set -eo pipefail

# Running in Builder Image Docker Container

# pwd = $REPO_COPY_DIRECTORY (/builds/dood/app)
. "${BUILDER_VENV_DIRECTORY}/bin/activate"

# pwd = $REPO_COPY_DIRECTORY (/builds/dood/app)
cd "${CLIENT_DIRECTORY}"
# pwd = ${REPO_COPY_DIRECTORY}/${CLIENT_DIRECTORY} (/builds/dood/app/client)

echo "pwd:"
pwd
echo "ls -la:"
ls -la

echo 'Run npm build'
npm set progress=false
npm install -s --no-progress
npm audit fix
mkdir -p static
mkdir -p static-vuedj
npm run build
echo 'Done...'

echo 'Format index.html as Jinja template'
python3 format_index_html.py # This has nothing to do with the python backend. Just a helper script.
echo 'Done...'

# pwd = ${REPO_COPY_DIRECTORY}/${CLIENT_DIRECTORY} (/builds/dood/app/client)
cd "../${BACKEND_DIRECTORY}"
# pwd = ${REPO_COPY_DIRECTORY}/${BACKEND_DIRECTORY} (/builds/dood/app/backend)

echo 'Install python modules'
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
echo 'Done...'

echo 'Collect static'
python3 manage.py collectstatic --noinput # Collects from /builds/dood/app/client/static and outputs to /builds/dood/client/staticfiles
echo 'Done...'

echo 'Run migrations'
python3 manage.py migrate
echo 'Done...'

# pwd = ${REPO_COPY_DIRECTORY}/${BACKEND_DIRECTORY} (/builds/dood/app/backend)
cd ..
# pwd = ${REPO_COPY_DIRECTORY} (/builds/dood/app)  (outside of this script not kept)

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
