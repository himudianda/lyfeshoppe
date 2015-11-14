# -*- coding: utf-8 -*-

from os import path
from datetime import timedelta


# This value is used for the following properties,
# it really should be your module's name.
#   Database name
#   Cache redis prefix
APP_NAME = 'cheermonk'
APP_ROOT = path.join(path.dirname(path.abspath(__file__)), '..')

# App settings, most settings you see here will change in production.
SECRET_KEY = 'pickabettersecret'
DEBUG = True
TESTING = False

SERVER_NAME = 'localhost:5000'

# Public build path. Files in this path will be accessible to the internet.
PUBLIC_BUILD_PATH = path.join(APP_ROOT, 'build', 'public')

# Flask-Webpack (assets) settings.
WEBPACK_MANIFEST_PATH = path.join(APP_ROOT, 'build', 'manifest.json')

# Seed settings.
SEED_ADMIN_EMAIL = 'dev@localhost.com'

# Database settings,
# The username and password must match what's in docker-compose.yml for dev.
db_uri = 'postgresql://cheermonk:bestpassword@localhost:5432/{0}'
SQLALCHEMY_DATABASE_URI = db_uri.format(APP_NAME)
SQLALCHEMY_POOL_SIZE = 5

# Cache settings.
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = 'redis://localhost:6379/0'
CACHE_KEY_PREFIX = APP_NAME

# Celery settings.
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_REDIS_MAX_CONNECTIONS = 5
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Celery recurring scheduled tasks.
CELERYBEAT_SCHEDULE = {
}

# Login settings.
REMEMBER_COOKIE_DURATION = timedelta(days=90)

# Mail settings.
MAIL_DEFAULT_SENDER = 'support@cheermonk.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'you@gmail.com'
MAIL_PASSWORD = 'awesomepassword'

# External end points.
ENDPOINT_CADVISOR = 'http://localhost:8080/containers/'
ENDPOINT_FLOWER = 'http://localhost:8081'
