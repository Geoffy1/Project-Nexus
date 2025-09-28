# Project Nexus — Job Board Backend

# Project Nexus — Job Board Backend

## Overview  
A backend API for a Job Board — built with **Django**, **PostgreSQL**, **Django REST Framework (DRF)**, **JWT auth**, **Celery + RabbitMQ**. The system supports role-based access (e.g. job seekers, employers, admins), job search and filtering, job applications, and asynchronous tasks (e.g. email notifications, cleanup) — all fully dockerized for consistency across environments.

### Goals  
- Provide a scalable, maintainable backend API for a job board  
- Support asynchronous processing (e.g. scheduled tasks) with Celery  
- Offer secure authentication and authorization via JWT  
- Enable smooth developer onboarding via Docker / containerization  
- Provide clear docs, tests, and CI for quality and maintainability  

---

## Setup & Quickstart

### Prerequisites  
- Docker & Docker Compose installed  
- (Optional) Python and Django locally, if you want to run without Docker

### Docker Quickstart

```bash
# Copy example env file
cp .env.example .env

# Build and start containers in detached mode
docker-compose up --build -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create a superuser (for admin access)
docker-compose exec web python manage.py createsuperuser

# Optionally, seed initial data or run fixtures if available
