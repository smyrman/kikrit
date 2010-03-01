# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

import os
import sys
import shutil

from PyQt4 import QtCore, QtGui

import settings


class InfoPage(QtGui.QWizardPage):
	txt_info = None
	cb_iunderstand = None

	def __init__(self, parent=None):
		QtGui.QWizardPage.__init__(self, parent)

		# Create widgets:
		self.cb_iunderstand = QtGui.QCheckBox(u"I understand", self)
		self.registerField("iunderstand*", self.cb_iunderstand)

		# Layout:
		self.setTitle(u"Welcome to KiKrit")
		self.setSubTitle(u"Your database is not jet configured. To do so, "
				"plese read on...")
		self.txt_info = QtGui.QTextEdit(u"This wizard will help you to either "
				"install a new database, or to import and migrate the database "
				"from a previos KiKrit installation. <br><br>"
				"This wizard should only be used if you have configured KiKrit "
				" to use a local SQLite database as your databse engine "
				"(default). If you use another database engine, or connect to "
				"a remote database, you should migrate or install the "
				"database manually by using the kikrit-admin.py tool. <br><br>"
				"Before continuing, make sure that your settings regarding "
				"the database engine is ok (see settings/production.py).")
		self.txt_info.setReadOnly(True)

		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.txt_info, 0, 0, 1, 1)
		grid.addWidget(self.cb_iunderstand, 1, 0, 1, 1)

		# Connect signals:FIXME



class ImportPage(QtGui.QWizardPage):
	rb_new_db = None
	rb_import_db = None

	le_old_kkdir = None
	pb_browse = None
	fd_browse = None

	def __init__(self, parent=None):
		QtGui.QWizardPage.__init__(self, parent)

		# Create widgets:
		self.rb_new_db = QtGui.QRadioButton(u"Create new database", self)
		self.registerField("create_new_db", self.rb_new_db)
		self.rb_import_db = QtGui.QRadioButton(u"Import database from a "\
				"previos KiKrit installation", self)
		self.registerField("import_db",self.rb_import_db)

		self.le_old_kkdir = QtGui.QLineEdit(self)
		self.le_old_kkdir.setText(os.path.dirname(settings.PROJECT_ROOT))
		self.le_old_kkdir.setDisabled(True)
		self.registerField("old_kkdir", self.le_old_kkdir)
		self.pb_browse = QtGui.QPushButton("...", self)
		self.pb_browse.setDisabled(True)
		self.fd_browse = QtGui.QFileDialog(self, "")
		self.fd_browse.setFileMode(self.fd_browse.Directory)

		# Layout:
		self.setTitle(u"Chose how to create the database")
		self.setSubTitle(u"Chose the later if you want to import the users, "\
				"merchandise, and transaction history from an existing "\
				"installation of KiKrit.")

		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.rb_new_db, 0, 0, 1, 2)
		grid.addWidget(self.rb_import_db, 1, 0, 1, 2)
		grid.addWidget(self.le_old_kkdir, 2, 0, 1, 1)
		grid.addWidget(self.pb_browse, 2, 1, 1, 1)

		# Connect signals:
		self.rb_import_db.toggled.connect(self.importRadioButtonToggled)
		self.pb_browse.clicked.connect(self.browsePushButtonPressed)
		self.fd_browse.fileSelected.connect(self.fileDialogDirSelected)

		self.rb_new_db.toggled.connect(self.completeChanged.emit)
		self.rb_import_db.toggled.connect(self.completeChanged.emit)
		self.le_old_kkdir.textChanged.connect(self.completeChanged.emit)


	def isComplete(self):
		if self.rb_new_db.isChecked():
			return True

		elif self.rb_import_db.isChecked():
			# Test if kkdir is a directory, and if it contains some files that
			# prooves that it is a KiKrit dir:
			kkdir = self.le_old_kkdir.text()
			if os.path.isdir(kkdir):
				lsdir = os.listdir(kkdir)
				if "qt_client" in lsdir and "django_kikrit" in lsdir and\
					("start_kikrit.py" in lsdir or "start-kikrit.py" in lsdir):
					return True

		return False


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



class ConfirmPage(QtGui.QWizardPage):
	txt_summary = None

	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)
		self.setCommitPage(True)

		# Create widgets:
		self.txt_summary = QtGui.QTextEdit()

		# Layout:
		self.setTitle(u"The point of no return...")
		self.setSubTitle(u"If you click commit now, the following operations "
				"will be preformed:")

		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.txt_summary, 0, 0)

		# Connect signals:

		# Emit complete changed:
		self.completeChanged.emit()


	def initializePage(self):
		txt = u""
		if self.field("create_new_db").toBool():
			txt += u"* Create new db named '%s'<br>" % "FIXME.sb"

		elif self.field("import_db").toBool():
			kkdir = self.field("old_kkdir").toString()
			txt += u"* Import and migrate db from '%s'<br>" % kkdir

		self.txt_summary.setText(txt)
		#QtGui.QWizardPage.initializePage(self)



class SummaryPage(QtGui.QWizardPage):
	txt_summary = None
	is_complete = False

	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)

		# Create widgets:
		self.txt_summary = QtGui.QTextEdit()

		# Layout:
		self.setTitle(u"Installing the database")
		self.setSubTitle(u"Waiting for resutls. Please be patient")

		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.txt_summary, 0, 0)


	def isComplete(self):
		return self.is_complete


	def initializePage(self):
		txt = u""
		if self.field("create_new_db").toBool():
			# Create new db:
			os.chdir(settings.PROJECT_ROOT)
			txt += u"Installing database..."
			self.txt_summary.setText(txt)

			ret = os.system("python kikrit-admin.py install --no-input")
			if ret == 0:
				txt += u" OK<br>"
				txt += u"<br> All operations completed sucessfully!<br>"
				self.setSubTitle("OK")
			else:
				txt += u" FAILED!<br> "
				txt += u"<br> Database creation failed!<br>"
				self.setSubTitle("ERROR")
			self.txt_summary.setText(txt)
			self.is_complete = True
			self.completeChanged.emit()


		elif self.field("import_db").toBool():
			kkdir = self.field("old_kkdir").toString()
			# FIXME: Add copy and migrate db commands
			pass

		self.txt_summary.setText(txt)
		#QtGui.QWizardPage.initializePage(self)
