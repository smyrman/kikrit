#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren
#
# This file is part of KiKrit which is distributed under GPLv3. See the file
# COPYING.txt for more details.

import os
import sys
from imp import find_module

from django.core.management import ManagementUtility, find_commands
from django.utils.importlib import import_module


class CommandUtility(ManagementUtility):
	"""A customized version of django's management utility that fetches
	commands from a custom folder structure. This class will get commands from
	the "<module_path>/commands", where module_path is derived from the
	module_name parameter given to the __init__ function.

	"""

	def __init__(self, module_name, *args, **kw):
		self.module_name = module_name
		super(CommandUtility, self).__init__(*args, **kw)

	def get_commands(self):
		module = import_module(self.module_name)
		path = module.__file__.rsplit(os.path.sep, 1)[0]
		return dict([(name, self.module_name) for name in find_commands(path)])

	def fetch_command(self, subcommand):
		if not subcommand in self.get_commands().keys():
			sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n"\
			                 % (subcommand, self.prog_name))
			sys.exit(1)

		module = import_module('%s.commands.%s' % (self.module_name, subcommand))
		return module.Command()

	def main_help_text(self):
		usage = ['', "Type '%s help <subcommand>' for help on a specific "\
		         "subcommand." % self.prog_name,'']
		usage.append('Available subcommands:')
		commands = self.get_commands().keys()
		commands.sort()
		for cmd in commands:
			usage.append('	%s' % cmd)
		return '\n'.join(usage)

	def execute(self):
		if '--version' in self.argv:
			from  kikrit_server import get_version
			from  django import get_version as get_django_version
			print "KiKrit Server v%s (on Django v%s)" %\
			      (get_version(), get_django_version())
		else:
			super(CommandUtility, self).execute()
