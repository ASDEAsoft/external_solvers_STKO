import sys
from PySide2.QtCore import (Signal, QTimer)
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QTableWidget, QTabWidget, QGridLayout, QWidget, QTableWidgetItem, QCheckBox)
from PySide2 import QtGui
import os
from STKODoubleItemDelegate import *

class STKOMonitorStatisticsWidget(QWidget):

	def __init__(self, parent=None):
		super(STKOMonitorStatisticsWidget, self).__init__(parent)
		# layout
		self.setLayout(QVBoxLayout())
		
		# Define Members:
		# cbox_autoscroll
		self.cbox_autoscroll = QCheckBox()
		self.cbox_autoscroll.setText("Auto-Scroll")
		self.cbox_autoscroll.setChecked(True)
		self.cbox_autoscroll.setToolTip("Auto-Scroll. If checked, the statistics table will automatically scroll to the bottom line")
		# table
		self.table = QTableWidget(0,7)
		self.table.setHorizontalHeaderLabels(["Stage ID", "Step ID", "dT", "Time", "Iterations"," Norm", "Perc[%]"])
		self.delegate = STKODoubleItemDelegate()
		self.delegate_perc = STKODoubleItemDelegate()
		self.delegate_perc.is_percentage = True
		#self.table.setItemDelegate(self.delegate)
		self.table.setItemDelegateForColumn(1, self.delegate)
		self.table.setItemDelegateForColumn(2, self.delegate)
		self.table.setItemDelegateForColumn(3, self.delegate)
		self.table.setItemDelegateForColumn(4, self.delegate)
		self.table.setItemDelegateForColumn(5, self.delegate)
		self.table.setItemDelegateForColumn(6, self.delegate_perc)
		
		self.current_step_id = 0
		self.current_stage_id = 1
		
		# timer
		self.timer = QTimer(self)
		self.timer.setInterval(1000) # each second
		
		# add to layout
		self.layout().addWidget(self.cbox_autoscroll)
		self.layout().addWidget(self.table)
		
		# setup connections
		self.timer.timeout.connect(self.updateStatistics)
		
		# start timer
		self.timer.start()
		
	def updateStatistics(self):
		# check file
		fname = '{}/STKO_monitor_statistics.stats'.format(os.getcwd())
		if not os.path.exists(fname):
			return
		with open(fname) as stat:
			line_counter = 0
			while True:
				line = stat.readline()
				if(not line):
					break
				line_counter += 1
				rowPosition = self.table.rowCount()
				if line_counter > rowPosition:
					# split and check words
					words = [y for y in [x.strip() for x in line.split(' ')] if y ]
					nkey = len(words)
					if nkey != 6:
						return
					
					# get current step id
					previous_step_id = self.current_step_id
					self.current_step_id = int(words[0])
					if self.current_step_id < previous_step_id:
						# this means a new stage started
						self.current_stage_id += 1
					
					# insert a new row
					self.table.insertRow(rowPosition)
					# first column is the stage id
					self.table.setItem(rowPosition, 0, QTableWidgetItem(str(self.current_stage_id)))
					# insert words for other columns
					for i in range(len(words)):
						self.table.setItem(rowPosition, i+1, QTableWidgetItem(words[i]))
		# make sure the last item is visible
		if self.cbox_autoscroll.isChecked():
			self.table.scrollToBottom()



