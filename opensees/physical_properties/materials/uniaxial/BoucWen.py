# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Non-linear'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('ratio of post-yield stiffness to the initial elastic stiffenss (0< α <1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_end()
		)
	
	# ko
	at_ko = MpcAttributeMetaData()
	at_ko.type = MpcAttributeType.QuantityScalar
	at_ko.name = 'ko'
	at_ko.group = 'Elasticity'
	at_ko.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ko')+'<br/>') + 
		html_par('initial elastic stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_end()
		)
	at_ko.dimension = u.F/u.L**2
	
	# n
	at_n = MpcAttributeMetaData()
	at_n.type = MpcAttributeType.Real
	at_n.name = 'n'
	at_n.group = 'Elasticity'
	at_n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('n')+'<br/>') + 
		html_par('parameter that controls transition from linear to nonlinear range (as n increases the transition becomes sharper; n is usually greater or equal to 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_end()
		)
	
	# gamma
	at_gamma = MpcAttributeMetaData()
	at_gamma.type = MpcAttributeType.Real
	at_gamma.name = 'gamma'
	at_gamma.group = 'Non-linear'
	at_gamma.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') + 
		html_par('parameter that control shape of hysteresis loop; depending on the values of γ and β softening, hardening or quasi-linearity can be simulated (look at the NOTES)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_end()
		)
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'Non-linear'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') + 
		html_par('parameter that control shape of hysteresis loop; depending on the values of γ and β softening, hardening or quasi-linearity can be simulated (look at the NOTES)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_end()
		)
	
	# Ao
	at_Ao = MpcAttributeMetaData()
	at_Ao.type = MpcAttributeType.Real
	at_Ao.name = 'Ao'
	at_Ao.group = 'Non-linear'
	at_Ao.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ao')+'<br/>') + 
		html_par('parameter that control tangent stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_end()
		)
	
	# deltaA
	at_deltaA = MpcAttributeMetaData()
	at_deltaA.type = MpcAttributeType.Real
	at_deltaA.name = 'deltaA'
	at_deltaA.group = 'Non-linear'
	at_deltaA.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('deltaA')+'<br/>') + 
		html_par('parameter that control tangent stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_end()
		)
	
	# deltaNu
	at_deltaNu = MpcAttributeMetaData()
	at_deltaNu.type = MpcAttributeType.Real
	at_deltaNu.name = 'deltaNu'
	at_deltaNu.group = 'Non-linear'
	at_deltaNu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('deltaNu')+'<br/>') + 
		html_par('parameter that control material degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_end()
		)
	
	# deltaEta
	at_deltaEta = MpcAttributeMetaData()
	at_deltaEta.type = MpcAttributeType.Real
	at_deltaEta.name = 'deltaEta'
	at_deltaEta.group = 'Non-linear'
	at_deltaEta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('deltaEta')+'<br/>') + 
		html_par('parameter that control material degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'BoucWen'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_ko)
	xom.addAttribute(at_n)
	xom.addAttribute(at_gamma)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_Ao)
	xom.addAttribute(at_deltaA)
	xom.addAttribute(at_deltaNu)
	xom.addAttribute(at_deltaEta)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial BoucWen $matTag $alpha $ko $n $gamma $beta $Ao $deltaA $deltaNu $deltaEta
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	ko_at = xobj.getAttribute('ko')
	if(ko_at is None):
		raise Exception('Error: cannot find "ko" attribute')
	ko = ko_at.quantityScalar
	
	n_at = xobj.getAttribute('n')
	if(n_at is None):
		raise Exception('Error: cannot find "n" attribute')
	n = n_at.real
	
	gamma_at = xobj.getAttribute('gamma')
	if(gamma_at is None):
		raise Exception('Error: cannot find "gamma" attribute')
	gamma = gamma_at.real
	
	beta_at = xobj.getAttribute('beta')
	if(beta_at is None):
		raise Exception('Error: cannot find "beta" attribute')
	beta = beta_at.real
	
	Ao_at = xobj.getAttribute('Ao')
	if(Ao_at is None):
		raise Exception('Error: cannot find "Ao" attribute')
	Ao = Ao_at.real
	
	deltaA_at = xobj.getAttribute('deltaA')
	if(deltaA_at is None):
		raise Exception('Error: cannot find "deltaA" attribute')
	deltaA = deltaA_at.real
	
	deltaNu_at = xobj.getAttribute('deltaNu')
	if(deltaNu_at is None):
		raise Exception('Error: cannot find "deltaNu" attribute')
	deltaNu = deltaNu_at.real
	
	deltaEta_at = xobj.getAttribute('deltaEta')
	if(deltaEta_at is None):
		raise Exception('Error: cannot find "deltaEta" attribute')
	deltaEta = deltaEta_at.real
	
	
	str_tcl = '{}uniaxialMaterial BoucWen {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, alpha, ko.value, n, gamma, beta, Ao, deltaA, deltaNu, deltaEta)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)