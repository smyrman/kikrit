#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import environ as os_environ
from os.path import dirname, abspath, join as path_join
sys.path.append(path_join(abspath(dirname(__file__)), ".."))
os_environ['DJANGO_SETTINGS_MODULE'] = 'django_kikrit.settings'

from PyQt4.QtGui import QApplication, QTabWidget

from qt_client.mainWidget import MainWidget
from qt_client.adminWidget import AdminWidget


def main():
	app = QApplication(sys.argv)
	tabs = QTabWidget()

	tabs.addTab(MainWidget(), "Main")
	tabs.addTab(AdminWidget(), "Admin")

	tabs.show()
	return app.exec_()


if __name__ == "__main__":
	main()

