# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# u
	at_u = MpcAttributeMetaData()
	at_u.type = MpcAttributeType.QuantityVector
	at_u.name = 'u'
	at_u.group = 'Non-linear'
	at_u.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('u')+'<br/>') + 
		html_par('strain (or deformation) at n-th point of the envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MultiLinear_Material','MultiLinear Material')+'<br/>') +
		html_end()
		)
	
	# f
	at_f = MpcAttributeMetaData()
	at_f.type = MpcAttributeType.QuantityVector
	at_f.name = 'f'
	at_f.group = 'Non-linear'
	at_f.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('f')+'<br/>') + 
		html_par('stress (or force) at n-th point of the envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MultiLinear_Material','MultiLinear Material')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'MultiLinear'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_u)
	xom.addAttribute(at_f)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial MultiLinear $matTag $u1 $f1 $u2 $f2 $u3 $f3 $u4 $f4 ...
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	u_at = xobj.getAttribute('u')
	if(u_at is None):
		raise Exception('Error: cannot find "u" attribute')
	u = u_at.quantityVector
	
	f_at = xobj.getAttribute('f')
	if(f_at is None):
		raise Exception('Error: cannot find "f" attribute')
	f = f_at.quantityVector
	
	if len(u) != 4:
		raise Exception('Error: expected a vector of 4 entries')
	if(len(u)!=len(f)):
		raise Exception('Error: different length of vectors')
	
	data = ' '.join(['{} {}'.format(u.valueAt(i), f.valueAt(i)) for i in range(4)])
	
	str_tcl = '{}uniaxialMaterial MultiLinear {} {}\n'.format(pinfo.indent, tag, data)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)