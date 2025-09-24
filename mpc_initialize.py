"""@package mpc_initialize
This module contains functions for the correct initialization of PyMpc.

More details here.
"""

import os
import PyMpc.Utils
import importlib

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
				raise Exception(f'Cannot find the specified external solver "{active_solver_name}" among the available ones: {ext_solvers}')
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
				raise Exception(f'Cannot find the specified external solver "{new_active_solver}" among the available ones: {ext_solvers}')
			active_ext_solver_module = importlib.import_module(new_active_solver + '.mpc_solver_initialize')
			active_ext_solver_module.initialize()
			# not needed. the active_ext_solver_module.initialize() method should set it!
			# but let's do it anyway...
			doc.solverName = new_active_solver 
		else:
			print('Warning: no external solver available')