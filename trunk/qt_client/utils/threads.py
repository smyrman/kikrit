# -*- coding: utf-8 -*-
import serial

from PyQt4 import QtCore


class RFIDThread(QtCore.QThread):
	"""A thread to check for bibed RFIDCards. Note that the device attribute
	must point to the right device for this driver to work.

	"""
	rfid_serial = None
	rfid_signal = QtCore.pyqtSignal(str, name="rfidSignal")

	def __init__(self, parent=None, device="/dev/ttyS0", timeout=0.1):
		QtCore.QThread.__init__(self, parent)
		if device != None:
			self.setDevice(device)


	def setDevice(self, device, timeout=0.1):
		self.rfid_serial = serial.Serial(device, 9600, timeout=timeout)


	def readRfid(self):
		"""Try to read RFID card. Return encoded

		"""
		raw_str = self.rfid_serial.read(100)
		str = ""
		for char in raw_str:
			if char == "\x00": str+="0"
			elif char == "\x80": str+="1"
			else: raise self.RFIDException("Unknown char: %s" % char)

		return str


	def run(self):
		# GUARD: Device not set?
		if self.rfid_serial == None:
			print "no device set. Entering 'debug' mode.. (a.k.a. deep sleep)"
			while 1: self.sleep(30)

		# Main loop:
		while 1:
			str = self.readRfid()
			if str:
				self.rfid_signal.emit(str)

	class RFIDException(Exception):
		pass


