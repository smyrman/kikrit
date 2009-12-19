# -*- coding: utf-8 -*-
from PyQt4.QtCore import QEvent, Qt, pyqtSignal
from PyQt4.QtGui import QLineEdit

class MyLineEdit(QLineEdit):
	left_pressed = pyqtSignal(name="leftRessed")
	right_pressed = pyqtSignal(name="rightPressed")
	up_pressed = pyqtSignal(name="upPressed")
	down_pressed = pyqtSignal(name="downPressed")
	return_pressed = pyqtSignal(name="returnPressed")

	def __init__(self, *args):
		QLineEdit.__init__(self, *args)


	def event(self, event):
		if event.type() == QEvent.KeyPress:
			k = event.key()

			if k == Qt.Key_Left:
				self.left_pressed.emit()
				return True

			elif k == Qt.Key_Right:
				self.right_pressed.emit()
				return True

			elif k == Qt.Key_Up:
				self.up_pressed.emit()
				return True

			elif k == Qt.Key_Down:
				self.down_pressed.emit()
				return True

			elif k == Qt.Key_Return:
				self.return_pressed.emit()
				return True

		return QLineEdit.event(self, event)


