#!/bin/bash
set -eo pipefail

# Running in Builder Image Docker Container

# pwd = $REPO_COPY_DIRECTORY (/builds/dood/app)
. "${BUILDER_VENV_DIRECTORY}/bin/activate"

# pwd = $REPO_COPY_DIRECTORY (/builds/dood/app)
cd "${CLIENT_DIRECTORY}"
# pwd = ${REPO_COPY_DIRECTORY}/${CLIENT_DIRECTORY} (/builds/dood/app/client)

echo 'Run npm build'
npm install -g npm
npm set progress=false
npm install -s --no-progress
npm audit fix
mkdir -p static
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

echo 'Run Django Tests...'
unset DJANGO_DATABASE_NAME # Will only unset within this script, not outside this script.
python3 manage.py test --attr='assertAlmostEqual' # The --attr filters subclasses of unittest.TestCase (else every helper method and everything would be considered a test-method by nose, which is annoying because it fails)
echo 'Done...'

echo 'Collect static'
python3 manage.py collectstatic --noinput # Collects from /builds/dood/app/client/static and outputs to /builds/dood/client/staticfiles
echo 'Done...'
