#!/usr/bin/env python
# -*- coding: utf-8 -*-

version_info = (0, 3, 0, 'alpha', 0)

def get_version(short=False):
	"""If short==False, outputs:
	'major.minor[.micro][ pre-alpha| alphaN| betaN]'
	If short==True, outputs:
	'major.minor[.micro][aN|bN]'
	"""
	version = '%d.%d' % version_info[:2]
	if version_info[2] != 0:
		version += '.%d' % version_info[2]
	if version_info[3] == 'final':
		pass
	elif short:
		version += '%s%d' % (version_info[3][0], version_info[4])
	elif version_info[3] == 'alpha' and version_info[4] == 0:
		version += ' pre-alpha'
	else:
		version += " %s %d" % version_info[3:]
