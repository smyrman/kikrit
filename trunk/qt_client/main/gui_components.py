# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from django_kikrit.accounts.models import BalanceImage
from qt_client.main.models import MerchandiseListModel

# FIXME: Get page_time from settings:
#from settings import BALANE_PAGE_TIME_SEC
BALANCE_PAGE_TIME_SEC = 5

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


	def event(self, event):
		if event.type() == QtCore.QEvent.KeyPress:
			k = event.key()

			if k == QtCore.Qt.Key_Left:
				self.left_pressed.emit()
				return True

			elif k == QtCore.Qt.Key_Right:
				self.right_pressed.emit()
				return True

			elif k == QtCore.Qt.Key_Up:
				self.up_pressed.emit()
				return True

			elif k == QtCore.Qt.Key_Down:
				self.down_pressed.emit()
				return True

			elif k in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
				self.return_pressed.emit()
				return True

			elif k == QtCore.Qt.Key_Escape:
				self.escape_pressed.emit()
				return True
			else:
				self.setFocus()

		return QtGui.QLineEdit.event(self, event)



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

		# Signals:
		self.timer.timeout.connect(self.timeoutEvent)


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





