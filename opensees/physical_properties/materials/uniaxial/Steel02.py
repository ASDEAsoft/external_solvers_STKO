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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
		html_end()
		)
	
	# R0
	at_R0 = MpcAttributeMetaData()
	at_R0.type = MpcAttributeType.Real
	at_R0.name = 'R0'
	at_R0.group = 'Non-linear'
	at_R0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R0')+'<br/>') + 
		html_par('initial elastic tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
		html_end()
		)
	
	# CR1
	at_CR1 = MpcAttributeMetaData()
	at_CR1.type = MpcAttributeType.Real
	at_CR1.name = 'CR1'
	at_CR1.group = 'Non-linear'
	at_CR1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('CR1')+'<br/>') + 
		html_par('initial elastic tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
		html_end()
		)
	
	# CR2
	at_CR2 = MpcAttributeMetaData()
	at_CR2.type = MpcAttributeType.Real
	at_CR2.name = 'CR2'
	at_CR2.group = 'Non-linear'
	at_CR2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('CR2')+'<br/>') + 
		html_par('initial elastic tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
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
		html_par('isotropic hardening parameter (see explanation under a1). (optional default = 1.0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
		html_end()
		)
	at_a2.setDefault(1.0)
	
	# a3
	at_a3 = MpcAttributeMetaData()
	at_a3.type = MpcAttributeType.Real
	at_a3.name = 'a3'
	at_a3.group = 'Optional parameters'
	at_a3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a3')+'<br/>') + 
		html_par('isotropic hardening parameter, increase of tension yield envelope as proportion of yield strength after a plastic strain of a4*(Fy/E0). (optional default = 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
		html_end()
		)
	at_a3.setDefault(0.0)
	
	# a4
	at_a4 = MpcAttributeMetaData()
	at_a4.type = MpcAttributeType.Real
	at_a4.name = 'a4'
	at_a4.group = 'Optional parameters'
	at_a4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a4')+'<br/>') + 
		html_par('isotropic hardening parameter (see explanation under a3). (optional default = 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
		html_end()
		)
	at_a4.setDefault(1.0)
	
	# sigInit
	at_sigInit = MpcAttributeMetaData()
	at_sigInit.type = MpcAttributeType.QuantityScalar
	at_sigInit.name = 'sigInit'
	at_sigInit.group = 'Optional parameters'
	at_sigInit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sigInit')+'<br/>') + 
		html_par('if (sigInit!= 0.0) { double epsInit = sigInit/E; eps = trialStrain+epsInit; } else eps = trialStrain') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel02_Material_--_Giuffr%C3%A9-Menegotto-Pinto_Model_with_Isotropic_Strain_Hardening','Steel02 Material')+'<br/>') +
		html_end()
		)
	at_sigInit.setDefault(0.0)
	at_sigInit.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'Steel02'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_E0)
	xom.addAttribute(at_R0)
	xom.addAttribute(at_CR1)
	xom.addAttribute(at_CR2)
	xom.addAttribute(at_b)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_a1)
	xom.addAttribute(at_a2)
	xom.addAttribute(at_a3)
	xom.addAttribute(at_a4)
	xom.addAttribute(at_sigInit)
	
	# use_Optional-dep
	xom.setVisibilityDependency(at_Optional, at_a1)
	xom.setVisibilityDependency(at_Optional, at_a2)
	xom.setVisibilityDependency(at_Optional, at_a3)
	xom.setVisibilityDependency(at_Optional, at_a4)
	xom.setVisibilityDependency(at_Optional, at_sigInit)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Steel02 $matTag $Fy $E $b $R0 $cR1 $cR2 <$a1 $a2 $a3 $a4 $sigInit>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	Fy_at = xobj.getAttribute('Fy')
	if(Fy_at is None):
		raise Exception('Error: cannot find "Fy" attribute')
	Fy = Fy_at.quantityScalar
	
	E_at = xobj.getAttribute('E0')
	if(E_at is None):
		raise Exception('Error: cannot find "E0" attribute')
	E = E_at.quantityScalar
	
	b_at = xobj.getAttribute('b')
	if(b_at is None):
		raise Exception('Error: cannot find "b" attribute')
	b = b_at.real
	
	R0_at = xobj.getAttribute('R0')
	if(R0_at is None):
		raise Exception('Error: cannot find "R0" attribute')
	R0 = R0_at.real
	
	cR1_at = xobj.getAttribute('CR1')
	if(cR1_at is None):
		raise Exception('Error: cannot find "CR1" attribute')
	cR1 = cR1_at.real
	
	cR2_at = xobj.getAttribute('CR2')
	if(cR2_at is None):
		raise Exception('Error: cannot find "CR2" attribute')
	cR2 = cR2_at.real
	
	
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
		
		sigInit_at = xobj.getAttribute('sigInit')
		if(sigInit_at is None):
			raise Exception('Error: cannot find "sigInit" attribute')
		sigInit = sigInit_at.quantityScalar
		
		sopt += ' {} {} {} {} {}'.format(a1, a2, a3, a4, sigInit.value)
	
	str_tcl = '{}uniaxialMaterial Steel02 {} {} {} {} {} {} {}{}\n'.format(pinfo.indent, tag, Fy.value, E.value, b, R0, cR1, cR2, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)