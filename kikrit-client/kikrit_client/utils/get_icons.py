# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

import os
from ConfigParser import ConfigParser, NoOptionError

from PyQt4 import QtGui

from utils.paths import path4os
import settings

CFG = ConfigParser()

def getIcon(icon_name, size=16):
	# GUARD: Empty name:
	if icon_name == "":
		return QtGui.QIcon("")

	# Find section based on size:
	sections = [int(s) for s in CFG.sections() if s.isdigit() and int(s) >= size]
	sections.sort()
	if CFG.has_section("svg"):
		section = "svg"
	elif len(sections) != 0:
		section = unicode(sections[0])
	else:
		section = "DEFAULT"
	# Get icon path:
	try:
		icon = CFG.get(section, icon_name).replace('/', os.path.sep)
		path = os.path.join(os.path.abspath(os.path.dirname(settings.ICONS)), icon)
	except NoOptionError:
		print "DEBUG: option '%s' not found in '%s'" % (icon_name, settings.ICONS)
		print "DEBUG: using section '%s'" % section
		path = ""

	return QtGui.QIcon(path)
