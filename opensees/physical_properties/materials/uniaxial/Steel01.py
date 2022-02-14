# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Fy
	at_Fy = MpcAttributeMetaData()
	at_Fy.type = MpcAttributeType.QuantityScalar
	at_Fy.name = 'Fy'
	at_Fy.group = 'Non-linear'
	at_Fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fy')+'<br/>') + 
		html_par('yield strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel01_Material','Steel01 Material')+'<br/>') +
		html_end()
		)
	at_Fy.dimension = u.F/u.L**2
	
	# E0
	at_E0 = MpcAttributeMetaData()
	at_E0.type = MpcAttributeType.QuantityScalar
	at_E0.name = 'E0'
	at_E0.group = 'Elasticity'
	at_E0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E0')+'<br/>') + 
		html_par('initial elastic tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel01_Material','Steel01 Material')+'<br/>') +
		html_end()
		)
	at_E0.dimension = u.F/u.L**2
	
	# b
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.Real
	at_b.name = 'b'
	at_b.group = 'Non-linear'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b')+'<br/>') + 
		html_par('strain-hardening ratio (ratio between post-yield tangent and initial elastic tangent)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel01_Material','Steel01 Material')+'<br/>') +
		html_end()
		)
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel01_Material','Steel01 Material')+'<br/>') +
		html_end()
		)
	
	# a1
	at_a1 = MpcAttributeMetaData()
	at_a1.type = MpcAttributeType.Real
	at_a1.name = 'a1'
	at_a1.group = 'Optional parameters'
	at_a1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a1')+'<br/>') + 
		html_par('isotropic hardening parameter, increase of compression yield envelope as proportion of yield strength after a plastic strain of a2*(Fy/E0). (optional).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel01_Material','Steel01 Material')+'<br/>') +
		html_end()
		)
	
	# a2
	at_a2 = MpcAttributeMetaData()
	at_a2.type = MpcAttributeType.Real
	at_a2.name = 'a2'
	at_a2.group = 'Optional parameters'
	at_a2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a2')+'<br/>') + 
		html_par('isotropic hardening parameter (see explanation under a1). (optional).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel01_Material','Steel01 Material')+'<br/>') +
		html_end()
		)
	
	# a3
	at_a3 = MpcAttributeMetaData()
	at_a3.type = MpcAttributeType.Real
	at_a3.name = 'a3'
	at_a3.group = 'Optional parameters'
	at_a3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a3')+'<br/>') + 
		html_par('isotropic hardening parameter, increase of tension yield envelope as proportion of yield strength after a plastic strain of a4*(Fy/E0). (optional)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel01_Material','Steel01 Material')+'<br/>') +
		html_end()
		)
	
	# a4
	at_a4 = MpcAttributeMetaData()
	at_a4.type = MpcAttributeType.Real
	at_a4.name = 'a4'
	at_a4.group = 'Optional parameters'
	at_a4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a4')+'<br/>') + 
		html_par('isotropic hardening parameter (see explanation under a3). (optional)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel01_Material','Steel01 Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Steel01'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_E0)
	xom.addAttribute(at_b)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_a1)
	xom.addAttribute(at_a2)
	xom.addAttribute(at_a3)
	xom.addAttribute(at_a4)
	
	# Optional_parameters-dep
	xom.setVisibilityDependency(at_Optional, at_a1)
	xom.setVisibilityDependency(at_Optional, at_a2)
	xom.setVisibilityDependency(at_Optional, at_a3)
	xom.setVisibilityDependency(at_Optional, at_a4)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Steel01 $matTag $Fy $E0 $b <$a1 $a2 $a3 $a4>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	Fy_at = xobj.getAttribute('Fy')
	if(Fy_at is None):
		raise Exception('Error: cannot find "Fy" attribute')
	Fy = Fy_at.quantityScalar
	
	E0_at = xobj.getAttribute('E0')
	if(E0_at is None):
		raise Exception('Error: cannot find "E0" attribute')
	E0 = E0_at.quantityScalar
	
	b_at = xobj.getAttribute('b')
	if(b_at is None):
		raise Exception('Error: cannot find "b" attribute')
	b = b_at.real
	
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		a1_at = xobj.getAttribute('a1')
		if(a1_at is None):
			raise Exception('Error: cannot find "a1" attribute')
		a1 = a1_at.real
		
		a2_at = xobj.getAttribute('a2')
		if(a2_at is None):
			raise Exception('Error: cannot find "a2" attribute')
		a2 = a2_at.real
		
		a3_at = xobj.getAttribute('a3')
		if(a3_at is None):
			raise Exception('Error: cannot find "a3" attribute')
		a3 = a3_at.real
		
		a4_at = xobj.getAttribute('a4')
		if(a4_at is None):
			raise Exception('Error: cannot find "a4" attribute')
		a4 = a4_at.real
		
		sopt += ' {} {} {} {}'.format(a1, a2, a3, a4)
	
	str_tcl = '{}uniaxialMaterial Steel01 {} {} {} {}{}\n'.format(pinfo.indent, tag, Fy.value, E0.value, b, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)