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

# Get the secret key from the environment. This is critical for security.
SECRET_KEY = os.getenv('SECRET_KEY')

# Determine if we are in the Render production environment.
# Render automatically sets the 'IS_RENDER' variable to 'True'.
IS_PRODUCTION = os.getenv('IS_RENDER', 'False') == 'True'

# DEBUG is True for local development and ALWAYS False for production.
DEBUG = not IS_PRODUCTION


# ==============================================================================
# HOSTS, CORS, AND CSRF CONFIGURATION
# ==============================================================================

# Define allowed hosts for security.
if IS_PRODUCTION:
    # On Render, get the hostname from the env var it provides.
    render_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    # Use the manual host from our env vars as a reliable backup.
    manual_hostname = os.getenv('ALLOWED_HOST')

    ALLOWED_HOSTS = []
    if render_hostname:
        ALLOWED_HOSTS.append(render_hostname)
    if manual_hostname:
        ALLOWED_HOSTS.append(manual_hostname)
else:
    # For local development, only allow these.
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Configure Cross-Origin Resource Sharing (CORS) and Cross-Site Request Forgery (CSRF).
# This tells our backend which frontend domains are allowed to talk to it.
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173') # Default for local dev

CORS_ALLOWED_ORIGINS = [
    # Add your Vercel frontend URL from the environment variable.
    frontend_url,
    # Also keep the local development URLs for convenience.
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
# For security, tell Django that it can trust POST/PUT requests from our frontend domain.
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS


# ==============================================================================
# DJANGO APPLICATIONS AND MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # For serving static files in development
    'django.contrib.staticfiles',
    # 3rd Party Apps
    'rest_framework',
    'corsheaders',
    # Our App
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Should be right after security
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Placed high up
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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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