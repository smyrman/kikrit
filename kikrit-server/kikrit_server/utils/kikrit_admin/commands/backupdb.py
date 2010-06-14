#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren
#
# This file is part of KiKrit which is distributed under GPLv3. See the file
# COPYING.txt for more details.

import os
from optparse import make_option
from datetime import datetime

from django.conf import settings
from django.core import management
from django.core.management.commands import dumpdata

from utils.kikrit_admin.base import NoArgsCommand



class Command(NoArgsCommand):
	option_list = dumpdata.Command.option_list

	help = "This comadn is a wrapper to the 'kikrit_server/manage.py dumdata'"\
	       "command. It creates a fixture file in the directory configured "\
	       "in BACKUP_DIR (default to <CONFIG_DIR>/backup)."

	args = None

	def handle_noargs(self, **options):
		verbosity = int(options.get('verbosity', '0'))

		filename = os.path.join(settings.BACKUP_DIR, "backup_%s.json" \
		                        % datetime.now().isoformat()[:19])

		self.print_header(verbosity, "Dumping data to fixture")
		options['stdout'] = open(filename, 'w+')
		management.call_command('dumpdata', **options)
		if verbosity:
			self.stdout.write("Backed up db content to:\n  '%s'\n" % filename)
