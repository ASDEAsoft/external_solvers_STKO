# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Elasticity'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-No_Tension_Material','Elastic-No Tension Material')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'ENT'
	xom.Xgroup = 'Some Standard Uniaxial Materials'
	xom.addAttribute(at_E)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ENT $matTag $E
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar
	
	
	str_tcl = '{}uniaxialMaterial ENT {} {}\n'.format(pinfo.indent, tag, E.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)