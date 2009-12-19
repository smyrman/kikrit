# -*- coding: utf-8 -*-

from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QWidget, QLineEdit, QLabel, QPushButton, QListView,\
		QGridLayout, QStackedWidget, QPixmap, QGraphicsView, QGraphicsScene,\
		QKeyEvent, QApplication

from django_kikrit.merchandise.models import Merchandise
from django_kikrit.accounts.models import RFIDCard

from qt_client.utils.key_emu import KeyEmulator
from qt_client.main.models import MerchandiseListModel
from qt_client.main.myLineEdit import MyLineEdit

class MainWidget(QWidget):
	"""The main tab, featuring the KiKrit client GUI.

	"""
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
		self.setFocusPolicy(Qt.StrongFocus)

		# Test image
		self.graphics = QGraphicsView()
		scene = QGraphicsScene()
		map = QPixmap("img/test.jpg") # hardcoded path, images should be in db?
		scene.addPixmap(map)
		self.graphics.setScene(scene)

		# Connect signals:
		self.parentWidget().currentChanged.connect(self.tabChanged)

		self.search_line.textChanged.connect(self.searchLineChanged)
		self.add_button.clicked.connect(self.addClicked)
		self.rem_button.clicked.connect(self.removeClicked)
		self.test_button.clicked.connect(self.showImage)

		self.search_line.right_pressed.connect(self.rightPressed)
		self.search_line.left_pressed.connect(self.leftPressed)
		self.search_line.up_pressed.connect(self.upPressed)
		self.search_line.down_pressed.connect(self.downPressed)
		self.search_line.return_pressed.connect(self.returnPressed)

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


	def tabChanged(self, index):
		if index == 0:
			self.search_line.grabKeyboard()
		else:
			self.search_line.releaseKeyboard()


	def addClicked(self):
		"""Called when the user presses the add-button"""
		sel = self.getSelected(self.left_list)
		self.right_list.model().add(sel)


	def removeClicked(self):
		"""Called when the user presses the remove-button"""
		sel = self.getSelected(self.right_list)
		removed = self.right_list.model().remove(sel)

	def showImage(self):
		cur = not(self.stack.currentIndex())
		self.stack.setCurrentIndex(cur)
		if cur:
			self.status.setText("OK")
		else:
			self.status.setText("Waiting...")

	def searchLineChanged(self, filter_str):
		self.left_list.model().filter(filter_str)

	def leftPressed(self):
		self.left_list.setFocus()

	def rightPressed(self):
		self.right_list.setFocus()

	def upPressed(self):
		# Find selected list
		list = None
		if self.right_list.hasFocus():
			list = self.right_list
		else:
			list = self.left_list

		# TODO: iterate with "QListViewItemIterator"

	def downPressed(self):
		print "down"

	def returnPressed(self):
		print "return"



class DebugWidget(QWidget):
	"""A small gui, used to debug the main/admin GUI

	"""
	last_merchandise_id = 0
	last_rfidcard_id = 0

	rfid_line = None
	rfid_submit = None
	rfid_get_button = None

	barcode_line = None
	barcode_submit = None
	barcode_get_button = None

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		# Initialize views and models:
		self.rfid_line = QLineEdit()
		self.barcode_line = QLineEdit()

		self.rfid_get_button = QPushButton("Get next rfid")
		self.barcode_get_button = QPushButton("Get next barcode")

		self.rfid_submit = QPushButton("Bib card")
		self.barcode_submit = QPushButton("Bip barcode")

		# Connect signals:
		self.connect(self.rfid_get_button, SIGNAL("clicked()"),
				self.rfidGetClicked)
		self.connect(self.barcode_get_button, SIGNAL("clicked()"),
				self.barcodeGetClicked)

		self.connect(self.rfid_submit, SIGNAL("clicked()"),
				self.rfidSubmitClicked)
		self.connect(self.barcode_submit, SIGNAL("clicked()"),
				self.barcodeSubmitClicked)

		# Create layout:
		grid = QGridLayout()
		grid.addWidget(self.rfid_get_button, 0, 0)
		grid.addWidget(self.rfid_line, 0, 1)
		grid.addWidget(self.rfid_submit, 0, 2)

		grid.addWidget(self.barcode_get_button, 1, 0)
		grid.addWidget(self.barcode_line, 1, 1)
		grid.addWidget(self.barcode_submit, 1, 2)

		self.setLayout(grid)

		# Set widget parameters:
		self.setWindowTitle('KiKrit Debug')
		self.resize(600, 100)
		self.move(200, 60)


	def rfidGetClicked(self):
		id = self.last_rfidcard_id + 1
		try:
			rfid_card = RFIDCard.objects.get(id=id)
		except RFIDCard.DoesNotExist:
			id = 1
			rfid_card = RFIDCard.objects.get(id=id)

		self.last_rfidcard_id = id
		self.rfid_line.setText(rfid_card.rfid_string)


	def barcodeGetClicked(self):
		id = self.last_merchandise_id + 1
		try:
			merchandise = Merchandise.objects.get(id=id)
		except Merchandise.DoesNotExist:
			id = 1
			merchandise = Merchandise.objects.get(id=id)

		self.last_merchandise_id = id
		self.barcode_line.setText(merchandise.ean)


	def rfidSubmitClicked(self):
		# TODO: Send RFID signal
		print "rfid submit clicked"


	def barcodeSubmitClicked(self):
		#str = self.barcode_line.getText()
		str = u"001"
		e = KeyEmulator()
		e.sendInput(str)
		e.sendKeyPress("Return")
		e.sendKeyRelease("Return")

		print "barcode submit clicked"

