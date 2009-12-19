# -*- coding: utf-8 -*-
import serial

from PyQt4.QtCore import QThread, pyqtSignal


class RFIDThread(QThread):
	"""A thread to check for bibed RFIDCards. Nothe that the device attribute
	must point to the right device for this driver to work.

	"""
	rfid_serial = None
	rfid_card_signal = None

	def __init__(self, parent=None, device="/dev/ttyS0", timeout=0.1):
		QThread.__init__(self, parent)
		self.rfid_serial = serial.Serial(device, 9600, timeout=timeout)
		self.rfid_card_signal = pyqtSignal()


	def setDevice(self, device, timeout=0.1):
		self.rfid_serial = serial.Serial(device, 9600, timeout=timeout)


	def readRfid(self):
		"""Try to read RFID card
		"""
		raw_str = self.serial_rfid.read(100)
		str = ""
		for char in raw_str:
			if char == "\x00": str+="0"
			elif char == "\x80": str+="1"
			else: raise Exception("Unknown char: %s" % char)
		return str


	def run(self):
		while 1:
			str = self.readRfid()
			if str:
				self.rfid_card_signal.emit(str)


