import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *
from opensees.conditions.utils import SpatialFunctionEval
import h5py
import sys
import traceback

from PySide2.QtCore import (
	QCoreApplication,
	Qt
	)
from PySide2.QtCore import (
	QTimer,
	QSize,
	Signal,
	Slot,
	QSignalBlocker
	)
from PySide2.QtGui import (
	QDoubleValidator
	)
from PySide2.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QGridLayout,
	QComboBox,
	QLabel,
	QSizePolicy,
	QPushButton,
	QMessageBox,
	QSplitter,
	QTabWidget,
	QLineEdit,
	QSlider,
	QApplication
	)
import shiboken2

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

plt_params = {
	'legend.fontsize': 'x-small',
	'axes.labelsize': 'x-small',
	'axes.titlesize':'x-small',
	'xtick.labelsize':'x-small',
	'ytick.labelsize':'x-small'
	}
def _make_plot_widget(width=3, height=3, dpi=100):
	# create the parent widget container
	container = QWidget()
	container_layout = QVBoxLayout()
	container.setLayout(container_layout)
	container_layout.setContentsMargins(0,0,0,0)
	# make the plot canvas
	fig = Figure(figsize=(width, height), dpi=dpi)
	canvas = FigureCanvas(fig)
	# setup
	canvas.control = container
	canvas.figure = fig
	plt.rcParams.update(plt_params)
	# we want just 1 subplot
	canvas.subplot = fig.add_subplot(111)
	canvas.subplot.grid(linestyle=':')
	canvas.subplot.plot()
	# done
	canvas.setParent(container)
	canvas.updateGeometry()
	# put it into the container
	container_layout.addWidget(canvas)
	container_layout.addWidget(NavigationToolbar(canvas, container))
	# dummy plot
	plot = canvas.subplot.plot([],[], color='red', linestyle='-', linewidth=1.5)[0]
	return (container, plot)

class _mybool:
	def __init__(self, value):
		self.value = value

class DRMWidget(QWidget):
	# Signals
	windowLoaded = Signal()
	# constructor
	def __init__(self, editor, xobj, parent = None):
		# base class initialization
		super(DRMWidget, self).__init__(parent)
		#
		# set up the layotu
		layout = QGridLayout()
		layout.setContentsMargins(0,0,0,0)
		self.setLayout(layout)
		#
		# time step selection
		tlabel = QLabel('Time')
		tdrop = QSlider(Qt.Horizontal)
		tdrop.setRange(0, 0)
		tstep_label = QLabel('Step: 0; Time: 0')
		layout.addWidget(tlabel, 0, 0)
		layout.addWidget(tdrop, 0, 1)
		layout.addWidget(tstep_label, 1, 1)
		tdrop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		#
		# node selection
		nlabel = QLabel('Control Node')
		ndrop = QComboBox()
		layout.addWidget(nlabel, 2, 0)
		layout.addWidget(ndrop, 2, 1)
		#
		# deformation 
		dlabel = QLabel('Deformation Scale')
		dedit = QLineEdit()
		dedit.setValidator(QDoubleValidator())
		dedit.setText('1.0')
		layout.addWidget(dlabel, 4, 0)
		layout.addWidget(dedit, 4, 1)
		#
		# tab for time series
		ttab = QTabWidget()
		ttab.setTabsClosable(False)
		ttab.setTabShape(QTabWidget.Rounded)
		ttab.setMovable(False)
		layout.addWidget(ttab, 3, 0, 1, 2)
		uxtab, uxplot = _make_plot_widget()
		uytab, uyplot = _make_plot_widget()
		uztab, uzplot = _make_plot_widget()
		vxtab, vxplot = _make_plot_widget()
		vytab, vyplot = _make_plot_widget()
		vztab, vzplot = _make_plot_widget()
		axtab, axplot = _make_plot_widget()
		aytab, ayplot = _make_plot_widget()
		aztab, azplot = _make_plot_widget()
		ttab.addTab(uxtab, 'Ux')
		ttab.addTab(uytab, 'Uy')
		ttab.addTab(uztab, 'Uz')
		ttab.addTab(vxtab, 'Vx')
		ttab.addTab(vytab, 'Vy')
		ttab.addTab(vztab, 'Vz')
		ttab.addTab(axtab, 'Ax')
		ttab.addTab(aytab, 'Ay')
		ttab.addTab(aztab, 'Az')
		#
		#
		# store gui stuff that we need
		self.tdrop = tdrop
		self.tstep_label = tstep_label
		self.ndrop = ndrop
		self.ttab = ttab
		# displacement plots
		self.uxtab = uxtab
		self.uytab = uytab
		self.uztab = uztab
		self.uxplot = uxplot
		self.uyplot = uyplot
		self.uzplot = uzplot
		self.displacement_visible = _mybool(True)
		# velocity plots
		self.vxtab = vxtab
		self.vytab = vytab
		self.vztab = vztab
		self.vxplot = vxplot
		self.vyplot = vyplot
		self.vzplot = vzplot
		self.velocity_visible = _mybool(True)
		# acceleration plots
		self.axtab = axtab
		self.aytab = aytab
		self.aztab = aztab
		self.axplot = axplot
		self.ayplot = ayplot
		self.azplot = azplot
		self.acceleration_visible = _mybool(True)
		# others
		self.dedit = dedit
		#
		# store editor and xobj
		self.editor = editor
		self.xobj = xobj
		#
		# we want to add this widget to the xobject editor
		# on the right of the main tree widget used for the editing of xobject attributes.
		self.editor_splitter = shiboken2.wrapInstance(editor.getChildPtr(MpcXObjectEditorChildCode.MainSplitter), QSplitter)
		self.editor_splitter.addWidget(self)
		#
		# default value data
		self.db = None
		self.dt = 0.0
		self.tstart = 0.0
		#
		# connections
		self.windowLoaded.connect(self.onWindowLoaded)
		self.tdrop.valueChanged.connect(self.onTDropValueChanged)
		self.ndrop.currentIndexChanged.connect(self.onNDropCurrentIndexChanged)
	
	# implement the show event
	def showEvent(self, event):
		super(DRMWidget, self).showEvent(event)
		self.windowLoaded.emit()
	
	@Slot()
	def onWindowLoaded(self):
		# initial size
		total_width = self.editor_splitter.size().width()
		width_1 = total_width//3
		self.editor_splitter.setSizes([1, 3])
	
	@Slot(int)
	def onTDropValueChanged(self, value):
		ctime = self.tstart + self.dt*float(value)
		self.tstep_label.setText('Step: {}; Time: {:.6g}'.format(value, ctime))
	
	@Slot(int)
	def onNDropCurrentIndexChanged(self, value):
		node_id = self.ndrop.itemData(value)
		isqa = False
		if node_id < 0:
			node_id = -node_id-1
			isqa = True
		if isqa:
			prefix = 'DRM_QA_Data'
		else:
			prefix = 'DRM_Data'
		group = self.db[prefix]
		targets = ('displacement', 'velocity', 'acceleration')
		plots = (
			(self.uxplot, self.uyplot, self.uzplot, self.displacement_visible), 
			(self.vxplot, self.vyplot, self.vzplot, self.velocity_visible), 
			(self.axplot, self.ayplot, self.azplot, self.acceleration_visible))
		if not isqa:
			loc = self.db['DRM_Data/data_location'][:]
		for i in range(len(targets)):
			# check whether the target exists
			target = targets[i]
			if target in group:
				try:
					# get data
					values = group[target]
					pos = node_id*3
					if not isqa:
						pos = loc[node_id]
					x = values[pos, :]
					y = values[pos+1, :]
					z = values[pos+2, :]
					# plot it
					iplot = plots[i]
					px = iplot[0]
					py = iplot[1]
					pz = iplot[2]
					px.set_xdata(self.time)
					px.set_ydata(x)
					py.set_xdata(self.time)
					py.set_ydata(y)
					pz.set_xdata(self.time)
					pz.set_ydata(z)
					# redraw
					for item in (px, py, pz):
						item.axes.relim()
						item.axes.autoscale_view()
						item.figure.canvas.draw()
					# show tabs if necessary
					self.ttab.setTabEnabled(i, True)
					iplot[3].value = True
				except Exception as err:
					print(traceback.format_exc())
			else:
				# hide the tabs if necessary
				self.ttab.setTabEnabled(i, False)
				iplot[3].value = False
				print("not", target)
		
	
	def setDatabase(self, db):
		# set a reference to the database
		if self.db:
			self.db.close()
		self.db = db
		# clear all
		self.tdrop.setRange(0, 0)
		self.tstep_label.setText('Step: 0; Time: 0')
		self.ndrop.clear()
		for i in (self.axplot, self.ayplot, self.azplot, self.uxplot, self.uyplot, self.uzplot):
			i.set_xdata([])
			i.set_ydata([])
		# quick return
		if db is None:
			return None
		# populate it
		dt = db['DRM_Metadata/dt'][()]
		self.dt = dt
		tstart = db['DRM_Metadata/tstart'][()]
		self.tstart = tstart
		tend = db['DRM_Metadata/tend'][()]
		self.tend = tend
		nsteps = db['DRM_Data/displacement'].shape[1]
		# save the time series
		self.time = np.arange(self.tstart, self.tend, self.dt)
		# time slider
		self.tdrop.setRange(0, nsteps-1)
		# qa points
		xyz = db['DRM_QA_Data/xyz'][:,:]
		for i in range(xyz.shape[0]):
			ix = xyz[i, 0]
			iy = xyz[i, 1]
			iz = xyz[i, 2]
			self.ndrop.addItem('QA [{}] ({:.3g}, {:.3g}, {:.3g})'.format(i, ix,iy,iz), -i-1)
		# grid points
		xyz = db['DRM_Data/xyz'][:,:]
		for i in range(xyz.shape[0]):
			ix = xyz[i, 0]
			iy = xyz[i, 1]
			iz = xyz[i, 2]
			self.ndrop.addItem('[{}] ({:.3g}, {:.3g}, {:.3g})'.format(i, ix,iy,iz), i)
		

def makeXObjectMetaData():
	
	# TODO: change the URL of doc
	
	def mka(name, type, group, description):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(description) +
			html_par(html_href('https://github.com/OpenSees/OpenSees/pull/751','DRM')+'<br/>') +
			html_end()
			)
		return a
	
	# mandatory parameters
	
	filename = mka('File Name', MpcAttributeType.String, 'Mandatory', 'The HDF5 file containing...')
	filename.stringType = 'OpenFilePath H5DRM Input database (*.h5drm *.H5DRM)'
	
	# optional paramrters
	
	factor = mka('factor', MpcAttributeType.Real, 'Optional', 'Load scale factor')
	factor.setDefault(1.0)
	
	crd_scale = mka('crd_scale', MpcAttributeType.Real, 'Optional', 'Coordinate scale factor')
	crd_scale.setDefault(1.0)
	
	distance_tolerance = mka('distance_tolerance', MpcAttributeType.Real, 'Optional', 'Tolerance for searching the nearest node')
	distance_tolerance.setDefault(1.0e-3)
	
	do_coordinate_transformation = mka('do_coordinate_transformation', MpcAttributeType.Boolean, 'Optional', '')
	do_coordinate_transformation.setDefault(True)
	
	do_center = mka('Center box', MpcAttributeType.Boolean, 'Optional', 'If True, The DRM Box will be translated at the center of the STKO domain')
	do_center.setDefault(True)
	
	xt = mka('Extra Translation', MpcAttributeType.QuantityVector3, 'Optional', 'An additional translation')
	
	vx = mka('Local X', MpcAttributeType.QuantityVector3, 'Optional', 'The Local X axis of the DRM Box (not necessarily a unit vector')
	vy = mka('Local Y', MpcAttributeType.QuantityVector3, 'Optional', 'The Local Y axis of the DRM Box (not necessarily a unit vector')
	
	xom = MpcXObjectMetaData()
	xom.name = 'H5DRM'
	xom.addAttribute(filename)
	xom.addAttribute(factor)
	xom.addAttribute(crd_scale)
	xom.addAttribute(distance_tolerance)
	xom.addAttribute(do_center)
	xom.addAttribute(xt)
	xom.addAttribute(vx)
	xom.addAttribute(vy)
	#xom.addAttribute(do_coordinate_transformation)
	
	return xom

def makeConditionRepresentationData(xobj):
	'''
	Create the condition representation data for STKO.
	Here we want an arrow (vector) representation in local
	coordinate system, that can be applied only on faces.
	We need to allocate a 3d vector for the data attribute.
	The components of this vector will be set using
	@ref fillConditionRepresentationData
	'''
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Points
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = False
	d.on_faces = False
	d.on_solids = True
	d.on_interactions = False
	return d

def _set_default_x(xobj):
	vx = xobj.getAttribute('Local X').quantityVector3.referenceValue
	if vx.norm() < 1.0e-10:
		vx.x = 1.0
		vx.y = 0.0
		vx.z = 0.0
def _set_default_y(xobj):
	vy = xobj.getAttribute('Local Y').quantityVector3.referenceValue
	if vy.norm() < 1.0e-10:
		vy.x = 0.0
		vy.y = 1.0
		vy.z = 0.0

class _constants:
	# gui
	gui = None

def _removeGui():
	if _constants.gui is not None:
		_constants.gui.db.close()
		_constants.gui.setParent(None)
		_constants.gui.deleteLater()
		_constants.gui = None

def onEditorClosing(editor, xobj):
	_removeGui()

def onEditFinished(editor, xobj):
	pass

def _setDatabaseOnGui(xobj):
	try:
		fname = xobj.getAttribute('File Name').string
		ffile = h5py.File(fname, 'r')
	except:
		QMessageBox.critical(QApplication.activeWindow(), 'Error', 'Invalid HDF5 file')
		ffile = None
	_constants.gui.setDatabase(ffile)

def onEditBegin(editor, xobj):
	# check any default value
	_set_default_x(xobj)
	_set_default_y(xobj)
	# create the gui
	_removeGui()
	_constants.gui = DRMWidget(editor, xobj)
	# check whether the file exists
	_setDatabaseOnGui(xobj)

def onAttributeChanged(editor, xobj, attribute_name):
	# or you can use this to automatically trigger the update
	if attribute_name == 'File Name':
		_setDatabaseOnGui(xobj)
