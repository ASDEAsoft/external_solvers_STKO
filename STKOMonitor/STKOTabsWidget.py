from STKODataWidget import *
from STKOMonitorPlotWidget import *
from PySide2.QtWidgets import (QTabWidget, QGridLayout)

class STKOTabsWidget(QTabWidget):
	def __init__(self, parent=None):
		super(STKOTabsWidget, self).__init__(parent)
		# Statistics
		self.monitor_tab()
		self.data_tab()
	def monitor_tab(self):
		# Plots
		plot = STKOMonitorPlotWidget()
		grid_tab = QGridLayout()
		plot.setLayout(grid_tab)
		self.addTab(plot, "Analysis Plots")
	def data_tab(self):
		# Plots
		plot = STKODataWidget()
		grid_tab = QGridLayout()
		plot.setLayout(grid_tab)
		self.addTab(plot, "Data")
