import sys
import traceback
from PySide2.QtCore import (Signal, QTimer, Qt, QLocale)
from PySide2.QtWidgets import (
	QLineEdit, QPushButton, QApplication,
	QVBoxLayout, QHBoxLayout,
	QDialog, QTableWidget, QTabWidget, QGridLayout,
	QWidget, QTableWidgetItem, QComboBox, QTreeWidget, QTreeWidgetItem, QAbstractItemView,
	QLabel, QSpinBox, QRadioButton, QSplitter)
from PySide2 import QtGui
import os
from STKODoubleItemDelegate import *
from numpy import arange, sin, pi
import numpy as np


# custom table widget with copy features
class TableWidget(QTableWidget):
	def __init__(self, parent=None):
		super(TableWidget, self).__init__(parent)

	def keyPressEvent(self, event):
		super(TableWidget, self).keyPressEvent(event)
		try:
			if event.matches(QtGui.QKeySequence.Copy):
				locale = QLocale()
				ranges = self.selectedRanges()
				if len(ranges) == 1:
					selection = ranges[0]
					data = '\n+'.join(
						'\t+'.join(locale.toString(self.item(i, j).data(Qt.DisplayRole))
								   for j in range(selection.leftColumn(), selection.rightColumn() + 1))
						for i in range(selection.topRow(), selection.bottomRow() + 1))
					QtGui.QGuiApplication.clipboard().setText(data)
		except:
			exdata = traceback.format_exc().splitlines()


class STKOPlotDataItem:
	def __init__(self, fname):
		self.file_name = fname
		self.display_name = os.path.splitext(os.path.basename(fname))[0]
		self.x = []
		self.y = []
		self.xmax = 0.0
		self.xmin = 0.0
		self.ymax = 0.0
		self.ymin = 0.0
		self.xLabel = ''
		self.yLabel = ''

	def load(self):
		'''
		loads the contents of file self.file_name.
		it does it incrementally loading only new data.
		returns the number of lines added
		'''
		if not os.path.exists(self.file_name):
			return 0
		n0 = len(self.x)
		with open(self.file_name, 'r') as f:
			counter = -1  # start at -1 to account for the first header line
			while True:
				line = f.readline()
				if not line:
					break
				counter += 1
				if counter <= n0 and counter != 0:
					continue  # skip lines already read
				# get line data
				data = [y for y in [x.strip() for x in line.split('\t')] if y]
				n = len(data)
				if counter == 0:
					# read first header line for axis labels
					if n > 0: self.xLabel = data[0]
					if n > 1: self.yLabel = data[1]
				else:
					# read plot values
					x = float(data[0]) if n > 0 else 0.0
					y = float(data[1]) if n > 1 else 0.0
					self.x.append(x)
					self.y.append(y)
					# accumulate min/max
					if len(self.x) == 1:
						self.xmin = x
						self.xmax = x
						self.ymin = y
						self.ymax = y
					else:
						self.xmin = min(self.xmin, x)
						self.xmax = max(self.xmax, x)
						self.ymin = min(self.ymin, y)
						self.ymax = max(self.ymax, y)
		# return true if some lines were added
		return len(self.x) - n0


class STKOPlotData:
	def __init__(self, plot, bg_plot):
		self.plot = plot
		self.bg_plot = bg_plot

class STKODataWidget(QWidget):

	def __init__(self, parent=None):
		super(STKODataWidget, self).__init__(parent)
		# layout
		main_layout = QHBoxLayout()
		main_layout.setContentsMargins(0, 0, 0, 0)
		unique_layout = QVBoxLayout()
		self.setLayout(main_layout)

		# containers
		self.unique_container = QWidget()
		self.unique_container.setLayout(unique_layout)

		# list of STKOPlotData
		self.data = {}
		self.keymap = {}

		# plot comboBox
		self.comboBox = QComboBox()

		# Define Members:
		# table
		self.unique_container.table = TableWidget()
		self.unique_container.table.setItemDelegate(STKODoubleItemDelegate(self.unique_container.table))
		self.unique_container.table.setColumnCount(2)
		self.reloadPlotData()

		# timer
		self.timer = QTimer(self)
		self.timer.setInterval(1000)  # each second

		# add to layout
		unique_layout.addWidget(self.comboBox)
		self.unique_container.layout().addWidget(self.unique_container.table)

		# splitter
		self.splitter = QSplitter(Qt.Vertical)

		# add to main layout
		self.splitter.addWidget(self.unique_container)
		self.splitter.setStretchFactor(0, 5)
		self.splitter.setStretchFactor(1, 1)
		main_layout.addWidget(self.splitter)

		# setup connections
		self.timer.timeout.connect(self.findPlotData)
		self.timer.timeout.connect(self.reloadPlotData)
		self.comboBox.currentIndexChanged.connect(self.onComboBoxIndexChanged)

		# start timer
		self.timer.start()

	def findPlotData(self):
		# check each file in the current directory
		all_files = []
		for root, subdirs, files in os.walk(os.getcwd()):
			for file in files:
				if file.endswith(".plt"):
					all_files.append(os.path.join(root, file))
		#
		# remove data not available anymore
		to_rem = []
		for key, data in self.data.items():
			if key not in all_files:
				to_rem.append(key)
		for key in to_rem:
			# remove from data
			del self.data[key]
			# remove from combo box
			for i in range(self.comboBox.count()):
				itemdata = self.comboBox.itemData(i)
				if key == itemdata:
					self.comboBox.removeItem(i)
					break
		#
		# add new data
		count_add = 0
		def_state = Qt.Unchecked
		for file in all_files:
			# skip files already detected
			if file in self.data:
				continue
			count_add += 1
			# create a plot item. Leave it empty, it will be read when necessary
			plot = STKOPlotDataItem(file)
			# create a plot bg item, if any... read it now because it is pre-computed by STKO
			bg_plot = None
			# create a new data item mapped to this path
			idata = STKOPlotData(plot, bg_plot)
			self.data[file] = idata
			# upate combobox
			self.comboBox.addItem(plot.display_name, plot.file_name)

		# data changed
		if len(to_rem) > 0 or count_add > 0:
			# reorder
			self.data = dict(sorted(self.data.items()))
			self.comboBox.model().sort(0, Qt.AscendingOrder)

	def reloadPlotData(self, force_update=False):
		do_update = False
		# single case
		current_key = self.comboBox.currentData()
		if current_key in self.data:
			current_data = self.data[current_key]
			nadd = 0
			if current_data.plot:
				nadd += current_data.plot.load()
			do_update = (nadd > 0)
		# done
		if do_update or force_update:
			self.updateTable(self.data)

	def onComboBoxIndexChanged(self):
		self.prepareTable()
		self.reloadPlotData(force_update=True)

	def prepareTable(self, force=False):
		keys = []
		current_key = self.comboBox.currentData()
		if current_key in self.data:
			keys.append(current_key)
		# done
		self.prepare(keys, force)

	def prepare(self, keys, force=False):
		import random
		import colorsys
		if list(self.keymap.keys()) != keys or force:
			self.keymap.clear()
			for key in keys:
				# 1 plot and 1 background for each key
				plot = self.data
				bg_plot = self.data
				# map it
				self.keymap[key] = (plot, bg_plot)

	def updateTable(self, all_data):
		# auxiliary function
		self.unique_container.table.setRowCount(0)

		def aux(plot, bg_plot, data, set_labels):
			items = (
				(plot, data.plot, data.plot.display_name),
				(bg_plot, data.bg_plot, '{} (Background)'.format(data.plot.display_name)))
			for item in items:
				plot = item[0]
				plot_data = item[1]
				if plot_data is not None:
					if set_labels:
						self.unique_container.table.setHorizontalHeaderLabels([plot_data.xLabel, plot_data.yLabel])
						self.unique_container.table.resizeColumnsToContents()

						def make_item(value):
							iy = QTableWidgetItem()
							iy.setData(Qt.DisplayRole, value)
							return iy

						for rowPosition in range(len(plot_data.x)):
							# insert a new row
							self.unique_container.table.insertRow(rowPosition)
							# first column is the stage id
							self.unique_container.table.setItem(rowPosition, 0,
															  make_item(plot_data.x[rowPosition]))
							self.unique_container.table.setItem(rowPosition, 1,
															  make_item(plot_data.y[rowPosition]))

		# process all
		counter = 0
		for key, data in all_data.items():
			if key in self.keymap:
				plot, bg_plot = self.keymap[key]
				aux(plot, bg_plot, data, (counter == 0))
				counter += 1
