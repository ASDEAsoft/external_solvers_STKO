# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fcc
	at_fcc = MpcAttributeMetaData()
	at_fcc.type = MpcAttributeType.QuantityScalar
	at_fcc.name = 'fcc'
	at_fcc.group = 'Non-linear'
	at_fcc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fcc')+'<br/>') + 
		html_par('concrete compressive strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	at_fcc.dimension = u.F/u.L**2
	
	# -fct
	at_use_fct = MpcAttributeMetaData()
	at_use_fct.type = MpcAttributeType.Boolean
	at_use_fct.name = '-fct'
	at_use_fct.group = 'Non-linear'
	at_use_fct.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-fct')+'<br/>') + 
		html_par('optional concrete tensile strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# fct
	at_fct = MpcAttributeMetaData()
	at_fct.type = MpcAttributeType.QuantityScalar
	at_fct.name = 'fct'
	at_fct.group = '-fct'
	at_fct.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fct')+'<br/>') + 
		html_par('optional concrete tensile strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	at_fct.dimension = u.F/u.L**2
	
	# -E
	at_use_E = MpcAttributeMetaData()
	at_use_E.type = MpcAttributeType.Boolean
	at_use_E.name = '-E'
	at_use_E.group = 'Non-linear'
	at_use_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-E')+'<br/>') + 
		html_par('optional concrete tensile strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = '-E'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('optional concrete tensile strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# -ni
	at_use_ni = MpcAttributeMetaData()
	at_use_ni.type = MpcAttributeType.Boolean
	at_use_ni.name = '-ni'
	at_use_ni.group = 'Non-linear'
	at_use_ni.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-ni')+'<br/>') + 
		html_par('optional Poisson coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# ni
	at_ni = MpcAttributeMetaData()
	at_ni.type = MpcAttributeType.Real
	at_ni.name = 'ni'
	at_ni.group = '-ni'
	at_ni.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ni')+'<br/>') + 
		html_par('optional Poisson coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# -Gt
	at_use_Gt = MpcAttributeMetaData()
	at_use_Gt.type = MpcAttributeType.Boolean
	at_use_Gt.name = '-Gt'
	at_use_Gt.group = 'Non-linear'
	at_use_Gt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-Gt')+'<br/>') + 
		html_par('optional tension fracture energy density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# Gt
	at_Gt = MpcAttributeMetaData()
	at_Gt.type = MpcAttributeType.QuantityScalar
	at_Gt.name = 'Gt'
	at_Gt.group = '-Gt'
	at_Gt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Gt')+'<br/>') + 
		html_par('optional tension fracture energy density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# -Gc
	at_use_Gc = MpcAttributeMetaData()
	at_use_Gc.type = MpcAttributeType.Boolean
	at_use_Gc.name = '-Gc'
	at_use_Gc.group = 'Non-linear'
	at_use_Gc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-Gc')+'<br/>') + 
		html_par('optional compression fracture energy density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# Gc
	at_Gc = MpcAttributeMetaData()
	at_Gc.type = MpcAttributeType.QuantityScalar
	at_Gc.name = 'Gc'
	at_Gc.group = '-Gc'
	at_Gc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Gc')+'<br/>') + 
		html_par('optional compression fracture energy density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# -rho_bar
	at_use_rho_bar = MpcAttributeMetaData()
	at_use_rho_bar.type = MpcAttributeType.Boolean
	at_use_rho_bar.name = '-rho_bar'
	at_use_rho_bar.group = 'Non-linear'
	at_use_rho_bar.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-rho_bar')+'<br/>') + 
		html_par('optional parameter of plastic volume change') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# rho_bar
	at_rho_bar = MpcAttributeMetaData()
	at_rho_bar.type = MpcAttributeType.Real
	at_rho_bar.name = 'rho_bar'
	at_rho_bar.group = '-rho_bar'
	at_rho_bar.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho_bar')+'<br/>') + 
		html_par('optional parameter of plastic volume change') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# -H
	at_use_H = MpcAttributeMetaData()
	at_use_H.type = MpcAttributeType.Boolean
	at_use_H.name = '-H'
	at_use_H.group = 'Non-linear'
	at_use_H.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-H')+'<br/>') + 
		html_par('optional linear hardening parameter for plasticity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# H
	at_H = MpcAttributeMetaData()
	at_H.type = MpcAttributeType.Real
	at_H.name = 'H'
	at_H.group = '-H'
	at_H.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('H')+'<br/>') + 
		html_par('optional linear hardening parameter for plasticity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# -theta
	at_use_theta = MpcAttributeMetaData()
	at_use_theta.type = MpcAttributeType.Boolean
	at_use_theta.name = '-theta'
	at_use_theta.group = 'Non-linear'
	at_use_theta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-theta')+'<br/>') + 
		html_par('optional ratio between isotropic and kinematic hardening') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# theta
	at_theta = MpcAttributeMetaData()
	at_theta.type = MpcAttributeType.Real
	at_theta.name = 'theta'
	at_theta.group = '-theta'
	at_theta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theta')+'<br/>') + 
		html_par('optional ratio between isotropic and kinematic hardening') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# -tangent
	at_use_tangent = MpcAttributeMetaData()
	at_use_tangent.type = MpcAttributeType.Boolean
	at_use_tangent.name = '-tangent'
	at_use_tangent.group = 'Non-linear'
	at_use_tangent.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-tangent')+'<br/>') + 
		html_par('optional integer to choose the computational stiffness matrix') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	# tangent
	at_tangent = MpcAttributeMetaData()
	at_tangent.type = MpcAttributeType.Integer
	at_tangent.name = 'tangent'
	at_tangent.group = '-tangent'
	at_tangent.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tangent')+'<br/>') + 
		html_par('optional integer to choose the computational stiffness matrix') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Damage2p','Damage2p Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Damage2p'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_fcc)
	xom.addAttribute(at_use_fct)
	xom.addAttribute(at_fct)
	xom.addAttribute(at_use_E)
	xom.addAttribute(at_E)
	xom.addAttribute(at_use_ni)
	xom.addAttribute(at_ni)
	xom.addAttribute(at_use_Gt)
	xom.addAttribute(at_Gt)
	xom.addAttribute(at_use_Gc)
	xom.addAttribute(at_Gc)
	xom.addAttribute(at_use_rho_bar)
	xom.addAttribute(at_rho_bar)
	xom.addAttribute(at_use_H)
	xom.addAttribute(at_H)
	xom.addAttribute(at_use_theta)
	xom.addAttribute(at_theta)
	xom.addAttribute(at_use_tangent)
	xom.addAttribute(at_tangent)
	
	# use_fct-dep
	xom.setVisibilityDependency(at_use_fct, at_fct)
	
	# use_E-dep
	xom.setVisibilityDependency(at_use_E, at_E)
	
	# use_ni-dep
	xom.setVisibilityDependency(at_use_ni, at_ni)
	
	# use_Gt-dep
	xom.setVisibilityDependency(at_use_Gt, at_Gt)
	
	# use_Gc-dep
	xom.setVisibilityDependency(at_use_Gc, at_Gc)
	
	# use_rho_bar-dep
	xom.setVisibilityDependency(at_use_rho_bar, at_rho_bar)
	
	# use_H-dep
	xom.setVisibilityDependency(at_use_H, at_H)
	
	# use_theta-dep
	xom.setVisibilityDependency(at_use_theta, at_theta)
	
	# use_tangent-dep
	xom.setVisibilityDependency(at_use_tangent, at_tangent)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial Damage2p $matTag $fcc <-fct $fct> <-E $E> <-ni $ni> <-Gt $Gt>
	# <-Gc $Gc> <-rho_bar $rho_bar> <-H $H> <-theta $theta> <-tangent $tangent>
	xobj = pinfo.phys_prop.XObject
	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fcc_at = xobj.getAttribute('fcc')
	if(fcc_at is None):
		raise Exception('Error: cannot find "fcc" attribute')
	fcc = fcc_at.quantityScalar
	
	# optional paramters
	sopt = ''
	
	use_fct_at = xobj.getAttribute('-fct')
	if(use_fct_at is None):
		raise Exception('Error: cannot find "-fct" attribute')
	use_fct = use_fct_at.boolean
	if use_fct:
		fct_at = xobj.getAttribute('fct')
		if(fct_at is None):
			raise Exception('Error: cannot find "fct" attribute')
		fct = fct_at.quantityScalar
		
		sopt += '{}'.format(fct.value)
	
	use_E_at = xobj.getAttribute('-E')
	if(use_E_at is None):
		raise Exception('Error: cannot find "-E" attribute')
	use_E = use_E_at.boolean
	if use_E:
		E_at = xobj.getAttribute('E')
		if(E_at is None):
			raise Exception('Error: cannot find "E" attribute')
		E = E_at.quantityScalar
		
		sopt += ' {}'.format(E.value)
	
	use_ni_at = xobj.getAttribute('-ni')
	if(use_ni_at is None):
		raise Exception('Error: cannot find "-ni" attribute')
	use_ni = use_ni_at.boolean
	if use_ni:
		ni_at = xobj.getAttribute('ni')
		if(ni_at is None):
			raise Exception('Error: cannot find "ni" attribute')
		ni = ni_at.real
		
		sopt += ' {}'.format(ni)
	
	use_Gt_at = xobj.getAttribute('-Gt')
	if(use_Gt_at is None):
		raise Exception('Error: cannot find "-Gt" attribute')
	use_Gt = use_Gt_at.boolean
	if use_Gt:
		Gt_at = xobj.getAttribute('Gt')
		if(Gt_at is None):
			raise Exception('Error: cannot find "Gt" attribute')
		Gt = Gt_at.quantityScalar
		
		sopt += ' {}'.format(Gt.value)
	
	use_Gc_at = xobj.getAttribute('-Gc')
	if(use_Gc_at is None):
		raise Exception('Error: cannot find "-Gc" attribute')
	use_Gc = use_Gc_at.boolean
	if use_Gc:
		Gc_at = xobj.getAttribute('Gc')
		if(Gc_at is None):
			raise Exception('Error: cannot find "Gc" attribute')
		Gc = Gc_at.quantityScalar
		
		sopt += ' {}'.format(Gc.value)
	
	use_rho_bar_at = xobj.getAttribute('-rho_bar')
	if(use_rho_bar_at is None):
		raise Exception('Error: cannot find "-rho_bar" attribute')
	use_rho_bar = use_rho_bar_at.boolean
	if use_rho_bar:
		rho_bar_at = xobj.getAttribute('rho_bar')
		if(rho_bar_at is None):
			raise Exception('Error: cannot find "rho_bar" attribute')
		rho_bar = rho_bar_at.real
		
		sopt += ' {}'.format(rho_bar)
	
	use_H_at = xobj.getAttribute('-H')
	if(use_H_at is None):
		raise Exception('Error: cannot find "-H" attribute')
	use_H = use_H_at.boolean
	if use_H:
		H_at = xobj.getAttribute('H')
		if(H_at is None):
			raise Exception('Error: cannot find "H" attribute')
		H = H_at.real
		
		sopt += ' {}'.format(H)
	
	use_theta_at = xobj.getAttribute('-theta')
	if(use_theta_at is None):
		raise Exception('Error: cannot find "-theta" attribute')
	use_theta = use_theta_at.boolean
	if use_theta:
		theta_at = xobj.getAttribute('theta')
		if(theta_at is None):
			raise Exception('Error: cannot find "theta" attribute')
		theta = theta_at.real
		
		sopt += ' {}'.format(theta)
	
	use_tangent_at = xobj.getAttribute('-tangent')
	if(use_tangent_at is None):
		raise Exception('Error: cannot find "-tangent" attribute')
	use_tangent = use_tangent_at.boolean
	if use_tangent:
		tangent_at = xobj.getAttribute('tangent')
		if(tangent_at is None):
			raise Exception('Error: cannot find "tangent" attribute')
		tangent = tangent_at.integer
		
		sopt += ' {}'.format(tangent)
	
	str_tcl = '{}nDMaterial Damage2p {} {} {}\n'.format(pinfo.indent, tag, fcc.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)