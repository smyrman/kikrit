# -*- coding: utf-8 -*-
import os
from ConfigParser import ConfigParser

from PyQt4 import QtGui

from settings import PROJECT_ROOT, ICONS

CFG = ConfigParser()
ICONS = ICONS.replace('/', os.path.sep) # Make path Windows compatible
CFG.read(ICONS)

def getIcon(icon_name, size=16):
	# GUARD: Empty name:
	if icon_name == "":
		return QtGui.QIcon("")

	# Find section based on size:
	sections = [int(s) for s in CFG.sections() if s.isdigit() and int(s) >= size]
	if len(sections) != 0:
		section = unicode(min(sections))
	else:
		section = CFG.DEFAULT

	# Get icon path:
	try:
		icon = CFG.get(section, icon_name).replace('/', os.path.sep)
		path = os.path.join(os.path.abspath(os.path.dirname(ICONS)), icon)
	except CFG.NoOptionError:
		print "DEBUG: icon %s not found in %s" % (icon_name, ICONS)
		path = ""

	return QtGui.QIcon(path)



