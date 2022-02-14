import sys
from PySide2.QtWidgets import (QLineEdit, QStyledItemDelegate)
from PySide2.QtGui import (QDoubleValidator)

class STKODoubleItemDelegate(QStyledItemDelegate):

	def __init__(self, parent=None):
		super(STKODoubleItemDelegate, self).__init__(parent)
		
		# Define Members:
		self.bottom = -sys.float_info.max
		self.top = sys.float_info.max
		self.decimals = 6
		self.edit_decimals = 12
		self.format = 'g'
		self.is_percentage = False
		
	def displayText(self, value, locale):
		a = float(value)
		if self.is_percentage:
			return "{} %".format(locale.toString(a*100.0, self.format, self.decimals))
		else:
			return locale.toString(a, self.format, self.decimals)
	
	def createEditor(self, parent, option, index):
		editor = QLineEdit(parent)
		editor.setValidator(QDoubleValidator(self.bottom, self.top, self.decimals, editor))
		return editor

