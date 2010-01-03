# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from PyQt4 import QtCore, QtGui

from settings import BALANCE_PAGE_TIME_SEC, MESSAGE_TIME_SEC
from django_kikrit.accounts.models import BalanceImage
from qt_client.utils.get_icons import getIcon
from qt_client.main.models import MerchandiseListModel


class SearchLine(QtGui.QLineEdit):
	"""LineEdid that grabs the keyboard, and send events upon some of the
	key_presses.

	"""
	left_pressed = QtCore.pyqtSignal(name="leftRessed")
	right_pressed = QtCore.pyqtSignal(name="rightPressed")
	up_pressed = QtCore.pyqtSignal(name="upPressed")
	down_pressed = QtCore.pyqtSignal(name="downPressed")
	return_pressed = QtCore.pyqtSignal(name="returnPressed")
	escape_pressed = QtCore.pyqtSignal(name="escapePressed")

	def __init__(self, *args):
		QtGui.QLineEdit.__init__(self, *args)


	def _validateKey(self, key_event):
		if unicode(key_event.text()) != "":
			return True
		return False


	def event(self, event):
		ret = QtGui.QLineEdit.event(self, event)

		if event.type() == QtCore.QEvent.KeyPress:
			k = event.key()
			if k == QtCore.Qt.Key_Left:
				self.left_pressed.emit()
				ret = True

			elif k == QtCore.Qt.Key_Right:
				self.right_pressed.emit()
				ret = True

			elif k == QtCore.Qt.Key_Up:
				self.up_pressed.emit()
				ret = True

			elif k == QtCore.Qt.Key_Down:
				self.down_pressed.emit()
				ret = True

			elif k in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
				self.return_pressed.emit()
				ret = True

			elif k == QtCore.Qt.Key_Escape:
				self.escape_pressed.emit()
				ret = True

			elif self._validateKey(event):
				self.setFocus()
				# Keypress does defaut action.
				# No custom signals are sent.

		return ret



class AmountLine(SearchLine):

	def _validateKey(self, key_event):
		return unicode(key_event.text()).isnumeric()


	def addToAmount(self, amount):
		try:
			i = int(self.text()) + amount
		except ValueError:
			i = amount

		if i < 0:
			i = 0

		self.setText(unicode(i))



class MessageLine(QtGui.QPushButton):
	STYLE_NONE = ("msgNone", "") # obj_name, icon_name
	STYLE_INFO = ("msgInfo", "info")
	STYLE_ERROR = ("msgError", "error")
	STYLE_CANCEL = ("msgCancel", "cancel")
	STYLE_SUCCESS = ("msgSuccess", "success")
	STYLE_PURCHASE = ("msgPurchase", "purchase")
	STYLE_DEPOSIT = ("msgDeposit", "deposit")

	timer = None

	def __init__(self, *args):
		QtGui.QPushButton.__init__(self, *args)

		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.timeoutEvent)
		self.setFlat(True)
		self.setAutoFillBackground(True)
		self._setStyle(self.STYLE_NONE)

	def _setStyle(self, style):
		self.setObjectName(style[0])
		self.setIcon(getIcon(style[1]))
		# Force style update:
		st = self.style()
		self.setStyle(st)

	def post(self, txt, style):
		self._setStyle(style)
		self.setText(txt)
		self.timer.start(MESSAGE_TIME_SEC*1000)

	def timeoutEvent(self):
		self.timer.stop()
		self.setText("")
		self._setStyle(self.STYLE_NONE)




class OrderPage(QtGui.QWidget):
	"""QStack page used to display the current order and total price.

	"""
	_sum1 = 0
	_sum2 = 0

	list_view = None
	total_label = None
	sum_label = None

	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)

		# Views:
		self.list_view = QtGui.QListView(self)
		self.list_view.setModel(MerchandiseListModel([]))
		self.list_view.setSelectionMode(QtGui.QListView.SingleSelection)
		#self.list_view.setSelectionMode(QtGui.QListView.ExtendedSelection)

		self.total_label = QtGui.QLabel("Total:")
		self.total_label.setAlignment(QtCore.Qt.AlignLeft)

		self.sum_label = QtGui.QLabel(self)
		self.sum_label.setAlignment(QtCore.Qt.AlignRight)
		self.sum_label.setText("%d,- (%d,-)" % (self._sum1, self._sum2))

		# Layout:
		sum_layout = QtGui.QGridLayout()

		grid = QtGui.QGridLayout(self)
		grid.setMargin(0)
		grid.addWidget(self.list_view, 0, 0, 1, 2)
		grid.addWidget(self.total_label, 1, 0)
		grid.addWidget(self.sum_label, 1, 1)
		self.setLayout(grid)

		# Style:
		self.setObjectName("orderPage")
		self.list_view.setObjectName("orderPage")
		self.total_label.setObjectName("orderPage")
		self.sum_label.setObjectName("orderPage")


	def items(self, indexes=None):
		if indexes != None:
			return [self.list_view.model().items[i.row()] for i in indexes]
		else:
			return self.list_view.model().items


	def addItems(self, items):
		self.list_view.model().add(items)
		self._sum1 += sum((i.ordinary_price for i in items))
		self._sum2 += sum((i.internal_price for i in items))
		self.sum_label.setText("%d,- (%d,-)" % (self._sum1, self._sum2))


	def removeItems(self, items):
		self.list_view.model().remove(items)
		self._sum1 -= sum((i.ordinary_price for i in items))
		self._sum2 -= sum((i.internal_price for i in items))
		self.sum_label.setText("%d,- (%d,-)" % (self._sum1, self._sum2))


	def emptyList(self):
		self.list_view.model().setData([])
		self._sum1 = 0
		self._sum2 = 0
		self.sum_label.setText("%d,- (%d,-)" % (self._sum1, self._sum2))



class BalancePage(QtGui.QWidget):
	"""QStack page used to display balance, balance image and color of an
	Account.

	"""
	reset_index = 0 # The index timeoutEvent will set the parent to.

	label1 = None
	lable2 = None
	image = None
	timer = None

	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)

		# Views:
		self.label1 = QtGui.QLabel("User's full name goes here", self)
		self.label1.setAlignment(QtCore.Qt.AlignCenter)

		self.label2 = QtGui.QLabel("Account balance goes here", self)
		self.label2.setAlignment(QtCore.Qt.AlignCenter)

		self.image = QtGui.QGraphicsView(self)
		self.image.setAlignment(QtCore.Qt.AlignCenter)

		self.timer = QtCore.QTimer()

		# Layout:
		grid = QtGui.QGridLayout(self)
		grid.setMargin(0)
		grid.addWidget(self.label1, 0, 0)
		grid.addWidget(self.image, 1, 0)
		grid.addWidget(self.label2, 2, 0)
		self.setLayout(grid)

		# Connect signals:
		self.timer.timeout.connect(self.timeoutEvent)

		# Style:
		self.setObjectName("balancePage")
		self.label1.setObjectName("balancePage")
		self.label2.setObjectName("balancePage")
		self.image.setObjectName("balancePage")


	def showPage(self, account):
		"""Takes an Account object. Update labels and balance image, then start
		the timer. then show this page.

		"""
		# Set lables:
		txt2 = u"Balance: %d" % account.balance
		self.label2.setText(txt2)

		# Try to get users full name:
		if account.user != None:
			txt1 = u"%s %s" % (account.user.first_name, account.user.last_name)
		else:
			txt1 = u" "
		# Or use account name:
		if txt1 == u" ":
			txt1 = account.name
		self.label1.setText(txt1)

		# Set image:
		scene = QtGui.QGraphicsScene()
		try:
			map = QtGui.QPixmap(account.get_image().image.name)
			scene.addPixmap(map)
		except BalanceImage.DoesNotExist:
			scene.addText("image not found")
		self.image.setScene(scene)

		# Start timer:
		self.timer.start(BALANCE_PAGE_TIME_SEC*1000)

		# Update parent index:
		self.parentWidget().setCurrentWidget(self)


	def timeoutEvent(self):
		self.parentWidget().setCurrentIndex(self.reset_index)
		self.timer.stop()





