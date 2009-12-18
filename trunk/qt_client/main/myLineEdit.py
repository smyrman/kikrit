# -*- coding: utf-8 -*-
from PyQt4.QtCore import QEvent, Qt, SIGNAL
from PyQt4.QtGui import QLineEdit

class MyLineEdit(QLineEdit):
	def __init__(self, *args):
		QLineEdit.__init__(self, *args)

	def event(self, event):
		if event.type() == QEvent.KeyPress:
			k = event.key()
			if k == Qt.Key_Left:
				self.emit(SIGNAL("LeftPressed()"))
				return True
			elif k == Qt.Key_Right:
				self.emit(SIGNAL("RightPressed()"))
				return True
			elif k == Qt.Key_Up:
				self.emit(SIGNAL("UpPressed()"))
				return True
			elif k == Qt.Key_Down:
				self.emit(SIGNAL("DownPressed()"))
				return True
			elif k == Qt.Key_Return:
				self.emit(SIGNAL("ReturnPressed()"))
				return True

		return QLineEdit.event(self, event)

