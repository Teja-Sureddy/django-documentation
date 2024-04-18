"""
Django settings for my_project project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import environ
import os

env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-fwbxeelgwxbx*+xp=qk7q07n7d#yaaafqrc1$!l@4lbhs+yyz-"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = []

INTERNAL_IPS = ["127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "debug_toolbar",
    "django_tables2",
    "django_filters",
    "django_htmx",
    "phonenumber_field",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.mfa",
    "rest_framework",
    "rest_framework.authtoken",
    "notifications",
    "channels",
    "django_q",
    "django_celery_results",
    # custom
    "my_apps.dashboard",
    "my_apps.users",
    "my_apps.rest",
    "my_apps.notification",
    "my_apps.pdf",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "my_apps.middleware.AuditLogMiddleware",
    "csp.middleware.CSPMiddleware",
    "my_apps.middleware.SecurityHeadersMiddleware",
]

ROOT_URLCONF = "my_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "my_project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media files (files, images)
MEDIA_URL = "assets/"
MEDIA_ROOT = os.path.join(BASE_DIR, "assets")

# Custom
# auth
AUTH_USER_MODEL = "users.User"

# phone number field
PHONENUMBER_DEFAULT_REGION = "IN"

# all-auth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # 'allauth.account.auth_backends.AuthenticationBackend',
    "my_apps.backend.MyCustomAuthBackend",
]
LOGIN_URL = "/user/login/"
LOGIN_REDIRECT_URL = "/dashboard/data/"
ACCOUNT_FORMS = {
    "signup": "my_apps.users.forms.CustomSignupForm",
    "login": "my_apps.users.forms.CustomLoginForm",
    "reset_password": "my_apps.users.forms.CustomPasswordResetForm",
    "reset_password_from_key": "my_apps.users.forms.CustomPasswordResetKeyForm",
    "reauthenticate": "my_apps.users.forms.CustomReauthenticateForm",
}
MFA_FORMS = {
    "activate_totp": "my_apps.users.forms.CustomActivateTOTPForm",
    "authenticate": "my_apps.users.forms.CustomAuthenticateForm",
    "reauthenticate": "my_apps.users.forms.CustomAuthenticateForm",
}
SOCIALACCOUNT_ADAPTER = "my_apps.users.utils.CustomSocialAccountAdapter"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_EMAIL_NOTIFICATIONS = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": env("GOOGLE_OAUTH_CLIENT"),
            "secret": env("GOOGLE_OAUTH_SECRET"),
            "key": "",
        },
    }
}
MFA_ADAPTER = "allauth.mfa.adapter.DefaultMFAAdapter"

# email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")

# channels
ASGI_APPLICATION = "my_project.asgi.application"

# channels redis
CHANNEL_LAYERS = {
    "default": {
        # without broker - in memory
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # with redis broker
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     'hosts': [('localhost', 6379)],
        # },
    },
}

# django-q
Q_CLUSTER = {
    "name": "DjangoORM",
    "workers": 4,  # Number of simultaneous tasks
    "timeout": 90,
    "retry": 90,
    "queue_limit": 100,
    "bulk": 10,
    "orm": "default",
}

# logging - inbuilt
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            # use RotatingFileHandler or TimedRotatingFileHandler to get logs in multiple files.
            "class": "logging.FileHandler",
            "filename": "./logs/django.log",
            "formatter": "simple",
        },
    },
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# cache - inbuilt
CACHES = {
    "default": {
        # without redis - in memory
        # "BACKEND": "django.core.cache.backends.db.DatabaseCache", # db caching
        # 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 'TIMEOUT': 3600,  # 1 hour
        # 'OPTIONS': {
        #     'MAX_ENTRIES': 1000
        # },
        # with redis
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_LOCATION"),
    }
}

# csp
CSP_DEFAULT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "cdnjs.cloudflare.com",
    "ajax.googleapis.com",
    "cdn.jsdelivr.net",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
)

# celery
CELERY_BROKER_URL = env("REDIS_LOCATION")
CELERY_RESULT_BACKEND = "django-db"
