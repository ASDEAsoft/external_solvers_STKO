# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# k
	at_k = MpcAttributeMetaData()
	at_k.type = MpcAttributeType.QuantityScalar
	at_k.name = 'k'
	at_k.group = 'Elasticity'
	at_k.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k')+'<br/>') + 
		html_par('bulk modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	at_k.dimension = u.F/u.L**2
	
	# G
	at_G = MpcAttributeMetaData()
	at_G.type = MpcAttributeType.QuantityScalar
	at_G.name = 'G'
	at_G.group = 'Elasticity'
	at_G.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('G')+'<br/>') + 
		html_par('shaer modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	at_G.dimension = u.F/u.L**2
	
	# sigmaY
	at_sigmaY = MpcAttributeMetaData()
	at_sigmaY.type = MpcAttributeType.QuantityScalar
	at_sigmaY.name = 'sigmaY'
	at_sigmaY.group = 'Non-linear'
	at_sigmaY.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sigmaY')+'<br/>') + 
		html_par('yield stress') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	at_sigmaY.dimension = u.F/u.L**2
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.Real
	at_rho.name = 'rho'
	at_rho.group = 'Non-linear'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('frictional strength parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	
	# rhoBar
	at_rhoBar = MpcAttributeMetaData()
	at_rhoBar.type = MpcAttributeType.Real
	at_rhoBar.name = 'rhoBar'
	at_rhoBar.group = 'Non-linear'
	at_rhoBar.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rhoBar')+'<br/>') + 
		html_par('controls evolution of plastic volume change, 0 ≤ rhoBar ≤ rho') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	
	# Kinf
	at_Kinf = MpcAttributeMetaData()
	at_Kinf.type = MpcAttributeType.QuantityScalar
	at_Kinf.name = 'Kinf'
	at_Kinf.group = 'Non-linear'
	at_Kinf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kinf')+'<br/>') + 
		html_par('nonlinear isotropic strain hardening parameter, Kinf ≥ 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	at_Kinf.dimension = u.F/u.L**2
	
	# Ko
	at_Ko = MpcAttributeMetaData()
	at_Ko.type = MpcAttributeType.QuantityScalar
	at_Ko.name = 'Ko'
	at_Ko.group = 'Non-linear'
	at_Ko.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ko')+'<br/>') + 
		html_par('nonlinear isotropic strain hardening parameter, Ko ≥ 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	at_Ko.dimension = u.F/u.L**2
	
	# delta1
	at_delta1 = MpcAttributeMetaData()
	at_delta1.type = MpcAttributeType.Real
	at_delta1.name = 'delta1'
	at_delta1.group = 'Non-linear'
	at_delta1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('delta1')+'<br/>') + 
		html_par('nonlinear isotropic strain hardening parameter, delta1 ≥ 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	
	# delta2
	at_delta2 = MpcAttributeMetaData()
	at_delta2.type = MpcAttributeType.Real
	at_delta2.name = 'delta2'
	at_delta2.group = 'Non-linear'
	at_delta2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('delta2')+'<br/>') + 
		html_par('tension softening parameter, delta2 ≥ 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	
	# H
	at_H = MpcAttributeMetaData()
	at_H.type = MpcAttributeType.Real
	at_H.name = 'H'
	at_H.group = 'Non-linear'
	at_H.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('H')+'<br/>') + 
		html_par('linear strain hardening parameter, H ≥ 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	
	# theta
	at_theta = MpcAttributeMetaData()
	at_theta.type = MpcAttributeType.Real
	at_theta.name = 'theta'
	at_theta.group = 'Non-linear'
	at_theta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theta')+'<br/>') + 
		html_par('controls relative proportions of isotropic and kinematic hardening, 0 ≤ theta ≤ 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	
	# density
	at_density = MpcAttributeMetaData()
	at_density.type = MpcAttributeType.QuantityScalar
	at_density.name = 'density'
	at_density.group = 'Non-linear'
	at_density.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('density')+'<br/>') + 
		html_par('mass density of the material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	#at_density.dimension = u.M/u.L**3
	
	# use_atmPressure
	at_use_atmPressure = MpcAttributeMetaData()
	at_use_atmPressure.type = MpcAttributeType.Boolean
	at_use_atmPressure.name = 'use_atmPressure'
	at_use_atmPressure.group = 'Non-linear'
	at_use_atmPressure.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_atmPressure')+'<br/>') + 
		html_par('optional atmospheric pressure for update of elastic bulk and shear moduli (default = 101 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	
	# atmPressure
	at_atmPressure = MpcAttributeMetaData()
	at_atmPressure.type = MpcAttributeType.QuantityScalar
	at_atmPressure.name = 'atmPressure'
	at_atmPressure.group = 'Optional parameter'
	at_atmPressure.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('atmPressure')+'<br/>') + 
		html_par('optional atmospheric pressure for update of elastic bulk and shear moduli (default = 101 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Drucker_Prager','Drucker Prager')+'<br/>') +
		html_end()
		)
	at_atmPressure.setDefault(101)
	at_atmPressure.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'DruckerPrager'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_k)
	xom.addAttribute(at_G)
	xom.addAttribute(at_sigmaY)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_rhoBar)
	xom.addAttribute(at_Kinf)
	xom.addAttribute(at_Ko)
	xom.addAttribute(at_delta1)
	xom.addAttribute(at_delta2)
	xom.addAttribute(at_H)
	xom.addAttribute(at_theta)
	xom.addAttribute(at_density)
	xom.addAttribute(at_use_atmPressure)
	xom.addAttribute(at_atmPressure)
	
	# use_atmPressure-dep
	xom.setVisibilityDependency(at_use_atmPressure, at_atmPressure)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial DruckerPrager $matTag $k $G $sigmaY $rho $rhoBar $Kinf $Ko $delta1 $delta2 $H $theta $density <$atmPressure>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	k_at = xobj.getAttribute('k')
	if(k_at is None):
		raise Exception('Error: cannot find "k" attribute')
	k = k_at.quantityScalar
	
	G_at = xobj.getAttribute('G')
	if(G_at is None):
		raise Exception('Error: cannot find "G" attribute')
	G = G_at.quantityScalar
	
	sigmaY_at = xobj.getAttribute('sigmaY')
	if(sigmaY_at is None):
		raise Exception('Error: cannot find "sigmaY" attribute')
	sigmaY = sigmaY_at.quantityScalar
	
	rho_at = xobj.getAttribute('rho')
	if(rho_at is None):
		raise Exception('Error: cannot find "rho" attribute')
	rho = rho_at.real
	
	rhoBar_at = xobj.getAttribute('rhoBar')
	if(rhoBar_at is None):
		raise Exception('Error: cannot find "rhoBar" attribute')
	rhoBar = rhoBar_at.real
	
	Kinf_at = xobj.getAttribute('Kinf')
	if(Kinf_at is None):
		raise Exception('Error: cannot find "Kinf" attribute')
	Kinf = Kinf_at.quantityScalar
	
	Ko_at = xobj.getAttribute('Ko')
	if(Ko_at is None):
		raise Exception('Error: cannot find "Ko" attribute')
	Ko = Ko_at.quantityScalar
	
	delta1_at = xobj.getAttribute('delta1')
	if(delta1_at is None):
		raise Exception('Error: cannot find "delta1" attribute')
	delta1 = delta1_at.real
	
	delta2_at = xobj.getAttribute('delta2')
	if(delta2_at is None):
		raise Exception('Error: cannot find "delta2" attribute')
	delta2 = delta2_at.real
	
	H_at = xobj.getAttribute('H')
	if(H_at is None):
		raise Exception('Error: cannot find "H" attribute')
	H = H_at.real
	
	theta_at = xobj.getAttribute('theta')
	if(theta_at is None):
		raise Exception('Error: cannot find "theta" attribute')
	theta = theta_at.real
	
	density_at = xobj.getAttribute('density')
	if(density_at is None):
		raise Exception('Error: cannot find "density" attribute')
	density = density_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	use_atmPressure_at = xobj.getAttribute('use_atmPressure')
	if(use_atmPressure_at is None):
		raise Exception('Error: cannot find "use_atmPressure" attribute')
	use_atmPressure = use_atmPressure_at.boolean
	if use_atmPressure:
		atmPressure_at = xobj.getAttribute('atmPressure')
		if(atmPressure_at is None):
			raise Exception('Error: cannot find "atmPressure" attribute')
		atmPressure = atmPressure_at.quantityScalar
		
		sopt += ' {}'.format(atmPressure.value)
	
	
	str_tcl = '{}nDMaterial DruckerPrager {} {} {} {} {} {} {} {} {} {} {} {} {}{}\n'.format(
			pinfo.indent, tag, k.value, G.value, sigmaY.value, rho, rhoBar, Kinf.value, Ko.value, delta1, delta2, H, theta, density.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)