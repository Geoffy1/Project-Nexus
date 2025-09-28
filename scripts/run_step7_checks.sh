#!/usr/bin/env bash
# scripts/run_step7_checks.sh
set -euo pipefail

SUPERUSER_NAME="superadmin"
SUPERUSER_PASS="SuperPass123!"
RECRUITER_NAME="recruiter1"
RECRUITER_PASS="RecruiterPass123!"
USER_NAME="normaluser"
USER_PASS="UserPass123!"

API_BASE="http://localhost:8000/api"
TOKEN_ENDPOINT="$API_BASE/auth/token/"

echo "Ensure docker containers are running..."
docker-compose up -d

echo "Waiting for web to be ready..."
sleep 5

docker-compose exec -T web python manage.py shell <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="$SUPERUSER_NAME").exists():
    User.objects.create_superuser(username="$SUPERUSER_NAME", email="super@example.com", password="$SUPERUSER_PASS")
if not User.objects.filter(username="$RECRUITER_NAME").exists():
    u = User.objects.create_user(username="$RECRUITER_NAME", email="rec@example.com", password="$RECRUITER_PASS")
    u.role = "recruiter"
    u.save()
if not User.objects.filter(username="$USER_NAME").exists():
    u = User.objects.create_user(username="$USER_NAME", email="user@example.com", password="$USER_PASS")
    u.role = "user"
    u.save()
print("Users ready.")
PY

get_token() {
  local username="$1"
  local password="$2"
  curl -s -X POST "$TOKEN_ENDPOINT" -d "username=$username&password=$password" | python -c "import sys,json; j=json.load(sys.stdin); print(j.get('access',''))"
}

TOKEN_SUPER=$(get_token "$SUPERUSER_NAME" "$SUPERUSER_PASS")
TOKEN_REC=$(get_token "$RECRUITER_NAME" "$RECRUITER_PASS")
TOKEN_USER=$(get_token "$USER_NAME" "$USER_PASS")

echo "Super token length: ${#TOKEN_SUPER}"
echo "Recruiter token length: ${#TOKEN_REC}"
echo "User token length: ${#TOKEN_USER}"

create_job() {
  local token="$1"
  curl -s -o /dev/stderr -w "HTTP_CODE:%{http_code}\n" -X POST "$API_BASE/jobs/" \
    -H "Authorization: Bearer $token" -H "Content-Type: application/json" \
    -d '{"title":"Automation Test Job","company":"CI","description":"Testing role-based create","location":"Nairobi","employment_type":"FT"}'
}

echo "== Superuser create =="
create_job "$TOKEN_SUPER"

echo "== Recruiter create =="
create_job "$TOKEN_REC"

echo "== Normal user create =="
create_job "$TOKEN_USER"

echo "== Anonymous create =="
curl -s -o /dev/stderr -w "HTTP_CODE:%{http_code}\n" -X POST "$API_BASE/jobs/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Anon Test Job","company":"CI","description":"Testing anonymous create","location":"Nairobi","employment_type":"FT"}'

echo "Done."

