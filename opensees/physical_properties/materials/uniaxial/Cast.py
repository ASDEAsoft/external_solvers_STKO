# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# n
	at_n = MpcAttributeMetaData()
	at_n.type = MpcAttributeType.Integer
	at_n.name = 'n'
	at_n.group = 'Non-linear'
	at_n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('n')+'<br/>') + 
		html_par('Number of yield fingers of the CSF-brace') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	
	# bo
	at_bo = MpcAttributeMetaData()
	at_bo.type = MpcAttributeType.QuantityScalar
	at_bo.name = 'bo'
	at_bo.group = 'Non-linear'
	at_bo.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bo')+'<br/>') + 
		html_par('Width of an individual yielding finger at its base of the CSF-brace') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	at_bo.dimension = u.L
	
	# h
	at_h = MpcAttributeMetaData()
	at_h.type = MpcAttributeType.QuantityScalar
	at_h.name = 'h'
	at_h.group = 'Non-linear'
	at_h.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h')+'<br/>') + 
		html_par('Thickness of an individual yielding finger') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	at_h.dimension = u.L
	
	# fy
	at_fy = MpcAttributeMetaData()
	at_fy.type = MpcAttributeType.QuantityScalar
	at_fy.name = 'fy'
	at_fy.group = 'Non-linear'
	at_fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fy')+'<br/>') + 
		html_par('Yield strength of the steel material of the yielding finger') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	at_fy.dimension = u.F/u.L**2
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Non-linear'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('Modulus of elasticity of the steel material of the yielding finger') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# L
	at_L = MpcAttributeMetaData()
	at_L.type = MpcAttributeType.QuantityScalar
	at_L.name = 'L'
	at_L.group = 'Non-linear'
	at_L.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('L')+'<br/>') + 
		html_par('Height of an individual yielding finger') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	at_L.dimension = u.L
	
	# b
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.Real
	at_b.name = 'b'
	at_b.group = 'Non-linear'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b')+'<br/>') + 
		html_par('Strain hardening ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	
	# Ro
	at_Ro = MpcAttributeMetaData()
	at_Ro.type = MpcAttributeType.Real
	at_Ro.name = 'Ro'
	at_Ro.group = 'Bauschinger effect'
	at_Ro.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ro')+'<br/>') + 
		html_par('Parameter that controls the Bauschinger effect. Recommended Values for Ro=between 10 to 30') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	
	# cR1
	at_cR1 = MpcAttributeMetaData()
	at_cR1.type = MpcAttributeType.Real
	at_cR1.name = 'cR1'
	at_cR1.group = 'Bauschinger effect'
	at_cR1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cR1')+'<br/>') + 
		html_par('Parameter that controls the Bauschinger effect. Recommended Value cR1=0.925') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	
	# cR2
	at_cR2 = MpcAttributeMetaData()
	at_cR2.type = MpcAttributeType.Real
	at_cR2.name = 'cR2'
	at_cR2.group = 'Bauschinger effect'
	at_cR2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cR2')+'<br/>') + 
		html_par('Parameter that controls the Bauschinger effect. Recommended Value cR2=0.150') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
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
		html_par('isotropic hardening parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
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
		html_par('isotropic hardening parameter, increase of compression yield envelope as proportion of yield strength after a plastic deformation of a2*(Pp/Kp)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
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
		html_par('isotropic hardening parameter (see explanation under a1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
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
		html_par('isotropic hardening parameter, increase of tension yield envelope as proportion of yield strength after a plastic deformation of a4*(Pp/Kp)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
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
		html_par('isotropic hardening parameter (see explanation under a3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CastFuse_Material','CastFuse Material')+'<br/>') +
		html_end()
		)
	at_a4.setDefault(1.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Cast'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_n)
	xom.addAttribute(at_bo)
	xom.addAttribute(at_h)
	xom.addAttribute(at_fy)
	xom.addAttribute(at_E)
	xom.addAttribute(at_L)
	xom.addAttribute(at_b)
	xom.addAttribute(at_Ro)
	xom.addAttribute(at_cR1)
	xom.addAttribute(at_cR2)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_a1)
	xom.addAttribute(at_a2)
	xom.addAttribute(at_a3)
	xom.addAttribute(at_a4)
	
	# use_Optional-dep
	xom.setVisibilityDependency(at_Optional, at_a1)
	xom.setVisibilityDependency(at_Optional, at_a2)
	xom.setVisibilityDependency(at_Optional, at_a3)
	xom.setVisibilityDependency(at_Optional, at_a4)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Cast $matTag $n $bo $h $fy $E $L $b $Ro $cR1 $cR2 <$a1 $a2 $a3 $a4>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	n_at = xobj.getAttribute('n')
	if(n_at is None):
		raise Exception('Error: cannot find "n" attribute')
	n = n_at.integer
	
	bo_at = xobj.getAttribute('bo')
	if(bo_at is None):
		raise Exception('Error: cannot find "bo" attribute')
	bo = bo_at.quantityScalar
	
	h_at = xobj.getAttribute('h')
	if(h_at is None):
		raise Exception('Error: cannot find "h" attribute')
	h = h_at.quantityScalar
	
	fy_at = xobj.getAttribute('fy')
	if(fy_at is None):
		raise Exception('Error: cannot find "fy" attribute')
	fy = fy_at.quantityScalar
	
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar
	
	L_at = xobj.getAttribute('L')
	if(L_at is None):
		raise Exception('Error: cannot find "L" attribute')
	L = L_at.quantityScalar
	
	b_at = xobj.getAttribute('b')
	if(b_at is None):
		raise Exception('Error: cannot find "b" attribute')
	b = b_at.real
	
	Ro_at = xobj.getAttribute('Ro')
	if(Ro_at is None):
		raise Exception('Error: cannot find "Ro" attribute')
	Ro = Ro_at.real
	
	cR1_at = xobj.getAttribute('cR1')
	if(cR1_at is None):
		raise Exception('Error: cannot find "cR1" attribute')
	cR1 = cR1_at.real
	
	cR2_at = xobj.getAttribute('cR2')
	if(cR2_at is None):
		raise Exception('Error: cannot find "cR2" attribute')
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
		
		sopt += '{} {} {} {}'.format(a1, a2, a3, a4)
	
	
	str_tcl = '{}uniaxialMaterial Cast {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, n, bo.value, h.value, fy.value, E.value, L.value, b, Ro, cR1, cR2, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)