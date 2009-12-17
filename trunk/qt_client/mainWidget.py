# -*- coding: utf-8 -*-

from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QWidget, QLineEdit, QLabel, QPushButton, QListView,\
		QGridLayout, QStackedWidget, QPixmap, QGraphicsView, QGraphicsScene,\
		QShortcut, QKeySequence

from django_kikrit.merchandise.models import Merchandise

from qt_client.models import MerchandiseListModel
from qt_client.myLineEdit import MyLineEdit

class MainWidget(QWidget):
	search_line = None
	status = None
	add_button = None
	rem_button = None
	left_list = None
	right_list = None
	stack = None
	graphics = None

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		# Initialize views and models:
		self.search_line = MyLineEdit()
		self.search_line.grabKeyboard()

		self.status = QLabel()
		self.status.setAlignment(Qt.AlignRight)

		self.left_list = QListView()
		self.right_list = QListView()
		self.left_list.setModel(MerchandiseListModel(self, self.getItems()))
		self.right_list.setModel(MerchandiseListModel(self, []))

		self.add_button = QPushButton("Add")
		self.rem_button = QPushButton("Remove")
		self.test_button = QPushButton("Test")

		# Test image
		self.graphics = QGraphicsView()
		scene = QGraphicsScene()
		map = QPixmap("img/test.jpg") # hardcoded path, images should be in db?
		scene.addPixmap(map)
		self.graphics.setScene(scene)

		# Connect signals:
		self.connect(self.search_line, SIGNAL("textChanged(QString)"),
				self.search_line_changed)
		self.connect(self.add_button, SIGNAL("clicked()"), self.add_clicked)
		self.connect(self.rem_button, SIGNAL("clicked()"), self.remove_clicked)
		self.connect(self.test_button, SIGNAL("clicked()"), self.show_image)

		self.connect(self.search_line, SIGNAL("RightPressed()"), self.add_clicked)
		self.connect(self.search_line, SIGNAL("LeftPressed()"), self.remove_clicked)

		# Create layout:
		self.stack = QStackedWidget()
		self.stack.insertWidget(0, self.right_list)
		self.stack.insertWidget(1, self.graphics)

		grid = QGridLayout()
		grid.addWidget(self.search_line, 0, 0)
		grid.addWidget(self.test_button, 0, 1)
		grid.addWidget(self.left_list, 1, 0)
		grid.addWidget(self.stack, 1, 1)
		grid.addWidget(self.add_button, 2, 0)
		grid.addWidget(self.rem_button, 2, 1)
		grid.addWidget(self.status, 3, 1)

		self.setLayout(grid)


	def getItems(self):
		""" Queries the database for all Merchandise objects, and return them
		as one large list.

		"""
		return list(Merchandise.objects.all())


	def getSelected(self, list_view):
		"""Return a list of selected items"""
		mdl = list_view.model()
		return [mdl.items[i.row()] for i in list_view.selectedIndexes()]


	def add_clicked(self):
		"""Called when the user presses the add-button"""
		sel = self.getSelected(self.left_list)
		#self.left_list.model().remove(sel)
		self.right_list.model().add(sel)


	def remove_clicked(self):
		"""Called when the user presses the remove-button"""
		sel = self.getSelected(self.right_list)
		removed = self.right_list.model().remove(sel)
		#self.left_list.model().add(sel)

	def show_image(self):
		cur = not(self.stack.currentIndex())
		self.stack.setCurrentIndex(cur)
		if cur:
			self.status.setText("OK")
		else:
			self.status.setText("Waiting...")

	def search_line_changed(self, filter_str):
		self.left_list.model().filter(filter_str)


