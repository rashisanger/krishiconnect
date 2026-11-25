
"""
Django settings for krishiconnect project.
"""

import os
import secrets
from pathlib import Path
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the project root .env file
load_dotenv(BASE_DIR / '.env')


# Security settings
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development').strip().lower()
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '').strip()
if DJANGO_ENV != 'development' and (
    not SECRET_KEY or SECRET_KEY.startswith('replace_with_')
):
    raise ImproperlyConfigured(
        'Set a unique DJANGO_SECRET_KEY outside development.'
    )
if not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(64)

DEBUG = os.getenv('DJANGO_DEBUG', 'False').strip().lower() in {'1', 'true', 'yes'}

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        'DJANGO_ALLOWED_HOSTS',
        'localhost,127.0.0.1,spied-harmonize-silliness.ngrok-free.dev',
    ).split(',')
    if host.strip()
]

# ngrok and other reverse proxies terminate HTTPS before forwarding to Django.
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.getenv(
    'SECURE_SSL_REDIRECT', 'True' if DJANGO_ENV == 'production' else 'False'
).strip().lower() in {'1', 'true', 'yes'}
SESSION_COOKIE_SECURE = os.getenv(
    'SESSION_COOKIE_SECURE', 'True' if DJANGO_ENV == 'production' else 'False'
).strip().lower() in {'1', 'true', 'yes'}
CSRF_COOKIE_SECURE = os.getenv(
    'CSRF_COOKIE_SECURE', 'True' if DJANGO_ENV == 'production' else 'False'
).strip().lower() in {'1', 'true', 'yes'}
SECURE_HSTS_SECONDS = int(os.getenv(
    'SECURE_HSTS_SECONDS', '3600' if DJANGO_ENV == 'production' else '0'
))
SECURE_CONTENT_TYPE_NOSNIFF = True


# Agmarknet API configuration
AGMARKNET_API_KEY = os.getenv('AGMARKNET_API_KEY', '')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'accounts',
    'farmers',
    'buyers',
    'crops',
    'market_prices',
    'enquiries',
    'analytics',

    'rest_framework_simplejwt.token_blacklist',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'krishiconnect.urls'


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


WSGI_APPLICATION = 'krishiconnect.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
SERVE_STATIC_FILES = os.getenv(
    'SERVE_STATIC_FILES', 'True' if DJANGO_ENV == 'development' else 'False'
).strip().lower() in {
    '1', 'true', 'yes'
}


# Email
default_email_backend = os.getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
    if DJANGO_ENV == 'production'
    else 'django.core.mail.backends.console.EmailBackend',
)
MAILERS = {
    'default': {
        'BACKEND': default_email_backend,
        'OPTIONS': ({
            'host': os.getenv('EMAIL_HOST', 'localhost'),
            'port': int(os.getenv('EMAIL_PORT', '25')),
            'use_tls': os.getenv('EMAIL_USE_TLS', 'False').strip().lower() in {'1', 'true', 'yes'},
            'use_ssl': os.getenv('EMAIL_USE_SSL', 'False').strip().lower() in {'1', 'true', 'yes'},
            'username': os.getenv('EMAIL_HOST_USER', ''),
            'password': os.getenv('EMAIL_HOST_PASSWORD', ''),
        } if default_email_backend.endswith('.smtp.EmailBackend') else {}),
    },
}


# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    origin.strip().rstrip('/')
    for origin in os.getenv(
        'CORS_ALLOWED_ORIGINS',
        ','.join([
            'http://localhost:3000',
            'http://127.0.0.1:3000',
            'http://localhost:4200',
            'http://127.0.0.1:4200',
            'http://localhost:5173',
            'http://127.0.0.1:5173',
        ]),
    ).split(',')
    if origin.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip().rstrip('/')
    for origin in os.getenv(
        'CSRF_TRUSTED_ORIGINS',
        ','.join([
            'http://localhost:5173',
            'http://127.0.0.1:5173',
            'http://localhost:3000',
            'http://127.0.0.1:3000',
            'https://spied-harmonize-silliness.ngrok-free.dev',
        ]),
    ).split(',')
    if origin.strip()
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'
