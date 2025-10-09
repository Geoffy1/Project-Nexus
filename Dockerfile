# Dockerfile (production)
FROM python:3.10-slim

LABEL maintainer="you <you@example.com>"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

# system deps required to build some packages (keep minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       libpq-dev \
       curl \
       netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# copy requirements and install deps
COPY requirements.txt /app/
RUN pip install --upgrade pip
# Use regular pip install (allow wheels). Avoid forcing no-binary which breaks psycopg2-binary.
RUN pip install -r /app/requirements.txt

# copy project
COPY . /app/

# create unprivileged user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

ENV PORT=8000
ENV DJANGO_SETTINGS_MODULE=jobboard.settings

# create static dir
RUN mkdir -p /app/staticfiles

EXPOSE 8000

# copy entrypoint and make executable
# Note: docker-compose mounts repo at /code in local dev. In container, entrypoint comes from mounted repo (so ensure host file is executable).
COPY ./entrypoint.sh /app/entrypoint.sh
#RUN chmod +x /app/entrypoint.sh
RUN chmod 755 /app/entrypoint.sh || true


ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "jobboard.wsgi:application", "--bind", "0.0.0.0:$PORT", "--workers", "3"]
