# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from PyQt4 import QtCore, QtGui

from qt_client.first_run.gui_components import ImportOrNotPage


class FirstRunWidget(QtGui.QWizard):
	page_import_or_not = None
	page_import_db = None
	page_edit_settings = None
	page_add_superuser = None


	def __init__(self, parent=None):
		QtGui.QWizard.__init__(self, parent)

		self.page_import_or_not = ImportOrNotPage(self)
		self.addPage(self.page_import_or_not)
		self.addPage(QtGui.QWizardPage())
		self.addPage(QtGui.QWizardPage())
