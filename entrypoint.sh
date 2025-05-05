#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is available."

if [ ! -f "/usr/src/app/myproject/manage.py" ]; then
  echo "manage.py not found, cannot continue."
  ls /usr/src/app/myproject
  exit 1
fi

cd /usr/src/app/myproject

python manage.py migrate
exec python manage.py runserver 0.0.0.0:8000




