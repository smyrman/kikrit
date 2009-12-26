# -*- coding: utf-8 -*-
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QWidget, QGridLayout
from PyQt4.QtWebKit import QWebView

from django_kikrit.settings import RUNSERVER_PORT
from qt_client.utils.key_emu import KeyEmulator


class AdminWidget(QWidget):
	web = None

	def __init__(self, rfid_thread, parent=None):
		QWidget.__init__(self, parent)

		# Define views and models:
		self.rfid_thread = rfid_thread

		self.web = QWebView()
		self.web.load(QUrl("http://localhost:%s/" % RUNSERVER_PORT))

		# Connect signals:
		if parent != None:
			self.parentWidget().currentChanged.connect(self.tabChanged)

		# Layout:
		grid = QGridLayout()
		grid.addWidget(self.web, 0, 0)
		self.setLayout(grid)

	def tabChanged(self, index):
		if index == 1:
			self.rfid_thread.rfid_signal.connect(self.rfidEvent)
		else:
			self.rfid_thread.rfid_signal.disconnect(self.rfidEvent)


	def rfidEvent(self, rfid_str):
		e = KeyEmulator()
		e.sendInput(rfid_str)

