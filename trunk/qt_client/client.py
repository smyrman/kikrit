#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import environ as os_environ
from os.path import dirname, abspath, join as path_join
sys.path.append(path_join(abspath(dirname(__file__)), ".."))
os_environ['DJANGO_SETTINGS_MODULE'] = 'django_kikrit.settings'

from PyQt4.QtGui import QApplication

from qt_client.widgets import MainWidget


def main():
	app = QApplication(sys.argv)
	widget = MainWidget()
	widget.show()
	return app.exec_()


if __name__ == "__main__":
	main()

