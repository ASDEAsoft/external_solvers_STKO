## @package Tester1D
# The Tester1D packages contains the tester and widget classes that are used
# to run a test of a uniaxial material

import subprocess
import os
import sys
import traceback
from io import StringIO
import json

import PyMpc
import PyMpc.App
import PyMpc.Math
import PyMpc.Units
from PyMpc.Units import MpcQuantityVector
from PyMpc import *

import opensees.utils.tcl_input as tclin
import opensees.utils.write_definitions as write_definitions
import opensees.utils.Gui.GuiUtils as gu
import opensees.definitions.utils.tester.TesterUtils as tu

from PySide2.QtCore import (
	QObject,
	Signal,
	Slot,
	QSignalBlocker,
	QLocale,
	QCoreApplication,
	QTimer,
	)
from PySide2.QtGui import (
	QDoubleValidator
	)
from PySide2.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QGridLayout,
	QHBoxLayout,
	QLabel,
	QSplitter,
	QPushButton,
	QComboBox,
	QSpinBox,
	QDoubleSpinBox,
	QLineEdit,
	QToolBar,
	QDialog,
	QFileDialog,
	QMessageBox,
	QSizePolicy
	)
import shiboken2

# creates the default label for Distribution tester widgets
def makeDistributionTesterLabel():
	label = QLabel(
		'<html><head/><body>'
		'<p align="center"><span style=" font-size:11pt; color:#003399;">'
		'Test Distribution'
		'</span></p>'
		'<p align="center"><span style=" color:#000000;">'
		'Here you can test your randomVariable. '
		'After defining randomVariable run the test! '
		'Material response will show in the charts below.'
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

## The Tester1D class class perform an async call to a new process
# that runs opensees and communicate with it in real time. we don't want the gui to freeze,
# so we do this operation in a worker thread
class TesterDistribution(QObject):

	# a signal to notify that we have
	# the new components of x, pdf and CDF
	testProcessUpdated = Signal(float, float, float, float)

	# create a new TesterDistribution passing as arguments
	# definition and a list of xs.
	def __init__(self, randomVariable, div, parent = None):
		# base class initialization
		super(TesterDistribution, self).__init__(parent)
		# self initialization
		self.randomVariable = randomVariable
		self.div = div
		self.x = []
		self.pdf = [] # pdf f
		self.cdf = [] # CDF F

	# prepares data for testing and returns the command to run
	# and the names of temporary files
	def __prepare_test(self):

		# some initial checks
		if self.randomVariable is None:
			raise Exception("No randomVariable provided to the tester")

		# make sure we have at least one OpenSEES installed and set to the STKO kits!
		opensees_cmd = PyMpc.App.currentSolverCommand()
		if not opensees_cmd:
			raise Exception("No external solver kit provided")

		# temporary directory
		temp_dir = '{}{}TesterDistribution'.format(MpcStandardPaths.getStandardPathDataLocation(), os.sep)
		temp_dir = temp_dir.replace('\\','/')
		if not os.path.exists(temp_dir):
			os.makedirs(temp_dir)
		print('Working directory: "{}"'.format(temp_dir))

		# temporary tcl script file
		temp_script = 'script.tcl'
		temp_script_file = '{}{}{}'.format(temp_dir, os.sep, temp_script)
		temp_script_file = temp_script_file.replace('\\','/')
		print('Script file: "{}"'.format(temp_script_file))

		# temporary txt output file
		temp_output = 'output.txt'
		temp_output_file = '{}{}{}'.format(temp_dir, os.sep, temp_output)
		temp_output_file = temp_output_file.replace('\\','/')
		print('Output file: "{}"'.format(temp_output_file))

		# create process info
		pinfo = tclin.process_info()
		pinfo.out_dir = temp_dir

		# get template
		template_filename = '{}/template_distribution.tcl'.format(os.path.dirname(__file__))
		template_file = open(template_filename, 'r')
		template = template_file.read()
		template_file.close()

		# write randomVariable
		buffer_randomVariable = StringIO()
		pinfo.out_file = buffer_randomVariable
		aux = MpcDefinitionCollection()
		aux[self.randomVariable.id] = self.randomVariable
		write_definitions.write_definitions(aux, pinfo)
		pinfo.out_file = None

		# open the tcl script file
		fo = open(temp_script_file, 'w')

		# replace placeholders with actual data
		# and write to file
		fo.write(template.replace(
			'__definitions__', buffer_randomVariable.getvalue()).replace(
			'__tag__', str(self.randomVariable.id)).replace(
			'__num__', str(self.div)).replace(
			'__out__', temp_output_file))

		# relase temporary buffers
		buffer_randomVariable.close()

		# close output file
		fo.close()

		# return data
		return (
			opensees_cmd,
			temp_dir,
			temp_script_file,
			temp_output_file
			)

	# Runs the test filling the self.strain self.stress members.
	def run(self):

		# prepare test
		(opensees_cmd, temp_dir, temp_script_file, temp_output_file) = self.__prepare_test()
		print('Running OpenSEES')
		print('command: {}'.format(opensees_cmd))
		print('args: {}'.format(temp_script_file))

		# launch opensees and communicate
		for item in tu.executeAsync([opensees_cmd, temp_script_file], temp_dir):
			if item.startswith('__R__'):
				# this linke contains precentage and strain/stress data
				tokens = item[5:].split()
				ipercen = float(tokens[0])
				ix = float(tokens[1])
				ipdf = float(tokens[2])
				icdf = float(tokens[3])
				self.x.append(ix)
				self.pdf.append(ipdf)
				self.cdf.append(icdf)
				# notify that tester data has been updated: emit signal
				self.testProcessUpdated.emit(ipercen, ix, ipdf, icdf)
			else:
				print(item)

		# remove temporary files
		os.remove(temp_script_file)
		os.remove(temp_output_file)

## prova
import random
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

params = {'legend.fontsize': 'x-small',
         'axes.labelsize': 'x-small',
         'axes.titlesize':'x-small',
         'xtick.labelsize':'x-small',
         'ytick.labelsize':'x-small'}

class MyMplCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
	def __init__(self, parent=None, width=5, height=4, dpi=100):

		fig = Figure(figsize=(width, height), dpi=dpi)
		FigureCanvas.__init__(self, fig)

		self.control = parent
		self.figure = fig

		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		plt.rcParams.update(params)
		# plt.tick_params(axis='x', which='both')
		# plt.tick_params(axis='y', which='both')

		#self.axes = fig.add_subplot(111)
		self.ax_pdf = fig.add_subplot(211)
		self.ax_pdf.set_title('pdf')
		self.ax_pdf.set_xlabel('x')
		self.ax_pdf.set_xlim(-2.0, 2.0)
		self.ax_pdf.set_ylabel('f(x)')
		self.ax_pdf.set_ylim(0, 1.0)
		self.ax_pdf.grid()
		# self.ax_pdf.set_ticks_position('both')
		self.ax_pdf.set_position([0.08, 0.58, 0.9, 0.38])
		self.ax_cdf = fig.add_subplot(212)
		self.ax_cdf.set_title('cdf')
		self.ax_cdf.set_xlabel('x')
		self.ax_cdf.set_xlim(-2.0, 2.0)
		self.ax_cdf.set_ylabel('F(x)')
		self.ax_cdf.set_ylim(0, 1.0)
		self.ax_cdf.grid()
		# self.ax_cdf.set_ticks_position('both')
		self.ax_cdf.set_position([0.08, 0.08, 0.9, 0.38])

		self.compute_initial_figure()

		self.setParent(parent)

		FigureCanvas.updateGeometry(self)


	def compute_initial_figure(self):
		hl_ax_pdf = self.ax_pdf.plot([],[])
		self.hl_ax_pdf = hl_ax_pdf[0]
		hl_ax_cdf = self.ax_cdf.plot([],[])
		self.hl_ax_cdf = hl_ax_cdf[0]

	def update_figure(self, x, f, F):

		# update pdf
		self.hl_ax_pdf.set_xdata(x)
		self.hl_ax_pdf.set_ydata(f)
		# self.hl_ax_pdf.set_xlim(np.min(self.hl_ax_pdf.get_xdata()),np.max(self.hl_ax_pdf.get_xdata()))

		# update cdf
		self.hl_ax_cdf.set_xdata(x)
		self.hl_ax_cdf.set_ydata(F)

		self.ax_pdf.set_xlim(min(x), max(x))
		self.ax_pdf.set_ylim(0, max(f)*1.05)
		self.ax_cdf.set_xlim(min(x), max(x))
		self.ax_cdf.set_ylim(0, 1)

		self.draw()
		# FigureCanvas.updateGeometry(self)

## The TesterDistributionWidget class is a widget used to run distribution simulation for randomVariables.
#
# This custom widget will be added in the right side of the STKO XObject Editor, next to the standard
# XObject Attribute Tree Editor. It consists of:
# 1. A QLabel with a brief description
# 2. A MpcChartWidget that shows the graphic results of the calculation
# 3. A QTableWidget with the result data
# 4. A QPushButton to run the simulation
#
# @note This widget requires a correctly installed external solver kit (i.e. an OpenSEES version installed
# and loaded in STKO kits)
# @note Some widgets used here comes from STKO Python API, they are C++ classes exposed to Python via Boost.Python
# while all other widgets are part of PySide2 and thus exposed via Shiboken2. Since they are incompatible, we use
# the shiboken2.wrapInstance method on the raw C++ pointer.
class TesterDistributionWidget(QWidget):

	## constructor
	def __init__(self, editor, xobj, parent = None):
		# base class initialization
		super(TesterDistributionWidget, self).__init__(parent)
		# layout
		self.setLayout(QVBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)

		# description label
		self.descr_label = makeDistributionTesterLabel()
		self.layout().addWidget(self.descr_label)

		# separator
		self.separator_1 = gu.makeHSeparator()
		self.layout().addWidget(self.separator_1)

		# Parameters
		# Parameters container
		self.parameters_container = QWidget()
		self.parameters_layout = QHBoxLayout()
		self.parameters_layout.setContentsMargins(0,0,0,0)
		self.parameters_container.setLayout(self.parameters_layout)
		# Parameters labels
		self.parameters_label_div = QLabel("Divisions")
		self.parameters_layout.addWidget(self.parameters_label_div)

		# parameters divisions spin box
		self.parameters_div_spinbox = QSpinBox()
		self.parameters_div_spinbox.setRange(1, 1000000)
		self.parameters_layout.addWidget(self.parameters_div_spinbox)

		self.parameters_layout.addStretch()

		self.layout().addWidget(self.parameters_container)

		# separator
		self.separator_2 = gu.makeHSeparator()
		self.layout().addWidget(self.separator_2)

		# matplotlib
		self.canvas = MyMplCanvas(self)
		self.layout().addWidget(self.canvas)
		self.navi_toolbar = NavigationToolbar(self.canvas, self)
		self.layout().addWidget(self.navi_toolbar)
		# vectors for charts
		self.x_vec = []
		self.f_vec = []
		self.F_vec = []

		# Run session
		# run container
		self.run_container = QWidget()
		self.layout().addWidget(self.run_container)
		# run layout
		self.run_layout = QGridLayout()
		self.run_layout.setContentsMargins(0,0,0,0)
		self.run_container.setLayout(self.run_layout)
		# run button
		self.run_button = QPushButton('Draw')
		self.run_layout.addWidget(self.run_button, 0, 0, 1, 1)
		# run progress bar
		self.run_progress_bar = gu.makeProgressBar()
		self.run_layout.addWidget(self.run_progress_bar, 0, 1, 1, 3)

		# store editor and xobj
		self.editor = editor
		self.xobj = xobj

		# we want to add this widget to the xobject editor
		# on the right of the main tree widget used for the editing of xobject attributes.
		self.editor_splitter = shiboken2.wrapInstance(editor.getChildPtr(MpcXObjectEditorChildCode.MainSplitter), QSplitter)
		self.editor_splitter.addWidget(self)
		total_width = self.editor_splitter.size().width()
		width_1 = total_width//3
		self.editor_splitter.setSizes([width_1, total_width - width_1])

		# the tester is none here
		self.tester = None

		# these variables are used for doing the gui-update only at certain steps
		self.old_percentage = 0.0
		self.delta_percentage = 0.0

		#################################################### $JSON
		# restore initial values from datastore
		a = self.xobj.getAttribute(MpcXObjectMetaData.dataStoreAttributeName())
		if a is None:
			raise Exception("Cannot find dataStore Attribute")
		ds = a.string
		try:
			jds = json.loads(ds)
			jds = jds['TesterDistribution']
			# Load data if present
			div = jds.get('num_div',100)

			self.parameters_div_spinbox.setValue(div)

		except:
			# if impossible to load, load default values
			self.parameters_div_spinbox.setValue(100)
		#################################################### $JSON

		# setup connections
		self.run_button.clicked.connect(self.onTestClicked)

	def onEditFinished(self):
		#################################################### $JSON
		# store initial values to datastore
		a = self.xobj.getAttribute(MpcXObjectMetaData.dataStoreAttributeName())
		if a is None:
			raise Exception("Cannot find dataStore Attribute")
		ds = a.string
		try:
			jds = json.loads(ds)
		except:
			jds = {}
		# Creation of dictionary with intial values to store
		num_divisions = self.parameters_div_spinbox.value()

		jds['TesterDistribution'] = {
			'num_div': num_divisions,
			}
		a.string = json.dumps(jds, indent=4)

		#################################################### $JSON

	@Slot(float, float, float, float)
	def onTestProcessUpdated(self, iperc, ix, ipdf, icdf):
		# update pdf and cdf data
		self.x.append(ix)
		self.f.append(ipdf)
		self.F.append(icdf)

		# update gui:
		# note: this is visual appealing and capture the user attention while
		# a job is beeing done. howver it slows down the job execution, so
		# we update the gui only at certain points
		self.delta_percentage += iperc - self.old_percentage
		self.old_percentage = iperc
		if self.delta_percentage > 0.0499 or iperc > 0.9999:
			self.delta_percentage = 0.0
			# update chart
			self.canvas.update_figure(self.x, self.f, self.F)
			# self.mpc_chart_widget.chart = self.chart
			# self.mpc_chart_widget.autoScale()
			# update progress bar
			self.run_progress_bar.setValue(int(round(iperc*100.0)))
			# process all events to prevent gui from freezing
			QCoreApplication.processEvents()

	def onTestClicked(self):
		# reset percentage data
		self.old_percentage = 0.0
		self.delta_percentage = 0.0

		self.x = []
		self.f = []
		self.F = []

		try:

			# check the xobject
			if self.xobj is None:
				raise Exception("The current XObject is NULL")
			if self.xobj.parent is None:
				raise Exception("The current XObject has no parent component")

			# get document
			doc = PyMpc.App.caeDocument()
			if doc is None:
				raise Exception("No current document")

			# get the parent component of this xobject
			parent_component = self.xobj.parent

			# get a unique set of all components referenced directly or indirectly
			# by parent_component.
			# this is mandatory in case the user wants to test materials that depends on other materials
			# defined previously.
			# this is a physical property so it can only reference other physical properties
			# that were defined previously, i.e. with a lower id
			ref_comp_vec = PyMpc.App.getReferencedComponents(parent_component)

			div = self.parameters_div_spinbox.value()

			# now we can run the tester
			self.tester = TesterDistribution(parent_component, div)
			self.tester.testProcessUpdated.connect(self.onTestProcessUpdated)
			parent_dialog = shiboken2.wrapInstance(self.editor.getParentWindowPtr(), QWidget)
			parent_dialog.setEnabled(False)
			self.editor.setCanClose(False)
			try:
				self.tester.run()
			finally:
				parent_dialog.setEnabled(True)
				self.editor.setCanClose(True)
				self.tester.deleteLater()
				self.tester = None

		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
