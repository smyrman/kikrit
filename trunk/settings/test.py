# Django settings for django_kikrit project.
import os
PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")

# DJANGO_KIKRIT SETTINGS:
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS


# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_ENGINE = 'sqlite3'
# Name or path to database file if using sqlite3.
DATABASE_NAME = PROJECT_ROOT+'/kikrittest.db'
# Not used with sqlite3.
DATABASE_USER = ''
# Not used with sqlite3.
DATABASE_PASSWORD = ''
# Set to empty string for localhost. Not used with sqlite3.
DATABASE_HOST = ''
# Set to empty string for default. Not used with sqlite3.
DATABASE_PORT = ''

SECRET_KEY = 's#(&@jcdlqc*#m&^yx16-u2i++_!-3+g@_f=!jdu3nq)#y#!%@'

# QT_CLINET SETTINGS:
RFID_DEVICE = None
BALANCE_PAGE_TIME_SEC = 5
MESSAGE_TIME_SEC = 5

STYLE_SHEET = PROJECT_ROOT + "/qt_client/styles/base/style.qss"
ICONS = PROJECT_ROOT + "/qt_client/styles/base/icons.cfg"
