## @package TesterTIM6D
# The TesterTIM6D packages contains the tester and widget classes that are used
# to run a test of a TIM material

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
import opensees.utils.write_physical_properties as write_physical_properties
import opensees.utils.Gui.GuiUtils as gu
import opensees.utils.Gui.TesterUtils as tu
from opensees.physical_properties.utils.tester.StrainHistory import *

from PySide2.QtCore import (
	QObject,
	Signal,
	Slot,
	QSignalBlocker,
	QLocale,
	QCoreApplication,
	QTimer,
	Qt,
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
	QRadioButton,
	QTabWidget,
	QToolBar,
	QDialog,
	QFileDialog,
	QMessageBox,
	QSizePolicy,
	QTableWidget,
	QTableWidgetItem
	)
import shiboken2


class TIMTraits:
	# types
	D3 = 0
	D5 = 1
	D6 = 2
	# attributes
	FREEDOFS = ["0 0 0 1 1 1", "0 0 0 0 0 1", "0 0 0 0 0 0"]
	STRAIN_SIZE = 6
	STRESS_COMPONENTS = ['Q\u2081', 'Q\u2082', 'Q\u2083', 'QR\u2081', 'QR\u2082', 'QR\u2083']
	STRAIN_COMPONENTS = ['q\u2081', 'q\u2082', 'q\u2083', 'qr\u2081', 'qr\u2082', 'qr\u2083']

## The TesterTIM6D class class perform an async call to a new process
# that runs opensees and communicate with it in real time. we don't want the gui to freeze,
# so we do this operation in a worker thread
class TesterTIM6D(QObject):
	
	# a signal to notify that we have
	# the new components of strain and stress
	testProcessUpdated = Signal(float, object, object)
	
	# create a new TesterTIM6D passing as arguments 
	# a map (MpcPropertyCollection) of physical properties
	# (or just one if the material does not depend on other materials), the component data,
	# and a list of strains.
	# in case of multiple materials the last one will be tested.
	def __init__(self, type, materials, cdata, time_history, strain_history, parent = None):
		# base class initialization
		super(TesterTIM6D, self).__init__(parent)
		# self initialization
		self.type = type # TIMTraits types (0, 1, 3)
		self.materials = materials
		self.cdata = cdata
		# copy the input strain vector in a private member. why? if the analysis does not finsh
		# correctly, the stress will have less entries than the strain
		self.__timeHistoryInput = time_history
		self.__strainHistoryInput = strain_history
		self.strain = []
		self.stress = []
	
	# prepares data for testing and returns the command to run
	# and the names of temporary files
	def __prepare_test(self):
		
		# some initial checks
		if len(self.materials) == 0:
			raise Exception("No material provided to the tester")
		if len(self.__strainHistoryInput) == 0:
			raise Exception("No strain history provided to the tester")
		
		# make sure we have at least one OpenSEES installed and set to the STKO kits!
		opensees_cmd = PyMpc.App.currentSolverCommand()
		if not opensees_cmd:
			raise Exception("No external solver kit provided")
		
		# temporary directory
		temp_dir = '{}{}TesterTIM6D'.format(MpcStandardPaths.getStandardPathDataLocation(), os.sep)
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
		template_filename = '{}/{}'.format(os.path.dirname(__file__), 'template_TIM6D.tcl')
		template_file = open(template_filename, 'r')
		template = template_file.read()
		template_file.close()
		
		# write materials
		buffer_materials = StringIO()
		pinfo.out_file = buffer_materials
		pinfo.ptype = tclin.process_type.writing_tcl_for_material_tester
		write_physical_properties.write_physical_properties(self.materials, pinfo, 'materials')
		pinfo.out_file = None
		
		# @note: since this is a MpcPropertyCollection (c++ ordered map)
		# the keys are ordered indices, so we test the last one!
		test_prop_id = self.materials.getlastkey(0)
		
		# write the time and strain vectors
		buffer_strain = tu.listToStringBuffer(self.__strainHistoryInput)
		buffer_time = tu.listToStringBuffer(self.__timeHistoryInput)
		
		# build flags for tensor component controls
		buffer_flags1 = StringIO()
		buffer_flags2 = StringIO()
		buffer_imps = StringIO()
		for i in range(TIMTraits.STRAIN_SIZE):
			ic = self.cdata[i]
			buffer_flags1.write('{} '.format(ic.control))
			buffer_flags2.write('{} '.format(ic.type))
			buffer_imps.write('{} '.format(ic.value))
		
		# open the tcl script file
		fo = open(temp_script_file, 'w')
		
		# replace placeholders with actual data
		# and write to file
		fo.write(template.replace(
			'__materials__', buffer_materials.getvalue()).replace(
			'__tag__', str(test_prop_id)).replace( 
			'__time__', buffer_time.getvalue()).replace(
			'__strain__', buffer_strain.getvalue()).replace(
			'__flags1__', buffer_flags1.getvalue()).replace(
			'__flags2__', buffer_flags2.getvalue()).replace(
			'__imps__', buffer_imps.getvalue()).replace(
			'__out__', temp_output_file).replace(
			'__freedofs__', TIMTraits.FREEDOFS[self.type]))
		
		# relase temporary buffers
		buffer_materials.close()
		buffer_strain.close()
		buffer_time.close()
		buffer_flags1.close()
		buffer_flags2.close()
		buffer_imps.close()
		
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
		
		# strain size
		ssize = TIMTraits.STRAIN_SIZE
		
		# launch opensees and communicate
		for item in tu.executeAsync([opensees_cmd, temp_script_file], temp_dir):
			if item.startswith('__R__'):
				# this line contains precentage and strain/stress data
				tokens = item[5:].split('|')
				ipercen = float(tokens[0])
				# get tokens for strain and stress
				tokens_strain = tokens[1].split()
				tokens_stress = tokens[2].split()
				istrain = [float(i) for i in tokens_strain]
				istress = [float(i) for i in tokens_stress]
				self.strain.append(istrain)
				self.stress.append(istress)
				# notify that tester data has been updated: emit signal
				self.testProcessUpdated.emit(ipercen, istrain, istress)
			else:
				print(item)
		
		# remove temporary files
		#os.remove(temp_script_file)
		#os.remove(temp_output_file)

## The TesterTIM6DWidget class is a widget used to run material simulation for uniaxialMaterial models.
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
class TesterTIM6DWidget(QWidget):
	
	## a custom radio button with an int data (0 to 5)
	class IndexedRadioButton(QRadioButton):
		def __init__(self, text, index, parent = None):
			QRadioButton.__init__(self, text, parent)
			self.index = index
	
	## constructor
	def __init__(self, type, editor, xobj, parent = None):
		# base class initialization
		super(TesterTIM6DWidget, self).__init__(parent)
		
		# nD type
		self.type = type
		ssize = TIMTraits.STRAIN_SIZE
		STRAIN_COMPONENTS = TIMTraits.STRAIN_COMPONENTS
		STRESS_COMPONENTS = TIMTraits.STRESS_COMPONENTS
		
		# layout
		self.setLayout(QVBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)
		
		# locale
		locale = QLocale()
		
		# description label
		self.descr_label = gu.makeTesterLabel()
		self.layout().addWidget(self.descr_label)
		
		# separator
		self.separator_1 = gu.makeHSeparator()
		self.layout().addWidget(self.separator_1)
		
		# Strain history
		# strain history container
		self.strain_hist_container = QWidget()
		self.strain_hist_layout = QGridLayout()
		self.strain_hist_layout.setContentsMargins(0,0,0,0)
		self.strain_hist_container.setLayout(self.strain_hist_layout)
		# strain history labels
		self.strain_hist_label_type = QLabel("Type")
		self.strain_hist_label_num_cyc = QLabel("Cycles")
		self.strain_hist_label_div = QLabel("Divisions")
		self.strain_hist_label_target_strain = QLabel("Target deformation")
		self.strain_hist_label_component = QLabel("Tested component")
		self.strain_hist_label_scale_positive = QLabel("Pos scale")
		self.strain_hist_label_scale_negative = QLabel("Neg scale")
		self.strain_hist_layout.addWidget(self.strain_hist_label_type, 0, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_num_cyc, 1, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_div, 2, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_target_strain, 3, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_component, 4, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_scale_positive, 5, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_scale_negative, 6, 0, 1, 1)
		# strain history type combobox
		self.strain_hist_cbox = QComboBox()
		for strain_hist_name in StrainHistoryFactory.getTypes():
			self.strain_hist_cbox.addItem(strain_hist_name)
		self.strain_hist_layout.addWidget(self.strain_hist_cbox, 0, 1, 1, 1)
		# strain history num_cyc spin box
		self.strain_hist_num_cyc_spinbox = QSpinBox()
		self.strain_hist_num_cyc_spinbox.setRange(1, 1000)
		self.strain_hist_layout.addWidget(self.strain_hist_num_cyc_spinbox, 1, 1, 1, 1)
		# strain history divisions spin box
		self.strain_hist_divisions_spinbox = QSpinBox()
		self.strain_hist_divisions_spinbox.setRange(1, 1000000)
		self.strain_hist_layout.addWidget(self.strain_hist_divisions_spinbox, 2, 1, 1, 1)
		# strain history max strain line edit
		self.strain_hist_target_strain = QLineEdit(locale.toString(-0.003))
		self.strain_hist_target_strain.setValidator(QDoubleValidator())
		self.strain_hist_layout.addWidget(self.strain_hist_target_strain, 3, 1, 1, 1)
		# strain history controlled component combobox
		self.strain_hist_component_cbox = QComboBox()
		for item in STRAIN_COMPONENTS:
			self.strain_hist_component_cbox.addItem(item)
		self.strain_hist_layout.addWidget(self.strain_hist_component_cbox, 4, 1, 1, 1)
		# strain history positive scale double spin box
		self.strain_hist_scale_positive_spinbox = QDoubleSpinBox()
		self.strain_hist_scale_positive_spinbox.setRange(-1000, 1000)
		self.strain_hist_scale_positive_spinbox.setDecimals(3)
		self.strain_hist_scale_positive_spinbox.setStepType(QDoubleSpinBox.AdaptiveDecimalStepType)
		self.strain_hist_layout.addWidget(self.strain_hist_scale_positive_spinbox, 5, 1, 1, 1)
		# strain history positive scale double spin box
		self.strain_hist_scale_negative_spinbox = QDoubleSpinBox()
		self.strain_hist_scale_negative_spinbox.setRange(-1000, 1000)
		self.strain_hist_scale_negative_spinbox.setDecimals(3)
		self.strain_hist_scale_negative_spinbox.setStepType(QDoubleSpinBox.AdaptiveDecimalStepType)
		self.strain_hist_layout.addWidget(self.strain_hist_scale_negative_spinbox, 6, 1, 1, 1)
		# strain history chart data
		self.strain_hist_chart_data = gu.makeChartData("Deformation-Time Response", "Pseudo-Time", "Deformation")
		# strain history chart item
		self.strain_hist_chart_item = MpcChartDataGraphicItem(self.strain_hist_chart_data)
		self.strain_hist_chart_item.color = MpcQColor(56,147,255, 255)
		self.strain_hist_chart_item.thickness = 1.5
		self.strain_hist_chart_item.penStyle = MpcQPenStyle.SolidLine
		# strain history chart
		self.strain_hist_chart = MpcChart(1)
		self.strain_hist_chart.addItem(self.strain_hist_chart_item)
		# strain history chart frame
		self.strain_hist_chart_frame = gu.makeChartFrame()
		self.strain_hist_layout.addWidget(self.strain_hist_chart_frame, 0, 2, 6, 2)
		# strain history chart widget
		self.strain_hist_mpc_chart_widget = MpcChartWidget()
		self.strain_hist_mpc_chart_widget.chart = self.strain_hist_chart
		self.strain_hist_mpc_chart_widget.removeLegend()
		self.strain_hist_chart_widget = shiboken2.wrapInstance(self.strain_hist_mpc_chart_widget.getPtr(), QWidget)
		self.strain_hist_chart_frame.layout().addWidget(self.strain_hist_chart_widget)
		# add it to main widget
		self.layout().addWidget(self.strain_hist_container)
		# set up grid strech factors
		self.strain_hist_layout.setColumnStretch(0, 0)
		self.strain_hist_layout.setColumnStretch(1, 0)
		self.strain_hist_layout.setColumnStretch(2, 0)
		self.strain_hist_layout.setColumnStretch(3, 2)
		
		# separator
		self.separator_2 = gu.makeHSeparator()
		self.layout().addWidget(self.separator_2)
		
		# add controls for other components
		self.components_container = QWidget()
		self.components_layout = QGridLayout()
		self.components_container.setLayout(self.components_layout)
		self.components_layout.setContentsMargins(0,0,0,0)
		self.components_descr_1 = QLabel("Type")
		self.components_descr_2 = QLabel("Reference value")
		self.components_layout.addWidget(self.components_descr_1, 0, 0, 1, 1)
		self.components_layout.addWidget(self.components_descr_2, 1, 0, 1, 1)
		self.components_strain = []
		self.components_stress = []
		self.components_groups = []
		self.components_values = []
		self.components_test = []
		for i in range(ssize):
			ice = TesterTIM6DWidget.IndexedRadioButton(STRAIN_COMPONENTS[i], i)
			ics = TesterTIM6DWidget.IndexedRadioButton(STRESS_COMPONENTS[i], i)
			ics.setChecked(True)
			icv = QLineEdit()
			icv.setValidator(QDoubleValidator())
			icv.setText(locale.toString(0.0))
			icg = QWidget()
			icg.setLayout(QVBoxLayout())
			icg.layout().setContentsMargins(0,0,0,0)
			icg.layout().addWidget(ice)
			icg.layout().addWidget(ics)
			ict = QLabel("(Tested)")
			self.components_strain.append(ice)
			self.components_stress.append(ics)
			self.components_groups.append(icg)
			self.components_values.append(icv)
			self.components_test.append(ict)
			self.components_layout.addWidget(icg, 0, i+1, 1, 1)
			self.components_layout.addWidget(icv, 1, i+1, 1, 1)
			self.components_layout.addWidget(ict, 2, i+1, 1, 1)
		self.layout().addWidget(self.components_container)
		
		# separator
		self.separator_3 = gu.makeHSeparator()
		self.layout().addWidget(self.separator_3)
		
		# stress-strain chart data (1 for each component)
		self.chart_tab_widget = QTabWidget()
		self.layout().addWidget(self.chart_tab_widget)
		self.chart_data = []
		self.chart_item = []
		self.chart = []
		self.chart_frame = []
		self.mpc_chart_widget = []
		self.chart_widget = []
		for i in range(ssize):
			# labels
			c_strain = STRAIN_COMPONENTS[i]
			c_stress = STRESS_COMPONENTS[i]
			# chart data
			chart_data = gu.makeChartData("{}-{} Response".format(c_strain, c_stress), c_strain, c_stress)
			self.chart_data.append(chart_data)
			# stress-strain chart item
			chart_item = MpcChartDataGraphicItem(chart_data)
			chart_item.color = MpcQColor(56,147,255, 255)
			chart_item.thickness = 1.5
			chart_item.penStyle = MpcQPenStyle.SolidLine
			self.chart_item.append(self.chart_item)
			# stress-strain chart
			chart = MpcChart(1)
			chart.addItem(chart_item)
			self.chart.append(chart)
			# stress-strain frame
			chart_frame = gu.makeChartFrame()
			self.chart_frame.append(chart_frame)
			# stress-strain chart widget
			mpc_chart_widget = MpcChartWidget()
			mpc_chart_widget.chart = chart
			mpc_chart_widget.removeLegend()
			self.mpc_chart_widget.append(mpc_chart_widget)
			chart_widget = shiboken2.wrapInstance(mpc_chart_widget.getPtr(), QWidget)
			self.chart_widget.append(chart_widget)
			chart_frame.layout().addWidget(chart_widget)
			# add tab
			self.chart_tab_widget.addTab(chart_frame, "{}-{}".format(c_strain, c_stress))
		
		# Run session
		# run container
		self.run_container = QWidget()
		self.layout().addWidget(self.run_container)
		# run layout
		self.run_layout = QGridLayout()
		self.run_layout.setContentsMargins(0,0,0,0)
		self.run_container.setLayout(self.run_layout)
		# run button
		self.run_button = QPushButton('Test')
		self.run_layout.addWidget(self.run_button, 0, 0, 1, 1)
		# data button
		self.data_button = QPushButton('Data...')
		self.run_layout.addWidget(self.data_button, 0, 1, 1, 1)
		# run progress bar
		self.run_progress_bar = gu.makeProgressBar()
		self.run_layout.addWidget(self.run_progress_bar, 0, 2, 1, 3)
		
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
		
		# call onStrainHistoryTypeChanged here because connections are not set yet!
		# this function will also set members for strain history
		self.onStrainHistoryTypeChanged()
		
		# same for onComponentsUpdated
		self.onComponentsUpdated()
		
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
			jds = jds['TesterTIM6D']
			class_name = jds['name']
			self.strain_hist_cbox.setCurrentText(class_name)
			# call this to set up default values (no connections here)
			self.onStrainHistoryTypeChanged()
			num_cycles = jds.get('num_cycl',self.strain_hist_num_cyc_spinbox.value())
			self.strain_hist_num_cyc_spinbox.setValue(num_cycles)
			num_divisions = jds.get('num_div',self.strain_hist_divisions_spinbox.value())
			self.strain_hist_divisions_spinbox.setValue(num_divisions)
			target_strain = jds.get('target_strain', QLocale().toDouble(self.strain_hist_target_strain.text())[0])
			self.strain_hist_target_strain.setText(QLocale().toString(target_strain))
			tested_comp = jds.get('tested_comp', 0) 
			self.strain_hist_component_cbox.setCurrentIndex(tested_comp)
			scale_pos = jds.get('scale_positive',self.strain_hist_scale_positive_spinbox.value())
			self.strain_hist_scale_positive_spinbox.setValue(scale_pos)
			scale_neg = jds.get('scale_negative',self.strain_hist_scale_negative_spinbox.value())
			self.strain_hist_scale_negative_spinbox.setValue(scale_neg)
			ctypes = jds.get('components_types',None)
			if ctypes:
				for i, istrain, istress in zip(ctypes, self.components_strain, self.components_stress):
					istrain.setChecked(i)
					istress.setChecked(not i)
			cvalues = jds.get('components_values',None)
			if cvalues:
				for i, ivalue in zip(cvalues, self.components_values):
					ivalue.setText(locale.toString(i))
			# call this to set up strain history with restored values (no connections here)
			self.onStrainHistoryParamChanged()
			self.onComponentsUpdated()
		except:
			# if impossible to load, load default values
			pass
		#################################################### $JSON
		
		# set up connections
		self.strain_hist_cbox.currentIndexChanged.connect(self.onStrainHistoryTypeChanged)
		self.strain_hist_num_cyc_spinbox.valueChanged.connect(self.onStrainHistoryParamChanged)
		self.strain_hist_divisions_spinbox.valueChanged.connect(self.onStrainHistoryParamChanged)
		self.strain_hist_target_strain.textEdited.connect(self.onStrainHistoryParamChanged)
		self.strain_hist_scale_positive_spinbox.valueChanged.connect(self.onStrainHistoryParamChanged)
		self.strain_hist_scale_negative_spinbox.valueChanged.connect(self.onStrainHistoryParamChanged)
		self.run_button.clicked.connect(self.onTestClicked)
		self.data_button.clicked.connect(self.onDataClicked)
		self.strain_hist_component_cbox.currentIndexChanged.connect(self.onComponentsUpdated)
	
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
		locale = QLocale()
		class_name = self.strain_hist_cbox.currentText()
		num_cycles = self.strain_hist_num_cyc_spinbox.value()
		num_divisions = self.strain_hist_divisions_spinbox.value()
		target_strain = locale.toDouble(self.strain_hist_target_strain.text())[0]
		tested_comp = self.strain_hist_component_cbox.currentIndex()
		scale_pos = self.strain_hist_scale_positive_spinbox.value()
		scale_neg = self.strain_hist_scale_negative_spinbox.value()
		ctypes = [ i.isChecked() for i in self.components_strain ]
		cvalues = [ locale.toDouble(i.text())[0] for i in self.components_values ]
		jds['TesterTIM6D'] = {
			'name': class_name,
			'num_cycl': num_cycles,
			'num_div': num_divisions,
			'target_strain': target_strain,
			'tested_comp': tested_comp,
			'scale_positive': scale_pos,
			'scale_negative': scale_neg,
			'components_types': ctypes,
			'components_values': cvalues,
			}
		a.string = json.dumps(jds, indent=4)
		#################################################### $JSON
	
	def onComponentsUpdated(self):
		# the tested component id
		tested_id = self.strain_hist_component_cbox.currentIndex()
		# switch tested labels on/off
		for i in range(TIMTraits.STRAIN_SIZE):
			if i == tested_id:
				self.components_test[i].setVisible(True)
				self.components_groups[i].setEnabled(False)
				self.components_values[i].setEnabled(False)
				self.components_strain[i].setChecked(True)
			else:
				self.components_test[i].setVisible(False)
				self.components_groups[i].setEnabled(True)
				self.components_values[i].setEnabled(True)
	
	def onStrainHistoryTypeChanged(self):
		# obtain self.strain_hist default self.strain_hist_params 
		# from new type
		class_name = self.strain_hist_cbox.currentText()
		self.strain_hist = StrainHistoryFactory.make(class_name)
		self.strain_hist_params = self.strain_hist.getDefaultParams()
		# send them to the ui (block signals first!)
		locks = [
			QSignalBlocker(self.strain_hist_num_cyc_spinbox),
			QSignalBlocker(self.strain_hist_divisions_spinbox),
			QSignalBlocker(self.strain_hist_scale_positive_spinbox),
			QSignalBlocker(self.strain_hist_scale_negative_spinbox),
			]
		self.strain_hist_num_cyc_spinbox.setValue(self.strain_hist_params.num_cycles)
		self.strain_hist_divisions_spinbox.setValue(self.strain_hist_params.num_divisions)
		self.strain_hist_num_cyc_spinbox.setEnabled(self.strain_hist_params.num_cycles_editable)
		self.strain_hist_scale_positive_spinbox.setValue(self.strain_hist_params.scale_pos)
		self.strain_hist_scale_negative_spinbox.setValue(self.strain_hist_params.scale_neg)
		# manually call the param changed slot
		# to update the plot
		self.onStrainHistoryParamChanged()
	
	def onStrainHistoryParamChanged(self):
		# update self.strain_hist_params
		self.strain_hist_params.num_cycles = self.strain_hist_num_cyc_spinbox.value()
		self.strain_hist_params.num_divisions = self.strain_hist_divisions_spinbox.value()
		# get ultimate strain
		self.strain_hist_params.target_strain = QLocale().toDouble(self.strain_hist_target_strain.text())[0]
		# get scale factors
		self.strain_hist_params.scale_pos = self.strain_hist_scale_positive_spinbox.value()
		self.strain_hist_params.scale_neg = self.strain_hist_scale_negative_spinbox.value()
		# update chart data
		try:
			self.strain_hist.build(self.strain_hist_params)
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
			self.strain_hist.strain = [0.0, 0.0]
		
		# make the total analysis last 1 (pseudo) seconds.
		# this is not mandatory now, but for future works it can be useful for rate dependent models
		dtime = 0.0
		self.strain_hist_time = [0.0]*len(self.strain_hist.strain)
		if len(self.strain_hist.strain) > 1:
			dtime = 1.0/float(len(self.strain_hist.strain) - 1)
		for i in range(len(self.strain_hist.strain)):
			self.strain_hist_time[i] = float(i)*dtime
		# update strain history chart data
		self.strain_hist_chart_data.y = PyMpc.Math.double_array(self.strain_hist.strain)
		self.strain_hist_chart_data.x = PyMpc.Math.double_array(self.strain_hist_time)
		# set chart
		self.strain_hist_mpc_chart_widget.chart = self.strain_hist_chart
		self.strain_hist_mpc_chart_widget.autoScale()
	
	@Slot(float, float, float)
	def onTestProcessUpdated(self, iperc, istrain, istress):
		# strain size
		ssize = TIMTraits.STRAIN_SIZE
		# update strain/stress data
		for i in range(ssize):
			self.chart_data[i].x.append(istrain[i])
			self.chart_data[i].y.append(istress[i])
		# update gui:
		# note: this is visual appealing and capture the user attention while
		# a job is beeing done. howver it slows down the job execution, so
		# we update the gui only at certain points
		self.delta_percentage += iperc - self.old_percentage
		self.old_percentage = iperc
		if self.delta_percentage > 0.0099 or iperc > 0.9999:
			self.delta_percentage = 0.0
			# update chart
			for i in range(ssize):
				self.mpc_chart_widget[i].chart = self.chart[i]
				self.mpc_chart_widget[i].autoScale()
			# update progress bar
			self.run_progress_bar.setValue(int(round(iperc*100.0)))
			# process all events to prevent gui from freezing
			QCoreApplication.processEvents()
	
	def onTestClicked(self):
		
		# strain size
		ssize = TIMTraits.STRAIN_SIZE
		
		# reset chart data
		for i in range(ssize):
			self.chart_data[i].x = PyMpc.Math.double_array()
			self.chart_data[i].y = PyMpc.Math.double_array()
		
		# reset percentage data
		self.old_percentage = 0.0
		self.delta_percentage = 0.0
		
		# check
		if abs(self.strain_hist_params.target_strain) < 1.0e-18:
			return
		
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
			materials[parent_component.id] = parent_component
			
			# build component controls
			locale = QLocale()
			cdata = []
			for i in range(ssize):
				tdata = tu.TensorComponentData()
				if not self.components_strain[i].isChecked():
					tdata.control = tu.TensorComponentData.STRESS #default = STRAIN
				if i == self.strain_hist_component_cbox.currentIndex():
					tdata.type = tu.TensorComponentData.TESTED #default = FIXED
				tdata.value = locale.toDouble(self.components_values[i].text())[0]
				cdata.append(tdata)
			
			# now we can run the tester
			self.tester = TesterTIM6D(self.type, materials, cdata, self.strain_hist_time, self.strain_hist.strain)
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
	
	def onDataClicked(self):
		try:
			ssize = TIMTraits.STRAIN_SIZE
			n = len(self.chart_data[0].x)
			dialog = QDialog()
			dialog.setLayout(QVBoxLayout())
			table = gu.TableWidget()
			table.setItemDelegate(gu.DoubleItemDelegate(table))
			table.setColumnCount(2*ssize)
			labels = []
			for i in range(ssize):
				labels.append(self.chart_data[i].xLabel)
				labels.append(self.chart_data[i].yLabel)
			table.setHorizontalHeaderLabels(labels)
			table.setRowCount(n)
			def make_item(value):
				iy = QTableWidgetItem()
				iy.setData(Qt.DisplayRole, value)
				return iy
			for i in range(n):
				for j in range(ssize):
					cdata = self.chart_data[j]
					table.setItem(i, j*2, make_item(cdata.x[i]))
					table.setItem(i, j*2+1, make_item(cdata.y[i]))
			dialog.layout().addWidget(table)
			dialog.exec_()
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))