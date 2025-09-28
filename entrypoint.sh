#!/usr/bin/env bash
set -euo pipefail

# Helper: parse DATABASE_URL if present to get host and port
parse_database_url() {
  # supports postgres://user:pass@host:port/dbname and postgresql://...
  if [ -n "${DATABASE_URL:-}" ]; then
    # Use Python to parse robustly
    host_port=$(python - <<PY
import os,urllib.parse
u = os.environ.get("DATABASE_URL")
if not u:
    print("")
else:
    p = urllib.parse.urlparse(u)
    # p.hostname and p.port may be None
    host = p.hostname or ""
    port = p.port or ""
    print(f"{host}:{port}")
PY
)
    DB_HOST_FROM_URL=${host_port%%:*}
    DB_PORT_FROM_URL=${host_port#*:}
    # If nothing parsed, leave empty
    if [ -n "$DB_HOST_FROM_URL" ] && [ "$DB_HOST_FROM_URL" != ":" ]; then
      export DB_HOST="$DB_HOST_FROM_URL"
    fi
    if [ -n "$DB_PORT_FROM_URL" ] && [ "$DB_PORT_FROM_URL" != "$DB_HOST_FROM_URL" ]; then
      export DB_PORT="$DB_PORT_FROM_URL"
    fi
  fi
}

# Set defaults if not provided
: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"
: "${WAIT_HOST_TIMEOUT:=60}"

# Try to parse DATABASE_URL if provided (overrides DB_HOST/DB_PORT)
parse_database_url

echo "Entrypoint: waiting for DB at ${DB_HOST}:${DB_PORT} (timeout ${WAIT_HOST_TIMEOUT}s)..."

# wait-for implementation with timeout
wait_for() {
  host="$1"
  port="$2"
  timeout="$3"
  start_ts=$(date +%s)
  while true; do
    if nc -z "$host" "$port" >/dev/null 2>&1; then
      echo "Port $port on $host is available"
      return 0
    fi
    now_ts=$(date +%s)
    elapsed=$((now_ts - start_ts))
    if [ "$elapsed" -ge "$timeout" ]; then
      echo "Timed out after ${timeout}s waiting for ${host}:${port}"
      return 1
    fi
    sleep 0.5
  done
}

# Only wait if DB host is not empty
if [ -n "${DB_HOST}" ]; then
  if ! wait_for "$DB_HOST" "$DB_PORT" "$WAIT_HOST_TIMEOUT"; then
    echo "Warning: database host ${DB_HOST}:${DB_PORT} not reachable; continuing anyway"
    # in many PaaS cases the DB might be reachable later; proceed so process doesn't die during startup
  fi
else
  echo "No DB_HOST set; skipping DB wait"
fi

# Run Django migrations / collectstatic (safe to run multiple times)
echo "Running migrations..."
python manage.py migrate --noinput || echo "Migrations returned non-zero exit code; continuing"

echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Collectstatic returned non-zero exit code; continuing"

# Execute the passed command (e.g. gunicorn or celery)
exec "$@"
