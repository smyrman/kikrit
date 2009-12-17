#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import chdir, environ
from os.path import dirname, abspath, join as path_join
BASEPATH = abspath(dirname(__file__))
sys.path.append(BASEPATH)
environ['DJANGO_SETTINGS_MODULE'] = 'django_kikrit.settings'
from subprocess import Popen

from qt_client import client

def main():
	# FIXME Get port from settings file!
	webserver = Popen((path_join(BASEPATH,"django_kikrit/manage.py"),
		"runserver", "localhost:8081"))

	#FIXME: remove chdir hack
	chdir(path_join(BASEPATH, "qt_client"))

	client.main()

	# End of program
	print "WARNING: The web server is still running. You can kill it with "\
			"killall python"


if __name__ == "__main__":
	main()
