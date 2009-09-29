from PyQt4.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt

class MyListModel(QAbstractListModel):
	words = [] # TODO utvid til navn, pris og ean

	def __init__(self, parent=None, words=[]):
		QAbstractListModel.__init__(self, parent)
		self.words = words

	def rowCount(self, parent=QModelIndex()):
		return len(self.words)

	#def columnCount(self, index=QModelIndex()):
	#	 return 1

	def data(self, index, role):
		if index.isValid() and role == Qt.DisplayRole:
			return QVariant(self.words[index.row()])
		else:
			return QVariant()

	def  headerData(self, section, index,  role):
		return "WTF"

	def add(self, objects):
		self.words.extend(objects)
		self.words.sort()
		self.reset()

	def remove(self, objects):
		for o in objects:
			self.words.remove(o)
		self.reset()

	def setAllData(self, new_list):
		"""replace old list with new list"""
		self.words = new_list
		self.reset()
