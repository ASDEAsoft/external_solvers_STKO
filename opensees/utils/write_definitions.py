import importlib

def write_definitions(definitions, pinfo):
	print('writing definitions...')
	# for each definition...
	for item_id, item in definitions.items():
		xobj = item.XObject
		if(xobj is None):
			raise Exception('null XObject in definition object')
		# if it is a randomVariable and it is the first one, first add reliability command
		if xobj.Xnamespace.startswith('randomVariable'):
			if not pinfo.firstRandomVariable:
				pinfo.firstRandomVariable = True
				pinfo.out_file.write('\n{}# Found for the first ime a random variable. Call reliability module\n'.format(pinfo.indent))
				pinfo.out_file.write('{}{}\n'.format(pinfo.indent, 'wipeReliability'))
				pinfo.out_file.write('{}{}\n'.format(pinfo.indent, 'reliability'))
		module_name = 'opensees.definitions.{}.{}'.format(xobj.Xnamespace, xobj.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl'):
			pinfo.definition = item
			module.writeTcl(pinfo)