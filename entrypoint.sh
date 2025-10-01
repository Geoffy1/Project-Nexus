#!/bin/sh
set -e

echo "Waiting for DB to be ready..."

# Minimal DB probe using psycopg2. Requires psycopg2-binary installed.
python - <<'PY'
import os, sys, time
from urllib.parse import urlparse
try:
    import psycopg2
except Exception:
    print("psycopg2 not installed — skipping DB wait")
    sys.exit(0)

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print('No DATABASE_URL set, skipping DB wait')
    sys.exit(0)

p = urlparse(DATABASE_URL)

while True:
    try:
        conn = psycopg2.connect(
            dbname=p.path[1:], 
            user=p.username, 
            password=p.password, 
            host=p.hostname, 
            port=p.port, 
            connect_timeout=5
        )
        conn.close()
        print('DB is available')
        break
    except Exception as e:
        print('DB not ready yet: {}'.format(e))
        time.sleep(2)
PY

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Optionally create a superuser from env vars (safe to run; will no-op if user exists)
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser if it does not exist..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '$DJANGO_SUPERUSER_USERNAME'
email = '$DJANGO_SUPERUSER_EMAIL'
pw = '$DJANGO_SUPERUSER_PASSWORD'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=pw)
" || true
fi

echo "Starting application..."
exec "$@"
