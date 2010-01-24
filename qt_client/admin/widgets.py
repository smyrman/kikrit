# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from PyQt4 import QtCore, QtGui, QtWebKit

from settings import RUNSERVER_PORT
from qt_client.utils.key_emu import KeyEmulator
from qt_client.utils.get_icons import getIcon


class AdminWidget(QtGui.QWidget):
	web = None
	home_url = None
	logout_url = None
	home_button = None
	back_button= None
	next_button = None
	lock_button = None

	def __init__(self, rfid_thread, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.rfid_thread = rfid_thread

		# Define url's
		self.home_url = QtCore.QUrl("http://localhost:%s/" % RUNSERVER_PORT)
		self.logout_url = QtCore.QUrl("http://localhost:%s/logout" %
				RUNSERVER_PORT)

		# Views:
		self.home_button = QtGui.QPushButton(getIcon("home", 32), "", self)
		self.back_button = QtGui.QPushButton(getIcon("back", 32), "", self)
		self.next_button = QtGui.QPushButton(getIcon("next", 32), "", self)
		self.lock_button = QtGui.QPushButton(getIcon("lock", 32), "Logout", self)
		self.web = QtWebKit.QWebView()

		self.home_button.clicked.connect(self.home)
		self.back_button.clicked.connect(self.back)
		self.next_button.clicked.connect(self.next)
		self.lock_button.clicked.connect(self.logout)
		self.web.urlChanged.connect(self.urlChanged)
		self.home()


		# Layout:
		grid = QtGui.QGridLayout(self)

		# QSizePolicy(hor, vert)
		small = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
				QtGui.QSizePolicy.Fixed)

		self.home_button.setSizePolicy(small)
		self.back_button.setSizePolicy(small)
		self.next_button.setSizePolicy(small)
		self.lock_button.setSizePolicy(small)

		# addWidget(row, col, row-size, col-size, align)
		grid.addWidget(self.home_button, 0, 0)
		grid.addWidget(self.back_button, 0, 1)
		grid.addWidget(self.next_button, 0, 2)
		grid.addWidget(self.lock_button, 0, 4, 1, 1, QtCore.Qt.AlignRight)
		grid.addWidget(self.web, 1, 0, 1, 5)
		self.setLayout(grid)

		# Connect signals:
		if parent != None:
			self.parentWidget().currentChanged.connect(self.tabChanged)
		self.rfid_thread.rfid_signal.connect(self.rfidEvent)


	def home(self):
		"""Opens the home page"""
		self.web.load(self.home_url)


	def back(self):
		"""Back button clicked, go one page back"""
		#self.web.page().history().back()
		self.web.back()


	def next(self):
		"""Next button clicked, go to next page"""
		#self.web.page().history().forward()
		self.web.forward()


	def logout(self):
		"""Logs out the user"""
		self.web.load(self.logout_url)


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_F5:
			self.web.reload()


	def urlChanged(self, new_url):
		"""Updates fade/unfade back/next buttons"""
		#history = self.web.page().history()
		history = self.web.history()

		# Clear history on logout, and rigth after login:
		if new_url == self.home_url:
			# FIXME: have away to determin if the user is loged in or not. It
			# would also enable us to use the loged in user in other aspects of
			# the program.
			history.clear()

		# Update buttons:
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


