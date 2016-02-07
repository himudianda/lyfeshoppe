# -*- coding: utf-8 -*-

from os import path
from datetime import timedelta

from celery.schedules import crontab


# This value is used for the following properties,
# it really should be your module's name.
#   Database name
#   Cache redis prefix
APP_NAME = 'lyfeshoppe'
APP_ROOT = path.join(path.dirname(path.abspath(__file__)), '..')

# App settings, most settings you see here will change in production.
SECRET_KEY = 'pickabettersecret'
DEBUG = True
TESTING = False
LOG_LEVEL = 'DEBUG'

# You will need to disable this to get Stripe's webhooks to work because you'll
# likely end up using tunneling tooling such as ngrok so the endpoints are
# reachable outside of your private network.
#
# The problem with this is, Flask won't allow any connections to the ngrok
# url with the SERVER_NAME set to localhost:8000. However if you comment out
# the SERVER_NAME below then webbooks will work but now url_for will not work
# inside of email templates.
#
# A better solution will turn up in the future.
SERVER_NAME = 'localhost:8000'

# Public build path. Files in this path will be accessible to the internet.
PUBLIC_BUILD_PATH = path.join(APP_ROOT, 'build', 'public')

STATIC_FILES_PATH = path.join(APP_ROOT, 'lyfeshoppe', 'static')

# Flask-Webpack (assets) settings.
WEBPACK_MANIFEST_PATH = path.join(APP_ROOT, 'build', 'manifest.json')

# Babel i18n translations.
ACCEPT_LANGUAGES = ['en', 'es']
LANGUAGES = {
    'en': 'English',
    'es': u'Español'
}
BABEL_DEFAULT_LOCALE = 'en'

# Seed settings.
SEED_ADMIN_EMAIL = 'nerdo.harry@gmail.com'
SEED_ADMIN_FNAME = 'Harshit'
SEED_ADMIN_LNAME = 'Imudianda'

# Database settings,
# The username and password must match what's in docker-compose.yml for dev.
db_uri = 'postgresql://lyfeshoppe:bestpassword@localhost:5432/{0}'
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
CELERYBEAT_SCHEDULE = {}

# Login settings.
REMEMBER_COOKIE_DURATION = timedelta(days=90)

# Mail settings.
MAIL_DEFAULT_SENDER = 'lyfeshoppe@gmail.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# External end points.
ENDPOINT_CADVISOR = 'http://localhost:8080/containers/'

# Facebook settings.
#
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': None,
        'secret': None
    }
}
