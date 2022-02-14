# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Elasticity'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('tangent stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hardening_Material','Hardening Material')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# sigmaY
	at_sigmaY = MpcAttributeMetaData()
	at_sigmaY.type = MpcAttributeType.QuantityScalar
	at_sigmaY.name = 'sigmaY'
	at_sigmaY.group = 'Non-linear'
	at_sigmaY.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sigmaY')+'<br/>') + 
		html_par('yield stress or force') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hardening_Material','Hardening Material')+'<br/>') +
		html_end()
		)
	at_sigmaY.dimension = u.F/u.L**2
	
	# H_iso
	at_H_iso = MpcAttributeMetaData()
	at_H_iso.type = MpcAttributeType.Real
	at_H_iso.name = 'H_iso'
	at_H_iso.group = 'Non-linear'
	at_H_iso.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('H_iso')+'<br/>') + 
		html_par('isotropic hardening Modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hardening_Material','Hardening Material')+'<br/>') +
		html_end()
		)
	
	# H_kin
	at_H_kin = MpcAttributeMetaData()
	at_H_kin.type = MpcAttributeType.Real
	at_H_kin.name = 'H_kin'
	at_H_kin.group = 'Non-linear'
	at_H_kin.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('H_kin')+'<br/>') + 
		html_par('kinematic hardening Modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hardening_Material','Hardening Material')+'<br/>') +
		html_end()
		)
	
	# use_eta
	at_use_eta = MpcAttributeMetaData()
	at_use_eta.type = MpcAttributeType.Boolean
	at_use_eta.name = 'use_eta'
	at_use_eta.group = 'Non-linear'
	at_use_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_eta')+'<br/>') + 
		html_par('visco-plastic coefficient (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hardening_Material','Hardening Material')+'<br/>') +
		html_end()
		)
	
	# eta
	at_eta = MpcAttributeMetaData()
	at_eta.type = MpcAttributeType.Real
	at_eta.name = 'eta'
	at_eta.group = 'Optional parameters'
	at_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eta')+'<br/>') + 
		html_par('visco-plastic coefficient (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hardening_Material','Hardening Material')+'<br/>') +
		html_end()
		)
	at_eta.setDefault(0.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Hardening'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_E)
	xom.addAttribute(at_sigmaY)
	xom.addAttribute(at_H_iso)
	xom.addAttribute(at_H_kin)
	xom.addAttribute(at_use_eta)
	xom.addAttribute(at_eta)
	
	# eta-dep
	xom.setVisibilityDependency(at_use_eta, at_eta)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Hardening $matTag $E $sigmaY $H_iso $H_kin <$eta>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar
	
	sigmaY_at = xobj.getAttribute('sigmaY')
	if(sigmaY_at is None):
		raise Exception('Error: cannot find "sigmaY" attribute')
	sigmaY = sigmaY_at.quantityScalar
	
	H_iso_at = xobj.getAttribute('H_iso')
	if(H_iso_at is None):
		raise Exception('Error: cannot find "H_iso" attribute')
	H_iso = H_iso_at.real
	
	H_kin_at = xobj.getAttribute('H_kin')
	if(H_kin_at is None):
		raise Exception('Error: cannot find "H_kin" attribute')
	H_kin = H_kin_at.real
	
	
	# optional paramters
	sopt = ''
	
	use_eta_at = xobj.getAttribute('use_eta')
	if(use_eta_at is None):
		raise Exception('Error: cannot find "use_eta" attribute')
	use_eta = use_eta_at.boolean
	if use_eta:
		eta_at = xobj.getAttribute('eta')
		if(eta_at is None):
			raise Exception('Error: cannot find "eta" attribute')
		eta = eta_at.real
		
		sopt += '{}'.format(eta)
	
	
	str_tcl = '{}uniaxialMaterial Hardening {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, E.value, sigmaY.value, H_iso, H_kin, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)