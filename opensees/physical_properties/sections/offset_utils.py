import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

class OffsetData:
	def __init__(self, dim = 3, y = 0.0, z = 0.0):
		self.dim = dim
		self.y = y
		self.z = z

def addOffsetMetaData(xom, dep_3d = None):
	'''
	this common utilty can be used by every section XObject python script to
	include section offsets in the local y and z directions
	'''
	
	at_y = MpcAttributeMetaData()
	at_y.type = MpcAttributeType.QuantityScalar
	at_y.name = 'Y/section_offset'
	at_y.group = 'Section Offset'
	at_y.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('y')+'<br/>') + 
		html_par('Offset along the local Y direction') +
		html_end()
		)
	at_y.dimension = u.L
	at_y.setDefault(0.0)
	
	at_z = MpcAttributeMetaData()
	at_z.type = MpcAttributeType.QuantityScalar
	at_z.name = 'Z/section_offset'
	at_z.group = 'Section Offset'
	at_z.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('z')+'<br/>') + 
		html_par('Offset along the local Z direction') +
		html_end()
		)
	at_z.dimension = u.L
	at_z.setDefault(0.0)
	
	xom.addAttribute(at_y)
	xom.addAttribute(at_z)
	if dep_3d is not None:
		xom.setVisibilityDependency(dep_3d, at_z)

def getOffsetData(xobj):
	'''
	if the xobj has the offset attributes, this will evaluate them and get their
	value.
	'''
	d = OffsetData()
	
	at_y = xobj.getAttribute('Y/section_offset')
	if at_y is None:
		return None
	d.y = at_y.quantityScalar.value
	
	at_z = xobj.getAttribute('Z/section_offset')
	if at_z is None:
		return None
	if not at_z.visible: # if not, we are in 2D
		d.z = 0.0
		d.dim = 2
	else:
		d.z = at_z.quantityScalar.value
		d.dim = 3
	
	return d

def updateVisibility(is_3D : bool, xobj : MpcXObject):
	'''
	this function will update the visibility of the offset attributes.
	useful when the optional dep_3d attribute is not used.
	'''
	at_z = xobj.getAttribute('Z/section_offset')
	if at_z:
		at_z.visible = is_3D
