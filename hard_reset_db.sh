#!/bin/bash

source ./resolve_os.sh
source ./backend/.venv/"${VBIN}"/activate

echo "Deleting database..."
rm ./db.sqlite3
echo "Deleting migrations..."
rm -rf ./backend/accounts/migrations
echo ".../accounts/migrations"
rm -rf ./backend/api/migrations
echo ".../api/migrations"
rm -rf ./backend/app/migrations
echo ".../app/migrations"

echo "Making migrations..."
python ./backend/manage.py makemigrations accounts api app

echo "Migrating..."
python ./backend/manage.py migrate

echo "Finished. You should now call createsuperuser via the Windows Supershell"
