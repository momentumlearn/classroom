"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from pathlib import Path

import environ
import django_heroku

# Build paths inside the project like this: BASE_DIR / path
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["127.0.0.1"]),
    SMTP_HOST=(str, None),
    SMTP_PORT=(int, 25),
    SMTP_USERNAME=(str, None),
    SMTP_PASSWORD=(str, None),
    SENTRY_DSN=(str, None),
    DJANGO_SECRET_KEY=(str, "-*vs66ys__8fn#p9i!t6f3zepdgtn(@d%6*j&6cm)tftpv4cko"),
)

if (Path(os.path.dirname(os.path.abspath(__file__))) / ".env").exists():
    environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # 3rd party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_extensions",
    "django_better_admin_arrayfield.apps.DjangoBetterAdminArrayfieldConfig",
    "crispy_forms",
    "adminsortable",
    "debug_toolbar",
    # My apps
    "users",
    "evaluations",
    "djanky",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "djanky.context_processors.js_data",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {"default": env.db()}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Authentication

SITE_ID = 1

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

INTERNAL_IPS = [
    "127.0.0.1",
]

# Mail

DEFAULT_FROM_EMAIL = "info@momentumlearn.com"

if env("SMTP_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("SMTP_HOST")
    EMAIL_PORT = env("SMTP_PORT")
    EMAIL_HOST_USER = env("SMTP_USERNAME")
    EMAIL_HOST_PASSWORD = env("SMTP_PASSWORD")
    EMAIL_USE_TLS = True

else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if env("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

# Configure Django App for Heroku.
django_heroku.settings(locals())
del DATABASES["default"]["OPTIONS"]["sslmode"]
