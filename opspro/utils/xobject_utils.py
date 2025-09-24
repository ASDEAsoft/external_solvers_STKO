'''
This module contains utility functions for handling XObjects in STKO's OpenSees interface.
It's equal to the opensees.utils.xobject_utils one. The only difference is the opspro instead of opensees in the module path.
TODO: unify the two modules.
'''

import PyMpc
from PyMpc import MpcAttributeIndexSourceType as stype
import importlib

def module_from_index_source_type(isource_type):
	if(isource_type == stype.Definition):
		return 'definitions'
	elif(isource_type == stype.PhysicalProperty):
		return 'physical_properties'
	elif(isource_type == stype.ElementProperty):
		return 'element_properties'
	elif(isource_type == stype.Condition):
		return 'conditions'
	elif(isource_type == stype.AnalysisStep):
		return 'analysis_steps'
	else:
		raise Exception('Unknown index source type: {}'.format(isource_type))

def _get_module_name(xobj):
	if not xobj.name:
		raise Exception('XObject has no name')
	if xobj.Xnamespace:
		return f'opspro.{module_from_index_source_type(xobj.parent.indexSourceType)}.{xobj.Xnamespace}.{xobj.name}'
	else:
		return f'opspro.{module_from_index_source_type(xobj.parent.indexSourceType)}.{xobj.name}'

def on_edit_begin(editor, xobj):
	module = importlib.import_module(_get_module_name(xobj))
	if hasattr(module, "onEditBegin"):
		module.onEditBegin(editor, xobj)

def on_editor_closing(editor, xobj):
	module = importlib.import_module(_get_module_name(xobj))
	if hasattr(module, "onEditorClosing"):
		module.onEditorClosing(editor, xobj)

def on_edit_finished(editor, xobj):
	module = importlib.import_module(_get_module_name(xobj))
	if hasattr(module, "onEditFinished"):
		module.onEditFinished(editor, xobj)

def on_attribute_changed(editor, xobj, attribute_name):
	module = importlib.import_module(_get_module_name(xobj))
	if hasattr(module, "onAttributeChanged"):
		module.onAttributeChanged(editor, xobj, attribute_name)

def on_convert_old_version(xobj, old_xobj):
	module = importlib.import_module(_get_module_name(xobj))
	if hasattr(module, "onConvertOldVersion"):
		module.onConvertOldVersion(xobj, old_xobj)