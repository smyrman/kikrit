#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre
#
# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.
#
#    KiKrit is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    KiKrit is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with KiKrit.  If not, see <http://www.gnu.org/licenses/>.

"""This is a shortcut for starting the webserver and the client in one
click/command. It requires that screen and bash is installed, and is therefore
not Windows compatible.

"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from settings import RUNSERVER_PORT
from qt_client import client

def main():
	os.chdir(PROJECT_ROOT)
	# If webserver is not running, start webserver in a new 'screen':
	SCREEN_NAME = "kikrit_webserver"

	if os.system("screen -ls | grep %s" % SCREEN_NAME) != 0:
		os.system("screen -d -m -S %s django_kikrit/manage.py runserver "\
				"localhost:%s" % (SCREEN_NAME, RUNSERVER_PORT))

	# Start client:
	client.main()

	# Reatatch webserver screen:
	os.system("screen -r %s" % SCREEN_NAME)


if __name__ == "__main__":
	main()
