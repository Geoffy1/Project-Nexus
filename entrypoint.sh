#!/bin/sh
set -e

echo "Waiting for DB to be ready..."
# Simple loop; for Render an external DB might be ready, but this is safe:
# You can replace with wait-for-it if you prefer.
until python -c "import sys,os; \
from urllib.parse import urlparse; \
db=os.getenv('DATABASE_URL'); \
import psycopg2, time; \
p=urlparse(db); \
conn=None; \
try: \
  conn=psycopg2.connect(dbname=p.path[1:], user=p.username, password=p.password, host=p.hostname, port=p.port, connect_timeout=5); \
  conn.close(); \
  sys.exit(0); \
except Exception as e: \
  print('DB not ready yet, sleeping...'); \
  time.sleep(2)"

do
  sleep 1
done

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if env vars provided (optional)
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --noinput --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

echo "Starting server..."
exec "$@"

