# Django settings for django_kikrit project.
from os.path import dirname, abspath, join as join_path

PROJECT_ROOT = join_path(dirname(abspath(__file__)), "..", "..")

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_ENGINE = 'sqlite3'
# Or path to database file if using sqlite3.
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

