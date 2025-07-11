# backend/portfolio_project/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

# Get the secret key from the environment
SECRET_KEY = os.getenv('SECRET_KEY')

# Determine if we are in a production environment (like Render)
IS_PRODUCTION = os.getenv('IS_RENDER', 'False') == 'True'

# Set DEBUG mode based on the environment
DEBUG = not IS_PRODUCTION


# ==============================================================================
# HOSTS & CORS CONFIGURATION
# ==============================================================================

# Define allowed hosts for security
if IS_PRODUCTION:
    # On Render, the RENDER_EXTERNAL_HOSTNAME is automatically provided
    render_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if render_hostname:
        ALLOWED_HOSTS = [render_hostname]
    else:
        ALLOWED_HOSTS = [] # Should not happen, but a safe default
else:
    # For local development, allow localhost and 127.0.0.1
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Configure Cross-Origin Resource Sharing (CORS)
# This allows our React frontend to make API calls to our Django backend.
if IS_PRODUCTION:
    # For production, we get the frontend URL from an environment variable
    CORS_ALLOWED_ORIGINS = [
        os.getenv('FRONTEND_URL', '') # e.g., 'https://my-portfolio.vercel.app'
    ]
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
    # CORS middleware should be placed high up, before common middleware
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

# Use dj-database-url to parse the DATABASE_URL environment variable
# This works for both local PostgreSQL and Render's managed database.
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600 # Keep connections alive for 10 minutes
    )
}


# ==============================================================================
# STATIC & MEDIA FILES (for user uploads and CSS/JS)
# ==============================================================================

# URL to use when referring to static files located in STATIC_ROOT
STATIC_URL = '/static/'
# The absolute path to the directory where collectstatic will gather static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Use WhiteNoise's storage backend for efficient caching and compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# URL that handles the media served from MEDIA_ROOT
MEDIA_URL = '/media/'
# The absolute path to the directory that will hold user-uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==============================================================================
# TEMPLATES, PASSWORDS, AND INTERNATIONALIZATION (Standard Django Settings)
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
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