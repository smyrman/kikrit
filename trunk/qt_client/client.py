#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import environ as os_environ
from os.path import dirname, abspath, join as path_join
BASEDIR = path_join(abspath(dirname(__file__)), "..")
sys.path.insert(0, BASEDIR)
os_environ['DJANGO_SETTINGS_MODULE'] = 'django_kikrit.settings'

from PyQt4.QtGui import QApplication, QTabWidget

# FIXME: Get DEVICE from settings
#from settings import DEVICE
DEVICE = None
from qt_client.main.widgets import MainWidget, DebugWidget
from qt_client.admin.widgets import AdminWidget
from qt_client.utils.threads import RFIDThread


def main():
	app = QApplication(sys.argv)

	tabs = QTabWidget()
	rfid_thread = RFIDThread(device=None)
	main_widget = MainWidget(rfid_thread, parent=tabs)
	admin_widget = AdminWidget(rfid_thread, parent=tabs)

	tabs.addTab(main_widget, "Main")
	tabs.addTab(admin_widget, "Admin")

	tabs.setWindowTitle('KiKrit')
	#tabs.showFullScreen() # Should be used in final release
	tabs.resize(600, 400)
	tabs.setMinimumSize(600, 400)
	tabs.move(200, 200)

	rfid_thread.start()
	tabs.show()

	#FIXME: Better argv check?
	if "--debug" in sys.argv[1:]:
		debug_panel = DebugWidget(tabs, rfid_thread)
		debug_panel.show()

	return app.exec_()


if __name__ == "__main__":
	main()

