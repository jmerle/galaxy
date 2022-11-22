"""
Django settings for siarnaq project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import json
import os
from datetime import timedelta
from pathlib import Path

import google.auth
import google.cloud.secretmanager as secretmanager
from configurations import Configuration
from google.auth import impersonated_credentials
from google.auth.credentials import Credentials


def _get_secret(
    credentials: Credentials, project_id: str, name: str, version: str = "latest"
) -> bytes:
    """Access the secret version from the Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    request = secretmanager.AccessSecretVersionRequest(
        name=client.secret_version_path(project_id, name, version)
    )
    return client.access_secret_version(request=request).payload.data


class Base(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Application definition

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "corsheaders",
        "rest_framework",
        "rest_framework_simplejwt",
        "siarnaq.api.user",
        "siarnaq.api.compete",
        "siarnaq.api.episodes",
        "siarnaq.api.teams",
        "drf_spectacular",
        "django_rest_passwordreset",
        "anymail",
    ]

    MIDDLEWARE = [
        # Place CORS first. See https://stackoverflow.com/a/45376281
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True

    ROOT_URLCONF = "siarnaq.urls"

    SITE_ID = 1

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "siarnaq/templates")],
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

    WSGI_APPLICATION = "siarnaq.wsgi.application"

    # Custom user model
    # https://docs.djangoproject.com/en/4.0/topics/auth/customizing

    AUTH_USER_MODEL = "user.User"

    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
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

    # Authentication with simple JWT
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "siarnaq.api.user.authentication.GoogleCloudAuthentication",
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 10,
    }

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    }

    # Internationalization
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = "static/"

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Penalized Elo configuration

    TEAMS_ELO_INITIAL = 1500.0
    TEAMS_ELO_K = 24.0
    TEAMS_ELO_SCALE = 400.0
    TEAMS_ELO_PENALTY = 0.85

    # Team limits

    TEAMS_MAX_TEAM_SIZE = 4

    # User avatar settings

    USER_MAX_AVATAR_SIZE = (512, 512)

    # Email config

    EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
    EMAIL_HOST_USER = "no-reply@battlecode.org"


class Local(Base):
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
    ]

    GALAXY_ADMIN_EMAILS = ["admin@example.com"]
    GALAXY_ADMIN_USERNAME = "galaxy-admin"

    GCLOUD_SERVICE_EMAIL = GALAXY_ADMIN_EMAILS[0]
    GCLOUD_LOCATION = "nowhere"
    GCLOUD_ENABLE_ACTIONS = False

    GCLOUD_BUCKET_PUBLIC = "nowhere-public"
    GCLOUD_BUCKET_SECURE = "nowhere-secure"
    GCLOUD_TOPIC_COMPILE = "nowhere-siarnaq-compile"
    GCLOUD_TOPIC_EXECUTE = "nowhere-siarnaq-execute"
    GCLOUD_ORDER_COMPILE = "compile-order"
    GCLOUD_ORDER_EXECUTE = "execute-order"

    DEBUG = True
    EMAIL_ENABLED = False

    GCLOUD_CREDENTIALS, GCLOUD_PROJECT = None, "null-project"
    SECRET_KEY = "django-insecure-2r0p5r8#j1!4v%cb@w#_^)6+^#vs5b*9mqf)!q)pz!5tqnbx*("
    ANYMAIL = {
        "MAILJET_API_KEY": "",
        "MAILJET_SECRET_KEY": "",
    }

    @property
    def DATABASES(self):
        return {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": str(self.BASE_DIR / "db.sqlite3"),
            }
        }


class Staging(Base):
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
    ]

    GALAXY_ADMIN_EMAILS = [
        "staging-siarnaq-agent@mitbattlecode.iam.gserviceaccount.com",
        "saturn-staging-compile@mitbattlecode.iam.gserviceaccount.com",
        "saturn-staging-execute@mitbattlecode.iam.gserviceaccount.com",
    ]
    GALAXY_ADMIN_USERNAME = "galaxy-admin"

    GCLOUD_SERVICE_EMAIL = GALAXY_ADMIN_EMAILS[0]
    GCLOUD_LOCATION = "us-east1"
    GCLOUD_ENABLE_ACTIONS = True

    GCLOUD_BUCKET_PUBLIC = "mitbattlecode-staging-public"
    GCLOUD_BUCKET_SECURE = "mitbattlecode-staging-secure"
    GCLOUD_TOPIC_COMPILE = "staging-siarnaq-compile"
    GCLOUD_TOPIC_EXECUTE = "staging-siarnaq-execute"
    GCLOUD_ORDER_COMPILE = "compile-order"
    GCLOUD_ORDER_EXECUTE = "execute-order"

    DEBUG = True
    EMAIL_ENABLED = False

    @classmethod
    def pre_setup(cls):
        super().pre_setup()
        user_credentials, cls.GCLOUD_PROJECT = google.auth.default()
        cls.GCLOUD_CREDENTIALS = impersonated_credentials.Credentials(
            source_credentials=user_credentials,
            target_principal=cls.GCLOUD_SERVICE_EMAIL,
            target_scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/userinfo.email",
            ],
        )
        secrets = json.loads(
            _get_secret(
                cls.GCLOUD_CREDENTIALS, cls.GCLOUD_PROJECT, "staging-siarnaq"
            ).decode()
        )
        cls.SECRET_KEY = secrets["django-key"]
        cls.ANYMAIL = {
            "MAILJET_API_KEY": secrets["mailjet-api-key"],
            "MAILJET_SECRET_KEY": secrets["mailjet-api-secret"],
        }
        cls.DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "NAME": "battlecode",
                "USER": "siarnaq",
                "PASSWORD": secrets["db-password"],
                "HOST": "db.staging.battlecode.org",
                "PORT": 5432,
            }
        }


class Production(Base):
    ALLOWED_HOSTS = [
        "play.battlecode.org",
    ]

    GALAXY_ADMIN_EMAILS = [
        "production-siarnaq-agent@mitbattlecode.iam.gserviceaccount.com",
        "saturn-production-compile@mitbattlecode.iam.gserviceaccount.com",
        "saturn-production-execute@mitbattlecode.iam.gserviceaccount.com",
    ]
    GALAXY_ADMIN_USERNAME = "galaxy-admin"

    GCLOUD_SERVICE_EMAIL = GALAXY_ADMIN_EMAILS[0]
    GCLOUD_LOCATION = "us-east1"
    GCLOUD_ENABLE_ACTIONS = True

    GCLOUD_BUCKET_PUBLIC = "mitbattlecode-production-public"
    GCLOUD_BUCKET_SECURE = "mitbattlecode-production-secure"
    GCLOUD_TOPIC_COMPILE = "production-siarnaq-compile"
    GCLOUD_TOPIC_EXECUTE = "production-siarnaq-execute"
    GCLOUD_ORDER_COMPILE = "compile-order"
    GCLOUD_ORDER_EXECUTE = "execute-order"

    DEBUG = False
    EMAIL_ENABLED = True

    @classmethod
    def pre_setup(cls):
        super().pre_setup()
        cls.GCLOUD_CREDENTIALS, cls.GCLOUD_PROJECT = google.auth.default()
        secrets = json.loads(
            _get_secret(
                cls.GCLOUD_CREDENTIALS, cls.GCLOUD_PROJECT, "production-siarnaq"
            ).decode()
        )
        cls.SECRET_KEY = secrets["django-key"]
        cls.DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "NAME": "battlecode",
                "USER": "siarnaq",
                "PASSWORD": secrets["db-password"],
                "HOST": (
                    f"/cloudsql/{cls.GCLOUD_PROJECT}:"
                    f"{cls.GCLOUD_LOCATION}:production-siarnaq-db"
                ),
            }
        }
        cls.ANYMAIL = {
            "MAILJET_API_KEY": secrets["mailjet-api-key"],
            "MAILJET_SECRET_KEY": secrets["mailjet-api-secret"],
        }
