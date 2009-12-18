from ctypes import CDLL
Xtst = CDLL("libXtst.so.6")
Xlib = CDLL("libX11.so.6")

class KeyEmulator(object):
	dpy = None

	def __init__(self, display=None):
		self.dpy = Xtst.XOpenDisplay(display)


	def sendInput(self, txt):
		"""Takes a string. Emulate keypresses for all symbols in string

		"""
		for c in txt:
			sym = Xlib.XStringToKeysym(c)
			code = Xlib.XKeysymToKeycode(self.dpy, sym)
			Xtst.XTestFakeKeyEvent(self.dpy, code, True, 0)
			Xtst.XTestFakeKeyEvent(self.dpy, code, False, 0)
		Xlib.XFlush(self.dpy)


	def sendKeyPress(self, key):
		"""Please see Xlib.XStringToKeysym for valid strings for key

		"""
		sym = Xlib.XStringToKeysym(str(key))
		code = Xlib.XKeysymToKeycode(self.dpy, sym)
		Xtst.XTestFakeKeyEvent(self.dpy, code, True, 0)
		Xlib.XFlush(self.dpy)


	def sendKeyRelease(self, key):
		"""Please see Xlib.XStringToKeysym for valid strings for key

		"""
		sym = Xlib.XStringToKeysym(str(key))
		code = Xlib.XKeysymToKeycode(self.dpy, sym)
		Xtst.XTestFakeKeyEvent(self.dpy, code, False, 0)
		Xlib.XFlush(self.dpy)

