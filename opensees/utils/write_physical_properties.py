import importlib

def write_physical_properties(physical_properties, pinfo, use_namespace):
	print('writing physical_properties...')
	
	for item_id, item in physical_properties.items():
		xobj = item.XObject
		if(xobj is None):
			raise Exception('null XObject in section object')
		if xobj.Xnamespace.startswith(use_namespace):
			module_name = 'opensees.physical_properties.{}.{}'.format(xobj.Xnamespace, xobj.name)
			module = importlib.import_module(module_name)
			if hasattr(module, 'writeTcl'):
				pinfo.phys_prop = item
				module.writeTcl(pinfo)