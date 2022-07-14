import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
# import opensees.element_properties.beam_column_elements.internalBeamColumnElement as internalBeamColumnElement
import opensees.physical_properties.special_purpose.beam_section_utils as bsutils
import opensees.element_properties.utils.geomTransf as gtran
import opensees.utils.Gui.GuiUtils as gu
import json

import PyMpc
import traceback
import importlib
from io import StringIO

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
	QToolTip,
	QLineEdit,
	)

import shiboken2

class _constants:
	#gui
	gui = None
	#version
	version = 1
	
	allowedSections = ["RectangularFiberSection", "Fiber", "Elastic"]
	fiberSections = ["RectangularFiberSection", "Fiber"]

class RCBeamColumnElementWidget(QWidget):
	# Class attribute for the activation of Debug printing
	_debug = False
	
	#constructor
	def __init__(self, editor, xobj, parent = None):
		# base class initialization
		super(RCBeamColumnElementWidget, self).__init__(parent)

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
		beam_widget.setLayout(QVBoxLayout())
		beam_widget.layout().addWidget(QLabel('<b>Select the desidered parameters</b>'))
		# beam_widget.layout().setContentsMargins(0,0,0,0)

		# Create the widget for distributed plasticity, lumped plasticity with finite length and lumped plasticity with zero length
		# the widget is common to the three formulations and contains:
		#   widget for the definition of the dimension of the problem (2D - 3D)
		#   widget for the selection of the transformation (Liner - PDelta - Corotational)
		#   widget fot the definition of distributed mass and an option for the selection of consistent or lumped formulation (lumped default)
		
		# Create the widget specifiying if 3D or 2D
		widgetDimension = QWidget()
		widgetDimension.setLayout(QFormLayout())
		# ComboBox for dimension of the problem
		self.comboDimension = QComboBox()
		self.comboDimension.addItems(['2D','3D'])
		self.comboDimension.setCurrentIndex(1)
		widgetDimension.layout().addRow(QLabel("Dimension: "),self.comboDimension)
		widgetDimension.layout().setContentsMargins(0,0,0,0)
		beam_widget.layout().addWidget(widgetDimension)
		beam_widget.layout().addWidget(gu.makeHSeparator())
		
		# Create the widget for transformation
		widgetTransf = QWidget()
		widgetTransf.setLayout(QFormLayout())
		# ComboBox for dimension of the problem
		self.comboTransformation = QComboBox()
		self.comboTransformation.addItems(['Linear','PDelta','Corotational'])
		self.comboTransformation.setCurrentIndex(0)
		widgetTransf.layout().addRow(QLabel("Transformation: "),self.comboTransformation)
		widgetTransf.layout().setContentsMargins(0,0,0,0)
		beam_widget.layout().addWidget(widgetTransf)
		beam_widget.layout().addWidget(gu.makeHSeparator())
		
		# Create the widget for distributed mass
		widgetMass = QWidget()
		widgetMass.setLayout(QFormLayout())
		# CheckBox for mass inclusion
		self.checkMass = QCheckBox('Include distributed mass')
		widgetMass.layout().addRow(self.checkMass)
		# Editbox for mass value
		self.editMass = QLineEdit()
		validator = QDoubleValidator()
		validator.setBottom(0)
		self.editMass.setValidator(validator)
		self.editMass.setToolTip("Mass density expressed in mass over length")
		widgetMass.layout().addRow(QLabel("Mass density: "),self.editMass)
		#combo boc for mass distribution (lumped - default - or consistent)
		self.comboMatrix = QComboBox()
		self.comboMatrix.addItems(['Lumped','Consistent'])
		self.comboMatrix.setCurrentIndex(0)
		widgetMass.layout().addRow(QLabel("Matrix formation: "),self.comboMatrix)
		
		self.editMass.setEnabled(False)
		self.comboMatrix.setEnabled(False)
			
		widgetMass.layout().setContentsMargins(0,0,0,0)
		beam_widget.layout().addWidget(widgetMass)
		beam_widget.layout().addWidget(gu.makeHSeparator())
		
		# Add a final stretch to the layout of the widget
		beam_widget.layout().addStretch(1)
		
		if RCBeamColumnElementWidget._debug:
			print('RCBeamColumnElement::__init__\t\t\t->\tAdding beam_widget')
		self.layout().addWidget(beam_widget)
		if RCBeamColumnElementWidget._debug:
			print('RCBeamColumnElement::__init__\t\t\t->\tAdded beam_widget')

		if RCBeamColumnElementWidget._debug:
			print('RCBeamColumnElement::__init__\t\t\t->\tAdding the widget to the main editor with shiboken')
		# we want to add this widget to the xobject editor
		# on the right of the main tree widget used for the editing of xobject attributes.
		self.editor_splitter = shiboken2.wrapInstance(editor.getChildPtr(MpcXObjectEditorChildCode.MainSplitter), QSplitter)
		self.editor_splitter.addWidget(self)
		total_width = self.editor_splitter.size().width()
		width_1 = 0
		self.editor_splitter.setSizes([width_1, total_width - width_1])
		if RCBeamColumnElementWidget._debug:
			print('RCBeamColumnElement::__init__\t\t\t->\tAdded the widget to the main editor')
		
		# No connection here, so called the toggled function. It should initialize
		# Read Datastore or load default values
		if RCBeamColumnElementWidget._debug:
			print('RCBeamColumnElement::__init__\t\t\t->\tReading the saved formulation or selecting by default distributed')
		# Read datastore attribute or load defaults (should be in the first opening, or the first use of a formulation module
		self.model = readDatastore(self.xobj)
		
		# Update the widgets to the loaded (or default) model
		
		# update the dimension
		self.comboDimension.setCurrentText(self.model.get('dimension'))
		# update the transformation
		self.comboTransformation.setCurrentText(self.model.get('transformation'))
		# update the mass widget
		self.checkMass.setChecked(self.model.get('includeMassDens'))
		self.editMass.setText(str(self.model.get('massDens')))
		self.comboMatrix.setCurrentText(self.model.get('massMatrix'))
		# Call the method since we still don't have connections
		self.includeMassDensChanged()
		
		# Set the connections
		# checkbox mass 
		self.checkMass.stateChanged.connect(self.includeMassDensChanged)
		
	def includeMassDensChanged(self):
		# hide or show the dependent widgets
		if self.checkMass.isChecked():
			self.editMass.setEnabled(True)
			self.comboMatrix.setEnabled(True)
		else:
			self.editMass.setEnabled(False)
			self.comboMatrix.setEnabled(False)
		
		
	def onEditFinished(self):
		if RCBeamColumnElementWidget._debug:
			print('RCBeamColumnElement::onEditFinished\t\t\t->\tEdit finished. Checking data and Saving data to datastore')
		# 
		# Saving data on datastore xobj
		
		# Save in the data store the needed data
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
		
		jds['RCBeamColumnElement'] = {
				'version': _constants.version,
				'dimension': self.comboDimension.currentText(),
				'transformation': self.comboTransformation.currentText(),
				'includeMassDens': self.checkMass.isChecked(),
				'massDens': float(self.editMass.text()),
				'massMatrix': self.comboMatrix.currentText(),
			}
		data.string = json.dumps(jds, indent=4)
		#################################################### $JSON
		
		if RCBeamColumnElementWidget._debug:
			print('RCBeamColumnElement::onEditFinished\t\t\t->\tData saved to data store: {}'.format(data.string))


def makeXObjectMetaData():

	xom = MpcXObjectMetaData()
	xom.name = 'RCBeamColumnElement'
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
	_constants.gui = RCBeamColumnElementWidget(editor,xobj)
	
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

def getNodalSpatialDim(xobj, xobj_phys_prop):
	# get the model from datastore
	try:
		model = readDatastore(xobj)
	except Exception:
		IO.write_cerr('WARNING: impossibile to get model from datastore\n')
		raise
	dimension = model.get('dimension')
	
	if dimension == '2D':
		ndm = 2
		ndf = 3
	else:
		ndm = 3
		ndf = 6
	
	return [(ndm,ndf),(ndm,ndf)]
	
def writeTcl(pinfo):

# # da massimo:
	# try:
		# pp = pinfo.phys_prop
		# el = pinfo.elem_prop
		# pp_ = mypp
		# el_ = myel
		# pinfo.phys_prop = pp_
		# pinfo.elem_prop = el_
		# use pinfo
	# except Exception as ex:
		
		# raise ex
	# finally:
		# pinfo.phys_prop = pp
		# pinfo.elem_prop = el
	
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
			
	elem = pinfo.elem
	#get physical and element properties
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	if (phys_prop is None):
		raise Exception('Error: RCBeamColumnElement has a null physical property.\nPlease assign a physical property of type "RCBeamColumnProperty"')
	if (elem_prop is None):
		raise Exception('Error: RCBeamColumnElement has a null element property.\nPlease assign a element property of type "RCBeamColumnElement"')
	# check if PP is the same as elem_prop (RCBeamColumnElement)
	if (phys_prop.XObject.name != 'RCBeamColumnProperty'):
		raise Exception('Error: RCBeamColumnElement needs a physical property of type "RCBeamColumnProperty".\nPlease assign a physical property of type "RCBeamColumnProperty"')
	
	tag = elem.id
	ppTag = phys_prop.id
	elem_xobj = elem_prop.XObject
	pp_xobj = phys_prop.XObject
	
	# get the model from datastore
	try:
		elem_model = readDatastore(elem_xobj)
		# import the module of the material and if the function exists get the parameters
		module_name = 'opensees.physical_properties.{}.{}'.format(pp_xobj.Xnamespace, pp_xobj.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'readDatastore'):
			pp_model = module.readDatastore(pp_xobj)
	except Exception:
		IO.write_cerr('Error: impossibile to get model from datastore\n')
		raise
	if (pp_model.formulation == 'distr') or (pp_model.formulation == 'lumpedFL'):
		# If model.formulation is 'distr' or 'lumpedFL' we call
		# element forceBeamColumn $eleTag $iNode $jNode $transfTag "IntegrationType arg1 arg2 ..." <-mass $massDens> <-iter $maxIters $tol>
		if elem_model.get('dimension') == '2D':
			ndm = 2
			ndf = 3
			Dimension2 = True
		else:
			ndm = 3
			ndf = 6
			Dimension2 = False
		pinfo.updateModelBuilder(ndm, ndf)
		
		ClassName = elem_xobj.name
		if pinfo.currentDescription != ClassName:
			pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, elem_xobj.Xnamespace, ClassName))
			pinfo.currentDescription = ClassName
			
		# nodes
		node_vect = [node.id for node in elem.nodes]
		# apply correction for joints
		if not elem_model.get('dimension') == '2D':
			if 'RCJointModel3D' in pinfo.custom_data:
				joint_manager = pinfo.custom_data['RCJointModel3D']
				joint_manager.adjustBeamConnectivity(pinfo, elem, node_vect)
		nstr = ' '.join(str(i) for i in node_vect)
		
		if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line or len(node_vect)!=2):
			raise Exception('Error: invalid type of element or number of nodes')
		
		if (pp_model.formulation == 'distr'):
			if pp_model.sameSection:
				# Standard Lobatto integration 
				secTag = pp_model.crossSection[0]
				numIntPts = pp_model.numIntPts
				# If necessary create the aggregator
				aggregateVy = aggregateVz = aggregateTorsion = False
				if (pp_model.includeShearVy[0]):
					if pp_model.shearVy[0] == 0:
						# This is the automatic computation
						raise Exception('Automatic computation for shear Vy not supported yet. Please select a uniaxial material for Vy')
					else:
						shearVyTag = pp_model.shearVy[0]
						aggregateVy = True
				if pp_model.dimension == '3D':
					if (pp_model.includeShearVz[0]):
						if pp_model.shearVz[0] == 0:
							# This is the automatic computation
							raise Exception('Automatic computation for shear Vz not supported yet. Please select a uniaxial material for Vz')
						else:
							shearVzTag = pp_model.shearVz[0]
							aggregateVz = True
					if (pp_model.includeTorsion[0]):
						if pp_model.torsion[0] == 0:
							# This is the automatic computation
							raise Exception('Automatic computation for torsion not supported yet. Please select a uniaxial material for torsion')
						else:
							torsionTag = pp_model.torsion[0]
							aggregateTorsion = True
				if aggregateVy or aggregateVz or aggregateTorsion:
					sopt = ''
					if aggregateVy:
						sopt += ' {} Vy'.format(shearVyTag)
					if aggregateVz:
						sopt += ' {} Vz'.format(shearVzTag)
					if aggregateTorsion:
						sopt += ' {} T'.format(torsionTag)
					sopt += ' -section {}'.format(secTag)
					# update the Section Tag to a new generated value
					secTag = pinfo.next_physicalProperties_id # auto-generated material
					pinfo.next_physicalProperties_id += 1
					str_tcl_aggregator = '\n{}{}\n'.format(pinfo.indent,'# Automatically generated section aggregator')
					str_tcl_aggregator += '{}section Aggregator {}{}\n'.format(pinfo.indent, secTag, sopt)
					pinfo.out_file.write(str_tcl_aggregator)
				sopt1 = 'Lobatto {} {}'.format(secTag,numIntPts)
			else:
				# User defined integration with Lobatto 5P distribution
				numIntPts = pp_model.numIntPts
				secTag = pp_model.crossSection
				weights = bsutils.beam_int_lobatto.get_weights(numIntPts)
				positions = bsutils.beam_int_lobatto.get_locations(numIntPts)
				
				if numIntPts < 1:
					raise Exception ('Error: insufficient "numIntPts" ')
				if numIntPts!= (len(secTag))!= (len(positions)):
					raise Exception('Error: incorrect length between vectors "secTag", "weights" and "positions" with "numIntPts"')
		
				secTag_ = ''
				positions_ = ''
				weights_ = ''
				first = True
				for i in range(len(secTag)):
					# If necessary create the aggregator
					aggregateVy = aggregateVz = aggregateTorsion = False
					if (pp_model.includeShearVy[i]):
						if pp_model.shearVy[i] == 0:
							# This is the automatic computation
							raise Exception('Automatic computation for shear Vy not supported yet. Please select a uniaxial material for Vy')
						else:
							shearVyTag = pp_model.shearVy[i]
							aggregateVy = True
					if pp_model.dimension == '3D':
						if (pp_model.includeShearVz[i]):
							if pp_model.shearVz[i] == 0:
								# This is the automatic computation
								raise Exception('Automatic computation for shear Vz not supported yet. Please select a uniaxial material for Vz')
							else:
								shearVzTag = pp_model.shearVz[i]
								aggregateVz = True
						if (pp_model.includeTorsion[i]):
							if pp_model.torsion[i] == 0:
								# This is the automatic computation
								raise Exception('Automatic computation for torsion not supported yet. Please select a uniaxial material for torsion')
							else:
								torsionTag = pp_model.torsion[i]
								aggregateTorsion = True
					if aggregateVy or aggregateVz or aggregateTorsion:
						sopt = ''
						if aggregateVy:
							sopt += ' {} Vy'.format(shearVyTag)
						if aggregateVz:
							sopt += ' {} Vz'.format(shearVzTag)
						if aggregateTorsion:
							sopt += ' {} T'.format(torsionTag)
						sopt += ' -section {}'.format(secTag[i])
						# update the Section Tag to a new generated value
						secTag[i] = pinfo.next_physicalProperties_id # auto-generated material
						pinfo.next_physicalProperties_id += 1
						if first:
							str_tcl_aggregator = '\n{}{}\n'.format(pinfo.indent,'# Automatically generated section aggregators')
							first = False
						else:
							str_tcl_aggregator = ''
						str_tcl_aggregator += '{}section Aggregator {}{}\n'.format(pinfo.indent, secTag[i], sopt)
						pinfo.out_file.write(str_tcl_aggregator)
					secTag_ += ' {}'.format(secTag[i])
					positions_ += ' {}'.format(positions[i])
					weights_ += ' {}'.format(weights[i])
					
				sopt1 = 'UserDefined {}{}{}{}'.format(numIntPts, secTag_, positions_, weights_)
		elif (pp_model.formulation == 'lumpedFL'):
			# Hinge integration - default HingeRadau
			secTag = pp_model.crossSection
			# computation of plastic hinge length
			# TODO: move somewhere in utils????
			if not pp_model.automaticHingeLength:
				# user provided custom hinge length
				lpI = pp_model.hingeLengthI
				lpJ = pp_model.hingeLengthJ
			else:
				# TODO: compute automaticHingeLength
				lp = [0, 0]
				for k in range(2):
					i = k * 2
					# First compute length of the structural element (the Edge?)
					# length = getLengthOfStructuralElement
					length = 3000
					shearLength = length * 0.5 # Here we assume Lv = 0.5*L. If we want to do something more, we could do M/V??????
					# Then compute the depth of cross section
					if sec_xobj.name != 'RectangularFiberSection':
						raise Exception('Error: lumpedFL formulation requires a RectangularFiberSection to compute automatic plastic hinge length. Please provide it manually.')
					sec_xobj = doc.getPhysicalProperty(secTag[i]).XObject
					w = _get_xobj_attribute(sec_xobj,'Width').quantityScalar.value
					h = _get_xobj_attribute(sec_xobj,'Height').quantityScalar.value
					minimumSectionLength = min(w,h) #TODO: check if it is the minimum the right choice (we need to choose one lp for both directions)
					# Then compute the mean diameter of tensile bars - note: I am using all bars here
					phi_corner = _get_xobj_attribute(sec_xobj, 'Corner Rebars Diam').quantityScalar.value
					num_corner = _get_xobj_attribute(sec_xobj, 'Corner Rebars Number').integer
					phi_bottom = _get_xobj_attribute(sec_xobj, 'Bottom Rebars Diam').quantityScalar.value
					num_bottom = _get_xobj_attribute(sec_xobj, 'Bottom Rebars Number').integer
					phi_top = _get_xobj_attribute(sec_xobj, 'Top Rebars Diam').quantityScalar.value
					num_top = _get_xobj_attribute(sec_xobj, 'Top Rebars Number').integer
					phi_left = _get_xobj_attribute(sec_xobj, 'Left Rebars Diam').quantityScalar.value
					num_left = _get_xobj_attribute(sec_xobj, 'Left Rebars Number').integer
					phi_right = _get_xobj_attribute(sec_xobj, 'Right Rebars Diam').quantityScalar.value
					num_right = _get_xobj_attribute(sec_xobj, 'Right Rebars Number').integer
					num_bars = num_corner + num_bottom + num_top + num_left + num_right
					phi_avg = phi_corner * num_corner + phi_bottom * num_bottom + phi_top * num_top + phi_left * num_left + phi_right * num_right
					phi_avg /= num_bars
					# TODO: check if the diameter is similar for all bars (difference higher than 10%?)
					if (abs(phi_corner - phi_avg)/phi_avg > 0.1) or (abs(phi_bottom - phi_avg)/phi_avg > 0.1) or (abs(phi_top - phi_avg)/phi_avg > 0.1) or (abs(phi_left - phi_avg)/phi_avg > 0.1) or (abs(phi_right - phi_avg)/phi_avg > 0.1):
						PyMpc.IO.write_cerr('Section {} of type {} has a great difference in bars diameter. The definition of average diameter for the computation of plastic hinge length may be innacurate. Plase check carefully the situation\n'.format(secTag[i],sec_xobj.name))
					# Then compute fy from the section
					fy = _get_xobj_attribute(sec_xobj, 'fy').quantityScalar.value
					# Finally compute plastic hinge length - for now according to Priestley et al. 1996
					lp[k] = 0.08 * shearLength + 0.022 * phi_avg * fy
				lpI = lp[0]
				lpJ = lp[1]
			# If use the same section, we adopt an elastic section created on the fly
			if pp_model.sameSection:
				# The user asked to use the same section, we create a new elastic section with the correct
				# properties
				# TODO: for now I suppose to use 0.5 as modifier, but we will include that as a specific option
				Izz_modifier = 0.5
				Iyy_modifier = 0.5
				# Load the fiber section (rectangular or not)
				sec_xobj = doc.getPhysicalProperty(secTag[0]).XObject
				sf = _get_xobj_attribute(sec_xobj,'Fiber section').customObject # Returns a MpcFiberSection
				se = sf.toElasticSection(only_surfaces = True)
				p = se.properties

				# w = _get_xobj_attribute(sec_xobj,'Width').quantityScalar.value
				# h = _get_xobj_attribute(sec_xobj,'Height').quantityScalar.value
				
				# TODO: for now I create a default value of Ec because only from the rectangular fiber section I have that value
				Ec = 25000
				if sec_xobj.name == 'RectangularFiberSection': 
					Ec = _get_xobj_attribute(sec_xobj, 'Ec').quantityScalar.referenceValue
				else:
					print('WARNING: the selected section has no Ec attribute. Assumed a default value of 25000')
				ni = 0.2
				G = Ec/(2*(1+ni))
				Izz = p.Izz
				Izz *= Izz_modifier
				A = p.area
				
				secTag[1] = pinfo.next_physicalProperties_id # auto-generated material
				pinfo.next_physicalProperties_id += 1
				str_tcl_elastic = '\n{}{}\n'.format(pinfo.indent,'# Automatically generated elastic section')
				if pp_model.dimension == '2D':
					str_tcl_elastic += '{}section Elastic {} {} {} {}\n'.format(pinfo.indent, secTag[1], Ec, A, Izz)
				else:
					Iyy = p.Iyy
					Iyy *= Iyy_modifier
					J = p.J
					str_tcl_elastic += '{}section Elastic {} {} {} {} {} {} {}\n'.format(pinfo.indent, secTag[1], Ec, A, Izz, Iyy, G, J)
				pinfo.out_file.write(str_tcl_elastic)
			# If necessary create the aggregators
			first = True
			for i in range(3):
				aggregateVy = aggregateVz = aggregateTorsion = False
				if (pp_model.includeShearVy[i]):
					if pp_model.shearVy[i] == 0:
						# This is the automatic computation
						raise Exception('Automatic computation for shear Vy not supported yet. Please select a uniaxial material for Vy')
					else:
						shearVyTag = pp_model.shearVy[i]
						aggregateVy = True
				if pp_model.dimension == '3D':
					if (pp_model.includeShearVz[i]):
						if pp_model.shearVz[i] == 0:
							# This is the automatic computation
							raise Exception('Automatic computation for shear Vz not supported yet. Please select a uniaxial material for Vz')
						else:
							shearVzTag = pp_model.shearVz[i]
							aggregateVz = True
					if (pp_model.includeTorsion[i]):
						if pp_model.torsion[i] == 0:
							# This is the automatic computation
							raise Exception('Automatic computation for torsion not supported yet. Please select a uniaxial material for torsion')
						else:
							torsionTag = pp_model.torsion[i]
							aggregateTorsion = True
				if aggregateVy or aggregateVz or aggregateTorsion:
					sopt = ''
					if aggregateVy:
						sopt += ' {} Vy'.format(shearVyTag)
					if aggregateVz:
						sopt += ' {} Vz'.format(shearVzTag)
					if aggregateTorsion:
						sopt += ' {} T'.format(torsionTag)
					sopt += ' -section {}'.format(secTag[i])
					# update the Section Tag to a new generated value
					secTag[i] = pinfo.next_physicalProperties_id # auto-generated material
					pinfo.next_physicalProperties_id += 1
					if first:
						str_tcl_aggregator = '\n{}{}\n'.format(pinfo.indent,'# Automatically generated section aggregators')
						first = False
					else:
						str_tcl_aggregator = ''
					str_tcl_aggregator += '{}section Aggregator {}{}\n'.format(pinfo.indent, secTag[i], sopt)
					pinfo.out_file.write(str_tcl_aggregator)
			
			sopt1 = 'HingeRadau {} {} {} {} {}'.format(secTag[0], lpI, secTag[2], lpJ, secTag[1])
		
		sopt = ''
		
		if elem_model.get('includeMassDens'):
			sopt += ' -mass {}'.format(elem_model.get('massDens'))
		if elem_model.get('massMatrix') == 'Consistent':
			sopt += ' -cMass'
			
		# geometric transformation command
		pinfo.out_file.write(gtran.writeGeomTransfType(pinfo, (not Dimension2), elem_model.get('transformation')))
		
		str_tcl = '{}element forceBeamColumn {} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, tag, sopt1, sopt)
		
		pinfo.out_file.write(str_tcl)
	elif (pp_model.formulation == 'lumpedZL'):
		# If the model.formulation is 'lumpedZL' I treat it as a HingedBeam where:
		# - Zero length elements of extremities are defined on the fly based on pp_model
		# - Interior elasticBeamColumn (or forceBeamColumn, it is up to us)
		if elem_model.get('dimension') == '2D':
			ndm = 2
			ndf = 3
			Dimension2 = True
		else:
			ndm = 3
			ndf = 6
			Dimension2 = False
		pinfo.updateModelBuilder(ndm, ndf)
		
		# let's see if we have to build hinges, and at what sides
		do_hinge_i = (elem.nodes[0].flags & MpcNodeFlags.OnVertex)
		do_hinge_j = (elem.nodes[1].flags & MpcNodeFlags.OnVertex)
	
		# exterior elements are zero length, created here but not in STKO
		auto_gen_data = tclin.auto_generated_element_data()
		if do_hinge_i:
			exterior_elem_i = pinfo.next_elem_id
			pinfo.next_elem_id += 1
			auto_gen_data.elements.append(exterior_elem_i)
		if do_hinge_j:
			exterior_elem_j = pinfo.next_elem_id
			pinfo.next_elem_id += 1
			auto_gen_data.elements.append(exterior_elem_j)
		if len(auto_gen_data.elements):
			pinfo.auto_generated_element_data_map[elem.id] = auto_gen_data
	
		# save original nodes' ids, they are going to be changed for processing inner elements
		# and then set back to the original ones
		# why? because the nodes generated by STKO are put into the model map
		# moreover, since they are created here, they are not in the node_to_model_map
		# just add their ndm/ndf pair to the node_to_model_map copying from the exterior ones
		exterior_node_i = pinfo.elem.nodes[0].id
		exterior_node_j = pinfo.elem.nodes[1].id
		# since we are going to change them (probably) with the joint model ...
		# save a copy to be used in the finally statement
		exterior_node_i_copy = exterior_node_i
		exterior_node_j_copy = exterior_node_j
		
		# nodes
		node_vect = [exterior_node_i, exterior_node_j]
		# apply correction for joints (2D)??
		if 'RCJointModel3D' in pinfo.custom_data:
			joint_manager = pinfo.custom_data['RCJointModel3D']
			node_pos = joint_manager.adjustBeamConnectivity(pinfo, elem, node_vect)
		else:
			node_pos = [elem.nodes[0].position, elem.nodes[1].position]
		exterior_node_i = node_vect[0]
		exterior_node_j = node_vect[1]
		
		if do_hinge_i:
			interior_node_i = pinfo.next_node_id
			pinfo.next_node_id += 1
			pinfo.node_to_model_map[interior_node_i] = pinfo.node_to_model_map[exterior_node_i]
		else:
			interior_node_i = exterior_node_i
		if do_hinge_j:
			interior_node_j = pinfo.next_node_id
			pinfo.next_node_id += 1
			pinfo.node_to_model_map[interior_node_j] = pinfo.node_to_model_map[exterior_node_j]
		else:
			interior_node_j = exterior_node_j
		
		'''
		in the following code block we need to do a hack:
		we change the indices of element/nodes for processing zero-length and interior
		beam element. but actually there is only 1 element in STKO.
		to make sure that the hacking is reverted to the original state we use 
		the following try-catch-finally block
		'''
		ndm_ndf = pinfo.node_to_model_map[exterior_node_i]
		pinfo.updateModelBuilder(ndm_ndf[0], ndm_ndf[1])
		FMT = pinfo.get_double_formatter()
		try:
		
			#------------------------------------------------- Interior nodes ---------------------------------------------------
			
			if do_hinge_i or do_hinge_j:
				strNode = '{}{} {} {} {} {}\n'.format(pinfo.indent,'\n# Extra nodes for zeroLength\n# node', 'tag', 'x', 'y', 'z')
				if do_hinge_i:
					strNode += '{}node {} {} {} {}\n'.format(pinfo.indent, interior_node_i, FMT(node_pos[0].x), FMT(node_pos[0].y), FMT(node_pos[0].z))
				if do_hinge_j:
					strNode += '{}node {} {} {} {}\n'.format(pinfo.indent, interior_node_j, FMT(node_pos[1].x), FMT(node_pos[1].y), FMT(node_pos[1].z))
				pinfo.out_file.write(strNode)
			
			#------------------------------------------------------- Beam -------------------------------------------------------
			
			# hack elem nodal id!!!!
			pinfo.elem.nodes[0].id = interior_node_i
			pinfo.elem.nodes[1].id = interior_node_j
			
			# nodes
			node_vect = [node.id for node in elem.nodes]
			# apply correction for joints
			if not Dimension2:
				if 'RCJointModel3D' in pinfo.custom_data:
					joint_manager = pinfo.custom_data['RCJointModel3D']
					joint_manager.adjustBeamConnectivity(pinfo, elem, node_vect)
			nstr = ' '.join(str(i) for i in node_vect)
			
			if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line or len(node_vect)!=2):
				raise Exception('Error: invalid type of element or number of nodes for elastic beam column')
				
			# Create elastic Beam Column with properties derived from rectangular section unless specified by user
			# or ForceBeamColumn with section if the proper section was selected
			
			if pp_model.sameSection:
				# Create elasticBeamColumn with properties derived from section provided
				secTag = pp_model.crossSection[0]
				if secTag == 0:
					raise Exception('Error: To automatic create the interior elastic beam column, a proper reference section should be given')
				
				# The user asked to use the same section, we create a new elastic section with the correct properties
				# TODO: for now I suppose to use 0.5 as modifier, but we will include that as a specific option
				Izz_modifier = 0.5
				Iyy_modifier = 0.5
				# Load the fiber section (rectangular or not)
				sec_xobj = doc.getPhysicalProperty(secTag).XObject
				if sec_xobj.name in _constants.fiberSections:
					sf = _get_xobj_attribute(sec_xobj,'Fiber section').customObject # Returns a MpcFiberSection
					se = sf.toElasticSection(only_surfaces = True)
					p = se.properties
					
					param = ''
					# w = _get_xobj_attribute(sec_xobj,'Width').quantityScalar.value
					# h = _get_xobj_attribute(sec_xobj,'Height').quantityScalar.value
					A = p.area
					
					# TODO: for now I create a default value of Ec because only from the rectangular fiber section I have that value
					Ec = 25000
					if sec_xobj.name == 'RectangularFiberSection': 
						Ec = _get_xobj_attribute(sec_xobj, 'Ec').quantityScalar.referenceValue
					else:
						print('WARNING: the selected section has no Ec attribute. Assumed a default value of 25000')
					
					
					
					param += '{} {}'.format(A, Ec)

					if pp_model.dimension == '3D':
						ni = 0.2
						G = Ec/(2*(1+ni))
						J = p.J
						Iyy = p.Iyy
						Iyy *= Iyy_modifier
						
						param += ' {} {} {}'.format(G, J, Iyy)
						
					Izz = p.Izz
					Izz *= Izz_modifier
					
					param += ' {}'.format(Izz)
				
				# optional parameters
				sopt = ''
				if elem_model.get('includeMassDens'):
					sopt += ' -mass {}'.format(elem_model.get('massDens'))
				if elem_model.get('massMatrix') == 'Consistent':
					sopt += ' -cMass'
				
				# geometric transformation command
				pinfo.out_file.write(gtran.writeGeomTransfType(pinfo, (not Dimension2), elem_model.get('transformation')))
				
				str_tcl = '{}element elasticBeamColumn {} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, param, tag, sopt)
				
				pinfo.out_file.write(str_tcl)
			else:
				# Create a forceBeamColumn with the proper section
				# Create elasticBeamColumn with properties derived from section provided
				secTag = pp_model.crossSection[1]
				if secTag == 0:
					raise Exception('Error: no valid section selected for interior element of lumped beam column element {}'.format(elem.id))
				# Standard Lobatto integration 
				numIntPts = 5
				# If necessary create the aggregator
				aggregateVy = aggregateVz = aggregateTorsion = False
				if (pp_model.includeShearVy[1]):
					if pp_model.shearVy[1] == 0:
						# This is the automatic computation
						raise Exception('Automatic computation for shear Vy not supported yet. Please select a uniaxial material for Vy')
					else:
						shearVyTag = pp_model.shearVy[1]
						aggregateVy = True
				if pp_model.dimension == '3D':
					if (pp_model.includeShearVz[1]):
						if pp_model.shearVz[1] == 0:
							# This is the automatic computation
							raise Exception('Automatic computation for shear Vz not supported yet. Please select a uniaxial material for Vz')
						else:
							shearVzTag = pp_model.shearVz[1]
							aggregateVz = True
					if (pp_model.includeTorsion[1]):
						if pp_model.torsion[1] == 0:
							# This is the automatic computation
							raise Exception('Automatic computation for torsion not supported yet. Please select a uniaxial material for torsion')
						else:
							torsionTag = pp_model.torsion[1]
							aggregateTorsion = True
				if aggregateVy or aggregateVz or aggregateTorsion:
					sopt = ''
					if aggregateVy:
						sopt += ' {} Vy'.format(shearVyTag)
					if aggregateVz:
						sopt += ' {} Vz'.format(shearVzTag)
					if aggregateTorsion:
						sopt += ' {} T'.format(torsionTag)
					sopt += ' -section {}'.format(secTag)
					# update the Section Tag to a new generated value
					secTag = pinfo.next_physicalProperties_id # auto-generated material
					pinfo.next_physicalProperties_id += 1
					str_tcl_aggregator = '\n{}{}\n'.format(pinfo.indent,'# Automatically generated section aggregator')
					str_tcl_aggregator += '{}section Aggregator {}{}\n'.format(pinfo.indent, secTag, sopt)
					pinfo.out_file.write(str_tcl_aggregator)
				sopt1 = 'Lobatto {} {}'.format(secTag,numIntPts)
				
				sopt = ''
		
				if elem_model.get('includeMassDens'):
					sopt += ' -mass {}'.format(elem_model.get('massDens'))
				if elem_model.get('massMatrix') == 'Consistent':
					sopt += ' -cMass'
				
				# geometric transformation command DIEGO TODO
				pinfo.out_file.write(gtran.writeGeomTransfType(pinfo, (not Dimension2), elem_model.get('transformation')))
				
				str_tcl = '{}element forceBeamColumn {} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, tag, sopt1, sopt)
				
				pinfo.out_file.write(str_tcl)
		
			
			#---------------------------------------------------- zeroLength i ----------------------------------------------------
			
			if do_hinge_i:
				# hack elem nodal id!!!!
				pinfo.elem.nodes[0].id = exterior_node_i # master
				pinfo.elem.nodes[1].id = interior_node_i # slave
				
				# hack elements id
				pinfo.elem.id = exterior_elem_i
				
				# write a comment
				pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, 'zero_length_elements', 'zeroLength'))
				
				# build the string of nodes
				node_vect = [node.id for node in elem.nodes]
				nstr = ' '.join(str(i) for i in node_vect) 
				
				# build material and direction vectors
				mat_string = ''
				dir_string = ''
				n_dir = 0
				
				# checks on provided data for both 2d and 3d
				if not pp_model.includePmaterial[0]:
					raise Exception('No material was specified for hinge I in axial direction. Please select a material for axial direction (P material)')
				if not pp_model.includeMyMaterial[0]:
					raise Exception('No material was specified for hinge I for bending about local Y axis. Please select a material for My')
				if not pp_model.includeShearVy[0]:
					raise Exception('No material was specified for hinge I for shear in Y local  axis. Please select a material for Vy')
				if pp_model.materialP[0] == 0:
					raise Exception('Automatic computation for P is not supported yet. Please select a uniaxial material')
				if pp_model.materialMy[0] == 0:
					raise Exception('Automatic computation for My is not supported yet. Please select a uniaxial material')
				if pp_model.shearVy[0] == 0:
					raise Exception('Automatic computation for Vy is not supported yet. Please select a uniaxial material')
				if Dimension2:
					# 2D problem
					mat_string = ' {} {} {}'.format(pp_model.materialP[0],pp_model.shearVy[0],pp_model.materialMy[0])
					dir_string = ' 1 2 3'
				else:
					# 3d problem
					# additional checks:
					if not pp_model.includeTorsion[0]:
						raise Exception('No material was specified for hinge I for torsion. Please select a material for torsion')
					if not pp_model.includeMzMaterial[0]:
						raise Exception('No material was specified for hinge I for bending about local Z axis. Please select a material for Mz')
					if not pp_model.includeShearVz[0]:
						raise Exception('No material was specified for hinge I for shear in Z local  axis. Please select a material for Vz')
					if pp_model.torsion[0] == 0:
						raise Exception('Automatic computation for T is not supported yet. Please select a uniaxial material')
					if pp_model.materialMz[0] == 0:
						raise Exception('Automatic computation for Mz is not supported yet. Please select a uniaxial material')
					if pp_model.shearVz[0] == 0:
						raise Exception('Automatic computation for Vz is not supported yet. Please select a uniaxial material')
					
					mat_string = ' {} {} {} {} {} {}'.format(pp_model.materialP[0],pp_model.shearVy[0],pp_model.shearVz[0],pp_model.torsion[0],pp_model.materialMy[0],pp_model.materialMz[0])
					dir_string = ' 1 2 3 4 5 6'
				
				# orientation vectors
				vect_x=elem.orientation.computeOrientation().col(0)
				vect_y=elem.orientation.computeOrientation().col(1)
				
				# No optional data
				sopt = ''
				
				# command
				str_tcl = '{}element zeroLength {} {} -mat{} -dir{}{} -orient {} {} {} {} {} {}\n'.format(
						pinfo.indent, elem.id, nstr, mat_string, dir_string, sopt, vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
				
				# now write the string into the file
				pinfo.out_file.write(str_tcl)
			#---------------------------------------------------- zeroLength j ----------------------------------------------------
			
			if do_hinge_j:
				# hack elem nodal id!!!!
				pinfo.elem.nodes[0].id = exterior_node_j # master
				pinfo.elem.nodes[1].id = interior_node_j # slave
				
				# hack elements id
				pinfo.elem.id = exterior_elem_j
				
				# write a comment
				pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, 'zero_length_elements', 'zeroLength'))
				
				# build the string of nodes
				node_vect = [node.id for node in elem.nodes]
				nstr = ' '.join(str(i) for i in node_vect) 
				
				# build material and direction vectors
				mat_string = ''
				dir_string = ''
				n_dir = 0
				
				# checks on provided data for both 2d and 3d
				if not pp_model.includePmaterial[2]:
					raise Exception('No material was specified for hinge J in axial direction. Please select a material for axial direction (P material)')
				if not pp_model.includeMyMaterial[2]:
					raise Exception('No material was specified for hinge J for bending about local Y axis. Please select a material for My')
				if not pp_model.includeShearVy[2]:
					raise Exception('No material was specified for hinge J for shear in Y local  axis. Please select a material for Vy')
				if pp_model.materialP[2] == 0:
					raise Exception('Automatic computation for P is not supported yet. Please select a uniaxial material')
				if pp_model.materialMy[2] == 0:
					raise Exception('Automatic computation for My is not supported yet. Please select a uniaxial material')
				if pp_model.shearVy[2] == 0:
					raise Exception('Automatic computation for Vy is not supported yet. Please select a uniaxial material')
				if Dimension2:
					# 2D problem
					mat_string = ' {} {} {}'.format(pp_model.materialP[2],pp_model.shearVy[2],pp_model.materialMy[2])
					dir_string = ' 1 2 3'
				else:
					# 3d problem
					# additional checks:
					if not pp_model.includeTorsion[2]:
						raise Exception('No material was specified for hinge J for torsion. Please select a material for torsion')
					if not pp_model.includeMzMaterial[2]:
						raise Exception('No material was specified for hinge J for bending about local Z axis. Please select a material for Mz')
					if not pp_model.includeShearVz[2]:
						raise Exception('No material was specified for hinge J for shear in Z local  axis. Please select a material for Vz')
					if pp_model.torsion[2] == 0:
						raise Exception('Automatic computation for T is not supported yet. Please select a uniaxial material')
					if pp_model.materialMz[2] == 0:
						raise Exception('Automatic computation for Mz is not supported yet. Please select a uniaxial material')
					if pp_model.shearVz[2] == 0:
						raise Exception('Automatic computation for Vz is not supported yet. Please select a uniaxial material')
					
					mat_string = ' {} {} {} {} {} {}'.format(pp_model.materialP[2],pp_model.shearVy[2],pp_model.shearVz[2],pp_model.torsion[2],pp_model.materialMy[2],pp_model.materialMz[2])
					dir_string = ' 1 2 3 4 5 6'
				
				# orientation vectors
				vect_x=elem.orientation.computeOrientation().col(0)
				vect_y=elem.orientation.computeOrientation().col(1)
				
				# No optional data
				sopt = ''
				
				# command
				str_tcl = '{}element zeroLength {} {} -mat{} -dir{}{} -orient {} {} {} {} {} {}\n'.format(
						pinfo.indent, elem.id, nstr, mat_string, dir_string, sopt, vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
				
				# now write the string into the file
				pinfo.out_file.write(str_tcl)
		
		except Exception as the_exception:
			
			# re-raise the exception here
			raise the_exception
			
		finally:
			
			# get rid of the hack
			# this code MUST be called even in case of exceptions!
			# thus the finally!
			
			pinfo.elem.nodes[0].id = exterior_node_i_copy
			pinfo.elem.nodes[1].id = exterior_node_j_copy
			
			pinfo.elem.id = tag
		
		
		
def readDatastore(xobj):
	# Try to read datastore or create default data
	# This method will be called the first time the module is loaded and every other time the formulation is changed.
	
	# Read datastore attribute or load defaults (should be in the first opening, or the first use of a formulation module
	data = xobj.getAttribute(MpcXObjectMetaData.dataStoreAttributeName())
	if data is None:
		raise Exception("Cannot find dataStore Attribute")
	ds = data.string
	if RCBeamColumnElementWidget._debug:
		print('RCBeamColumnElement::readDatastore\t\t\t->\tdata: {} .'.format(data.string))
	
	try:
		jds = json.loads(ds)
		jds = jds['RCBeamColumnElement']
		#Load data if present
		dimension = jds.get('dimension','3D')
		transf = jds.get('transformation','Linear')
		includeMassDens = jds.get('includeMassDens',False)
		massDens = jds.get('massDens',0)
		massMatrix = jds.get('massMatrix','Lumped')
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
		if RCBeamColumnElementWidget._debug:
			print('impossible to read dataStore, load default - distributed formulation')
		dimension = '3D'
		transf = 'Linear'
		includeMassDens = False
		massDens = 0
		massMatrix = 'Lumped'
	# End Loading DATA
	# LOADED SAVED VALUES FROM JSON (OR DEFAULT) IF JSON IS EMPY
	return {'dimension': dimension, 'transformation': transf, 'includeMassDens': includeMassDens, 'massDens': massDens, 'massMatrix': massMatrix}
			
		
