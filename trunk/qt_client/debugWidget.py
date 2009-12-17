# -*- coding: utf-8 -*-
from random import random

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QLineEdit, QPushButton, QGridLayout
from django_kikrit.accounts.models import RFIDCard
from django_kikrit.merchandise.models import Merchandise

#from qt_client.mainWidget import MainWidget

class DebugWidget(QWidget):
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
		# TODO: Set rfid_line text
		print rfid_card.rfid_string


	def barcodeGetClicked(self):
		id = self.last_merchandise_id + 1
		try:
			merchandise = Merchandise.objects.get(id=id)
		except Merchandise.DoesNotExist:
			id = 1
			merchandise = Merchandise.objects.get(id=id)

		self.last_merchandise_id = id
		# TODO: Set barcode_line text
		print merchandise.ean


	def rfidSubmitClicked(self):
		# TODO: Send signal to MainWidget
		print "rfid submit clicked"


	def barcodeSubmitClicked(self):
		# TODO: Append barcode_line.text to MainWidget.search_line
		# TODO: Send signal to MainWidget
		print "barcode submit clicked"


