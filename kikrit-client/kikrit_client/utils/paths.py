"""
Os Compatibility
"""

import os
import re

def path4os(path):
	"""A small helper function to normalize path (i.e. 'A/../B' becomes 'B'),
	replace environment variables '$var'. '${var}' and the common prefixes '~'
	and '/etc/' on Windos, and convert posixpath to ntpath if os==Windows.
	"""
	# Windows specific:
	if os.name == 'nt':
		# Replace '/etc/' with 'C:\Documents and Settings\All Users\config'
		regexp = re.compile('^/etc/')
		path = regexp.sub('${ALLUSERSPROFILE}/config/', path, 1)
	# replace ~ and ~user with HOME path:
	path = os.path.expanduser(path)
	# replace $var and ${var} with evironement variable var:
	path = os.path.expandvars(path)
	# Replace things like '/./' and 'A/../B'. Repace '/' with '\' on Windows:
	path = os.path.normpath(path)
	return path
