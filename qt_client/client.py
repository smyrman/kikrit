#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

"""KiKrit client is the front-end application of KiKrit. It enables purchase of
merchendaise and the performance of administrative tasks (as long as the
Django web server is running).

If you don't want to run KiKrit in the usual way, KiKrit has a number of
command line arguments:
	--help		Prints this tekst
	--version	Outout KiKrit version and database revision information
	--firstrun	Issue the first-run dialog, even when the database is corectly
				installed
	--debug		Enables the debug panel - useful for developers.
"""

import sys
import os

from PyQt4 import QtGui, QtCore

PROJECT_ROOT = os.path.abspath(__file__).rsplit(os.path.sep, 2)[0]
sys.path.insert(0, PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from qt_client.main.widgets import MainWidget, DepositWidget
from qt_client.admin.widgets import AdminWidget
from qt_client.first_run.widgets import FirstRunWidget
from qt_client.utils.widgets import DebugWidget
from qt_client.utils.threads import RFIDThread

from settings import RFID_DEVICE, STYLE_SHEET, SPLASH_SCREEN
STYLE_SHEET = STYLE_SHEET.replace("/", os.path.sep)
SPLASH_SCREEN = SPLASH_SCREEN.replace("/", os.path.sep)


def main():

	# Handle all parameters exept --debug. The first two parameters don't need
	# the qt app to be created.

	if "--help" in sys.argv[1:]:
		print __doc__
		return 0

	if "--version" in sys.argv[1:]:
		import version
		print "KiKrit", version.KIKRIT_VERSION
		print "Database revision", version.DATABASE_REVISION
		return 0

	# --firstrun needs the qt. app to be created.
	app = QtGui.QApplication(sys.argv)

	if "--firstrun" in sys.argv[1:]:
		first_run = FirstRunWidget()
		first_run.setWindowTitle("KiKrit FirstRun Wizard")
		first_run.setWindowIcon(QtGui.QIcon("graphics/favicon.png"))
		first_run.show()
		return app.exec_()

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
	#deposit_widget = DepositWidget(rfid_thread, parent=tabs)
	admin_widget = AdminWidget(rfid_thread, parent=tabs)

	tabs.addTab(main_widget, "Main")
	#tabs.addTab(deposit_widget, "Deposit")
	tabs.addTab(admin_widget, "Admin")

	tabs.setWindowTitle("KiKrit")
	tabs.setWindowIcon(QtGui.QIcon("graphics/favicon.png"))
	tabs.setMinimumSize(600, 400)
	maximize = True

	# Debug panel:
	if "--debug" in sys.argv[1:]:
		debug_panel = DebugWidget(tabs.window(), rfid_thread)
		debug_panel.show()

		rfid_thread.setDevice(None)
		maximize = False
		tabs.resize(1000, 600)
		tabs.move(10, 200)

	# Show main window / start threads:
	rfid_thread.start()
	splash.finish(tabs)
	if maximize:
		tabs.showMaximized()
	else:
		tabs.show()

	ret = app.exec_()
	rfid_thread.terminate()
	return ret


if __name__ == "__main__":
	main()

