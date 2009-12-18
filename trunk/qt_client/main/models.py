# -*- coding: utf-8 -*-
from PyQt4.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt


class MerchandiseListModel(QAbstractListModel):
	items = []
	all_items = []
	last_filter_str = ""


	def __init__(self, parent=None, items=[]):
		QAbstractListModel.__init__(self, parent)
		self.items = items
		self.all_items = items


	def rowCount(self, parent=QModelIndex()):
		return len(self.items)


	#def columnCount(self, index=QModelIndex()):
	#	 return 1


	def data(self, index, role):
		if index.isValid() and role == Qt.DisplayRole:
			item = self.items[index.row()]
			return QVariant(item.__unicode__())
		else:
			return QVariant()


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
		"""replace old list with new list

		"""
		self.items = new_list
		self.reset()

