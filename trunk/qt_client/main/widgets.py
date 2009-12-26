# -*- coding: utf-8 -*-

from PyQt4.QtCore import SIGNAL, Qt, QModelIndex
from PyQt4.QtGui import QWidget, QLineEdit, QLabel, QPushButton, QListView,\
		QGridLayout, QStackedWidget, QPixmap, QGraphicsView, QGraphicsScene,\
		QKeyEvent, QApplication, QItemSelectionModel

from django_kikrit.merchandise.models import Merchandise, buy_merchandise
from django_kikrit.accounts.models import Account, RFIDCard

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
	test_button = None
	left_list = None
	right_list = None
	stack = None
	graphics = None

	def __init__(self, rfid_thread, parent=None):
		QWidget.__init__(self, parent)

		# Initialize views and models:
		self.rfid_thread = rfid_thread

		self.search_line = MyLineEdit(self)
		self.search_line.grabKeyboard()

		self.status = QLabel(self)
		self.status.setAlignment(Qt.AlignRight)

		self.left_list = QListView(self)
		self.left_list.setModel(MerchandiseListModel(self.getItems(), self))
		self.left_list.setSelectionMode(QListView.SingleSelection)
		#self.left_list.setSelectionMode(QListView.ExtendedSelection)

		self.right_list = QListView(self)
		self.right_list.setModel(MerchandiseListModel([], self))
		self.right_list.setSelectionMode(QListView.SingleSelection)
		#self.right_list.setSelectionMode(QListView.ExtendedSelection)

		self.add_button = QPushButton("Add", self)
		self.rem_button = QPushButton("Remove", self)
		self.test_button = QPushButton("Test", self)
		#self.setFocusPolicy(Qt.StrongFocus)

		# Test image
		self.graphics = QGraphicsView(self)
		scene = QGraphicsScene(self)
		map = QPixmap("img/test.jpg") # hardcoded path, images should be in db?
		scene.addPixmap(map)
		self.graphics.setScene(scene)

		# Connect signals:
		if parent != None:
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
		self.search_line.escape_pressed.connect(self.escapePressed)

		self.rfid_thread.rfid_signal.connect(self.rfidEvent)

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


	def setSelected(self, list_view, new_index=None, next=False):
		"""Takes a QListView object, and int and a bool. Changes selection to
		new_index, or to prev or next item in list view.

		"""
		# Get new_index:
		if new_index == None:
			if next:
				indexes = [ i.row() +1 for i in list_view.selectedIndexes()]
				if len(indexes) == 0: indexes = [0]
			else:
				indexes = [ i.row() -1 for i in list_view.selectedIndexes()]
				if len(indexes) == 0: indexes = [-1]
			new_index = indexes[0]

		# Check range:
		row_count = list_view.model().rowCount()
		if new_index < 0:
			new_index += row_count
		elif new_index >= row_count:
			new_index -= row_count

		# Update selection:
		mdl_index = list_view.model().index(new_index, 0)
		list_view.selectionModel().select(mdl_index,
				QItemSelectionModel.ClearAndSelect)


	def tabChanged(self, index):
		if index == 0:
			self.search_line.grabKeyboard()
		else:
			self.search_line.releaseKeyboard()


	def addClicked(self):
		"""Called when the user presses the add-button"""
		indexes = self.left_list.selectedIndexes()

		if len(indexes) > 0:
			# Add items to right_list:
			mdl = self.left_list.model()
			sel = [mdl.items[i.row()] for i in indexes]
			self.right_list.model().add(sel)
		self.search_line.selectAll()


	def removeClicked(self):
		"""Called when the user presses the remove-button"""
		indexes = self.right_list.selectedIndexes()

		if len(indexes) > 0:
			# Remove items from right_list:
			mdl = self.right_list.model()
			sel = [mdl.items[i.row()] for i in indexes]
			removed = mdl.remove(sel)

			# Reset selection:
			self.right_list.selectionModel().select(indexes[0],
				QItemSelectionModel.ClearAndSelect)


	def showImage(self):
		cur = not(self.stack.currentIndex())
		self.stack.setCurrentIndex(cur)
		if cur:
			self.status.setText("OK")
		else:
			self.status.setText("Waiting...")


	def searchLineChanged(self, filter_str):
		self.left_list.setFocus()
		self.left_list.model().filter(filter_str)
		self.setSelected(self.left_list, new_index=0)


	def leftPressed(self):
		self.left_list.setFocus()


	def rightPressed(self):
		self.right_list.setFocus()


	def upPressed(self):
		if self.right_list.hasFocus():
			self.setSelected(self.right_list, next=False)
		else:
			self.setSelected(self.left_list, next=False)


	def downPressed(self):
		if self.right_list.hasFocus():
			self.setSelected(self.right_list, next=True)
		else:
			self.setSelected(self.left_list, next=True)


	def returnPressed(self):
		if self.right_list.hasFocus():
			self.removeClicked()
		else:
			self.addClicked()

	def escapePressed(self):
		self.right_list.model().setData([])
		self.search_line.setText("")
		self.status.setText("Order Canceled")
		self.left_list.setFocus()


	def rfidEvent(self, rfid_str):
		try:
			card = RFIDCard.objects.get(rfid_string=unicode(rfid_str))
		except RFIDCard.DoesNotExist:
			self.status.setText("No transaction: RFID card not found!")
			return False

		if buy_merchandise(card.account, self.right_list.model().items):
			self.right_list.model().setData([])
			self.search_line.setText("")
			color = Account.COLOR_CHOICES[card.account.color][1]
			self.status.setText("Transaction sucsessfull: Your are %s." %
					color)
			return True

		else:
			color = Account.COLOR_CHOICES[card.account.color][0]
			self.status.setText("No transaction: Your are %s." %
					color)
			return False



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

	def __init__(self, main_widget, parent=None):
		QWidget.__init__(self, parent)

		# Initialize views and models:
		self.main_widget = main_widget

		self.rfid_line = QLineEdit()
		self.barcode_line = QLineEdit()

		self.rfid_get_button = QPushButton("Get next rfid")
		self.barcode_get_button = QPushButton("Get next barcode")

		self.rfid_submit = QPushButton("Bib card")
		self.barcode_submit = QPushButton("Bip barcode")

		# Connect signals:
		self.rfid_get_button.clicked.connect(self.rfidGetClicked)
		self.barcode_get_button.clicked.connect(self.barcodeGetClicked)

		self.rfid_submit.clicked.connect(self.rfidSubmitClicked)
		self.barcode_submit.clicked.connect(self.barcodeSubmitClicked)

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
		str = self.rfid_line.text()
		self.main_widget.setFocus()
		self.main_widget.rfid_thread.rfid_signal.emit(str)
		print "rfid submit clicked"


	def barcodeSubmitClicked(self):
		str = self.barcode_line.text()
		e = KeyEmulator()

		self.main_widget.setFocus()
		e.sendInput(str)
		e.sendKeyPress("Return")
		e.sendKeyRelease("Return")
		print "barcode submit clicked"

