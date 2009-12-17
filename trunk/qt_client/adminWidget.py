# -*- coding: utf-8 -*-
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QWidget, QGridLayout
from PyQt4.QtWebKit import QWebView

class AdminWidget(QWidget):
	web = None
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.web = QWebView()
		self.web.load(QUrl("http://omegav.no/"))

		grid = QGridLayout()
		grid.addWidget(self.web, 0, 0)
		self.setLayout(grid)

