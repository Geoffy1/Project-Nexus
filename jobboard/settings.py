import os
from pathlib import Path
import environ
import datetime
import dj_database_url  # ✅ Enabled for Render DB parsing

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ----------------------------
# 🔐 SECURITY & CORE SETTINGS
# ----------------------------

SECRET_KEY = os.getenv("SECRET_KEY", env("SECRET_KEY", default="changeme"))
if SECRET_KEY == "changeme" and not env.bool("DEBUG", default=True):
    raise Exception('SECRET_KEY environment variable is required in production')

DEBUG = os.getenv("DEBUG", "False") == "True"

allowed_hosts_str = os.getenv("DJANGO_ALLOWED_HOSTS", env("DJANGO_ALLOWED_HOSTS", default="localhost"))
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_str.split(",") if h.strip()]

if not DEBUG and not ALLOWED_HOSTS:
    raise Exception("ALLOWED_HOSTS must be set in production")

# ----------------------------
# 🗄️ DATABASE CONFIGURATION
# ----------------------------

# ✅ Use Render’s DATABASE_URL automatically
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://jobboard_db_t5z9_user:33HSE0dx6iGjQD6xYhdKIyafHTBZ9pfc@dpg-d3cq252li9vc73dqaif0-a/jobboard_db_t5z9"
)
DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
}

# ----------------------------
# 📦 STATIC & MEDIA FILES
# ----------------------------

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ----------------------------
# 🐇 CELERY CONFIGURATION
# ----------------------------

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL",
    env("CELERY_BROKER_URL", default="amqp://guest:guest@rabbitmq:5672//")
)
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND",
    env("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")
)

# ----------------------------
# 🧩 INSTALLED APPS
# ----------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third-party
    "rest_framework",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",

    # local apps
    "accounts",
    "jobs",
    "applications",
    "django.contrib.postgres",
]

# ----------------------------
# ⚙️ MIDDLEWARE
# ----------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "jobboard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "jobboard.wsgi.application"

# ----------------------------
# 👥 AUTHENTICATION
# ----------------------------

AUTH_USER_MODEL = "accounts.User"

# ----------------------------
# 🔐 REST FRAMEWORK
# ----------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Job Board API",
    "DESCRIPTION": "API docs for Project Nexus job board",
    "VERSION": "1.0.0",
}

# ----------------------------
# 🌍 INTERNATIONALIZATION
# ----------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------
# 🔐 PASSWORD VALIDATORS
# ----------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]



# # jobboard/settings.py
# import os
# from pathlib import Path
# import environ
# import datetime
# # import dj_database_url # Uncomment if you want to use dj-database-url for DATABASE_URL

# BASE_DIR = Path(__file__).resolve().parent.parent
# env = environ.Env()
# # Read .env file for development and local variables
# environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# # --- PRODUCTION / ENVIRONMENT-CRITICAL SETTINGS ---
# # Use os.getenv for critical settings often set by hosting environment
# # SECRET_KEY: Must be set in the production environment
# SECRET_KEY = os.getenv("SECRET_KEY", env("SECRET_KEY", default="changeme"))
# if SECRET_KEY == "changeme" and not env.bool("DEBUG", default=True):
#     raise Exception('SECRET_KEY environment variable is required in production')

# # DEBUG: Use environment variable, default to False if not explicitly set
# DEBUG = os.getenv('DEBUG', 'False') == 'True'

# # ALLOWED_HOSTS: Read from environment, or fall back to .env/default
# allowed_hosts_str = os.getenv('DJANGO_ALLOWED_HOSTS', env("DJANGO_ALLOWED_HOSTS", default="localhost"))
# ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_str.split(',') if h.strip()]
# if not DEBUG and not ALLOWED_HOSTS:
#     raise Exception('ALLOWED_HOSTS must be set in production')

# # Static files (WhiteNoise configuration)
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATIC_URL = "/static/"
# # Use CompressedManifestStaticFilesStorage for cache-busting in production
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# # Celery: Prefer environment variables set by hosting platform
# CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", env("CELERY_BROKER_URL", default="amqp://guest:guest@rabbitmq:5672//"))
# CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", env("CELERY_RESULT_BACKEND", default="redis://redis:6379/0"))

# # DATABASES: Prefer environment variable (e.g., set by hosting platform)
# # If using dj-database-url:
# # try:
# #     DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}
# # except Exception:
# #     # Fallback to env.db() if DATABASE_URL is not set or parse fails
# #     DATABASES = {
# #         "default": env.db("DATABASE_URL", default="postgresql://jobboard_db_t5z9_user:33HSE0dx6iGjQD6xYhdKIyafHTBZ9pfc@dpg-d3cq252li9vc73dqaif0-a/jobboard_db_t5z9")
# #     }
# # Else, just use the environ setup:
# DATABASES = {
#     "default": env.db("DATABASE_URL", default="postgresql://jobboard_db_t5z9_user:33HSE0dx6iGjQD6xYhdKIyafHTBZ9pfc@dpg-d3cq252li9vc73dqaif0-a/jobboard_db_t5z9")
# }


# # --- GENERAL & DJANGO CORE SETTINGS ---

# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # third-party
#     "rest_framework",
#     "drf_spectacular",
#     "rest_framework_simplejwt", # Added simplejwt
#     "django_filters",
#     "corsheaders",

#     # local apps
#     "accounts",
#     "jobs",
#     "applications",
#     'django.contrib.postgres',
# ]

# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     # WhiteNoise must be near the top
#     "whitenoise.middleware.WhiteNoiseMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "corsheaders.middleware.CorsMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "jobboard.urls"

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [],
#         "APP_DIRS": True,
#         "OPTIONS": {"context_processors": [
#             "django.template.context_processors.debug",
#             "django.template.context_processors.request",
#             "django.contrib.auth.context_processors.auth",
#             "django.contrib.messages.context_processors.messages",
#         ],},
#     },
# ]

# WSGI_APPLICATION = "jobboard.wsgi.application"

# AUTH_USER_MODEL = "accounts.User"


# # --- REST FRAMEWORK & SECURITY SETTINGS ---

# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
#     "DEFAULT_FILTER_BACKENDS": [
#         "django_filters.rest_framework.DjangoFilterBackend",
#         "rest_framework.filters.SearchFilter",
#         "rest_framework.filters.OrderingFilter",
#     ],
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 10,
# }

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=60),
#     "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
# }

# SPECTACULAR_SETTINGS = {
#     "TITLE": "Job Board API",
#     "DESCRIPTION": "API docs for Project Nexus job board",
#     "VERSION": "1.0.0",
# }


# # --- INTERNATIONALIZATION & MISC ---

# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "UTC"
# USE_I18N = True
# USE_TZ = True


# # --- AUTH & PASSWORD VALIDATION (Defaults) ---

# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
# ]