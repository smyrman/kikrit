"""
This module includes the default settings for kikrit_server. Any user defined
settings should be configured in one of PROJECT_ROOT/server_settings.py,
~/config/kikrit/server_settings.py, or /etc/kikrit/server_settings.py. On
Loldos (a.k.a. Windows) this paths will be slightly different. I.e
'/etc/kikrit/' will be replaced by something like:
'C:\\Doncument and Settings\\All Users\\config\\kikrit\\'

Note that ALL settings in this file CAN be overriden in the user defined
settings file. Event those that shouldn't be (i.e. INSTALLED_APPS).

Also note that some user defined settings modifies the default settings:
  DEBUG ; affects TEMPLATE_DEBUG, SERVE_STATIC_MEDIA
  BASE_URL ; affects MEDIA_URL, ADMIN_MEDIA_PREFIX, UPLOAD_URL
  MEDIA_URL ; affects UPLOAD_URL
  STANDALONE ; affects SERVE_STATIC_MEDIA, CLIENT_AUTHENTICATION_LEVEL,
               UPLOAD_PATH
"""

import os
import sys
import re
from imp import load_source

from utils.paths import path4os


PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 2)[0]

## FIND (USER DEFINED) CONFIG FILE ##
# Search for server_settings.py and import module as cfg:
for path in (PROJECT_ROOT, '~user/config/kikrit', '/etc/kikrit'):
	file_name = path4os(path+'/server_settings.py')
	if os.path.exists(file_name):
		CONFIG_DIR = path4os(path)
		CONFIG_FILE = file_name
		# import CONFIG_FILE as cfg:
		cfg = load_source('cfg', CONFIG_FILE)
		break
del file_name

def cfg_get(attr, default=None):
	"""Small helper function to get user defined settings or defaults"""
	return getattr(cfg, attr, default)

## DEBUG ##
DEBUG = cfg_get('DEBUG', False)
TEMPLATE_DEBUG = DEBUG

## RUNNING IN LOCALHOST MODE ##
# If STANDALONE is True, that implies that the server and client are runing on
# the same machine. It also implies that the server wil run using Django's
# development server (./manage.py runserver), and that it will only be
# accesible to localhost.

STANDALONE = cfg_get('STANDALONE', False)
SERVE_STATIC_MEDIA = STANDALONE or DEBUG

# Clinet authentication levels:
# 0 - No authentication
# 1 - CLIENT_KEY needed
CLIENT_AUTHENTICATON_lEVEL = 1
if STANDALONE:
	CLIENT_AUTHENTICATON_LEVEL = 0

### LOCALE ##
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

USE_I18N = False


## URLS AND PATHS ##
SITE_ID = 1

# prefix all urls:
BASE_URL = cfg_get('BASE_URL', '/')

MEDIA_ROOT = path4os(PROJECT_ROOT+'/kikrit_server/media')
UPLOAD_PATH = cfg_get('UPLOAD_PATH', path4os(MEDIA_ROOT+'/upload'))

MEDIA_URL = cfg_get('MEDIA_URL', BASE_URL+'media/')
UPLOAD_URL = MEDIA_URL + '/upload/'
ADMIN_MEDIA_PREFIX = BASE_URL + 'media_admin/'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'kikrit_server.urls'

TEMPLATE_DIRS = (
	PROJECT_ROOT + '/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
	'kikrit_server.accounts',
	'kikrit_server.merchandise',
	'kikrit_server.utils',
	'kikrit_server.jquery_widgets',
	'south',
)

## OVERIDE DEFAULTS ##

# The following is eqivalent to something like 'from server_settings import *':
regex = re.compile(r'^__.*__$')
for attr in dir(cfg):
	# Skip attrs like __file__, __bultin__, etc:
	if regex.match(attr) or attr == 'regex':
		continue
	exec('%s = cfg.%s' % (attr, attr))
del regex, cfg, cfg_get
