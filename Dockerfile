# Dockerfile
FROM python:3.10-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Default command (override in docker-compose for web/celery)
CMD ["gunicorn", "jobboard.wsgi:application", "--bind", "0.0.0.0:8000"]

# Create a non-root user
RUN addgroup --system app && adduser --system --ingroup app app

# Change ownership of /code so the user can access it
RUN chown -R app:app /code

# Switch to non-root user
USER app
