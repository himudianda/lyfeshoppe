# -*- coding: utf-8 -*-
from os import path
from datetime import timedelta


APP_NAME = 'cheermonk'
APP_ROOT = path.join(path.dirname(path.abspath(__file__)), '..')

SECRET_KEY = 'pickabettersecret'
DEBUG = True
TESTING = False

# Database settings,
# The username and password must match what's in docker-compose.yml for dev.
db_uri = 'postgresql://cheermonk:bestpassword@localhost:5432/{0}'
SQLALCHEMY_DATABASE_URI = db_uri.format(APP_NAME)
SQLALCHEMY_POOL_SIZE = 5

# Public build path. Files in this path will be accessible to the internet.
PUBLIC_BUILD_PATH = path.join(APP_ROOT, 'build', 'public')

# Flask-Webpack (assets) settings.
WEBPACK_MANIFEST_PATH = path.join(APP_ROOT, 'build', 'manifest.json')


# Login settings.
REMEMBER_COOKIE_DURATION = timedelta(days=90)
