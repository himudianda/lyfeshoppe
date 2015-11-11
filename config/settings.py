# -*- coding: utf-8 -*-

APP_NAME = 'cheermonk'
DEBUG = True
TESTING = False

# Database settings,
# The username and password must match what's in docker-compose.yml for dev.
db_uri = 'postgresql://cheermonk:bestpassword@localhost:5432/{0}'
SQLALCHEMY_DATABASE_URI = db_uri.format(APP_NAME)
SQLALCHEMY_POOL_SIZE = 5

