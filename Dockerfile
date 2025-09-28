# # # Dockerfile
# # FROM python:3.10-slim

# # # Prevent Python from writing .pyc files
# # ENV PYTHONDONTWRITEBYTECODE 1
# # ENV PYTHONUNBUFFERED 1

# # # Install system dependencies
# # RUN apt-get update && apt-get install -y \
# #     build-essential \
# #     libpq-dev \
# #     postgresql-client \
# #     curl \
# #     && rm -rf /var/lib/apt/lists/*

# # # Set work directory
# # WORKDIR /code

# # # Install Python dependencies
# # COPY requirements.txt /code/
# # RUN pip install --upgrade pip
# # RUN pip install -r requirements.txt

# # # Copy project
# # COPY . /code/

# # # Default command (override in docker-compose for web/celery)
# # CMD ["gunicorn", "jobboard.wsgi:application", "--bind", "0.0.0.0:8000"]

# # # Create a non-root user
# # RUN addgroup --system app && adduser --system --ingroup app app

# # # Change ownership of /code so the user can access it
# # RUN chown -R app:app /code

# # # Switch to non-root user
# # USER app
# # Dockerfile
# FROM python:3.10-slim

# # Prevent Python from writing .pyc files and buffer stdout/stderr
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /code

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     netcat-openbsd \
#     gcc \
#     libpq-dev \
#     postgresql-client \
#     curl \
#     --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt /code/
# RUN pip install --upgrade pip \
#     && pip install -r requirements.txt

# # Copy project
# COPY . /code/

# # Copy entrypoint script and ensure it’s executable
# COPY entrypoint.sh /code/entrypoint.sh
# RUN chmod +x /code/entrypoint.sh

# # Create a non-root user and set permissions
# RUN addgroup --system app && adduser --system --ingroup app app \
#     && chown -R app:app /code
# USER app

# # Default command (can be overridden in docker-compose for web/celery)
# CMD ["/code/entrypoint.sh", "gunicorn", "jobboard.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

# Dockerfile
FROM python:3.10-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat-openbsd \
    gcc \
    libpq-dev \
    postgresql-client \
    curl \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Ensure entrypoint is executable
COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /code

# Switch to non-root user
USER appuser

# Default command (overridable in docker-compose.yml)
CMD ["/code/entrypoint.sh", "gunicorn", "jobboard.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
