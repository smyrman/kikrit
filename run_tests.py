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

def main():
	return os.system("django_kikrit/manage.py test merchandise accounts utils")

if __name__ == "__main__":
	exit(main())

