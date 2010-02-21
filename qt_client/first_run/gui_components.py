
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from PyQt4 import QtCore, QtGui


class ImportOrNotPage(QtGui.QWizardPage):
	rb_new_db = None
	rb_import_db = None

	def __init__(self, parent=None):
		QtGui.QWizardPage.__init__(self, parent)

		self.rb_new_db = QtGui.QRadioButton(u"Create new database", self)
		self.registerField("import_db", self.rb_new_db, "0")
		self.rb_import_db = QtGui.QRadioButton(u"Import database from a "\
				"previos KiKrit installation", self)
		self.registerField("import_db",self.rb_import_db, "1")

		self.setTitle(u"Chose how to create the database")
		self.setSubTitle(u"Chose the later if you want to import the users, "\
				"merchandise, and transaction history from an earlier "\
				"version.")

		#TODO: Add greyed out line/edit with a file browser button next to it.
		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.rb_new_db, 0, 0)
		grid.addWidget(self.rb_import_db, 1, 0)



	def nextId(self):
		id = QtGui.QWizardPage.nextId(self)
		if self.rb_import_db.isChecked():
			id += 1
		return id
