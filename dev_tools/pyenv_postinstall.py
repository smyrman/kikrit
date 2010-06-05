import os
import sys

def main():
	"""For virtual environments, symlink sip.so and PyQt4 into the
	site-packeges directory. Note that python-pyqt4 and python-sip must be
	installed to your system for this to work.

	"""
	pyenv = sys.argv[1]

	# commands will be issued from the root of your python vitualenv.
	site_packages = "lib/python%s/site-packages" % sys.version[:3]
	commands = [
		# These commands will enable the system's PyQt4 in your virtualenv
		"ln -s /usr/%s/sip.so %s" % (site_packages, site_packages),
		"ln -s /usr/%s/PyQt4 %s" % (site_packages, site_packages),
	]

	os.chdir(pyenv)
	os.system('\n'.join(commands))


if __name__ == '__main__':
	main()
