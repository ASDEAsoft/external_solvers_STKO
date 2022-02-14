# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# s1p
	at_s1p = MpcAttributeMetaData()
	at_s1p.type = MpcAttributeType.QuantityScalar
	at_s1p.name = 's1p'
	at_s1p.group = 'Non-linear'
	at_s1p.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('s1p')+'<br/>') + 
		html_par('stress (or force) at first point of the envelope in the positive direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	at_s1p.dimension = u.F/u.L**2
	
	# e1p
	at_e1p = MpcAttributeMetaData()
	at_e1p.type = MpcAttributeType.Real
	at_e1p.name = 'e1p'
	at_e1p.group = 'Non-linear'
	at_e1p.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e1p')+'<br/>') + 
		html_par('strain (deformation) at first point of the envelope in the positive direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# s2p
	at_s2p = MpcAttributeMetaData()
	at_s2p.type = MpcAttributeType.QuantityScalar
	at_s2p.name = 's2p'
	at_s2p.group = 'Non-linear'
	at_s2p.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('s2p')+'<br/>') + 
		html_par('stress (or force) at second point of the envelope in the positive direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	at_s2p.dimension = u.F/u.L**2
	
	# e2p
	at_e2p = MpcAttributeMetaData()
	at_e2p.type = MpcAttributeType.Real
	at_e2p.name = 'e2p'
	at_e2p.group = 'Non-linear'
	at_e2p.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e2p')+'<br/>') + 
		html_par('strain (deformation) at second point of the envelope in the positive direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# Optional_1
	at_Optional_1 = MpcAttributeMetaData()
	at_Optional_1.type = MpcAttributeType.Boolean
	at_Optional_1.name = 'Optional_1'
	at_Optional_1.group = 'Non-linear'
	at_Optional_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional_1')+'<br/>') + 
		html_par('to activate s3p, e3p, s3n, e3n') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# s3p
	at_s3p = MpcAttributeMetaData()
	at_s3p.type = MpcAttributeType.QuantityScalar
	at_s3p.name = 's3p'
	at_s3p.group = 'Optional parameters'
	at_s3p.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('s3p')+'<br/>') + 
		html_par('stress (or force) at third point of the envelope in the positive direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	at_s3p.dimension = u.F/u.L**2
	
	# e3p
	at_e3p = MpcAttributeMetaData()
	at_e3p.type = MpcAttributeType.Real
	at_e3p.name = 'e3p'
	at_e3p.group = 'Optional parameters'
	at_e3p.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e3p')+'<br/>') + 
		html_par('strain (deformation) at third point of the envelope in the positive direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# s1n
	at_s1n = MpcAttributeMetaData()
	at_s1n.type = MpcAttributeType.QuantityScalar
	at_s1n.name = 's1n'
	at_s1n.group = 'Non-linear'
	at_s1n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('s1n')+'<br/>') + 
		html_par('stress (or force) at first point of the envelope in the negative direction*') +
		html_par('* negative backbone points should be entered as negative numeric values') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	at_s1n.dimension = u.F/u.L**2
	
	# e1n
	at_e1n = MpcAttributeMetaData()
	at_e1n.type = MpcAttributeType.Real
	at_e1n.name = 'e1n'
	at_e1n.group = 'Non-linear'
	at_e1n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e1n')+'<br/>') + 
		html_par('strain (deformation) at third point of the envelope in the positive direction') +
		html_par('* negative backbone points should be entered as negative numeric values') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# s2n
	at_s2n = MpcAttributeMetaData()
	at_s2n.type = MpcAttributeType.QuantityScalar
	at_s2n.name = 's2n'
	at_s2n.group = 'Non-linear'
	at_s2n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('s2n')+'<br/>') + 
		html_par('stress (or force) at second point of the envelope in the negative direction*') +
		html_par('* negative backbone points should be entered as negative numeric values') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	at_s2n.dimension = u.F/u.L**2
	
	# e2n
	at_e2n = MpcAttributeMetaData()
	at_e2n.type = MpcAttributeType.Real
	at_e2n.name = 'e2n'
	at_e2n.group = 'Non-linear'
	at_e2n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e2n')+'<br/>') + 
		html_par('strain (deformation) at third point of the envelope in the positive direction') +
		html_par('* negative backbone points should be entered as negative numeric values') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# s3n
	at_s3n = MpcAttributeMetaData()
	at_s3n.type = MpcAttributeType.QuantityScalar
	at_s3n.name = 's3n'
	at_s3n.group = 'Optional parameters'
	at_s3n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('s3n')+'<br/>') + 
		html_par('stress (or force) at third point of the envelope in the negative direction*') +
		html_par('* negative backbone points should be entered as negative numeric values') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	at_s3n.dimension = u.F/u.L**2
	
	# e3n
	at_e3n = MpcAttributeMetaData()
	at_e3n.type = MpcAttributeType.Real
	at_e3n.name = 'e3n'
	at_e3n.group = 'Optional parameters'
	at_e3n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e3n')+'<br/>') + 
		html_par('strain (deformation) at third point of the envelope in the positive direction') +
		html_par('* negative backbone points should be entered as negative numeric values') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# pinchX
	at_pinchX = MpcAttributeMetaData()
	at_pinchX.type = MpcAttributeType.Real
	at_pinchX.name = 'pinchX'
	at_pinchX.group = 'Non-linear'
	at_pinchX.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pinchX')+'<br/>') + 
		html_par('pinching factor for strain (or deformation) during reloading') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# pinchY
	at_pinchY = MpcAttributeMetaData()
	at_pinchY.type = MpcAttributeType.Real
	at_pinchY.name = 'pinchY'
	at_pinchY.group = 'Non-linear'
	at_pinchY.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pinchY')+'<br/>') + 
		html_par('pinching factor for stress (or force) during reloading') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# damage1
	at_damage1 = MpcAttributeMetaData()
	at_damage1.type = MpcAttributeType.Real
	at_damage1.name = 'damage1'
	at_damage1.group = 'Non-linear'
	at_damage1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('damage1')+'<br/>') + 
		html_par('damage due to ductility: D1(m-1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# damage2
	at_damage2 = MpcAttributeMetaData()
	at_damage2.type = MpcAttributeType.Real
	at_damage2.name = 'damage2'
	at_damage2.group = 'Non-linear'
	at_damage2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('damage2')+'<br/>') + 
		html_par('damage due to energy: D2(Ei/Eult)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# use_beta
	at_use_beta = MpcAttributeMetaData()
	at_use_beta.type = MpcAttributeType.Boolean
	at_use_beta.name = 'use_beta'
	at_use_beta.group = 'Non-linear'
	at_use_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_beta')+'<br/>') + 
		html_par('power used to determine the degraded unloading stiffness based on ductility, m-b (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'Optional parameters'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') + 
		html_par('power used to determine the degraded unloading stiffness based on ductility, m-b (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	at_beta.setDefault(0.0)
	
	# Optional_2
	at_Optional_2 = MpcAttributeMetaData()
	at_Optional_2.type = MpcAttributeType.Boolean
	at_Optional_2.name = 'Optional_2'
	at_Optional_2.group = 'Non-linear'
	at_Optional_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional_2')+'<br/>') + 
		html_par('to activate curveTag, curveType, degrade') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# curveTag
	at_curveTag = MpcAttributeMetaData()
	at_curveTag.type = MpcAttributeType.Index
	at_curveTag.name = 'curveTag'
	at_curveTag.group = 'Optional parameters'
	at_curveTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('curveTag')+'<br/>') + 
		html_par('an integer tag for the ' + html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_Curve','Limit Curve')+ ' defining the limit surface' + '<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# curveType
	at_curveType = MpcAttributeMetaData()
	at_curveType.type = MpcAttributeType.Integer
	at_curveType.name = 'curveType'
	at_curveType.group = 'Optional parameters'
	at_curveType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('curveType')+'<br/>') + 
		html_par('an integer defining the type of LimitCurve (0 = no curve, 1 = axial curve, all other curves can be any other integer)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	
	# degrade
	at_degrade = MpcAttributeMetaData()
	at_degrade.type = MpcAttributeType.Integer
	at_degrade.name = 'degrade'
	at_degrade.group = 'Optional parameters'
	at_degrade.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('degrade')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Limit_State_Material','Limit State Material')+'<br/>') +
		html_end()
		)
	at_degrade.setDefault(0)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'LimitState'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_s1p)
	xom.addAttribute(at_e1p)
	xom.addAttribute(at_s2p)
	xom.addAttribute(at_e2p)
	xom.addAttribute(at_Optional_1)
	xom.addAttribute(at_s3p)
	xom.addAttribute(at_e3p)
	xom.addAttribute(at_s1n)
	xom.addAttribute(at_e1n)
	xom.addAttribute(at_s2n)
	xom.addAttribute(at_e2n)
	xom.addAttribute(at_s3n)
	xom.addAttribute(at_e3n)
	xom.addAttribute(at_pinchX)
	xom.addAttribute(at_pinchY)
	xom.addAttribute(at_damage1)
	xom.addAttribute(at_damage2)
	xom.addAttribute(at_use_beta)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_Optional_2)
	xom.addAttribute(at_curveTag)
	xom.addAttribute(at_curveType)
	xom.addAttribute(at_degrade)
	
	# Optional_1-dep
	xom.setVisibilityDependency(at_Optional_1, at_s3p)
	xom.setVisibilityDependency(at_Optional_1, at_e3p)
	xom.setVisibilityDependency(at_Optional_1, at_s3n)
	xom.setVisibilityDependency(at_Optional_1, at_e3n)
	
	# beta-dep
	xom.setVisibilityDependency(at_use_beta, at_beta)
	
	# Optional_2-dep
	xom.setVisibilityDependency(at_Optional_2, at_curveTag)
	xom.setVisibilityDependency(at_Optional_2, at_curveType)
	xom.setVisibilityDependency(at_Optional_2, at_degrade)
	
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial LimitState $matTag $s1p $e1p $s2p $e2p $s3p $e3p $s1n $e1n
	#$s2n $e2n $s3n $e3n $pinchX $pinchY $damage1 $damage2 $beta $curveTag $curveType.
	
	'''
	#uniaxialMaterial LimitState $matTag $s1p $e1p $s2p $e2p <$s3p $e3p> $s1n $e1n $s2n $e2n
	#<$s3n $e3n> $pinchX $pinchY $damage1 $damage2 <$beta> <$curveTag $curveType $degrade>
	'''
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	s1p_at = xobj.getAttribute('s1p')
	if(s1p_at is None):
		raise Exception('Error: cannot find "s1p" attribute')
	s1p = s1p_at.quantityScalar
	
	e1p_at = xobj.getAttribute('e1p')
	if(e1p_at is None):
		raise Exception('Error: cannot find "e1p" attribute')
	e1p = e1p_at.real
	
	s2p_at = xobj.getAttribute('s2p')
	if(s2p_at is None):
		raise Exception('Error: cannot find "s2p" attribute')
	s2p = s2p_at.quantityScalar
	
	e2p_at = xobj.getAttribute('e2p')
	if(e2p_at is None):
		raise Exception('Error: cannot find "e2p" attribute')
	e2p = e2p_at.real
	
	# optional paramters
	sopt1 = ''
	sopt2 = ''
	
	Optional_1_at = xobj.getAttribute('Optional_1')
	if(Optional_1_at is None):
		raise Exception('Error: cannot find "Optional_1" attribute')
	Optional_1 = Optional_1_at.boolean
	if Optional_1:
		s3p_at = xobj.getAttribute('s3p')
		if(s3p_at is None):
			raise Exception('Error: cannot find "s3p" attribute')
		s3p = s3p_at.quantityScalar
		
		e3p_at = xobj.getAttribute('e3p')
		if(e3p_at is None):
			raise Exception('Error: cannot find "e3p" attribute')
		e3p = e3p_at.real
		
		s3n_at = xobj.getAttribute('s3n')
		if(s3n_at is None):
			raise Exception('Error: cannot find "s3n" attribute')
		s3n = s3n_at.quantityScalar
		
		e3n_at = xobj.getAttribute('e3n')
		if(e3n_at is None):
			raise Exception('Error: cannot find "e3n" attribute')
		e3n = e3n_at.real
		
		sopt1 += '{} {}'.format(s3p.value, e3p)
		sopt2 += '{} {}'.format(s3n.value, e3n)
		
		
	s1n_at = xobj.getAttribute('s1n')
	if(s1n_at is None):
		raise Exception('Error: cannot find "s1n" attribute')
	s1n = s1n_at.quantityScalar
	
	e1n_at = xobj.getAttribute('e1n')
	if(e1n_at is None):
		raise Exception('Error: cannot find "e1n" attribute')
	e1n = e1n_at.real
	
	s2n_at = xobj.getAttribute('s2n')
	if(s2n_at is None):
		raise Exception('Error: cannot find "s2n" attribute')
	s2n = s2n_at.quantityScalar
	
	e2n_at = xobj.getAttribute('e2n')
	if(e2n_at is None):
		raise Exception('Error: cannot find "e2n" attribute')
	e2n = e2n_at.real
	
	pinchX_at = xobj.getAttribute('pinchX')
	if(pinchX_at is None):
		raise Exception('Error: cannot find "pinchX" attribute')
	pinchX = pinchX_at.real
	
	pinchY_at = xobj.getAttribute('pinchY')
	if(pinchY_at is None):
		raise Exception('Error: cannot find "pinchY" attribute')
	pinchY = pinchY_at.real
	
	damage1_at = xobj.getAttribute('damage1')
	if(damage1_at is None):
		raise Exception('Error: cannot find "damage1" attribute')
	damage1 = damage1_at.real
	
	damage2_at = xobj.getAttribute('damage2')
	if(damage2_at is None):
		raise Exception('Error: cannot find "damage2" attribute')
	damage2 = damage2_at.real
	
	
	# optional paramter
	sopt3 = ''
	
	use_beta_at = xobj.getAttribute('use_beta')
	if(use_beta_at is None):
		raise Exception('Error: cannot find "use_beta" attribute')
	use_beta = use_beta_at.boolean
	if use_beta:
		beta_at = xobj.getAttribute('beta')
		if(beta_at is None):
			raise Exception('Error: cannot find "beta" attribute')
		beta = beta_at.real
		
		sopt3 += '{}'.format(beta)
	
	
	# optional paramters
	sopt4 = ''
	
	Optional_2_at = xobj.getAttribute('Optional_2')
	if(Optional_2_at is None):
		raise Exception('Error: cannot find "Optional_2" attribute')
	Optional_2 = Optional_2_at.boolean
	if Optional_2:
		curveTag_at = xobj.getAttribute('curveTag')
		if(curveTag_at is None):
			raise Exception('Error: cannot find "curveTag" attribute')
		curveTag = curveTag_at.index
		
		curveType_at = xobj.getAttribute('curveType')
		if(curveType_at is None):
			raise Exception('Error: cannot find "curveType" attribute')
		curveType = curveType_at.integer
		
		degrade_at = xobj.getAttribute('degrade')
		if(degrade_at is None):
			raise Exception('Error: cannot find "degrade" attribute')
		degrade = degrade_at.integer
		
		sopt4 += '{} {} {}'.format(curveTag, curveType, degrade)
	
	
	str_tcl = '{}uniaxialMaterial LimitState {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, s1p.value, e1p, s2p.value, e2p, sopt1, s1n.value, e1n, s2n.value, e2n,
			sopt2, pinchX, pinchY, damage1, damage2, sopt3, sopt4)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)