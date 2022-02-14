import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

# encoder and decoder for using datastore indexes
from opensees.utils.datastore_utils import MpcDataStoreEncoder, MpcDataStoreDecoder
import opensees.physical_properties.materials.uniaxial.Design.Concrete_support_data.concreteMaterials as concreteMaterials
import opensees.utils.Gui.GuiUtils as gu
import json

import os
import PyMpc
import traceback
from io import StringIO

strengthString = {'k': 'Characteristic (5th percentile) strength because selected new material',
				'm': 'Mean strength because selected existing material'}

from PySide2.QtCore import (
	QSignalBlocker,
	QSize,
	Qt
	)

from PySide2.QtGui import (
	QPixmap,
	QImage,
	QDoubleValidator,
	)

from PySide2.QtWidgets import (
	QWidget,
	QDialog,
	QVBoxLayout,
	QHBoxLayout,
	QGridLayout,
	QFormLayout,
	QGroupBox,
	QRadioButton,
	QComboBox,
	QSpinBox,
	QCheckBox,
	QSplitter,
	QPushButton,
	QLabel,
	QSizePolicy,
	QMessageBox,
	QFrame,
	QScrollArea,
	QTextEdit,
	QLineEdit,
	)

import shiboken2

class _constants:
	#gui
	gui = None
	#version
	version = 1

class concreteWidget(QWidget):
	# Class attribute for the activation of Debug printing
	_debug = True
	
	#constructor
	def __init__(self, editor, xobj, parent = None):
		# base class initialization
		super(concreteWidget, self).__init__(parent)

		# store editor and xobj
		self.editor = editor
		self.xobj = xobj

		# layout
		self.setLayout(QVBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)

		# description label
		descr_label = QLabel(
			'<html><head/><body>'
			'<p align="center"><span style=" font-size:11pt; color:#003399;">'
			'Concrete material'
			'</span></p>'
			'<p align="center"><span style=" color:#000000;">'
			'This widget permits to create an instance of simplified concrete material'
			'to use in design'
			'<br>The widget is connected on real-time to the attributes'
			'of the object'
			'</span></p>'
			'</body></html>'
		)
		descr_label.setWordWrap(True)
		self.layout().addWidget(descr_label)

		# Horizontal separator
		separator_1 = gu.makeHSeparator()
		self.layout().addWidget(separator_1)

		#Container for the whole widget
		material_widget = QWidget()
		material_widget.setLayout(QGridLayout())
		material_widget.layout().setContentsMargins(0,0,0,0)
		
		# Add a combo box that takes data from default standard (EC2 / NTC 2018 for now)
		material_widget.layout().addWidget(QLabel("Concrete strength class: "),0,0,1,1)
		self.comboMaterial = QComboBox()
		
		# self.comboMaterial.setMinimumWidth(250)
		material_widget.layout().addWidget(self.comboMaterial,0,1,1,1)
		
		# Add a checkbox for existing concrete
		self.checkExisting = QCheckBox("Existing concrete")
		self.checkExisting.setToolTip("If existing the strength used is mean strength. Otherwise characteristic (5% percentile) will be used")
		material_widget.layout().addWidget(self.checkExisting,1,0,1,2)
		
		# Add Line Edit for fc (m or k)
		label = QLabel("Compressive strength (fc)")
		material_widget.layout().addWidget(label,2,0,1,1)
		self.edit_fc = QLineEdit()
		validator = QDoubleValidator()
		validator.setBottom(0)
		self.edit_fc.setValidator(validator)
		material_widget.layout().addWidget(self.edit_fc,2,1,1,1)
		
		# Add Line Edit for Ec
		label = QLabel("Elastic modulus (Ec)")
		material_widget.layout().addWidget(label,3,0,1,1)
		self.edit_Ec = QLineEdit()
		self.edit_Ec.setToolTip('Mean Elastic modulus')
		validator = QDoubleValidator()
		validator.setBottom(0)
		self.edit_Ec.setValidator(validator)
		material_widget.layout().addWidget(self.edit_Ec,3,1,1,1)
		
		# Add Line Edit for eps_c
		label = QLabel("Peak strain")
		material_widget.layout().addWidget(label,4,0,1,1)
		self.edit_epsc = QLineEdit()
		validator = QDoubleValidator()
		validator.setBottom(0)
		self.edit_epsc.setValidator(validator)
		material_widget.layout().addWidget(self.edit_epsc,4,1,1,1)
		
		# Add Line Edit for eps_cu
		label = QLabel("Ultimate strain")
		material_widget.layout().addWidget(label,5,0,1,1)
		self.edit_epscu = QLineEdit()
		validator = QDoubleValidator()
		validator.setBottom(0)
		self.edit_epscu.setValidator(validator)
		material_widget.layout().addWidget(self.edit_epscu,5,1,1,1)
		
		# Add the material widget to the main layout
		self.layout().addWidget(material_widget)
		self.layout().addStretch(1)

		if concreteWidget._debug:
			print('concreteWidget::__init__\t\t\t->\tCreated the main widgets')
		
		# store editor and xobj
		self.editor = editor
		self.xobj = xobj
		
		if concreteWidget._debug:
			print('concreteWidget::__init__\t\t\t->\tAdding the widget to the editor')
		# we want to add this widget to the xobject editor
		# on the right of the main tree widget used for the editing of xobject attributes.
		self.editor_splitter = shiboken2.wrapInstance(editor.getChildPtr(MpcXObjectEditorChildCode.MainSplitter), QSplitter)
		self.editor_splitter.addWidget(self)
		total_width = self.editor_splitter.size().width()
		width_1 = 0 #○total_width//3
		self.editor_splitter.setSizes([width_1, total_width - width_1])
		
		if concreteWidget._debug:
			print('concreteWidget::__init__\t\t\t->\tAdded the widget to the editor')
		
		# Open Datastore to see if some data is existing
		#################################################### $JSON
		# restore initial values from datastore
		a = self.xobj.getAttribute(MpcXObjectMetaData.dataStoreAttributeName())
		if a is None:
			raise Exception("Cannot find dataStore Attribute")
		ds = a.string
		try:
			# Default values - To discuss
			jds = json.loads(ds)
			jds = jds['ConcreteSimplifiedMaterial']
			class_name = jds['standard']
			self.standard = jds.get('standard','EN1992')
			self.classStrength = jds.get('classStrength','25')
			self.existing = jds.get('existing',False)
		except:
			# Default values - To discuss
			self.standard = 'EN1992'
			self.classStrength = '25'
			self.existing = False
		#################################################### $JSON
		
		# Get the standard strength class values and a link to the right class to call
		out = concreteMaterials.concreteStandardFactory.make(self.standard)
		standardStrengthValues = out[0]
		self.className = out[1]
		for c in standardStrengthValues.keys():
			self.comboMaterial.addItem('{}'.format(standardStrengthValues[c]['name']),c)
		self.comboMaterial.addItem('Custom',0)
		idx = self.comboMaterial.findData(self.classStrength)
		self.comboMaterial.setCurrentIndex(idx)
		# update the concrete model
		if float(self.classStrength) > 0:
				self.concrete = self.className(self.classStrength)
		else:
			self.edit_fc.setText('{}'.format(_get_xobj_attribute(self.xobj, 'fc').quantityScalar.referenceValue))
			if self.existing:
				fck = '{}'.format(float(self.edit_fc.text()) - 8)
			else:
				fck = self.edit_fc.text()
			self.concrete = self.className(fck)
		print(self.concrete)
		# Set the checking box for existing material:
		self.checkExisting.setChecked(self.existing)
		
		# call methods because there are not connections yet (use default values)
		self.onCheckExistingChanged()
		if float(self.classStrength) > 0:
			self.onMaterialChanged()
		else:
			self.onStrengthManuallyChanged()
		
		# Establish the connections:
		# The change of class strength combo updates the Line edits:
		self.comboMaterial.currentIndexChanged.connect(self.onMaterialChanged)
		# The change of existing checkbox triggers the change of fc m or fc k
		self.checkExisting.stateChanged.connect(self.onCheckExistingChanged)
		# The manual change of fck (or fcm if Existing), updates all the other materials
		self.edit_fc.editingFinished.connect(self.onStrengthManuallyChanged)
		
		# self.confinementModel_cbox.currentIndexChanged.connect(self.onClassStrengthChanged)
	
	def onStrengthManuallyChanged(self):
		# TODO: THERE IS A CRASH HERE!
		# write custom in the combobox, blocking the signal before
		locks = [QSignalBlocker(self.comboMaterial)]
		idx = self.comboMaterial.findData(0)
		self.comboMaterial.setCurrentIndex(idx)
		self.classStrength = self.comboMaterial.currentData()
		print('The class strength was set to {} du to manual override'.format(self.classStrength))
		
		if self.existing:
			fc = self.concrete.fcm
			add = -8
		else:
			fc = self.concrete.fck
			add = 0
		print('reference value to check variation = {} - should add {} to obtain fck'.format(fc,add))
		if abs(float(self.edit_fc.text()) - fc) > 1e-8:
			# update fck
			new_fck = float(self.edit_fc.text())+add
			print('changed from previus value: update the model to fck = {}'.format(float(new_fck)))
			self.concrete.set_strength_class('{}'.format(new_fck))
			
		# update the line edits
		self.edit_Ec.setText('{}'.format(self.concrete.Ecm))
		self.edit_epsc.setText('{}'.format(self.concrete.eps_c2))
		self.edit_epscu.setText('{}'.format(self.concrete.eps_cu2))
		
	def onCheckExistingChanged(self):
		if self.checkExisting.isChecked():
			self.existing = True
			self.edit_fc.setToolTip(strengthString['m'])
			self.edit_fc.setText('{}'.format(self.concrete.fcm))
		else:
			self.existing = False
			self.edit_fc.setToolTip(strengthString['k'])
			self.edit_fc.setText('{}'.format(self.concrete.fck))
	
	def onMaterialChanged(self):
		print('Material Changed from the combo box')
		# the strength class was changed update all values
		self.classStrength = self.comboMaterial.currentData()
		# update the concrete model
		self.concrete = self.className(self.classStrength)
		
		# update the line edits
		if self.existing:
			self.edit_fc.setText('{}'.format(self.concrete.fcm))
		else:
			self.edit_fc.setText('{}'.format(self.concrete.fck))
		self.edit_Ec.setText('{}'.format(self.concrete.Ecm))
		self.edit_epsc.setText('{}'.format(self.concrete.eps_c2))
		self.edit_epscu.setText('{}'.format(self.concrete.eps_cu2))
		
	def onEditFinished(self):
		if concreteWidget._debug:
			print('concreteWidget::onEditFinished\t\t\t->\tEdit finished in the widget. Saving eventual needed data to datastore -> things needed for GUI')
		#Save in the data store the needed data
		#################################################### $JSON
		# store values to datastore
		data = self.xobj.getAttribute(MpcXObjectMetaData.dataStoreAttributeName())
		if data is None:
			raise Exception("Cannot find dataStore Attribute")
		ds = data.string
		try:
			jds = json.loads(ds)
		except:
			jds = {}
			
		# Save everything needed for distributed formulation
		jds['ConcreteSimplifiedMaterial'] = {
			'version': _constants.version,
			'standard': self.standard,
			'classStrength': self.classStrength,
			'existing': self.existing
		}
		data.string = json.dumps(jds, indent=4, cls=MpcDataStoreEncoder)
		
		if concreteWidget._debug:
			print('concreteWidget::onEditFinished\t\t\t->\tData saved to data store: {}'.format(data.string))
			
		# Save to the xobj the needed parameters:
		_get_xobj_attribute(self.xobj, 'fc').quantityScalar.referenceValue = float(self.edit_fc.text())
		_get_xobj_attribute(self.xobj, 'eps_c').real = float(self.edit_epsc.text())
		_get_xobj_attribute(self.xobj, 'eps_cu').real = float(self.edit_epscu.text())
		_get_xobj_attribute(self.xobj, 'Ec').quantityScalar.referenceValue = float(self.edit_Ec.text())
		_get_xobj_attribute(self.xobj, 'n').real = self.concrete.n


def makeXObjectMetaData():

	def make_attr(name, group, descr):
		at = MpcAttributeMetaData()
		at.name = name
		at.group = group
		at.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('http://www.google.it','Ref Link')+'<br/>') +
			html_end()
			)
		return at

	xom = MpcXObjectMetaData()
	xom.name = 'Concrete'
	# xom.Xgroup = ''
	
	# Material parameters
	at_fc = make_attr('fc', 'Material Properties', 'Compressive strength of confined concrete')
	at_fc.type = MpcAttributeType.QuantityScalar
	at_fc.setDefault(0.0)
	at_fc.dimension = u.F/u.L**2
	at_fc.visible = True
	at_fc.editable = True
	# Peak strain
	at_epsc = make_attr('eps_c', 'Material Properties', 'Peak strain of concrete')
	at_epsc.type = MpcAttributeType.Real
	at_epsc.setDefault(0.0)
	at_epsc.visible = True
	at_epsc.editable = True
	# Ultimate strain
	at_epscu = make_attr('eps_cu', 'Material Properties', 'Ultimate strain of concrete')
	at_epscu.type = MpcAttributeType.Real
	at_epscu.setDefault(0.0)
	at_epscu.visible = True
	at_epscu.editable = True
	# Elastic modulus of concrete
	at_Ec = make_attr('Ec', 'Material Properties', 'Elastic modulus of concrete')
	at_Ec.type = MpcAttributeType.QuantityScalar
	at_Ec.dimension = u.F/u.L**2
	at_Ec.setDefault(0.0)
	at_Ec.visible = True
	at_Ec.editable = True
	# Exponent of the parabola-rectangle law
	at_n = make_attr('n', 'Material Properties', 'Exponent of the parabola part in the constitutive law')
	at_n.type = MpcAttributeType.Real
	at_n.setDefault(2.0)
	at_n.visible = True
	at_n.editable = True
	
	# add a last attribute for versioning
	av = MpcAttributeMetaData()
	av.type = MpcAttributeType.Integer
	av.description = (
		html_par('Version {}'.format(_constants.version))
		)
	av.name = 'version'
	av.setDefault(_constants.version)
	av.editable = False
	av.visible = True
	
	xom.addAttribute(at_fc)
	xom.addAttribute(at_epsc)
	xom.addAttribute(at_epscu)
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_n)
	xom.addAttribute(av)

	return xom

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def _removeGui():
	if _constants.gui is not None:
		_constants.gui.setParent(None)
		_constants.gui.deleteLater()
		_constants.gui = None

def onEditorClosing(editor, xobj):
	_removeGui()

def onEditFinished(editor, xobj):
	if _constants.gui is not None:
		_constants.gui.onEditFinished()

def onEditBegin(editor, xobj):
	_removeGui()
	_constants.gui = concreteWidget(editor,xobj)
	
def onConvertOldVersion(xobj, old_xobj):
	'''
	try to convert objects from old versions to the current one.
	current version: 1
	'''
	
	version = 0 # default one
	av = old_xobj.getAttribute('version')
	if av:
		version = av.integer
	
	# just a safety check
	cav = xobj.getAttribute('version')
	if cav is None:
		IO.write_cerr('Cannot find "version" attribute in AnalysesCommand\n')
		return
		
	cav.integer = _constants.version
		
	# Check version
	if version == 0:
		# It should never happen because the xboj was included with version 1, so nobody should have an old version of the xobj
		pass
	if version < cav.integer:
		# The current version is newer than the file version, will do whatever will be needed
		# Here the logic for version change (update) should be included. For instance what to do when moving from version 1 to 2, to 3 etc.
		pass
		
	

