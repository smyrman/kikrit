# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from PyQt4 import QtCore, QtGui

from django_kikrit.accounts.models import Account, RFIDCard
from django_kikrit.merchandise.models import Merchandise, buy_merchandise,\
		deposit_money
from qt_client.main.models import MerchandiseListModel
from qt_client.main.gui_components import SearchLine, AmountLine, MessageLine,\
		OrderPage, BalancePage


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

	msg = None

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

		self.stack = QtGui.QStackedWidget()
		self.order_page = OrderPage(self.stack)
		self.balance_page = BalancePage(self.stack)
		self.stack.insertWidget(0, self.order_page)
		self.stack.insertWidget(1, self.balance_page)

		self.add_button = QtGui.QPushButton("Add", self)
		self.remove_button = QtGui.QPushButton("Remove", self)

		self.msg = MessageLine()

		# Layout:
		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.search_line, 0, 0)
		grid.addWidget(self.merchandise_list, 1, 0)
		grid.addWidget(self.add_button, 2, 0)
		grid.addWidget(self.stack, 1, 1, 1, 1)
		grid.addWidget(self.remove_button, 2, 1)
		grid.addWidget(self.msg, 0, 1)

		self.setLayout(grid)

		# Connect signals:
		if parent != None:
			self.parentWidget().currentChanged.connect(self.tabChanged)

		self.search_line.textChanged.connect(self.searchLineChanged)
		self.search_line.right_pressed.connect(self.rightPressed)
		self.search_line.left_pressed.connect(self.leftPressed)
		self.search_line.up_pressed.connect(self.upPressed)
		self.search_line.down_pressed.connect(self.downPressed)
		self.search_line.return_pressed.connect(self.returnPressed)
		self.search_line.escape_pressed.connect(self.escapePressed)

		self.add_button.clicked.connect(self.addClicked)
		self.remove_button.clicked.connect(self.removeClicked)
		self.rfid_thread.rfid_signal.connect(self.rfidEvent)


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
		if self.parentWidget().widget(index) == self:
			self.search_line.grabKeyboard()
		else:
			self.search_line.releaseKeyboard()


	def addClicked(self):
		"""Called when the user presses the add-button"""
		# Set stack index:
		if self.stack.currentIndex() != 0:
			self.stack.setCurrentIndex(0)

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
			self.merchandise_list.setFocus()
			self._setSelected(self.merchandise_list, next=False)


	def downPressed(self):
		if self.order_page.list_view.hasFocus():
			self._setSelected(self.order_page.list_view, next=True)
		else:
			self.merchandise_list.setFocus()
			self._setSelected(self.merchandise_list, next=True)


	def returnPressed(self):
		if self.order_page.list_view.hasFocus():
			self.removeClicked()
		else:
			self.addClicked()


	def escapePressed(self):
		if len(self.order_page.items()) > 0:
			self.msg.post("Order canceled", self.msg.STYLE_CANCEL)
		self._reset()


	def rfidEvent(self, rfid_str):
		# GUARD: tab has focus?
		if not self._tabHasFocus():
			return

		# Get account:
		try:
			card = RFIDCard.objects.get(rfid_string=unicode(rfid_str))
			account = card.account
		except RFIDCard.DoesNotExist:
			self.msg.post(u"RFID card not found", self.msg.STYLE_ERROR)
			account = None

		# Execute purchase:
		if account != None:
			items = self.order_page.items()
			self.balance_page.showPage(account)
			if len(items) == 0:
				pass
			elif buy_merchandise(account, items):
				self._reset()
				color = account.COLOR_CHOICES[account.get_color()][1]
				self.msg.post(u"A successfull purchase mr. %s" % color,
						self.msg.STYLE_PURCHASE)
			else:
				color = account.COLOR_CHOICES[account.get_color()][1]
				self.msg.post(u"Transaction was dissalowed mr. %s" % color,
						self.msg.STYLE_ERROR)



class DepositWidget(QtGui.QWidget):
	label = None
	amount_line = None
	msg = None

	stack = None
	balance_page = None
	empty_page = None

	def __init__(self, rfid_thread, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.rfid_thread = rfid_thread

		# Views:
		self.label = QtGui.QLabel("Amount to deposit:")
		self.label.setAlignment(QtCore.Qt.AlignRight)

		self.amount_line = AmountLine()
		self.amount_line.grabKeyboard()

		self.msg = MessageLine()

		self.stack = QtGui.QStackedWidget()
		self.empty_page = QtGui.QWidget(self.stack)
		self.balance_page = BalancePage(self.stack)
		self.stack.addWidget(self.empty_page)
		self.stack.addWidget(self.balance_page)

		# Layout:
		grid = QtGui.QGridLayout()
		grid.addWidget(self.label, 0, 0)
		grid.addWidget(self.amount_line, 0, 1)
		grid.addWidget(self.stack, 1, 0, 1, 2)
		grid.addWidget(self.msg, 2, 1)
		self.setLayout(grid)

		# Connect signals:
		if parent != None:
			self.parentWidget().currentChanged.connect(self.tabChanged)
		self.rfid_thread.rfid_signal.connect(self.rfidEvent)

		self.amount_line.right_pressed.connect(self.rightPressed)
		self.amount_line.left_pressed.connect(self.leftPressed)
		self.amount_line.up_pressed.connect(self.upPressed)
		self.amount_line.down_pressed.connect(self.downPressed)
		self.amount_line.escape_pressed.connect(self.escapePressed)


	def _reset(self):
		self.amount_line.setText("")
		self.stack.setCurrentIndex(0)


	def _tabHasFocus(self):
		"""Returns True if self is the parrents current widget, or if there is
		no parent. Otherwise return False.

		"""
		parent = self.parentWidget()
		if parent == None or parent.currentWidget() == self:
			return True
		return False


	def tabChanged(self, index):
		if self.parentWidget().widget(index) == self:
			self.amount_line.grabKeyboard()
		else:
			self.amount_line.releaseKeyboard()


	def leftPressed(self):
		self.amount_line.addToAmount(-1)
		self.amount_line.selectAll()


	def rightPressed(self):
		self.amount_line.addToAmount(1)
		self.amount_line.selectAll()


	def upPressed(self):
		self.amount_line.addToAmount(10)
		self.amount_line.selectAll()


	def downPressed(self):
		self.amount_line.addToAmount(-10)
		self.amount_line.selectAll()

	def escapePressed(self):
		self._reset()


	def rfidEvent(self, rfid_str):
		# Guard: This widget has focus?
		if not self._tabHasFocus():
			return

		# Get amount:
		try:
			txt = self.amount_line.text()
			if txt == "": txt = "0"
			amount = int(txt)
			if float(amount) != float(txt):
				amount = None
				self.msg.post("Deposit amount must be an integer",
						self.msg.STYLE_ERROR)
		except ValueError:
			amount = None
			self.msg.post("Deposit amount must be an integer",
					self.msg.STYLE_ERROR)


		# Get card:
		try:
			card = RFIDCard.objects.get(rfid_string=unicode(rfid_str))
		except RFIDCard.DoesNotExist:
			self.msg.post("RFID card not found",
					self.msg.STYLE_ERROR)
			card = None

		# Execute deposit:
		if card != None and amount != None:
			if amount > 0:
				deposit_money(card.account, amount)
				self._reset()
				self.msg.post(u"An amount of %d,- was deposited" % amount,
						self.msg.STYLE_DEPOSIT)
				self.balance_page.showPage(card.account)
			else:
				self._reset()
				self.balance_page.showPage(card.account)


