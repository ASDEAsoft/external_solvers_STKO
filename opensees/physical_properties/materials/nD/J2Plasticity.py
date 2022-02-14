# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# K
	at_K = MpcAttributeMetaData()
	at_K.type = MpcAttributeType.QuantityScalar
	at_K.name = 'K'
	at_K.group = 'Elasticity'
	at_K.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K')+'<br/>') + 
		html_par('bulk modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/J2_Plasticity_Material','J2 Plasticity Material')+'<br/>') +
		html_end()
		)
	at_K.dimension = u.F/u.L**2
	
	# G
	at_G = MpcAttributeMetaData()
	at_G.type = MpcAttributeType.QuantityScalar
	at_G.name = 'G'
	at_G.group = 'Elasticity'
	at_G.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('G')+'<br/>') + 
		html_par('shaer modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/J2_Plasticity_Material','J2 Plasticity Material')+'<br/>') +
		html_end()
		)
	at_G.dimension = u.F/u.L**2
	
	# sig0
	at_sig0 = MpcAttributeMetaData()
	at_sig0.type = MpcAttributeType.QuantityScalar
	at_sig0.name = 'sig0'
	at_sig0.group = 'Non-linear'
	at_sig0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sig0')+'<br/>') + 
		html_par('initial yield stress') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/J2_Plasticity_Material','J2 Plasticity Material')+'<br/>') +
		html_end()
		)
	at_sig0.dimension = u.F/u.L**2
	
	# sigInf
	at_sigInf = MpcAttributeMetaData()
	at_sigInf.type = MpcAttributeType.QuantityScalar
	at_sigInf.name = 'sigInf'
	at_sigInf.group = 'Non-linear'
	at_sigInf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sigInf')+'<br/>') + 
		html_par('final saturation yield stress') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/J2_Plasticity_Material','J2 Plasticity Material')+'<br/>') +
		html_end()
		)
	at_sigInf.dimension = u.F/u.L**2
	
	# delta
	at_delta = MpcAttributeMetaData()
	at_delta.type = MpcAttributeType.QuantityScalar
	at_delta.name = 'delta'
	at_delta.group = 'Non-linear'
	at_delta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('delta')+'<br/>') + 
		html_par('exponential hardening parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/J2_Plasticity_Material','J2 Plasticity Material')+'<br/>') +
		html_end()
		)
	
	# H
	at_H = MpcAttributeMetaData()
	at_H.type = MpcAttributeType.QuantityScalar
	at_H.name = 'H'
	at_H.group = 'Non-linear'
	at_H.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('H')+'<br/>') + 
		html_par('	linear hardening parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/J2_Plasticity_Material','J2 Plasticity Material')+'<br/>') +
		html_end()
		)
	at_H.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'J2Plasticity'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_K)
	xom.addAttribute(at_G)
	xom.addAttribute(at_sig0)
	xom.addAttribute(at_sigInf)
	xom.addAttribute(at_delta)
	xom.addAttribute(at_H)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial J2Plasticity $matTag $K $G $sig0 $sigInf $delta $H
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	K_at = xobj.getAttribute('K')
	if(K_at is None):
		raise Exception('Error: cannot find "K" attribute')
	K = K_at.quantityScalar
	
	G_at = xobj.getAttribute('G')
	if(G_at is None):
		raise Exception('Error: cannot find "G" attribute')
	G = G_at.quantityScalar
	
	sig0_at = xobj.getAttribute('sig0')
	if(sig0_at is None):
		raise Exception('Error: cannot find "sig0" attribute')
	sig0 = sig0_at.quantityScalar
	
	sigInf_at = xobj.getAttribute('sigInf')
	if(sigInf_at is None):
		raise Exception('Error: cannot find "sigInf" attribute')
	sigInf = sigInf_at.quantityScalar
	
	delta_at = xobj.getAttribute('delta')
	if(delta_at is None):
		raise Exception('Error: cannot find "delta" attribute')
	delta = delta_at.quantityScalar
	
	H_at = xobj.getAttribute('H')
	if(H_at is None):
		raise Exception('Error: cannot find "H" attribute')
	H = H_at.quantityScalar
	
	str_tcl = '{}nDMaterial J2Plasticity {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, K.value, G.value, sig0.value, sigInf.value, delta.value, H.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)