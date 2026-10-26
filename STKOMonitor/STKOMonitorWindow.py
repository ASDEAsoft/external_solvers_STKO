from STKOMonitorStatisticsWidget import *
from STKOMonitorTimerWidget import *
from STKOTabsWidget import *
import sys
from PySide2.QtWidgets import (QVBoxLayout, QMainWindow, QDockWidget, QWidget, QTabWidget, QTabBar, QStyle)
from PySide2.QtCore import Qt

class STKOMonitorWindow(QMainWindow):

	def __init__(self, parent=None):
		super(STKOMonitorWindow, self).__init__(parent)
		self.setWindowTitle("STKO Monitor")
		
		# central
		central_widget = QWidget()
		central_widget.setLayout(QVBoxLayout())
		# the tabs keep the same margin from the window as the Statistics dock
		# above them; none at the bottom, where the timer brings its own
		m = self.style().pixelMetric(QStyle.PM_LayoutLeftMargin)
		central_widget.layout().setContentsMargins(m, m, m, 0)
		self.setCentralWidget(central_widget)
		
		# tabs
		self.tab = STKOTabsWidget()
		central_widget.layout().addWidget(self.tab)
		
		# timer
		self.timer = STKOMonitorTimerWidget()
		central_widget.layout().addWidget(self.timer)
		
		# stat widget
		self.stats_dock = QDockWidget("Statistics")
		self.stats_dock.setAllowedAreas(Qt.TopDockWidgetArea)
		self.stats = STKOMonitorStatisticsWidget()
		self.stats_dock.setWidget(self.stats)
		self.addDockWidget(Qt.TopDockWidgetArea, self.stats_dock)
		
		# resize
		self.resize(780, 720)
		


