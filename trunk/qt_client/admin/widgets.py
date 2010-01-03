# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from PyQt4 import QtCore, QtGui, QtWebKit

from settings import RUNSERVER_PORT
from qt_client.utils.key_emu import KeyEmulator


class AdminWidget(QtGui.QWidget):
	web = None

	def __init__(self, rfid_thread, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.rfid_thread = rfid_thread

		# Views:
		self.web = QtWebKit.QWebView()
		self.web.load(QtCore.QUrl("http://localhost:%s/" % RUNSERVER_PORT))

		# Layout:
		grid = QtGui.QGridLayout()
		grid.addWidget(self.web, 0, 0)
		self.setLayout(grid)

		# Connect signals:
		if parent != None:
			self.parentWidget().currentChanged.connect(self.tabChanged)
		self.rfid_thread.rfid_signal.connect(self.rfidEvent)


	def _tabHasFocus(self):
		"""Returns True if self is the parrents current widget, or if there is
		no parent. Otherwise return False.

		"""
		parent = self.parentWidget()
		if parent == None or parent.currentWidget() == self:
			return True
		return False


	def tabChanged(self, index):
		#if self.parentWidget().widget(index) == self:
		pass


	def rfidEvent(self, rfid_str):
		# Guard: This widget has focus?
		if not self._tabHasFocus():
			return

		e = KeyEmulator()
		e.sendInput(rfid_str)


