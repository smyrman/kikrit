# -*- coding: utf-8 -*-

# Copyright (C) 2010: Sindre Røkenes Myren, Andreas Hopland Sperre

# This file is part of KiKrit wich is distrebuted under GPLv3. See the file
# COPYING.txt for more details.

from PyQt4 import QtCore


class MerchandiseListModel(QtCore.QAbstractListModel):
	items = []
	all_items = []
	last_filter_str = ""


	def __init__(self, items=[], parent=None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self.items = items
		self.all_items = items


	def rowCount(self, parent=QtCore.QModelIndex()):
		return len(self.items)


	#def columnCount(self, index=QModelIndex()):
	#	 return 1


	def data(self, index, role):
		if index.isValid() and role == QtCore.Qt.DisplayRole:
			item = self.items[index.row()]
			return QtCore.QVariant(item.__unicode__())
		else:
			return QtCore.QVariant()


	def filter(self, filter_str):
		"""Reduce items to only list those that match the filter_str

		"""
		if self.last_filter_str in filter_str:
			filter_items = self.items
		else:
			filter_items = self.all_items

		self.last_filter_str = filter_str
		self.items = [item for item in filter_items if item.filter(filter_str)]
		self.reset()


	def headerData(self, section, index,  role):
		return "WTF"


	def add(self, objects):
		self.items.extend(objects)
		self.items.sort()
		self.reset()


	def remove(self, objects):
		for o in objects:
			self.items.remove(o)
		self.reset()


	def setAllData(self, new_list):
		self.all_items = new_list
		self.items = new_list
		self.reset()


	def setData(self, new_list):
		"""replace old list with new list

		"""
		self.items = new_list
		self.reset()


