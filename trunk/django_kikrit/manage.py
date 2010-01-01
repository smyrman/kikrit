#!/usr/bin/env python
import sys
import os

PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 2)[0]
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core.management import execute_manager


try:
	import settings # Assumed to be in the same directory.
except ImportError:
	sys.stderr.write("Error: Can't find the file 'settings.py' in the "
			"directory containing %r. It appears you've customized "
			"things.\nYou'll have to run django-admin.py, passing it your "
			"settings module.\n(If the file settings.py does indeed exist, "
			"it's causing an ImportError somehow.)\n" % __file__)
	sys.exit(1)


if __name__ == "__main__":
	execute_manager(settings)

