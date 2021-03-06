"""
Django settings for mprj_api project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta

from decouple import config, Csv
from dj_database_url import parse as db_url
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent.parent

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
        default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
        cast=db_url
    ),
    'dominio_db': config(
        'DOMINIO_DB',
        default='sqlite:///' + BASE_DIR.child('dominio.sqlite3'),
        cast=db_url
    )
}

TABLE_NAMESPACE = config('TABLE_NAMESPACE')
EXADATA_NAMESPACE = config("EXADATA_NAMESPACE")
ALERTAS_NAMESPACE = config("ALERTAS_NAMESPACE")
IMPALA_HOST = config('IMPALA_HOST')
IMPALA_PORT = config('IMPALA_PORT', cast=int)

SCHEMA_ALERTAS = config("SCHEMA_ALERTAS")
SCHEMA_OPENGEO_BDA = config("SCHEMA_OPENGEO_BDA")

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
    default=BASE_DIR.child('static')
)

MEDIA_URL = config(
    'MEDIA_URL',
    default='/media'
)
MEDIA_ROOT = config(
    'MEDIA_ROOT',
    default=BASE_DIR.child('media')
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} - {pathname}:{funcName} --> {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR.child("dominio_login.log"),
            'formatter': 'verbose',
        },
        'file_proxies': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR.child("proxies.log"),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config("DJANGO_LOG_LEVEL", default="INFO"),
        },
        'proxies': {
            'level': config("PROXIES_LOG_LEVEL", default="INFO"),
            'formatter': 'verbose',
            'handlers': ['console', 'file_proxies'],
            'propagate': True,
        },
        'dominio.login': {
            'level': config("DOMINIO_LOG_LEVEL", default="INFO"),
            'formatter': 'verbose',
            'handlers': ['console', 'file'],
            'propagate': True,
        },
    },
}




JWT_SECRET = SECRET_KEY

#HBASE
HBASE_SERVER = config("HBASE_SERVER")
HBASE_TIMEOUT = config("HBASE_TIMEOUT", cast=int, default=300000)
EXADATA_DETRAN_PHOTO_ORIGIN = config("EXADATA_DETRAN_PHOTO_ORIGIN")

HBASE_DISPENSAR_ALERTAS_TABLE = config("HBASE_DISPENSAR_ALERTAS_TABLE")
HBASE_DISPENSAR_ALLALERTAS_TABLE = config("HBASE_DISPENSAR_ALLALERTAS_TABLE")
HBASE_ALERTAS_OUVIDORIA_TABLE = config("HBASE_ALERTAS_OUVIDORIA_TABLE")

EXADATA_DETRAN_DATA_ORIGIN = config("EXADATA_DETRAN_DATA_ORIGIN")

# SIMPLE AUTH
SIMPLE_AUTH_TOKEN = config("SIMPLE_AUTH_TOKEN")
CADUNICO_AUTH_TOKEN = config("CADUNICO_AUTH_TOKEN", default="token")

# DETRAN
DETRAN_CNPJ = config("DETRAN_CNPJ")
DETRAN_CHAVE = config("DETRAN_CHAVE")
DETRAN_PERFIL = config("DETRAN_PERFIL")
DETRAN_CPF = config("DETRAN_CPF")
DETRAN_URL_ENVIO = config("DETRAN_URL_ENVIO")
DETRAN_URL_BUSCA = config("DETRAN_URL_BUSCA")

PROMOTRON_HBASE_SERVER = config("PROMOTRON_HBASE_SERVER")
PROMOTRON_HBASE_NAMESPACE = config("PROMOTRON_HBASE_NAMESPACE")
PROMOTRON_HBASE_TIMEOUT = config("PROMOTRON_HBASE_TIMEOUT", cast=int, default=300000)

# SCA
SCA_AUTH = config("SCA_AUTH")
SCA_CHECK = config("SCA_CHECK")

# DOMINIO
DOMINIO_ESPECIAL_ROLES = config("DOMINIO_ESPECIAL_ROLES", cast=Csv())

# DESAPARECIDOS
DESAPARECIDOS_DB_USER = config('DESAPARECIDOS_DB_USER')
DESAPARECIDOS_DB_PWD = config('DESAPARECIDOS_DB_PWD')
DESAPARECIDOS_DB_HOST = config('DESAPARECIDOS_DB_HOST')
DESAPARECIDOS_DATA_LEN = config('DESAPARECIDOS_DATA_LEN', cast=int)
DESAPARECIDOS_CACHE_TIMEOUT = config(
    'DESAPARECIDOS_CACHE_TIMEOUT',
    cast=int,
    default=86400
)
PROXIES_PLACAS_ROLE = config("PROXIES_PLACAS_ROLE", default="role")

ACCESS_TOKEN_LIFETIME = config("ACCESS_TOKEN_LIFETIME", cast=int, default=5)
REFRESH_TOKEN_LIFETIME = config("REFRESH_TOKEN_LIFETIME", cast=int, default=1)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME),
}

#SOLR
ZOOKEEPER_SERVER = config("ZOOKEEPER_SERVER", default="zookeeper")
PLACAS_SOLR_COLLECTION = config("PLACAS_SOLR_COLLECTION", default="placas")
PLACAS_SOLR_MAX_ROWS = config("PLACAS_SOLR_MAX_ROWS", cast=int, default=1_000)

HOST_SOLR = config("HOST_SOLR", "host-solr")

#EMAIL
EMAIL_SMTP_SERVER = config("EMAIL_SMTP_SERVER")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_OUVIDORIA = config("EMAIL_OUVIDORIA")


EMAIL_SUBJECT_OUVIDORIA_COMPRAS = config("EMAIL_SUBJECT_OUVIDORIA_COMPRAS")
EMAIL_SUBJECT_OUVIDORIA_SANEAMENTO = config(
    "EMAIL_SUBJECT_OUVIDORIA_SANEAMENTO"
)

#KERBEROS AUTH
KERBEROS_USER = config("KERBEROS_USER")
KERBEROS_SERVICE_NAME = config("KERBEROS_SERVICE_NAME")


URL_PAINEL_COMPRAS = config(
    "URL_PAINEL_COMPRAS",
    default="https://tableau2020.mprj.mp.br/t/MPMAPAS/views/"
    "TESTE-COVID-19GATE/CONUnidadeGestora?"
    ":isGuestRedirectFromVizportal=y&:embed=y&:linktarget=_self"
    "&:tabs=no&:tollbar=yes&contrato_iditem={contrato_iditem}"
    "&CONTRATACAO={contratacao}"
)
URL_PAINEL_SANEAMENTO = config(
    "URL_PAINEL_SANEAMENTO",
    "https://geo.mprj.mp.br/portal/apps/experiencebuilder/experience/"
    "?id=35ae775b7f37418c9c65f47d62943d67"
)

PROMOTOR_CARGO_SIGLA = config("PROMOTOR_CARGO_SIGLA", default="PJ")
FUNCIONARIO_CARGO_SIGLA = config("FUNCIONARIO_CARGO_SIGLA", default="FUNC")

CADUNICO_SOLR_MAX_ROWS = config("CADUNICO_SOLR_MAX_ROWS", cast=int, default=10)
