# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui


class MyLineEdit(QtGui.QLineEdit):
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

		return QtGui.QLineEdit.event(self, event)


