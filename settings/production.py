# -*- coding: utf-8 -*-
# Django settings for django_kikrit project.
import os

PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 2)[0]

# DJANGO_KIKRIT SETTINGS:
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle':
DATABASE_ENGINE = 'sqlite3'
# Name or path to database file if using sqlite3:
DATABASE_NAME = os.path.join(PROJECT_ROOT, 'kikrit_prod.db')
# Not used with sqlite3:
DATABASE_USER = ''
# Not used with sqlite3:
DATABASE_PASSWORD = ''
# Set to empty string for localhost. Not used with sqlite3:
DATABASE_HOST = ''
# Set to empty string for default. Not used with sqlite3:
DATABASE_PORT = ''

SECRET_KEY = 'Enter an unique random string here @¥${[½¥£'

# QT_CLINET SETTINGS:
RFID_DEVICE = "/dev/ttyS0"
BALANCE_PAGE_TIME_SEC = 5
MESSAGE_TIME_SEC = 5

STYLE_SHEET = PROJECT_ROOT + "/qt_client/styles/base/style.qss"
ICONS = PROJECT_ROOT + "/qt_client/styles/base/icons.cfg"
