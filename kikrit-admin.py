#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.
#
#	 KiKrit is free software: you can redistribute it and/or modify
#	 it under the terms of the GNU General Public License as published by
#	 the Free Software Foundation, either version 3 of the License, or
#	 (at your option) any later version.
#
#	 KiKrit is distributed in the hope that it will be useful,
#	 but WITHOUT ANY WARRANTY; without even the implied warranty of
#	 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	 GNU General Public License for more details.
#
#	 You should have received a copy of the GNU General Public License
#	 along with KiKrit.  If not, see <http://www.gnu.org/licenses/>.


"""kikrit-admin.py supplies an easy wrapper for some django_kikrit/manage.py
commands (and more). It is meant to be an easy to use commnad line tool that
makes the most common administrative tasks easy.

Available command argumets are:
    help      Show this text, or print help about a specifc command
    install   Install database (according to settings) and load initial data
    backup    Backup your database to a 'json fixture' in your bacup directory
    migrate   Migrate an outdated database to match the current KiKrit version

"""

import os
import sys
import datetime
from inspect import cleandoc

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core import management
from django.conf import settings


# A mapping that mapps user input commands to python functions.
COMMANDS =	{"help":"help", "install":"install", "backup":"backup",
		"migrate":"migrate"}

# Helper functions:
def eprint(str):
	print "%s: error: %s" % (sys.argv[0], str)


# Commands:

def help(*args):
	"""Crying for help is nice, but I don't think this is the way you would
	rather use this command. Try 'help install' or whatever, but screaming for
	help like this brings you nowhere.

	"""
	if len(args) > 0:
		if args[0] in COMMANDS:
			print cleandoc(eval(COMMANDS[args[0]]).__doc__)
		elif args[0].lower() in ('sex', 'girls'):
			print "You shuld try asking her out some time..."
		elif args[0].lower() in ('boys', 'lads', 'men'):
			print "Men, or 'male humans' are often thought of as much "\
				"simpler then their female counterparts. Many women see men "\
				"as giant, strong and half-brained ogers. Still, there is "\
				"just something about those creatures that women tend to "\
				"'fall for'."
		elif args[0].lower() in ('robots',):
			print "Robots are very sexy indeed. Their reproduction is "\
				"however often controlled by the much more simple-minded "\
				"humans."
		else:
			print "I realy can't help you with '%s'." % " ".join(args)
	else:
		print cleandoc(__doc__)


def install(*args):
	"""First calls:
	  '$ django_kikrit/manage.py syncdb [--noinput]'.

	This will install all database tables for all 'django apps' that do not use
	'south migrations' (You might google 'django' and 'django south' to find out
	more).

	Then calls:
	  '$ django_kikrit/manage.py safe_migrateion --autoskip-first [--noinput] [--no-initial-data]'

	This will install or upgrade all apps that use 'south migrations'.

	Finally, if not '--no-initial-data' is supplied, run:
	  '$ django_kikrit/manage.py loaddata django_kikrit/accounts/fixtures/default_*'
	This will load all default fixtures for the accounts app into the database.
	The 'merchandise' and 'utils' app currently does not have any initial data.

	Supported options:
	  --noinput          Do not ask the user for input.
	  --no-initial-data  Do not load initial data from fixtures.


	"""
	# deafaults:
	interactive = True
	no_initial_data = False

	# A (very) simplistic way to get options:
	if len(args) > 0:
		if '--noinput' in args:
			interactive = False
		if '--no-initial-data' in args:
			no_initial_data = True
	elif len(args) > 2:
		eprint("Unhandled arguments or options!")
		exit(1)

	management.call_command('syncdb', interactive=interactive,)
	management.call_command('safe_migration', interactive=interactive,
			autoskip=True, no_initial_data=no_initial_data)
	# If not


def backup(*args):
	"""Performs a 'manage.py dumpdata' operation, and pipline the output to
	a file in your bacup directory (configured in settings/production.py
	BACUP_DIR = ...). When this is done, the file is formated to have newlines
	between each entry.

	"""

	# Preform manage.py dumpdata
	filename = "backup_%s.json" % datetime.datetime.now().isoformat()[:19]
	filename = os.path.join(BACKUP_DIR, filename)
	cmd = "django_kikrit/manage.py dumpdata --format json > %s" % filename
	ret = os.system(cmd.replace("/", os.path.sep))
	if ret != 0:
		eprint("Backup failed!")
		exit(1)
	print "Backed up db content to '%s'" % filename

	# Better formating of file:
	f = open(filename)
	line = f.readline()
	f.close()
	lines = line.replace("}},","}},\n")
	f = open(filename, 'w')
	f.write(lines)
	f.close()

	return filename


def migrate(*args):
	"""This command preforms the exact same operations as the 'install'
	command, except that it does not load any initial data.

	Supported options:
	  --noinput  Do NOT ask the user for input.

	"""
	if not '--no-initial-data' in args:
		args += ('--no-initial-data',)
	install(*args)


def main():
	os.chdir(PROJECT_ROOT)
	if len(sys.argv) < 2:
		eprint("You must supply a command argument.. Try to add 'help'")
		exit(1)
	elif sys.argv[1] in COMMANDS:
		# Call the command with argumets:
		eval(COMMANDS[sys.argv[1]])(*sys.argv[2:])
		exit(0)
	else:
		eprint("The command argument '%s' was not found. Try to add 'help'" %\
				sys.argv[1])
		exit(1)


if __name__ == "__main__":
	main()
