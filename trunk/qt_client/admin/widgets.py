# -*- coding: utf-8 -*-
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QWidget, QGridLayout
from PyQt4.QtWebKit import QWebView

from django_kikrit.settings import RUNSERVER_PORT


class AdminWidget(QWidget):
	web = None
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.web = QWebView()
		self.web.load(QUrl("http://localhost:%s/" % RUNSERVER_PORT))

		grid = QGridLayout()
		grid.addWidget(self.web, 0, 0)
		self.setLayout(grid)

