#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

from PyQt4 import QtGui

BASEDIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")
sys.path.insert(0, BASEDIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_kikrit.settings'
from qt_client.main.widgets import MainWidget
from qt_client.admin.widgets import AdminWidget
from qt_client.utils.widgets import DebugWidget
from qt_client.utils.threads import RFIDThread

# FIXME: Get DEVICE from settings
#from settings import DEVICE
DEVICE = None

def main():
	app = QtGui.QApplication(sys.argv)

	tabs = QtGui.QTabWidget()
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

	if "--debug" in sys.argv[1:]:
		debug_panel = DebugWidget(tabs.window(), rfid_thread)
		debug_panel.show()

	return app.exec_()


if __name__ == "__main__":
	main()

