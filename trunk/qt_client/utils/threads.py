# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

import serial

from PyQt4 import QtCore


class RFIDThread(QtCore.QThread):
	"""A thread to check for bibed RFIDCards. Note that the device attribute
	must point to the right device for this driver to work.

	"""
	device = None
	rfid_serial = None
	rfid_signal = QtCore.pyqtSignal(str, name="rfidSignal")

	def __init__(self, parent=None, device=None, timeout=0.1):
		QtCore.QThread.__init__(self, parent)
		self.setDevice(device, timeout)


	def setDevice(self, device, timeout=0.1):
		self.device = device
		# GUARD: device is None?
		if device == None:
			self.rfid_serial = None
			return False

		# Try to set rfid_serial:
		ret = False
		try:
			self.rfid_serial = serial.Serial(device, 9600, timeout=timeout)
			ret = True
		except serial.serialutil.SerialException:
			pass

		return ret


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
		if self.device == None:
			print "WARNING: RFID device not set",
			"\n -> Check the RFID_DEVICE parameter in your settings!"
			while 1:
				self.sleep(30)
		# Main loop:
		while 1:
			#if self.rfid_serial == None:
			try:
				str = self.readRfid()
				if str:
					self.rfid_signal.emit(str)
			except AttributeError:
				if not self.setDevice(self.device):
					print "WARNING: Serial device '%s' not found!" \
							% self.device
					print " -> retry in 10 sec."
					self.sleep(10)

	class RFIDException(Exception):
		pass


