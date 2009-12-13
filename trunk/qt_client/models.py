# -*- coding: utf-8 -*-

from PyQt4.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt
class Item(): # TODO better name
	def __init__(self, name, price, ean):
		self.name = unicode(name)
		self.price = price
		self.ean = ean

	def getName(self):
		return u"%s - %d,-" % (self.name, self.price)


class MyListModel(QAbstractListModel):
	items = [] # array of Item(s)

	def __init__(self, parent=None, items=[]):
		QAbstractListModel.__init__(self, parent)
		self.items = items

	def rowCount(self, parent=QModelIndex()):
		return len(self.items)

	#def columnCount(self, index=QModelIndex()):
	#	 return 1

	def data(self, index, role):
		if index.isValid() and role == Qt.DisplayRole:
			item = self.items[index.row()]
			return QVariant(item.getName())
		else:
			return QVariant()

	def getItemsByName(self, names):
		ret = []
		for n in names:
			for i in self.items:
				if i.getName() == unicode(n):
					ret.append(i)
		print names
		return ret

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

	def setAllData(self, new):
		"""replace old list with new list"""
		self.items = new_list
		self.reset()
