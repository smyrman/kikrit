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

# COMMANDS
def help(*args):
	print "Commands:\n"\
		"  help - show this text\n"\
		"  install - install database (according to settings) and load"\
		"initial data\n"\
		"  backup [multiline] - bacup all data from the database to a file.\n"\
		"  git-update [git-remote, git-branch] - Shorthand for 'backup', 'git"\
		"pull', 'rm kikrit_prod.db' and 'django_kikrit/manage.py load_data'."

def install(*args):
		# Create super-user, populate db with initial data:
		cmd = "django_kikrit/manage.py syncdb"
		os.system(cmd.replace("/", os.path.sep))

def backup(*args):
		# Create super-user, populate db with initial data:
		filename = "backup_%s.json" % datetime.datetime.now().isoformat()[:19]
		cmd = "django_kikrit/manage.py dumpdata --format json > %s" % filename
		os.system(cmd.replace("/", os.path.sep))
		print "Backed up db content to '%s'" % filename

		# Better formating of file:
		if "multiline" in args:
			f = open(filename)
			line = f.readline()
			f.close()
			lines = line.replace("}},","}},\n")
			f = open(filename, 'w')
			f.write(lines)
			f.close()
		return filename

def git_update(*args):
	filename = backup()
	os.system("git pull %s" % " ".join(args))
	os.system("mv kikrit_prod.db kikrit_prod.db.1")
	install()
	cmd = "django_kikrit/manage.py loaddata %s" % filename

	if os.system(cmd.replace("/", os.path.sep)) == 0:
		os.system("rm kikrit_prod.db.1")
		print "Migration complete"
	else:
		print "Migration failed! Original db available in 'kikrit_prod.db.1'"\
			" and backup file '%s'" % filename


def main():
	os.chdir(PROJECT_ROOT)
	if len(sys.argv) < 2:
		print "You must supply a command argument.. Try to add 'help'"
	elif sys.argv[1] == "help":
		help(*sys.argv[2:])
	elif sys.argv[1] == "install":
		install(*sys.argv[2:])
	elif sys.argv[1] == "backup":
		backup(*sys.argv[2:])
	elif sys.argv[1] == "git-update":
		git_update(*sys.argv[2:])
	else:
		print "Command argument not found little man.. Try to add 'help'"

if __name__ == "__main__":
	main()
