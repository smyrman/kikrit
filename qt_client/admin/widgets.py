# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from PyQt4 import QtCore, QtGui, QtWebKit

from settings import RUNSERVER_PORT
from qt_client.utils.key_emu import KeyEmulator


class AdminWidget(QtGui.QWidget):
	web = None
	back_button= None
	next_button = None

	def __init__(self, rfid_thread, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.rfid_thread = rfid_thread

		# Views:
		self.web = QtWebKit.QWebView()
		self.web.urlChanged.connect(self.updateButtons)
		self.web.load(QtCore.QUrl("http://localhost:%s/" % RUNSERVER_PORT))

		self.back_button = QtGui.QPushButton("<--", self)
		self.next_button = QtGui.QPushButton("-->", self)
		self.back_button.clicked.connect(self.back)
		self.next_button.clicked.connect(self.next)
		
		# Layout:
		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.back_button, 0, 0)
		grid.addWidget(self.next_button, 0, 1)
		grid.addWidget(self.web, 1, 0, 1, 2)
		self.setLayout(grid)

		# Connect signals:
		if parent != None:
			self.parentWidget().currentChanged.connect(self.tabChanged)
		self.rfid_thread.rfid_signal.connect(self.rfidEvent)



	def back(self):
		"""Back button clicked, go one page back"""
		self.web.page().history().back()
	
	def next(self):
		"""Next button clicked, go to next page"""
		self.web.page().history().forward()

	def updateButtons(self):
		"""Updates fade/unfade back/next buttons"""
		history = self.web.page().history()
		if history.canGoBack():
			self.back_button.setEnabled(True)
		else:
			self.back_button.setEnabled(False)

		if history.canGoForward():
			self.next_button.setEnabled(True)
		else:
			self.next_button.setEnabled(False)


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


