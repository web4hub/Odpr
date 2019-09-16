#!/bin/bash
set -eo pipefail

# Running in Builder Image Docker Container

# pwd = $CI_PROJECT_DIR (/builds/dood/app)
. "${BUILDER_VENV_DIRECTORY}/bin/activate"

# pwd = $CI_PROJECT_DIR (/builds/dood/app)
cd "${CLIENT_DIRECTORY}"
# pwd = ${CI_PROJECT_DIR}/${CLIENT_DIRECTORY} (/builds/dood/app/client)

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

# pwd = ${CI_PROJECT_DIR}/${CLIENT_DIRECTORY} (/builds/dood/app/client)
cd "../${BACKEND_DIRECTORY}"
# pwd = ${CI_PROJECT_DIR}/${BACKEND_DIRECTORY} (/builds/dood/app/backend)

echo 'Install python modules'
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
echo 'Done...'

echo 'Run Django Tests...'
unset DJANGO_DATABASE_NAME # Will only unset within this script, not outside this script. Needed, to test with sqlite3 instead of postgres.
python3 manage.py makemigrations accounts api filer odpr_shared_models documentation sceneries scenery_requests
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py test --attr='assertAlmostEqual' 2>&1 | tee test_results.txt # The --attr filters subclasses of unittest.TestCase (else every helper method and everything would be considered a test-method by nose, which is annoying because it fails)
COVERAGE_RESULT=$(cat test_results.txt | sed -rn 's~^[^TOTAL](.*)\s+([[:digit:]]+)\s+([[:digit:]]+)\s+([[:digit:]]+)\%.*$~\1 \2 \3~p' | awk '{ result+=$2; if($1!~"admin|models") { statements+=$2; miss+=$3} } END { printf "%.2f", (1-miss/statements)*100 }')
echo "COVERAGE_RESULT ${COVERAGE_RESULT}"
echo "Creating badge for coverage with value=\"${COVERAGE_RESULT}\""

# float number comparison
flesseq() {
    awk -v n1="$1" -v n2="$2" 'BEGIN {if (n1+0<=n2+0) exit 0; exit 1}'
}

if flesseq $COVERAGE_RESULT 36.0; then
	coverage_color="red"
elif flesseq $COVERAGE_RESULT 58.0; then
	coverage_color="orange"
elif flesseq $COVERAGE_RESULT 70.0; then
	coverage_color="yellow"
else
	coverage_color="green"
fi
COVERAGE_RESULT="${COVERAGE_RESULT}%"

anybadge -l "coverage" -v "${COVERAGE_RESULT}" -f coverage.svg -c "${coverage_color}"
echo 'Done...'

echo 'Collect static'
python3 manage.py collectstatic --noinput # Collects from /builds/dood/app/client/static and outputs to /builds/dood/client/staticfiles
echo 'Done...'
