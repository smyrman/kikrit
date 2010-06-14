#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren
#
# This file is part of KiKrit which is distributed under GPLv3. See the file
# COPYING.txt for more details.

import os
from optparse import make_option
from random import choice
from datetime import datetime

from django.conf import settings
from django.core import management
from django.core.management import CommandError
from django.template.loader import render_to_string

from utils.paths import path4os
from utils.kikrit_admin.base import NoArgsCommand


class Command(NoArgsCommand):
	_ERROR_CREATE_FILE = "The file '%s' could not be created"
	_ERROR_CREATE_DIR = "The directory '%s' could not be created"
	_ERROR_PARAMS_VALIDATION = "PARAMS didn't validate to key-value pairs"

	option_list = NoArgsCommand.option_list + (
		make_option('--noinput', action='store_false', dest='interactive',
			default=True, help="Don't ask the user for any input"),
		make_option('--environ', action='store', type='choice',
			dest='environ', choices=['webserver', 'standalone-client', 'dev'],
			default='webserver',
			help="Specify which default settings to use when a parameter, or "\
			"CONFIGDIR, is not specified lagal choices are: "\
			"['webserver' (default), 'standalone-client', 'dev']"),
		make_option('--configdir', action='store', type='string',
			dest='configdir', default=None,
			help="Where to put the generated file"),
		make_option('--params', action='store', type='string', dest='params',
			default = None,
			help="Specify a comma seperated list of key-value pairs with the "\
			"syntax: BOOL1=True,STRING1='test',INT1=4. Note that this script "\
			"performs no sort of validation of your keys/values!"),
		make_option('--force', action='store_true', dest='force',
			help="If file exist, owerwrite it"),
		)

	help = "Create a file 'server_settings.py' in CONFIGDIR. If you are "\
	       "writing your own script on top of this one; legal keys for "\
	       "--params include:\n"\
	       "\tDEBUG (boolean)\n"\
	       "\tSTANDALONE_CLIENT (boolean)\n"\
	       "\tDATABASE_ENGINE (string)\n"\
	       "\tDATABASE_NAME (string)\n"\
	       "\tDATABASE_USER (string)\n"\
	       "\tDATABASE_PASSWORD (string)\n"\
	       "\tDATABASE_HOST (string)\n"\
	       "\tDATABASE_PORT (string)"
	args = None

	configdir_defaults = {
		'webserver': path4os(settings.PROJECT_ROOT+'/..'),
		'standalone-client': path4os(settings.PROJECT_ROOT+'/..'),
		'dev': path4os(settings.PROJECT_ROOT+'/..'),
	}

	params_defaults = {
		'default':{
			'DEBUG':'False',
			'STANDALONE_CLIENT':'False',
			'DATABASE_ENGINE':'""',
			'DATABASE_NAME':'""',
			'DATABASE_USER':'""',
			'DATABASE_PASSWORD':'""',
			'DATABASE_HOST':'""',
			'DATABASE_PORT':'""',
		},
		'webserver':{
			'DATABASE_ENGINE':'"postgresql_psycopg2"',
			'DATABASE_NAME':'"kikrit"',
		},
		'standalone-client':{
			'STANDALONE_CLIENT':'True',
			'DATABASE_ENGINE':'"sqlite3"',
			'DATABASE_NAME':'CONFIG_DIR + "%skikrit_prod.db"' % os.path.sep,
		},
		'dev':{
			'DEBUG':'True',
			'STANDALONE_CLIENT':'True',
			'DATABASE_ENGINE':'"sqlite3"',
			'DATABASE_NAME':'CONFIG_DIR + "%skikrit_dev.db"' % os.path.sep,
		},
	}

	def handle_noargs(self, **options):
		verbosity = int(options.get('verbosity'))
		interactive = options.get('interactive')
		force = options.get('force')
		env = options.get('environ')
		data = self.params_defaults['default']
		data.update(self.params_defaults[env])
		configdir = options.get('configdir') or self.configdir_defaults[env]
		configdir = os.path.abspath(configdir)
		filename = os.path.join(configdir, 'server_settings.py')
		params_str = options.get('params', None)

		# if params, updated data dict:
		if params_str:
			try:
				params = dict((p.split('=') for p in params_str.split(',')))
			except ValueError:
				raise CommandError(self._ERROR_PARAMS_VALIDATION)
			data.update(params)

		# If config dir does not exist, try to create it:
		if not os.path.isdir(configdir):
			try:
				# Note that the mask parameter (0775), is anded with the
				# operating system's umask, and that the leading '0' means that
				# the number is octal (so don't remove it). On Windows, the
				# mode is ignored
				os.makedirs(configdir, 0775)
			except OSError:
				raise CommandError(self._ERROR_CREATE_DIR % configdir)
			if verbosity:
				self.stdout.write("Created directory '%s'\n" % configdir)

		# GUARD: If the settings file exist, should it be overwritten?
		if os.path.exists(filename):
			self.stderr.write("file '%s' exists!\n" % filename)

			overwrite = force
			if interactive:
				input = raw_input("Do you want to overwrite it (yes/no)? ")
				overwrite = (input.lower() in ('y','yes')) # True or False

			if not overwrite:
				raise CommandError(self._ERROR_CREATE_FILE % filename)

		# Generate a random string for seed generation:
		data['SECRET_KEY'] = '"%s"' % ''.join([
				choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
				for i in range(50)])

		# include information about the generation:
		data['generator'] = "kikrit-admin"
		data['timestamp'] = datetime.now().isoformat()

		# Create the settings file:
		template = 'kikrit_admin/server_settings.py-dist'
		text = render_to_string(template, data)
		try:
			settings_file = open(filename,'w+')
			settings_file.write(text)
			settings_file.close()
			if verbosity:
				self.stdout.write("File '%s' was created\n" % filename)
		except OSError:
			raise CommandError(self._ERROR_CREATE_FILE % filename)
