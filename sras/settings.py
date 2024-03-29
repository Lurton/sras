"""
Django settings for sras project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

from sras import CONFIG

DOMAIN_NAME = "cput.ac.za"
HasHish = "anypassword"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIRECTORY = BASE_DIR / "media"
STATIC_DIRECTORY = BASE_DIR / "static"
STATICFILES_DIRS = [STATIC_DIRECTORY]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5t=wry28z9@@cs3%96h@v4=cejk0znnk1xfm(io)v&d53nw_&='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    "administration.apps.AdministrationConfig",
    "structure.apps.StructureConfig",
    "widget_tweaks",
    "django.contrib.humanize",
    "hijack",
    "hijack.contrib.admin"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "core.middleware.UserPersonPermissionMiddleware",
    "hijack.middleware.HijackUserMiddleware"
]

# ============================================================= [EMAIL SETTINGS]
# ============================================================= [EMAIL SETTINGS]
EMAIL_ENABLED = True
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_AWS_REGION = CONFIG.get("aws_region")
EMAIL_AWS_CHARSET = "UTF-8"
EMAIL_AWS_IAM_USER = CONFIG.get("setup").get("aws").get("ses").get("access_key_id")
EMAIL_AWS_SES_ARN = CONFIG.get("setup").get("aws").get("ses").get("identity")
EMAIL_HOST = CONFIG.get("setup").get("aws").get("ses").get("smtp_host")
EMAIL_HOST_USER = EMAIL_AWS_IAM_USER
EMAIL_HOST_PASSWORD = CONFIG.get("setup").get("aws").get("ses").get("access_key_secret")
SERVER_EMAIL = "The Student Residence <administrator@takealotgroup.team>"
DEFAULT_FROM_EMAIL = "The Student Residence <administrator@takealotgroup.team>"



# EMAIL_ENABLED = True
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_AWS_REGION = CONFIG.get("aws_region")
# EMAIL_AWS_CHARSET = "UTF-8"
# EMAIL_AWS_IAM_USER = CONFIG.get("setup").get("aws").get("ses").get("access_key_id")
# EMAIL_AWS_SES_ARN = CONFIG.get("setup").get("aws").get("ses").get("identity")
# EMAIL_HOST = CONFIG.get("setup").get("aws").get("ses").get("smtp_host")
# EMAIL_HOST_USER = "argusshinze@outlook.com"
# EMAIL_HOST_PASSWORD = HasHish
# SERVER_EMAIL = f"CPUT Residence <no-reply@{DOMAIN_NAME}>"
# DEFAULT_FROM_EMAIL = f"CPUT Residence <no-reply@{DOMAIN_NAME}>"

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# ============================================================= [OTHER SETTINGS]
SITE_ID = 1
SITE_TITLE = "Student Residence Administration System"
SITE_VERSION = "1.0"
SITE_DESCRIPTION = "The Student Residence Administration System"
SITE_AUTHOR = "Argus Ndabashinze"

# Authentication URL defaults.
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend"
]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
    }
]

# Pagination - Defaults.
PAGE_SIZE = 33

ROOT_URLCONF = 'sras.urls'

# Authentication URL defaults.
LOGIN_REDIRECT_URL = "/dashboard/"
LOGIN_URL = "/login/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.template_variables'
            ],
        },
    },
]

WSGI_APPLICATION = 'sras.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sras',
        'USER': 'sras',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
