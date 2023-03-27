"""
Django settings for tickets project.

Generated by 'django-admin startproject' using Django 1.8.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import environ
from datetime import timedelta

# Import environment variables
env = environ.Env(DEBUG=(bool, False))
# reading .env file
environ.Env.read_env(env.str('ENV_PATH', '.env'))

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = "/webserver"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

LOGIN_REDIRECT_URL = '/'

# AUTH_USER_MODEL = 'users.CustomUser'

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# Application definition

INSTALLED_APPS = (
    # Django Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.core.management',
    'django_celery_beat',
    'rest_framework',
    'corsheaders',
    "jwtauth",

    # Nictiz apps
    'atc_lookup',
    'app',
    'build_tree',
    'build_tree_excel',
    'snomed_list_generator',
    'homepage',
    'django_select2',
    'mapping',
    'epd',
    'termspace',
    'dhd',
    'postcoordination',
    'validation',
)

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated",],
    "DEFAULT_PARSER_CLASSES":["rest_framework.parsers.JSONParser",],
    "DEFAULT_AUTHENTICATION_CLASSES":
        [
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ],
    }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[
    "http://localhost:9123",
    "http://127.0.0.1:9123",
    "http://62.138.184.153:9123",
    "https://flower.test-nictiz.nl",
])
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", default=False)
CORS_SUPPORTS_CREDENTIALS = True
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE=None
CSRF_COOKIE_DOMAIN = env.str("CSRF_COOKIE_DOMAIN", default=".test-nictiz.nl")
SESSION_COOKIE_DOMAIN = env.str("SESSION_COOKIE_DOMAIN", default=".test-nictiz.nl")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['.test-nictiz.nl'])

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': env('POSTGRES_DB'),
       'USER': env('POSTGRES_USER'),
       'PASSWORD': env('POSTGRES_PASS'),
       'HOST': env('POSTGRES_HOST', default='postgres'),
       'PORT': env('POSTGRES_PORT', default='5432'),
   }
}

CELERY_BROKER_URL = "amqp://guest:guest@rabbitmq:5672"


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')


## Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

MAPPING_TOOL_URL = env.str("MAPPING_TOOL_URL", default='https://termservice.test-nictiz.nl/node/')
SNOWSTORM_URL = env.str("SNOWSTORM_URL", default="https://snowstorm.test-nictiz.nl")

TERMINOLOGIE_URL = env.str("TERMINOLOGIE_URL", "https://terminologieserver.nl")
TERMINOLOGIE_USERNAME = env.str("TERMINOLOGIE_USERNAME", "")
TERMINOLOGIE_PASSWORD = env.str("TERMINOLOGIE_PASSWORD", "")

MAPPING_API_SECRET = str(env("mapping_api_secret"))

# TODO: replace with TERMINOLOGIE_*
NTS_CLIENT_ID = env("nts_client")
NTS_APIKEY = env("nts_apikey")


PROJECTS_SORTED_ALPHABETICALLY = [3, 13]
