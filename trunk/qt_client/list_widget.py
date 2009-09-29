#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QApplication, QLineEdit, QLabel,\
		QPushButton, QListView, QGridLayout

from list_model import MyListModel

class MyWidget(QWidget):
	search_line = None
	status_text = None
	add_button = None
	rem_button = None
	left_list = None
	right_list = None


	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.search_line = QLineEdit()
		self.search_line.grabKeyboard()
		self.connect(self.search_line, SIGNAL("textChanged(QString)"),
		             self.search)
		self.status_text = QLabel()


		self.add_button = QPushButton("Add")
		self.rem_button = QPushButton("Remove")

		self.connect(self.add_button, SIGNAL("clicked()"), self.add)
		self.connect(self.rem_button, SIGNAL("clicked()"), self.remove)

		self.left_list = QListView()
		self.left_list.setModel(MyListModel(self, ["A", "B", "C"]))
		self.right_list = QListView()
		self.right_list.setModel(MyListModel(self))

		grid = QGridLayout()
		grid.addWidget(self.search_line, 0, 0)
		grid.addWidget(self.left_list, 1, 0)
		grid.addWidget(self.right_list, 1, 1)
		grid.addWidget(self.add_button, 2, 0)
		grid.addWidget(self.rem_button, 2, 1)
		grid.addWidget(self.status_text, 3, 1)
		self.setLayout(grid)

		self.setWindowTitle('Laughing app')
		self.resize(300, 100)
		self.move(400, 400)

	def selected(self, list):
		selected = []
		for i in list.selectedIndexes():
			selected.append(i.data().toString())
			print i.data().toString()
		return selected

	def add(self):
		selected = self.selected(self.left_list)
		self.left_list.model().remove(selected)
		self.right_list.model().add(selected)

	def remove(self):
		selected = self.selected(self.right_list)
		self.right_list.model().remove(selected)
		self.left_list.model().add(selected)


	def search(self):
		self.status_text.setText(self.search_line.text())

def main():
	app = QApplication(argv)
	widget = MyWidget()
	widget.show()
	return app.exec_()

if __name__ == "__main__":
	main()
