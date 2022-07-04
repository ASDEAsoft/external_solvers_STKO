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
import opensees.utils.write_physical_properties as write_physical_properties
import opensees.utils.Gui.GuiUtils as gu
import opensees.physical_properties.utils.tester.TesterUtils as tu
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
	QToolBar,
	QDialog,
	QFileDialog,
	QMessageBox,
	QSizePolicy,
	QTableWidget,
	QTableWidgetItem
	)
import shiboken2

## The Tester1D class class perform an async call to a new process
# that runs opensees and communicate with it in real time. we don't want the gui to freeze,
# so we do this operation in a worker thread
class Tester1D(QObject):
	
	# a signal to notify that we have
	# the new components of strain and stress
	testProcessUpdated = Signal(float, float, float)
	
	# create a new Tester1D passing as arguments 
	# a map (MpcPropertyCollection) of physical properties
	# (or just one if the material does not depend on other materials)
	# and a list of strains.
	# in case of multiple materials the last one will be tested.
	def __init__(self, materials, time_history, strain_history, parent = None):
		# base class initialization
		super(Tester1D, self).__init__(parent)
		# self initialization
		self.materials = materials
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
		temp_dir = '{}{}Tester1D'.format(MpcStandardPaths.getStandardPathDataLocation(), os.sep)
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
		template_filename = '{}/template_1d.tcl'.format(os.path.dirname(__file__))
		template_file = open(template_filename, 'r')
		template = template_file.read()
		template_file.close()
		
		# write materials
		buffer_materials = StringIO()
		pinfo.out_file = buffer_materials
		write_physical_properties.write_physical_properties(self.materials, pinfo, 'materials')
		pinfo.out_file = None
		
		# @note: since this is a MpcPropertyCollection (c++ ordered map)
		# the keys are ordered indices, so we test the last one!
		test_prop_id = self.materials.getlastkey(0)
		
		# write the time and strain vectors
		buffer_strain = tu.listToStringBuffer(self.__strainHistoryInput)
		buffer_time = tu.listToStringBuffer(self.__timeHistoryInput)
		
		# open the tcl script file
		fo = open(temp_script_file, 'w')
		
		# replace placeholders with actual data
		# and write to file
		fo.write(template.replace(
			'__materials__', buffer_materials.getvalue()).replace(
			'__tag__', str(test_prop_id)).replace(
			'__time__', buffer_time.getvalue()).replace(
			'__strain__', buffer_strain.getvalue()).replace(
			'__out__', temp_output_file))
		
		# relase temporary buffers
		buffer_materials.close()
		buffer_strain.close()
		buffer_time.close()
		
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
				# this line contains precentage and strain/stress data
				tokens = item[5:].split()
				ipercen = float(tokens[0])
				istrain = float(tokens[1])
				istress = float(tokens[2])
				self.strain.append(istrain)
				self.stress.append(istress)
				# notify that tester data has been updated: emit signal
				self.testProcessUpdated.emit(ipercen, istrain, istress)
			else:
				print(item)
		
		# remove temporary files
		os.remove(temp_script_file)
		os.remove(temp_output_file)
		
## The Tester1D class class perform an async call to a new process
# that runs opensees and communicate with it in real time. we don't want the gui to freeze,
# so we do this operation in a worker thread
class Tester1DMaterialConfinedSection(QObject):
	
	# a signal to notify that we have
	# the new components of strain and stress
	testProcessUpdated = Signal(float, float, float)
	
	# create a new Tester1DMaterialConfinedSection passing as arguments 
	# a map (MpcPropertyCollection) of physical properties
	# (or just one if the material does not depend on other materials)
	# and a list of strains.
	# in case of multiple materials the last one will be tested.
	def __init__(self, materialTclString, time_history, strain_history, parent = None):
		# base class initialization
		super(Tester1DMaterialConfinedSection, self).__init__(parent)
		# self initialization
		self.materialTclString = materialTclString
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
		if self.materialTclString is None:
			raise Exception("No material provided to the tester")
		if len(self.__strainHistoryInput) == 0:
			raise Exception("No strain history provided to the tester")
		
		# make sure we have at least one OpenSEES installed and set to the STKO kits!
		opensees_cmd = PyMpc.App.currentSolverCommand()
		if not opensees_cmd:
			raise Exception("No external solver kit provided")
		
		# temporary directory
		temp_dir = '{}{}Tester1D'.format(MpcStandardPaths.getStandardPathDataLocation(), os.sep)
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
		template_filename = '{}/template_1d.tcl'.format(os.path.dirname(__file__))
		template_file = open(template_filename, 'r')
		template = template_file.read()
		template_file.close()
		
		from io import StringIO
		
		# write the time and strain vectors
		buffer_strain = tu.listToStringBuffer(self.__strainHistoryInput)
		buffer_time = tu.listToStringBuffer(self.__timeHistoryInput)
		
		# open the tcl script file
		fo = open(temp_script_file, 'w')
		
		# replace placeholders with actual data
		# and write to file
		fo.write(template.replace(
			'__materials__', self.materialTclString).replace(
			'__tag__', str(1)).replace(
			'__time__', buffer_time.getvalue()).replace(
			'__strain__', buffer_strain.getvalue()).replace(
			'__out__', temp_output_file))
		
		# release temporary buffers
		buffer_strain.close()
		buffer_time.close()
		
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
				istrain = float(tokens[1])
				istress = float(tokens[2])
				self.strain.append(istrain)
				self.stress.append(istress)
				# notify that tester data has been updated: emit signal
				self.testProcessUpdated.emit(ipercen, istrain, istress)
		
		# remove temporary files
		os.remove(temp_script_file)
		os.remove(temp_output_file)


## The Tester1DWidget class is a widget used to run material simulation for uniaxialMaterial models.
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
class Tester1DWidget(QWidget):
	
	## constructor
	def __init__(self, editor, xobj, parent = None):
		# base class initialization
		super(Tester1DWidget, self).__init__(parent)
		# layout
		self.setLayout(QVBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)
		
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
		self.strain_hist_label_target_strain = QLabel("Target strain")
		self.strain_hist_label_scale_positive = QLabel("Pos scale")
		self.strain_hist_label_scale_negative = QLabel("Neg scale")
		self.strain_hist_layout.addWidget(self.strain_hist_label_type, 0, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_num_cyc, 1, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_div, 2, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_target_strain, 3, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_scale_positive, 4, 0, 1, 1)
		self.strain_hist_layout.addWidget(self.strain_hist_label_scale_negative, 5, 0, 1, 1)
		# strain history type combobox
		self.strain_hist_cbox = QComboBox()
		for strain_hist_name in StrainHistoryFactory.getTypes():
			self.strain_hist_cbox.addItem(strain_hist_name)
		self.strain_hist_layout.addWidget(self.strain_hist_cbox, 0, 1, 1, 1)
		# and its editor button for custom histories
		self.custom_hist_button = QPushButton()
		self.custom_hist_button.setText("...")
		self.custom_hist_button.setToolTip("Click to edit the custom strain history")
		self.custom_hist_button.setMaximumWidth(24)
		self.strain_hist_layout.addWidget(self.custom_hist_button, 0, 2, 1, 1)
		self.custom_hist_vector = MpcQuantityVector()
		# strain history num_cyc spin box
		self.strain_hist_num_cyc_spinbox = QSpinBox()
		self.strain_hist_num_cyc_spinbox.setRange(1, 1000)
		self.strain_hist_layout.addWidget(self.strain_hist_num_cyc_spinbox, 1, 1, 1, 1)
		# strain history divisions spin box
		self.strain_hist_divisions_spinbox = QSpinBox()
		self.strain_hist_divisions_spinbox.setRange(1, 1000000)
		self.strain_hist_layout.addWidget(self.strain_hist_divisions_spinbox, 2, 1, 1, 1)
		# strain history max strain line edit
		self.strain_hist_target_strain = QLineEdit(QLocale().toString(-0.003))
		self.strain_hist_target_strain.setValidator(QDoubleValidator())
		self.strain_hist_layout.addWidget(self.strain_hist_target_strain, 3, 1, 1, 1)
		# strain history positive scale double spin box
		self.strain_hist_scale_positive_spinbox = QDoubleSpinBox()
		self.strain_hist_scale_positive_spinbox.setRange(-1000, 1000)
		self.strain_hist_scale_positive_spinbox.setDecimals(3)
		self.strain_hist_scale_positive_spinbox.setStepType(QDoubleSpinBox.AdaptiveDecimalStepType)
		self.strain_hist_layout.addWidget(self.strain_hist_scale_positive_spinbox, 4, 1, 1, 1)
		# strain history positive scale double spin box
		self.strain_hist_scale_negative_spinbox = QDoubleSpinBox()
		self.strain_hist_scale_negative_spinbox.setRange(-1000, 1000)
		self.strain_hist_scale_negative_spinbox.setDecimals(3)
		self.strain_hist_scale_negative_spinbox.setStepType(QDoubleSpinBox.AdaptiveDecimalStepType)
		self.strain_hist_layout.addWidget(self.strain_hist_scale_negative_spinbox, 5, 1, 1, 1)
		# strain history chart data
		self.strain_hist_chart_data = gu.makeChartData("Strain-Time Response", "Pseudo-Time", "Strain")
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
		self.strain_hist_layout.addWidget(self.strain_hist_chart_frame, 0, 2, 6, 1)
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
		self.strain_hist_layout.setColumnStretch(2, 2)
		
		# separator
		self.separator_2 = gu.makeHSeparator()
		self.layout().addWidget(self.separator_2)
		
		# Test toolbar
		self.toolbar = QToolBar()
		self.toolbar.addAction("Load",self.loadReferenceData)
		self.toolbar.addAction("Unload",self.unloadReferenceData)
		self.toolbar.addAction("Genetic", self.geneticCalibrationPressed)
		self.layout().addWidget(self.toolbar)
		# stress-strain chart data
		self.chart_data = gu.makeChartData("Stress-Strain Response", "Strain", "Stress")
		self.chart_reference_data = gu.makeChartData("Reference Curve", "Strain", "Stress", 2)
		# stress-strain chart item
		self.chart_item = MpcChartDataGraphicItem(self.chart_data)
		self.chart_item.color = MpcQColor(56,147,255, 255)
		self.chart_item.thickness = 1.5
		self.chart_item.penStyle = MpcQPenStyle.SolidLine
		# stress-strain reference chart item
		self.chart_reference_item = MpcChartDataGraphicItem(self.chart_reference_data)
		self.chart_reference_item.color = MpcQColor(190,190,255, 255)
		self.chart_reference_item.thickness = 1.5
		self.chart_reference_item.penStyle = MpcQPenStyle.SolidLine
		# reference stress and strain vectors
		self.reference_strain = MpcQuantityVector()
		self.reference_stress = MpcQuantityVector()
		
		# stress-strain chart
		self.chart = MpcChart(1)
		self.chart.addItem(self.chart_item)
		self.chart.addItem(self.chart_reference_item)
		# stress-strain frame
		self.chart_frame = gu.makeChartFrame()
		self.layout().addWidget(self.chart_frame)
		# stress-strain chart widget
		self.mpc_chart_widget = MpcChartWidget()
		self.mpc_chart_widget.chart = self.chart
		self.mpc_chart_widget.removeLegend()
		self.chart_widget = shiboken2.wrapInstance(self.mpc_chart_widget.getPtr(), QWidget)
		self.chart_frame.layout().addWidget(self.chart_widget)
		
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
			jds = jds['Tester1D']
			# Load data if present
			reference_strain = jds.get('reference_strain',[])
			reference_strain_vec = PyMpc.Math.vec(len(reference_strain))
			for i in range(len(reference_strain)):
				reference_strain_vec[i] = reference_strain[i]
			self.reference_strain.referenceValue = reference_strain_vec
			
			reference_stress = jds.get('reference_stress',[])
			reference_stress_vec = PyMpc.Math.vec(len(reference_stress))
			for i in range(len(reference_stress)):
				reference_stress_vec[i] = reference_stress[i]
			self.reference_stress.referenceValue = reference_stress_vec
			
			# update the chart if data is loaded
			self.updateReferenceCurve()
			
			class_name = jds['name']
			self.strain_hist_cbox.setCurrentText(class_name)
			# call this to set up default values (no connections here)
			self.onStrainHistoryTypeChanged()
			num_cycles = jds.get('num_cycl',self.strain_hist_num_cyc_spinbox.value())
			self.strain_hist_num_cyc_spinbox.setValue(num_cycles)
			num_divisions = jds.get('num_div',self.strain_hist_divisions_spinbox.value())
			self.strain_hist_divisions_spinbox.setValue(num_divisions)
			scale_pos = jds.get('scale_positive',self.strain_hist_scale_positive_spinbox.value())
			self.strain_hist_scale_positive_spinbox.setValue(scale_pos)
			scale_neg = jds.get('scale_negative',self.strain_hist_scale_negative_spinbox.value())
			self.strain_hist_scale_negative_spinbox.setValue(scale_neg)
			
			target_strain = jds.get('target_strain', QLocale().toDouble(self.strain_hist_target_strain.text())[0])
			self.strain_hist_target_strain.setText(QLocale().toString(target_strain))
			
			custom_vector = jds.get('custom_vector',[])
			custom_vector_vec = PyMpc.Math.vec(len(custom_vector))
			for i in range(len(custom_vector)):
				custom_vector_vec[i] = custom_vector[i]
			self.custom_hist_vector.referenceValue = custom_vector_vec
			
			# call this to set up strain history with restored values (no connections here)
			self.onStrainHistoryParamChanged()
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
		self.custom_hist_button.clicked.connect(self.onCustomHistClicked)
		
	def updateReferenceCurve(self):
		# Read the data and save the list
		# Read data and fill the lists
		eps = []
		for i in range(len(self.reference_strain)):
			eps.append(self.reference_strain.referenceValueAt(i))
		sig = []
		for i in range(len(self.reference_stress)):
			sig.append(self.reference_stress.referenceValueAt(i))
		# Save the chart data
		self.chart_reference_data.y = PyMpc.Math.double_array(sig)
		self.chart_reference_data.x = PyMpc.Math.double_array(eps)
		# update chart
		self.mpc_chart_widget.chart = self.chart
		self.mpc_chart_widget.autoScale()
		
	def loadReferenceData(self):
		try:
			# choose file
			# the active / last used directory is accessible with ???
			dialog = QFileDialog(self)
			dialog.setFileMode(QFileDialog.AnyFile)
			dialog.setViewMode(QFileDialog.Detail)
			if dialog.exec():
				fileName = dialog.selectedFiles()
				print(fileName)
				# Load the data
				try:
					fileObj = open(fileName[0], 'r')
				except (OSError, IOError):
					PyMpc.IO.write_cerr('File "{}" not found \n'.format(fileName))
				else:
					# Read data and fill the lists
					eps, sig = [], []
					for line in fileObj:
						values = [float(s) for s in line.split()]
						eps.append(values[0])
						sig.append(values[1])
					fileObj.close()
					# Save strain and stress in reference vectors for future access
					ref_strain_vec = PyMpc.Math.vec(len(eps))
					for i in range(len(eps)):
						ref_strain_vec[i] = eps[i]
					self.reference_strain.referenceValue = ref_strain_vec
					ref_stress_vec = PyMpc.Math.vec(len(sig))
					for i in range(len(eps)):
						ref_stress_vec[i] = sig[i]
					self.reference_stress.referenceValue = ref_stress_vec
					
					# update the chart
					self.updateReferenceCurve()
					
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
		
	def unloadReferenceData(self):
		# Erase the vectors for reference strain and stress
		self.reference_strain.resize(0,1)
		self.reference_stress.resize(0,1)
		# Erse the data
		self.chart_reference_data.y = PyMpc.Math.double_array([])
		self.chart_reference_data.x = PyMpc.Math.double_array([])
		# update chart
		self.mpc_chart_widget.chart = self.chart
		self.mpc_chart_widget.autoScale()
		
	def geneticCalibrationPressed(self):
		print('Pressed the button to automatically calibrate with genetic algorithm')
	
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
		class_name = self.strain_hist_cbox.currentText()
		num_cycles = self.strain_hist_num_cyc_spinbox.value()
		num_divisions = self.strain_hist_divisions_spinbox.value()
		target_strain = QLocale().toDouble(self.strain_hist_target_strain.text())[0]
		scale_pos = self.strain_hist_scale_positive_spinbox.value()
		scale_neg = self.strain_hist_scale_negative_spinbox.value()
		custom_vector = []
		for i in range(len(self.custom_hist_vector)):
			custom_vector.append(self.custom_hist_vector.referenceValueAt(i))
		reference_strain = []
		for i in range(len(self.reference_strain)):
			reference_strain.append(self.reference_strain.referenceValueAt(i))
		reference_stress = []
		for i in range(len(self.reference_stress)):
			reference_stress.append(self.reference_stress.referenceValueAt(i))
			
		jds['Tester1D'] = {
			'name': class_name, 
			'num_cycl': num_cycles, 
			'num_div': num_divisions, 
			'target_strain': target_strain, 
			'scale_positive': scale_pos, 
			'scale_negative': scale_neg, 
			'custom_vector': custom_vector, 
			'reference_strain': reference_strain, 
			'reference_stress': reference_stress 
			}
		a.string = json.dumps(jds, indent=4)
		
		#################################################### $JSON
	
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
		# show/hide custom hist button
		self.custom_hist_button.setVisible(class_name == "Custom")
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
		# get the custom_vector
		self.strain_hist_params.custom_history_vector = self.custom_hist_vector
		if self.strain_hist_cbox.currentText() == "ReferenceCurveHistory":
			# DIEGO: da spostare?
			if len(self.reference_strain) == 0:
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setText("Error reference strain history")
				msg.setInformativeText("No reference stress-strain curve was provided")
				msg.setWindowTitle("Reference strain history")
				msg.setDetailedText("Please provide stress-strain curve or change strain history\nSetting default strain history")
				msg.setStandardButtons(QMessageBox.Ok)
				# retval = msg.exec_()
				msg.exec_()
				# PER MASSIMO: PER DIEGO
				# L'eccezione meglio non lanciarla perche si trova in uno slot che viene chiamato
				# nell'event loop della gui... in questi casi (errori dell'utente) meglio gestirli con messaggi di errore
				# e fallback su valori di default.
				# raise Exception("Please provide a reference curve or change strain history") 
				if self.strain_hist_cbox.count() > 0:
					print('Setting a default strain history')
					# qui ci vuole un signal blocker, altrimenti cambiare il valore corrente della combobox
					# lancia il segnale che richiama onStrainHistoryTypeChanged, che richiama questo metodo
					# in un loop infinito fino ad andare in stack overflow
					blocker = QSignalBlocker(self.strain_hist_cbox)
					self.strain_hist_cbox.setCurrentText("CyclicAsymmetric") # qui ho cambiato in setCurrentText 
					print('Setted Cyclic Asymmetric')
					# Ora lo puoi chiamare tranquillamente. Crashava perche per sbaglio avevi scritto
					# strain_hist_cbox.currentText("qualcosa") invece di strain_hist_cbox.setCurrentText("qualcosa")
					# per cui lui non cambiava mai il testo corrente e tornava sempre in questo metodo nell'if alla rigas 599!!
					self.onStrainHistoryTypeChanged() # Questo CRASHA - immagino vadano bloccate le call?
			self.strain_hist_params.custom_history_vector = self.reference_strain
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
		
	def onCustomHistClicked(self):
		MpcEditQuantityVectorEditorDialog(self.custom_hist_vector, self.editor)
		
		self.onStrainHistoryParamChanged()
	
	@Slot(float, float, float)
	def onTestProcessUpdated(self, iperc, istrain, istress):
		# update strain/stress data
		self.chart_data.x.append(istrain)
		self.chart_data.y.append(istress)
		# update gui:
		# note: this is visual appealing and capture the user attention while
		# a job is beeing done. howver it slows down the job execution, so
		# we update the gui only at certain points
		self.delta_percentage += iperc - self.old_percentage
		self.old_percentage = iperc
		if self.delta_percentage > 0.0099 or iperc > 0.9999:
			self.delta_percentage = 0.0
			# update chart
			self.mpc_chart_widget.chart = self.chart
			self.mpc_chart_widget.autoScale()
			# update progress bar
			self.run_progress_bar.setValue(int(round(iperc*100.0)))
			# process all events to prevent gui from freezing
			QCoreApplication.processEvents()
	
	def onTestClicked(self):
		
		# reset chart data
		self.chart_data.x = PyMpc.Math.double_array()
		self.chart_data.y = PyMpc.Math.double_array()
		
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
			
			# now we can run the tester
			self.tester = Tester1D(materials, self.strain_hist_time, self.strain_hist.strain)
			self.tester.testProcessUpdated.connect(self.onTestProcessUpdated)
			parent_dialog = shiboken2.wrapInstance(self.editor.getParentWindowPtr(), QWidget)
			parent_dialog.setEnabled(False)
			self.editor.setCanClose(False)
			self.data_button.setEnabled(False)
			try:
				self.tester.run()
			finally:
				parent_dialog.setEnabled(True)
				self.data_button.setEnabled(True)
				self.editor.setCanClose(True)
				self.tester.deleteLater()
				self.tester = None
			
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
	
	def onDataClicked(self):
		try:
			n = len(self.chart_data.x)
			dialog = QDialog()
			dialog.setLayout(QVBoxLayout())
			table = gu.TableWidget()
			table.setItemDelegate(gu.DoubleItemDelegate(table))
			table.setColumnCount(2)
			table.setHorizontalHeaderLabels([self.chart_data.xLabel, self.chart_data.yLabel])
			table.setRowCount(n)
			def make_item(value):
				iy = QTableWidgetItem()
				iy.setData(Qt.DisplayRole, value)
				return iy
			for i in range(n):
				table.setItem(i, 0, make_item(self.chart_data.x[i]))
				table.setItem(i, 1, make_item(self.chart_data.y[i]))
			dialog.layout().addWidget(table)
			dialog.exec_()
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))