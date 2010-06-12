#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren
#
# This file is part of KiKrit which is distributed under GPLv3. See the file
# COPYING.txt for more details.

import sys
from optparse import NO_DEFAULT

from django.core.management import setup_environ

from utils.command_utility import CommandUtility


def call_command(subcommand, *args, **options):
	"""Calls the given command, with the given options and args/kwargs.

	This is the primary API you should use for calling specific commands.

	Some examples:
	    call_command('installdb')
	    call_command('installdb', load_initial_data=False)

	"""
	utility = CommandUtility('utils.kikrit_admin', sys.argv)

	if not subcommand in utility.get_commands().keys():
		sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n"\
		                 % (subcommand, self.prog_name))
		sys.exit(1)

	command = utility.fetch_command(subcommand)
	defaults = dict([(o.dest, o.default)
	                 for o in command.option_list
	                 if o.default is not NO_DEFAULT])
	defaults.update(options)
	command.execute(*args, **defaults)


def execute_kikrit_admin(settings_mod, argv=None):
	setup_environ(settings_mod)
	utility = CommandUtility('utils.kikrit_admin', sys.argv)
	utility.execute()
