# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from django_kikrit.merchandise.models import Merchandise, buy_merchandise
from django_kikrit.accounts.models import Account, RFIDCard

from qt_client.main.models import MerchandiseListModel
from qt_client.main.gui_components import SearchLine, OrderPage, BalancePage


class MainWidget(QtGui.QWidget):
	"""The main tab, featuring the KiKrit client GUI.

	"""
	search_line = None
	merchandise_list = None

	stack = None
	order_page = None
	balance_page = None

	add_button = None
	remove_button = None

	status = None

	def __init__(self, rfid_thread, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.rfid_thread = rfid_thread

		# Views:
		self.search_line = SearchLine(self)
		self.search_line.grabKeyboard()

		self.merchandise_list = QtGui.QListView(self)
		self.merchandise_list.setModel(MerchandiseListModel(self._getItems(),
			self))
		self.merchandise_list.setSelectionMode(QtGui.QListView.SingleSelection)
		#self.merchandise_list.setSelectionMode(QtGui.QListView.ExtendedSelection)

		self.stack = QtGui.QStackedWidget()
		self.order_page = OrderPage(self.stack)
		self.balance_page = BalancePage(self.stack)
		self.stack.insertWidget(0, self.order_page)
		self.stack.insertWidget(1, self.balance_page)

		self.add_button = QtGui.QPushButton("Add", self)
		self.remove_button = QtGui.QPushButton("Remove", self)

		# TODO: Replace self.status with an instance of a custom class.
		self.status = QtGui.QLabel(self)
		self.status.setAlignment(QtCore.Qt.AlignRight)

		# Signals:
		if parent != None:
			self.parentWidget().currentChanged.connect(self.tabChanged)

		self.search_line.textChanged.connect(self.searchLineChanged)
		self.add_button.clicked.connect(self.addClicked)
		self.remove_button.clicked.connect(self.removeClicked)

		self.search_line.right_pressed.connect(self.rightPressed)
		self.search_line.left_pressed.connect(self.leftPressed)
		self.search_line.up_pressed.connect(self.upPressed)
		self.search_line.down_pressed.connect(self.downPressed)
		self.search_line.return_pressed.connect(self.returnPressed)
		self.search_line.escape_pressed.connect(self.escapePressed)

		self.rfid_thread.rfid_signal.connect(self.rfidEvent)

		# Layout:
		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.search_line, 0, 0)
		grid.addWidget(self.merchandise_list, 1, 0)
		grid.addWidget(self.add_button, 2, 0)
		grid.addWidget(self.stack, 1, 1)
		grid.addWidget(self.remove_button, 2, 1)
		grid.addWidget(self.status, 3, 1)

		self.setLayout(grid)

	def _reset(self):
		self.stack.setCurrentWidget(self.order_page)
		self.order_page.emptyList()
		self.search_line.setText("")
		self.merchandise_list.setFocus()


	def _tabHasFocus(self):
		"""Returns true if self is the parrents current widget, or if there is
		no parent.

		"""
		parent = self.parentWidget()
		if parent == None or parent.currentWidget() == self:
			return True
		return False

	def _getItems(self):
		""" Queries the database for all Merchandise objects, and return them
		as one large list.

		"""
		return list(Merchandise.objects.all())


	def _setSelected(self, list_view, new_index=None, next=False):
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
				QtGui.QItemSelectionModel.ClearAndSelect)


	def tabChanged(self, index):
		if self.parentWidget().indexOf(self) == index:
			self.search_line.grabKeyboard()
		else:
			self.search_line.releaseKeyboard()


	def addClicked(self):
		"""Called when the user presses the add-button"""
		# Set stack index:
		self.stack.setCurrentWidget(self.order_page)

		indexes = self.merchandise_list.selectedIndexes()

		if len(indexes) > 0:
			# Add items to order_page:
			mdl = self.merchandise_list.model()
			sel = [mdl.items[i.row()] for i in indexes]
			self.order_page.addItems(sel)
		self.search_line.selectAll()


	def removeClicked(self):
		"""Called when the user presses the remove-button"""
		indexes = self.order_page.list_view.selectedIndexes()

		if len(indexes) > 0:
			# Remove items from order_page:
			sel = self.order_page.items(indexes)
			self.order_page.removeItems(sel)

			# Reset selection:
			self.order_page.list_view.selectionModel().select(indexes[0],
					QtGui.QItemSelectionModel.ClearAndSelect)


	def searchLineChanged(self, filter_str):
		self.merchandise_list.model().filter(filter_str)
		self._setSelected(self.merchandise_list, new_index=0)


	def leftPressed(self):
		self.merchandise_list.setFocus()


	def rightPressed(self):
		self.order_page.list_view.setFocus()


	def upPressed(self):
		if self.order_page.list_view.hasFocus():
			self._setSelected(self.order_page.list_view, next=False)
		else:
			self._setSelected(self.merchandise_list, next=False)


	def downPressed(self):
		if self.order_page.list_view.hasFocus():
			self._setSelected(self.order_page.list_view, next=True)
		else:
			self._setSelected(self.merchandise_list, next=True)


	def returnPressed(self):
		if self.order_page.list_view.hasFocus():
			self.removeClicked()
		else:
			self.addClicked()

	def escapePressed(self):
		self._reset()
		self.status.setText("Order Canceled")


	def rfidEvent(self, rfid_str):
		# GUARD: tab has focus?
		if not self._tabHasFocus():
			return

		# Get card:
		try:
			card = RFIDCard.objects.get(rfid_string=unicode(rfid_str))
		except RFIDCard.DoesNotExist:
			self.status.setText("RFID card not found!")
			card = None

		# Execute purchase:
		if card != None:
			if buy_merchandise(card.account, self.order_page.items()):
				color = Account.COLOR_CHOICES[card.account.color][1]
				self._reset()
				self.status.setText("A sucsessfull purchace mr. "+ color)
				self.balance_page.showPage(card.account)
			else:
				color = Account.COLOR_CHOICES[card.account.color][1]
				self.status.setText("Transaction was disallowed mr. "+ color)




