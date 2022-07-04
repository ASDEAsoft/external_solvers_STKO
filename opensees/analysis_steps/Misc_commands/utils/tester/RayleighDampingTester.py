## @package Tester1D
# The Tester1D packages contains the tester and widget classes that are used
# to run a test of a uniaxial material

import subprocess
import os
import sys
import traceback
from io import StringIO
import json
import math

import PyMpc
import PyMpc.App
import PyMpc.Math
import PyMpc.Units
from PyMpc.Units import MpcQuantityVector
from PyMpc import *

import opensees.utils.tcl_input as tclin
import opensees.utils.Gui.GuiUtils as gu

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
def makeRayleighDampingTesterLabel():
	label = QLabel(
		'<html><head/><body>'
		'<p align="center"><span style=" font-size:11pt; color:#003399;">'
		'Rayleigh Damping Tester'
		'</body></html>'
		)
	label.setWordWrap(True)
	return label

class RayleighDampingTester(QObject):

	# a signal to notify that we have
	# the new components of x, mass and stiff
	testProcessUpdated = Signal(float, float, float, float, float, bool)
	# testProcessUpdated = Signal(float, float, float, float)

	# create a new RayleighDampingTester passing as arguments
	# definition and a list of xs.
	def __init__(self, randomVariable, xobj, parent = None):
		# base class initialization
		super(RayleighDampingTester, self).__init__(parent)
		# self initialization
		self.randomVariable = randomVariable
		self.x = []
		self.mass = [] # mass f
		self.stiff = [] # stiff F
		# self.mk =[]
		self.xobj =xobj

	# prepares data for testing and returns the command to run
	# and the names of temporary files
	
	# Runs the test filling the self.strain self.stress members.
	def run(self):
		fmax = self.xobj.getAttribute('f2/Rayleigh').real*1.1
		a0 = self.xobj.getAttribute('alphaM/Rayleigh').real
		a1 = self.xobj.getAttribute('Betak/Rayleigh').real
		csi = max(self.xobj.getAttribute('damp_1/Rayleigh').real,self.xobj.getAttribute('damp_2/Rayleigh').real) *1.5
		nsteps = 1000
		for i in np.linspace(0.0, fmax, nsteps):
			ix = i
			self.x.append(i)
			imass = a0/(2.0*math.pi*2.0*i)
			self.mass.append(imass)
			istiff = a1 * math.pi*2.0*i/2.0
			self.stiff.append(istiff)
			# self.testProcessUpdated.emit(ix, imass, istiff, imass+istiff, csi)
			do_update = False
			if i > fmax*0.9999:
				do_update = True
			self.testProcessUpdated.emit(ix, imass, istiff,imass+istiff, csi, do_update)
			# self.mk.append(imass+istiff)

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

		# fig = Figure(figsize=(width, height), dpi=dpi)
		
		# fig, axs = plt.subplots(1, 2)
		# x1 =[]
		# y1= []
		# self.ax_mass = plt.plot(x1, y1, label = 'test 1')
		# self.ax_stiff =  plt.plot(x1, y1, label = 'test 2')
		# self.ax_mK =  plt.plot(x1, y1, label = 'test 3')
		# self.ax_f1 =  plt.plot(x1, y1, label = 'test 4')
		# self.ax_f2 =  plt.plot(x1, y1, label = 'test 5')
		# plt.legend() 
		# fig = plt.figure()
		
		fig = Figure(figsize=(width, height), dpi=dpi)
		FigureCanvas.__init__(self, fig)

		self.control = parent
		self.figure = fig

		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		plt.rcParams.update(params)
		
		self.ax_mass = fig.add_subplot(111)
		self.ax_mass.set_title('Damping')
		self.ax_mass.set_xlabel('f[Hz]')
		self.ax_mass.set_xlim(0.0, 15.0)
		self.ax_mass.set_ylabel('csi')
		self.ax_mass.set_ylim(0, 1)
		self.ax_mass.grid()
		self.ax_mass.plot()
	
		self.ax_stiff =  fig.add_subplot(111)
		self.ax_mK= fig.add_subplot(111)
		self.ax_f1= fig.add_subplot(111)
		self.ax_f2= fig.add_subplot(111)
		
		# fig.legend((self.ax_f1,self.ax_f2), ('Line 3', 'Line 4'), 'upper right')
		
		self.compute_initial_figure()

		self.setParent(parent)

		FigureCanvas.updateGeometry(self)


	def compute_initial_figure(self):
		hl_ax_mass = self.ax_mass.plot([],[],'r-')
		self.hl_ax_mass = hl_ax_mass[0]
		self.hl_ax_mass.set_label('Mass proportional')
		self.ax_mass.legend()
		hl_ax_stiff = self.ax_stiff.plot([],[],'g-')
		self.hl_ax_stiff = hl_ax_stiff[0]
		self.hl_ax_stiff.set_label('Stiffness proportional')
		self.ax_stiff.legend()
		hl_ax_mK = self.ax_mK.plot([],[])
		self.hl_ax_mK = hl_ax_mK[0]
		self.hl_ax_mK.set_label('Rayleigh Damping')
		self.ax_mK.legend()
		
		hl_ax_f1 = self.ax_f1.plot([],[],'k:')
		self.hl_ax_f1 = hl_ax_f1[0]
		hl_ax_f2 = self.ax_f2.plot([],[],'k:')
		self.hl_ax_f2 = hl_ax_f2[0]

	def update_figure(self, x, mass, stiff, mK, csi , xobj):

		# update mass
		self.hl_ax_mass.set_xdata(x)
		self.hl_ax_mass.set_ydata(mass)
		# self.hl_ax_mass.set_xlim(np.min(self.hl_ax_mass.get_xdata()),np.max(self.hl_ax_mass.get_xdata()))

		self.hl_ax_stiff.set_xdata(x)
		self.hl_ax_stiff.set_ydata(stiff)
		
		self.hl_ax_mK.set_xdata(x)
		self.hl_ax_mK.set_ydata(mK)
		
		f1 = xobj.getAttribute('f1/Rayleigh').real
		damp_1 = xobj.getAttribute('damp_1/Rayleigh').real
		
		x_1=[]
		x_1.append(f1)
		x_1.append(f1)
		csi_1=[]
		csi_1.append(0.0)
		csi_1.append(damp_1)
		self.hl_ax_f1.set_xdata(x_1)
		self.hl_ax_f1.set_ydata(csi_1)
		
		f2 = xobj.getAttribute('f2/Rayleigh').real
		damp_2 = xobj.getAttribute('damp_2/Rayleigh').real
		x_2=[]
		x_2.append(f2)
		x_2.append(f2)
		csi_2=[]
		csi_2.append(0.0)
		csi_2.append(damp_2)
		self.hl_ax_f2.set_xdata(x_2)
		self.hl_ax_f2.set_ydata(csi_2)
		
		self.ax_mass.set_xlim(0.0, 1.1*f2)
		self.ax_mass.set_ylim(0, csi)

		self.draw()
		# FigureCanvas.updateGeometry(self)


class RayleighDampingTesterWidget(QWidget):

	## constructor
	def __init__(self, editor, xobj, parent = None):
		# base class initialization
		super(RayleighDampingTesterWidget, self).__init__(parent)
		# layout
		self.setLayout(QVBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)

		# description label
		self.descr_label = makeRayleighDampingTesterLabel()
		self.layout().addWidget(self.descr_label)

		# separator
		self.separator_1 = gu.makeHSeparator()
		self.layout().addWidget(self.separator_1)

		# matplotlib
		self.canvas = MyMplCanvas(self)
		self.layout().addWidget(self.canvas)
		self.navi_toolbar = NavigationToolbar(self.canvas, self)
		self.layout().addWidget(self.navi_toolbar)
		# vectors for charts
		self.x_vec = []
		self.f_vec = []
		self.F_vec = []
		# self.mk_vec = []
		
		
		# Run session
		# run container
		self.run_container = QWidget()
		self.layout().addWidget(self.run_container)
		# run layout
		self.run_layout = QGridLayout()
		self.run_layout.setContentsMargins(0,0,0,0)
		self.run_container.setLayout(self.run_layout)
		# run button
		# self.run_button = QPushButton('Draw')
		# self.run_layout.addWidget(self.run_button, 0, 0, 1, 1)
		
		self.layout().addStretch(1)

		# store editor and xobj
		self.editor = editor
		self.xobj = xobj

		self.csi = max(xobj.getAttribute('damp_2/Rayleigh').real,xobj.getAttribute('damp_1/Rayleigh').real)*2.0
		# we want to add this widget to the xobject editor
		# on the right of the main tree widget used for the editing of xobject attributes.
		self.editor_splitter = shiboken2.wrapInstance(editor.getChildPtr(MpcXObjectEditorChildCode.MainSplitter), QSplitter)
		self.editor_splitter.addWidget(self)
		total_width = self.editor_splitter.size().width()
		width_1 = total_width//3
		self.editor_splitter.setSizes([width_1, total_width - width_1])

		# the tester is none here
		self.tester = None

		# setup connections
		#self.run_button.clicked.connect(self.onTestClicked)

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
		num_divisions = 1

		jds['RayleighDampingTester'] = {
			'num_div': num_divisions,
			}
		a.string = json.dumps(jds, indent=4)

		#################################################### $JSON

	@Slot(float, float, float, float, float, bool)
	def onTestProcessUpdated(self, ix, imass, istiff, imk, csi, do_update):
		# update mass and stiff data
		self.x.append(ix)
		self.m.append(imass)
		self.K.append(istiff)
		self.mK.append(imk)
		self.csi = csi
		# update gui:
		# note: this is visual appealing and capture the user attention while
		# a job is beeing done. howver it slows down the job execution, so
		# we update the gui only at certain points
		
		if do_update:
			# self.canvas.update_figure(self.x, self.m, self.K, self.mk, self.csi)
			self.canvas.update_figure(self.x, self.m, self.K, self.mK, self.csi, self.xobj)
				# self.mpc_chart_widget.chart = self.chart
				# self.mpc_chart_widget.autoScale()
				# update progress bar
				# process all events to prevent gui from freezing
			QCoreApplication.processEvents()

	def onTestClicked(self):
		# reset percentage data
		self.x = []
		self.m = []
		self.K = []
		self.mK= []

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

			# now we can run the tester
			self.tester = RayleighDampingTester(parent_component, self.xobj)
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

class RayleighDampingGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if RayleighDampingGuiGlobals.gui is not None:
		RayleighDampingGuiGlobals.gui.setParent(None)
		RayleighDampingGuiGlobals.gui.deleteLater()
		RayleighDampingGuiGlobals.gui = None

def onEditorClosing(editor, xobj):
	__removeGui()

def onEditFinished(editor, xobj):
	if RayleighDampingGuiGlobals.gui is not None:
		RayleighDampingGuiGlobals.gui.onEditFinished()

def onEditBegin_Tester(editor, xobj):
	__removeGui()
	RayleighDampingGuiGlobals.gui = RayleighDampingTesterWidget(editor,xobj)
	for i in xobj.attributes:
		if xobj.attributes[i].group == 'Rayleigh Input Parameters':
			update = True
			f1 = xobj.getAttribute('f1/Rayleigh').real
			w1 = 2.0 *math.pi * f1
			f2 = xobj.getAttribute('f2/Rayleigh').real
			w2 = 2.0 *math.pi * f2
			csi1 =  xobj.getAttribute('damp_1/Rayleigh').real
			csi2 =  xobj.getAttribute('damp_2/Rayleigh').real
			if abs(w1- w2) < 1.0e-3 :
				a0 =0.0
				a1=0.0
			else :
				a0= 2.0* w1 * w2 *(csi1*w2- csi2 *w1)/(w2*w2-w1*w1)
				a1= 2.0 *(csi2*w2- csi1 *w1)/(w2*w2-w1*w1)
			xobj.getAttribute('alphaM/Rayleigh').real= a0
			xobj.getAttribute('Betak/Rayleigh').real = a1
	RayleighDampingGuiGlobals.gui.onTestClicked()

def onAttributeChanged_Tester(editor, xobj, name):#attendere Max per far fare il cambio della vista senza uscire dall'editor
	update = False
	attribute = xobj.getAttribute(name)
	if attribute.group == 'Rayleigh Input Parameters':
		update = True
		f1 = xobj.getAttribute('f1/Rayleigh').real
		w1 = 2.0 *math.pi * f1
		f2 = xobj.getAttribute('f2/Rayleigh').real
		w2 = 2.0 *math.pi * f2
		csi1 =  xobj.getAttribute('damp_1/Rayleigh').real
		csi2 =  xobj.getAttribute('damp_2/Rayleigh').real
		if abs(w1- w2) < 1.0e-3 :
			a0 =0.0
			a1=0.0
		else :
			a0= 2.0* w1 * w2 *(csi1*w2- csi2 *w1)/(w2*w2-w1*w1)
			a1= 2.0 *(csi2*w2- csi1 *w1)/(w2*w2-w1*w1)
		xobj.getAttribute('alphaM/Rayleigh').real= a0
		xobj.getAttribute('Betak/Rayleigh').real = a1
	
	if update :
		RayleighDampingGuiGlobals.gui.onTestClicked()
