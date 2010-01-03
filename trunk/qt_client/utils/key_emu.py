# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from ctypes import CDLL
Xtst = CDLL("libXtst.so.6")
Xlib = CDLL("libX11.so.6")

class KeyEmulator(object):
	display = None

	def __init__(self, display=None):
		self.display = Xtst.XOpenDisplay(display)


	def sendInput(self, txt):
		"""Emulate keypresses for all symbols in txt.  Special keys, as Return,
		Esc etc., can be encapsled by Curly baracses like this: {Return}. Pleas
		see Xlib.XStringToKeysym for where to find reference of valid symbols.

		"""
		special_key = False
		key = u""
		txt = unicode(txt)
		for c in txt:
			# Get special keys, like Return, Esc osv:
			if c == u'{':
				special_key = True
				continue
			elif c == u'}':
				special_key = False

			if special_key:
				key += c
				continue
			elif key == u"":
				key = c

			sym = Xlib.XStringToKeysym(key)
			key = u""
			code = Xlib.XKeysymToKeycode(self.display, sym)
			Xtst.XTestFakeKeyEvent(self.display, code, True, 0)
			Xtst.XTestFakeKeyEvent(self.display, code, False, 0)
		Xlib.XFlush(self.display)


	def sendKeyPress(self, key):
		"""Please see Xlib.XStringToKeysym for valid strings for key

		"""
		sym = Xlib.XStringToKeysym(str(key))
		code = Xlib.XKeysymToKeycode(self.display, sym)
		Xtst.XTestFakeKeyEvent(self.display, code, True, 0)
		Xlib.XFlush(self.display)


	def sendKeyRelease(self, key):
		"""Please see Xlib.XStringToKeysym for valid strings for key

		"""
		sym = Xlib.XStringToKeysym(str(key))
		code = Xlib.XKeysymToKeycode(self.display, sym)
		Xtst.XTestFakeKeyEvent(self.display, code, False, 0)
		Xlib.XFlush(self.display)

