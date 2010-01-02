#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file supplies an easy wrapper for django_kikrit/manage.py, and contains
# only a few essential commands.

import os
import sys
import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

if sys.argv[1] == "help":
	print "Commands:\n"\
		"help - show this text\n"\
		"install - install database according to settings and load initial",\
		"data\n"\
		"backup - bacup all data from a to file."

elif sys.argv[1] == "install":
	# Create super-user, populate db with initial data:
	cmd = "django_kikrit/manage.py syncdb"
	os.system(cmd.replace("/", os.path.sep))

elif sys.argv[1] == "backup":
	# Create super-user, populate db with initial data:
	filename = "backup_%s.json" % datetime.datetime.now().isoformat()[:19]
	cmd = "django_kikrit/manage.py dumpdata --format json > %s" % filename
	os.system(cmd.replace("/", os.path.sep))

else:
	print "Command argument not found little man.. Try to add 'help'"
