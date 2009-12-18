#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import environ as os_environ
from os.path import dirname, abspath, join as path_join
sys.path.append(path_join(abspath(dirname(__file__)), ".."))
os_environ['DJANGO_SETTINGS_MODULE'] = 'django_kikrit.settings'

from PyQt4.QtGui import QApplication, QTabWidget

from qt_client.main.widget import MainWidget
from qt_client.admin.widget import AdminWidget
from qt_client.debugWidget import DebugWidget


def main():
	app = QApplication(sys.argv)
	tabs = QTabWidget()

	tabs.addTab(MainWidget(), "Main")
	tabs.addTab(AdminWidget(), "Admin")
	
	# Set widget parameters:
	tabs.setWindowTitle('KiKrit')
	#tabs.showFullScreen() # Should be used in final release
	tabs.resize(600, 400)
	tabs.move(200, 200)
	tabs.show()

	#FIXME: Check arv for "--debug".
	#debug_panel = DebugWidget()
	#debug_panel.show()

	return app.exec_()


if __name__ == "__main__":
	main()

