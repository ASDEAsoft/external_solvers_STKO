import sys
from PySide2.QtCore import (Signal, QTimer)
from PySide2.QtWidgets import (QHBoxLayout, QWidget, QLabel)
from PySide2 import QtGui
import os

class STKOMonitorTimerWidget(QWidget):

	def __init__(self, parent=None):
		super(STKOMonitorTimerWidget, self).__init__(parent)
		# layout
		self.setLayout(QHBoxLayout())
		
		# Define Members:
		self.label = QLabel()
		self.label.setText('Elapsed Time [d : hh:mm:ss] = {} : {:02d}:{:02d}:{:02d}'.format(0, 0, 0, 0))
		
		# add to layout
		self.layout().addWidget(self.label)
		
		# timer
		self.timer = QTimer(self)
		self.timer.setInterval(1000) # each second
		
		# setup connections
		self.timer.timeout.connect(self.updateTime)
		
		# start timer
		self.timer.start()
		
	def updateTime(self):
		# check file
		fname = '{}/STKO_time_monitor.tim'.format(os.getcwd())
		if not os.path.exists(fname):
			return
		with open(fname) as f:
			t = f.read().splitlines()
			n = len(t)
			t0 = int(t[0]) if n > 0 else 0
			t1 = int(t[1]) if n > 1 else t0
			# times are in seconds
			dt = t1 - t0
			# format
			seconds = dt%60
			dt -= seconds
			minutes = int((dt/60)%60)
			dt -= minutes*60
			hours = int((dt/60/60)%24)
			dt -= hours*60*60
			days = int(dt/60/60/24)
			# write
			self.label.setText('Elapsed Time [d : hh:mm:ss] = {} : {:02d}:{:02d}:{:02d}'.format(days, hours, minutes, seconds))



