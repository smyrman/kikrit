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
import time
from subprocess import Popen, PIPE

PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 1)[0]
sys.path.append(PROJECT_ROOT)

from settings import RUNSERVER_PORT
from qt_client import client

def main():
	os.chdir(PROJECT_ROOT)

	try:
		# Start django web-server in the background
		args = ("django_kikrit/manage.py", "runserver", "--noreload",
				"localhost:%s" % RUNSERVER_PORT)
		p1 = Popen(args, stdout=PIPE, stderr=PIPE)

		# Start the qt_client
		args = ["qt_client/client.py",] + sys.argv[1:]
		#p2 = Popen(args, stdout=PIPE, stderr=PIPE)
		p2 = Popen(args)
		p2.communicate()
	except:
		p1.kill()
		p2.kill()
		import traceback
		traceback.print_exc()
		exit(1)

	p1.kill()


if __name__ == "__main__":
	main()
