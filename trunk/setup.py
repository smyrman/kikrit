#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.
#
#    KiKrit is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    KiKrit is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with KiKrit.  If not, see <http://www.gnu.org/licenses/>.


"""This file supplies an easy wrapper for django_kikrit/manage.py, and contains
only a few essential commands.

"""
import os
import sys
import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

if len(sys.argv) < 2:
	print "You must supply a command argument.. Try to add 'help'"

elif sys.argv[1] == "help":
	print "Commands:\n"\
		"help - show this text\n"\
		"install - install database (according to settings) and load initial",\
		"data\n"\
		"backup - bacup all data from the database to a file."

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
