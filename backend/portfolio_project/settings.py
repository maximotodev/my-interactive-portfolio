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

# Get the secret key from the environment
SECRET_KEY = os.getenv('SECRET_KEY')

# Determine if we are in the Render production environment
# Render automatically sets the 'IS_RENDER' variable to 'True'
IS_PRODUCTION = os.getenv('IS_RENDER', 'False') == 'True'

# DEBUG is True for local development and False for production
DEBUG = not IS_PRODUCTION


# ==============================================================================
# HOSTS & CORS CONFIGURATION
# ==============================================================================

# Define allowed hosts for security
if IS_PRODUCTION:
    # On Render, the RENDER_EXTERNAL_HOSTNAME is automatically provided
    render_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    ALLOWED_HOSTS = [render_hostname] if render_hostname else []
else:
    # For local development
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Configure Cross-Origin Resource Sharing (CORS)
if IS_PRODUCTION:
    # For production, get the live frontend URL from an environment variable on Render
    frontend_url = os.getenv('FRONTEND_URL')
    CORS_ALLOWED_ORIGINS = [frontend_url] if frontend_url else []
else:
    # For local development, allow the Vite server's address
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


# ==============================================================================
# DJANGO APPLICATIONS AND MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # WhiteNoise is added here for serving static files efficiently
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # 3rd Party Apps
    'rest_framework',
    'corsheaders',
    # Our App
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise Middleware should be placed right after the security middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS middleware should be placed high up
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
        conn_max_age=600 # Keep connections alive for 10 minutes
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