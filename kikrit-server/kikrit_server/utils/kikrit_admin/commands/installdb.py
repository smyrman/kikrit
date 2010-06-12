#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren
#
# This file is part of KiKrit which is distributed under GPLv3. See the file
# COPYING.txt for more details.

import os
import re
from optparse import make_option

from django.conf import settings
from django.core import management

from utils.kikrit_admin.base import NoArgsCommand


class Command(NoArgsCommand):
	option_list = NoArgsCommand.option_list + (
		make_option('--no-initial-data', action='store_false',
			dest='load_initial_data', default=True,
			help="dont load the default data into the database"),
		make_option('--noinput', action='store_false', dest='interactive',
			default=False, help="Don't ask the user for any input"),
		)

	help = "A wrapper to kikrit_server/manage.py's 'syncdb', 'autofake', "\
	       "'migrate' and 'loaddata' commands. It installs all database "\
	       "tables, and loads the database with initial data."

	args = None

	def handle_noargs(self, **options):
		verbosity = int(options.get('verbosity', '0'))

		# install default database:
		self.print_header(verbosity, "Create some db tables")
		management.call_command('syncdb', **options)
		self.print_header(verbosity, "Autofake first migration")
		management.call_command('autofake', **options)
		self.print_header(verbosity, "Migrate db tables")
		management.call_command('migrate', **options)

		# GUARD: load initial data?
		if not options.get('load_initial_data'):
			return

		self.print_header(verbosity, "Load default data")
		# Get fixture paths for all apps:
		apps = ('accounts', 'merchandise', 'utils')
		fixture_paths = (os.path.join(settings.PROJECT_ROOT, app, 'fixtures')
		                 for app in apps)

		# Get default fixtures:
		fixtures = []
		regex = re.compile(r'^default_\w+\.json$')
		for path in fixture_paths:
			if not os.path.isdir(path):
				continue
			files = os.listdir(path)
			fixtures.extend((os.path.join(path, f)
			                 for f in files if regex.match(f)))

		# Load data from default fixtures:
		management.call_command('loaddata', *fixtures, **options)
