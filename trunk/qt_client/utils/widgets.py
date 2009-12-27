# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from django_kikrit.merchandise.models import Merchandise
from django_kikrit.accounts.models import RFIDCard

from qt_client.utils.key_emu import KeyEmulator


class DebugWidget(QtGui.QWidget):
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

	def __init__(self, main_window, rfid_thread, parent=None):
		QtGui.QWidget.__init__(self, parent)

		# Initialize views and models:
		self.rfid_thread = rfid_thread
		self.main_window = main_window

		self.rfid_line = QtGui.QLineEdit()
		self.barcode_line = QtGui.QLineEdit()

		self.rfid_get_button = QtGui.QPushButton("Get next rfid")
		self.barcode_get_button = QtGui.QPushButton("Get next barcode")

		self.rfid_submit = QtGui.QPushButton("Bib card")
		self.barcode_submit = QtGui.QPushButton("Bip barcode")

		# Connect signals:
		self.rfid_get_button.clicked.connect(self.rfidGetClicked)
		self.barcode_get_button.clicked.connect(self.barcodeGetClicked)

		self.rfid_submit.clicked.connect(self.rfidSubmitClicked)
		self.barcode_submit.clicked.connect(self.barcodeSubmitClicked)

		# Create layout:
		grid = QtGui.QGridLayout()
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
		self.main_window.activateWindow()
		self.rfid_thread.rfid_signal.emit(str)
		print "rfid submit clicked"


	def barcodeSubmitClicked(self):
		str = self.barcode_line.text()
		e = KeyEmulator()

		self.main_window.activateWindow()
		e.sendInput(str)
		e.sendKeyPress("Return")
		e.sendKeyRelease("Return")
		print "barcode submit clicked"

