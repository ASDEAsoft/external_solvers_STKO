# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# C
	at_C = MpcAttributeMetaData()
	at_C.type = MpcAttributeType.Real
	at_C.name = 'C'
	at_C.group = 'Non-linear'
	at_C.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('C')+'<br/>') + 
		html_par('damping coeficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Viscous_Material','Viscous Material')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Elasticity'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('power factor (=1 means linear damping)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Viscous_Material','Viscous Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Viscous'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_C)
	xom.addAttribute(at_alpha)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Viscous $matTag $C $alpha
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	C_at = xobj.getAttribute('C')
	if(C_at is None):
		raise Exception('Error: cannot find "C" attribute')
	C = C_at.real
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	
	str_tcl = '{}uniaxialMaterial Viscous {} {} {}\n'.format(pinfo.indent, tag, C, alpha)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)