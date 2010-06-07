# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from PyQt4 import QtCore, QtGui

from first_run.gui_components import InfoPage, ImportPage, ConfirmPage,\
                                     SummaryPage


class FirstRunWidget(QtGui.QWizard):
	page_info = None
	page_importdb = None
	page_confirm = None
	page_sumary = None


	def __init__(self, parent=None):
		QtGui.QWizard.__init__(self, parent)

		self.page_info = InfoPage(self)
		self.addPage(self.page_info)
		self.page_importdb = ImportPage(self)
		self.addPage(self.page_importdb)
		self.page_confirm = ConfirmPage(self)
		self.addPage(self.page_confirm)
		self.page_summary = SummaryPage(self)
		self.addPage(self.page_summary)
