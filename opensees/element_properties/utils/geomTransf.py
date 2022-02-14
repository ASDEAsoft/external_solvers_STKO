from PyMpc import *
from mpc_utils_html import *

def makeAttribute(group, name = 'transType'):
	'''
	Creates the common attribute for coordinate transformation.
	Only the transformation type is user-defined. Local axes and section offsets are
	obtained from assocuiated orientation and physical property
	'''
	at_transType = MpcAttributeMetaData()
	at_transType.type = MpcAttributeType.String
	at_transType.name = name
	at_transType.group = group
	at_transType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext(name)+'<br/>') +
		html_par(' The geometric-transformation command is used to construct a coordinate-transformation (CrdTransf) object, which transforms beam element stiffness and resisting force from the basic system to the global-coordinate system.The command has at least one argument, the transformation type.') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Linear_Transformation','Linear transformation')+'<br/>') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/PDelta_Transformation','P-Delta transformation')+'<br/>') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Corotational_Transformation','Corotational transformation')+'<br/>') +
		html_end()
		)
	at_transType.sourceType = MpcAttributeSourceType.List
	at_transType.setSourceList(['Linear', 'PDelta', 'Corotational'])
	at_transType.setDefault('Linear')
	return at_transType

def writeGeomTransfType(pinfo, is3D, transType):
	'''
	crates a string for the coordinate transformation command. The tag is taken
	equal to the current element in pinfo.
	This function returns a end-line-terminated string
	'''
	
	import importlib
	from io import StringIO
	import math
	ss = StringIO()
	
	# current element data
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	xobj = phys_prop.XObject
	
	# write comment and main command
	ss.write('# Geometric transformation command\n')
	ss.write('geomTransf {} {}'.format(transType, elem.id))
	
	# 3x3 element orientation matrix [vX | vY | vZ]
	T = elem.orientation.computeOrientation()
	vZ = T.col(2)
	
	# in 3D we need the vecxz
	if is3D:
		ss.write(' {} {} {}'.format(vZ.x, vZ.y, vZ.z))
	
	# let's see if we have section offsets
	# from the physical property xobject
	if xobj.Xnamespace:
		module_name = 'opensees.physical_properties.{}.{}'.format(xobj.Xnamespace, xobj.name)
	else:
		module_name = 'opensees.physical_properties.{}'.format(xobj.name)
	module = importlib.import_module(module_name)
	if hasattr(module, 'getSectionOffset'):
		# here we assume the getSectionOffset method returns a tuple with y and z offsets in local directions.
		# if there is no offset, they will be both zero
		offset_y, offset_z = module.getSectionOffset(xobj)
		# those 2 scalars are in the local direction.
		# transform them in global coordinates
		if math.sqrt(offset_y**2 + offset_z**2) > 1.0e-14:
			vY = T.col(1)
			vO = vY*offset_y + vZ*offset_z
			# write the offset option
			if is3D:
				# -jntOffset $dXi $dYi $dZi $dXj $dYj $dZj
				ss.write(' -jntOffset {0} {1} {2}   {0} {1} {2}'.format(vO.x, vO.y, vO.z))
			else:
				# -jntOffset $dXi $dYi $dXj $dYj
				ss.write(' -jntOffset {0} {1}   {0} {1}'.format(vO.x, vO.y))
	
	# append and endline and return
	ss.write('\n')
	return ss.getvalue()

def writeGeomTransf(pinfo, is3D, name = 'transType'):
	'''
	same as above, but taking the type from the xobject, assuming the makeAttribute 
	method was used.
	'''
	elem_prop = pinfo.elem_prop
	xobj = elem_prop.XObject
	transType_at = xobj.getAttribute(name)
	if(transType_at is None):
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	transType = transType_at.string
	return writeGeomTransfType(pinfo, is3D, transType)