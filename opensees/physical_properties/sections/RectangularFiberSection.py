import PyMpc.Units as u
import PyMpc.IO
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.physical_properties.sections.offset_utils as ofu
import opensees.utils.Gui.GuiUtils as gu
from opensees.physical_properties.utils.tester.StrainHistory import *
from opensees.physical_properties.utils.tester.Tester1D import Tester1D
from opensees.physical_properties.utils.tester.Tester1D import Tester1DMaterialConfinedSection
from PySide2.QtCore import QCoreApplication

import datetime

# import datetime
import math
import traceback
import importlib
import json

from PySide2.QtCore import (
	QTimer,
	QSize,
	Slot,
	QSignalBlocker
	)
from PySide2.QtWidgets import (
	QWidget,
	QDialog,
	QVBoxLayout,
	QComboBox,
	QSplitter,
	QLabel,
	QSizePolicy,
	QGridLayout,
	QTextEdit,
	QMessageBox,
	QFrame
	)
import shiboken2
# import random

class __constants:
	groups_for_section_update = ([
		'Section geometry',
		'Rebars',
		'Stirrups',
		'Materials'])
	groups_for_confined_law_update = ([
		'Confined Concrete'])
	# gui
	gui = None

'''
Massimo 2024.
Some logic for confinement is inside the GUI. This prevents somthing like re-computing
the confinement just before writing the Tcl files (for example if a material changes without
updating the section)
'''
class RCSectionLogic:
	# todo: move here all the logic from the GUI
	def obtainConfinementParameters(xobj):
		import math

		# checks
		doc = App.caeDocument()
		if doc is None:
			raise Exception('no active cae document')
		mat_cover = doc.getPhysicalProperty(_get_xobj_attribute(xobj, 'Concrete (Cover) Material').index)
		mat_core = doc.getPhysicalProperty(_get_xobj_attribute(xobj, 'Concrete (Core) Material').index)
		if mat_core:
			raise Exception('Cannot call automatic-confinement functions with a valid core material')
		if mat_cover is None:
			raise Exception('Cannot call automatic-confinement functions without a valid cover material')
		module_name = 'opensees.physical_properties.{}.{}'.format(mat_cover.XObject.Xnamespace, mat_cover.XObject.name)
		module = importlib.import_module(module_name)
		if not hasattr(module, 'getMaterialProperties'):
			raise Exception('Material {} not suported for automatic computation of confinement. Impossibile to compute automatically confined law. Provide it manually\n'.format(mat_cover.XObject.name))
		if not hasattr(module, 'getParamsConfinedVersion'):
			raise Exception('uniaxialMaterial {} for cover not recognized. Provide material for core manually'.format(mat_cover.XObject.name))

		# confinement model
		ds = xobj.getAttribute(MpcXObjectMetaData.dataStoreAttributeName()).string
		jds = json.loads(ds)
		jds = jds['ConfinedRectangulaSection']
		class_name = jds['name']
		lateral_pressure_description = jds['lat_press']
		lateral_pressure = ''
		for key, value in lateral_pressure_computation_description.items():
			if value == lateral_pressure_description:
				lateral_pressure = key

		# self.onConfinementModelChanged()
		confinementModel = ConfinementModelsFactory.make(class_name)

		# section
		W = max(1.0e-10, _get_xobj_attribute(xobj, 'Width').quantityScalar.value)
		H = max(1.0e-10, _get_xobj_attribute(xobj, 'Height').quantityScalar.value)
		C = max(1.0e-10, _get_xobj_attribute(xobj, 'Cover').quantityScalar.value)
		SD = _get_xobj_attribute(xobj, 'Stirrup Diam').quantityScalar.value
		Wc = W - 2.0*(C+SD/2.0)
		Hc = H - 2.0*(C+SD/2.0)
		Ac = Wc * Hc # Area of concrete core measured from centerline to centerline of confinement steel

		# stirrups
		AsSt = math.pi * (SD**2) / 4.0
		s = _get_xobj_attribute(xobj, 'Stirrup Spacing').quantityScalar.value
		AsY = AsSt * _get_xobj_attribute(xobj, 'Stirrup Legs Y').integer
		AsZ = AsSt * _get_xobj_attribute(xobj, 'Stirrup Legs Z').integer
		rhoY = AsY / (s * Hc)
		rhoZ = AsZ / (s * Wc)

		# rebars
		phi_corner = _get_xobj_attribute(xobj, 'Corner Rebars Diam').quantityScalar.value
		num_corner = _get_xobj_attribute(xobj, 'Corner Rebars Number').integer
		phi_bottom = _get_xobj_attribute(xobj, 'Bottom Rebars Diam').quantityScalar.value
		num_bottom = _get_xobj_attribute(xobj, 'Bottom Rebars Number').integer
		phi_top = _get_xobj_attribute(xobj, 'Top Rebars Diam').quantityScalar.value
		num_top = _get_xobj_attribute(xobj, 'Top Rebars Number').integer
		phi_left = _get_xobj_attribute(xobj, 'Left Rebars Diam').quantityScalar.value
		num_left = _get_xobj_attribute(xobj, 'Left Rebars Number').integer
		phi_right = _get_xobj_attribute(xobj, 'Right Rebars Diam').quantityScalar.value
		num_right = _get_xobj_attribute(xobj, 'Right Rebars Number').integer
		phi_max = max(phi_corner,max(phi_bottom, max(phi_top, max(phi_left, phi_right))))
		Wcc = Wc - phi_max - SD 
		Hcc = Hc - phi_max - SD
		bi2 = 0.0
		AsLong = 0.0
		# corner
		AsLong += num_corner * 4.0*(math.pi*(phi_corner**2)/4.0)
		# bottom
		if num_bottom > 0:
			Wcc_mod = Wcc
			if num_bottom > 1:
				Wcc_mod -= 2.0*Wcc/(num_bottom+1)
				bi2 += (((Wcc-Wcc_mod)/2.0)**2) * (num_bottom + 1)
			else:
				bi2 += ((Wcc/2.0)**2) * (num_bottom + 1)
			AsLong += num_bottom * math.pi * (phi_bottom**2) / 4
		else:
			bi2 += Wcc**2
		# top
		if num_top > 0:
			Wcc_mod = Wcc
			if num_top > 1:
				Wcc_mod -= 2.0*Wcc/(num_top+1)
				bi2 += (((Wcc-Wcc_mod)/2.0)**2) * (num_top + 1)
			else:
				bi2 += ((Wcc/2.0)**2) * (num_top + 1)
			AsLong += num_top * math.pi * (phi_top**2) / 4
		else:
			bi2 += Wcc**2
		# left
		if num_left > 0:
			Hcc_mod = Hcc
			if num_left > 1:
				Hcc_mod -= 2.0*Hcc/(num_left+1)
				bi2 += (((Hcc-Hcc_mod)/2.0)**2) * (num_left + 1)
			else:
				bi2 += ((Hcc/2.0)**2) * (num_left + 1)
			AsLong += num_left * math.pi * (phi_left**2) / 4
		else:
			bi2 += Hcc**2
		# right
		if num_right > 0:
			Hcc_mod = Hcc
			if num_right > 1:
				Hcc_mod -= 2.0*Hcc/(num_right+1)
				bi2 += (((Hcc-Hcc_mod)/2.0)**2) * (num_right + 1)
			else:
				bi2 += ((Hcc/2.0)**2) * (num_right + 1)
			AsLong += num_right * math.pi * (phi_right**2) / 4
		else:
			bi2 += Hcc**2
		# done
		rhoCC = AsLong/Ac # Longitudinal steel ratio

		# done
		fy = _get_xobj_attribute(xobj, 'fy').quantityScalar.value
		epssu = _get_xobj_attribute(xobj, 'epssu').real
		fc, epsc0, epscu, Ec = module.getMaterialProperties(mat_cover.XObject)
		confinementModel_params = ConfinementModelParameters( H, W, C, SD, s, bi2, rhoCC, rhoY, rhoZ, fy, epssu, fc, epsc0, epscu, Ec, lateral_pressure)

		# self.onConfinementParamsChanged()
		confinementModel.computeConfinement(confinementModel_params)
		fcc = confinementModel.fcc
		epscc0 = confinementModel.epscc0
		epsccu = confinementModel.epsccu

		# return
		print(fcc, epscc0, epsccu, Ec, lateral_pressure)
		return (fcc, epscc0, epsccu, Ec)

class RectangularFiberSectionWidget(QWidget):
	# constructor
	def __init__(self, editor, xobj, parent = None):
		
		# base class initialization
		super(RectangularFiberSectionWidget, self).__init__(parent)
		# layout
		self.setLayout(QVBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)
		
		# description label
		self.descr_label = QLabel(
			'<html><head/><body>'
			'<p align="center"><span style=" font-size:11pt; color:#003399;">'
			'Reinforced Concrete Rectangular Fiber Section'
			'</span></p>'
			'<p align="center"><span style=" color:#000000;">'
			'This widget represents the rectangular fiber section'
			'<br>The widget is connected on real-time to the attributes'
			'of the object'
			'Material response for confined and unconfined concrete will show in the chart below.'
			'</span></p>'
			'<p align="center"><span style=" font-weight:600; font-style:italic; color:#000000;">'
			'Note'
			'</span>'
			'<span style=" font-style:italic; color:#000000;">'
			': to run the test you need to have at least one external solver kit properly set up.'
			'</span></p>'
			'</body></html>'
		)
		self.descr_label.setWordWrap(True)
		self.layout().addWidget(self.descr_label)
		
		# separator
		self.separator_1 = gu.makeHSeparator()
		self.layout().addWidget(self.separator_1)
		
		# Section and options for computation of confinement
		self.sec_widget_container = QWidget()
		self.sec_widget_layout = QGridLayout()
		self.sec_widget_layout.setContentsMargins(0,0,0,0)
		self.sec_widget_container.setLayout(self.sec_widget_layout)
		# section widget container
		# # note: it comes from PyMpc so we need to take the c++ ptr
		# # and use shiboken2 to wrap it as a simple widget
		# 1) get section and clear graphis, that must be done on the main thread
		sec = _get_xobj_attribute(xobj, 'Fiber section').customObject;
		sec.clear()
		# # 2) create the scene widget, pass the section in the constructor
		# #    so that the widget will be created and optimized for visualization
		# #    of fiber cross sections
		self.sec_widget = MpcSceneWidget(sec)
		# # 3) wrap the Mpc widget by means of shiboken2
		self.scene_widget = shiboken2.wrapInstance(self.sec_widget.getPtr(), QWidget)
		self.scene_widget.setMinimumSize(QSize(250,250))
		self.sec_widget_layout.addWidget(self.scene_widget, 0, 0, 10, 1)
		
		# # Selection of confinement model
		# Label
		self.confinementModel_label_type = QLabel("Select confinement model:")
		self.sec_widget_layout.addWidget(self.confinementModel_label_type, 0, 1, 1, 1)
		# 	selection of model combobox
		self.confinementModel_cbox = QComboBox()
		for confinementModelName in ConfinementModelsFactory.getTypes():
			self.confinementModel_cbox.addItem(confinementModelName)
		self.sec_widget_layout.addWidget(self.confinementModel_cbox, 1, 1, 1, 1)
		
		# # Option for computation of lateral pressure
		# Label
		self.lateralPressure_label_type = QLabel("Select computation of lateral pressure:")
		self.sec_widget_layout.addWidget(self.lateralPressure_label_type, 2, 1, 1, 1)
		# Combobox
		self.lateralPresssure_cbox = QComboBox()
		for key in lateral_pressure_computation_description.keys():
			self.lateralPresssure_cbox.addItem(lateral_pressure_computation_description[key])
		self.sec_widget_layout.addWidget(self.lateralPresssure_cbox, 3, 1, 1, 1)
		
		# Plain text edit with reported results of computation
		self.console_text_edit = QTextEdit()
		# self.console_text_edit.setReadOnly(True)
		self.sec_widget_layout.addWidget(self.console_text_edit, 4, 1, 6, 1)
		
		# my_text_edit.setReadOnly(True)
		# You can then insert/append text using QTextCursors or using setHtml() which allows you to set the entire contents of the text edit. The formatting syntax is basic HTML, like <b> etc. you can read a bunch more about that here: http://qt-project.org/doc/qt-4.8/qtextedit.html#using-qtextedit-as-a-display-widget

		# but a simple example would be

		# my_text_edit.textCursor().insertHtml('normal text')
		# my_text_edit.textCursor().insertHtml('<b>bold text</b>')

		# add it to main widget
		self.layout().addWidget(self.sec_widget_container)
		# # set up grid strech factors
		# self.strain_hist_layout.setColumnStretch(0, 0)
		# self.strain_hist_layout.setColumnStretch(1, 0)
		# self.strain_hist_layout.setColumnStretch(2, 0)
		# self.strain_hist_layout.setColumnStretch(3, 2)
		
		# separator
		self.separator_2 = gu.makeHSeparator()
		self.layout().addWidget(self.separator_2)
		
		# Chart for unconfined and confined concrete
		# TO BE DELETED BEGIN ##############################################################
		# As test and reference include mander law - TO BE DELETED
		self.chart_data_unconfined_reference = gu.makeChartData("Unc-REF", "Strain", "Stress", 3)
		# stress-strain chart item
		chart_item = MpcChartDataGraphicItem(self.chart_data_unconfined_reference)
		chart_item.color = MpcQColor(105, 188, 255, 125)
		chart_item.thickness = 1.0
		chart_item.penStyle = MpcQPenStyle.SolidLine
		# TO BE DELETED END ##############################################################
		# Create the stress-strain for concrete unconfined (cover) and confined (core) chart
		self.chart = MpcChart(1)
		self.chart.addItem(chart_item)
		self.chart.name = "Stress-Strain response of concrete"
		# Unconfined concrete - selected by user
		self.chart_data_unconfined = gu.makeChartData("Unconfined", "Strain", "Stress", 1)
		# stress-strain chart item
		chart_item = MpcChartDataGraphicItem(self.chart_data_unconfined)
		chart_item.color = MpcQColor(56,147,255, 255)
		chart_item.thickness = 1.5
		chart_item.penStyle = MpcQPenStyle.SolidLine
		self.chart.addItem(chart_item)
		# TO BE DELETED BEGIN ##############################################################
		# As test and reference include mander law for confined concrete - TO BE DELETED
		self.chart_data_confined_reference = gu.makeChartData("Conf-REF", "Strain", "Stress", 4)
		# stress-strain chart item
		chart_item = MpcChartDataGraphicItem(self.chart_data_confined_reference)
		chart_item.color = MpcQColor(255, 136, 183, 125)
		chart_item.thickness = 1.0
		chart_item.penStyle = MpcQPenStyle.SolidLine
		self.chart.addItem(chart_item)
		# TO BE DELETED END ##############################################################
		# Confined concrete - selected by user or autocomputed
		self.chart_data_confined = gu.makeChartData("Confined", "Strain", "Stress", 2)
		# stress-strain chart item
		chart_item = MpcChartDataGraphicItem(self.chart_data_confined)
		chart_item.color = MpcQColor(255, 76, 122, 255)
		chart_item.thickness = 1.5
		chart_item.penStyle = MpcQPenStyle.SolidLine
		self.chart.addItem(chart_item)
		# stress-strain frame
		self.chart_frame = gu.makeChartFrame()
		self.layout().addWidget(self.chart_frame)
		# stress-strain chart widget
		self.mpc_chart_widget = MpcChartWidget()
		self.mpc_chart_widget.chart = self.chart
		# self.mpc_chart_widget.removeLegend()
		self.chart_widget = shiboken2.wrapInstance(self.mpc_chart_widget.getPtr(), QWidget)
		self.chart_frame.layout().addWidget(self.chart_widget)
		
		# sc = MyStaticMplCanvas()
		# self.layout().addWidget(sc)
		
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
		
		# call methods because there are not connections yet
		self.onSectionChanged()
		self.onMaterialChanged()
		
		#################################################### $JSON
		# restore initial values from datastore
		a = self.xobj.getAttribute(MpcXObjectMetaData.dataStoreAttributeName())
		if a is None:
			raise Exception("Cannot find dataStore Attribute")
		ds = a.string
		try:
			jds = json.loads(ds)
			jds = jds['ConfinedRectangulaSection']
			class_name = jds['name']
			self.confinementModel_cbox.setCurrentText(class_name)
			# call this to set up default values (no connections here)
			self.onConfinementModelChanged()
			
			lat_press = jds.get('lat_press',self.lateralPresssure_cbox.currentText())
			self.lateralPresssure_cbox.setCurrentText(lat_press)
			
			# call this to compute confinement (no connections here)
			self.onConfinementParamsChanged()
			
		except:
			# if impossible to load, load default values
			# call onConfinementModelChanged here because connections are not set yet!
			self.onConfinementModelChanged()
			self.onConfinementParamsChanged()
		#################################################### $JSON
		
		# Set the connections
		self.confinementModel_cbox.currentIndexChanged.connect(self.onConfinementModelChanged)
		self.lateralPresssure_cbox.currentIndexChanged.connect(self.onConfinementParamsChanged)
		
		# # create a timer to update the position
		# # of this dialog to follow the editor dialog every 10 milliseconds
		# self.timer = QTimer(self)
		# self.timer.timeout.connect(self.updateMyPosition)
		# self.timer.start(10)
	
	# def updateMyPosition(self):
		# # anchor this dialog to the top-right corner of
		# # the editor dialog
		# p = self.parent().pos()
		# p.setX(p.x() + self.parent().size().width())
		# self.move(p)
		
	def onSectionChanged(self):
		# This method is called when section attributes are changed
		# (e.g. width, height, cover, bars, ecc)
		sec = _get_xobj_attribute(self.xobj, 'Fiber section').customObject;
		sec.clear()
		
		# rebuild the section
		try:
			self.__build_section()
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
			
	def onMaterialChanged(self):
		# This method is called when cover material is changed
		# rebuild the section
		try:
			self.getMaterialProperties()
			if self.confinementModel_params.peakStressConcrete < 0:
				# Unconfined material was sucesfully provided
				self.runTesterUnconfined()
			else:
				# Delete unconfined curve
				self.chart_data_unconfined.x = PyMpc.Math.double_array()
				self.chart_data_unconfined.y = PyMpc.Math.double_array()
				# Update chart
				self.mpc_chart_widget.chart = self.chart
				self.mpc_chart_widget.autoScale()
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
			
	def onConfinementParamsChanged(self):
		lateral_pressure_description = self.lateralPresssure_cbox.currentText()
		lateral_pressure = "weigh_avrg"
		for key, value in lateral_pressure_computation_description.items():
			if value == lateral_pressure_description:
				lateral_pressure = key
		# print('****** Lateral pressure ** : ', lateral_pressure)
		self.confinementModel_params.lat_press_computation = lateral_pressure
		try:
			outputString = self.confinementModel.computeConfinement(self.confinementModel_params)
			# Save on the xboj the confined data
			_get_xobj_attribute(self.xobj, 'fcc').quantityScalar.referenceValue = self.confinementModel.fcc
			_get_xobj_attribute(self.xobj, 'epscc0').real = self.confinementModel.epscc0
			_get_xobj_attribute(self.xobj, 'epsccu').real = self.confinementModel.epsccu
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
		# Clear the console edit text
		self.console_text_edit.clear()
		self.console_text_edit.append(outputString)
		# Update Mander (Reference) Curves
		self.updateManderCurves()
		# Update the Confined Curves
		try:
			if self.confinementModel.fcc < 0:
				self.runTesterConfined()
			else:
				# Delete confined curve
				self.chart_data_confined.x = PyMpc.Math.double_array()
				self.chart_data_confined.y = PyMpc.Math.double_array()
				# Update chart
				self.mpc_chart_widget.chart = self.chart
				self.mpc_chart_widget.autoScale()
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
		
	def onConfinementModelChanged(self):
		# Get the name of the confinement model
		class_name = self.confinementModel_cbox.currentText()
		self.confinementModel = ConfinementModelsFactory.make(class_name)
		# send them to the ui
		# Get the default for lateral pressure computation
		self.confinementModel_params.lat_press_computation = self.confinementModel.getDefaultLateralPressureComputation()
		index = self.lateralPresssure_cbox.findText(lateral_pressure_computation_description[self.confinementModel_params.lat_press_computation])
		index = max(index, 0)
		self.lateralPresssure_cbox.setCurrentIndex(index)
		
	def getMaterialProperties(self):
		# get document, we need it to get materials
		doc = App.caeDocument()
		if doc is None:
			raise Exception('no active cae document')
		mat_cover = doc.getPhysicalProperty(_get_xobj_attribute(self.xobj, 'Concrete (Cover) Material').index)
		mat_core = doc.getPhysicalProperty(_get_xobj_attribute(self.xobj, 'Concrete (Core) Material').index)
		fy = _get_xobj_attribute(self.xobj, 'fy').quantityScalar.value
		epssu = _get_xobj_attribute(self.xobj, 'epssu').real
		
		fc = 0.0
		epsc0 = 0.0
		epscu = 0.0
		Ec = 0.0
		if mat_core is None:	
			if mat_cover is not None:
				# import the module of the material and if the function exists get the parameters
				module_name = 'opensees.physical_properties.{}.{}'.format(mat_cover.XObject.Xnamespace, mat_cover.XObject.name)
				module = importlib.import_module(module_name)
				if hasattr(module, 'getMaterialProperties'):
					fc, epsc0, epscu, Ec = module.getMaterialProperties(mat_cover.XObject)
				else:
					PyMpc.IO.write_cerr('Material {} not suported for automatic computation of confinement. Impossibile to compute automatically confined law. Provide it manually\n'.format(mat_cover.XObject.name))
					# Message box
					msg = QMessageBox()
					msg.setText("Material {} not supported for automatic computation of confinement. Impossibile to compute automatically confined law. Provide it manually\n".format(mat_cover.XObject.name))
					msg.exec()
		self.confinementModel_params.yieldStressSteel = fy
		self.confinementModel_params.ultimateStrainSteel = epssu

		self.confinementModel_params.peakStressConcrete = fc
		self.confinementModel_params.peakStrainConcrete = epsc0
		self.confinementModel_params.ultimateStrainConcrete = epscu
		self.confinementModel_params.elasticModulusConcrete = Ec
		# Save Ec in the xobj
		_get_xobj_attribute(self.xobj, 'Ec').quantityScalar.referenceValue = Ec
		
	def updateManderCurves(self):
		# compute Mander curve for unconfined concrete
		fc = self.confinementModel_params.peakStressConcrete
		epsc0 = self.confinementModel_params.peakStrainConcrete
		epscu = self.confinementModel_params.ultimateStrainConcrete
		Ec = self.confinementModel_params.elasticModulusConcrete
		eps = []
		sig = []
		if fc < 0.0:
			eps, sig = self.__compute_Mander_Law(Ec, fc, epsc0, epscu, False)
		# Update chart data
		# self.chart_data_unconfined_reference.x = PyMpc.Math.double_array()
		self.chart_data_unconfined_reference.x = PyMpc.Math.double_array(eps)
		self.chart_data_unconfined_reference.y = PyMpc.Math.double_array(sig)
		# compute Mander curve for confined concrete
		fcc = self.confinementModel.fcc
		epscc0 = self.confinementModel.epscc0
		epsccu = self.confinementModel.epsccu
		eps = []
		sig = []
		if fcc < 0.0:
			eps, sig = self.__compute_Mander_Law(Ec, fcc, epscc0, epsccu, True)
		# Update chart data
		self.chart_data_confined_reference.x = PyMpc.Math.double_array(eps)
		self.chart_data_confined_reference.y = PyMpc.Math.double_array(sig)
		# set chart
		self.mpc_chart_widget.chart = self.chart
		self.mpc_chart_widget.autoScale()
		
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
		class_name = self.confinementModel_cbox.currentText()
		lat_press_computation = self.lateralPresssure_cbox.currentText()
		jds['ConfinedRectangulaSection'] = {'name': class_name, 'lat_press': lat_press_computation}
		a.string = json.dumps(jds, indent=4)
		#################################################### $JSON
	
	def __compute_Mander_Law(self, Ec, fc, epsc0, epscu, confined):
		eps = [x * epscu/100.0 for x in range(0,102)]
		sig = [0] * len(eps)
		if fc < 0.0:
			for i in range(1,len(eps)):
				e = -eps[i]
				x = e / (-epsc0)
				Esec = fc / epsc0
				r = Ec / (Ec - Esec)
				s = -fc * x * r / (r - 1 + x**r)
				if not confined:
					if e >= (-2*epsc0):
						s = 2*(-fc)*r/(r-1+2**r)*(-epscu-e)/(-epscu-2*(-epsc0))
				if e >= (-epscu):
					s = 0
				sig[i] = -s
		return eps, sig
	
	def __build_section(self):
		import opensees.physical_properties.sections.RectangulaFiberSection_support_data.RectangularFiberSectionChecks as checks
		
		pi = 3.14159265359

		# get document, we need it to get materials
		doc = App.caeDocument()
		if doc is None:
			raise Exception('no active cae document')
		mat_core = doc.getPhysicalProperty(_get_xobj_attribute(self.xobj, 'Concrete (Core) Material').index)
		mat_cover = doc.getPhysicalProperty(_get_xobj_attribute(self.xobj, 'Concrete (Cover) Material').index)
		mat_rebars = doc.getPhysicalProperty(_get_xobj_attribute(self.xobj, 'Rebars Material').index)

		# get fiber section
		sec = _get_xobj_attribute(self.xobj, 'Fiber section').customObject;

		# parameters
		W = max(1.0e-10, _get_xobj_attribute(self.xobj, 'Width').quantityScalar.value)
		H = max(1.0e-10, _get_xobj_attribute(self.xobj, 'Height').quantityScalar.value)
		C = max(1.0e-10, _get_xobj_attribute(self.xobj, 'Cover').quantityScalar.value)
		SD = _get_xobj_attribute(self.xobj, 'Stirrup Diam').quantityScalar.value
		Wc = W - 2.0*(C+SD/2.0)
		Hc = H - 2.0*(C+SD/2.0)
		
		checks.geometry_check(W, H, C, SD)
		Ac = Wc * Hc # Area of concrete core measured from centerline to centerline of confinement steel
		
		# mesh subdivision
		subdvs = _get_xobj_attribute(self.xobj, 'Mesh Subdivisions').integer
		if subdvs < 1:
			subdvs = 15
		# lambda for 4node face
		mesh_size = max(W,H)/subdvs
		# TO DO: Option selectable by user (number of divisions / mesh_size)
		def face4(x,y,w,h,mat):
			face = FxOccFactory.surfaces().rectangle(x,y,w,h)
			face_fib_group = MpcBeamFiberSectionSurfaceFiberGroup('', face)
			face_fib_group.meshSize = mesh_size
			face_fib_group.material = mat
			face_fib_group.makeMesh()
			sec.addSurfaceFiber(face_fib_group)	
			id = 0
			if mat is not None:
				id = mat.id

		# create the core face and the cover faces
		face4(-Wc/2.0, -Hc/2.0, Wc, Hc, mat_core)
		face4(-Wc/2.0, -H/2.0, Wc, C+SD/2.0, mat_cover) # bottom
		face4(-Wc/2.0,  Hc/2.0, Wc, C+SD/2.0, mat_cover) # top
		face4(-W/2.0,  -Hc/2.0, C+SD/2.0, Hc, mat_cover) # left
		face4(Wc/2.0,  -Hc/2.0, C+SD/2.0, Hc, mat_cover) # right
		face4(-W/2.0,  -H/2.0, C+SD/2.0, C+SD/2.0, mat_cover) # bottom-left
		face4( Wc/2.0, -H/2.0, C+SD/2.0, C+SD/2.0, mat_cover) # bottom-right
		face4(-W/2.0,   Hc/2.0, C+SD/2.0, C+SD/2.0, mat_cover) # top-left
		face4( Wc/2.0,  Hc/2.0, C+SD/2.0, C+SD/2.0, mat_cover) # top-left

		# rebars
		def line2(x1,y1, x2,y2, mat, phi, num):
			line = FxOccFactory.curves().line(x1,y1, x2,y2)
			line_fib_group = MpcBeamFiberSectionPunctualFiberGroup('', line)
			dummy_spacing = 1.0
			line_fib_group.edgeData = MpcBeamFiberPunctualEdgeData(
				MpcBeamFiberPunctualEdgeDataInputType.ByNumber, phi, num, dummy_spacing)
			line_fib_group.material = mat
			line_fib_group.generateRebarsLocations()
			line_fib_group.generateFibers()
			sec.addPunctualFiber(line_fib_group)
		# add checks of number of bars TODO Diego
		phi_corner = _get_xobj_attribute(self.xobj, 'Corner Rebars Diam').quantityScalar.value
		num_corner = _get_xobj_attribute(self.xobj, 'Corner Rebars Number').integer
		if num_corner <= 0:
			msg = QMessageBox()
			msg.setText("At least one corner bar is needed")
			msg.exec()
			_get_xobj_attribute(self.xobj, 'Corner Rebars Number').integer = 1
		if num_corner > 3:
			msg = QMessageBox()
			msg.setText("Maximum 3 corner bars are supported")
			msg.exec()
			_get_xobj_attribute(self.xobj, 'Corner Rebars Number').integer = 3
		phi_bottom = _get_xobj_attribute(self.xobj, 'Bottom Rebars Diam').quantityScalar.value
		num_bottom = _get_xobj_attribute(self.xobj, 'Bottom Rebars Number').integer
		if num_bottom < 0:
			msg = QMessageBox()
			msg.setText("Negative number of bars is not allowed")
			msg.exec()
			_get_xobj_attribute(self.xobj, 'Bottom Rebars Number').integer = 0
		phi_top = _get_xobj_attribute(self.xobj, 'Top Rebars Diam').quantityScalar.value
		num_top = _get_xobj_attribute(self.xobj, 'Top Rebars Number').integer
		if num_top < 0:
			msg = QMessageBox()
			msg.setText("Negative number of bars is not allowed")
			msg.exec()
			_get_xobj_attribute(self.xobj, 'Top Rebars Number').integer = 0
		phi_left = _get_xobj_attribute(self.xobj, 'Left Rebars Diam').quantityScalar.value
		num_left = _get_xobj_attribute(self.xobj, 'Left Rebars Number').integer
		if num_left < 0:
			msg = QMessageBox()
			msg.setText("Negative number of bars is not allowed")
			msg.exec()
			_get_xobj_attribute(self.xobj, 'Left Rebars Number').integer = 0
		phi_right = _get_xobj_attribute(self.xobj, 'Right Rebars Diam').quantityScalar.value
		num_right = _get_xobj_attribute(self.xobj, 'Right Rebars Number').integer
		if num_right < 0:
			msg = QMessageBox()
			msg.setText("Negative number of bars is not allowed")
			msg.exec()
			_get_xobj_attribute(self.xobj, 'Right Rebars Number').integer = 0
		phi_max = max(phi_corner,max(phi_bottom, max(phi_top, max(phi_left, phi_right))))
		Wcc = Wc - phi_max - SD 
		Hcc = Hc - phi_max - SD
		
		# Calcolo bi2 mentre disegno le fibre di acciaio
		bi2 = 0.0
		AsLong = 4.0*(pi*(phi_corner**2)/4.0)
		numBars = 4
		
		# Draw corner bars
		line2(-Wcc/2.0, -Hcc/2.0, Wcc/2.0, -Hcc/2.0, mat_rebars, phi_corner, 2)
		line2(-Wcc/2.0,  Hcc/2.0, Wcc/2.0,  Hcc/2.0, mat_rebars, phi_corner, 2)
		if num_corner > 1:
			# Assume 2 bars
			Wcc_mod = Wcc
			Wcc_mod -= 2*phi_corner 
			line2(-Wcc_mod/2.0, -Hcc/2.0, Wcc_mod/2.0, -Hcc/2.0, mat_rebars, phi_corner, 2)
			line2(-Wcc_mod/2.0,  Hcc/2.0, Wcc_mod/2.0,  Hcc/2.0, mat_rebars, phi_corner, 2)
			AsLong += 4.0*(pi*(phi_corner**2)/4.0)
			if num_corner > 2:
				# 3 bars on the corner
				Hcc_mod = Hcc
				Hcc_mod -= 2*phi_corner
				line2(-Wcc/2.0, Hcc_mod/2.0, -Wcc/2.0, -Hcc_mod/2.0, mat_rebars, phi_corner, 2)
				line2(Wcc/2.0, Hcc_mod/2.0, Wcc/2.0, -Hcc_mod/2.0, mat_rebars, phi_corner, 2)
				AsLong += 4.0*(pi*(phi_corner**2)/4.0)
		# draw bottom bars
		if num_bottom > 0:
			Wcc_mod = Wcc
			if num_bottom > 1:
				Wcc_mod -= 2.0*Wcc/(num_bottom+1)
				bi2 += (((Wcc-Wcc_mod)/2.0)**2) * (num_bottom + 1)
			else:
				bi2 += ((Wcc/2.0)**2) * (num_bottom + 1)
			line2(-Wcc_mod/2.0, -Hcc/2.0, Wcc_mod/2.0, -Hcc/2.0, mat_rebars, phi_bottom, num_bottom)
			AsLong += num_bottom * pi * (phi_bottom**2) / 4
		else:
			bi2 += Wcc**2 
		# Draw top bars
		if num_top > 0:
			Wcc_mod = Wcc
			if num_top > 1:
				Wcc_mod -= 2.0*Wcc/(num_top+1)
				bi2 += (((Wcc-Wcc_mod)/2.0)**2) * (num_top + 1)
			else:
				bi2 += ((Wcc/2.0)**2) * (num_top + 1)
			line2(-Wcc_mod/2.0, Hcc/2.0, Wcc_mod/2.0, Hcc/2.0, mat_rebars, phi_top, num_top)
			AsLong += num_top * pi * (phi_top**2) / 4
		else:
			bi2 += Wcc**2
		# draw left bars
		if num_left > 0:
			Hcc_mod = Hcc
			if num_left > 1:
				Hcc_mod -= 2.0*Hcc/(num_left+1)
				bi2 += (((Hcc-Hcc_mod)/2.0)**2) * (num_left + 1)
			else:
				bi2 += ((Hcc/2.0)**2) * (num_left + 1)
			line2(-Wcc/2.0, -Hcc_mod/2.0, -Wcc/2.0, Hcc_mod/2.0, mat_rebars, phi_left, num_left)
			AsLong += num_left * pi * (phi_left**2) / 4
		else:
			bi2 += Hcc**2
		# draw right bars
		if num_right > 0:
			Hcc_mod = Hcc
			if num_right > 1:
				Hcc_mod -= 2.0*Hcc/(num_right+1)
				bi2 += (((Hcc-Hcc_mod)/2.0)**2) * (num_right + 1)
			else:
				bi2 += ((Hcc/2.0)**2) * (num_right + 1)
			line2(Wcc/2.0, -Hcc_mod/2.0, Wcc/2.0, Hcc_mod/2.0, mat_rebars, phi_right, num_right)
			AsLong += num_right * pi * (phi_right**2) / 4
		else:
			bi2 += Hcc**2

		# print('bi^2 = {} mm2\n'.format(bi2))
		
		rhoCC = AsLong/Ac # Longitudinal steel ratio
		
		# Stirrups
		AsSt = pi* (SD**2) / 4.0 
		s = _get_xobj_attribute(self.xobj, 'Stirrup Spacing').quantityScalar.value
		AsY = AsSt * _get_xobj_attribute(self.xobj, 'Stirrup Legs Y').integer
		AsZ = AsSt * _get_xobj_attribute(self.xobj, 'Stirrup Legs Z').integer
		rhoY = AsY / (s * Hc)
		rhoZ = AsZ / (s * Wc)
		
		# Save section parameters
		self.confinementModel_params = ConfinementModelParameters( H, W, C, SD, s, bi2, rhoCC, rhoY, rhoZ, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "weigh_avrg")
		
		# done
		sec.regenerateVisualRepresentation()
		sec.commitChanges()
		
		# build graphics (must be done on the main gui thread)
		sec.buildGraphics()

		# update bounding box and fit all
		self.sec_widget.scene.updateBoundingBox()
		self.sec_widget.fitAll()
	
	def runTesterUnconfined(self):
		# Create a strain history Monotonic for now - in the future we could add the possibility to select monotonic or cyclic
		self.strain_hist = StrainHistoryFactory.make('Monotonic')
		self.strain_hist_params = self.strain_hist.getDefaultParams()
		self.strain_hist_params.target_strain = self.confinementModel_params.ultimateStrainConcrete*1.05; #self.confinementModel.epsccu
		self.strain_hist_params.num_divisions = 20 # BUG_CBOX_RACE-make it faster
		self.strain_hist.build(self.strain_hist_params)
		# make the total analysis last 1 (pseudo) seconds.
		# this is not mandatory now, but for future works it can be useful for rate dependent models
		dtime = 0.0
		self.strain_hist_time = [0.0]*len(self.strain_hist.strain)
		if len(self.strain_hist.strain) > 1:
			dtime = 1.0/float(len(self.strain_hist.strain) - 1)
		for i in range(len(self.strain_hist.strain)):
			self.strain_hist_time[i] = float(i)*dtime
		# reset chart data
		self.chart_data_unconfined.x = PyMpc.Math.double_array()
		self.chart_data_unconfined.y = PyMpc.Math.double_array()
		
		# reset percentage data
		self.old_percentage = 0.0
		self.delta_percentage = 0.0
		
		# Create a tester object
		try:
			# check the xobject
			if self.xobj is None:
				raise Exception("The current XObject is NULL")
			# if self.xobj.parent is None:
				# raise Exception("The current XObject has no parent component")
			
			# get document, we need it to get the materials
			doc = PyMpc.App.caeDocument()
			if doc is None:
				raise Exception("No current document")
			
			# Get the cover material
			mat_cover = doc.getPhysicalProperty(_get_xobj_attribute(self.xobj, 'Concrete (Cover) Material').index)
			if mat_cover is not None:
				
				# get a unique set of all components referenced directly or indirectly
				# by parent_component.
				# this is mandatory in case the user wants to test materials that depends on other materials
				# defined previously.
				# this is a physical property so it can only reference other physical properties
				# that were defined previously, i.e. with a lower id
				ref_comp_vec = PyMpc.App.getReferencedComponents(mat_cover)
				
				# put them in an ordered map
				# so they stay ordered as in STKO.
				# this is mandatory for writing them in the correct order!
				materials = MpcPropertyCollection()
				for item in ref_comp_vec:
					if item.indexSourceType != MpcAttributeIndexSourceType.PhysicalProperty:
						raise Exception(
							'One of the referenced component\'s source type is "{}"'
							'while it should be "{}".\n'
							'This should never happen. Please contact the developers.'.format(
								item.indexSourceType,
								MpcAttributeIndexSourceType.PhysicalProperty)
							)
					materials[item.id] = item
				
				# put the materials we want to test as the last item
				materials[mat_cover.id] = mat_cover
				
				# now we can run the tester
				lch = 1.0 # not needed in this tester, just for compatibility
				self.tester = Tester1D(materials, lch, self.strain_hist_time, self.strain_hist.strain)
				#self.tester.testProcessUpdated.connect(self.onTestUnconfinedProcessUpdated)
				#parent_dialog = shiboken2.wrapInstance(self.editor.getParentWindowPtr(), QWidget)
				#parent_dialog.setEnabled(False)
				self.editor.setCanClose(False)
				try:
					self.tester.run()
					self.onTestUnconfinedProcessUpdatedAllInOne()
				finally:
					#parent_dialog.setEnabled(True)
					self.editor.setCanClose(True)
					self.tester.deleteLater()
					self.tester = None
				
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
			
	@Slot(float, float, float)
	def onTestUnconfinedProcessUpdated(self, iperc, istrain, istress):
		# update strain/stress data
		self.chart_data_unconfined.x.append(istrain)
		self.chart_data_unconfined.y.append(istress)
		# update gui:
		# note: this is visual appealing and capture the user attention while
		# a job is beeing done. however it slows down the job execution, so
		# we update the gui only at certain points
		self.delta_percentage += iperc - self.old_percentage
		self.old_percentage = iperc
		if self.delta_percentage > 0.0099 or iperc > 0.9999:
			self.delta_percentage = 0.0
			# update chart
			self.mpc_chart_widget.chart = self.chart
			self.mpc_chart_widget.autoScale()
			# update progress bar
			# self.run_progress_bar.setValue(int(round(iperc*100.0)))
			# process all events to prevent gui from freezing
			QCoreApplication.processEvents()
	def onTestUnconfinedProcessUpdatedAllInOne(self):
		# update strain/stress data
		for x,y in zip(self.tester.strain, self.tester.stress):
			self.chart_data_unconfined.x.append(x)
			self.chart_data_unconfined.y.append(y)
			# update chart
			self.mpc_chart_widget.chart = self.chart
			self.mpc_chart_widget.autoScale()
			
	def runTesterConfined(self):
		# Create a strain history Monotonic for now - in the future we could add the possibility to select monotonic or cyclic
		self.strain_hist = StrainHistoryFactory.make('Monotonic')
		self.strain_hist_params = self.strain_hist.getDefaultParams()
		self.strain_hist_params.target_strain = self.confinementModel.epsccu*1.05;
		self.strain_hist_params.num_divisions = 20 # BUG_CBOX_RACE-make it faster
		self.strain_hist.build(self.strain_hist_params)
		# make the total analysis last 1 (pseudo) seconds.
		# this is not mandatory now, but for future works it can be useful for rate dependent models
		dtime = 0.0
		self.strain_hist_time = [0.0]*len(self.strain_hist.strain)
		if len(self.strain_hist.strain) > 1:
			dtime = 1.0/float(len(self.strain_hist.strain) - 1)
		for i in range(len(self.strain_hist.strain)):
			self.strain_hist_time[i] = float(i)*dtime
		# reset chart data
		self.chart_data_confined.x = PyMpc.Math.double_array()
		self.chart_data_confined.y = PyMpc.Math.double_array()
		
		# reset percentage data
		self.old_percentage = 0.0
		self.delta_percentage = 0.0
		
		# Create a tester object
		try:
			# check the xobject
			if self.xobj is None:
				raise Exception("The current XObject is NULL")
			# if self.xobj.parent is None:
				# raise Exception("The current XObject has no parent component")
			
			# get document, we need it to get the materials
			doc = PyMpc.App.caeDocument()
			if doc is None:
				raise Exception("No current document")
				
			# Get the core material
			mat_core = doc.getPhysicalProperty(_get_xobj_attribute(self.xobj, 'Concrete (Core) Material').index)
			if mat_core is not None:
				# get a unique set of all components referenced directly or indirectly
				# by parent_component.
				# this is mandatory in case the user wants to test materials that depends on other materials
				# defined previously.
				# this is a physical property so it can only reference other physical properties
				# that were defined previously, i.e. with a lower id
				ref_comp_vec = PyMpc.App.getReferencedComponents(mat_core)
				
				# put them in an ordered map
				# so they stay ordered as in STKO.
				# this is mandatory for writing them in the correct order!
				materials = MpcPropertyCollection()
				for item in ref_comp_vec:
					if item.indexSourceType != MpcAttributeIndexSourceType.PhysicalProperty:
						raise Exception(
							'One of the referenced component\'s source type is "{}"'
							'while it should be "{}".\n'
							'This should never happen. Please contact the developers.'.format(
								item.indexSourceType,
								MpcAttributeIndexSourceType.PhysicalProperty)
							)
					materials[item.id] = item
				
				# put the materials we want to test as the last item
				materials[mat_core.id] = mat_core
				
				# now we can run the tester
				lch = 1.0 # not needed in this tester, just for compatibility
				self.tester = Tester1D(materials, lch, self.strain_hist_time, self.strain_hist.strain)
				#self.tester.testProcessUpdated.connect(self.onTestConfinedProcessUpdated)
				#parent_dialog = shiboken2.wrapInstance(self.editor.getParentWindowPtr(), QWidget)
				#parent_dialog.setEnabled(False)
				self.editor.setCanClose(False)
				try:
					self.tester.run()
					self.onTestConfinedProcessUpdatedAllInOne()
				finally:
					#parent_dialog.setEnabled(True)
					self.editor.setCanClose(True)
					self.tester.deleteLater()
					self.tester = None
			else: 
				# Get the cover material
				mat_cover = doc.getPhysicalProperty(_get_xobj_attribute(self.xobj, 'Concrete (Cover) Material').index)
				if mat_cover is not None:
					# I try to create on the fly the confined material
					# import the module of the material and if the function exists get the parameters
					module_name = 'opensees.physical_properties.{}.{}'.format(mat_cover.XObject.Xnamespace, mat_cover.XObject.name)
					module = importlib.import_module(module_name)
					if hasattr(module, 'getParamsConfinedVersion'):
						# Compute stress corresponding to ultimate strain with Mander Law
						epsccu = self.confinementModel.epsccu
						fcc = self.confinementModel.fcc
						epscc0 = self.confinementModel.epscc0
						Ec = self.confinementModel_params.elasticModulusConcrete
						e = -epsccu*0.9999
						x = e / (-epscc0)
						Esec = fcc / epscc0
						r = Ec / (Ec - Esec)
						s = -fcc * x * r / (r - 1 + x**r)
						fccu = -s
						params = module.getParamsConfinedVersion(mat_cover.XObject, fcc, epscc0, epsccu, fccu)
						materialTclString = "uniaxialMaterial {} 1".format(mat_cover.XObject.name)
						for param in params:
							materialTclString += " {}".format(param)
						# now we can run the tester
						lch = 1.0 # not needed in this tester, just for compatibility
						self.tester = Tester1DMaterialConfinedSection(materialTclString, lch, self.strain_hist_time, self.strain_hist.strain)
						#self.tester.testProcessUpdated.connect(self.onTestConfinedProcessUpdated)
						#parent_dialog = shiboken2.wrapInstance(self.editor.getParentWindowPtr(), QWidget)
						#parent_dialog.setEnabled(False)
						self.editor.setCanClose(False)
						try:
							self.tester.run()
							self.onTestConfinedProcessUpdatedAllInOne()
						finally:
							#parent_dialog.setEnabled(True)
							self.editor.setCanClose(True)
							self.tester.deleteLater()
							self.tester = None
					else:
						PyMpc.IO.write_cerr('Error: uniaxialMaterial {} for cover not recognized for computing core concrete.\n'.format(mat_cover.XObject.name))
				else:
					# I cannot create the confined material because the cover is not provided
					pass
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
			
	
	@Slot(float, float, float)
	def onTestConfinedProcessUpdated(self, iperc, istrain, istress):
		# update strain/stress data
		self.chart_data_confined.x.append(istrain)
		self.chart_data_confined.y.append(istress)
		# update gui:
		# note: this is visual appealing and capture the user attention while
		# a job is beeing done. however it slows down the job execution, so
		# we update the gui only at certain points
		self.delta_percentage += iperc - self.old_percentage
		self.old_percentage = iperc
		if self.delta_percentage > 0.0099 or iperc > 0.9999:
			self.delta_percentage = 0.0
			# update chart
			self.mpc_chart_widget.chart = self.chart
			self.mpc_chart_widget.autoScale()
			# update progress bar
			# self.run_progress_bar.setValue(int(round(iperc*100.0)))
			# process all events to prevent gui from freezing
			QCoreApplication.processEvents()
	def onTestConfinedProcessUpdatedAllInOne(self):
		# update strain/stress data
		for x,y in zip(self.tester.strain, self.tester.stress):
			self.chart_data_confined.x.append(x)
			self.chart_data_confined.y.append(y)
			# update chart
			self.mpc_chart_widget.chart = self.chart
			self.mpc_chart_widget.autoScale()

def makeXObjectMetaData():
	
	def make_attr(name, group, descr):
		at = MpcAttributeMetaData()
		at.name = name
		at.group = group
		at.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fiber_Section','Rectangular Fiber Section')+'<br/>') +
			html_end()
			)
		return at

	# Section
	at_Section = make_attr('Fiber section', 'temp', '')
	at_Section.type = MpcAttributeType.CustomAttributeObject
	at_Section.customObjectPrototype = MpcBeamFiberSection()
	at_Section.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Section.indexSource.addAllowedNamespace('materials.uniaxial') # we want uniaxial materials for fibers
	at_Section.editable = False
	
	# -GJ
	at_use_GJ = make_attr('-GJ', 'Optional parameters', 'use linear-elastic torsional')
	at_use_GJ.type = MpcAttributeType.Boolean
	at_use_GJ.visible = False
	at_use_GJ.editable = False
	at_use_GJ.setDefault(True)
	
	# -torsion
	at_use_torsion = make_attr('-torsion', 'Optional parameters', 'Specify a uniaxial material for torsion')
	at_use_torsion.type = MpcAttributeType.Boolean
	at_use_torsion.visible = False
	at_use_torsion.editable = False
	at_use_torsion.setDefault(False)
	
	# Torsion selection
	at_Torsion = make_attr('Torsion', 'Optional parameters', 'Choose between -GJ and -torsion')
	at_Torsion.type = MpcAttributeType.String
	at_Torsion.sourceType = MpcAttributeSourceType.List
	at_Torsion.setSourceList(['-GJ', '-torsion'])
	at_Torsion.setDefault('-GJ')

	# GJ
	at_GJ = make_attr('GJ', 'Optional parameters', 
				   'linear-elastic torsional stiffness assigned to the section')
	at_GJ.type = MpcAttributeType.QuantityScalar
	at_GJ.dimension = u.F/u.L**2 * u.L**4
	
	# torsionMatTag
	at_mat_torsion = make_attr('torsionMatTag', 'Optional parameters', 
				'uniaxialMaterial tag assigned to the section for torsional response (can be nonlinear)')
	at_mat_torsion.type = MpcAttributeType.Index
	at_mat_torsion.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_mat_torsion.indexSource.addAllowedNamespace("materials.uniaxial")
	# geometry --------------------------------------------------------
	
	#2D
	at_2D = make_attr('2D', 'Section geometry', '')
	at_2D.type = MpcAttributeType.Boolean
	at_2D.editable = False
	
	#3D
	at_3D = make_attr('3D', 'Section geometry', '')
	at_3D.type = MpcAttributeType.Boolean
	at_3D.editable = False
	
	# Dimension
	at_Dimension = make_attr('Dimension', 'Section geometry', 'Choose between 2D and 3D')
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('3D')
	
	# W
	at_W = make_attr('Width', 'Section geometry', '')
	at_W.type = MpcAttributeType.QuantityScalar
	at_W.dimension = u.L
	at_W.setDefault(400.0)

	# H
	at_H = make_attr('Height', 'Section geometry', '')
	at_H.type = MpcAttributeType.QuantityScalar
	at_H.dimension = u.L
	at_H.setDefault(400.0)

	# C
	at_C = make_attr('Cover', 'Section geometry', '')
	at_C.type = MpcAttributeType.QuantityScalar
	at_C.dimension = u.L
	at_C.setDefault(20.0)
	
	# meshSize
	at_meshSubdvs = make_attr('Mesh Subdivisions', 'Section geometry', 'Number of subdivisions in the longest side')
	at_meshSubdvs.type = MpcAttributeType.Integer
	at_meshSubdvs.setDefault(15)

	# geometry --------------------------------------------------------
	at_CR_diam = make_attr('Corner Rebars Diam', 'Rebars', 'Number of bars used in corner (from 1 to 3).')
	at_CR_diam.type = MpcAttributeType.QuantityScalar
	at_CR_diam.dimension = u.L
	at_CR_diam.setDefault(16.0)
	at_CR_num = make_attr('Corner Rebars Number', 'Rebars', '')
	at_CR_num.type = MpcAttributeType.Integer
	at_CR_num.setDefault(1)
	
	at_BR_diam = make_attr('Bottom Rebars Diam', 'Rebars', '')
	at_BR_diam.type = MpcAttributeType.QuantityScalar
	at_BR_diam.dimension = u.L
	at_BR_diam.setDefault(16.0)
	at_BR_num = make_attr('Bottom Rebars Number', 'Rebars', '')
	at_BR_num.type = MpcAttributeType.Integer
	at_BR_num.setDefault(1)

	at_TR_diam = make_attr('Top Rebars Diam', 'Rebars', '')
	at_TR_diam.type = MpcAttributeType.QuantityScalar
	at_TR_diam.dimension = u.L
	at_TR_diam.setDefault(16.0)
	at_TR_num = make_attr('Top Rebars Number', 'Rebars', '')
	at_TR_num.type = MpcAttributeType.Integer
	at_TR_num.setDefault(1)

	at_LR_diam = make_attr('Left Rebars Diam', 'Rebars', '')
	at_LR_diam.type = MpcAttributeType.QuantityScalar
	at_LR_diam.dimension = u.L
	at_LR_diam.setDefault(16.0)
	at_LR_num = make_attr('Left Rebars Number', 'Rebars', '')
	at_LR_num.type = MpcAttributeType.Integer
	at_LR_num.setDefault(1)

	at_RR_diam = make_attr('Right Rebars Diam', 'Rebars', '')
	at_RR_diam.type = MpcAttributeType.QuantityScalar
	at_RR_diam.dimension = u.L
	at_RR_diam.setDefault(16.0)
	at_RR_num = make_attr('Right Rebars Number', 'Rebars', '')
	at_RR_num.type = MpcAttributeType.Integer
	at_RR_num.setDefault(1)

	# geometry --------------------------------------------------------
	at_S_diam = make_attr('Stirrup Diam', 'Stirrups', '')
	at_S_diam.type = MpcAttributeType.QuantityScalar
	at_S_diam.dimension = u.L
	at_S_diam.setDefault(8.0)

	at_S_spac = make_attr('Stirrup Spacing', 'Stirrups', '')
	at_S_spac.type = MpcAttributeType.QuantityScalar
	at_S_spac.dimension = u.L
	at_S_spac.setDefault(150.0)

	at_S_legs_y = make_attr('Stirrup Legs Y', 'Stirrups', 'Number of legs parallel to Y axis')
	at_S_legs_y.type = MpcAttributeType.Integer
	at_S_legs_y.setDefault(2)

	at_S_legs_z = make_attr('Stirrup Legs Z', 'Stirrups', 'Number of legs parallel to Z axis')
	at_S_legs_z.type = MpcAttributeType.Integer
	at_S_legs_z.setDefault(2)

	# materials --------------------------------------------------------
	# core (confined) can be explicit or auto-computed with a confinement model
	at_mat_core = make_attr('Concrete (Core) Material', 'Materials', '')
	at_mat_core.type = MpcAttributeType.Index
	at_mat_core.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_mat_core.indexSource.addAllowedNamespace("materials.uniaxial")
	# cover (unconfined) is mandatory
	at_mat_cover = make_attr('Concrete (Cover) Material', 'Materials', '')
	at_mat_cover.type = MpcAttributeType.Index
	at_mat_cover.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_mat_cover.indexSource.addAllowedNamespace("materials.uniaxial")
	# rebars
	at_mat_rebars = make_attr('Rebars Material', 'Materials', '')
	at_mat_rebars.type = MpcAttributeType.Index
	at_mat_rebars.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_mat_rebars.indexSource.addAllowedNamespace("materials.uniaxial")
	#Stirrups
	# Yield strength of steel stirrups
	at_fy = make_attr('fy', 'Stirrups', 'Yield stress for stirrups')
	at_fy.type = MpcAttributeType.QuantityScalar
	at_fy.dimension = u.F/u.L**2
	at_fy.setDefault(450)
	# Ultimate strain of Stirrups
	at_epssu = make_attr('epssu', 'Stirrups', 'Ultimate strain for stirrups')
	at_epssu.type = MpcAttributeType.Real
	at_epssu.setDefault(0.15)
	
	# Results of confinement
	# Elastic modulus of concrete
	at_Ec = make_attr('Ec', 'Confinement', 'Elastic modulus of concrete')
	at_Ec.type = MpcAttributeType.QuantityScalar
	at_Ec.setDefault(0.0)
	at_Ec.visible = False
	at_Ec.editable = False
	# Confined compressive strength
	at_fcc = make_attr('fcc', 'Confinement', 'Compressive strength of confined concrete')
	at_fcc.type = MpcAttributeType.QuantityScalar
	at_fcc.dimension = u.F/u.L**2
	at_fcc.setDefault(0.0)
	at_fcc.visible = False
	at_fcc.editable = False
	# Peak strain
	at_epscc0 = make_attr('epscc0', 'Confinement', 'Peak strain of confined concrete')
	at_epscc0.type = MpcAttributeType.Real
	at_epscc0.setDefault(0.0)
	at_epscc0.visible = False
	at_epscc0.editable = False
	# Ultimate strain
	at_epsccu = make_attr('epsccu', 'Confinement', 'Ultimate strain of confined concrete')
	at_epsccu.type = MpcAttributeType.Real
	at_epsccu.setDefault(0.0)
	at_epsccu.visible = False
	at_epsccu.editable = False
	
	# make the XObject meta data
	xom = MpcXObjectMetaData()
	xom.name = 'RectangularFiberSection'
	xom.addAttribute(at_Section)
	xom.addAttribute(at_use_GJ)
	xom.addAttribute(at_use_torsion)
	xom.addAttribute(at_Torsion)
	xom.addAttribute(at_GJ)
	xom.addAttribute(at_mat_torsion)
	
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_W)
	xom.addAttribute(at_H)
	xom.addAttribute(at_C)
	xom.addAttribute(at_meshSubdvs)
	xom.addAttribute(at_CR_diam)
	xom.addAttribute(at_CR_num)
	xom.addAttribute(at_BR_diam)
	xom.addAttribute(at_BR_num)
	xom.addAttribute(at_TR_diam)
	xom.addAttribute(at_TR_num)
	xom.addAttribute(at_LR_diam)
	xom.addAttribute(at_LR_num)
	xom.addAttribute(at_RR_diam)
	xom.addAttribute(at_RR_num)
	xom.addAttribute(at_mat_core)
	xom.addAttribute(at_mat_cover)
	xom.addAttribute(at_mat_rebars)
	
	xom.addAttribute(at_S_diam)
	xom.addAttribute(at_S_spac)
	xom.addAttribute(at_S_legs_y)
	xom.addAttribute(at_S_legs_z)
	xom.addAttribute(at_fy)
	xom.addAttribute(at_epssu)
	
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_fcc)
	xom.addAttribute(at_epscc0)
	xom.addAttribute(at_epsccu)
	
	# Visibility dependecies
	xom.setVisibilityDependency(at_use_GJ, at_GJ)
	xom.setVisibilityDependency(at_use_torsion, at_mat_torsion)
	
	# auto-exclusive dependencies
	# Dimension
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	# Torsion
	xom.setBooleanAutoExclusiveDependency(at_Torsion, at_use_GJ)
	xom.setBooleanAutoExclusiveDependency(at_Torsion, at_use_torsion)
	
	# add offset
	ofu.addOffsetMetaData(xom, dep_3d = at_3D)
	
	return xom

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def __removeGui():
	if __constants.gui is not None:
		__constants.gui.setParent(None)
		__constants.gui.deleteLater()
		__constants.gui = None

def onEditorClosing(editor, xobj):
	__removeGui()

def onEditFinished(editor, xobj):
	if __constants.gui is not None:
		__constants.gui.onEditFinished()

def onEditBegin(editor, xobj):
	__removeGui()
	__constants.gui = RectangularFiberSectionWidget(editor, xobj)

def onAttributeChanged(editor, xobj, attribute_name):

	'''
	This method is called everytime the value of an attribute is changed.
	The xobject containing the modified attribute and the attribute name
	are passed as input arguments to this function.
	'''
	attribute = _get_xobj_attribute(xobj, attribute_name)

	if attribute.group in __constants.groups_for_section_update:
		# Da fare su un altro thread? Per ora no.
		__constants.gui.onSectionChanged()
		__constants.gui.onMaterialChanged()
		__constants.gui.onConfinementParamsChanged()
		

def makeExtrusionBeamDataCompoundInfo(xobj):
	
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
	
	# common
	is_param = True
	is_gap = False
	offset_y, offset_z = getSectionOffset(xobj)
	
	info = MpcSectionExtrusionBeamDataCompoundInfo()
	'''
	here the property that has the extrusion source (MpcBeamFiberSection)
	is the xobject parent itself
	'''
	if xobj.parent is not None:
		parent_id = xobj.parent.componentId
		prop = doc.getPhysicalProperty(parent_id)
		if prop is not None:
			info.add(prop, 1.0, is_param, is_gap, offset_y, offset_z)
	
	return info
	
def getSectionOffset(xobj):
	offset_y = 0.0
	offset_z = 0.0
	odata = ofu.getOffsetData(xobj)
	if odata:
		offset_y = odata.y
		offset_z = odata.z
	return offset_y, offset_z
	
def computeDomain(xobj, theta = None):
	import opensees.physical_properties.sections.RectangulaFiberSection_support_data.RectangularFiberSectionDomain as domain
	# get fiber section
	sec = _get_xobj_attribute(xobj, 'Fiber section').customObject;
	# Section data
	W = max(1.0e-10, _get_xobj_attribute(xobj, 'Width').quantityScalar.value)
	H = max(1.0e-10, _get_xobj_attribute(xobj, 'Height').quantityScalar.value)
	C = max(1.0e-10, _get_xobj_attribute(xobj, 'Cover').quantityScalar.value)
	SD = _get_xobj_attribute(xobj, 'Stirrup Diam').quantityScalar.value
	Wc = W - 2.0*(C+SD/2.0)
	Hc = H - 2.0*(C+SD/2.0)
	# Reinfocement data
	phi_corner = _get_xobj_attribute(xobj, 'Corner Rebars Diam').quantityScalar.value
	num_corner = _get_xobj_attribute(xobj, 'Corner Rebars Number').integer
	Wcc = Wc - phi_corner - SD 
	Hcc = Hc - phi_corner - SD
	# Creo delle liste per le armature: yReinf, zReinf, phiReinf
	yReinf = [-Wcc/2.0, Wcc/2.0, Wcc/2.0, -Wcc/2.0]
	zReinf = [-Hcc/2.0, -Hcc/2.0, Hcc/2.0, Hcc/2.0]
	phiReinf = [phi_corner]*4
	# Call domain construction
	if theta is None:
		print('Compute without theta')
		eps_a, kappa_y, kappa_z = domain.computeUltimateStrainConditions(W,H,C,SD,yReinf,zReinf,phiReinf,sec)
	else:
		print('Compute with theta = {}'.format(theta))
		eps_a, kappa_y, kappa_z = domain.computeUltimateStrainConditions(W,H,C,SD,yReinf,zReinf,phiReinf,sec,theta)
	N, My, Mz = domain.computeDomainForUltimateConditions(sec,eps_a,kappa_y,kappa_z)
	return N, My, Mz

def writeTcl (pinfo):
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
	mat_core = doc.getPhysicalProperty(_get_xobj_attribute(xobj, 'Concrete (Core) Material').index)
	ConfinedMaterialId = 0
	if mat_core is None:
		# if material for core is None, then create a new material on the fly with automatic confinement computation
		# I need to create a new material with the same class of the cover material
		mat_cover = doc.getPhysicalProperty(_get_xobj_attribute(xobj, 'Concrete (Cover) Material').index)
		if mat_cover is not None:
			# import the module of the material and if the function exists get the parameters
			module_name = 'opensees.physical_properties.{}.{}'.format(mat_cover.XObject.Xnamespace, mat_cover.XObject.name)
			module = importlib.import_module(module_name)
			if hasattr(module, 'getParamsConfinedVersion'):
				# Compute confined parameters
				fcc, epscc0, epsccu, Ec = RCSectionLogic.obtainConfinementParameters(xobj)
				e = -epsccu*0.9999
				x = e / (-epscc0)
				Esec = fcc / epscc0
				r = Ec / (Ec - Esec)
				s = -fcc * x * r / (r - 1 + x**r)
				fccu = -s
				params = module.getParamsConfinedVersion(mat_cover.XObject,fcc,epscc0,epsccu,fccu)
				# uniaxialMaterial {} $matTag [PARAMETERS]
				ConfinedMaterialId = pinfo.next_physicalProperties_id # auto-generated material
				pinfo.next_physicalProperties_id += 1
				str_tcl_mat_confined = '{}{}\n'.format(pinfo.indent,'\n# Automatically generated material for confined concrete core\n')
				str_tcl_mat_confined += '{}uniaxialMaterial {} {} '.format(pinfo.indent, mat_cover.XObject.name, ConfinedMaterialId)
				for p in params:
					str_tcl_mat_confined += '{} '.format(p)
				str_tcl_mat_confined += '\n'
				pinfo.out_file.write(str_tcl_mat_confined)
			else:
				str_exc = 'uniaxialMaterial {} for cover not recognized. Provide material for core manually'.format(mat_cover.XObject.name)
				raise Exception(str_exc)
	
	sopt = ''
	
	at_use_GJ = xobj.getAttribute('-GJ')
	if(at_use_GJ is None):
		raise Exception('Error: cannot find "-GJ" attribute')
	if at_use_GJ.boolean:
		at_GJ = xobj.getAttribute('GJ')
		if(at_GJ is None):
			raise Exception('Error: cannot find "GJ" attribute')
		GJ = at_GJ.quantityScalar
		
		sopt = ' -GJ {}'.format(GJ.value)
	at_use_torsion = xobj.getAttribute('-torsion')
	if(at_use_torsion is None):
		raise Exception('Error: cannot find "-torsion" attribute')
	if at_use_torsion.boolean:
		at_mat_torsion = xobj.getAttribute('torsionMatTag')
		if(at_mat_torsion is None):
			raise Exception('Error: cannot find "torsionMatTag" attribute')
		torsionMatTag = at_mat_torsion.index
		
		sopt = ' -torsion {}'.format(torsionMatTag)
	
	at_Section = xobj.getAttribute('Fiber section')
	if(at_Section is None):
		raise Exception('Error: cannot find "Fiber section" attribute')
	Section = at_Section.customObject
	
	if Section is None:
		raise Exception('Error: Section is None')
	
	cx = Section.centroid.x
	cy = Section.centroid.y
	sopt1 = ''
	for group in Section.punctualFibers:
		for fiber in group.fibers.fibers:
			sopt1 +='\nfiber {} {} {} {}'.format(fiber.x-cx, fiber.y-cy, fiber.area, group.material.id)
	sopt2 = ''
	for i in range(len(Section.surfaceFibers)):
		group = Section.surfaceFibers[i]
		for fiber in group.fibers.fibers:
			if (i == 0) and (group.material is None):
				# Core not assigned, must be the newly created one
				matid = ConfinedMaterialId
			else:
				matid = group.material.id
			sopt2 +='\nfiber {} {} {} {}'.format(fiber.x-cx, fiber.y-cy, fiber.area, matid)
	sopt3 = ''
	for group in Section.linearFibers:
		for fiber in group.fibers.fibers:
			sopt3 +='\nfiber {} {} {} {}'.format(fiber.x-cx, fiber.y-cy, fiber.area, group.material.id)
	
	str_tcl = '\n{}section Fiber {}{}'.format(pinfo.indent, tag, sopt)
	str_tcl += '{}{}{}{}{}\n'.format(' {',sopt1,sopt2,sopt3,'}')
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
	

class ConfinementModelParameters:
	def __init__(self, H, W, C, SD, s, bi2, rhoCC, rhoY, rhoZ, fy, epssu, fc, epsc0, epscu, Ec, lat_press_computation):
		self.height = H
		self.width = W
		self.cover = C
		self.stirrupsDiameter = SD
		self.stirrupsSpacing = s
		self.sumBiSquared = bi2
		self.rhoCC = rhoCC
		self.ratioStirrupsY = rhoY
		self.ratioStirrupsZ = rhoZ
		self.yieldStressSteel = fy
		self.ultimateStrainSteel = epssu
		self.peakStressConcrete = fc
		self.peakStrainConcrete = epsc0
		self.ultimateStrainConcrete = epscu
		self.elasticModulusConcrete = Ec
		self.lat_press_computation = lat_press_computation

class ConfinementManderModel:
	def __init__(self):
		# constructor
		self.fcc = 0.0
		self.epscc0 = 0.0
		self.epsccu = 0.0
		
	def computeConfinement(self, params):
		outputString = ""
		H = params.height
		W = params.width
		C = params.cover
		SD = params.stirrupsDiameter
		outputString += '<table width="100%">'
		outputString += "<tr><td colspan = \"3\"><b>Geometry:</b></td></tr>"
		outputString += "<tr><td>H</td><td>Height of the section</td><td>{}</td></tr>".format(H)
		outputString += "<tr><td>W</td><td>Width of the section</td><td>{}</td></tr>".format(W)
		outputString += "<tr><td>C</td><td>Net cover (from surface to stirrups)</td><td>{}</td></tr>".format(C)
		outputString += "<tr><td>SD</td><td>Stirrups diameter</td><td>{}</td></tr>".format(SD)
		
		rhoCC = params.rhoCC
		outputString += "<tr><td>rhoCC</td><td>Ratio of longitudinal steel</td><td>{}</td></tr>".format(rhoCC)
		
		# Concrete core width and height (measured from centerline to centerline of confinement steel)
		Wc = W - 2.0 * (C+SD/2.0)
		outputString += "<tr><td>Wc</td><td>Width of concrete core</td><td>{}</td></tr>".format(Wc)
		Hc = H - 2.0 * (C+SD/2.0)
		outputString += "<tr><td>Hc</td><td>Height of concrete core</td><td>{}</td></tr>".format(Hc)
		# Area of concrete core measured from centerline to centerline of confinement steel
		Ac = Wc * Hc
		outputString += "<tr><td>Ac</td><td>Area of confined core</td><td>{}</td></tr>".format(Ac)
		
		
		bi2 = params.sumBiSquared
		outputString += "<tr><td>bi2</td><td>Sum of squared distances between bars</td><td>{}</td></tr>".format(bi2)
		alpha_n = 1 - (bi2/6.0)/(Wc * Hc)
		outputString += "<tr><td>a_n</td><td>effectiveness factor in plane</td><td>{}</td></tr>".format(alpha_n)
		
		s = params.stirrupsSpacing
		outputString += "<tr><td>s</td><td>spacing between stirrups</td><td>{}</td></tr>".format(s)
		sp = s - SD # Clear longitudinal distance between hoops or spirals
		outputString += "<tr><td>s'</td><td>clear spacing between stirrups</td><td>{}</td></tr>".format(sp)
		alpha_s = (1-sp/(2*Wc))*(1-sp/(2*Hc))
		outputString += "<tr><td>a_s</td><td>effectiveness factor in elevation</td><td>{}</td></tr>".format(alpha_s)
		
		alpha = alpha_n * alpha_s
		outputString += "<tr><td>a</td><td>effectiveness factor = (a_s*a_n)</td><td>{}</td></tr>".format(alpha)
		
		# Concrete core area excluding longitudinal rebars
		Acc = Ac*(1-rhoCC) 
		outputString += "<tr><td>Acc</td><td>Area of confined core excluding bars</td><td>{}</td></tr>".format(Acc)
		
		Ae = Ac*(alpha) # Concrete area that is effectively confined
		outputString += "<tr><td>Ae</td><td>Area effectively confined</td><td>{}</td></tr>".format(Ae)
		Ke = Ae/Acc; # Coefficient measuring the effectiveness of the confinemenet steel
		outputString += "<tr><td>Ke</td><td>Effectiveness factor</td><td>{}</td></tr>".format(Ke)
		
		# Material properties for stirrups (steel)
		fy = params.yieldStressSteel
		epssu = params.ultimateStrainSteel
		outputString += "<tr><td colspan = \"3\"><b>Materials:</b></td></tr>"
		outputString += "<tr><td>fy</td><td>Yield stress for steel of stirrups</td><td>{}</td></tr>".format(fy)
		outputString += "<tr><td>epssu</td><td>Ultimate strain for steel of stirrups</td><td>{:.3f} %</td></tr>".format(epssu*100)
		# Material properties for concrete
		fc = params.peakStressConcrete
		epsc0 = params.peakStrainConcrete
		epscu = params.ultimateStrainConcrete
		outputString += "<tr><td>fc</td><td>Peak stress for unconfined concrete</td><td>{}</td></tr>".format(fc)
		outputString += "<tr><td>epsc0</td><td>Peak strain for unconfined concrete</td><td>{:.3f} ‰</td></tr>".format(epsc0*1000)
		outputString += "<tr><td>epscu</td><td>Ultimate strain for unconfined concrete</td><td>{:.3f} ‰</td></tr>".format(epscu*1000)
		
		# return 0, 0, 0, ["test", "test"]
		# only if I have valid material properties
		if fc < 0.0 and fy > 0.0:
			fc = -fc
			outputString += "<tr><td colspan = \"3\"><b>Confinement computation:</b></td></tr>"
			# Lateral pressure by stirrups in Y and Z directions
			rhoY = params.ratioStirrupsY
			rhoZ = params.ratioStirrupsZ
			outputString += "<tr><td>rhoY</td><td>Stirrups ratio parallel to Y dir</td><td>{}</td></tr>".format(rhoY)
			outputString += "<tr><td>rhoZ</td><td>Stirrups ratio parallel to Z dir</td><td>{}</td></tr>".format(rhoZ)
			
			fLY = rhoY * fy
			fLZ = rhoZ * fy
			outputString += "<tr><td>fLY</td><td>Lateral pressure in Y direction</td><td>{}</td></tr>".format(fLY)
			outputString += "<tr><td>fLZ</td><td>Lateral pressure in Z direction</td><td>{}</td></tr>".format(fLZ)
			# Effective lateral pressure by stirrups in Y and Z directions
			fLYp = fLY * Ke
			fLZp = fLZ * Ke
			outputString += "<tr><td>fLY'</td><td>Effective lateral pressure in Y direction</td><td>{}</td></tr>".format(fLYp)
			outputString += "<tr><td>fLZ'</td><td>Effective lateral pressure in Z direction</td><td>{}</td></tr>".format(fLZp)
			# Computation of mean lateral pressure based on selected option
			lat_pressure_computation = params.lat_press_computation
			if lat_pressure_computation not in lateral_pressure_computation_description.keys():
				PyMpc.IO.write_cerr('Warning - Option for lateral pressure computation not recognized\nAssumed Weighted Average\n')
				lat_pressure_computation = "weigh_avrg"
			outputString += "<tr><td colspan = \"3\">Lateral pressure computed with {}</td></tr>".format(lateral_pressure_computation_description[lat_pressure_computation])
			s2, s3 = fLYp, fLZp
			if s2 < s3:
				s2, s3 = s3, s2
			s_lat = getLateralEquivalentPressure(lat_pressure_computation,s2,s3,fc)
			outputString += "<tr><td>fLp</td><td>Lateral pressure</td><td>{}</td></tr>".format(s_lat)
			K = 2.254*(math.sqrt(1+7.94*s_lat/fc)-1)-2*s_lat/fc
			outputString += "<tr><td>K</td><td>Strength increment coefficient</td><td>{}</td></tr>".format(K)
			fcc = -fc * (1 + K)
			# Computation of peak strain
			epscc0 = epsc0 * (1 + 5*K)
			# Computation of ultimate strain
			# Approx. formulation Fardis
			epsccu = -(-epscu + 2 * epssu * (-s_lat)/fcc)
			
			outputString += "<tr><td><b><i>fcc</b></i></td><td><b><i>Strength of confined concrete</b></i></td><td><b><i>{:.3f}</b></i></td></tr>".format(fcc)
			outputString += "<tr><td><b><i>epscc0</b></i></td><td><b><i>Peak strain of confined concrete</b></i></td><td><b><i>{:.3f} ‰</b></i></td></tr>".format(epscc0*1000)
			outputString += "<tr><td><b><i>epsccu</b></i></td><td><b><i>Ultimate strain of confined concrete</b></i></td><td><b><i>{:.3f} ‰</b></i></td></tr>".format(epsccu*1000)
		else:
			# If settings are wrong use unconfind also for core
			outputString += "<tr><td><b><i>No Confinement computation</i></b></td></tr>"
			fcc = fc
			epscc0 = epsc0
			epsccu = epscu
		outputString += "<\table>"
		
		self.fcc = fcc
		self.epscc0 = epscc0
		self.epsccu = epsccu
		return outputString
		
	def getDefaultLateralPressureComputation(self):
		return ("willam_warnke")
		
class ConfinementEN1998_3Model:
	def __init__(self):
		# constructor
		self.fcc = 0.0
		self.epscc0 = 0.0
		self.epsccu = 0.0
		
	def computeConfinement(self, params):
		outputString = ""
		H = params.height
		W = params.width
		C = params.cover
		SD = params.stirrupsDiameter
		outputString += '<table width="100%">'
		outputString += "<tr><td colspan = \"3\"><b>Geometry:</b></td></tr>"
		outputString += "<tr><td>H</td><td>Height of the section</td><td>{}</td></tr>".format(H)
		outputString += "<tr><td>W</td><td>Width of the section</td><td>{}</td></tr>".format(W)
		outputString += "<tr><td>C</td><td>Net cover (from surface to stirrups)</td><td>{}</td></tr>".format(C)
		outputString += "<tr><td>SD</td><td>Stirrups diameter</td><td>{}</td></tr>".format(SD)
		
		rhoCC = params.rhoCC
		outputString += "<tr><td>rhoCC</td><td>Ratio of longitudinal steel</td><td>{}</td></tr>".format(rhoCC)
		
		# Concrete core width and height (measured from centerline to centerline of confinement steel)
		Wc = W - 2.0 * (C+SD/2.0)
		outputString += "<tr><td>Wc</td><td>Width of concrete core</td><td>{}</td></tr>".format(Wc)
		Hc = H - 2.0 * (C+SD/2.0)
		outputString += "<tr><td>Hc</td><td>Height of concrete core</td><td>{}</td></tr>".format(Hc)
		# Area of concrete core measured from centerline to centerline of confinement steel
		Ac = Wc * Hc
		outputString += "<tr><td>Ac</td><td>Area of confined core</td><td>{}</td></tr>".format(Ac)
		
		
		bi2 = params.sumBiSquared
		outputString += "<tr><td>bi2</td><td>Sum of squared distances between bars</td><td>{}</td></tr>".format(bi2)
		# NTC 2018 eq [4.1.12.f] ed EC 
		alpha_n = 1 - (bi2/6.0)/(Wc * Hc)
		outputString += "<tr><td>a_n</td><td>effectiveness factor in plane</td><td>{}</td></tr>".format(alpha_n)
		
		s = params.stirrupsSpacing
		outputString += "<tr><td>s</td><td>spacing between stirrups</td><td>{}</td></tr>".format(s)
		# NTC 2018 eq [4.1.12.g] ed EC 
		alpha_s = (1-s/(2*Wc))*(1-s/(2*Hc))
		outputString += "<tr><td>a_s</td><td>effectiveness factor in elevation</td><td>{}</td></tr>".format(alpha_s)
		
		alpha = alpha_n * alpha_s
		outputString += "<tr><td>a</td><td>effectiveness factor = (a_s*a_n)</td><td>{}</td></tr>".format(alpha)
		
		# Concrete core area excluding longitudinal rebars
		Acc = Ac*(1-rhoCC) 
		outputString += "<tr><td>Acc</td><td>Area of confined core excluding bars</td><td>{}</td></tr>".format(Acc)
		
		Ae = Acc*(alpha) # Concrete area that is effectively confined
		outputString += "<tr><td>Ae</td><td>Area effectively confined</td><td>{}</td></tr>".format(Ae)
		
		# Material properties for stirrups (steel)
		fy = params.yieldStressSteel
		epssu = params.ultimateStrainSteel
		outputString += "<tr><td colspan = \"3\"><b>Materials:</b></td></tr>"
		outputString += "<tr><td>fy</td><td>Yield stress for steel of stirrups</td><td>{}</td></tr>".format(fy)
		outputString += "<tr><td>epssu</td><td>Ultimate strain for steel of stirrups</td><td>{:.3f} %</td></tr>".format(epssu*100)
		# Material properties for concrete
		fc = params.peakStressConcrete
		epsc0 = params.peakStrainConcrete
		epscu = params.ultimateStrainConcrete
		outputString += "<tr><td>fc</td><td>Peak stress for unconfined concrete</td><td>{}</td></tr>".format(fc)
		outputString += "<tr><td>epssu</td><td>Ultimate strain for steel of stirrups</td><td>{:.3f} ‰</td></tr>".format(epsc0*1000)
		outputString += "<tr><td>epssu</td><td>Ultimate strain for steel of stirrups</td><td>{:.3f} ‰</td></tr>".format(epscu*1000)
		
		# return 0, 0, 0, ["test", "test"]
		# only if I have valid material properties
		if fc < 0.0 and fy > 0.0:
			fc = -fc
			outputString += "<tr><td colspan = \"3\"><b>Confinement computation:</b></td></tr>"
			# Lateral pressure by stirrups in Y and Z directions
			rhoY = params.ratioStirrupsY
			rhoZ = params.ratioStirrupsZ
			outputString += "<tr><td>rhoY</td><td>Stirrups ratio parallel to Y dir</td><td>{}</td></tr>".format(rhoY)
			outputString += "<tr><td>rhoZ</td><td>Stirrups ratio parallel to Z dir</td><td>{}</td></tr>".format(rhoZ)
			
			fLY = rhoY * fy
			fLZ = rhoZ * fy
			outputString += "<tr><td>fLY</td><td>Lateral pressure in Y direction</td><td>{}</td></tr>".format(fLY)
			outputString += "<tr><td>fLZ</td><td>Lateral pressure in Z direction</td><td>{}</td></tr>".format(fLZ)
			
			# Computation of mean lateral pressure based on selected option
			lat_pressure_computation = params.lat_press_computation
			if lat_pressure_computation not in lateral_pressure_computation_description.keys():
				PyMpc.IO.write_cerr('Warning - Option for lateral pressure computation not recognized\nAssumed Weighted Average\n')
				lat_pressure_computation = "weigh_avrg"
			outputString += "<tr><td colspan = \"3\">Lateral pressure computed with {}</td></tr>".format(lateral_pressure_computation_description[lat_pressure_computation])
			s2, s3 = fLY, fLZ
			if s2 < s3:
				s2, s3 = s3, s2
			s_lat = getLateralEquivalentPressure(lat_pressure_computation,s2,s3,fc)
			outputString += "<tr><td>fL</td><td>Lateral pressure</td><td>{}</td></tr>".format(s_lat)
			s_lat *= alpha # Attenzione Fardis che va capito se coefficiente a può moltiplicare p7fc.. dipende se K lineare o no...
			outputString += "<tr><td>fL'</td><td>Effective ateral pressure</td><td>{}</td></tr>".format(s_lat)
			# Strength increment EC8-3:2005 eq [A.6] - Newman & Newman (1971)
			K = 3.7*(s_lat/fc)**0.86
			outputString += "<tr><td>K</td><td>Strength increment coefficient</td><td>{}</td></tr>".format(K)
			fcc = -fc * (1 + K)
			# Computation of peak strain EC8-3:2005 eq [A.7] Richart et al. (1928)
			epscc0 = epsc0 * (1 + 5*K)
			# Computation of ultimate strain EC8-3:2005 eq [A.8]
			epsccu = -(0.004 + 0.5*s_lat/fc)
			
			outputString += "<tr><td><b><i>fcc</b></i></td><td><b><i>Strength of confined concrete</b></i></td><td><b><i>{:.3f}</b></i></td></tr>".format(fcc)
			outputString += "<tr><td><b><i>epscc0</b></i></td><td><b><i>Peak strain of confined concrete</b></i></td><td><b><i>{:.3f} ‰</b></i></td></tr>".format(epscc0*1000)
			outputString += "<tr><td><b><i>epsccu</b></i></td><td><b><i>Peak strain of confined concrete</b></i></td><td><b><i>{:.3f} ‰</b></i></td></tr>".format(epsccu*1000)
		else:
			# If settings are wrong use unconfind also for core
			outputString += "<tr><td><b><i>No Confinement computation</i></b></td></tr>"
			fcc = fc
			epscc0 = epsc0
			epsccu = epscu
		outputString += "<\table>"
		
		self.fcc = fcc
		self.epscc0 = epscc0
		self.epsccu = epsccu
		return outputString
		
	def getDefaultLateralPressureComputation(self):
		return ("weigh_avrg")
		
class ConfinementNTC2018Model:
	def __init__(self):
		# constructor
		self.fcc = 0.0
		self.epscc0 = 0.0
		self.epsccu = 0.0
		
	def computeConfinement(self, params):
		outputString = ""
		H = params.height
		W = params.width
		C = params.cover
		SD = params.stirrupsDiameter
		outputString += '<table width="100%">'
		outputString += "<tr><td colspan = \"3\"><b>Geometry:</b></td></tr>"
		outputString += "<tr><td>H</td><td>Height of the section</td><td>{}</td></tr>".format(H)
		outputString += "<tr><td>W</td><td>Width of the section</td><td>{}</td></tr>".format(W)
		outputString += "<tr><td>C</td><td>Net cover (from surface to stirrups)</td><td>{}</td></tr>".format(C)
		outputString += "<tr><td>SD</td><td>Stirrups diameter</td><td>{}</td></tr>".format(SD)
		
		rhoCC = params.rhoCC
		outputString += "<tr><td>rhoCC</td><td>Ratio of longitudinal steel</td><td>{}</td></tr>".format(rhoCC)
		
		# Concrete core width and height (measured from centerline to centerline of confinement steel)
		Wc = W - 2.0 * (C+SD/2.0)
		outputString += "<tr><td>Wc</td><td>Width of concrete core</td><td>{}</td></tr>".format(Wc)
		Hc = H - 2.0 * (C+SD/2.0)
		outputString += "<tr><td>Hc</td><td>Height of concrete core</td><td>{}</td></tr>".format(Hc)
		# Area of concrete core measured from centerline to centerline of confinement steel
		Ac = Wc * Hc
		outputString += "<tr><td>Ac</td><td>Area of confined core</td><td>{}</td></tr>".format(Ac)
		
		
		bi2 = params.sumBiSquared
		outputString += "<tr><td>bi2</td><td>Sum of squared distances between bars</td><td>{}</td></tr>".format(bi2)
		# NTC2018 eq [4.1.12.f]
		alpha_n = 1 - (bi2/6.0)/(Wc * Hc)
		outputString += "<tr><td>a_n</td><td>effectiveness factor in plane</td><td>{}</td></tr>".format(alpha_n)
		
		s = params.stirrupsSpacing
		outputString += "<tr><td>s</td><td>spacing between stirrups</td><td>{}</td></tr>".format(s)
		# NTC2018 eq [4.1.12.g]
		alpha_s = (1-s/(2*Wc))*(1-s/(2*Hc))
		outputString += "<tr><td>a_s</td><td>effectiveness factor in elevation</td><td>{}</td></tr>".format(alpha_s)
		
		# NTC2018 eq [4.1.12.f]
		alpha = alpha_n * alpha_s
		outputString += "<tr><td>a</td><td>effectiveness factor = (a_s*a_n)</td><td>{}</td></tr>".format(alpha)
		
		# Concrete core area excluding longitudinal rebars
		Acc = Ac*(1-rhoCC) 
		outputString += "<tr><td>Acc</td><td>Area of confined core excluding bars</td><td>{}</td></tr>".format(Acc)
		
		Ae = Acc*(alpha) # Concrete area that is effectively confined
		outputString += "<tr><td>Ae</td><td>Area effectively confined</td><td>{}</td></tr>".format(Ae)
		
		# Material properties for stirrups (steel)
		fy = params.yieldStressSteel
		epssu = params.ultimateStrainSteel
		outputString += "<tr><td colspan = \"3\"><b>Materials:</b></td></tr>"
		outputString += "<tr><td>fy</td><td>Yield stress for steel of stirrups</td><td>{}</td></tr>".format(fy)
		outputString += "<tr><td>epssu</td><td>Ultimate strain for steel of stirrups</td><td>{:.3f} %</td></tr>".format(epssu*100)
		# Material properties for concrete
		fc = params.peakStressConcrete
		epsc0 = params.peakStrainConcrete
		epscu = params.ultimateStrainConcrete
		outputString += "<tr><td>fc</td><td>Peak stress for unconfined concrete</td><td>{}</td></tr>".format(fc)
		outputString += "<tr><td>epssu</td><td>Ultimate strain for steel of stirrups</td><td>{:.3f} ‰</td></tr>".format(epsc0*1000)
		outputString += "<tr><td>epssu</td><td>Ultimate strain for steel of stirrups</td><td>{:.3f} ‰</td></tr>".format(epscu*1000)
		
		# return 0, 0, 0, ["test", "test"]
		# only if I have valid material properties
		if fc < 0.0 and fy > 0.0:
			fc = -fc
			outputString += "<tr><td colspan = \"3\"><b>Confinement computation:</b></td></tr>"
			# Lateral pressure by stirrups in Y and Z directions
			rhoY = params.ratioStirrupsY
			rhoZ = params.ratioStirrupsZ
			outputString += "<tr><td>rhoY</td><td>Stirrups ratio parallel to Y dir</td><td>{}</td></tr>".format(rhoY)
			outputString += "<tr><td>rhoZ</td><td>Stirrups ratio parallel to Z dir</td><td>{}</td></tr>".format(rhoZ)
			fLY = rhoY * fy
			fLZ = rhoZ * fy
			outputString += "<tr><td>fLY</td><td>Lateral pressure in Y direction</td><td>{}</td></tr>".format(fLY)
			outputString += "<tr><td>fLZ</td><td>Lateral pressure in Z direction</td><td>{}</td></tr>".format(fLZ)
			# Computation of mean lateral pressure based on selected option
			lat_pressure_computation = params.lat_press_computation
			if lat_pressure_computation not in lateral_pressure_computation_description.keys():
				PyMpc.IO.write_cerr('Warning - Option for lateral pressure computation not recognized\nAssumed Weighted Average\n')
				lat_pressure_computation = "weigh_avrg"
			outputString += "<tr><td colspan = \"3\">Lateral pressure computed with {}</td></tr>".format(lateral_pressure_computation_description[lat_pressure_computation])
			s2, s3 = fLY, fLZ
			if s2 < s3:
				s2, s3 = s3, s2
			s_lat = getLateralEquivalentPressure(lat_pressure_computation,s2,s3,fc)
			outputString += "<tr><td>fLp</td><td>Lateral pressure</td><td>{}</td></tr>".format(s_lat)
			# NTC2018 eq [4.1.12.a]
			s_lat *= alpha 
			# Strength increment - NTC2018 eq [4.1.8-9]
			if s_lat/fc <= 0.05:
				fcc = fc * (1 + 5 * s_lat/fc) # eq [4.1.8]
			else:
				fcc = fc * (1.125 + 2.5 * s_lat/fc) # eq [4.1.9]
			K = fcc / fc - 1
			fcc *= -1
			outputString += "<tr><td>K</td><td>Strength increment coefficient</td><td>{}</td></tr>".format(K)
			# Computation of peak strain - NTC2018 eq [4.1.10]
			epscc0 = epsc0 * (-fcc/fc)**2

			# Computation of ultimate strain - NTC2018 eq [4.1.11]
			epsccu = -(0.0035 + 0.2 * s_lat/fc)
			
			outputString += "<tr><td><b><i>fcc</b></i></td><td><b><i>Strength of confined concrete</b></i></td><td><b><i>{:.3f}</b></i></td></tr>".format(fcc)
			outputString += "<tr><td><b><i>epscc0</b></i></td><td><b><i>Peak strain of confined concrete</b></i></td><td><b><i>{:.3f} ‰</b></i></td></tr>".format(epscc0*1000)
			outputString += "<tr><td><b><i>epsccu</b></i></td><td><b><i>Peak strain of confined concrete</b></i></td><td><b><i>{:.3f} ‰</b></i></td></tr>".format(epsccu*1000)
		else:
			# If settings are wrong use unconfind also for core
			outputString += "<tr><td><b><i>No Confinement computation</i></b></td></tr>"
			fcc = fc
			epscc0 = epsc0
			epsccu = epscu
		outputString += "<\table>"
		
		self.fcc = fcc
		self.epscc0 = epscc0
		self.epsccu = epsccu
		return outputString
		
	def getDefaultLateralPressureComputation(self):
		return ("geom_avrg")

## A Factory class used to generate strain histories given their names
class ConfinementModelsFactory:
	
	## A static dictionary that maps class names to class types
	supportedTypes = {
		"Mander et al. 1988" : ConfinementManderModel,
		"EN1998-3" : ConfinementEN1998_3Model,
		"NTC 2018" : ConfinementNTC2018Model
		}
	
	## Gives a list of names of all supported strain history types
	@staticmethod
	def getTypes():
		return ConfinementModelsFactory.supportedTypes.keys()
	
	## Constructs the required type given its name.
	# @note If the given name is not among the ones given by @ref getTypes
	# and Exception will be thrown
	@staticmethod
	def make(className):
		if not className in ConfinementModelsFactory.supportedTypes.keys():
			raise Exception('The given class "{}" is not supported by the ConfinementModelsFactory'.format(className))
		classType = ConfinementModelsFactory.supportedTypes[className]
		return classType()

# A static dictionary for the options of computation of lateral pressure
lateral_pressure_computation_description = {
	"willam_warnke": "Willam and Warnke 5-p surface",
	"weigh_avrg": "Weighted average: slat = (s2+4*s3)/5",
	"geom_avrg": "Geometric average: slat = (s2*s3)^0.5",
	"arith_avrg": "Arithmetic average: slat = (s2+s3)/2",
	"min": "Minimum value: slat = min(s2,s3)"
}

def weighted_average(s2, s3, fc):
	return (s2 + 4*s3)/5.0
	
def geometric_average(s2, s3, fc):
	return math.sqrt(s2 * s3)
	
def arithmetic_average(s2, s3, fc):
	return (s2 + s3) / 2.0
	
def minimum_pressure(s2, s3, fc):
	return min(s2, s3)
	
def willam_warnke(s2, s3, fc):
	s1 = -s3
	s2 = -s2
	s3 = -fc
	
	sig_oct = 1.0/3.0 * (s1 + s2 + s3)
	tau_oct = 1.0/3.0 * math.sqrt((s1-s2)**2 + (s2-s3)**2 + (s3-s1)**2)
	cosTheta = (s1-sig_oct) / (math.sqrt(2.0)*tau_oct)
	
	s_oct = sig_oct / fc
	T = 0.069232-0.661091*s_oct-0.049350*s_oct**2;
	C = 0.122965-1.150502*s_oct-0.315545*s_oct**2;
	
	D = 4*(C**2-T**2)*cosTheta**2;
	t_oct = C*(0.5*D/cosTheta+(2*T-C)*(D+5*T**2-4*T*C)**0.5)/(D+(2*T-C)**2)
	tau_oct2 = fc * t_oct
	sig_3 = (s1+s2)/2-math.sqrt(4.5*tau_oct2**2-0.75*(s1-s2)**2)
	maxIter = 100
	i = 1
	while (abs(sig_3-s3) >= 0.001) and (i <= maxIter):
		s3 = sig_3
		sig_oct = 1.0/3.0 * (s1 + s2 + s3)
		tau_oct = 1.0/3.0 * math.sqrt((s1-s2)**2 + (s2-s3)**2 + (s3-s1)**2)
		cosTheta = (s1-sig_oct) / (math.sqrt(2.0)*tau_oct)
		
		s_oct = sig_oct / fc
		T = 0.069232-0.661091*s_oct-0.049350*s_oct**2;
		C = 0.122965-1.150502*s_oct-0.315545*s_oct**2;
		
		D = 4*(C**2-T**2)*cosTheta**2;
		t_oct = C*(0.5*D/cosTheta+(2*T-C)*(D+5*T**2-4*T*C)**0.5)/(D+(2*T-C)**2)
		tau_oct2 = fc * t_oct
		sig_3 = (s1+s2)/2-math.sqrt(4.5*tau_oct2**2-0.75*(s1-s2)**2)
		i += 1
	
	# Computation of lateral pressure to give sig_3 = fcc
	if i >= maxIter:
		print("WARNING: Solution of Willam and Warnke surface not found, used weighted average")
		s_lat = weighted_average(-s1,-s2,fc)
		K = 2.254*(math.sqrt(1+7.94*s_lat/fc)-1)-2*s_lat/fc
		fcc = fc * (1 + K)
	else:
		fcc = sig_3
		K = (fcc / -fc) - 1
		s_lat = (391541213.0/100000000.0 - (153304521477511369.0/2500.0 - 20169648520000.0*K)**(0.5)/2000000.0 - K/2.0)*(-fc)
	return -s_lat

def getLateralEquivalentPressure(key,s2,s3,fc):
	lateral_pressure_computation_switcher = {
		"willam_warnke": willam_warnke,
		"weigh_avrg": weighted_average,
		"geom_avrg": geometric_average,
		"arith_avrg": arithmetic_average,
		"min": minimum_pressure
	}
	func = lateral_pressure_computation_switcher.get(key, lambda: "Invalid selection") # Non dovrebbe mai essere invalid
	return func(s2,s3,fc)