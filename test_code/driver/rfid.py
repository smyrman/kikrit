#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written for python 3.1

# This file contain functions for reading the rf-id device.
# PS! The device must be set for this driver to work.
import serial

DEVICE = "/dev/ttyS0"
SER_RFID = serial.Serial(DEVICE, 9600, timeout=0.1)

def read_rfid(timeout=None):
	"""Reader
	"""
	raw_str = SER_RFID.read(100)
	str = ""
	for char in raw_str:
		if char == "\x00": str+="0"
		if char == "\x80": str+="1"
	return str

print read_rfid()
