# -*- coding: utf-8 -*-
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QWidget, QGridLayout
from PyQt4.QtWebKit import QWebView

class AdminWidget(QWidget):
	web = None
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.web = QWebView()
		# FIXME: Get port from django_kikrit.settings
		self.web.load(QUrl("http://localhost:8081/"))

		grid = QGridLayout()
		grid.addWidget(self.web, 0, 0)
		self.setLayout(grid)

