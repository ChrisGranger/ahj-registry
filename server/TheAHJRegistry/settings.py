"""
Django settings for TheAHJRegistry project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from typing import List
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yk8a3q*uo4o$m+k+o!zt&a@9v7)@9w4cg&qc0j&tur587#w#bm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS: List[str] = []

GEOS_LIBRARY_PATH = '/usr/local/lib/libgeos_c.so'

GDAL_LIBRARY_PATH = '/usr/local/lib/libgdal.so'


# Application definition

INSTALLED_APPS = [
    'ahj_app.apps.AhjAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'django_filters',
    'ahj_app.apps.AhjConfig',
    'djoser',
    'corsheaders',
    'simple_history'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'ahj_app.middleware.LoggingMiddleware.SkipRequestLoggingMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3030',
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:3030',
]

ROOT_URLCONF = 'TheAHJRegistry.urls'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': {
        'django_filters.rest_framework.DjangoFilterBackend'
    },
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'ahj_app.authentication.WebpageTokenAuth',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        # 'rest_framework.throttling.UserRateThrottle',
        # 'rest_framework.throttling.AnonRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        # 'user': '10/day',
        'anon': '10/day'
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'TheAHJRegistry.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': '',
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'OPTIONS': {
            'sql_mode': 'STRICT_ALL_TABLES',
        },
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
            'verbose': {
                'format': '{levelname} {request.user} {request.auth} {request.META[REMOTE_ADDR]} {asctime} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{request.user} {message}',
                'style': '{',
            },
        },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/api.log'),
            'when': 'midnight',
            'backupCount': 14,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SUNSPEC_SUPPORT_EMAIL = 'support@sunspec.org'

DOMAIN = 'localhost:8080'
SITE_NAME = 'AHJ Registry'

DJOSER = {
    'LOGIN_FIELD': 'Email',
    'TOKEN_MODEL': 'ahj_app.models.WebpageToken',

    'Password_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': '#/password_reset_confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,

    'SERIALIZERS': {
        'user_create': 'ahj_app.serializers.UserCreateSerializer',
        'user': 'ahj_app.serializers.UserCreateSerializer',
        'token': 'ahj_app.serializers.WebpageTokenSerializer'
    }
}

AUTH_USER_MODEL = 'ahj_app.User'
ADMIN_ACCOUNT_USERNAME = ''
ADMIN_ACCOUNT_EMAIL = ''
ADMIN_ACCOUNT_PASSWORD = ''
APPLY_APPROVED_EDITS = True

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

GOOGLE_MAPS_KEY = ''
