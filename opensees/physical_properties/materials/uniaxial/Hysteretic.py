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
		html_par('stress(or force) at first point of the envelope in the positive direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('stress(or force) at second point of the envelope in the positive direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('stress(or force) at third point of the envelope in the positive direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('stress(or force) at first point of the envelope in the negative direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('strain (deformation) at first point of the envelope in the negative direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('stress(or force) at second point of the envelope in the negative direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('strain (deformation) at second point of the envelope in the negative direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('stress(or force) at third point of the envelope in the negative direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('strain (deformation) at third point of the envelope in the negative direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
		html_end()
		)
		
	# pinchx
	at_pinchx = MpcAttributeMetaData()
	at_pinchx.type = MpcAttributeType.Real
	at_pinchx.name = 'pinchx'
	at_pinchx.group = 'Non-linear'
	at_pinchx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pinchx')+'<br/>') + 
		html_par('pinching factor for strain (or deformation) during reloading') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
		html_end()
		)
	
	# pinchy
	at_pinchy = MpcAttributeMetaData()
	at_pinchy.type = MpcAttributeType.Real
	at_pinchy.name = 'pinchy'
	at_pinchy.group = 'Non-linear'
	at_pinchy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pinchy')+'<br/>') + 
		html_par('pinching factor for stress (or force) during reloading') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('damage due to ductility: D1(mu-1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('damage due to energy: D2(Eii/Eult)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('power used to determine the degraded unloading stiffness based on ductility, mu-beta (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
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
		html_par('power used to determine the degraded unloading stiffness based on ductility, mu-beta (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
		html_end()
		)
	at_beta.setDefault(0.0)
	
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hysteretic_Material','Hysteretic Material')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'Hysteretic'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(at_s1p)
	xom.addAttribute(at_e1p)
	xom.addAttribute(at_s2p)
	xom.addAttribute(at_e2p)
	xom.addAttribute(at_s3p)
	xom.addAttribute(at_e3p)
	xom.addAttribute(at_s1n)
	xom.addAttribute(at_e1n)
	xom.addAttribute(at_s2n)
	xom.addAttribute(at_e2n)
	xom.addAttribute(at_s3n)
	xom.addAttribute(at_e3n)
	xom.addAttribute(at_pinchx)
	xom.addAttribute(at_pinchy)
	xom.addAttribute(at_damage1)
	xom.addAttribute(at_damage2)
	xom.addAttribute(at_use_beta)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_Optional)
	
	#Optional-dep
	xom.setVisibilityDependency(at_Optional, at_s3p)
	xom.setVisibilityDependency(at_Optional, at_e3p)
	xom.setVisibilityDependency(at_Optional, at_s3n)
	xom.setVisibilityDependency(at_Optional, at_e3n)
	
	#beta-dep
	xom.setVisibilityDependency(at_use_beta, at_beta)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Hysteretic $matTag $s1p $e1p $s2p $e2p
	#<$s3p $e3p> $s1n $e1n $s2n $e2n <$s3n $e3n>
	#$pinchX $pinchY $damage1 $damage2 <$beta>
	
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
	
	pinchx_at = xobj.getAttribute('pinchx')
	if(pinchx_at is None):
		raise Exception('Error: cannot find "pinchx" attribute')
	pinchx = pinchx_at.real
	
	pinchy_at = xobj.getAttribute('pinchy')
	if(pinchy_at is None):
		raise Exception('Error: cannot find "pinchy" attribute')
	pinchy = pinchy_at.real
	
	damage1_at = xobj.getAttribute('damage1')
	if(damage1_at is None):
		raise Exception('Error: cannot find "damage1" attribute')
	damage1 = damage1_at.real
	
	damage2_at = xobj.getAttribute('damage2')
	if(damage2_at is None):
		raise Exception('Error: cannot find "damage2" attribute')
	damage2 = damage2_at.real
	
	
	# optional paramters
	sopt1 = ''
	sopt2 = ''
	sopt3 = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		#<$s3p $e3p>
		s3p_at = xobj.getAttribute('s3p')
		if(s3p_at is None):
			raise Exception('Error: cannot find "s3p" attribute')
		s3p = s3p_at.quantityScalar
		
		e3p_at = xobj.getAttribute('e3p')
		if(e3p_at is None):
			raise Exception('Error: cannot find "e3p" attribute')
		e3p = e3p_at.real
		
		sopt1 += '{} {}'.format(s3p.value, e3p)
		
		#<$s3n $e3n>
		s3n_at = xobj.getAttribute('s3n')
		if(s3n_at is None):
			raise Exception('Error: cannot find "s3n" attribute')
		s3n = s3n_at.quantityScalar
		
		e3n_at = xobj.getAttribute('e3n')
		if(e3n_at is None):
			raise Exception('Error: cannot find "e3n" attribute')
		e3n = e3n_at.real
		
		sopt2 += '{} {}'.format(s3n.value, e3n)
	
	#<$beta>
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
	
	
	str_tcl = '{}uniaxialMaterial Hysteretic {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, s1p.value, e1p, s2p.value, e2p, sopt1, s1n.value, e1n, s2n.value, e2n,
			sopt2, pinchx, pinchy, damage1, damage2, sopt3)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)