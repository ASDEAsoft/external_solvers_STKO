from STKODataWidget import *
from STKOMonitorPlotWidget import *
from STKOMonitorEnergyWidget import STKOMonitorEnergyWidget
from PySide2.QtWidgets import (QTabWidget, QGridLayout)

class STKOTabsWidget(QTabWidget):
	def __init__(self, parent=None):
		super(STKOTabsWidget, self).__init__(parent)
		# Statistics
		self.monitor_tab()
		self.data_tab()
		self.energy_tab()
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
	def energy_tab(self):
		# Energy balance: shown once a balance file (.ebal) is found
		self.energy = STKOMonitorEnergyWidget()
		self.energy.filesChanged.connect(self.onEnergyFilesChanged)
	def onEnergyFilesChanged(self, count):
		index = self.indexOf(self.energy)
		if count > 0 and index < 0:
			self.addTab(self.energy, "Energy Balance")
		elif count == 0 and index >= 0:
			self.removeTab(index)
