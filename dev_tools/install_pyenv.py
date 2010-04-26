#!/usr/bin/env python
"""
This script is a tool to install all python dependencies for MolMod in a
seperate Python virtual environment. The script requires that virtualenv and
pip are installed.

If you are not able to install this tools, you may download the latest
redistrabutable python virtual environment for MolMod from:
git://forge.hpc.ntnu.no:molmod-pyenv.git

Usage:
  python install_pyenv.py PATH_TO_VIRTUALENV
  python install_pyenv.py -h,--help

Options:
  -h, --help	Show this text

"""

import sys
import os
from inspect import cleandoc


### SCRIPT CONFIG ###

# Python package manager:
# This script is written with pip in mind. But if you want to use a diffrent PM,
# you will probably just have to change PYPM, PYENV_PREFIX and PYPKGS so that
# the generated commands looks ok.
PYPM = "pip"

# The prefix PYPM uses to specify the virtual environment:
# pip uses '-E ', and easy_install uses '--prefix '.\
PYENV_PREFIX = "-E "

# List of packages to isntall with PYPM:
# Format is (DISPLAY_NAME, PKG_NAME),
# if pypm is pip, PKG_NAME can be the pip or easy_install package name,
# optionslly prefixed with '-U ' to specify latest option OR the repository
# location of a Git, Subersion or Mercurial project prefixed with '-e '. It is
# also possible to install several packages in on bulk:
# #("Additional dependencies", "foo baar pycairo"),
PYPKGS = [
	("django", "-U django"), # The stable branch
	#("django-svn",
	#	"-e svn+http://code.djangoproject.com/svn/django/trunk#egg=django"),
	("additional site-packages", "-U South pyserial PIL"),
]

# If you want to, you can specify a default python virtual environment to use:
PYENV = None

# Al EXTRA_COMMMANDS will be issued from the root of your python vitualenv.
site_packages = "lib/python%s/site-packages" % sys.version[:3]

EXTRA_COMMANDS = [
	# These commands will enable the system's PyQt4 in your virtualenv
	"ln -s /usr/%s/sip.so %s" % (site_packages, site_packages),
	"ln -s /usr/%s/PyQt4 %s" % (site_packages, site_packages),
]
del site_packages


### CODE ###
# Bash color codes:
COLOR_LRED = "\033[1;31m%s\033[0m"
COLOR_CYAN = "\033[1;36m%s\033[0m"


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


def install_pkgs(args):
	"""Install all needed site-packages for MolMod with pip"""
	pypm = PYPM
	pyenv = PYENV_PREFIX+args["pyenv"]

	# Build and executes the install commands:
	# Typically, the install commands will looks like this;
	# pip -E path/to/your/env install -e git://ex.com/foo.git#egg=foo
	# OR
	# pip -E path/to/your/env install -U bar
	for display_name, pkg_name in PYPKGS:
		print COLOR_LRED % ("\n### Installing %s ###" % display_name)
		cmd = "%s %s install %s" % (pypm, pyenv, pkg_name)
		print COLOR_CYAN % ("CMD: %s" % cmd)
		os.system(cmd)

	print COLOR_LRED % ("\n### Issuing extra commands ###")
	for cmd in EXTRA_COMMANDS:
		os.chdir(args["pyenv"])
		print COLOR_CYAN % ("CMD: %s" % cmd)
		os.system(cmd)


def main():
	# Configure commands to use for the installation:
	args = check_args()
	install_pkgs(args)


if __name__ == "__main__":
	main()
