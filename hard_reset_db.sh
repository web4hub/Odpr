#!/bin/bash

source ./resolve_os.sh
source .venv/"${VBIN}"/activate

echo "Deleting database..."
rm ./db.sqlite3
echo "Deleting migrations..."
rm -rf ./accounts/migrations
echo ".../accounts/migrations"
rm -rf ./api/migrations
echo ".../api/migrations"
rm -rf ./app/migrations
echo ".../app/migrations"

echo "Making migrations..."
python manage.py makemigrations accounts api app

echo "Migrating..."
python manage.py migrate

echo "Finished. You should now call createsuperuser via the Windows Supershell"
