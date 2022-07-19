"""@package mpc_initialize
This module contains functions for the correct initialization of PyMpc.

More details here.
"""

import os
import PyMpc.Utils
import importlib

# import opensees.physical_properties.sections.RectangulaFiberSection_support_data.ThreadUtils as tu
from PySide2.QtCore import Qt, QObject, Signal, Slot, QThread, QEventLoop, QTimer
from PySide2.QtWidgets import QMessageBox, QApplication, QDialog, QLabel, QProgressBar, QVBoxLayout, QTextEdit
'''
A simple QObject that wraps a user-defined function,
and calls this function waiting for it to finish
'''
class QBlockingSlot(QObject):
	requestCall = Signal()
	done = Signal()
	def __init__(self, function, parent = None):
		super(QBlockingSlot, self).__init__(parent)
		self.requestCall.connect(self.run)
		self.function = function
	def run(self):
		self.function()
		self.done.emit()
	def call(self):
		loop = QEventLoop()
		self.done.connect(loop.quit)
		self.requestCall.emit()
		loop.exec_()

'''
Utility to run a function with a QBlockingSlot on the GUI thread
'''
def runOnMainThread(function):
	bslot = QBlockingSlot(function)
	bslot.moveToThread(QApplication.instance().thread())
	bslot.call()

'''
A simple worker dialog, with a progres bar to track
the percentage of an operation
'''
class WorkerDialog(QDialog):
	def __init__(self, parent = None):
		# call base class constructor
		super(WorkerDialog, self).__init__(parent)
		# set up this dialog with the progress bar
		self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setLayout(QVBoxLayout())
		self.layout().addWidget(QLabel("Work in progres. Please wait"))
		self.pbar = QProgressBar()
		self.pbar.setRange(1, 100)
		self.pbar.setTextVisible(True)
		self.layout().addWidget(self.pbar)
		self.tedit = QTextEdit()
		self.layout().addWidget(self.tedit)
		# add a timer for a delayed opacity
		self.setWindowOpacity(0.0)
		self.delay = 0.0
		self.timer = QTimer(self)
		self.timer.setInterval(25)
		self.timer.timeout.connect(self.onTimerTimeOut)
		
	def showEvent(self, event):
		# call the base class method
		super(WorkerDialog, self).showEvent(event)
		self.timer.start()
	def reject(self):
		# we don't want this dialog to close if the user
		# presses the X button or the Escape key
		pass
	
	@Slot(str)
	def addTextLine(self, text):
		self.console_text_edit.append(text)
	
	@Slot()
	def clearTextEdit(self):
		self.console_text_edit.clear()
	
	@Slot(int)
	def setPercentage(self, value):
		self.pbar.setValue(value)
	@Slot()
	def onTimerTimeOut(self):
		if self.delay < 1.0:
			self.delay += 0.05
		else:
			self.setWindowOpacity(self.windowOpacity() + 0.05)
			if self.windowOpacity() == 1.0:
				self.timer.stop()
				self.timer.timeout.disconnect(self.onTimerTimeOut)

'''
Runs worker (instance of a class derived from Worker)
on a working thread using the provided dialog. The dialog
should have the sendPercentage(int) signal defined and should
derive from QDialog
'''
def runOnWorkerThread(worker, dialog = None):
	# Just to avoid debug issues on module import: Massimo Petracca 23/03/2021 - todo: solve it using PySide2 in debug also
	if dialog is None:
		dialog = WorkerDialog()
	# initial checks
	if not isinstance(worker, QObject):
		raise Exception('the worker object should inherit from QObject')
	if not hasattr(worker, 'finished'):
		raise Exception('the worker object should have the finished() signal')
	if not hasattr(worker, 'sendPercentage'):
		raise Exception('the worker object should have the sendPercentage(int) signal')
	if not hasattr(worker, 'sendTextLine'):
		raise Exception('the worker object should have the sendTextLine(str) signal')
	if not hasattr(worker, 'clearTextEdit'):
		raise Exception('the worker object should have the clearTextEdit() signal')
	if not isinstance(dialog, QDialog):
		raise Exception('the dialog object should inherit from QDialog')
	if not hasattr(dialog, 'setPercentage'):
		raise Exception('the dialog object should have a method called setPercentage(int)')
	if not callable(dialog.setPercentage):
		raise Exception('the dialog object setPercentage attribute is not a callable')
		
	# create the thread, the worker, and move the worker to the thread
	thread = QThread()
	worker.moveToThread(thread)
	
	# set up worker and thread connections
	worker.finished.connect(thread.quit)
	worker.finished.connect(worker.deleteLater)
	thread.started.connect(worker.run)
	thread.finished.connect(thread.deleteLater)
	worker.sendPercentage.connect(dialog.setPercentage)
	thread.finished.connect(dialog.accept)
	worker.sendTextLine.connect(dialog.addTextLine)
	worker.clearTextEdit.connect(dialog.clearTextEdit)
	
	# start the thread
	thread.start()
	
	# run dialog event loop
	dialog.exec_()









def _list_subdirs_name(current_dir, to_skip = []):
	""" returns a list of all directories in current_dir, 
	relative to current_dir, 
	and skipping all subdirectories.
	"""
	first_level_dirs = []
	first_done = False # skip the first one! it is the current_dir itself.
	for path, subdirs, files in os.walk(current_dir):
		if first_done:
			path = os.path.relpath(path, current_dir)
			if not path in to_skip:
				first_level_dirs.append(path)
			del subdirs[:] # only one level deep
		else:
			first_done = True
	return first_level_dirs

def _get_external_solvers_names():
	solvers_dir = PyMpc.Utils.get_external_solvers_dir()
	skip_directories = ([
		'__pycache__',
		'.git',
		'STKOMonitor',
		])
	ext_solvers = _list_subdirs_name(solvers_dir, skip_directories)
	return ext_solvers

def initialize():
	"""Function called by the application to initialize the global python interface.
	This function is called once in each application run.
	"""
	print('--------------------------------------------------------')
	print('           Python Interface Initialization              ')
	print('                      (global)                          ')
	print('--------------------------------------------------------')
	print('')
	
	print('Available external solvers:')
	for x in _get_external_solvers_names():
		print('   ',x)
	print('')
	
	# Massimo Petracca: 16/03/2021:
	# The backend should be set before we import matplotlib.pyplot for the first time
	# so we can do it here
	import matplotlib
	# Make sure that we are using QT5
	matplotlib.use('Qt5Agg')

def initialize_get_available_solvers():
	"""Function called by the application to get a list of available external solvers
	@todo send descriptions as well
	"""
	return _get_external_solvers_names()

def initialize_on_new_document():
	"""Function called by the application to initialize the document-wise python interface.
	This function is called everytime a new document is created or open.
	"""
	print('--------------------------------------------------------')
	print('           Python Interface Initialization              ')
	print('                   (document-wise)                      ')
	print('--------------------------------------------------------')
	print('     Initializing python interface of new document      ')
	print('--------------------------------------------------------')
	print('')
	
	# get the current document
	doc = PyMpc.App.caeDocument()
	
	active_solver_name = doc.solverName
	if active_solver_name == '':
		# no solver for this document.
		# just wait for the user to set an external solver
		print('No external solver set for this document.')
	else:
		# we have an external solver.
		# initialize it. (a consistency check will be performed)
		ext_solvers = _get_external_solvers_names()
		if len(ext_solvers) > 0 :
			if not active_solver_name in ext_solvers:
				raise Exception('Cannot find the specified external solver')
			active_ext_solver_module = importlib.import_module(active_solver_name + '.mpc_solver_initialize')
			active_ext_solver_module.initialize()
		else:
			print('Warning: no external solver available')

def initialize_on_set_external_solver(new_active_solver):
	"""Function called by the application to initialize the document-wise
	 python interface when the active external solver changes.
	"""
	
	print('--------------------------------------------------------')
	print('           Python Interface Initialization              ')
	print('                   (document-wise)                      ')
	print('--------------------------------------------------------')
	print(' Initializing python interface on active solver changed ')
	print('--------------------------------------------------------')
	print('')
	
	# get the current document
	doc = PyMpc.App.caeDocument()
	
	if new_active_solver == '':
		# an empty string is meant as null solver!
		print('Unloading external solver ...')
		doc.unregisterMetaDataAll()
		doc.solverName = new_active_solver
	else:
		# set the new solver.
		ext_solvers = _get_external_solvers_names()
		if len(ext_solvers) > 0 :
			if not new_active_solver in ext_solvers:
				raise Exception('Cannot find the specified external solver')
			active_ext_solver_module = importlib.import_module(new_active_solver + '.mpc_solver_initialize')
			active_ext_solver_module.initialize()
			# not needed. the active_ext_solver_module.initialize() method should set it!
			# but let's do it anyway...
			doc.solverName = new_active_solver 
		else:
			print('Warning: no external solver available')