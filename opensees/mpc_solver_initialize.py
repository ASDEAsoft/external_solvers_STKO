import PyMpc
import PyMpc.Utils
import importlib
import os
import pkgutil

def __load_module_internal(namespace, the_register_func):
	basedir = '{}{}opensees'.format(PyMpc.Utils.get_external_solvers_dir(), os.sep)
	the_dir = '{}{}{}'.format(basedir, os.sep, os.sep.join(namespace))
	the_namespace = '.'.join(namespace)
	if len(namespace) > 0:
		the_xnamespace = '.'.join(namespace[1:])
	else:
		the_xnamespace = ''
	#msg_loaded = []
	the_modules = [imodule_name for _, imodule_name, _ in pkgutil.iter_modules([ the_dir ])]
	for imodule_name in the_modules:
		#msg_loaded.append('registering {} [{}]:  {}'.format(namespace[0], the_xnamespace, imodule_name))
		imodule = importlib.import_module('opensees.{}.{}'.format(the_namespace , imodule_name))
		if hasattr(imodule, 'makeXObjectMetaData'):
			imetadata = imodule.makeXObjectMetaData()
			imetadata.Xnamespace = the_xnamespace
			the_register_func(imetadata)

	#if len(msg_loaded) > 0:
	#	msg_loaded.append('--------------------------------------------------------------')
	#	print('\n'.join(msg for msg in msg_loaded))

def initialize():
	
	""" Called by @ref mpc_initialize module when this solver
	is set as the current solver for the active document
	"""
	print('Loading External Solver: OpenSees')
	
	# get the current document
	doc = PyMpc.App.caeDocument()
	
	# clear old solver stuff
	doc.unregisterMetaDataAll()
	opensees_dir = PyMpc.Utils.get_external_solvers_dir() + os.sep + 'opensees'
	
	# register all metadata of physical properties
	__load_module_internal(['physical_properties', 'materials', 'nD'], doc.registerMetaDataPhysicalProperty)
	__load_module_internal(['physical_properties', 'materials', 'nD', 'PlugIn'], doc.registerMetaDataPhysicalProperty)
	__load_module_internal(['physical_properties', 'materials', 'uniaxial'], doc.registerMetaDataPhysicalProperty)
	__load_module_internal(['physical_properties', 'materials', 'uniaxial', 'PlugIn'], doc.registerMetaDataPhysicalProperty)
	__load_module_internal(['physical_properties', 'materials', 'uniaxial', 'Design'], doc.registerMetaDataPhysicalProperty)
	__load_module_internal(['physical_properties', 'sections'], doc.registerMetaDataPhysicalProperty)
	__load_module_internal(['physical_properties', 'special_purpose'], doc.registerMetaDataPhysicalProperty)
	
	# register all metadata of element properties
	__load_module_internal(['element_properties', 'absorbingBoundaries'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'beam_column_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'bearing_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'brick_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'tetrahedron_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'cable_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'contact_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'joint_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'link_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'misc'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'quadrilateral_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'shell'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'special_purpose'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'triangular_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'truss_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'up_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'zero_length_elements'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'RC Beam-Truss Models'], doc.registerMetaDataElementProperty)
	__load_module_internal(['element_properties', 'RC Beam-Column Joint Models'], doc.registerMetaDataElementProperty)
	
	# register all metadata of conditions
	__load_module_internal(['conditions', 'Constraints', 'sp'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Constraints', 'mp'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Ground_Motion'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Loads', 'eleLoad'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Loads', 'Generic'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Loads', 'Force'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Loads', 'sp'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Loads', 'Moving'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Mass'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'GroundMotion'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Multi_Support_Excitation_Pattern'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'Uniform_Excitation_Pattern'], doc.registerMetaDataCondition)
	__load_module_internal(['conditions', 'DigitalTwin'], doc.registerMetaDataCondition)
	
	# register all metadata of definition
	__load_module_internal(['definitions', 'frictionModel'], doc.registerMetaDataDefinition)
	__load_module_internal(['definitions', 'timeSeries'], doc.registerMetaDataDefinition)
	__load_module_internal(['definitions', 'randomVariable'], doc.registerMetaDataDefinition)
	__load_module_internal(['definitions', 'limitCurves'], doc.registerMetaDataDefinition)
	__load_module_internal(['definitions', 'misc'], doc.registerMetaDataDefinition)
	
	# register all metadata of analysis steps
	__load_module_internal(['analysis_steps', 'Patterns', 'addPattern'], doc.registerMetaDataAnalysisStep)
	__load_module_internal(['analysis_steps', 'Patterns', 'removePattern'], doc.registerMetaDataAnalysisStep)
	__load_module_internal(['analysis_steps', 'Recorders'], doc.registerMetaDataAnalysisStep)
	__load_module_internal(['analysis_steps', 'Analyses'], doc.registerMetaDataAnalysisStep)
	__load_module_internal(['analysis_steps', 'Custom'], doc.registerMetaDataAnalysisStep)
	__load_module_internal(['analysis_steps', 'Misc_commands'], doc.registerMetaDataAnalysisStep)
