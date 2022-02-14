import sys
from PySide2.QtCore import (Signal, QTimer, Qt)
from PySide2.QtWidgets import (
	QLineEdit, QPushButton, QApplication, 
	QVBoxLayout, QHBoxLayout,
	QDialog, QTableWidget, QTabWidget, QGridLayout, 
	QWidget, QTableWidgetItem, QComboBox, QTreeWidget, QTreeWidgetItem, QAbstractItemView,
	QLabel, QSpinBox, QRadioButton, QSplitter)
from PySide2 import QtGui
import os
from STKODoubleItemDelegate import *

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

params = {
	'legend.fontsize': 'x-small',
	'axes.labelsize': 'x-small',
	'axes.titlesize':'x-small',
	'xtick.labelsize':'x-small',
	'ytick.labelsize':'x-small'
	}

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
			counter = -1 # start at -1 to account for the first header line
			while True:
				line = f.readline()
				if not line:
					break
				counter += 1
				if counter <= n0 and counter != 0:
					continue # skip lines already read
				# get line data
				data = [y for y in [x.strip() for x in line.split('\t')] if y ]
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

class STKOMonitorPlotWidget(QWidget):

	def __init__(self, parent=None):
		super(STKOMonitorPlotWidget, self).__init__(parent)
		# layout
		main_layout = QHBoxLayout()
		main_layout.setContentsMargins(0,0,0,0)
		right_layout = QVBoxLayout()
		left_layout = QVBoxLayout()
		self.setLayout(main_layout)
		
		# containers
		self.left_container = QWidget()
		self.left_container.setLayout(left_layout)
		self.right_container = QWidget()
		self.right_container.setLayout(right_layout)
		
		# canvas
		self.canvas = MyMplCanvas(self)
		
		# list of STKOPlotData
		self.data = {}
		
		# switches
		self.radio_single = QRadioButton('Single')
		self.radio_multi = QRadioButton('Multiple')
		
		# plot comboBox
		self.comboBox = QComboBox()
		
		# plot list
		self.tree = QTreeWidget()
		self.tree.setItemsExpandable(False)
		self.tree.setRootIsDecorated(False)
		self.tree.setHeaderHidden(True)
		self.tree_root = QTreeWidgetItem(["All"])
		self.tree_root.setFlags(self.tree_root.flags() | Qt.ItemIsAutoTristate)
		self.tree_root.setFlags(self.tree_root.flags() &~ Qt.ItemIsUserCheckable)
		self.tree.addTopLevelItem(self.tree_root)
		self.tree_root.setExpanded(True)
		self.tree.setEnabled(False)
		
		# random seed
		self.label_seed = QLabel('Random Seed:')
		self.seed = QSpinBox()
		self.seed.setMinimum(0)
		self.seed.setMaximum(1000000)
		self.seed.setMaximumWidth(100)
		self.canvas.seed = 73
		self.seed.setValue(self.canvas.seed)
		self.seed_cont = QWidget()
		self.seed_cont.setLayout(QHBoxLayout())
		self.seed_cont.layout().setContentsMargins(0,0,0,0)
		self.seed_cont.layout().addWidget(self.label_seed)
		self.seed_cont.layout().addWidget(self.seed)
		
		# timer
		self.timer = QTimer(self)
		self.timer.setInterval(1000) # each second
		
		# splitter
		self.splitter = QSplitter(Qt.Horizontal)
		
		# add to left layout
		left_layout.addWidget(self.canvas)
		left_layout.addWidget(NavigationToolbar(self.canvas, self))
		
		# add to right layout
		right_layout.addWidget(self.radio_single)
		right_layout.addWidget(self.comboBox)
		right_layout.addWidget(self.radio_multi)
		right_layout.addWidget(self.tree)
		self.radio_single.setChecked(True)
		right_layout.addWidget(self.seed_cont)
		
		# add to main layout
		self.splitter.addWidget(self.left_container)
		self.splitter.addWidget(self.right_container)
		self.splitter.setStretchFactor(0, 5)
		self.splitter.setStretchFactor(1, 1)
		main_layout.addWidget(self.splitter)
		
		# setup connections
		self.timer.timeout.connect(self.findPlotData)
		self.timer.timeout.connect(self.reloadPlotData)
		self.comboBox.currentIndexChanged.connect(self.onComboBoxIndexChanged)
		self.tree.itemClicked.connect(self.onTreeItemClicked)
		self.radio_single.toggled.connect(self.onSingleToggled)
		self.seed.valueChanged.connect(self.onSeedChanged)
		
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
			# remove from tree
			for i in range(self.tree_root.childCount()):
				item = self.tree_root.child(i)
				itemdata = item.data(0, Qt.UserRole)
				if key == itemdata:
					self.tree_root.removeChild(item)
					break
		#
		# add new data
		count_add = 0
		def_state = Qt.Unchecked
		if self.tree_root.childCount() == 0 or self.tree_root.checkState(0) == Qt.Checked:
			def_state = Qt.Checked
		for file in all_files:
			# skip files already detected
			if file in self.data:
				continue
			count_add += 1
			# create a plot item. Leave it empty, it will be read when necessary
			plot = STKOPlotDataItem(file)
			# create a plot bg item, if any... read it now because it is pre-computed by STKO
			bg_plot = None
			bg_file_name = '{}.pltbg'.format(os.path.splitext(file)[0])
			if os.path.exists(bg_file_name):
				bg_plot = STKOPlotDataItem(bg_file_name)
				bg_plot.load()
			# create a new data item mapped to this path
			idata = STKOPlotData(plot, bg_plot)
			self.data[file] = idata
			# upate combobox
			self.comboBox.addItem(plot.display_name, plot.file_name)
			# update tree
			node = QTreeWidgetItem([plot.display_name])
			node.setData(0, Qt.UserRole, plot.file_name)
			node.setFlags(node.flags() &~ Qt.ItemIsUserCheckable)
			node.setCheckState(0, def_state)
			self.tree_root.addChild(node)
		
		# data changed
		if len(to_rem) > 0 or count_add > 0:
			# reorder
			self.data = dict(sorted(self.data.items()))
			self.comboBox.model().sort(0, Qt.AscendingOrder)
			self.tree_root.sortChildren(0, Qt.AscendingOrder)
			# reset canvas
			self.prepareCanvas()
	
	def reloadPlotData(self, force_update=False):
		do_update = False
		if self.radio_single.isChecked():
			# single case
			current_key = self.comboBox.currentData()
			if current_key in self.data:
				current_data = self.data[current_key]
				nadd = 0
				if current_data.plot:
					nadd += current_data.plot.load()
				do_update = (nadd > 0)
		else:
			# multiple case
			nadd = 0
			for i in range(self.tree_root.childCount()):
				item = self.tree_root.child(i)
				if item.checkState(0) == Qt.Checked:
					current_key = item.data(0, Qt.UserRole)
					if current_key in self.data:
						current_data = self.data[current_key]
						if current_data.plot:
							nadd += current_data.plot.load()
			do_update = (nadd > 0)
		# done
		if do_update or force_update:
			self.canvas.updatePlot(self.data)
	
	def onComboBoxIndexChanged(self):
		if self.radio_single.isChecked():
			self.prepareCanvas()
			self.reloadPlotData(force_update=True)
	
	def onTreeItemClicked(self, item, column):
		if(item.checkState(column) == Qt.Unchecked):
			item.setCheckState(column, Qt.Checked)
		else:
			item.setCheckState(column, Qt.Unchecked)
		if self.radio_multi.isChecked():
			self.prepareCanvas()
			self.reloadPlotData(force_update=True)
	
	def onSingleToggled(self, checked):
		self.comboBox.setEnabled(checked)
		self.tree.setEnabled(not checked)
		self.prepareCanvas()
		self.reloadPlotData(force_update=True)
	
	def onSeedChanged(self, new_seed):
		self.canvas.seed = new_seed
		self.prepareCanvas(force = True)
		self.reloadPlotData(force_update=True)
	
	def prepareCanvas(self, force=False):
		keys = []
		if self.radio_single.isChecked():
			# single case
			current_key = self.comboBox.currentData()
			if current_key in self.data:
				keys.append(current_key)
		else:
			# multiple case
			for i in range(self.tree_root.childCount()):
				item = self.tree_root.child(i)
				if item.checkState(0) == Qt.Checked:
					itemdata = item.data(0, Qt.UserRole)
					if itemdata in self.data:
						keys.append(itemdata)
		# done
		self.canvas.prepare(keys, force)
	
class MyMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		# base initialization
		fig = Figure(figsize=(width, height), dpi=dpi)
		FigureCanvas.__init__(self, fig)
		# setup
		self.control = parent
		self.figure = fig
		plt.rcParams.update(params)
		# we want just 1 subplot
		self.subplot = fig.add_subplot(111)
		self.subplot.grid(linestyle=':')
		self.subplot.plot()
		# data (map plot names to plots)
		self.keymap = {}
		self.seed = 0
		# done
		self.setParent(parent)
		FigureCanvas.updateGeometry(self)
	
	def prepare(self, keys, force=False):
		import random
		import colorsys
		if list(self.keymap.keys()) != keys or force:
			self.subplot.clear()
			self.subplot.grid(linestyle=':')
			self.keymap.clear()
			random.seed(self.seed)
			for key in keys:
				# random colors from 0 to 1
				h = random.gauss(0.653, 0.25)
				c1 = colorsys.hls_to_rgb(h, 0.45, 0.6)
				c2 = colorsys.hls_to_rgb(h, 0.65, 0.5)
				# 1 plot and 1 background for each key
				plot = self.subplot.plot([],[], color=c1, linestyle='-', linewidth=1.5)[0]
				bg_plot = self.subplot.plot([],[], color=c2, linestyle='--', linewidth=1.0)[0]
				# map it
				self.keymap[key] = (plot, bg_plot)
			self.subplot.plot()
	
	def updatePlot(self, all_data):
		# auxiliary function
		def aux(plot, bg_plot, data, set_labels):
			items = (
				(plot, data.plot, data.plot.display_name), 
				(bg_plot, data.bg_plot, '{} (Background)'.format(data.plot.display_name)))
			for item in items:
				plot = item[0]
				plot_data = item[1]
				label = item[2]
				if plot_data is not None:
					plot.set_xdata(plot_data.x)
					plot.set_ydata(plot_data.y)
					if set_labels:
						self.subplot.set_xlabel(plot_data.xLabel)
						self.subplot.set_ylabel(plot_data.yLabel)
					plot.set_label(label)
				else:
					plot.set_xdata([])
					plot.set_ydata([])
					plot.set_label('_nolegend_')
		# process all
		counter = 0
		for key, data in all_data.items():
			if key in self.keymap:
				plot, bg_plot = self.keymap[key]
				aux(plot, bg_plot, data, (counter == 0))
				counter += 1
		# bounds
		self.subplot.relim()
		self.subplot.autoscale_view()
		# done
		if counter > 0:
			self.subplot.legend()
		self.draw()