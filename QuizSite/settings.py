"""
Django settings for QuizSite project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from django.core.management.utils import get_random_secret_key

SECRET_KEY = os.getenv("DJANGO_SECRET", '7m2Tvxb7olx576cfupqURRWEcnlOhVdFNqyoVbfSYeFxDLORRL')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # os.getenv("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    '127.0.0.1',
    '161.35.252.20',
    '104.248.224.128',
    'www.quizbox.app',
    'quizbox.app',
    '*.quizbox.app',
    'localhost',
    'quiz-box.azurewebsites.net',
    '*.azurewebsites.net',
]

CSRF_TRUSTED_ORIGINS = [
    'https://www.quizbox.app',
    'https://quizbox.app',
    'https://quizbox-site-wzdyo.ondigitalocean.app',
    'https://*.azurewebsites.net',
]

# Application definition

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = [
    'Records.apps.RecordsConfig',
    'Quiz.apps.QuizConfig',
    'Bracket.apps.BracketConfig',
    # 'Auth.apps.AuthConfig',
    'api.apps.ApiConfig',
    'Material.apps.MaterialConfig',
    'TournamentManager.apps.TournamentmanagerConfig',
    'quiz_games.apps.QuizGamesConfig',

    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.google',

    'django_simple_tags',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'QuizSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # `allauth` needs this from django
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'QuizSite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql'

#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'quizdb_prod',
        'USER': 'doadmin',
        'PASSWORD': 'AVNS_inpSFP2HTHFolJTB4EY',
        'HOST': 'quizbox-dbs-do-user-12108150-0.b.db.ondigitalocean.com',
        'PORT': 25060,
        # 'OPTIONS': {
        #     'sslmode': 'require',
        #     'sslrootcert': BASE_DIR / 'ca-certificate.crt',
        #
        # },

    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # # {
    # #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # # },
    # # {
    # #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    # '/var/www/static/',
]

STATIC_ROOT = BASE_DIR / '/collected_static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Email Settings. Does mine work?
# EMAIL_HOST = "smtp.migadu.org"
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
