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
    help    Show this text, or print help about a specifc command
    install Install database (according to settings) and load initial data
    backup  Backup your database to a 'json fixture' in your bacup directory
    migrate Doens nothing (Will be implemented when needed)

Deprecated commands that still work are:
    backup multiline  Issuing only 'backup' now does what this did (file
                      formating)
    git-update        Shorthand for 'backup', 'git pull', 'rm kikrit_prod.db'
                      and 'django_kikrit/manage.py load_data'.

"""
import os
import sys
import datetime
from inspect import cleandoc

from settings import BACKUP_DIR

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

COMMANDS =	{"help":"help", "install":"install", "backup":"backup",
		"migrate":"migrate", "git-update":"git_update"}


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
		else:
			print "I realy can't help you with '%s'." % " ".join(args)
	else:
		print cleandoc(__doc__)


def install(*args):
	"""Currently just calls 'django_kikrit/manage.py syncdb'. This will create
	the database tables that need to be created, and load the database with
	the initial data that is found in 'initia_data.json'.

	"""
	# Create super-user, populate db with initial data:
	cmd = "django_kikrit/manage.py syncdb %s" % " ".join(args)
	ret = os.system(cmd.replace("/", os.path.sep))
	if ret != 0:
		eprint("Syncdb failed!")
		exit(1)


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


def git_update(*args):
	"""Takes all the parameters that 'git pull' does.
	WARNING: This command is deprecated and will soon be removed!
	"""
	filename = backup()
	os.system("git pull %s" % " ".join(args))
	os.system("mv kikrit_prod.db kikrit_prod.db.1")
	install()

	cmd = "django_kikrit/manage.py loaddata %s" % filename
	ret = os.system(cmd.replace("/", os.path.sep))

	if ret == 0:
		os.system("rm kikrit_prod.db.1")
		print "Migration complete"
	else:
		print "Migration failed! Original db available in 'kikrit_prod.db.1'"\
		      " and backup file '%s'" % filename
		exit(1)


def migrate(*args):
	"""This function does nothing at the moment. When migrations become needed,
	it will make sure the database structure is up to data, (e.g. that the
	database revision is at the right number).

	"""
	pass


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
