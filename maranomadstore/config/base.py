"""
Django settings for maranomadstore project.

Generated by 'django-admin startproject' using Django 4.1.2.
"""

import os
from datetime import timedelta
from pathlib import Path

import braintree
import environ
from django.utils.translation import gettext_lazy as _

env = environ.Env()
# reading .env file
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# General

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale/")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

DEBUG = True

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", _("English")),
    ("es", _("Spanish")),
)

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
ROOT_URLCONF = "maranomadstore.urls"
WSGI_APPLICATION = "maranomadstore.wsgi.application"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-2o7lpg2s6txb$w6y74v%x(p5(c6t8d*nf#$g@xcy%788-@r8a-"


ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_seeder",
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

LOCAL_APPS = [
    "accounts",
    "duka",
    "cart",
    "orders",
    "payment",
    "coupons",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # for lingua transation
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC

# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "staticfiles"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# MEDIA
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

print("\n\n\n")
print(os.path.join(BASE_DIR.parent, "templates/"))
print("\n\n\n")

# TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR.parent, "templates/")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
                "accounts.context_processors.allauth_settings",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
# FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# AUTHENTICATION
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_ADAPTER = "accounts.adapters.AccountAdapter"
ACCOUNT_FORMS = {"signup": "accounts.forms.UserSignupForm"}
SOCIALACCOUNT_ADAPTER = "accounts.adapters.SocialAccountAdapter"
SOCIALACCOUNT_FORMS = {"signup": "accounts.forms.UserSocialSignupForm"}


# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "accounts.CustomUser"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "accounts:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# PAYMENTS
BRAINTREE_CONF = braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id="123",
    public_key="123",
    private_key="12345",
    # merchant_id=env("BRAINTREE_MERCHANT_ID"),
    # public_key=env("BRAINTREE_PUBLIC_KEY"),
    # private_key=env("BRAINTREE_PRIVATE_KEY"),
)

CART_SESSION_ID = "cart"

# REDIS
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 1

# EMAIL
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5


# ADMIN
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Marvin Kweyu""", "hello@marvinkweyu.net")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# Django rest framework
# If intergrating with the REST framework, these will be the default settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.CursorPagination",
    "PAGE_SIZE": 30,
}


SPECTACULAR_SETTINGS = {
    "TITLE": "The Mara Nomad Store API",
    "DESCRIPTION": "Documentation of API endpoints for The Mara Nomad Store",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "maranomads",
    "JWT_AUTH_REFRESH_COOKIE": "maranomads-refresh-token",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}
