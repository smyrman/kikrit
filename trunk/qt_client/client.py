#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os.path import dirname, abspath
from PyQt4.QtGui import QApplication

BASEPATH = abspath(dirname(__file__))+"/.."
sys.path.append(BASEPATH)
from qt_client.widgets import MyWidget

def main():
	app = QApplication(sys.argv)
	widget = MyWidget()
	widget.show()
	return app.exec_()

if __name__ == "__main__":
	main()

