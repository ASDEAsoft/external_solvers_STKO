from PyMpc import *

def getExtrusionDataAllItems(prop):
	'''
	utility function used in @ref makeExtrusionBeamDataCompoundInfo.
	check whether a property has extrusion info. returns:
	1) None if no extrusion info could be found
	2) prop itself if prop is the one that has the extrusion custom object in its xobj
	3) the nested property (as indexed sub.property in prop) that has the
	   extrusion custom object in its xobj
	'''
	
	import importlib
	
	if prop is None:
		return None
	xobj = prop.XObject
	if xobj is None:
		return None
	if xobj.Xnamespace:
		module_name = 'opensees.physical_properties.{}.{}'.format(xobj.Xnamespace, xobj.name)
	else:
		module_name = 'opensees.physical_properties.{}'.format(xobj.name)
	module = importlib.import_module(module_name)
	if not hasattr(module, 'makeExtrusionBeamDataCompoundInfo'):
		#return None
		dummy = MpcSectionExtrusionBeamDataCompoundInfoItem()
		dummy.property = prop
		dummy_coll = MpcSectionExtrusionBeamDataCompoundInfoItemCollection()
		dummy_coll.append(dummy)
		return dummy_coll
	info = module.makeExtrusionBeamDataCompoundInfo(xobj)
	'''
	here we return the whole list of properties with extrusion and their weights
	'''
	return info.items

def getExtrusionDataSingleItem(prop):
	all_items = getExtrusionDataAllItems(prop)
	if all_items is None:
		return None
	num_items = len(all_items)
	if num_items == 0:
		return None
	if num_items > 1:
		raise Exception('Error one of the referenced sub-properties has more than 1 extrusion info item')
	'''
	ok. return the first item.
	'''
	return all_items[0]

def checkOffsetCompatibility(all_items):
	'''
	when an element has more cross sections, they might have different offset.
	we do not allow this.
	print a warning saying that we will consider the abs-max of all offsets
	'''
	
	if len(all_items) < 2:
		return
	
	ymax = 0.0
	zmax = 0.0
	first_done = False
	for item in all_items:
		if item is not None:
			iy = item.yOffset
			iz = item.zOffset
			if first_done:
				if abs(iy) > abs(ymax):
					ymax = iy
				if abs(iz) > abs(zmax):
					zmax = iz
			else:
				ymax = iy
				zmax = iz
				first_done = True
	
	num_diff = 0
	for item in all_items:
		if item is not None:
			if abs(item.yOffset - ymax) > 1.0e-14:
				num_diff += 1
				item.yOffset = ymax
			if abs(item.zOffset - zmax) > 1.0e-14:
				num_diff += 1
				item.zOffset = zmax
	if num_diff > 0:
		print((
			'Warning: cross sections in a compound physical property have different offsets. '
			'This is not allowed. STKO will consider for the absolute max of them'))