#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

import sys
import os

from django.core.management import execute_manager

try:
	import settings # Assumed to be in the same directory.
	if settings.PROJECT_ROOT not in sys.path:
		sys.path.append(settings.PROJECT_ROOT)

except ImportError:
	sys.stderr.write("Error: Can't find the file 'settings.py' in the "
			"directory containing %r. It appears you've customized "
			"things.\nYou'll have to run django-admin.py, passing it your "
			"settings module.\n(If the file settings.py does indeed exist, "
			"it's causing an ImportError somehow.)\n" % __file__)
	sys.exit(1)


if __name__ == "__main__":
	execute_manager(settings)
