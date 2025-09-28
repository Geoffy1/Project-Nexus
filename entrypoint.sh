#!/usr/bin/env bash
set -e

# Wait for DB to be ready (simple strategy)
echo "Waiting for postgres..."
while ! nc -z ${DB_HOST:-db} ${DB_PORT:-5432}; do
  sleep 0.5
done

# Run migrations and collectstatic
echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Optionally run any other startup tasks (e.g. create default data)
# Exec the container main process (Gunicorn)
exec "$@"

