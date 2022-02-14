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
		html_par('bulk modulus constant') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	at_G0.dimension = u.F/u.L**2
	
	# nu
	at_nu = MpcAttributeMetaData()
	at_nu.type = MpcAttributeType.Real
	at_nu.name = 'nu'
	at_nu.group = 'Non-linear'
	at_nu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nu')+'<br/>') + 
		html_par('poisson ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# e_init
	at_e_init = MpcAttributeMetaData()
	at_e_init.type = MpcAttributeType.Real
	at_e_init.name = 'e_init'
	at_e_init.group = 'Non-linear'
	at_e_init.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e_init')+'<br/>') + 
		html_par('initial void ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# Mc
	at_Mc = MpcAttributeMetaData()
	at_Mc.type = MpcAttributeType.Real
	at_Mc.name = 'Mc'
	at_Mc.group = 'Non-linear'
	at_Mc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mc')+'<br/>') + 
		html_par('critical state stress ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.Real
	at_c.name = 'c'
	at_c.group = 'Non-linear'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') + 
		html_par('ratio of critical state stress ratio in extension and compression') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# lambda_c
	at_lambda_c = MpcAttributeMetaData()
	at_lambda_c.type = MpcAttributeType.Real
	at_lambda_c.name = 'lambda_c'
	at_lambda_c.group = 'Non-linear'
	at_lambda_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lambda_c')+'<br/>') + 
		html_par('critical state line constant') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
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
		html_par('critical void ratio at p = 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
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
		html_par('critical state line constant') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# P_atm
	at_P_atm = MpcAttributeMetaData()
	at_P_atm.type = MpcAttributeType.QuantityScalar
	at_P_atm.name = 'P_atm'
	at_P_atm.group = 'Non-linear'
	at_P_atm.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('P_atm')+'<br/>') + 
		html_par('atmospheric pressure') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	at_P_atm.dimension = u.F/u.L**2
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.Real
	at_m.name = 'm'
	at_m.group = 'Non-linear'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') + 
		html_par('yield surface constant (radius of yield surface in stress ratio space)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# h0
	at_h0 = MpcAttributeMetaData()
	at_h0.type = MpcAttributeType.Real
	at_h0.name = 'h0'
	at_h0.group = 'Non-linear'
	at_h0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h0')+'<br/>') + 
		html_par('constant parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# ch
	at_ch = MpcAttributeMetaData()
	at_ch.type = MpcAttributeType.Real
	at_ch.name = 'ch'
	at_ch.group = 'Non-linear'
	at_ch.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ch')+'<br/>') + 
		html_par('constant parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# nb
	at_nb = MpcAttributeMetaData()
	at_nb.type = MpcAttributeType.Real
	at_nb.name = 'nb'
	at_nb.group = 'Non-linear'
	at_nb.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nb')+'<br/>') + 
		html_par('bounding surface parameter, nb ≥ 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# A0
	at_A0 = MpcAttributeMetaData()
	at_A0.type = MpcAttributeType.Real
	at_A0.name = 'A0'
	at_A0.group = 'Non-linear'
	at_A0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('A0')+'<br/>') + 
		html_par('dilatancy parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
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
		html_par('dilatancy surface parameter nd ≥ 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# z_max
	at_z_max = MpcAttributeMetaData()
	at_z_max.type = MpcAttributeType.Real
	at_z_max.name = 'z_max'
	at_z_max.group = 'Non-linear'
	at_z_max.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('z_max')+'<br/>') + 
		html_par('fabric-dilatancy tensor parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# cz
	at_cz = MpcAttributeMetaData()
	at_cz.type = MpcAttributeType.Real
	at_cz.name = 'cz'
	at_cz.group = 'Non-linear'
	at_cz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cz')+'<br/>') + 
		html_par('fabric-dilatancy tensor parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# Den
	at_Den = MpcAttributeMetaData()
	at_Den.type = MpcAttributeType.QuantityScalar
	at_Den.name = 'Den'
	at_Den.group = 'Non-linear'
	at_Den.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Den')+'<br/>') + 
		html_par('mass density of the material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	#at_Den.dimension = u.M/u.L**3
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	
	# intScheme
	at_intScheme = MpcAttributeMetaData()
	at_intScheme.type = MpcAttributeType.Integer
	at_intScheme.name = 'intScheme'
	at_intScheme.group = 'Optional parameters'
	at_intScheme.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('intScheme')+'<br/>') + 
		html_par('plastic integration scheme (default = 2)') +
		html_par('0: forward explicit,') +
		html_par('1: backward implicit,') +
		html_par('2: improved backward implicit') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	at_intScheme.sourceType = MpcAttributeSourceType.List
	at_intScheme.setSourceList([0, 1, 2])
	at_intScheme.setDefault(2)
	
	# TanType
	at_TanType = MpcAttributeMetaData()
	at_TanType.type = MpcAttributeType.Integer
	at_TanType.name = 'TanType'
	at_TanType.group = 'Optional parameters'
	at_TanType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('TanType')+'<br/>') + 
		html_par('material modulus matrix (default = 2)') +
		html_par('0: elastic stiffness,') +
		html_par('1: continuum elastoplastic stiffness,') +
		html_par('2: consistent elastoplastic stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	at_TanType.sourceType = MpcAttributeSourceType.List
	at_TanType.setSourceList([0, 1, 2])
	at_TanType.setDefault(2)
	
	# JacoType
	at_JacoType = MpcAttributeMetaData()
	at_JacoType.type = MpcAttributeType.Integer
	at_JacoType.name = 'JacoType'
	at_JacoType.group = 'Optional parameters'
	at_JacoType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('JacoType')+'<br/>') + 
		html_par('jacobian matrix used for newton iterations (default = 1)') +
		html_par('0: finite difference jacobian,') +
		html_par('1: analytical jacobian') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	at_JacoType.sourceType = MpcAttributeSourceType.List
	at_JacoType.setSourceList([0, 1])
	at_JacoType.setDefault(1)
	
	# TolF
	at_TolF = MpcAttributeMetaData()
	at_TolF.type = MpcAttributeType.Real
	at_TolF.name = 'TolF'
	at_TolF.group = 'Optional parameters'
	at_TolF.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('TolF')+'<br/>') + 
		html_par('drift from yield surface tolerance (default = 1.0e-7)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	at_TolF.setDefault(1.0e-7)
	
	# TolR
	at_TolR = MpcAttributeMetaData()
	at_TolR.type = MpcAttributeType.Real
	at_TolR.name = 'TolR'
	at_TolR.group = 'Optional parameters'
	at_TolR.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('TolR')+'<br/>') + 
		html_par('newton iterations residuals tolerance (default = 1.0e-7)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Manzari_Dafalias_Material','Manzari Dafalias Material')+'<br/>') +
		html_end()
		)
	at_TolR.setDefault(1.0e-7)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ManzariDafalias'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_G0)
	xom.addAttribute(at_nu)
	xom.addAttribute(at_e_init)
	xom.addAttribute(at_Mc)
	xom.addAttribute(at_c)
	xom.addAttribute(at_lambda_c)
	xom.addAttribute(at_e0)
	xom.addAttribute(at_ksi)
	xom.addAttribute(at_P_atm)
	xom.addAttribute(at_m)
	xom.addAttribute(at_h0)
	xom.addAttribute(at_ch)
	xom.addAttribute(at_nb)
	xom.addAttribute(at_A0)
	xom.addAttribute(at_nd)
	xom.addAttribute(at_z_max)
	xom.addAttribute(at_cz)
	xom.addAttribute(at_Den)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_intScheme)
	xom.addAttribute(at_TanType)
	xom.addAttribute(at_JacoType)
	xom.addAttribute(at_TolF)
	xom.addAttribute(at_TolR)
	
	# use_Optional-dep
	xom.setVisibilityDependency(at_Optional, at_intScheme)
	xom.setVisibilityDependency(at_Optional, at_TanType)
	xom.setVisibilityDependency(at_Optional, at_JacoType)
	xom.setVisibilityDependency(at_Optional, at_TolF)
	xom.setVisibilityDependency(at_Optional, at_TolR)
	
	return xom

def writeTcl(pinfo):
	
	#nDmaterial ManzariDafalias $matTag $G0 $nu $e_init $Mc $c $lambda_c $e0 $ksi $P_atm
	# $m $h0 $ch $nb $A0 $nd $z_max $cz $Den <$intScheme $TanType $JacoType $TolF $TolR>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	G0_at = xobj.getAttribute('G0')
	if(G0_at is None):
		raise Exception('Error: cannot find "G0" attribute')
	G0 = G0_at.quantityScalar
	
	nu_at = xobj.getAttribute('nu')
	if(nu_at is None):
		raise Exception('Error: cannot find "nu" attribute')
	nu = nu_at.real
	
	e_init_at = xobj.getAttribute('e_init')
	if(e_init_at is None):
		raise Exception('Error: cannot find "e_init" attribute')
	e_init = e_init_at.real
	
	Mc_at = xobj.getAttribute('Mc')
	if(Mc_at is None):
		raise Exception('Error: cannot find "Mc" attribute')
	Mc = Mc_at.real
	
	c_at = xobj.getAttribute('c')
	if(c_at is None):
		raise Exception('Error: cannot find "c" attribute')
	c = c_at.real
	
	lambda_c_at = xobj.getAttribute('lambda_c')
	if(lambda_c_at is None):
		raise Exception('Error: cannot find "lambda_c" attribute')
	lambda_c = lambda_c_at.real
	
	e0_at = xobj.getAttribute('e0')
	if(e0_at is None):
		raise Exception('Error: cannot find "e0" attribute')
	e0 = e0_at.real
	
	ksi_at = xobj.getAttribute('ksi')
	if(ksi_at is None):
		raise Exception('Error: cannot find "ksi" attribute')
	ksi = ksi_at.real
	
	P_atm_at = xobj.getAttribute('P_atm')
	if(P_atm_at is None):
		raise Exception('Error: cannot find "P_atm" attribute')
	P_atm = P_atm_at.quantityScalar
	
	m_at = xobj.getAttribute('m')
	if(m_at is None):
		raise Exception('Error: cannot find "m" attribute')
	m = m_at.real
	
	h0_at = xobj.getAttribute('h0')
	if(h0_at is None):
		raise Exception('Error: cannot find "h0" attribute')
	h0 = h0_at.real
	
	ch_at = xobj.getAttribute('ch')
	if(ch_at is None):
		raise Exception('Error: cannot find "ch" attribute')
	ch = ch_at.real
	
	nb_at = xobj.getAttribute('nb')
	if(nb_at is None):
		raise Exception('Error: cannot find "nb" attribute')
	nb = nb_at.real
	
	A0_at = xobj.getAttribute('A0')
	if(A0_at is None):
		raise Exception('Error: cannot find "A0" attribute')
	A0 = A0_at.real
	
	nd_at = xobj.getAttribute('nd')
	if(nd_at is None):
		raise Exception('Error: cannot find "nd" attribute')
	nd = nd_at.real
	
	z_max_at = xobj.getAttribute('z_max')
	if(z_max_at is None):
		raise Exception('Error: cannot find "z_max" attribute')
	z_max = z_max_at.real
	
	cz_at = xobj.getAttribute('cz')
	if(cz_at is None):
		raise Exception('Error: cannot find "cz" attribute')
	cz = cz_at.real
	
	Den_at = xobj.getAttribute('Den')
	if(Den_at is None):
		raise Exception('Error: cannot find "Den" attribute')
	Den = Den_at.quantityScalar
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		intScheme_at = xobj.getAttribute('intScheme')
		if(intScheme_at is None):
			raise Exception('Error: cannot find "intScheme" attribute')
		intScheme = intScheme_at.integer
		
		TanType_at = xobj.getAttribute('TanType')
		if(TanType_at is None):
			raise Exception('Error: cannot find "TanType" attribute')
		TanType = TanType_at.integer
		
		JacoType_at = xobj.getAttribute('JacoType')
		if(JacoType_at is None):
			raise Exception('Error: cannot find "JacoType" attribute')
		JacoType = JacoType_at.integer
		
		TolF_at = xobj.getAttribute('TolF')
		if(TolF_at is None):
			raise Exception('Error: cannot find "TolF" attribute')
		TolF = TolF_at.real
		
		TolR_at = xobj.getAttribute('TolR')
		if(TolR_at is None):
			raise Exception('Error: cannot find "TolR" attribute')
		TolR = TolR_at.real
		
		sopt += ' {} {} {} {}'.format(intScheme, TanType, JacoType, TolF, TolR)
	
	str_tcl = '{}nDMaterial ManzariDafalias {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}{}\n'.format(
			pinfo.indent, tag, G0.value, nu, e_init, Mc, c, lambda_c, e0, ksi, P_atm.value, m, h0, ch, nb, A0, nd, z_max, cz, Den.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)