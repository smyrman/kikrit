#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren
#
# This file is part of KiKrit which is distributed under GPLv3. See the file
# COPYING.txt for more details.

import sys

from django.core.management import base

class NoArgsCommand(base.NoArgsCommand):
	# stdout, stderr explicitly set for Django 2.1 compatibility:
	stdout = sys.stdout
	stderr = sys.stderr

	def print_header(self, verbosity, text):
		# FIXME: use prety collors
		if verbosity:
			self.stdout.write("\n## %s ##\n" % text)


class BaseCommand(base.BaseCommand):
	# stdout, stderr explicitly set for Django 2.1 compatibility:
	stdout = sys.stdout
	stderr = sys.stderr

	def print_header(self, verbosity, text):
		# FIXME: use prety collors
		if verbosity:
			self.stdout.write("\n## %s ##\n" % text)
