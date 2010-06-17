#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren
#
# This file is part of KiKrit which is distributed under GPLv3. See the file
# COPYING.txt for more details.

from optparse import make_option

from utils import kikrit_admin
from utils.kikrit_admin.base import NoArgsCommand


class Command(NoArgsCommand):
	option_list = NoArgsCommand.option_list + (
		make_option('--load-initial-data', action='store_true',
			dest='load_initial_data', default=False,
			help="Load default data into the database."),
		make_option('--noinput', action='store_false', dest='interactive',
			default=True, help="Don't ask the user for any input"),
		)

	help = "Preforms exacly the same steps as the 'installdb' commnand; "\
	       "except that it does not load initial data by default."

	def handle_noargs(self, **options):
		kikrit_admin.call_command('installdb', **options)
