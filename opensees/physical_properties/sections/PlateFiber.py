import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeExtrusionShellDataInfo(xobj):
	h_at = xobj.getAttribute('h')
	if(h_at is None):
		raise Exception('Error: cannot find "h" attribute')
	h = h_at.quantityScalar.value
	info = MpcSectionExtrusionShellDataInfo(h)
	return info

def makeXObjectMetaData():
	
	# matTag
	at_matTag = MpcAttributeMetaData()
	at_matTag.type = MpcAttributeType.Index
	at_matTag.name = 'matTag'
	at_matTag.group = 'Group'
	at_matTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') + 
		html_par('nDMaterial tag to be assigned to each fiber') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plate_Fiber_Section','Plate Fiber Section')+'<br/>') +
		html_end()
		)
	at_matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag.indexSource.addAllowedNamespace('materials.nD')
	
	# h
	at_h = MpcAttributeMetaData()
	at_h.type = MpcAttributeType.QuantityScalar
	at_h.name = 'h'
	at_h.group = 'Group'
	at_h.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h')+'<br/>') + 
		html_par('plate thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plate_Fiber_Section','Plate Fiber Section')+'<br/>') +
		html_end()
		)
	at_h.dimension = u.L
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'PlateFiber'
	xom.addAttribute(at_matTag)
	xom.addAttribute(at_h)
	
	return xom

def writeTcl(pinfo):
	
	#section PlateFiber $secTag $matTag $h
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	matTag_at = xobj.getAttribute('matTag')
	if(matTag_at is None):
		raise Exception('Error: cannot find "matTag" attribute')
	matTag = matTag_at.index
	
	h_at = xobj.getAttribute('h')
	if(h_at is None):
		raise Exception('Error: cannot find "h" attribute')
	h = h_at.quantityScalar
	
	
	str_tcl = '{}section PlateFiber {} {} {}\n'.format(pinfo.indent, tag, matTag, h.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)