"""
Django settings for mprj_api project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from decouple import config, Csv
from dj_database_url import parse as db_url
from datetime import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'ordered_model',
    'corsheaders',
    'colorfield',

    'dominio',
    'icones',
    'lupa',
    'login',
    'mprj_plus',
    'nested_admin',
    'desaparecidos',
    'proxies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if config('CORS', default=False, cast=bool):
    MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

ROOT_URLCONF = 'mprj_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mprj_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        cast=db_url
    ),
    'dominio_db': config(
        'DOMINIO_DB',
        default='sqlite:///' + os.path.join(BASE_DIR, 'dominio.sqlite3'),
        cast=db_url
    )
}

TABLE_NAMESPACE = config('TABLE_NAMESPACE')
IMPALA_HOST = config('IMPALA_HOST')
IMPALA_PORT = config('IMPALA_PORT', cast=int)

PG_HOST = config('PG_HOST')
PG_BASE = config('PG_BASE')
PG_USER = config('PG_USER')
PG_PASSWORD = config('PG_PASSWORD', "")

ORA_USER = config('ORA_USER')
ORA_PASS = config('ORA_PASS')
ORA_HOST = config('ORA_HOST')


DATABASE_ROUTERS = ['mprj_api.db_routers.DominioRouter']

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = config(
    'STATIC_URL',
    default='/static'
)
STATIC_ROOT = config(
    'STATIC_ROOT',
    default=os.path.join(BASE_DIR, 'static')
)

MEDIA_URL = config(
    'MEDIA_URL',
    default='/media'
)
MEDIA_ROOT = config(
    'MEDIA_ROOT',
    default=os.path.join(BASE_DIR, 'media')
)

# CORS configuration

CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = ['*']

# E-mail
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# CACHE Configuration
CACHE_BACKEND = config(
    "CACHE_BACKEND", default='django.core.cache.backends.locmem.LocMemCache'
)
CACHES = {
    'default': {
        'BACKEND': CACHE_BACKEND,
        'LOCATION': config(
            'CACHE_LOCATION',
            default='localhost:6379'
        ),
        'OPTIONS': {
            'DB': config(
                'CACHE_DATABASE_NUMBER',
                default=1
            ),
        }
    }
}
CACHE_TIMEOUT = config("CACHE_TIMEOUT", default=300, cast=int)

JWT_SECRET = SECRET_KEY

#HBASE
HBASE_SERVER = config("HBASE_SERVER")
HBASE_TIMEOUT = config("HBASE_TIMEOUT", cast=int, default=300000)
HBASE_DETRAN_BASE = config("HBASE_DETRAN_BASE")

IMPALA_DETRAN_TABLE = config("IMPALA_DETRAN_TABLE")
