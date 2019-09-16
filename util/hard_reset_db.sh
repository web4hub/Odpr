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
rm -rf ../backend/odpr_shared_models/migrations
echo ".../odpr_shared_models/migrations"
rm -rf ../backend/sceneries/migrations
echo ".../sceneries/migrations"
rm -rf ../backend/scenery_requests/migrations
echo ".../scenery_requests/migrations"
rm -rf ../backend/documentation/migrations
echo ".../documentation/migrations"

echo "Making migrations..."
#python ../backend/manage.py makemigrations accounts odpr_shared_models documentation sceneries scenery_requests
#python ../backend/manage.py makemigrations

echo "Migrating..."
#python ../backend/manage.py migrate

echo "Finished. You can now create a new superuser by registering a user at localhost:8000/api/v1/auth/register/ (don't forget the trailing slash/)"
