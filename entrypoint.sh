#!/usr/bin/env bash
set -euo pipefail

: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"
: "${WAIT_HOST_TIMEOUT:=60}"
: "${FAIL_ON_TIMEOUT:=1}"

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
      if [ "${FAIL_ON_TIMEOUT}" -eq 1 ]; then
        exit 1
      else
        return 1
      fi
    fi
    sleep 0.5
  done
}

if [ -n "${DB_HOST}" ]; then
  wait_for "$DB_HOST" "$DB_PORT" "$WAIT_HOST_TIMEOUT"
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
