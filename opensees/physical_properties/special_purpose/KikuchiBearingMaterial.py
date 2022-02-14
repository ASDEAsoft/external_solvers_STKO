import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# matMSSTag
	at_matMSSTag = MpcAttributeMetaData()
	at_matMSSTag.type = MpcAttributeType.Index
	at_matMSSTag.name = 'matMSSTag'
	at_matMSSTag.group = '-matMSS'
	at_matMSSTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matMSSTag')+'<br/>') +
		html_par('matTag for MSS') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	at_matMSSTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matMSSTag.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# matMNSTag
	at_matMNSTag = MpcAttributeMetaData()
	at_matMNSTag.type = MpcAttributeType.Index
	at_matMNSTag.name = 'matMNSTag'
	at_matMNSTag.group = '-matMNS'
	at_matMNSTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matMNSTag')+'<br/>') +
		html_par('matTag for MNS') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	at_matMNSTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matMNSTag.indexSource.addAllowedNamespace("materials.uniaxial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'KikuchiBearingMaterial'
	xom.Xgroup = 'Bearing Material'
	xom.addAttribute(at_matMSSTag)
	xom.addAttribute(at_matMNSTag)
	
	
	return xom