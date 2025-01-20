from PySide2.QtCore import Qt
from PySide2.QtGui import QDoubleValidator, QColor
from PySide2.QtWidgets import (
	QTableWidget,
	QTableWidgetItem,
	QStyledItemDelegate,
	QLineEdit,
	QColorDialog
)
import sys

class _DoubleDelegate(QStyledItemDelegate):
	def __init__(self, parent = None):
		super(_DoubleDelegate, self).__init__(parent = parent)
	def displayText(self, value, locale):
		a = value.toDouble()
		ia = int(a)
		na = 0
		if ia > 0:
			na = len(locale.toString(ia))
		return locale.toString(a, 'g', 6+na) # 6 decimals
	def createEditor(self, parent, option, index):
		editor = QLineEdit(parent)
		editor.setValidator(QDoubleValidator(-sys.float_info.max, sys.float_info.max, 12, editor))
		return editor

class _ColorDelegate(QStyledItemDelegate):
	def __init__(self, parent = None):
		super(_ColorDelegate, self).__init__(parent = parent)
	def paint(self, painter, option, index):
		color = index.model().data(index, Qt.EditRole)
		painter.save()
		painter.fillRect(option.rect, color)
		painter.restore()
	def createEditor(parent, option, index):
		editor = QColorDialog(parent)
		editor.setOptions(QColorDialog.ShowAlphaChannel)
		return editor
	def setEditorData(self, editor, index):
		color = index.model().data(index, Qt.EditRole)
		editor.setCurrentColor(color)
	def setModelData(self, editor, model, index):
		model.setData(index, editor.currentColor(), Qt.EditRole)

'''
# SERIAL_NUMBER PART_NUMBER COORD_X COORD_Y COORD_Z X1 X2 X3 Y1 Y2 Y3 R G B
'''
class MonStrNodeWidget(QTableWidget):
	def __init__(self, parent = None):
		super(MonStrNodeWidget, self).__init__(parent = parent)
		# set up columns and labels
		self.setColumnCount(12)
		self.setHorizontalHeaderLabels([
			'Serial Number', 'Part Number',
			'X', 'Y', 'Z',
			'vX1', 'vX2', 'vX3',
			'vY1', 'vY2', 'vY3',
			'Color'
			])
		for i in range(2):
			self.setColumnWidth(i, 100)
		for i in range(2, 12):
			self.setColumnWidth(i, 60)
		# delegates
		ddel = _DoubleDelegate()
		cdel = _ColorDelegate()
		for i in range(2, 11):
			self.setItemDelegateForColumn(i, ddel)
		#self.setItemDelegateForColumn(11, cdel)
		# try fill
		locale = self.locale()
		self.setRowCount(1)
		self.setItem(0, 0, self._def_item('Serial'))
		self.setItem(0, 1, self._def_item('Part'))
		for i in range(2, 11):
			self.setItem(0, i, self._edit_item(i+0.1))
		self.setItem(0, 11, self._edit_item(QColor(Qt.red)))
	def _def_item(self, value):
		return QTableWidgetItem(value)
	def _edit_item(self, value):
		item = QTableWidgetItem()
		item.setData(Qt.DisplayRole, value)
		return item
	