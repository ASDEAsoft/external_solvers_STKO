## @package GuiUtils
# The GuiUtils packages contains utility functions commonly used by all tester widgets
# to promote code re-use

import traceback
import PyMpc
from PyMpc import MpcChartData
from PySide2.QtCore import (
	Qt,
	QLocale,
	)
from PySide2.QtGui import (
	QDoubleValidator,
	QKeySequence,
	QGuiApplication
	)
from PySide2.QtWidgets import (
	QVBoxLayout,
	QFrame,
	QLabel,
	QProgressBar,
	QStyledItemDelegate,
	QLineEdit,
	QTableWidget,
	)

# create a separator
def makeSeparator():
	s = QFrame()
	s.setFrameShape(QFrame.HLine)
	s.setFrameShadow(QFrame.Sunken)
	return s
	
# create a chart frame container
def makeChartFrame():
	f = QFrame()
	f.setStyleSheet(
		'.QFrame {\n'
		'background-color: rgb(255, 255, 255);\n'
		'border: 1px solid rgb(150, 150, 150);\n'
		'}'
		)
	f.setLayout(QVBoxLayout())
	f.layout().setContentsMargins(8,8,8,8)
	return f
	
# create a default and empty chart data
def makeChartData(name, xlabel, ylabel, id = 1):
	d = MpcChartData(id)
	d.name = name
	d.xLabel = xlabel
	d.yLabel = ylabel
	d.x.append(0.0)
	d.y.append(0.0)
	return d

# creates the default label for all tester widgets
def makeTesterLabel():
	label = QLabel(
		'<html><head/><body>'
		'<p align="center"><span style=" font-size:11pt; color:#003399;">'
		'Material Test'
		'</span></p>'
		'<p align="center"><span style=" color:#000000;">'
		'Here you can test your material. '
		'After defining material parameters, choose a strain history and run the test! '
		'Material response will show in the chart below.'
		'</span></p>'
		'<p align="center"><span style=" font-weight:600; font-style:italic; color:#000000;">'
		'Note'
		'</span>'
		'<span style=" font-style:italic; color:#000000;">'
		': to run the test you need to have at least one external solver kit properly set up.'
		'</span></p>'
		'</body></html>'
		)
	label.setWordWrap(True)
	return label

# creates a progress bar
def makeProgressBar():
	b = QProgressBar()
	b.setRange(0, 100)
	b.setValue(0)
	b.setTextVisible(True)
	return b

# custom double item delegate
class DoubleItemDelegate(QStyledItemDelegate):
	def __init__(self, parent=None):
		try:
			import sys
			super(DoubleItemDelegate, self).__init__(parent)
			self.top = sys.float_info.max
			self.bottom = -self.top
			self.decimals = 4
			self.edit_decimals = 12
			self.format = 'g'
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
	def displayText(self, value, locale):
		try:
			ia = int(value)
			na = 0
			if ia > 0:
				na = len(locale.toString(ia))
			return locale.toString(value, self.format, self.decimals+na)
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
			return "Error"
	def createEditor(self, parent, option, index):
		try:
			editor = QLineEdit(parent)
			editor.setValidator(QDoubleValidator(self.bottom, self.top, self.edit_decimals, editor))
			return editor
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
			return None

# custom table widget with copy features
class TableWidget(QTableWidget):
	def __init__(self, parent = None):
		super(TableWidget, self).__init__(parent)
	def keyPressEvent(self, event):
		super(TableWidget, self).keyPressEvent(event)
		try:
			if event.matches(QKeySequence.Copy):
				locale = QLocale()
				ranges = self.selectedRanges()
				if len(ranges) == 1:
					selection = ranges[0]
					data = '\n'.join(
						'\t'.join(locale.toString(self.item(i,j).data(Qt.DisplayRole)) 
							for j in range(selection.leftColumn(), selection.rightColumn()+1)) 
								for i in range(selection.topRow(), selection.bottomRow()+1))
					QGuiApplication.clipboard().setText(data)
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))