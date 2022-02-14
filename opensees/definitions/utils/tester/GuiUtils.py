## @package GuiUtils
# The GuiUtils packages contains utility functions commonly used by all tester widgets
# to promote code re-use

from PyMpc import MpcChartData
from PySide2.QtWidgets import (
	QVBoxLayout,
	QFrame,
	QLabel,
	QProgressBar
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

# creates a progress bar
def makeProgressBar():
	b = QProgressBar()
	b.setRange(0, 100)
	b.setValue(0)
	b.setTextVisible(True)
	return b
