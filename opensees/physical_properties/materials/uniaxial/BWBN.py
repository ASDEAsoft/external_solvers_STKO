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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
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
		html_par('parameter that controls transition from linear to nonlinear range (as n increases the transition becomes sharper; n is usually grater or equal to 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
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
		html_par('parameter that control shape of hysteresis loop; depending on the values of γ and β softening, hardening or quasi-linearity can be simulated (look at the BoucWen Material)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
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
		html_par('parameter that control shape of hysteresis loop; depending on the values of γ and β softening, hardening or quasi-linearity can be simulated (look at the BoucWen Material)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BoucWen_Material','BoucWen Material')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
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
		html_par('parameter that controls tangent stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
		html_end()
		)
	
	# q
	at_q = MpcAttributeMetaData()
	at_q.type = MpcAttributeType.Real
	at_q.name = 'q'
	at_q.group = 'Pinching'
	at_q.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('q')+'<br/>') + 
		html_par('parameter that control pinching') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
		html_end()
		)
	
	# zetas
	at_zetas = MpcAttributeMetaData()
	at_zetas.type = MpcAttributeType.Real
	at_zetas.name = 'zetas'
	at_zetas.group = 'Pinching'
	at_zetas.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('zetas')+'<br/>') + 
		html_par('parameter that control pinching') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
		html_end()
		)
	
	# p
	at_p = MpcAttributeMetaData()
	at_p.type = MpcAttributeType.Real
	at_p.name = 'p'
	at_p.group = 'Pinching'
	at_p.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p')+'<br/>') + 
		html_par('parameter that control pinching') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
		html_end()
		)
	
	# Shi
	at_Shi = MpcAttributeMetaData()
	at_Shi.type = MpcAttributeType.Real
	at_Shi.name = 'Shi'
	at_Shi.group = 'Pinching'
	at_Shi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Shi')+'<br/>') + 
		html_par('parameter that control pinching') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
		html_end()
		)
	
	# deltaShi
	at_deltaShi = MpcAttributeMetaData()
	at_deltaShi.type = MpcAttributeType.Real
	at_deltaShi.name = 'deltaShi'
	at_deltaShi.group = 'Pinching'
	at_deltaShi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('deltaShi')+'<br/>') + 
		html_par('parameter that control pinching') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
		html_end()
		)
	
	# lambda
	at_lambda = MpcAttributeMetaData()
	at_lambda.type = MpcAttributeType.Real
	at_lambda.name = 'lambda'
	at_lambda.group = 'Pinching'
	at_lambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lambda')+'<br/>') + 
		html_par('parameter that control pinching') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
		html_end()
		)
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = 'Non-linear'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') + 
		html_par('tolerance') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
		html_end()
		)
	
	# maxIter
	at_maxIter = MpcAttributeMetaData()
	at_maxIter.type = MpcAttributeType.Integer
	at_maxIter.name = 'maxIter'
	at_maxIter.group = 'Non-linear'
	at_maxIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxIter')+'<br/>') + 
		html_par('maximum iterations') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BWBN_Material','BWBN Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'BWBN'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_ko)
	xom.addAttribute(at_n)
	xom.addAttribute(at_gamma)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_Ao)
	xom.addAttribute(at_q)
	xom.addAttribute(at_zetas)
	xom.addAttribute(at_p)
	xom.addAttribute(at_Shi)
	xom.addAttribute(at_deltaShi)
	xom.addAttribute(at_lambda)
	xom.addAttribute(at_tol)
	xom.addAttribute(at_maxIter)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial BWBN $matTag $alpha $ko $n $gamma $beta $Ao $q $zetas $p $Shi $deltaShi $lambda $tol $maxIter
	
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
	
	q_at = xobj.getAttribute('q')
	if(q_at is None):
		raise Exception('Error: cannot find "q" attribute')
	q = q_at.real
	
	zetas_at = xobj.getAttribute('zetas')
	if(zetas_at is None):
		raise Exception('Error: cannot find "zetas" attribute')
	zetas = zetas_at.real
	
	p_at = xobj.getAttribute('p')
	if(p_at is None):
		raise Exception('Error: cannot find "p" attribute')
	p = p_at.real
	
	Shi_at = xobj.getAttribute('Shi')
	if(Shi_at is None):
		raise Exception('Error: cannot find "Shi" attribute')
	Shi = Shi_at.real
	
	deltaShi_at = xobj.getAttribute('deltaShi')
	if(deltaShi_at is None):
		raise Exception('Error: cannot find "deltaShi" attribute')
	deltaShi = deltaShi_at.real
	
	lambda_at = xobj.getAttribute('lambda')
	if(lambda_at is None):
		raise Exception('Error: cannot find "lambda" attribute')
	lambd = lambda_at.real
	
	tol_at = xobj.getAttribute('tol')
	if(tol_at is None):
		raise Exception('Error: cannot find "tol" attribute')
	tol = tol_at.real
	
	maxIter_at = xobj.getAttribute('maxIter')
	if(maxIter_at is None):
		raise Exception('Error: cannot find "maxIter" attribute')
	maxIter = maxIter_at.integer
	
	
	str_tcl = '{}uniaxialMaterial BWBN {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, alpha, ko.value, n, gamma, beta, Ao, q, zetas, p, Shi, deltaShi, lambd, tol, maxIter)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)