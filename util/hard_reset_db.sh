#!/bin/bash

cd "$(dirname "$0")"

source resolve_os.sh
source ../backend/.venv/"${VBIN}"/activate

echo "Deleting database..."
rm ../db.sqlite3
echo "Deleting migrations..."
rm -rf ../backend/accounts/migrations
echo ".../accounts/migrations"
rm -rf ../backend/api/migrations
echo ".../api/migrations"
rm -rf ../backend/app/migrations
echo ".../app/migrations"

echo "Making migrations..."
$PYTHON ../backend/manage.py makemigrations accounts api app

echo "Migrating..."
$PYTHON ../backend/manage.py migrate

echo "Finished. You can now create a new superuser by registering a user at localhost:8000/api/v1/auth/register/ (don't forget the trailing slash/)"
