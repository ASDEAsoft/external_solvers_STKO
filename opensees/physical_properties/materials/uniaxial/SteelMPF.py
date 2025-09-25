# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fyp
	at_fyp = MpcAttributeMetaData()
	at_fyp.type = MpcAttributeType.QuantityScalar
	at_fyp.name = 'fyp'
	at_fyp.group = 'Non-linear'
	at_fyp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fyp')+'<br/>') + 
		html_par('Yield strength in tension (positive loading direction)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
		html_end()
		)
	at_fyp.dimension = u.F/u.L**2
	
	# fyn
	at_fyn = MpcAttributeMetaData()
	at_fyn.type = MpcAttributeType.QuantityScalar
	at_fyn.name = 'fyn'
	at_fyn.group = 'Non-linear'
	at_fyn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fyn')+'<br/>') + 
		html_par('Yield strength in compression (negative loading direction)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
		html_end()
		)
	at_fyn.dimension = u.F/u.L**2
	
	# E0
	at_E0 = MpcAttributeMetaData()
	at_E0.type = MpcAttributeType.QuantityScalar
	at_E0.name = 'E0'
	at_E0.group = 'Elasticity'
	at_E0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E0')+'<br/>') + 
		html_par('Initial tangent modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
		html_end()
		)
	at_E0.dimension = u.F/u.L**2
	
	# bp
	at_bp = MpcAttributeMetaData()
	at_bp.type = MpcAttributeType.Real
	at_bp.name = 'bp'
	at_bp.group = 'Non-linear'
	at_bp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bp')+'<br/>') + 
		html_par('Strain hardening ratio in tension (positive loading direction)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
		html_end()
		)
	
	# bn
	at_bn = MpcAttributeMetaData()
	at_bn.type = MpcAttributeType.Real
	at_bn.name = 'bn'
	at_bn.group = 'Non-linear'
	at_bn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bn')+'<br/>') + 
		html_par('Strain hardening ratio in compression (negative loading direction)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
		html_end()
		)
	
	# R0 (to insert curvature unit)
	at_R0 = MpcAttributeMetaData()
	at_R0.type = MpcAttributeType.Real
	at_R0.name = 'R0'
	at_R0.group = 'Non-linear'
	at_R0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R0')+'<br/>') + 
		html_par('Initial value of the curvature parameter R (R0 = 20 recommended)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
		html_end()
		)
	
	# cR1 (to insert curvature unit)
	at_cR1 = MpcAttributeMetaData()
	at_cR1.type = MpcAttributeType.Real
	at_cR1.name = 'cR1'
	at_cR1.group = 'Non-linear'
	at_cR1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cR1')+'<br/>') + 
		html_par('Curvature degradation parameter (a1 = 0.925 recommended)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
		html_end()
		)
	
	# cR2 (to insert curvature unit)
	at_cR2 = MpcAttributeMetaData()
	at_cR2.type = MpcAttributeType.Real
	at_cR2.name = 'cR2'
	at_cR2.group = 'Non-linear'
	at_cR2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cR2')+'<br/>') + 
		html_par('Curvature degradation parameter (a2 = 0.15 or 0.0015 recommended)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
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
		html_par('Isotropic hardening in compression parameter (optional, default = 0.0). Shifts compression yield envelope by a proportion of compressive yield strength after a maximum plastic tensile strain of $a2($fyp/$E0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
		html_end()
		)
	at_a1.setDefault(0.0)
	
	# a2 
	at_a2 = MpcAttributeMetaData()
	at_a2.type = MpcAttributeType.Real
	at_a2.name = 'a2'
	at_a2.group = 'Optional parameters'
	at_a2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a2')+'<br/>') + 
		html_par('Isotropic hardening in compression parameter (optional, default = 1.0). See explanation of a1.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
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
		html_par('Isotropic hardening in tension parameter (optional, default = 0.0). Shifts tension yield envelope by a proportion of tensile yield strength after a maximum plastic compressive strain of $a3($fyn/$E0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
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
		html_par('sotropic hardening in tension parameter (optional, default = 1.0). See explanation of a3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SteelMPF_-_Menegotto_and_Pinto_(1973)_Model_Extended_by_Filippou_et_al._(1983)','SteelMPF Material')+'<br/>') +
		html_end()
		)
	at_a4.setDefault(1.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'SteelMPF'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(at_fyp)
	xom.addAttribute(at_fyn)
	xom.addAttribute(at_E0)
	xom.addAttribute(at_bp)
	xom.addAttribute(at_bn)
	xom.addAttribute(at_R0)
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
	
	#uniaxialMaterial SteelMPF $mattag $fyp $fyn $E0 $bp $bn $R0 $cR1 $cR2 <$a1 $a2 $a3 $a4>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fyp_at = xobj.getAttribute('fyp')
	if(fyp_at is None):
		raise Exception('Error: cannot find "fyp" attribute')
	fyp = fyp_at.quantityScalar
	
	fyn_at = xobj.getAttribute('fyn')
	if(fyn_at is None):
		raise Exception('Error: cannot find "fyn" attribute')
	fyn = fyn_at.quantityScalar
	
	E0_at = xobj.getAttribute('E0')
	if(E0_at is None):
		raise Exception('Error: cannot find "E0" attribute')
	E0 = E0_at.quantityScalar
	
	bp_at = xobj.getAttribute('bp')
	if(bp_at is None):
		raise Exception('Error: cannot find "bp" attribute')
	bp = bp_at.real
	
	bn_at = xobj.getAttribute('bn')
	if(bn_at is None):
		raise Exception('Error: cannot find "bn" attribute')
	bn = bn_at.real
	
	R0_at = xobj.getAttribute('R0')
	if(R0_at is None):
		raise Exception('Error: cannot find "R0" attribute')
	R0 = R0_at.real
	
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
	
	
	str_tcl = '{}uniaxialMaterial SteelMPF {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fyp.value, fyn.value, E0.value, bp, bn, R0, cR1, cR2, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)