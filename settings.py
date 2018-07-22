"""
Django settings for sandwhichi_api project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&mx%m)l0r)h+lm2en$1v7dp(!aic&2d82yjk!$h8_!o#p9bvp9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['local.sandwhichi.com']

# Application definition
AUTH_USER_MODEL = 'user.User'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',

    'account.apps.AccountConfig',
    'common.apps.CommonConfig',
    'user.apps.UserConfig',
    'project.apps.ProjectConfig',
    'location.apps.LocationConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'base.middlewares.APIResponseMiddleWare',
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ('local.sandwhichi.com:3000', )

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 20,
}

JWT_AUTH = {
    'JWT_ALGORITHM': 'HS256',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_PAYLOAD_HANDLER': 'base.handlers.jwt.jwt_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'base.handlers.jwt.jwt_response_payload_handler',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'base.handlers.jwt.jwt_get_username_from_payload_handler',
    'JWT_ALLOW_REFRESH': True,
    'JWT_VERIFY': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
PASSWORD_RESET_TIMEOUT_DAYS = 1

SWAGGER_SETTINGS = {
    'JSON_EDITOR': True,
}

AWS_S3_ACCESS_KEY_ID = 'AKIAJUPFBBGVTYQIVGHA'
AWS_S3_SECRET_ACCESS_KEY = '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'
RAW_IMAGE_BUCKET_BASE_URL = 'https://sandwhichi-dev-raw-image.s3.ap-northeast-2.amazonaws.com/'
RAW_IMAGE_BUCKET_NAME = 'sandwhichi-dev-raw-image'
RAW_IMAGE_BUCKET_REGION_NAME = 'ap-northeast-2'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAI3TWYMRG4V44NAUQ' # AWS_SES_ACCESS_KEY_ID
EMAIL_HOST_PASSWORD = 'Ah5dAsyg9+Db9x8g+oeLOMnSS22EcehHanImWJ/vKuSc' # AWS_SES_SECRET_ACCESS_KEY
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Sandwhichi <noreply@sandwhichi.com>'
EMAIL_SUBJECT_PREFIX = '[Sandwhichi]'

ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sandwhichi',
        'USER': 'root',
        'PASSWORD': 'secret',
        'HOST': 'local.sandwhichi.com',
        'PORT': '33061',
        'OPTIONS': {
            'sql_mode': 'TRADITIONAL',
            'charset': 'utf8mb4',
            'init_command': 'SET default_storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_general_ci',
            'compress': True
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# Social Access
NAVER_LOGIN_CLIENT_ID = 'HAjQ7lH1Jk8PqJUeHajh'
NAVER_LOGIN_SECRET = 'hI6ia8l3HQ'
GOOGLE_PLUS_CLIENT_ID = '910544055896-tiucajkqq3pt6l38v7kge5h6q20cs3ai.apps.googleusercontent.com'
GOOGLE_PLUS_SECRET= '-NB71lIhG2lj5spc4IZGZ5Mf'