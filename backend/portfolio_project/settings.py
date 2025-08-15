# backend/portfolio_project/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file for local development
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = os.getenv('SECRET_KEY')

# Determine if we are in the Render production environment
IS_PRODUCTION = os.getenv('IS_RENDER', 'False') == 'True'

# DEBUG is True for local development and ALWAYS False for production
DEBUG = not IS_PRODUCTION


# ==============================================================================
# HOSTS, CORS, AND SECURITY CONFIGURATION
# ==============================================================================

ALLOWED_HOSTS = []
if IS_PRODUCTION:
    render_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if render_hostname:
        ALLOWED_HOSTS.append(render_hostname)
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Get the frontend URL from environment variables for production, with a fallback for local dev
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

# CORS settings: A list of origins that are authorized to make cross-site HTTP requests.
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
    # Also include local dev URLs in the list for convenience
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# CSRF settings: A list of hosts which are trusted for cross-site sharing of credentials.
CSRF_TRUSTED_ORIGINS = [
    FRONTEND_URL,
    # Also include local dev URLs
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Production-only security settings suggested by the other LLM
if IS_PRODUCTION:
    
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Optional but recommended security headers
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# ==============================================================================
# CACHING CONFIGURATION (WITH REDIS FOR PRODUCTION)
# ==============================================================================

# Use Redis for caching if the REDIS_URL is available (in production on Render)
if 'REDIS_URL' in os.environ:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ.get('REDIS_URL'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
# Otherwise, use the simple in-memory cache for local development
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
# ==============================================================================
# DJANGO APPLICATIONS AND MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio_project.urls'
WSGI_APPLICATION = 'portfolio_project.wsgi.application'


# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}


# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedRootStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==============================================================================
# TEMPLATES, PASSWORDS, AND INTERNATIONALIZATION
# ==============================================================================

TEMPLATES = [
    {'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}},
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# DJANGO DEFAULTS
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'