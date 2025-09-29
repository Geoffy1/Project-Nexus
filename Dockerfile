# Dockerfile (production)
FROM python:3.10-slim

LABEL maintainer="you <you@example.com>"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

# system deps required to build psycopg2 and others
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
RUN pip install --no-binary :all: -r /app/requirements.txt

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

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "jobboard.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "4"]
