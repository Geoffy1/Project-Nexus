# Dockerfile (production-ready for Render)
FROM python:3.10-slim

LABEL maintainer="you <you@example.com>"

# Environment variables for Python optimization and standard Docker settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential gcc libpq-dev curl netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (leverages Docker caching)
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy entrypoint and make executable
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy project files
COPY . /app/

# Create an unprivileged user and switch to it for security
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

USER appuser

# Runtime environment defaults (Render will override these)
ENV PORT=8000
ENV DJANGO_SETTINGS_MODULE=jobboard.settings

# Ensure static dir exists and is writable by appuser
RUN mkdir -p /app/staticfiles || true

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

# 🌟 CRITICAL FIX: Use JSON-array form with bash -c to evaluate $PORT 🌟
# This ensures Gunicorn binds to the port provided by Render's $PORT variable (e.g., 8000)
# The ${PORT:-8000} syntax provides a safe default if Render doesn't inject the variable.
CMD ["bash", "-c", "gunicorn jobboard.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3"]