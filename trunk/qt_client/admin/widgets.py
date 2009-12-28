# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtWebKit

from django_kikrit.settings import RUNSERVER_PORT
from qt_client.utils.key_emu import KeyEmulator


class AdminWidget(QtGui.QWidget):
	web = None

	def __init__(self, rfid_thread, parent=None):
		QtGui.QWidget.__init__(self, parent)

		# Define views and models:
		self.rfid_thread = rfid_thread

		self.web = QtWebKit.QWebView()
		self.web.load(QtCore.QUrl("http://localhost:%s/" % RUNSERVER_PORT))

		# Connect signals:
		if parent != None:
			self.parentWidget().currentChanged.connect(self.tabChanged)
		self.rfid_thread.rfid_signal.connect(self.rfidEvent)

		# Layout:
		grid = QtGui.QGridLayout()
		grid.addWidget(self.web, 0, 0)
		self.setLayout(grid)


	def _tabHasFocus(self):
		"""Returns true if self is the parrents current widget, or if there is
		no parent.

		"""
		parent = self.parentWidget()
		if parent == None or parent.currentWidget() == self:
			return True
		return False


	def tabChanged(self, index):
		#if self.parentWidget().indexOf(self) == index:
		pass


	def rfidEvent(self, rfid_str):
		# Guard: This widget has focus?
		if not self._tabHasFocus():
			return

		e = KeyEmulator()
		e.sendInput(rfid_str)

