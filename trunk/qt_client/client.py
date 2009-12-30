#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

from PyQt4 import QtGui

PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")
sys.path.insert(0, PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from qt_client.main.widgets import MainWidget, DepositWidget
from qt_client.admin.widgets import AdminWidget
from qt_client.utils.widgets import DebugWidget
from qt_client.utils.threads import RFIDThread

from settings import RFID_DEVICE

def main():
	app = QtGui.QApplication(sys.argv)

	tabs = QtGui.QTabWidget()
	rfid_thread = RFIDThread(device=RFID_DEVICE)
	main_widget = MainWidget(rfid_thread, parent=tabs)
	deposit_widget = DepositWidget(rfid_thread, parent=tabs)
	admin_widget = AdminWidget(rfid_thread, parent=tabs)

	if "--debug" in sys.argv[1:]:
		debug_panel = DebugWidget(tabs.window(), rfid_thread)
		debug_panel.show()
		rfid_thread.setDevice(None)

	tabs.addTab(main_widget, "Main")
	tabs.addTab(deposit_widget, "Deposit")
	tabs.addTab(admin_widget, "Admin")

	tabs.setWindowTitle('KiKrit')
	#tabs.showFullScreen() # Should be used in final release
	tabs.resize(600, 400)
	tabs.setMinimumSize(600, 400)
	tabs.move(200, 200)

	rfid_thread.start()
	tabs.show()

	return app.exec_()


if __name__ == "__main__":
	main()

