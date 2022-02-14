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

# create a horizontal separator
def makeHSeparator():
	s = QFrame()
	s.setFrameShape(QFrame.HLine)
	s.setFrameShadow(QFrame.Sunken)
	return s
	
# create a vertical separator
def makeVSeparator():
	s = QFrame()
	s.setFrameShape(QFrame.HLine)
	s.setFrameShadow(QFrame.Sunken)
	return s
	