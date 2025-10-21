# 🧠 Project Nexus Job Board  

### 🚀 A Modern Django + DRF API for Managing Jobs, Categories, and Applications  

The **Project Nexus Job Board API** is a robust backend system built using **Django**, **Django REST Framework**, and **PostgreSQL** — designed to streamline job postings, categories, and applications. It’s fully containerized with **Docker** and deployable on **Render** with production-ready configurations.  

---

## 🌟 Features

- 🧩 **Jobs Management** – Create, read, update, and delete job listings.  
- 🏷 **Categories** – Organize jobs by category with easy filtering.  
- 📩 **Applications** – Allow users to apply for jobs and track submissions.  
- 🔒 **JWT Authentication** – Secure API access via JSON Web Tokens.  
- 🩺 **Health Check Endpoint** – Monitor the app’s uptime and readiness.  
- 📜 **Auto-generated API Docs** – Explore endpoints with Swagger UI via `drf-spectacular`.  
- ⚙️ **Dockerized** – Simple container-based deployment for local and cloud use.  
- 🌐 **Render Deployment Ready** – Includes environment variables and production settings.  

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend Framework** | Django 5 + Django REST Framework |
| **Database** | PostgreSQL |
| **Authentication** | JWT (via SimpleJWT) |
| **API Documentation** | drf-spectacular (Swagger UI) |
| **Deployment** | Render |
| **Containerization** | Docker |
| **Broker (optional)** | Celery + RabbitMQ |

---

## 📂 Project Structure

Project-Nexus/
├── jobboard/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── jobs/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ └── admin.py
├── applications/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ └── admin.py
├── templates/
│ ├── home.html
│ ├── base.html
│ └── error.html
├── Dockerfile
├── requirements.txt
├── manage.py
└── README.md


---

## ⚙️ Environment Variables

These should be configured in Render or your `.env` file:

| Variable | Example Value | Description |
|-----------|----------------|-------------|
| `SECRET_KEY` | `your-secret-key` | Django security key |
| `DEBUG` | `False` | Disable debug mode in production |
| `DJANGO_ALLOWED_HOSTS` | `your-app.onrender.com` | Comma-separated allowed hosts |
| `DATABASE_URL` | `postgresql://user:password@host:port/dbname` | Postgres connection string |
| `CELERY_BROKER_URL` | `amqp://user:password@host/vhost` | RabbitMQ broker URL (optional) |
| `PORT` | `8000` | Default Django port |

---

## 🐳 Docker Setup

### 1️⃣ Build and run locally:
```bash
docker-compose up --build

2️⃣ Migrate the database:
docker-compose exec web python manage.py migrate

3️⃣ Create a superuser:
docker-compose exec web python manage.py createsuperuser

4️⃣ Access locally:

API Root: http://localhost:8000

Admin Panel: http://localhost:8000/admin

Swagger Docs: http://localhost:8000/api/docs/

🧭 API Endpoints
| Endpoint                   | Description                          |
| -------------------------- | ------------------------------------ |
| `/`                        | Landing page with project info       |
| `/health/`                 | Health check endpoint                |
| `/api/jobs/`               | CRUD operations for jobs             |
| `/api/categories/`         | CRUD operations for categories       |
| `/api/applications/`       | CRUD operations for job applications |
| `/api/docs/`               | Swagger UI documentation             |
| `/api/auth/token/`         | Obtain JWT                           |
| `/api/auth/token/refresh/` | Refresh JWT                          |


☁️ Render Deployment Guide

1️⃣ Push your code to GitHub (public or private).
2️⃣ Create a Render Web Service:
• Environment: Python 3
• Build Command:
pip install -r requirements.txt
python manage.py collectstatic --noinput

. Start Command:
gunicorn jobboard.wsgi:application
3️⃣ Add the environment variables (listed above).
4️⃣ Deploy — Render will automatically build and host your Django app.
5️⃣ Visit your live endpoint (e.g., https://project-nexus.onrender.com).

🧪 Health Check

To confirm Render sees your service as healthy:
curl https://project-nexus.onrender.com/health/

Expected response:

 #{"status": "ok"}

🎨 Frontend Templates (HTML)
✅ templates/home.html

A responsive landing page with a gradient background and fade-in animation to greet API users.

✅ templates/base.html

The base layout template for reusability across pages.

✅ templates/error.html

Simple, user-friendly 404 or server error page.

🧑‍💻 Developer
👤 Geofrey Simiyu Njogu
Full-Stack Software Engineer | Python • Django • React • TypeScript
🌐 geoffy1.github.io

🐙 https://github.com/Geoffy1

