#!/bin/sh

echo "Waiting for database..."
sleep 3

python manage.py collectstatic --noinput
python manage.py migrate

exec "$@"
