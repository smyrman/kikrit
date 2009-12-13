#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QLineEdit, QLabel, QPushButton, QListView,\
		QGridLayout

from qt_client.models import MyListModel, Item


class MyWidget(QWidget):
	search_line = None
	status_text = None
	add_button = None
	rem_button = None
	left_list = None
	right_list = None


	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.search_line = QLineEdit(u"Sindre fix ascii øl")
		self.search_line.grabKeyboard()
		self.connect(self.search_line, SIGNAL("textChanged(QString)"),
		             self.search)
		self.status_text = QLabel()


		self.add_button = QPushButton("Add")
		self.rem_button = QPushButton("Remove")

		self.connect(self.add_button, SIGNAL("clicked()"), self.add)
		self.connect(self.rem_button, SIGNAL("clicked()"), self.remove)

		self.left_list = QListView()
		self.left_list.setModel(MyListModel(self, self.getItems()))
		self.right_list = QListView()
		self.right_list.setModel(MyListModel(self, []))

		grid = QGridLayout()
		grid.addWidget(self.search_line, 0, 0)
		grid.addWidget(self.left_list, 1, 0)
		grid.addWidget(self.right_list, 1, 1)
		grid.addWidget(self.add_button, 2, 0)
		grid.addWidget(self.rem_button, 2, 1)
		grid.addWidget(self.status_text, 3, 1)
		self.setLayout(grid)

		self.setWindowTitle('KiKrit')
		self.resize(400, 400)
		self.move(200, 200)

	def getItems(self):
		items = []
		# TODO probe en database...
		items.append( Item(u"Øl", 16, 403) ) # TODO python elsker tydligvis asci
		items.append( Item(u"Vin", 16, 80) )
		return items


	def getSelected(self, list):
		"""Returnerer en liste med valgte objekter av typen Item"""
		names = []
		for i in list.selectedIndexes():
			names.append(i.data().toString())
		selected = list.model().getItemsByName(names)

		# DEBUG:
		for s in selected:
			print u"selected:", s.name, s.price, s.ean
		return selected

	def add(self):
		"""Called when the user presses the add-button"""
		sel = self.getSelected(self.left_list)
		#self.left_list.model().remove(sel)
		self.right_list.model().add(sel)

	def remove(self):
		"""Called when the user presses the remove-button"""
		sel = self.getSelected(self.right_list)
		removed = self.right_list.model().remove(sel)
		#self.left_list.model().add(sel)


	def search(self):
		self.status_text.setText(self.search_line.text())

