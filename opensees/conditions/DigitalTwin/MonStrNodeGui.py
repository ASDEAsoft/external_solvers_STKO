from PySide2.QtCore import Qt, Slot, Signal
from PySide2.QtGui import QDoubleValidator, QColor
from PySide2.QtWidgets import (
	QWidget,
	QGridLayout,
	QTableWidget,
	QTableWidgetItem,
	QStyledItemDelegate,
	QLineEdit,
	QColorDialog,
	QSpinBox,
)
import sys

class _DoubleDelegate(QStyledItemDelegate):
	def __init__(self, parent = None):
		super(_DoubleDelegate, self).__init__(parent = parent)
	def displayText(self, value, locale):
		"""Shows the text while not editing, with fewer (6) decimals."""
		ia = int(value)
		na = len(locale.toString(ia)[0]) if ia > 0 else 0
		return f"{value:.{6+na}g}"
	def setEditorData(self, editor, index):
		"""Sets the editor with the current model data with full 12 decimals."""
		value = index.model().data(index, role=Qt.DisplayRole)
		if isinstance(value, (int, float)):
			editor.setText(f"{value:.12g}")  # Format text to the correct decimal places
	def setModelData(self, editor, model, index):
		"""Saves the edited value back to the model."""
		text = editor.text()
		try:
			value = float(text)
			model.setData(index, value, role=Qt.DisplayRole)
		except ValueError:
			pass  # Ignore invalid input
	def createEditor(self, parent, option, index):
		"""Sets a QLineEdit with a QDoubleValidator (with 12 decimals) as editor."""
		editor = QLineEdit(parent)
		editor.setValidator(QDoubleValidator(-sys.float_info.max, sys.float_info.max, 12, editor))
		return editor

class _ColorDelegate(QStyledItemDelegate):
	def __init__(self, parent = None):
		super(_ColorDelegate, self).__init__(parent = parent)
	def paint(self, painter, option, index):
		""" Paint the cell background with the stored QColor """
		if index.isValid():
			color = index.data(Qt.UserRole)  # Expecting a QColor object
			if isinstance(color, QColor):
				painter.fillRect(option.rect, color)  # Fill background with color
		# Call base class paint for text and other properties
		super().paint(painter, option, index)
	def createEditor(self, parent, option, index):
		""" Open QColorDialog to pick a color """
		color = index.data(Qt.UserRole)  # Get current color
		if not isinstance(color, QColor):
			color = QColor(Qt.white)  # Default color if invalid
		new_color = QColorDialog.getColor(color, parent, "Select Color")
		if new_color.isValid():
			self.commitData.emit(parent)
			self.closeEditor.emit(parent, Qt.UserRole)
			index.model().setData(index, new_color, Qt.UserRole)  # Update model data
		return None  # No need to create a persistent editor
	def setEditorData(self, editor, index):
		""" Not needed since we handle editing inline """
		pass
	def setModelData(self, editor, model, index):
		""" Not needed since we set data in createEditor() """
		pass

'''
# SERIAL_NUMBER PART_NUMBER COORD_X COORD_Y COORD_Z X1 X2 X3 Y1 Y2 Y3 R G B
'''
class MonStrTableNodeWidget(QTableWidget):
	def __init__(self, xobj, parent = None):
		super(MonStrTableNodeWidget, self).__init__(parent = parent)
		# set xobj
		self.xobj = xobj
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
		ddel = _DoubleDelegate(self)
		cdel = _ColorDelegate(self)
		for i in range(2, 11):
			self.setItemDelegateForColumn(i, ddel)
		self.setItemDelegateForColumn(11, cdel)
		# fill
		self.fillFromXObject()
	def _def_item(self, value):
		return QTableWidgetItem(value)
	def _disp_item(self, value):
		item = QTableWidgetItem()
		item.setData(Qt.DisplayRole, value)
		return item
	def _user_item(self, value):
		item = QTableWidgetItem()
		item.setData(Qt.UserRole, value)
		return item
	def _demo(self):
		self.setRowCount(1)
		self.setItem(0, 0, self._def_item('Serial'))
		self.setItem(0, 1, self._def_item('Part'))
		for i in range(2, 11):
			self.setItem(0, i, self._disp_item(i+0.1))
		self.setItem(0, 11, self._user_item(QColor(Qt.red)))
	def _get_attributes(self):
		ser = self.xobj.getAttribute('SerialNumber').stringVector
		par = self.xobj.getAttribute('PartNumber').stringVector
		pos = self.xobj.getAttribute('Position').quantityMatrix
		dx = self.xobj.getAttribute('XDirection').quantityMatrix
		dy = self.xobj.getAttribute('YDirection').quantityMatrix
		col = self.xobj.getAttribute('Color').quantityMatrix
		return (ser, par, pos, dx, dy, col)
	@Slot()
	def fillFromXObject(self):
		ser, par, pos, dx, dy, col = self._get_attributes()
		N = len(ser)
		print('found {} sensors ...'.format(N))
	@Slot(int)
	def updateSensorCount(self, new_count):
		print(new_count)
		ser, par, pos, dx, dy, col = self._get_attributes()
		N = len(ser)
		try:
			if new_count < N:
				ser = ser[:new_count]
				par = par[:new_count]
				self.xobj.getAttribute('SerialNumber').stringVector = ser
				self.xobj.getAttribute('PartNumber').stringVector = par
			else:
				for i in range(N, new_count):
					ser.append('Serial')
					par.append('Part')
			pos.resize(new_count, 3)
			dx.resize(new_count, 3)
			dy.resize(new_count, 3)
			col.resize(new_count, 3)
		except Exception as ex:
			print(ex)

'''
The compound widget
'''
class MonStrNodeWidget(QWidget):
	def __init__(self, xobj, parent = None):
		super(MonStrNodeWidget, self).__init__(parent = parent)
		# store xobj
		self.xobj = xobj
		# set up sub widgets
		self.spin_number = QSpinBox(self)
		self.spin_number.setRange(0, 1000000)
		self.table = MonStrTableNodeWidget(xobj, parent = self)
		# layout
		lay = QGridLayout()
		lay.setContentsMargins(0,0,0,0)
		row = 0
		lay.addWidget(self.spin_number, row, 0, 1, 1)
		row += 1
		lay.addWidget(self.table, row, 0, 1, 1)
		row += 1
		# done
		self.setLayout(lay)
		# connections
		self.spin_number.valueChanged.connect(self.table.updateSensorCount)