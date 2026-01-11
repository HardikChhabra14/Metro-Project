#!/bin/sh

echo "Waiting for database..."

# Wait for PostgreSQL to be ready
while ! nc -z db 5432; do
  sleep 0.5
done

echo "PostgreSQL started"

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
export DJANGO_SETTINGS_MODULE=metro.metro.settings
