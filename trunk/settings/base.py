# Django settings for django_kikrit project.
import os

PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 2)[0]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = False

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'django_kikrit', 'media')
MEDIA_URL = '/media'
ADMIN_MEDIA_PREFIX = '/media/'
UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'upload') # Here goes BalanceImages

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

ROOT_URLCONF = 'django_kikrit.urls'

TEMPLATE_DIRS = (
	PROJECT_ROOT + '/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
	'django_kikrit.accounts',
	'django_kikrit.merchandise',
	'django_kikrit.utils',
)
AUTH_PROFILE_MODULE = 'auth.Account'

RUNSERVER_PORT = '8081'
