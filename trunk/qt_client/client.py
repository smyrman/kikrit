#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

import sys
import os

from PyQt4 import QtGui, QtCore

PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 2)[0]
sys.path.insert(0, PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from qt_client.main.widgets import MainWidget, DepositWidget
from qt_client.admin.widgets import AdminWidget
from qt_client.utils.widgets import DebugWidget
from qt_client.utils.threads import RFIDThread

from settings import RFID_DEVICE, STYLE_SHEET, SPLASH_SCREEN
STYLE_SHEET = STYLE_SHEET.replace("/", os.path.sep)
SPLASH_SCREEN = SPLASH_SCREEN.replace("/", os.path.sep)


def main():
	app = QtGui.QApplication(sys.argv)

	# Splash:
	splash = QtGui.QSplashScreen(QtGui.QPixmap(SPLASH_SCREEN))
	splash.show()
	app.processEvents()

	# Stylesheet:
	app.setStyleSheet(open(STYLE_SHEET).read())

	# Threads:
	rfid_thread = RFIDThread(device=RFID_DEVICE)

	# Main window (tabs):
	tabs = QtGui.QTabWidget()
	main_widget = MainWidget(rfid_thread, parent=tabs)
	deposit_widget = DepositWidget(rfid_thread, parent=tabs)
	admin_widget = AdminWidget(rfid_thread, parent=tabs)

	tabs.addTab(main_widget, "Main")
	tabs.addTab(deposit_widget, "Deposit")
	tabs.addTab(admin_widget, "Admin")

	tabs.setWindowTitle('KiKrit')
	#tabs.showFullScreen() # Should be used in final release
	tabs.resize(1000, 600)
	tabs.setMinimumSize(600, 400)
	tabs.move(10, 200)

	# Debug panel:
	if "--debug" in sys.argv[1:]:
		debug_panel = DebugWidget(tabs.window(), rfid_thread)
		debug_panel.show()
		rfid_thread.setDevice(None)

	# Show main window / start threads:
	rfid_thread.start()
	splash.finish(tabs)
	tabs.show()

	return app.exec_()


if __name__ == "__main__":
	main()

