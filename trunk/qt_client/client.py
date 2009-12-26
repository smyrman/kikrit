#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import environ as os_environ
from os.path import dirname, abspath, join as path_join
BASEDIR = path_join(abspath(dirname(__file__)), "..")
sys.path.insert(0, BASEDIR)
os_environ['DJANGO_SETTINGS_MODULE'] = 'django_kikrit.settings'

from PyQt4.QtGui import QApplication, QTabWidget

from qt_client.main.widgets import MainWidget, DebugWidget
from qt_client.admin.widgets import AdminWidget
from qt_client.utils.threads import RFIDThread

from subprocess import Popen

def main():
	app = QApplication(sys.argv)
	tabs = QTabWidget()

	# FIXME: Get DEVICE from settings
	rfid_thread = RFIDThread(device=None)
	rfid_thread.start()

	tabs.addTab(MainWidget(rfid_thread, parent=tabs), "Main")
	tabs.addTab(AdminWidget(rfid_thread, parent=tabs), "Admin")

	# Set widget parameters:
	tabs.setWindowTitle('KiKrit')
	#tabs.showFullScreen() # Should be used in final release
	tabs.resize(600, 400)
	tabs.setMinimumSize(600, 400)
	tabs.move(200, 200)
	tabs.show()

	#FIXME: Better argv check?
	if "--debug" in sys.argv[1:]:
		debug_panel = DebugWidget(rfid_thread)
		debug_panel.show()

	return app.exec_()


if __name__ == "__main__":
	main()

