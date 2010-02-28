#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

"""This file should always be run before commit!

"""

import os

PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 2)[0]

def main():
	# Run Django database tests for our apps:
	os.chdir(PROJECT_ROOT)
	apps = "accounts merchandise utils"
	return os.system("django_kikrit/manage.py test -v 0 %s" % apps)


if __name__ == "__main__":
	exit(main())
