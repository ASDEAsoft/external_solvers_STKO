import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# matTag
	at_matTag = MpcAttributeMetaData()
	at_matTag.type = MpcAttributeType.Index
	at_matTag.name = 'matTag'
	at_matTag.group = 'Group'
	at_matTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') +
		html_par('tag associated with previously-defined ndMaterial object') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthND_Element','ZeroLengthND Element')+'<br/>') +
		html_end()
		)
	at_matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag.indexSource.addAllowedNamespace("materials.nD")
	
	# uniTag
	at_uniTag = MpcAttributeMetaData()
	at_uniTag.type = MpcAttributeType.Index
	at_uniTag.name = 'uniTag'
	at_uniTag.group = 'Group'
	at_uniTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('uniTag')+'<br/>') +
		html_par('tag associated with previously-defined UniaxialMaterial object which may be used to represent uncoupled behavior orthogonal to the plane of the NDmaterial response. SEE NOTES 2 and 3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthND_Element','ZeroLengthND Element')+'<br/>') +
		html_end()
		)
	at_uniTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_uniTag.indexSource.addAllowedNamespace("materials.uniaxial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLengthNDMaterial'
	xom.Xgroup = 'Zero-Length Material'
	xom.addAttribute(at_matTag)
	xom.addAttribute(at_uniTag)
	
	
	return xom