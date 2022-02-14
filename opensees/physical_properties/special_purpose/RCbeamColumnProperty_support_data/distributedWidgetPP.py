from PyMpc import *
import opensees.physical_properties.utils.GuiUtils as gu
# Import the section navigator
from opensees.physical_properties.special_purpose.RCbeamColumnProperty_support_data.sectionsNavigator import SectionsNavigator
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
import opensees.physical_properties.special_purpose.beam_section_utils as bsutils
import traceback
import PyMpc
import PyMpc.App
import os


# INTEGRATION AND POINTS REMOVED ON 04/09/2020 -> the lines are commented with # SET_INTEGRATION
# uncomment to restore the ability. By default it is setted with 5 integration points and Gauss Lobatto integration.

class modelDistributed:
	def __init__(self, dimension, integration, numIntPts, sameSection, currSec, crossSec, PMMinteraction, includePmaterial, materialP, includeMyMaterial, materialMy, includeMzMaterial, materialMz, includeShearVy, shearVy, includeShearVz, shearVz, includeTorsion, torsion ):
		self.formulation = 'distr'
		self.dimension = dimension
		self.integration = integration
		self.numIntPts = numIntPts
		self.sameSection = sameSection
		self.currentSection = currSec
		self.crossSection = crossSec
		self.PMMinteraction = PMMinteraction
		self.includePmaterial = includePmaterial
		self.materialP = materialP
		self.includeMyMaterial = includeMyMaterial
		self.materialMy = materialMy
		self.includeMzMaterial = includeMzMaterial
		self.materialMz = materialMz
		self.includeShearVy = includeShearVy
		self.shearVy = shearVy
		self.includeShearVz = includeShearVz
		self.shearVz = shearVz
		self.includeTorsion = includeTorsion
		self.torsion = torsion
		
from PySide2.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QGridLayout,
	QLabel,
	QComboBox,
	QCheckBox,
	QPushButton,
	QSpinBox,
	)

from PySide2.QtCore import (
	QSignalBlocker,
	)

import shiboken2

class _constants:
	#some constants
	integrationTypes = {"Lobatto": [bsutils.beam_int_lobatto.get_minIntPoints(), bsutils.beam_int_lobatto.get_maxIntPoints()]} #, "Legendre": [1,10], "Radau": [1,10], "NewtonCotes": [2,10], "Trapezoidal": [1,99], "CompositeSimpson": [1,9]}
	allowedSections = ["RectangularFiberSection", "Fiber", "Elastic"]
	fiberSections = ["RectangularFiberSection", "Fiber"]

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

class distributedWidgetPP(QWidget):

	# Class attribute for the activation of Debug printing
	_debug = False

	def __init__(self, xobj, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Save the xobj
		self.xobj = xobj
		
		self.setLayout(QVBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)
		
		# Create the widget specifiying if 3D or 2D
		widgetDimension = QWidget()
		widgetDimension.setLayout(QtWidgets.QFormLayout())
		# ComboBox for dimension of the problem
		self.comboDimension = QComboBox()
		self.comboDimension.addItems(['2D','3D'])
		self.comboDimension.setCurrentIndex(1)
		widgetDimension.layout().addRow(QLabel("Dimension: "),self.comboDimension)
		self.layout().addWidget(widgetDimension)
		self.layout().addWidget(gu.makeHSeparator())
		
		# Create the widget for the definition of the cross Sections
		widgetCrossSection = QWidget()
		widgetCrossSection.setLayout(QVBoxLayout())
		# widgetCrossSection.layout().setContentsMargins(0,0,0,0)
		# Title of the cross section widget
		widgetCrossSection.layout().addWidget(QLabel('<b>Cross Sections (PMM interaction)</b>'))
		# Container HBox Widget: Left controls - Right Preview
		widget1 = QWidget()
		widget1.setLayout(QHBoxLayout())
		widget1.layout().setContentsMargins(0,0,0,0)
		# Container of controls VBox Widget
		widget2 = QWidget()
		widget2.setLayout(QVBoxLayout())
		widget2.layout().setContentsMargins(0,0,0,0)
		# Label
		widget2.layout().addWidget(QLabel('Select Cross Section'))
		# Combobox for section selection
		self.comboSection = QComboBox()
		self.comboSection.addItem("None", 0)
		# Do a loop for getting the sections (Rectangular for the moment? or also general?)
		tag = self.xobj.parent.componentId
		# get document, we need it to get sections
		doc = App.caeDocument()
		if doc is None:
			raise Exception('no active cae document')
		# Cycle all physical properties and add to the map of the alowed sections
		for item_id, item in doc.physicalProperties.items():
			if item_id >= tag:
				break
			if item.XObject is None:
				raise Exception('null XObject in physical property')
			if item.XObject.Xnamespace.startswith('sections'):
				if item.XObject.name in _constants.allowedSections:
					str = "{}: {}".format(item_id,item.XObject.parent.componentName)
					self.comboSection.addItem(str, item_id)
		widget2.layout().addWidget(self.comboSection)
		widget2.layout().addStretch(1)
		
		# Preview of the section
		self.widgetSceneContainer = QWidget()
		self.widgetSceneContainer.setLayout(QVBoxLayout())
		self.widgetSceneContainer.setContentsMargins(0,0,0,0)
		if self.comboSection.currentData() > 0:
			sec_xobj = doc.getPhysicalProperty(self.comboSection.currentData()).XObject
		self.sec_widget = MpcSceneWidget()
		self.scene_widget = shiboken2.wrapInstance(self.sec_widget.getPtr(), QWidget)
		self.widgetSceneContainer.setMinimumSize(QtCore.QSize(150,150))
		self.widgetSceneContainer.layout().addWidget(self.scene_widget)
		
		widget1.layout().addWidget(widget2)
		widget1.layout().addWidget(self.widgetSceneContainer)
		widgetCrossSection.layout().addWidget(widget1)
		
		# Add possibility to define uncoupled phenomenological laws.
		self.checkBoxPMMinteraction = QCheckBox('Consider PMM interaction by fiber model')
		self.checkBoxPMMinteraction.setChecked(True)
		widgetCrossSection.layout().addWidget(self.checkBoxPMMinteraction)
		widgetPhenomenologicalPMM = QWidget()
		widgetPhenomenologicalPMM.setLayout(QGridLayout())
		widgetPhenomenologicalPMM.layout().setContentsMargins(0,0,0,0)
		# Check and Selection of P
		self.checkBoxMaterialP = QCheckBox("uniaxialMaterial for P (axial):")
		self.comboMaterialP = QComboBox()
		# Check and Selection of My
		self.checkBoxMaterialMy = QCheckBox("uniaxialMaterial for My:")
		self.comboMaterialMy = QComboBox()
		# Check and Selection of Mz
		self.checkBoxMaterialMz = QCheckBox("uniaxialMaterial for Mz:")
		self.comboMaterialMz = QComboBox()
		# Do a loop for getting the uniaxial materials for shear
		# Include possibility to perform automatic computation
		self.comboMaterialP.addItem("None", 0)
		self.comboMaterialMy.addItem("None", 0)
		self.comboMaterialMz.addItem("None", 0)
		# Cycle all physical properties and add to the map of the alowed sections
		for item_id, item in doc.physicalProperties.items():
			if item_id >= tag:
				break
			if item.XObject is None:
				raise Exception('null XObject in physical property')
			if item.XObject.Xnamespace.startswith('materials.uniaxial'):
					str = "{}: {}".format(item_id,item.XObject.parent.componentName)
					self.comboMaterialP.addItem(str, item_id)
					self.comboMaterialMy.addItem(str, item_id)
					self.comboMaterialMz.addItem(str, item_id)
		# Add the controls to the widget
		widgetPhenomenologicalPMM.layout().addWidget(self.checkBoxMaterialP,0,0,1,1)
		widgetPhenomenologicalPMM.layout().addWidget(self.checkBoxMaterialMy,1,0,1,1)
		widgetPhenomenologicalPMM.layout().addWidget(self.checkBoxMaterialMz,2,0,1,1)
		widgetPhenomenologicalPMM.layout().addWidget(self.comboMaterialP,0,1,1,1)
		widgetPhenomenologicalPMM.layout().addWidget(self.comboMaterialMy,1,1,1,1)
		widgetPhenomenologicalPMM.layout().addWidget(self.comboMaterialMz,2,1,1,1)
		
		widgetCrossSection.layout().addWidget(widgetPhenomenologicalPMM)
		
		# Add the widgetCrossSection to the layout of the left widget
		self.layout().addWidget(widgetCrossSection)
		self.layout().addWidget(gu.makeHSeparator())
		
		# Create the widget for the definition of the shear behavior (included as section aggregators)
		widgetShearAggregators = QWidget()
		widgetShearAggregators.setLayout(QGridLayout())
		# widgetShearAggregators.layout().setContentsMargins(11,0,11,0)
		# Title of the cross section widget
		widgetShearAggregators.layout().addWidget(QLabel('<b>Shear behavior (section aggregators)</b>'),0,0,1,2)
		self.checkBoxIncludeShearVy = QCheckBox("Include shear Vy: ")
		self.checkBoxIncludeShearVz = QCheckBox("Include shear Vz: ")
		self.comboShearVy = QComboBox()
		self.comboShearVz = QComboBox()
		# Do a loop for getting the uniaxial materials for shear
		# Include possibility to perform automatic computation
		self.comboShearVy.addItem("None", 0)
		self.comboShearVz.addItem("None", 0)
		# Cycle all physical properties and add to the map of the alowed sections
		for item_id, item in doc.physicalProperties.items():
			if item_id >= tag:
				break
			if item.XObject is None:
				raise Exception('null XObject in physical property')
			if item.XObject.Xnamespace.startswith('materials.uniaxial'):
					str = "{}: {}".format(item_id,item.XObject.parent.componentName)
					self.comboShearVy.addItem(str, item_id)
					self.comboShearVz.addItem(str, item_id)
		
		# Add the controls to the widget
		widgetShearAggregators.layout().addWidget(self.checkBoxIncludeShearVy,1,0,1,1)
		widgetShearAggregators.layout().addWidget(self.checkBoxIncludeShearVz,2,0,1,1)
		widgetShearAggregators.layout().addWidget(self.comboShearVy,1,1,1,1)
		widgetShearAggregators.layout().addWidget(self.comboShearVz,2,1,1,1)
		
		# Add the widgetShearAggregators to the layout of the left widget
		self.layout().addWidget(widgetShearAggregators)
		self.layout().addWidget(gu.makeHSeparator())
		
		# Create the widget for the definition of the torsion behavior (included as section aggregators)
		self.widgetTorsionAggregators = QWidget()
		self.widgetTorsionAggregators.setLayout(QGridLayout())
		# widgetTorsionAggregators.layout().setContentsMargins(11,0,11,0)
		# Title of the cross section widget
		self.widgetTorsionAggregators.layout().addWidget(QLabel('<b>Torsion behavior (section aggregator)</b>'),0,0,1,2)
		self.checkBoxIncludeTorsion = QCheckBox("Include torsion T: ")
		self.comboTorsion = QComboBox()
		# Do a loop for getting the uniaxial materials for shear
		# Include possibility to perform automatic computation: Elastic with GJ
		self.comboTorsion.addItem("None", 0)
		# Cycle all physical properties and add to the map of the alowed sections
		for item_id, item in doc.physicalProperties.items():
			if item_id >= tag:
				break
			if item.XObject is None:
				raise Exception('null XObject in physical property')
			if item.XObject.Xnamespace.startswith('materials.uniaxial'):
					str = "{}: {}".format(item_id,item.XObject.parent.componentName)
					self.comboTorsion.addItem(str, item_id)
		
		# Add the controls to the widget
		self.widgetTorsionAggregators.layout().addWidget(self.checkBoxIncludeTorsion,1,0,1,1)
		self.widgetTorsionAggregators.layout().addWidget(self.comboTorsion,1,1,1,1)
		
		# Add the widgetTorsionAggregators to the layout of the left widget
		self.layout().addWidget(self.widgetTorsionAggregators)
		self.layout().addWidget(gu.makeHSeparator())
		
		# Widget for Navigation of sections
		widgetSectionNavigator = QWidget()
		widgetSectionNavigator.setLayout(QGridLayout())
		# Title of the navigation widget
		widgetSectionNavigator.layout().addWidget(QLabel('<b>Sections navigation</b>'),0,0,1,4)
		self.useSameSections = QCheckBox("Use same sections on all integration points")
		widgetSectionNavigator.layout().addWidget(self.useSameSections,1,0,1,4)
		# Widget SecNav
		self.secNav = SectionsNavigator(n_secs = 5)
		self.secNav.setColor('#D7D7E6')
		self.secNav.setSelectedColor('#46D0FF')
		self.secNav.setCircleRadius(4.0)
		self.secNav.setPadding(4.0)
		widgetSectionNavigator.layout().addWidget(self.secNav,2,0,1,4)
		# Buttons for navigation
		self.buttonsNavSection = []
		self.buttonsNavSection.append(QPushButton("<<"))
		self.buttonsNavSection.append(QPushButton("<"))
		self.buttonsNavSection.append(QPushButton(">"))
		self.buttonsNavSection.append(QPushButton(">>"))
		for i, btn in enumerate(self.buttonsNavSection):
			widgetSectionNavigator.layout().addWidget(btn,3,i,1,1)
			
		# Add widget for Navigation to the layout of the left widget
		self.layout().addWidget(widgetSectionNavigator)
		self.layout().addWidget(gu.makeHSeparator())
		
		# # SET_INTEGRATION
		# # Add the widget for the definition of the integration scheme
		# widgetIntegration = QWidget()
		# widgetIntegration.setLayout(QtWidgets.QFormLayout())
		# widgetIntegration.layout().addRow(QLabel('<b>Integration scheme</b>'))
		# # Integration type combo
		# self.comboIntegrationType = QComboBox()
		# listOfTypes = list(_constants.integrationTypes.keys())
		# self.comboIntegrationType.addItems(listOfTypes)
		# widgetIntegration.layout().addRow(QLabel("Integration Type"),self.comboIntegrationType)
		# # Number of integration points Spin
		# self.spinNumIntPoints = QSpinBox()
		# #kater to move on changed integration scheme
		# self.spinNumIntPoints.setValue(5)
		# self.spinNumIntPoints.setMinimum(_constants.integrationTypes.get("Lobatto")[0])
		# self.spinNumIntPoints.setMaximum(_constants.integrationTypes.get("Lobatto")[1]) # To check: Lobatto accepts max 9 int points
		# widgetIntegration.layout().addRow(QLabel("Number of integration points"),self.spinNumIntPoints)
		
		# # Add the widget for the definiion of the integration scheme to the layout of the left widget
		# self.layout().addWidget(widgetIntegration)
		# self.layout().addWidget(gu.makeHSeparator())
		# # END SET_INTEGRATION
		
		# Add a final stretch to the layout of the left widget
		self.layout().addStretch(1)
		
		# Setup the connections
		# Change Dimension (2D/3D)
		self.comboDimension.currentIndexChanged.connect(self.changedDimension)
		# Select a new section from the comboBox
		self.comboSection.currentIndexChanged.connect(self.changedCrossSection)
		# Change PMM from fiber to uncoupled phenomenological
		self.checkBoxPMMinteraction.stateChanged.connect(self.changedPMMinteraction)
		# phenomenological PMM
		self.checkBoxMaterialP.stateChanged.connect(self.changedPhenomenologicalPInclusion)
		self.comboMaterialP.currentIndexChanged.connect(self.changedMaterialP)
		self.checkBoxMaterialMy.stateChanged.connect(self.changedPhenomenologicalMyInclusion)
		self.comboMaterialMy.currentIndexChanged.connect(self.changedMaterialMy)
		self.checkBoxMaterialMz.stateChanged.connect(self.changedPhenomenologicalMzInclusion)
		self.comboMaterialMz.currentIndexChanged.connect(self.changedMaterialMz)
		# Specify if using all the same sections
		self.useSameSections.stateChanged.connect(self.changedUseSameSection)
		# Buttons for section Navigation
		self.buttonsNavSection[0].clicked.connect(self.firstSection)
		self.buttonsNavSection[1].clicked.connect(self.previousSection)
		self.buttonsNavSection[2].clicked.connect(self.nextSection)
		self.buttonsNavSection[3].clicked.connect(self.lastSection)
		# # SET_INTEGRATION
		# # Integration scheme
		# self.comboIntegrationType.currentIndexChanged.connect(self.changedIntegrationType)
		# self.spinNumIntPoints.valueChanged.connect(self.changedNumberOfIntegrationPoints)
		# # END SET_INTEGRATION
		# shear aggregator
		self.checkBoxIncludeShearVy.stateChanged.connect(self.changedShearInclusion)
		self.checkBoxIncludeShearVz.stateChanged.connect(self.changedShearInclusion)
		self.comboShearVy.currentIndexChanged.connect(self.changedMaterialVy)
		self.comboShearVz.currentIndexChanged.connect(self.changedMaterialVz)
		# Torsion aggregator
		self.checkBoxIncludeTorsion.stateChanged.connect(self.changedTorsionInclusion)
		self.comboTorsion.currentIndexChanged.connect(self.changedMaterialT)
		
	def getSelectedCrossSection(self):
		return self.comboSection.currentData()
		
	def initialize(self, model, preview):
		# Save the model
		self.model = model
		self.previewImage = preview
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::initialize\t\t\t->\tInitialized values. Model before updating GUI:')
			self.printModel()
		
		# Update the widget contents
		self.updateGUI()
		
		# Update the preview image and the section navigator 
		self.updateImage()
		self.updateSectionNavigator()
		
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::initialize\t\t\t->\tUpdated GUI. Model after updating GUI:')
			self.printModel()
			
	def updateViewsChangingDimension(self):
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateViewsChangingDimension\t->\tupdating the views after changing in dimension')
		if self.model.dimension == '2D':
			# moved to 2D show only Y local
			self.checkBoxIncludeShearVz.hide()
			self.comboShearVz.hide()
			self.widgetTorsionAggregators.hide()
			if not self.checkBoxPMMinteraction.isChecked():
				self.comboMaterialMz.hide()
				self.checkBoxMaterialMz.hide()
		elif self.model.dimension == '3D':
			# moved to 3D. Show both Y and Z local
			self.checkBoxIncludeShearVz.show()
			self.comboShearVz.show()
			self.widgetTorsionAggregators.show()
			if not self.checkBoxPMMinteraction.isChecked():
				self.comboMaterialMz.show()
				self.checkBoxMaterialMz.show()
		
	def changedDimension(self):
		# Changed the dimension
		if self.sender() is not None:
			# Update the model
			self.model.dimension = self.comboDimension.currentText()
			if distributedWidgetPP._debug:
				print('distributedWidgetPP::changedDimension\t\t\t->\tDimension set to {}. Model updated:'.format(self.model.dimension))
				self.printModel()
		# Update the views
		self.updateViewsChangingDimension()
		
		if self.sender() is not None:
			# update the section Navigator
			self.updateSectionNavigator()
	
	def updateSectionNavigator(self):
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateSectionNavigator\t\t\t->\tCalling the function with this model')
			self.printModel()
			print('distributedWidgetPP::updateSectionNavigator\t\t\t->\tSetting current section')
		if self.model.sameSection:
			self.secNav.setCurrentSection(-1)
		else:
			self.secNav.setCurrentSection(self.model.currentSection)
		
		# Reset the labels in order to rewrite them
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateSectionNavigator\t\t\t->\tResetting labels')
		self.secNav.resetLabels()
		
		# Update the widget navigator Secion
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateSectionNavigator\t\t\t->\tSetting cross section')
		tooltip = []
		indexSec = []
		if self.model.PMMinteraction:
			for cS in self.model.crossSection:
				idx = self.comboSection.findData(cS)
				indexSec.append('{}'.format(cS))
				if idx >= 0:
					tooltip.append(self.comboSection.itemText(idx))
			self.secNav.addLabels('Sec',indexSec,tooltip,True)
		else:
			showMaterialP = False
			showMaterialMy = False
			showMaterialMz = False
			if self.model.sameSection:
				if (self.model.includePmaterial[0]):
					showMaterialP = True
				if (self.model.includeMyMaterial[0]):
					showMaterialMy = True
				if self.model.dimension == '3D':
					if (self.model.includeMzMaterial[0]):
						showMaterialMz = True
			else:
				for p in self.model.includePmaterial:
					if p:
						showMaterialP = True
						break
				for m in self.model.includeMyMaterial:
					if m:
						showMaterialMy = True
						break
				if self.model.dimension == '3D':
					for m in self.model.includeMzMaterial:
						if m:
							showMaterialMz = True
							break
			if showMaterialP:
				tooltip = []
				indexSec = []
				for i_s, s in zip(self.model.includePmaterial,self.model.materialP):
					if not i_s:
						tooltip.append('Not considered')
						indexSec.append('N')
					else:
						idx = self.comboMaterialP.findData(s)
						if s == 0:
							indexSec.append('A')
						else:
							indexSec.append('{}'.format(s))
						if idx >= 0:
							tooltip.append(self.comboMaterialP.itemText(idx))
				self.secNav.addLabels('P',indexSec,tooltip,True)
			if showMaterialMy:
				tooltip = []
				indexSec = []
				for i_s, s in zip(self.model.includeMyMaterial,self.model.materialMy):
					if not i_s:
						tooltip.append('Not considered')
						indexSec.append('N')
					else:
						idx = self.comboMaterialMy.findData(s)
						if s == 0:
							indexSec.append('A')
						else:
							indexSec.append('{}'.format(s))
						if idx >= 0:
							tooltip.append(self.comboMaterialMy.itemText(idx))
				self.secNav.addLabels('My',indexSec,tooltip,True)
			if showMaterialMz:
				tooltip = []
				indexSec = []
				for i_s, s in zip(self.model.includeMzMaterial,self.model.materialMz):
					if not i_s:
						tooltip.append('Not considered')
						indexSec.append('N')
					else:
						idx = self.comboMaterialMz.findData(s)
						if s == 0:
							indexSec.append('A')
						else:
							indexSec.append('{}'.format(s))
						if idx >= 0:
							tooltip.append(self.comboMaterialMz.itemText(idx))
				self.secNav.addLabels('Mz',indexSec,tooltip,True)
		
		# shear section aggregator
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateSectionNavigator\t\t\t->\tChecking aggregators')
		showShearVy = False
		showShearVz = False
		showTorsion = False
		
		if self.model.sameSection:
			if (self.model.includeShearVy[0]):
				showShearVy = True
			if self.model.dimension == '3D':
				if (self.model.includeShearVz[0]):
					showShearVz = True
			if (self.model.includeTorsion[0]):
				showTorsion = True
		else:
			for i in self.model.includeShearVy:
				if i:
					showShearVy = True
					break
			if self.model.dimension == '3D':
				for i in self.model.includeShearVz:
					if i:
						showShearVz = True
						break
			for i in self.model.includeTorsion:
				if i:
					showTorsion = True
					break
		if showShearVy:
			tooltip = []
			indexSec = []
			for i_s, s in zip(self.model.includeShearVy,self.model.shearVy):
				if not i_s:
					tooltip.append('Not considered')
					indexSec.append('N')
				else:
					idx = self.comboShearVy.findData(s)
					if s == 0:
						indexSec.append('A')
					else:
						indexSec.append('{}'.format(s))
					if idx >= 0:
						tooltip.append(self.comboShearVy.itemText(idx))
			self.secNav.addLabels('Vy',indexSec,tooltip,True)
			
		if showShearVz:
			tooltip = []
			indexSec = []
			for i_s, s in zip(self.model.includeShearVz,self.model.shearVz):
				if not i_s:
					tooltip.append('Not considered')
					indexSec.append('N')
				else:
					idx = self.comboShearVz.findData(s)
					if s == 0:
						indexSec.append('A')
					else:
						indexSec.append('{}'.format(s))
					if idx >= 0:
						tooltip.append(self.comboShearVz.itemText(idx))
			self.secNav.addLabels('Vz',indexSec,tooltip,True)
		
		if showTorsion:
			tooltip = []
			indexSec = []
			for i_s, s in zip(self.model.includeTorsion,self.model.torsion):
				if not i_s:
					tooltip.append('Not considered')
					indexSec.append('N')
				else:
					idx = self.comboTorsion.findData(s)
					if s == 0:
						indexSec.append('A')
					else:
						indexSec.append('{}'.format(s))
					if idx >= 0:
						tooltip.append(self.comboTorsion.itemText(idx))
			self.secNav.addLabels('T',indexSec,tooltip,True)
					
		self.secNav.updateGeometry()
		
	def setIntegration(self, integration, numIntPts):
		self.model.integration = integration
		self.model.numIntPts = numIntPts
		
	# def setSameSection(self, sameSection):
		# # Update the model
		# self.model.sameSection = sameSection
		# # Update the view
		# self.useSameSections.setChecked(self.model.sameSection)
		
	# def setCurrentSection(self, sec):
		# self.model.currentSection = sec
		
	# def setCrossSection(self, crossSec):
		# self.model.crossSection = crossSec
		
	# def setShearVyAggregator(self, includeShearVy, shearVy):
		# self.model.includeShearVy = includeShearVy
		# self.model.shearVy = shearVy
		
	# def setShearVzAggregator(self, includeShearVz, shearVz):
		# self.model.includeShearVz = includeShearVz
		# self.model.shearVz = shearVz
		
	# def setTorsionAggregator(self, includeTorsion, torsion):
		# self.model.includeTorsion = includeTorsion
		# self.model.torsion = torsion
		
	def updateGUI(self):
	
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateGUI\t\t\t->\tModel before updating GUI:')
			self.printModel()
		# update GUI should be called manually when I change the model and want to update the widgets,
		# thus all the interested connections are blocked
		# blocking signals
		locks = [
			# SET_INTEGRATION
			# QSignalBlocker(self.comboIntegrationType),
			# QSignalBlocker(self.spinNumIntPoints),
			QSignalBlocker(self.comboDimension),
			QSignalBlocker(self.comboSection),
			QSignalBlocker(self.checkBoxPMMinteraction),
			QSignalBlocker(self.checkBoxMaterialP),
			QSignalBlocker(self.comboMaterialP),
			QSignalBlocker(self.checkBoxMaterialMy),
			QSignalBlocker(self.comboMaterialMy),
			QSignalBlocker(self.checkBoxMaterialMz),
			QSignalBlocker(self.comboMaterialMz),
			QSignalBlocker(self.useSameSections),
			QSignalBlocker(self.comboShearVy),
			QSignalBlocker(self.checkBoxIncludeShearVy),
			QSignalBlocker(self.comboShearVz),
			QSignalBlocker(self.checkBoxIncludeShearVz),
			QSignalBlocker(self.comboTorsion),
			QSignalBlocker(self.checkBoxIncludeTorsion),
			]
		
		# Update dimension
		self.comboDimension.setCurrentText(self.model.dimension)
		
		# SET_INTEGRATION
		# # Integration scheme
		# self.comboIntegrationType.setCurrentText(self.model.integration)
		# self.spinNumIntPoints.setValue(self.model.numIntPts)
		
		# Get current section
		sec = self.model.currentSection
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateGUI\t\t\t->\tsection for update of the gui (from 0 to numIntPts): {} - all same section? {}'.format(sec,self.model.sameSection))
		
		# Cross section Widget
		# Updating the combo of the section
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateGUI\t\t\t->\tUpdating to the following section (index of the xobj): ',self.model.crossSection[sec])
		idx = self.comboSection.findData(self.model.crossSection[sec])
		if idx >= 0:
			self.comboSection.setCurrentIndex(idx)
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateGUI\t\t\t->\tUpdated the combo of the section')
		# self.getSectionAndUpdateSectionPreviewWidget() #TODO: I could call it later from the combo changed -> try then erase from here
		
		# PMM interaction
		self.checkBoxPMMinteraction.setChecked(self.model.PMMinteraction)
		
		idx = self.comboMaterialP.findData(self.model.materialP[sec])
		if idx >= 0:
			self.comboMaterialP.setCurrentIndex(idx)
		self.checkBoxMaterialP.setChecked(self.model.includePmaterial[sec])
		
		idx = self.comboMaterialMy.findData(self.model.materialMy[sec])
		if idx >= 0:
			self.comboMaterialMy.setCurrentIndex(idx)
		self.checkBoxMaterialMy.setChecked(self.model.includeMyMaterial[sec])
		
		idx = self.comboMaterialMz.findData(self.model.materialMz[sec])
		if idx >= 0:
			self.comboMaterialMz.setCurrentIndex(idx)
		self.checkBoxMaterialMz.setChecked(self.model.includeMzMaterial[sec])
		
		# Shear aggregator
		idx = self.comboShearVy.findData(self.model.shearVy[sec])
		if idx >= 0:
			self.comboShearVy.setCurrentIndex(idx)
		self.checkBoxIncludeShearVy.setChecked(self.model.includeShearVy[sec])
		
		idx = self.comboShearVz.findData(self.model.shearVz[sec])
		if idx >= 0:
			self.comboShearVz.setCurrentIndex(idx)
		self.checkBoxIncludeShearVz.setChecked(self.model.includeShearVz[sec])
		
		# Torsion aggregator
		idx = self.comboTorsion.findData(self.model.torsion[sec])
		if idx >= 0:
			self.comboTorsion.setCurrentIndex(idx)
		self.checkBoxIncludeTorsion.setChecked(self.model.includeTorsion[sec])

		# section navigator
		self.useSameSections.setChecked(self.model.sameSection)
		self.updateSectionNavigator()
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateGUI\t\t\t->\tUpdated the GUI, the model is:')
			self.printModel()
		
		# Force the call the the blocked signals that we need (just those that deals with the GUI -> showing / hiding widgets)
		self.updateViewsChangingDimension() #This function will show / hide the controls based on the dimension of the problem (2D/3D)
		self.getSectionAndUpdateSectionPreviewWidget() #This function will update the Preview Widget
		self.updateViewsChangingPMMinteraction() # This function will show hide controls based on PMM interaction selection
		self.changedPhenomenologicalPInclusion()
		self.changedPhenomenologicalMyInclusion()
		self.changedPhenomenologicalMzInclusion()
		self.changedShearInclusion()
		self.changedTorsionInclusion()

		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateGUI\t\t\t->\tCalling update Nav Buttons')
		self.updateNavButtons()
		
	def getSection(self):
		# get the document, we need it to get the sections
		doc = App.caeDocument()
		if doc is None:
			raise Exception('no active cae document')
		# If the section is something other than none
		if self.model.crossSection[self.model.currentSection] > 0:
			# Get the section for the preview
			sec_xobj = doc.getPhysicalProperty(self.model.crossSection[self.model.currentSection]).XObject
			# If it is a fiber section:
			if sec_xobj.name in _constants.fiberSections:
				self.sec = _get_xobj_attribute(sec_xobj,'Fiber section').customObject # Returns a MpcFiberSection
				self.shape = None # I don't need a custom FxShape
				# done
				self.sec.regenerateVisualRepresentation()
				self.sec.commitChanges()
				# build graphics (must be done on the main gui thread)
				self.sec.buildGraphics()
			else:
				print('It is an elastic section: ')
				self.sec = MpcBeamFiberSection() # I create a dummy fiber section to initialize the scene widget
				sec = _get_xobj_attribute(sec_xobj,'Section').customObject
				self.shape = sec.makeVisualRepresentation() # Returns a FxShape
				
		
	def getSectionAndUpdateSectionPreviewWidget(self):
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::getSectionAndUpdateSectionPreviewWidget\t\t\t->\tgettingSection and updating PreviewWidget')
		
		# Get out the old widget
		self.widgetSceneContainer.layout().removeWidget(self.scene_widget)
		aux = self.scene_widget
		
		# If the section is something other than none
		if self.model.crossSection[self.model.currentSection] > 0:
			# get the section object and save it into self.sec
			self.getSection()
			
			# Create the MpcSceneWidget
			self.sec_widget = MpcSceneWidget(self.sec)
			
			if self.shape is not None:
				self.sec_widget.addCustomDrawableEntity(self.shape)
			
			# update bounding box and fit all
			self.sec_widget.scene.updateBoundingBox()
			self.sec_widget.fitAll()
		else:
			# Create an ampty MpcSceneWidtget
			self.sec_widget = MpcSceneWidget()
		
		# Create and add the new widget
		self.scene_widget = shiboken2.wrapInstance(self.sec_widget.getPtr(), QWidget)
		aux.deleteLater()
		self.widgetSceneContainer.layout().addWidget(self.scene_widget) # insertWidget(1,self.scene_widget)
	
	def changedCrossSection(self):
		if not self.model.sameSection:
			self.model.crossSection[self.model.currentSection] = self.comboSection.currentData()
		else:
			self.model.crossSection = [self.comboSection.currentData()] * self.model.numIntPts
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::changedCrossSection\t\t\t->\tCross section changed. The new model is:')
			self.printModel()
		self.getSectionAndUpdateSectionPreviewWidget()
		self.updateSectionNavigator()
	
	def changedUseSameSection(self):
		if self.useSameSections.isChecked():
			self.model.sameSection = True
			# Force to have the same sections everywhere (all equal to current)
			self.setSectionsToCurrent()
			self.model.currentSection = 0
			self.secNav.setCurrentSection(-1)
		else:
			self.model.sameSection = False
			self.model.currentSection = 0
			self.secNav.setCurrentSection(0)
		self.updateNavButtons()
		self.updateSectionNavigator()
			
	def setSectionsToCurrent(self):
		crossSection = self.model.crossSection[self.model.currentSection]
		includeShearVy = self.model.includeShearVy[self.model.currentSection]
		shearVy = self.model.shearVy[self.model.currentSection]
		includeShearVz = self.model.includeShearVz[self.model.currentSection]
		shearVz = self.model.shearVz[self.model.currentSection]
		includeTorsion = self.model.includeTorsion[self.model.currentSection]
		torsion = self.model.torsion[self.model.currentSection]
		includePmaterial = self.model.includePmaterial[self.model.currentSection]
		materialP = self.model.materialP[self.model.currentSection]
		includeMyMaterial = self.model.includeMyMaterial[self.model.currentSection]
		materialMy = self.model.materialMy[self.model.currentSection]
		includeMzMaterial = self.model.includeMzMaterial[self.model.currentSection]
		materialMz = self.model.materialMz[self.model.currentSection]
		# Reset vectors
		self.model.crossSection = [crossSection] * self.model.numIntPts
		self.model.includeShearVy = [includeShearVy] * self.model.numIntPts
		self.model.shearVy = [shearVy] * self.model.numIntPts
		self.model.includeShearVz = [includeShearVz] * self.model.numIntPts
		self.model.shearVz = [shearVz] * self.model.numIntPts
		self.model.includeTorsion = [includeTorsion] * self.model.numIntPts
		self.model.torsion = [torsion] * self.model.numIntPts
		self.model.includePmaterial = [includePmaterial] * self.model.numIntPts
		self.model.materialP = [materialP] * self.model.numIntPts
		self.model.includeMyMaterial = [includeMyMaterial] * self.model.numIntPts
		self.model.materialMy = [materialMy] * self.model.numIntPts
		self.model.includeMzMaterial = [includeMzMaterial] * self.model.numIntPts
		self.model.materialMz = [materialMz] * self.model.numIntPts
	
	def updateNavButtons(self):
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::updateNavButtons\t\t->\tCalling update Nav Buttons')
			self.printModel()
			print('distributedWidgetPP::updateNavButtons\t\t->\tself.model.sameSection: {}'.format(self.model.sameSection))
		if self.model.sameSection:
			if distributedWidgetPP._debug:
				print('distributedWidgetPP::updateNavButtons\t\t->\tUsing the same section. Disable buttons')
			for btn in self.buttonsNavSection:
				btn.setEnabled(False)
		else:
			for btn in self.buttonsNavSection:
				btn.setEnabled(True)
			# Show or hide the nav buttons depending on where we are in the navigation
			maxIdx = self.model.numIntPts - 1
			minIdx = 0
			for btn in self.buttonsNavSection:
				btn.setEnabled(True)
			if self.model.currentSection == minIdx:
				self.buttonsNavSection[0].setEnabled(False)
				self.buttonsNavSection[1].setEnabled(False)
			if self.model.currentSection == maxIdx:
				self.buttonsNavSection[2].setEnabled(False)
				self.buttonsNavSection[3].setEnabled(False)
	
	def firstSection(self):
		self.model.currentSection = 0
		self.secNav.setCurrentSection(self.model.currentSection)
		self.updateNavButtons()
		self.updateGUI()
		
	def previousSection(self):
		self.model.currentSection -= 1
		if self.model.currentSection < 0:
			self.model.currentSection = 0
		self.secNav.setCurrentSection(self.model.currentSection)
		self.updateNavButtons()
		self.updateGUI()
		
	def nextSection(self):
		maxIdx = self.model.numIntPts - 1
		self.model.currentSection += 1
		if self.model.currentSection > maxIdx:
			self.model.currentSection = maxIdx
		self.secNav.setCurrentSection(self.model.currentSection)
		self.updateNavButtons()
		self.updateGUI()
		
	def lastSection(self):
		self.model.currentSection = self.model.numIntPts - 1
		self.secNav.setCurrentSection(self.model.currentSection)
		self.updateNavButtons()
		self.updateGUI()
		
	def changedMaterialVy(self):
		if not self.model.sameSection:
			self.model.shearVy[self.model.currentSection] = self.comboShearVy.currentData()
		else:
			self.model.shearVy = [self.comboShearVy.currentData()] * self.model.numIntPts
		self.updateSectionNavigator()
		
	def changedMaterialVz(self):
		if not self.model.sameSection:
			self.model.shearVz[self.model.currentSection] = self.comboShearVz.currentData()
		else:
			self.model.shearVz = [self.comboShearVz.currentData()] * self.model.numIntPts
		self.updateSectionNavigator()
		
	def changedMaterialT(self):
		if not self.model.sameSection:
			self.model.torsion[self.model.currentSection] = self.comboTorsion.currentData()
		else:
			self.model.torsion = [self.comboTorsion.currentData()] * self.model.numIntPts
		self.updateSectionNavigator()
		
	def changedMaterialP(self):
		if not self.model.sameSection:
			self.model.materialP[self.model.currentSection] = self.comboMaterialP.currentData()
		else:
			self.model.materialP = [self.comboMaterialP.currentData()] * self.model.numIntPts
		self.updateSectionNavigator()
		
	def changedMaterialMy(self):
		if not self.model.sameSection:
			self.model.materialMy[self.model.currentSection] = self.comboMaterialMy.currentData()
		else:
			self.model.materialMy = [self.comboMaterialMy.currentData()] * self.model.numIntPts
		self.updateSectionNavigator()
		
	def changedMaterialMz(self):
		if not self.model.sameSection:
			self.model.materialMz[self.model.currentSection] = self.comboMaterialMz.currentData()
		else:
			self.model.materialMz = [self.comboMaterialMz.currentData()] * self.model.numIntPts
		self.updateSectionNavigator()
	
	# SET_INTEGRATION
	# def changedIntegrationType(self):
		# self.setIntegration(self.comboIntegrationType.currentText(), self.spinNumIntPoints.value())
		# # If there are new limits on integration Points, set them here
	
	# SET_INTEGRATION
	# def changedNumberOfIntegrationPoints(self):
		# if self.spinNumIntPoints.value() > self.numIntPts:
			# for _ in range(self.spinNumIntPoints.value() - self.numIntPts):
				# self.crossSection.append(self.crossSection[0])
				# self.includeShearVy.append(self.includeShearVy[0])
				# self.shearVy.append(self.shearVy[0])
				# self.includeShearVz.append(self.includeShearVz[0])
				# self.shearVz.append(self.shearVz[0])
				# self.includeTorsion.append(self.includeTorsion[0])
				# self.torsion.append(self.torsion[0])
			# self.numIntPts = self.spinNumIntPoints.value()
		# elif self.spinNumIntPoints.value() < self.numIntPts:
			# # delete points
			# for _ in range(self.numIntPts - self.spinNumIntPoints.value()):
				# self.crossSection.pop()
				# self.includeShearVy.pop()
				# self.shearVy.pop()
				# self.includeShearVz.pop()
				# self.shearVz.pop()
				# self.includeTorsion.pop()
				# self.torsion.pop()
			# self.numIntPts = self.spinNumIntPoints.value()
		# # update the section navigation
		# self.secNav.setNumberOfSections(self.spinNumIntPoints.value(), currSec = self.currentSection)
		# # call the event to update the navigation widget
		# self.printModel()
		# self.changedUseSameSection()
		# self.updateSectionNavigator()
	
	def updateViewsChangingPMMinteraction(self):
		if self.checkBoxPMMinteraction.isChecked():
			self.checkBoxMaterialP.hide()
			self.comboMaterialP.hide()
			self.checkBoxMaterialMy.hide()
			self.comboMaterialMy.hide()
			self.checkBoxMaterialMz.hide()
			self.comboMaterialMz.hide()
		else:
			self.checkBoxMaterialP.show()
			self.comboMaterialP.show()
			self.checkBoxMaterialMy.show()
			self.comboMaterialMy.show()
			if self.model.dimension == '3D':
				self.checkBoxMaterialMz.show()
				self.comboMaterialMz.show()
			else:
				self.checkBoxMaterialMz.hide()
				self.comboMaterialMz.hide()
				
	def changedPMMinteraction(self):
		# Update model 
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::changedPMMinteraction\t->\tPMM Interaction changed.')
		self.model.PMMinteraction = self.checkBoxPMMinteraction.isChecked()
		# Update the views 
		self.updateViewsChangingPMMinteraction()
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::changedPMMinteraction\t->\tPMM Interaction changed. The new model after update is:')
			self.printModel()
		self.updateImage()
		self.updateSectionNavigator()
		
	def changedShearInclusion(self):
		if distributedWidgetPP._debug:
			print('distributedWidgetPP::changedShearInclusion\t-\t\t>\tCalled shear InclusionChanged\n')
			print('\t\t\t\t\t\t\tSender:', self.sender())
		
		if self.sender() is not None:
			# Someone sent the signal, I need to update the model and later updates the views
			if self.sender().text().startswith('Include shear Vy'):
				# Update the model for shear Vy
				if self.checkBoxIncludeShearVy.isChecked():
					if not self.model.sameSection:
						self.model.includeShearVy[self.model.currentSection] = True
					else:
						self.model.includeShearVy = [True] * self.model.numIntPts
				else:
					if not self.model.sameSection:
						self.model.includeShearVy[self.model.currentSection] = False
					else:
						self.model.includeShearVy = [False] * self.model.numIntPts
			elif self.sender().text().startswith('Include shear Vz'):
				# Update the model for shear Vz
				if self.checkBoxIncludeShearVz.isChecked():
					if not self.model.sameSection:
						self.model.includeShearVz[self.model.currentSection] = True
					else:
						self.model.includeShearVz = [True] * self.model.numIntPts
				else:
					if not self.model.sameSection:
						self.model.includeShearVz[self.model.currentSection] = False
					else:
						self.model.includeShearVz = [False] * self.model.numIntPts
		
		# Update the views now that the model is fine
		if self.checkBoxIncludeShearVy.isChecked():
			self.comboShearVy.setEnabled(True)
		else:
			self.comboShearVy.setEnabled(False)
		if self.checkBoxIncludeShearVz.isChecked():
			self.comboShearVz.setEnabled(True)
		else:
			self.comboShearVz.setEnabled(False)
		
		if self.sender() is not None:
			self.updateImage()
			self.updateSectionNavigator()
		
	def changedTorsionInclusion(self):
		if distributedWidgetPP._debug:
			print('\n\ndistributedWidgetPP::changedTorsionInclusion\t\t->\tCalled torsion Inclusion change')
			print('\t\t\t\t\t\t\tSender:', self.sender())
		
		if self.sender() is not None:
			# Someone sent the signal, I need to update the model and later updates the views
			if self.checkBoxIncludeTorsion.isChecked():
				self.comboTorsion.setEnabled(True)
				if not self.model.sameSection:
					self.model.includeTorsion[self.model.currentSection] = True
				else:
					self.model.includeTorsion = [True] * self.model.numIntPts
			else:
				self.comboTorsion.setEnabled(False)
				if not self.model.sameSection:
					self.model.includeTorsion[self.model.currentSection] = False
				else:
					self.model.includeTorsion = [False] * self.model.numIntPts
		
		# Update the views now that the model is updated
		if self.checkBoxIncludeTorsion.isChecked():
			self.comboTorsion.setEnabled(True)
		else:
			self.comboTorsion.setEnabled(False)
				
		if self.sender() is not None:
			self.updateImage()
			self.updateSectionNavigator()
	
	def changedPhenomenologicalPInclusion(self):
		if distributedWidgetPP._debug:
			print('\n\ndistributedWidgetPP::changedPhenomenologicalPInclusion\t\t->\tCalled P Inclusion change')
			print('\t\t\t\t\t\t\tSender:', self.sender())
		
		if self.sender() is not None:
			# Someone sent the signal, I need to update the model and later updates the views
			if self.checkBoxMaterialP.isChecked():
				if not self.model.sameSection:
					self.model.includePmaterial[self.model.currentSection] = True
				else:
					self.model.includePmaterial = [True] * self.model.numIntPts
			else:
				if not self.model.sameSection:
					self.model.includePmaterial[self.model.currentSection] = False
				else:
					self.model.includePmaterial = [False] * self.model.numIntPts
		
		# Update the views now that the model is updated
		if self.checkBoxMaterialP.isChecked():
			self.comboMaterialP.setEnabled(True)
		else:
			self.comboMaterialP.setEnabled(False)
		
		if self.sender() is not None:
			self.updateImage()
			self.updateSectionNavigator()
				
	def changedPhenomenologicalMyInclusion(self):
		if distributedWidgetPP._debug:
			print('\n\ndistributedWidgetPP::changedPhenomenologicalMyInclusion\t\t->\tCalled My Inclusion change')
			print('\t\t\t\t\t\t\tSender:', self.sender())
		
		if self.sender() is not None:
			# Someone sent the signal, I need to update the model and later updates the views
			if self.checkBoxMaterialMy.isChecked():
				if not self.model.sameSection:
					self.model.includeMyMaterial[self.model.currentSection] = True
				else:
					self.model.includeMyMaterial = [True] * self.model.numIntPts
			else:
				if not self.model.sameSection:
					self.model.includeMyMaterial[self.model.currentSection] = False
				else:
					self.model.includeMyMaterial = [False] * self.model.numIntPts
		
		# Update the views now that the model is updated
		if self.checkBoxMaterialMy.isChecked():
			self.comboMaterialMy.setEnabled(True)
		else:
			self.comboMaterialMy.setEnabled(False)
		
		if self.sender() is not None:
			self.updateImage()
			self.updateSectionNavigator()
	
	def changedPhenomenologicalMzInclusion(self):
		if distributedWidgetPP._debug:
			print('\n\ndistributedWidgetPP::changedPhenomenologicalMzInclusion\t\t->\tCalled Mz Inclusion change')
			print('\t\t\t\t\t\t\tSender:', self.sender())
		
		if self.sender() is not None:
			# Someone sent the signal, I need to update the model and later updates the views
			if self.checkBoxMaterialMz.isChecked():
				if not self.model.sameSection:
					self.model.includeMzMaterial[self.model.currentSection] = True
				else:
					self.model.includeMzMaterial = [True] * self.model.numIntPts
			else:
				if not self.model.sameSection:
					self.model.includeMzMaterial[self.model.currentSection] = False
				else:
					self.model.includeMzMaterial = [False] * self.model.numIntPts
		
		# Update the views now that the model is updated
		if self.checkBoxMaterialMz.isChecked():
			self.comboMaterialMz.setEnabled(True)
		else:
			self.comboMaterialMz.setEnabled(False)
		
		if self.sender() is not None:
			self.updateImage()
			self.updateSectionNavigator()
		
	def updateImage(self):
		filename = __file__
		folder = os.path.dirname(filename)
		fileName = os.path.abspath(os.path.join(folder, "img/distributed"))
		ext = '.png'
		suff = ''
		if self.model.sameSection:
			if (self.model.includeShearVy[0]):
				suff += 'Vy'
			if (self.model.includeShearVz[0]):
				suff += 'Vz'
			if (self.model.includeTorsion[0]):
				suff += 'T'
		else:
			for i in self.model.includeShearVy:
				if i:
					suff += 'Vy'
					break
			for i in self.model.includeShearVz:
				if i:
					suff += 'Vz'
					break
			for i in self.model.includeTorsion:
				if i:
					suff += 'T'
					break
		pixmap = QtGui.QPixmap(fileName + suff + ext)
		self.previewImage.setPixmap(pixmap)
	
	def printModel(self):
		print('\tDimension: {}'.format(self.model.dimension))
		print('\tsameSections? {}'.format(self.model.sameSection))
		print('\tCurrent section: {}'.format(self.model.currentSection))
		print('\tcrossSections: {}'.format(self.model.crossSection))
		print('\tPMMinteraction: {}'.format(self.model.PMMinteraction))
		print('\tincludePmaterial: {}'.format(self.model.includePmaterial))
		print('\tPmaterial: {}'.format(self.model.materialP))
		print('\tincludeMyMaterial: {}'.format(self.model.includeMyMaterial))
		print('\tMyMaterial: {}'.format(self.model.materialMy))
		print('\tincludeMzMaterial: {}'.format(self.model.includeMzMaterial))
		print('\tMzMaterial: {}'.format(self.model.materialMz))
		print('\tincludeShearVy: {}'.format(self.model.includeShearVy))
		print('\tshearVy: {}'.format(self.model.shearVy))
		print('\tincludeShearVz: {}'.format(self.model.includeShearVz))
		print('\tshearVz: {}'.format(self.model.shearVz))
		print('\tincludeTorsion: {}'.format(self.model.includeTorsion))
		print('\ttorsion: {}'.format(self.model.torsion))
																										
	