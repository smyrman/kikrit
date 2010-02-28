
# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

import os
import sys

from PyQt4 import QtCore, QtGui

from settings import PROJECT_ROOT


class ImportOrNotPage(QtGui.QWizardPage):
	rb_new_db = None
	rb_import_db = None

	le_old_kkdir = None
	pb_browse = None
	fd_browse = None

	def __init__(self, parent=None):
		QtGui.QWizardPage.__init__(self, parent)

		# Create widgets:
		self.rb_new_db = QtGui.QRadioButton(u"Create new database", self)
		self.registerField("new_db", self.rb_new_db)
		self.rb_import_db = QtGui.QRadioButton(u"Import database from a "\
				"previos KiKrit installation", self)
		self.registerField("import_db",self.rb_import_db)

		self.le_old_kkdir = QtGui.QLineEdit(self)
		self.le_old_kkdir.setText(PROJECT_ROOT)
		self.registerField("old_kkdir", self.le_old_kkdir)
		self.pb_browse = QtGui.QPushButton("...", self)
		self.le_old_kkdir.setDisabled(True)
		self.pb_browse.setDisabled(True)
		self.fd_browse = QtGui.QFileDialog(self, "")
		self.fd_browse.setFileMode(self.fd_browse.Directory)

		# Layout:
		self.setTitle(u"Chose how to create the database")
		self.setSubTitle(u"Chose the later if you want to import the users, "\
				"merchandise, and transaction history from an earlier "\
				"version")

		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.rb_new_db, 0, 0, 1, 2)
		grid.addWidget(self.rb_import_db, 1, 0, 1, 2)
		grid.addWidget(self.le_old_kkdir, 2, 0, 1, 1)
		grid.addWidget(self.pb_browse, 2, 1, 1, 1)

		# Connect signals:
		self.rb_import_db.toggled.connect(self.importRadioButtonToggled)
		self.pb_browse.clicked.connect(self.browsePushButtonPressed)
		self.fd_browse.fileSelected.connect(self.fileDialogDirSelected)


	def nextId(self):
		id = QtGui.QWizardPage.nextId(self)
		#if self.rb_import_db.isChecked():
		#	id += 1
		return id


	def importRadioButtonToggled(self, value):
		if value:
			self.le_old_kkdir.setDisabled(False)
			self.pb_browse.setDisabled(False)
		else:
			self.le_old_kkdir.setDisabled(True)
			self.pb_browse.setDisabled(True)


	def browsePushButtonPressed(self):
		start = os.path.dirname(unicode(self.le_old_kkdir.text()))
		self.fd_browse.setDirectory(start)
		self.fd_browse.show()


	def fileDialogDirSelected(self, path):
		self.le_old_kkdir.setText(unicode(path))


class EditSetingsPage(QtGui.QWizardPage):
	le_rand_str = None
	pb_manual_edit = None

	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)

		# Create widgets:

		# Layout:

		# Connect signals:
