import PyMpc
import PyMpc.Utils
import importlib
import os
import pkgutil

def __load_module_internal(namespace, the_register_func):
	"""
	Dynamically loads and registers modules from a specified namespace directory.

	Args:
		namespace (list of str): The namespace path as a list of directory names.
		the_register_func (callable): A function to register the metadata object returned by each module.

	Description:
		- Constructs the directory path based on the provided namespace.
		- Iterates over all modules in the target directory.
		- Imports each module dynamically using the constructed namespace.
		- If the module has a 'makeXObjectMetaData' function, it is called to obtain metadata.
		- Sets the 'Xnamespace' attribute of the metadata to the sub-namespace (excluding the first element).
		- Registers the metadata using the provided registration function.
	"""
	basedir = '{}{}opspro'.format(PyMpc.Utils.get_external_solvers_dir(), os.sep)
	the_dir = '{}{}{}'.format(basedir, os.sep, os.sep.join(namespace))
	the_namespace = '.'.join(namespace)
	if len(namespace) > 0:
		the_xnamespace = '.'.join(namespace[1:])
	else:
		the_xnamespace = ''
	the_modules = [imodule_name for _, imodule_name, _ in pkgutil.iter_modules([ the_dir ])]
	for imodule_name in the_modules:
		imodule = importlib.import_module('opspro.{}.{}'.format(the_namespace , imodule_name))
		if hasattr(imodule, 'makeXObjectMetaData'):
			imetadata = imodule.makeXObjectMetaData()
			imetadata.Xnamespace = the_xnamespace
			the_register_func(imetadata)

def initialize():
	
	"""
	  Called by @ref mpc_initialize module when this solver
	  is set as the current solver for the active document
	"""

	print('Loading External Solver: OpenSees for STKO-Professional')
	
	# get the current document
	doc = PyMpc.App.caeDocument()
	
	# clear old solver stuff
	doc.unregisterMetaDataAll()
	opensees_dir = PyMpc.Utils.get_external_solvers_dir() + os.sep + 'opspro'
	
	# register all metadata of physical properties
	__load_module_internal(['physical_properties'], doc.registerMetaDataPhysicalProperty)
	
	# register all metadata of element properties
	# ...
	
	# register all metadata of conditions
	# ...
	
	# register all metadata of definition
	# ...
	
	# register all metadata of analysis steps
	# ...
