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
	return None

def on_edit_begin(editor, xobj):
	module_name = 'opensees.{}.{}.{}'.format(
		module_from_index_source_type(xobj.parent.indexSourceType),
		xobj.Xnamespace,
		xobj.name
		)
	module = importlib.import_module(module_name)
	if hasattr(module, "onEditBegin"):
		module.onEditBegin(editor, xobj)

def on_editor_closing(editor, xobj):
	module_name = 'opensees.{}.{}.{}'.format(
		module_from_index_source_type(xobj.parent.indexSourceType),
		xobj.Xnamespace,
		xobj.name
		)
	module = importlib.import_module(module_name)
	if hasattr(module, "onEditorClosing"):
		module.onEditorClosing(editor, xobj)

def on_edit_finished(editor, xobj):
	module_name = 'opensees.{}.{}.{}'.format(
		module_from_index_source_type(xobj.parent.indexSourceType),
		xobj.Xnamespace,
		xobj.name
		)
	module = importlib.import_module(module_name)
	if hasattr(module, "onEditFinished"):
		module.onEditFinished(editor, xobj)

def on_attribute_changed(editor, xobj, attribute_name):
	module_name = 'opensees.{}.{}.{}'.format(
		module_from_index_source_type(xobj.parent.indexSourceType),
		xobj.Xnamespace,
		xobj.name
		)
	module = importlib.import_module(module_name)
	if hasattr(module, "onAttributeChanged"):
		module.onAttributeChanged(editor, xobj, attribute_name)

def on_convert_old_version(xobj, old_xobj):
	module_name = 'opensees.{}.{}.{}'.format(
		module_from_index_source_type(xobj.parent.indexSourceType),
		xobj.Xnamespace,
		xobj.name
		)
	module = importlib.import_module(module_name)
	if hasattr(module, "onConvertOldVersion"):
		module.onConvertOldVersion(xobj, old_xobj)