# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fy
	at_fy = MpcAttributeMetaData()
	at_fy.type = MpcAttributeType.QuantityScalar
	at_fy.name = 'fy'
	at_fy.group = 'Non-linear'
	at_fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fy')+'<br/>') + 
		html_par('yield strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RambergOsgoodSteel_Material','RambergOsgoodSteel Material')+'<br/>') +
		html_end()
		)
	at_fy.dimension = u.F/u.L**2
	
	# E0
	at_E0 = MpcAttributeMetaData()
	at_E0.type = MpcAttributeType.QuantityScalar
	at_E0.name = 'E0'
	at_E0.group = 'Elasticity'
	at_E0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E0')+'<br/>') + 
		html_par('initial elastic tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RambergOsgoodSteel_Material','RambergOsgoodSteel Material')+'<br/>') +
		html_end()
		)
	at_E0.dimension = u.F/u.L**2
	
	# a
	at_a = MpcAttributeMetaData()
	at_a.type = MpcAttributeType.Real
	at_a.name = 'a'
	at_a.group = 'Non-linear'
	at_a.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a')+'<br/>') + 
		html_par('yield offset and the Commonly used value for $a is 0.002') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RambergOsgoodSteel_Material','RambergOsgoodSteel Material')+'<br/>') +
		html_end()
		)
	
	# n
	at_n = MpcAttributeMetaData()
	at_n.type = MpcAttributeType.Real
	at_n.name = 'n'
	at_n.group = 'Non-linear'
	at_n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('n')+'<br/>') + 
		html_par('Parameters to control the transition from elastic to plastic branches. And controls the hardening of the material by increasing the \'n\' hardening ratio will be decreased. Commonly used values for $n are ~5 or greater') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RambergOsgoodSteel_Material','RambergOsgoodSteel Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'RambergOsgoodSteel'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(at_fy)
	xom.addAttribute(at_E0)
	xom.addAttribute(at_a)
	xom.addAttribute(at_n)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial RambergOsgoodSteel $matTag $fy $E0 $a $n
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fy_at = xobj.getAttribute('fy')
	if(fy_at is None):
		raise Exception('Error: cannot find "fy" attribute')
	fy = fy_at.quantityScalar
	
	E0_at = xobj.getAttribute('E0')
	if(E0_at is None):
		raise Exception('Error: cannot find "E0" attribute')
	E0 = E0_at.quantityScalar
	
	a_at = xobj.getAttribute('a')
	if(a_at is None):
		raise Exception('Error: cannot find "a" attribute')
	a = a_at.real
	
	n_at = xobj.getAttribute('n')
	if(n_at is None):
		raise Exception('Error: cannot find "n" attribute')
	n = n_at.real
	
	
	str_tcl = '{}uniaxialMaterial RambergOsgoodSteel {} {} {} {} {}\n'.format(pinfo.indent, tag, fy.value, E0.value, a, n)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)