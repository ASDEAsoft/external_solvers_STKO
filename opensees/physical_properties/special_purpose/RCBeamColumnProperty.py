import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.physical_properties.sections.extrusion_utils as exutils
import opensees.physical_properties.special_purpose.beam_section_utils as bsutils
# encoder and decoder for using datastore indexes
from opensees.utils.datastore_utils import MpcDataStoreEncoder, MpcDataStoreDecoder
# Import the section navigator widget
from opensees.physical_properties.special_purpose.RCbeamColumnProperty_support_data.sectionsNavigator import SectionsNavigator
# Import the sub.widgets of the physical properties
from opensees.physical_properties.special_purpose.RCbeamColumnProperty_support_data.distributedWidgetPP import distributedWidgetPP
from opensees.physical_properties.special_purpose.RCbeamColumnProperty_support_data.lumpedFLWidgetPP import lumpedFLWidgetPP
from opensees.physical_properties.special_purpose.RCbeamColumnProperty_support_data.lumpedZLWidgetPP import lumpedZLWidgetPP
# Import the models for the physical properties (where the data is stored)
from opensees.physical_properties.special_purpose.RCbeamColumnProperty_support_data.distributedWidgetPP import modelDistributed
from opensees.physical_properties.special_purpose.RCbeamColumnProperty_support_data.lumpedFLWidgetPP import modelLumpedFL
from opensees.physical_properties.special_purpose.RCbeamColumnProperty_support_data.lumpedZLWidgetPP import modelLumpedZL
import opensees.utils.Gui.GuiUtils as gu
import json

import os
import PyMpc
import traceback
from io import StringIO

from PySide2.QtCore import (
	QSignalBlocker,
	QSize,
	Qt
	)

from PySide2.QtGui import (
	QPixmap,
	QImage
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
	QScrollArea
	)

import shiboken2

class _constants:
	#gui
	gui = None
	#version
	version = 1

class RCBeamColumnWidget(QWidget):
	# Class attribute for the activation of Debug printing
	_debug = False
	
	#constructor
	def __init__(self, editor, xobj, parent = None):
		# base class initialization
		super(RCBeamColumnWidget, self).__init__(parent)

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
			'Non linear beam-column element'
			'</span></p>'
			'<p align="center"><span style=" color:#000000;">'
			'This widget permits to create a beam-column element for non linear analyses'
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
		beam_widget = QWidget()
		beam_widget.setLayout(QHBoxLayout())
		beam_widget.layout().setContentsMargins(0,0,0,0)

		# Add a radio group to choose the selected formulation (DISTRIBUTED - LUMPED FL - LUMPED ZL)
		group_radios = QFrame()
		group_radios.setFrameShape(QFrame.StyledPanel)
		group_radios.setFrameShadow(QFrame.Sunken)
		label = QLabel('<b>Select the desidered formulation</b>')
		# Create the radio buttons for the available formulations
		self.radioDistributed = QRadioButton("&Distributed plasticity")
		self.radioLumpedFL = QRadioButton("&Lumped plasticity with finite length hinge")
		self.radioLumpedZL = QRadioButton("Lumped plasicity with &zeroLength hinge")
		#Set the layout of the radio group
		group_radios.setLayout(QVBoxLayout())
		group_radios.layout().addWidget(label)
		group_radios.layout().addWidget(self.radioDistributed)
		group_radios.layout().addWidget(self.radioLumpedFL)
		group_radios.layout().addWidget(self.radioLumpedZL)
		group_radios.layout().addStretch(1)
		# Add to the layout
		beam_widget.layout().addWidget(group_radios)

		#Create a container widget for the three beam widgets
		containerBeamWidgets = QFrame()
		containerBeamWidgets.setFrameShape(QFrame.StyledPanel)
		containerBeamWidgets.setFrameShadow(QFrame.Sunken)
		containerBeamWidgets.setLayout(QHBoxLayout())
		containerBeamWidgets.layout().setContentsMargins(0,0,0,0)

		# Create the widget for distributed plasticity
		self.widgetDistributed = distributedWidgetPP(self.xobj)
		# self.widgetDistributed.setMinimumSize(QSize(500,800))

		# Add the widget for lumped plasticity with finite length
		self.widgetLumpedFL = lumpedFLWidgetPP(self.xobj)

		# Add the widget for lumped plasticity with zero length
		self.widgetLumpedZL = lumpedZLWidgetPP(self.xobj)

		# Add to the container the three widgets
		containerBeamWidgets.layout().addWidget(self.widgetDistributed)
		containerBeamWidgets.layout().addWidget(self.widgetLumpedFL)
		containerBeamWidgets.layout().addWidget(self.widgetLumpedZL)
		
		# Add the container Widget in a Scroll Area
		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		# scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		# TODO: solve bug and fix minimum size for this widget.
		scroll.setWidget(containerBeamWidgets)
		
		# Add the Preview in the right. For now it is a static image.
		# In future it will be a CAD dynamic preview
		imgContainer = QWidget()
		imgContainer.setLayout(QVBoxLayout())
		imgContainer.layout().setContentsMargins(0,0,0,0)
		# Image
		filename = __file__
		folder = os.path.dirname(filename)
		default_img = "RCbeamColumnProperty_support_data/img/distributed.png"
		abs_default_img = os.path.abspath(os.path.join(folder, default_img))
		
		pixmap = QPixmap(abs_default_img)
		self.lblImagePreview = QLabel()
		self.lblImagePreview.setPixmap(pixmap)
		self.lblImagePreview.setScaledContents(False)
		self.lblImagePreview.setMinimumSize(QSize(191,253))
		self.lblImagePreview.setMaximumSize(QSize(191,253))
		self.lblImagePreview.setStyleSheet("background-color: white")
		imgContainer.layout().addWidget(self.lblImagePreview)
		lbl = QLabel('Preview')
		lbl.setAlignment(Qt.AlignCenter)
		imgContainer.layout().addWidget(lbl)
		imgContainer.layout().addStretch(1)

		# Add to the layout
		beam_widget.layout().addWidget(scroll)
		beam_widget.layout().addWidget(imgContainer)
		beam_widget.layout().setStretch(0, .1)
		beam_widget.layout().setStretch(1, 4)
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::__init__\t\t\t->\tAdding beam_widget')
		self.layout().addWidget(beam_widget)
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::__init__\t\t\t->\tAdded beam_widget')

		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::__init__\t\t\t->\tAdding the widget to the main editor with shiboken')
		# we want to add this widget to the xobject editor
		# on the right of the main tree widget used for the editing of xobject attributes.
		self.editor_splitter = shiboken2.wrapInstance(editor.getChildPtr(MpcXObjectEditorChildCode.MainSplitter), QSplitter)
		self.editor_splitter.addWidget(self)
		total_width = self.editor_splitter.size().width()
		width_1 = 0
		self.editor_splitter.setSizes([width_1, total_width - width_1])
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::__init__\t\t\t->\tAdded the widget to the main editor')
		
		# No connection here, so called the toggled function. It should initialize
		# Read Datastore or load default values
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::__init__\t\t\t->\tReading the saved formulation or selecting by default distributed')
		# Read datastore attribute or load defaults (should be in the first opening, or the first use of a formulation module
		data = self.xobj.getAttribute(MpcXObjectMetaData.dataStoreAttributeName())
		if data is None:
			raise Exception("Cannot find dataStore Attribute")
		ds = data.string
		try:
			jds = json.loads(ds)
			jds = jds['RCBeamColumnPhysicalProperty']
			#Load data if present
			formulation = jds.get('formulation','distr')
		except:
			formulation = 'distr'
		# Selecting the right radio from the formulation saved
		self.radioDistributed.setChecked (False)
		self.radioLumpedFL.setChecked(False)
		self.radioLumpedZL.setChecked(False)
		if formulation == 'distr':
			self.radioDistributed.setChecked (True)
		elif formulation == 'lumpedFL':
			self.radioLumpedFL.setChecked(True)
		elif formulation == 'lumpedZL':
			self.radioLumpedZL.setChecked(True)
			
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::__init__\t\t\t->\tCalling toggled radio (connections not set yet)')
		self.toggledRadio()
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::__init__\t\t\t->\tCalled toggled radio, now setting connections')
		
		# Set the connections
		# show the correct widget when the correspondent radio is selected:
		# Distributed Widget
		self.radioDistributed.toggled.connect(self.toggledRadio)
		# Lumped with finite length hinge
		self.radioLumpedFL.toggled.connect(self.toggledRadio)
		# Lumped with zero length hinge
		self.radioLumpedZL.toggled.connect(self.toggledRadio)
		
	
		
	def toggledRadio(self):
		# Should not be needed the following block: erase later
		# # First thing: block the signals in order to not call recursively this function
		# # blocking signals
		# if RCBeamColumnWidget._debug:
			# print('RCBeamColumnProperty::toggledRadio\t\t\t->\tBlocking signals of radio buttons')
		# locks = [
			# QSignalBlocker(self.radioDistributed),
			# QSignalBlocker(self.radioLumpedFL),
			# QSignalBlocker(self.radioLumpedZL),
			# ]
			
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::toggledRadio\t\t\t->\tCalling readDatastore to retrieve saved data on datastore to be used if the user goes back to the previous widget')
		model = readDatastore(self.xobj)
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::toggledRadio\t\t\t->\tFrom datastore read the following cross section: {}'.format(model.crossSection))
			
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::toggleRadio\t\t\t->\tChanged the radio button')
		if self.radioDistributed.isChecked():
			if RCBeamColumnWidget._debug:
				print('RCBeamColumnProperty::toggledRadio\t\t\t->\tChecked radioDistributed')
			# check if saved in datastore is distributed
			
			if model.formulation == 'distr':
				if RCBeamColumnWidget._debug:
					print('RCBeamColumnProperty::toggledRadio\t\t\t->\tIn datastore there is distributed, load that')
			else:
				if RCBeamColumnWidget._debug:
					print('RCBeamColumnProperty::toggledRadio\t\t\t->\tIn datastore there is not distributed, load default values for that')
				formulation = 'distr'
				model = defaultsForFormulation(formulation)
			# Initialize the widget
			if RCBeamColumnWidget._debug:
				print('RCBeamColumnProperty::toggledRadio\t\t\t->\tInitializing the distributed widget with the model obtained from dataStore or generated from default')
			self.widgetDistributed.initialize(model, self.lblImagePreview)
			# Show the correct widget
			self.widgetDistributed.show()
			# Hide the other widgets
			self.widgetLumpedFL.hide()
			self.widgetLumpedZL.hide()
			return
		if self.radioLumpedFL.isChecked():
			if RCBeamColumnWidget._debug:
				print('RCBeamColumnProperty::toggledRadio\t\t\t->\tChecked radioLumpedFL')
			# check if saved in datastore is distributed
			
			if model.formulation == 'lumpedFL':
				if RCBeamColumnWidget._debug:
					print('RCBeamColumnProperty::toggledRadio\t\t\t->\tIn datastore there is lumpedFL, load that')
			else:
				if RCBeamColumnWidget._debug:
					print('RCBeamColumnProperty::toggledRadio\t\t\t->\tIn datastore there is not lumpedFL, load default values for that')
				formulation = 'lumpedFL'
				model = defaultsForFormulation(formulation)
			# Initialize the widget
			if RCBeamColumnWidget._debug:
				print('\t\t\tcross Section passed to initialize: {}'.format(model.crossSection))
			if RCBeamColumnWidget._debug:
				print('RCBeamColumnProperty::toggledRadio\t\t\t->\tInitializing the lumpedFL widget with the model obtained from dataStore or generated from default')
			self.widgetLumpedFL.initialize(model, self.lblImagePreview)
			# Show the correct widget
			self.widgetLumpedFL.show()
			# Hide the other widgets
			self.widgetDistributed.hide()
			self.widgetLumpedZL.hide()
			return
		if self.radioLumpedZL.isChecked():
			if RCBeamColumnWidget._debug:
				print('RCBeamColumnProperty::toggledRadio\t\t\t->\tChecked radioLumpedZL')
			# check if saved in datastore is distributed
			
			if model.formulation == 'lumpedZL':
				if RCBeamColumnWidget._debug:
					print('RCBeamColumnProperty::toggledRadio\t\t\t->\tIn datastore there is lumpedZL, load that')
			else:
				if RCBeamColumnWidget._debug:
					print('RCBeamColumnProperty::toggledRadio\t\t\t->\tIn datastore there is not lumpedZL, load default values for that')
				formulation = 'lumpedZL'
				model = defaultsForFormulation(formulation)
			# Initialize the widget
			if RCBeamColumnWidget._debug:
				print('\t\t\tcross Section passed to initialize: {}'.format(model.crossSection))
			if RCBeamColumnWidget._debug:
				print('RCBeamColumnProperty::toggledRadio\t\t\t->\tInitializing the lumpedZL widget with the model obtained from dataStore or generated from default')
			self.widgetLumpedZL.initialize(model, self.lblImagePreview)
			# Show the correct widget
			self.widgetLumpedZL.show()
			# Hide the other widgets
			self.widgetDistributed.hide()
			self.widgetLumpedFL.hide()
			return
		
	def onEditFinished(self):
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::onEditFinished\t\t\t->\tEdit finished. Checking data and Saving data to datastore')
		# 
		# Saving data on datastore xobj
		
		#Get the formulation chosen by the user
		if self.radioDistributed.isChecked():
			formulation = 'distr'
		if self.radioLumpedFL.isChecked():
			formulation = 'lumpedFL'
		if self.radioLumpedZL.isChecked():
			formulation = 'lumpedZL'
		
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
			
		if formulation == 'distr':
			# Save everything needed for distributed formulation
			jds['RCBeamColumnPhysicalProperty'] = {
				'version': _constants.version,
				'dimension': self.widgetDistributed.model.dimension,
				'formulation': self.widgetDistributed.model.formulation,
				'distr.integration': self.widgetDistributed.model.integration,
				'distr.numIntPts': self.widgetDistributed.model.numIntPts,
				'distr.sameSection': self.widgetDistributed.model.sameSection,
				'distr.includeShearVy': self.widgetDistributed.model.includeShearVy,
				'distr.shearVy': MpcIndexVectorWrapper(self.widgetDistributed.model.shearVy, MpcAttributeIndexSourceType.PhysicalProperty),
				'distr.includeShearVz': self.widgetDistributed.model.includeShearVz,
				'distr.shearVz': MpcIndexVectorWrapper(self.widgetDistributed.model.shearVz, MpcAttributeIndexSourceType.PhysicalProperty),
				'distr.includeTorsion': self.widgetDistributed.model.includeTorsion,
				'distr.torsion': MpcIndexVectorWrapper(self.widgetDistributed.model.torsion, MpcAttributeIndexSourceType.PhysicalProperty),
				'distr.crossSection': MpcIndexVectorWrapper(self.widgetDistributed.model.crossSection, MpcAttributeIndexSourceType.PhysicalProperty),
				'distr.currentSection': self.widgetDistributed.model.currentSection,
				'distr.PMMinteraction': self.widgetDistributed.model.PMMinteraction,
				'distr.includePmaterial': self.widgetDistributed.model.includePmaterial,
				'distr.materialP': MpcIndexVectorWrapper(self.widgetDistributed.model.materialP, MpcAttributeIndexSourceType.PhysicalProperty),
				'distr.includeMyMaterial': self.widgetDistributed.model.includeMyMaterial,
				'distr.includeMzMaterial': self.widgetDistributed.model.includeMzMaterial,
				'distr.materialMy': MpcIndexVectorWrapper(self.widgetDistributed.model.materialMy, MpcAttributeIndexSourceType.PhysicalProperty),
				'distr.materialMz': MpcIndexVectorWrapper(self.widgetDistributed.model.materialMz, MpcAttributeIndexSourceType.PhysicalProperty),
			}
			data.string = json.dumps(jds, indent=4, cls=MpcDataStoreEncoder)
		elif formulation == 'lumpedFL':
			# Save everything needed for distributed formulation
			# TODO: check if everything is ok, otherwise send Warnings or Critical errors
			
			jds['RCBeamColumnPhysicalProperty'] = {
				'version': _constants.version,
				'dimension': self.widgetLumpedFL.model.dimension,
				'formulation': self.widgetLumpedFL.model.formulation,
				'lumpedFL.integration': self.widgetLumpedFL.model.integration,
				'lumpedFL.numIntPts': self.widgetLumpedFL.model.numIntPts,
				'lumpedFL.sameSection': self.widgetLumpedFL.model.sameSection,
				'lumpedFL.includeShearVy': self.widgetLumpedFL.model.includeShearVy,
				'lumpedFL.shearVy': MpcIndexVectorWrapper(self.widgetLumpedFL.model.shearVy, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedFL.includeShearVz': self.widgetLumpedFL.model.includeShearVz,
				'lumpedFL.shearVz': MpcIndexVectorWrapper(self.widgetLumpedFL.model.shearVz, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedFL.includeTorsion': self.widgetLumpedFL.model.includeTorsion,
				'lumpedFL.torsion': MpcIndexVectorWrapper(self.widgetLumpedFL.model.torsion, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedFL.crossSection': MpcIndexVectorWrapper(self.widgetLumpedFL.model.crossSection, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedFL.currentSection': self.widgetLumpedFL.model.currentSection,
				'lumpedFL.PMMinteraction': self.widgetLumpedFL.model.PMMinteraction,
				'lumpedFL.includePmaterial': self.widgetLumpedFL.model.includePmaterial,
				'lumpedFL.materialP': MpcIndexVectorWrapper(self.widgetLumpedFL.model.materialP, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedFL.includeMyMaterial': self.widgetLumpedFL.model.includeMyMaterial,
				'lumpedFL.includeMzMaterial': self.widgetLumpedFL.model.includeMzMaterial,
				'lumpedFL.materialMy': MpcIndexVectorWrapper(self.widgetLumpedFL.model.materialMy, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedFL.materialMz': MpcIndexVectorWrapper(self.widgetLumpedFL.model.materialMz, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedFL.automaticHingeLength': self.widgetLumpedFL.model.automaticHingeLength,
				'lumpedFL.hingeLengthI': self.widgetLumpedFL.model.hingeLengthI,
				'lumpedFL.hingeLengthJ': self.widgetLumpedFL.model.hingeLengthJ,
			}
			data.string = json.dumps(jds, indent=4, cls = MpcDataStoreEncoder)
		elif formulation == 'lumpedZL':
			# Save everything needed for distributed formulation

			jds['RCBeamColumnPhysicalProperty'] = {
				'version': _constants.version,
				'dimension': self.widgetLumpedZL.model.dimension,
				'formulation': self.widgetLumpedZL.model.formulation,
				'lumpedZL.numIntPts': self.widgetLumpedZL.model.numIntPts,
				'lumpedZL.sameSection': self.widgetLumpedZL.model.sameSection,
				'lumpedZL.includeShearVy': self.widgetLumpedZL.model.includeShearVy,
				'lumpedZL.shearVy': MpcIndexVectorWrapper(self.widgetLumpedZL.model.shearVy, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedZL.includeShearVz': self.widgetLumpedZL.model.includeShearVz,
				'lumpedZL.shearVz': MpcIndexVectorWrapper(self.widgetLumpedZL.model.shearVz, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedZL.includeTorsion': self.widgetLumpedZL.model.includeTorsion,
				'lumpedZL.torsion': MpcIndexVectorWrapper(self.widgetLumpedZL.model.torsion, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedZL.crossSection': MpcIndexVectorWrapper(self.widgetLumpedZL.model.crossSection, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedZL.currentSection': self.widgetLumpedZL.model.currentSection,
				'lumpedZL.includePmaterial': self.widgetLumpedZL.model.includePmaterial,
				'lumpedZL.materialP': MpcIndexVectorWrapper(self.widgetLumpedZL.model.materialP, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedZL.includeMyMaterial': self.widgetLumpedZL.model.includeMyMaterial,
				'lumpedZL.includeMzMaterial': self.widgetLumpedZL.model.includeMzMaterial,
				'lumpedZL.materialMy': MpcIndexVectorWrapper(self.widgetLumpedZL.model.materialMy, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedZL.materialMz': MpcIndexVectorWrapper(self.widgetLumpedZL.model.materialMz, MpcAttributeIndexSourceType.PhysicalProperty),
				'lumpedZL.automaticHingeLength': self.widgetLumpedZL.model.automaticHingeLength,
				'lumpedZL.hingeLengthI': self.widgetLumpedZL.model.hingeLengthI,
				'lumpedZL.hingeLengthJ': self.widgetLumpedZL.model.hingeLengthJ,
			}
			data.string = json.dumps(jds, indent=4, cls = MpcDataStoreEncoder)
		#################################################### $JSON
		
		if RCBeamColumnWidget._debug:
			print('RCBeamColumnProperty::onEditFinished\t\t\t->\tData saved to data store: {}'.format(data.string))


def makeXObjectMetaData():

	xom = MpcXObjectMetaData()
	xom.name = 'RCBeamColumnProperty'
	xom.Xgroup = 'Beam-Column'
	
	# add a last attribute for versioning
	av = MpcAttributeMetaData()
	av.type = MpcAttributeType.Integer
	av.description = (
		html_par('Version {}'.format(_constants.version))
		)
	av.name = 'version'
	av.setDefault(_constants.version)
	av.editable = False
	xom.addAttribute(av)

	return xom

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def makeExtrusionBeamDataCompoundInfo(xobj):

	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')

	info = MpcSectionExtrusionBeamDataCompoundInfo()
	'''
	here the property that has the extrusion source (MpcBeamFiberSection)
	is the property whose id is stored in the attribute 'sectionTag', and not
	this property (Aggregator). So we first get the attribute and check
	whether the user decided to use a fiber beam cross section for the P-My-Mz part
	of the Aggregator. If so, get the indexed property from the document. That
	will be the one containing the extrusion source. See the opensees.physical_properties.sections.Fiber.py module.
	'''
	# get the model from the datastore
	try:
		model = readDatastore(xobj)
		if model.formulation == 'distr':
			# Distributed formulation - Lobatto or USER (only if not same Section)
			is_param = True
			is_gap = False
			if model.sameSection:
				# Single section with lobatto standard rule:
				secTag = model.crossSection[0]
				prop = doc.getPhysicalProperty(secTag)
				info_item = exutils.getExtrusionDataSingleItem(prop)
				info.add(info_item.property, 1.0, is_param, is_gap, info_item.yOffset, info_item.zOffset)
				return info
			else:
				# Multiple sections with user rule, replicating lobatto 5 GP scheme
				n = model.numIntPts
				secTag = model.crossSection
				weights = bsutils.beam_int_lobatto.get_weights(n)
				'''
				here we allow some of the n properties to be None. but not all of them!
				'''
				num_valid = 0
				processed_info_items = [None]*n
				for i in range(n):
					prop = doc.getPhysicalProperty(secTag[i])
					info_item = exutils.getExtrusionDataSingleItem(prop)
					processed_info_items[i] = info_item
					if info_item is not None:
						num_valid += 1
				if num_valid == 0:
					return info # quick return
				'''
				fill info
				'''
				exutils.checkOffsetCompatibility(processed_info_items)
				for i in range(n):
					info_item = processed_info_items[i]
					info.add(info_item.property, weights[i], is_param, is_gap, info_item.yOffset, info_item.zOffset)
				return info
		elif model.formulation == 'lumpedFL':
			# lumpedFL formulation - Standard hinge rule
			is_gap = False
			is_param = False
			secTagI = model.crossSection[0]
			secTagE = model.crossSection[1]
			secTagJ = model.crossSection[2]
			# computation of plastic hinge length
			# TODO: move somewhere in utils????
			if not model.automaticHingeLength:
				# user provided custom hinge length
				lpI = model.hingeLengthI
				lpJ = model.hingeLengthJ
				l_E = 1.0
			else:
				# HP: 	standard sections with EC1998-3 eq A.5 have the first term (0.1Lv) that is around 30% of 
				#		plastic hinge length. Thus I estimate the length with this information
				#		Using A.9, Lv/30 is the first term and is 20% of the plastic hinge length. This is 
				#		the commented second case.
				#		In future maybe we can compute this stuff depending on option set by user.
				lpI = 0.167 # 0.1Lv
				lpJ = 0.167 # 0.1Lv
				# lpI = 0.083 # Lv/30
				# lpJ = 0.083 # Lv/30
				l_E = 1.0 - lpI - lpJ
				is_param = True
			'''
			here we allow some of the n properties to be None. but not all of them!
			'''
			prop_I = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagI))
			prop_J = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagJ))
			prop_E = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagE))
			if (prop_I is None) and (prop_J is None) and (prop_E is None):
				return info # quick return
			'''
			fill info.
			'''
			# print(prop_I, prop_J, prop_E)
			exutils.checkOffsetCompatibility([prop_I, prop_E, prop_J])
			info.add(prop_I.property, lpI, is_param, is_gap, prop_I.yOffset, prop_I.zOffset)
			info.add(None, 0.0, False, is_gap, 0, 0)
			info.add(prop_E.property, l_E, True, is_gap, prop_E.yOffset, prop_E.zOffset)
			info.add(None, 0.0, False, is_gap, 0, 0)
			info.add(prop_J.property, lpJ, is_param, is_gap, prop_J.yOffset, prop_J.zOffset)
			return info
		elif model.formulation == 'lumpedZL':
			# lumpedFL formulation - Standard hinge rule
			is_gap = False
			is_param = False
			secTagE = model.crossSection[1]
			# computation of plastic hinge length
			# TODO: move somewhere in utils????
			if not model.automaticHingeLength:
				# user provided custom hinge length
				lpI = model.hingeLengthI
				lpJ = model.hingeLengthJ
				l_E = 1.0
			else:
				# HP: 	standard sections with EC1998-3 eq A.5 have the first term (0.1Lv) that is around 30% of 
				#		plastic hinge length. Thus I estimate the length with this information
				#		Using A.9, Lv/30 is the first term and is 20% of the plastic hinge length. This is 
				#		the commented second case.
				#		In future maybe we can compute this stuff depending on option set by user.
				lpI = 0.167 # 0.1Lv
				lpJ = 0.167 # 0.1Lv
				# lpI = 0.083 # Lv/30
				# lpJ = 0.083 # Lv/30
				l_E = 1.0 - lpI - lpJ
				is_param = True

			prop_E = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagE))
			if (prop_E is None):
				return info # quick return
			'''
			fill info.
			'''
			# print(prop_I, prop_J, prop_E)
			info.add(None, 0.05, True, True, prop_E.yOffset, prop_E.zOffset)
			info.add(prop_E.property, 0.9, True, False, prop_E.yOffset, prop_E.zOffset)
			info.add(None, 0.05, True, True, prop_E.yOffset, prop_E.zOffset)
			return info
	except Exception:
		IO.write_cerr('WARNING: impossibile to get model from datastore\n')
		raise
	finally:
		return info

def getSectionOffset(xobj):
	offset_y = 0.0
	offset_z = 0.0
	info = makeExtrusionBeamDataCompoundInfo(xobj)
	if info is not None:
		if len(info.items) > 0:
			item = info.items[0]
			offset_y = item.yOffset
			offset_z = item.zOffset
	return offset_y, offset_z

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
	_constants.gui = RCBeamColumnWidget(editor,xobj)
	
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
		
	
def defaultsForFormulation(formulation):
	dimension = '3D'
	if formulation == 'distr':
		integration = 'Lobatto'
		numIntPts = 5
		sameSection = True
		includeShearVy = [False] * numIntPts
		includeShearVz = [False] * numIntPts
		shearVy = [0] * numIntPts
		shearVz = [0] * numIntPts
		includeTorsion = [False] * numIntPts
		torsion = [0] * numIntPts
		crossSection = [0] * numIntPts
		PMMinteraction = True
		includePmaterial = [False] * numIntPts
		materialP = [0] * numIntPts
		includeMyMaterial = [False] * numIntPts
		materialMy = [0] * numIntPts
		includeMzMaterial = [False] * numIntPts
		materialMz = [0] * numIntPts
		currentSection = 0
		model = modelDistributed(dimension, integration, numIntPts, sameSection, currentSection, crossSection, PMMinteraction, includePmaterial, materialP, includeMyMaterial, materialMy, includeMzMaterial, materialMz, includeShearVy, shearVy, includeShearVz, shearVz, includeTorsion, torsion)
	elif formulation == 'lumpedFL':
		integration = 'HingeRadau'
		numIntPts = 3
		sameSection = True
		includeShearVy = [False] * numIntPts
		includeShearVz = [False] * numIntPts
		shearVy = [0] * numIntPts
		shearVz = [0] * numIntPts
		includeTorsion = [False] * numIntPts
		torsion = [0] * numIntPts
		crossSection = [0] * numIntPts
		PMMinteraction = True
		includePmaterial = [False] * numIntPts
		materialP = [0] * numIntPts
		includeMyMaterial = [False] * numIntPts
		materialMy = [0] * numIntPts
		includeMzMaterial = [False] * numIntPts
		materialMz = [0] * numIntPts
		currentSection = 0
		autoHingeLength = True
		hingeLengthI = 0
		hingeLengthJ = 0
		model = modelLumpedFL(dimension, integration, numIntPts, sameSection, currentSection, crossSection, PMMinteraction, includePmaterial, materialP, includeMyMaterial, materialMy, includeMzMaterial, materialMz, includeShearVy, shearVy, includeShearVz, shearVz, includeTorsion, torsion, autoHingeLength, hingeLengthI, hingeLengthJ)
	elif formulation == 'lumpedZL':
		numIntPts = 3
		sameSection = True
		includeShearVy = [False] * numIntPts
		includeShearVz = [False] * numIntPts
		shearVy = [0] * numIntPts
		shearVz = [0] * numIntPts
		includeTorsion = [False] * numIntPts
		torsion = [0] * numIntPts
		crossSection = [0] * numIntPts
		includePmaterial = [False] * numIntPts
		materialP = [0] * numIntPts
		includeMyMaterial = [False] * numIntPts
		materialMy = [0] * numIntPts
		includeMzMaterial = [False] * numIntPts
		materialMz = [0] * numIntPts
		currentSection = 0
		autoHingeLength = True
		hingeLengthI = 0
		hingeLengthJ = 0
		model = modelLumpedZL(dimension, numIntPts, sameSection, currentSection, crossSection, includePmaterial, materialP, includeMyMaterial, materialMy, includeMzMaterial, materialMz, includeShearVy, shearVy, includeShearVz, shearVz, includeTorsion, torsion, autoHingeLength, hingeLengthI, hingeLengthJ)
	else:
		return None
	
	return model
		
def readDatastore(xobj):
	# Try to read datastore or create default data
	# This method will be called the first time the module is loaded and every other time the formulation is changed.
	
	# Read datastore attribute or load defaults (should be in the first opening, or the first use of a formulation module
	data = xobj.getAttribute(MpcXObjectMetaData.dataStoreAttributeName())
	if data is None:
		raise Exception("Cannot find dataStore Attribute")
	ds = data.string
	if RCBeamColumnWidget._debug:
		print('RCBeamColumnProperty::readDatastore\t\t\t->\tdata: {} .'.format(data.string))
	
	try:
		jds = json.loads(ds, cls = MpcDataStoreDecoder)
		jds = jds['RCBeamColumnPhysicalProperty']
		#Load data if present
		dimension = jds.get('dimension','3D')
		formulation = jds.get('formulation','distr')
		if formulation == 'distr':
			if RCBeamColumnWidget._debug:
				print('reading dataStore distr')
			integration = jds.get('distr.integration','Lobatto')
			numIntPts = jds.get('distr.numIntPts',5)
			sameSection = jds.get('distr.sameSection',True)
			includeShearVy = jds.get('distr.includeShearVy',[False] * numIntPts)
			includeShearVz = jds.get('distr.includeShearVz',[False] * numIntPts)
			shearVyVID = jds.get('distr.shearVy',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			shearVy = []
			for s in shearVyVID.value:
				shearVy.append(s)
			shearVzVID = jds.get('distr.shearVz',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			shearVz = []
			for s in shearVzVID.value:
				shearVz.append(s)
			includeTorsion = jds.get('distr.includeTorsion',[False] * numIntPts)
			torsionVID = jds.get('distr.torsion',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			torsion = []
			for s in torsionVID.value:
				torsion.append(s)
			crossSectionVID = jds.get('distr.crossSection',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			crossSection = []
			for s in crossSectionVID.value:
				crossSection.append(s)
			currentSection = jds.get('distr.currentSection',0)
			PMMinteraction = jds.get('distr.PMMinteraction', True)
			includePmaterial = jds.get('distr.includePmaterial', [False] * numIntPts)
			materialPVID = jds.get('distr.materialP', MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			materialP = []
			for s in materialPVID.value:
				materialP.append(s)
			includeMyMaterial = jds.get('distr.includeMyMaterial', [False] * numIntPts)
			includeMzMaterial = jds.get('distr.includeMzMaterial', [False] * numIntPts)
			materialMyVID = jds.get('distr.materialMy', MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			materialMy = []
			for s in materialMyVID.value:
				materialMy.append(s)
			materialMzVID = jds.get('distr.materialMz', MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			materialMz = []
			for s in materialMzVID.value:
				materialMz.append(s)
			model = modelDistributed(dimension, integration, numIntPts, sameSection, currentSection, crossSection, PMMinteraction, includePmaterial, materialP, includeMyMaterial, materialMy, includeMzMaterial, materialMz, includeShearVy, shearVy, includeShearVz, shearVz, includeTorsion, torsion)
		elif formulation == 'lumpedFL':
			if RCBeamColumnWidget._debug:
				print('reading dataStore lumpedFL')
			integration = jds.get('lumpedFL.integration','HingeRadau')
			numIntPts = 3 # 2 plastic hinges and internal section (generally elastic)
			sameSection = jds.get('lumpedFL.sameSection',True)
			includeShearVy = jds.get('lumpedFL.includeShearVy',[False] * numIntPts)
			includeShearVz = jds.get('lumpedFL.includeShearVz',[False] * numIntPts)
			shearVyVID = jds.get('lumpedFL.shearVy',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			shearVy = []
			for s in shearVyVID.value:
				shearVy.append(s)
			shearVzVID = jds.get('lumpedFL.shearVz',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			shearVz = []
			for s in shearVzVID.value:
				shearVz.append(s)
			includeTorsion = jds.get('lumpedFL.includeTorsion',[False] * numIntPts)
			torsionVID = jds.get('lumpedFL.torsion',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			torsion = []
			for s in torsionVID.value:
				torsion.append(s)
			crossSectionVID = jds.get('lumpedFL.crossSection',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			crossSection = []
			for s in crossSectionVID.value:
				crossSection.append(s)
			currentSection = jds.get('lumpedFL.currentSection',0)
			PMMinteraction = jds.get('lumpedFL.PMMinteraction', True)
			includePmaterial = jds.get('lumpedFL.includePmaterial', [False] * numIntPts)
			materialPVID = jds.get('lumpedFL.materialP', MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			materialP = []
			for s in materialPVID.value:
				materialP.append(s)
			includeMyMaterial = jds.get('lumpedFL.includeMyMaterial', [False] * numIntPts)
			includeMzMaterial = jds.get('lumpedFL.includeMzMaterial', [False] * numIntPts)
			materialMyVID = jds.get('lumpedFL.materialMy', MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			materialMy = []
			for s in materialMyVID.value:
				materialMy.append(s)
			materialMzVID = jds.get('lumpedFL.materialMz', MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			materialMz = []
			for s in materialMzVID.value:
				materialMz.append(s)
			autoHingeLength = jds.get('lumpedFL.automaticHingeLength', True)
			hingeLengthI = jds.get('lumpedFL.hingeLengthI', 0)
			hingeLengthJ = jds.get('lumpedFL.hingeLengthJ', 0)
			model = modelLumpedFL(dimension, integration, numIntPts, sameSection, currentSection, crossSection, PMMinteraction, includePmaterial, materialP, includeMyMaterial, materialMy, includeMzMaterial, materialMz, includeShearVy, shearVy, includeShearVz, shearVz, includeTorsion, torsion, autoHingeLength, hingeLengthI, hingeLengthJ)
		elif formulation == 'lumpedZL':
			if RCBeamColumnWidget._debug:
				print('reading dataStore lumpedZL')
			numIntPts = 3 # 2 plastic hinges and internal section (generally elastic)
			sameSection = jds.get('lumpedZL.sameSection',True)
			includeShearVy = jds.get('lumpedZL.includeShearVy',[False] * numIntPts)
			includeShearVz = jds.get('lumpedZL.includeShearVz',[False] * numIntPts)
			shearVyVID = jds.get('lumpedZL.shearVy',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			shearVy = []
			for s in shearVyVID.value:
				shearVy.append(s)
			shearVzVID = jds.get('lumpedZL.shearVz',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			shearVz = []
			for s in shearVzVID.value:
				shearVz.append(s)
			includeTorsion = jds.get('lumpedZL.includeTorsion',[False] * numIntPts)
			torsionVID = jds.get('lumpedZL.torsion',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			torsion = []
			for s in torsionVID.value:
				torsion.append(s)
			crossSectionVID = jds.get('lumpedZL.crossSection',MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			crossSection = []
			for s in crossSectionVID.value:
				crossSection.append(s)
			currentSection = jds.get('lumpedZL.currentSection',0)
			includePmaterial = jds.get('lumpedZL.includePmaterial', [False] * numIntPts)
			materialPVID = jds.get('lumpedZL.materialP', MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			materialP = []
			for s in materialPVID.value:
				materialP.append(s)
			includeMyMaterial = jds.get('lumpedZL.includeMyMaterial', [False] * numIntPts)
			includeMzMaterial = jds.get('lumpedZL.includeMzMaterial', [False] * numIntPts)
			materialMyVID = jds.get('lumpedZL.materialMy', MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			materialMy = []
			for s in materialMyVID.value:
				materialMy.append(s)
			materialMzVID = jds.get('lumpedZL.materialMz', MpcIndexVectorWrapper([0] * numIntPts, MpcAttributeIndexSourceType.PhysicalProperty))
			materialMz = []
			for s in materialMzVID.value:
				materialMz.append(s)
			autoHingeLength = jds.get('lumpedZL.automaticHingeLength', True)
			hingeLengthI = jds.get('lumpedZL.hingeLengthI', 0)
			hingeLengthJ = jds.get('lumpedZL.hingeLengthJ', 0)
			model = modelLumpedZL(dimension, numIntPts, sameSection, currentSection, crossSection, includePmaterial, materialP, includeMyMaterial, materialMy, includeMzMaterial, materialMz, includeShearVy, shearVy, includeShearVz, shearVz, includeTorsion, torsion, autoHingeLength, hingeLengthI, hingeLengthJ)
		# TO DO:
		# Check that indexes of CrossSection, ShearVy, ShearVz, Torsion are in the data of the combo boxes,
		# Otherwise take defaults.
	except:
		# exdata = traceback.format_exc().splitlines()
		# PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
		# if impossible to load, load default values:
			# Distributed plasticity with 5 point Lobatto Integration
			# No Shear Aggregators
			# No torsion Aggregator
			# None cross section
			# All the same sections
			# PMM accounted by fiber section
		IO.write_cerr('impossible to read dataStore, load default - distributed formulation\n')
		if RCBeamColumnWidget._debug:
			print('impossible to read dataStore, load dafault - distributed formulation')
		formulation = 'distr'
		model = defaultsForFormulation(formulation)
	# End Loading DATA
	# LOADED SAVED VALUES FROM JSON (OR DEFAULT) IF JSON IS EMPY
	return model
