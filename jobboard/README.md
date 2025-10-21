# 🚀 Project Nexus: Job Board Backend API

**Live API URL:** `https://project-nexus-uulu.onrender.com`

**Project Status: Exceptional Work! 🟢**

Project Nexus is the capstone project for the **ProDev Backend Engineering** program, demonstrating mastery in building a scalable, secure, and fully functional **RESTful API** for a Job Board platform. The project focuses on robust API design, role-based access control, optimized database querying, and a containerized deployment workflow.

---

## 🌟 Key Features

* **Job Management:** Full **CRUD** (Create, Read, Update, Delete) functionality for job postings.
* **Role-Based Access Control (RBAC):** Separate permissions for **Admins** (to manage jobs/categories) and **Users** (to apply for jobs).
* **Secure Authentication:** Implemented using **JSON Web Tokens (JWT)** for stateless, secure API access.
* **Optimized Search:** Advanced query indexing on **PostgreSQL** for efficient job filtering by location, category, and keywords.
* **Asynchronous Tasks (Celery):** Uses an external message queue (**CloudAMQP/RabbitMQ**) for background processing (e.g., job application notifications, data cleanup).
* **API Documentation:** Comprehensive API reference available via **Swagger/OpenAPI**.

---

## 💻 Technologies Used (The Stack)

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | **Python 3.10, Django** | Primary framework for rapid development and API logic. |
| **API** | **Django REST Framework (DRF)** | Building robust, clean, and RESTful endpoints. |
| **Database** | **PostgreSQL** | Reliable, scalable relational database with advanced indexing features. |
| **Authentication**| **Django Simple JWT** | Secure, token-based authentication (Bearer tokens). |
| **Async/Queuing**| **Celery, RabbitMQ (CloudAMQP)** | Manages high-volume or long-running tasks asynchronously. |
| **Deployment** | **Docker, Render** | Containerization and cloud hosting for scalability and portability. |
| **Documentation**| **DRF Spectacular (Swagger)** | Auto-generated, interactive API documentation. |

---

## ⚙️ Build and Deployment Process (Zero to Hero)

The application is deployed as a **Dockerized Web Service** on **Render**. This section details the steps and environment configuration that ensures the application is highly available and production-ready.

### 1. The Containerization (Dockerfile)

The `Dockerfile` is the blueprint for the production environment, ensuring consistency across all environments.

* **Base Image:** `FROM python:3.10-slim` for a minimal, secure base.
* **Dependencies:** Installs necessary tools (`build-essential`, `libpq-dev`) to compile Python packages.
* **Security:** Creates and switches to an unprivileged `appuser` for running the application.
* **Runtime Command (The Fix):** The final `CMD` ensures Gunicorn binds to the port defined by Render's environment variable (`$PORT`).

```dockerfile
# ... Dockerfile setup steps ...
# 🌟 CRITICAL FIX: Use JSON-array form with bash -c to evaluate $PORT 🌟
CMD ["bash", "-c", "gunicorn jobboard.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3"]
````

### 2\. The Render Configuration (Web Service)

| Configuration | Value | Description |
| :--- | :--- | :--- |
| **Type** | Web Service (using Docker) | Tells Render to use the `Dockerfile` for the build. |
| **Build Command**| `pip install -r requirements.txt && python manage.py collectstatic --noinput` | Installs dependencies and prepares static files during the build phase. |
| **Start Command**| `gunicorn jobboard.wsgi:application --bind 0.0.0.0:$PORT` | The primary runtime command (backed up by the Dockerfile's `CMD`). |
| **Environment** | **PostgreSQL, CloudAMQP** | External services are connected via Environment Variables provided by Render. |

### 3\. Environment Variables (The Credentials)

The following variables are crucial for the production environment and are securely configured on Render's dashboard:

| Key | Value Example | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | `39%pj3jbgh#mge7k4ube...` | High-entropy Django secret key for security. |
| `PORT` | `8000` | The port Render requires the service to bind to. |
| `DATABASE_URL` | `postgresql://jobboard_db_t5z9_user...` | Connection string to the managed Render PostgreSQL instance. |
| `CELERY_BROKER_URL`| `amaps://zjpmzhnw:Cc13y9BkrBXgbb1Hq-...` | Secure connection to the external CloudAMQP (RabbitMQ) message broker. |
| `DJANGO_ALLOWED_HOSTS`| `project-nexus-uulu.onrender.com` | Prevents HTTP Host header attacks in production. |

### 4\. Zero Downtime Deployment Flow

1.  **Trigger:** A push to the `main` branch triggers an automated deployment on Render.
2.  **Container Build:** The `Dockerfile` is executed, creating a new, up-to-date image.
3.  **Entrypoint Execution:** The `entrypoint.sh` script runs necessary setup, including **database migrations** and `collectstatic`.
4.  **Service Swap:** The new container starts, Gunicorn successfully binds to port `8000` (**Verified in logs**), and Render routes traffic to the new healthy instance, ensuring **zero downtime**.

-----

## 🗺️ API Documentation (Swagger UI)

The interactive API documentation is essential for frontend collaborators and is hosted directly alongside the API.

  * **Swagger UI (Documentation):** `https://project-nexus-uulu.onrender.com/api/docs/`
  * **API Schema:** `https://project-nexus-uulu.onrender.com/api/schema/`

-----

## 🤝 Collaboration & Review

This project fulfills the requirements for the ProDev Backend Engineering program.
  * **Presentation:** The project is prepared for a live demonstration, showcasing functionality, code quality, and the deployed architecture.
  * **Frontend Collaboration:** Frontend learners can use the **Swagger UI** link above to quickly understand and integrate with all available endpoints.

<!-- end list -->

```
```