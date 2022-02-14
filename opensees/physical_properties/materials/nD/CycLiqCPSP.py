import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# G0
	at_G0 = MpcAttributeMetaData()
	at_G0.type = MpcAttributeType.QuantityScalar
	at_G0.name = 'G0'
	at_G0.group = 'Non-linear'
	at_G0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('G0')+'<br/>') + 
		html_par('A constant related to elastic shear modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	at_G0.dimension = u.F/u.L**2
	
	# kappa
	at_kappa = MpcAttributeMetaData()
	at_kappa.type = MpcAttributeType.QuantityScalar
	at_kappa.name = 'kappa'
	at_kappa.group = 'Non-linear'
	at_kappa.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kappa')+'<br/>') + 
		html_par('A constant related to elastic bulk modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	at_kappa.dimension = u.F/u.L**2
	
	# h
	at_h = MpcAttributeMetaData()
	at_h.type = MpcAttributeType.Real
	at_h.name = 'h'
	at_h.group = 'Non-linear'
	at_h.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h')+'<br/>') + 
		html_par('Model parameter for plastic modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# M
	at_M = MpcAttributeMetaData()
	at_M.type = MpcAttributeType.Real
	at_M.name = 'M'
	at_M.group = 'Non-linear'
	at_M.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('M')+'<br/>') + 
		html_par('Critical state stress ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# dre1
	at_dre1 = MpcAttributeMetaData()
	at_dre1.type = MpcAttributeType.Real
	at_dre1.name = 'dre1'
	at_dre1.group = 'Non-linear'
	at_dre1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dre1')+'<br/>') + 
		html_par('Coefficient for reversible dilatancy generation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# dre2
	at_dre2 = MpcAttributeMetaData()
	at_dre2.type = MpcAttributeType.Real
	at_dre2.name = 'dre2'
	at_dre2.group = 'Non-linear'
	at_dre2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dre2')+'<br/>') + 
		html_par('Coefficient for reversible dilatancy release') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# rdr
	at_rdr = MpcAttributeMetaData()
	at_rdr.type = MpcAttributeType.QuantityScalar
	at_rdr.name = 'rdr'
	at_rdr.group = 'Non-linear'
	at_rdr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rdr')+'<br/>') + 
		html_par('Reference shear strain length') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	at_rdr.dimension = u.L
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Non-linear'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('Parameter controlling the decrease rate of irreversible dilatancy') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# dir
	at_dir = MpcAttributeMetaData()
	at_dir.type = MpcAttributeType.Real
	at_dir.name = 'dir'
	at_dir.group = 'Non-linear'
	at_dir.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir')+'<br/>') + 
		html_par('Coefficient for irreversible dilatancy potential') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# lambdac
	at_lambdac = MpcAttributeMetaData()
	at_lambdac.type = MpcAttributeType.Real
	at_lambdac.name = 'lambdac'
	at_lambdac.group = 'Non-linear'
	at_lambdac.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lambdac')+'<br/>') + 
		html_par('Critical state constant') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# ksi
	at_ksi = MpcAttributeMetaData()
	at_ksi.type = MpcAttributeType.Real
	at_ksi.name = 'ksi'
	at_ksi.group = 'Non-linear'
	at_ksi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ksi')+'<br/>') + 
		html_par('Critical state constant') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# e0
	at_e0 = MpcAttributeMetaData()
	at_e0.type = MpcAttributeType.Real
	at_e0.name = 'e0'
	at_e0.group = 'Non-linear'
	at_e0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e0')+'<br/>') + 
		html_par('Void ratio at pc=0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# np
	at_np = MpcAttributeMetaData()
	at_np.type = MpcAttributeType.Real
	at_np.name = 'np'
	at_np.group = 'Non-linear'
	at_np.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('np')+'<br/>') + 
		html_par('Material constant for peak mobilized stress ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# nd
	at_nd = MpcAttributeMetaData()
	at_nd.type = MpcAttributeType.Real
	at_nd.name = 'nd'
	at_nd.group = 'Non-linear'
	at_nd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nd')+'<br/>') + 
		html_par('Material constant for reversible dilatancy generation stress ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# ein
	at_ein = MpcAttributeMetaData()
	at_ein.type = MpcAttributeType.Real
	at_ein.name = 'ein'
	at_ein.group = 'Non-linear'
	at_ein.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ein')+'<br/>') + 
		html_par('Initial void ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# use_rho
	at_use_rho = MpcAttributeMetaData()
	at_use_rho.type = MpcAttributeType.Boolean
	at_use_rho.name = 'use_rho'
	at_use_rho.group = 'Non-linear'
	at_use_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_rho')+'<br/>') + 
		html_par('Saturated mass density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Optional parameters'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('Saturated mass density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCPSP_Material','CycLiqCPSP Material')+'<br/>') +
		html_end()
		)
	#at_rho.dimension = u.M/u.L**3
	
	xom = MpcXObjectMetaData()
	xom.name = 'CycLiqCPSP'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_G0)
	xom.addAttribute(at_kappa)
	xom.addAttribute(at_h)
	xom.addAttribute(at_M)
	xom.addAttribute(at_dre1)
	xom.addAttribute(at_dre2)
	xom.addAttribute(at_rdr)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_dir)
	xom.addAttribute(at_lambdac)
	xom.addAttribute(at_ksi)
	xom.addAttribute(at_e0)
	xom.addAttribute(at_np)
	xom.addAttribute(at_nd)
	xom.addAttribute(at_ein)
	xom.addAttribute(at_use_rho)
	xom.addAttribute(at_rho)
	
	#use_rho-dep
	xom.setVisibilityDependency(at_use_rho, at_rho)
	
	return xom

def writeTcl(pinfo):
	
	#nDmaterial CycLiqCPSP $matTag $G0 $kappa $h $M $dre1 $dre2 $rdr $alpha $dir $lambdac $ksi $e0 $np $nd $ein <$rho>
	xobj = pinfo.phys_prop.XObject
	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	G0_at = xobj.getAttribute('G0')
	if(G0_at is None):
		raise Exception('Error: cannot find "G0" attribute')
	G0 = G0_at.quantityScalar
	
	kappa_at = xobj.getAttribute('kappa')
	if(kappa_at is None):
		raise Exception('Error: cannot find "kappa" attribute')
	kappa = kappa_at.quantityScalar
	
	h_at = xobj.getAttribute('h')
	if(h_at is None):
		raise Exception('Error: cannot find "h" attribute')
	h = h_at.real
	
	M_at = xobj.getAttribute('M')
	if(M_at is None):
		raise Exception('Error: cannot find "M" attribute')
	M = M_at.real
	
	dre1_at = xobj.getAttribute('dre1')
	if(dre1_at is None):
		raise Exception('Error: cannot find "dre1" attribute')
	dre1 = dre1_at.real
	
	dre2_at = xobj.getAttribute('dre2')
	if(dre2_at is None):
		raise Exception('Error: cannot find "dre2" attribute')
	dre2 = dre2_at.real
	
	rdr_at = xobj.getAttribute('rdr')
	if(rdr_at is None):
		raise Exception('Error: cannot find "rdr" attribute')
	rdr = rdr_at.quantityScalar
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	dir_at = xobj.getAttribute('dir')
	if(dir_at is None):
		raise Exception('Error: cannot find "dir" attribute')
	dir = dir_at.real
	
	lambdac_at = xobj.getAttribute('lambdac')
	if(lambdac_at is None):
		raise Exception('Error: cannot find "lambdac" attribute')
	lambdac = lambdac_at.real
	
	ksi_at = xobj.getAttribute('ksi')
	if(ksi_at is None):
		raise Exception('Error: cannot find "ksi" attribute')
	ksi = ksi_at.real
	
	e0_at = xobj.getAttribute('e0')
	if(e0_at is None):
		raise Exception('Error: cannot find "e0" attribute')
	e0 = e0_at.real
	
	np_at = xobj.getAttribute('np')
	if(np_at is None):
		raise Exception('Error: cannot find "np" attribute')
	np = np_at.real
	
	nd_at = xobj.getAttribute('nd')
	if(nd_at is None):
		raise Exception('Error: cannot find "nd" attribute')
	nd = nd_at.real
	
	ein_at = xobj.getAttribute('ein')
	if(ein_at is None):
		raise Exception('Error: cannot find "ein" attribute')
	ein = ein_at.real
	
	# optional paramters
	sopt = ''
	
	use_rho_at = xobj.getAttribute('use_rho')
	if(use_rho_at is None):
		raise Exception('Error: cannot find "use_rho" attribute')
	use_rho = use_rho_at.boolean
	if use_rho:
		rho_at = xobj.getAttribute('rho')
		if(rho_at is None):
			raise Exception('Error: cannot find "rho" attribute')
		rho = rho_at.quantityScalar
		
		sopt += '{}'.format(rho.value)
	
	str_tcl = '{}nDMaterial CycLiqCPSP {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, G0.value, kappa.value, h, M, dre1, dre2, rdr.value, alpha, dir, lambdac, ksi, e0, np, nd, ein, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)