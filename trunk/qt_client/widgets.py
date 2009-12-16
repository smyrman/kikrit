#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QLineEdit, QLabel, QPushButton, QListView,\
		QGridLayout

from django_kikrit.merchandise.models import Merchandise

from qt_client.models import MerchandiseListModel


class MainWidget(QWidget):
	search_line = None
	msg_field = None
	add_button = None
	rem_button = None
	left_list = None
	right_list = None

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		# Initialize views and models:
		self.search_line = QLineEdit(u"")
		self.search_line.grabKeyboard()

		self.msg_field = QLabel()

		self.left_list = QListView()
		self.right_list = QListView()
		self.left_list.setModel(MerchandiseListModel(self, self.getItems()))
		self.right_list.setModel(MerchandiseListModel(self, []))

		self.add_button = QPushButton("Add")
		self.rem_button = QPushButton("Remove")

		# Connect signals:
		self.connect(self.search_line, SIGNAL("textChanged(QString)"),
 				self.left_list.model().filter)
		self.connect(self.add_button, SIGNAL("clicked()"), self.add)
		self.connect(self.rem_button, SIGNAL("clicked()"), self.remove)

		# Create layout:
		grid = QGridLayout()
		grid.addWidget(self.search_line, 0, 0)
		grid.addWidget(self.left_list, 1, 0)
		grid.addWidget(self.right_list, 1, 1)
		grid.addWidget(self.add_button, 2, 0)
		grid.addWidget(self.rem_button, 2, 1)
		grid.addWidget(self.msg_field, 3, 1)
		self.setLayout(grid)

		# Set widget parameters:
		self.setWindowTitle('KiKrit')
		self.resize(600, 400)
		self.move(200, 200)


	def getItems(self):
		""" Queries the database for all Merchandise objects, and return them
		as one large list.

		"""
		return list(Merchandise.objects.all())


	def getSelected(self, list_view):
		"""Return a list of selected items

		"""
		mdl = list_view.model()
		return [mdl.items[i.row()] for i in list_view.selectedIndexes()]


	def add(self):
		"""Called when the user presses the add-button

		"""
		sel = self.getSelected(self.left_list)
		#self.left_list.model().remove(sel)
		self.right_list.model().add(sel)


	def remove(self):
		"""Called when the user presses the remove-button

		"""
		sel = self.getSelected(self.right_list)
		removed = self.right_list.model().remove(sel)
		#self.left_list.model().add(sel)

