#!/usr/bin/env python
"""
This script is a tool to install most python dependencies for this project in a
seperate Python virtual environment. The script requires that virtualenv and
pip are installed.

Usage:
  python install_pyenv.py PATH_TO_VIRTUALENV
  python install_pyenv.py -h,--help

Options:
  -h, --help	Show this text

"""

import sys
import os
from inspect import cleandoc

PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 2)[0]

# Bash color codes:
COLOR_LRED = "\033[1;31m%s\033[0m"
COLOR_CYAN = "\033[1;36m%s\033[0m"


### CONFIG ###
# Optionally you can specify a default location for your pyenv
PYENV = None

### CONFIG END ###
def eprint(str):
	"""Error printing"""
	print "%s: Error: %s" % (sys.argv[0], str)


def check_args():
	"""Check sys.argv for options and position arguments. Returns a dict of
	arguments, or ends the program.

	"""
	# Set defaults:
	ret = {"pyenv": PYENV}

	# Check sys.argv for opts or args:
	# This way of cheking for opts and args are rather simplistic, but for
	# a dev-tool, it should be more then sufficiant.
	if "-h" in sys.argv or "--help" in sys.argv:
		print cleandoc(__doc__)
		exit(0)
	elif len(sys.argv) < 2:
		if not PYENV:
			eprint("You must specify the path to a virtualenv!")
			exit(1)
	else:
		ret["pyenv"] = sys.argv[1]

	return ret


def install(args):
	"""Install all needed site-packages for MolMod with pip"""
	pyenv = args["pyenv"]

	# pip requirement files:
	base_path = os.path.join(PROJECT_ROOT, 'requirements')
	req_files = ('base.txt', 'optional.txt')

	# Execute commands:
	for f in req_files:
		print COLOR_LRED % ("\n### Installing %s packages ###" % f)
		cmd = "pip -E %s install -U -r %s" %\
				(pyenv, os.path.join(base_path, f))
		print COLOR_CYAN % ("CMD: %s" % cmd)
		os.system(cmd)

	print COLOR_LRED % ("\n### Issuing extra commands ###")
	f = "post_install.py"
	cmd = 'python %s %s' % (os.path.join(base_path, f), pyenv)
	print COLOR_CYAN % ("CMD: %s" % cmd)
	os.system(cmd)


def main():
	install(check_args())


if __name__ == "__main__":
	main()
