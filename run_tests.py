#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

"""
This file should always be run before commit!

"""

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def main():
	apps = "accounts merchandise utils"
	return os.system("%s/django_kikrit/manage.py test %s" % (PROJECT_ROOT, apps))

if __name__ == "__main__":
	exit(main())

