import PyMpc
import PyMpc.Math
from opensees.utils.xobject_utils import module_from_index_source_type as mod_from_stype
import importlib

def evaluate(xobj):
	module_name = 'opensees.{}.{}.{}'.format(
		mod_from_stype(xobj.parent.indexSourceType),
		xobj.Xnamespace,
		xobj.name
		)
	module = importlib.import_module(module_name)
	xy = module.evaluateFunctionAttribute(xobj)
	return xy