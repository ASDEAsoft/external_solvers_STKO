import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# kInit
	at_kInit = MpcAttributeMetaData()
	at_kInit.type = MpcAttributeType.QuantityScalar
	at_kInit.name = 'kInit'
	at_kInit.group = 'Group'
	at_kInit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kInit')+'<br/>') +
		html_par('initial elastic stiffness in local shear direction') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_kInit.dimension = u.F/u.L
	
	# fy
	at_fy = MpcAttributeMetaData()
	at_fy.type = MpcAttributeType.Real
	at_fy.name = 'fy'
	at_fy.group = 'Group'
	at_fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fy')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# Gr
	at_Gr = MpcAttributeMetaData()
	at_Gr.type = MpcAttributeType.Real
	at_Gr.name = 'Gr'
	at_Gr.group = 'Group'
	at_Gr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Gr')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# kbulk
	at_kbulk = MpcAttributeMetaData()
	at_kbulk.type = MpcAttributeType.Real
	at_kbulk.name = 'kbulk'
	at_kbulk.group = 'Group'
	at_kbulk.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kbulk')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# D1
	at_D1 = MpcAttributeMetaData()
	at_D1.type = MpcAttributeType.Real
	at_D1.name = 'D1'
	at_D1.group = 'Group'
	at_D1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D1')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# D2
	at_D2 = MpcAttributeMetaData()
	at_D2.type = MpcAttributeType.Real
	at_D2.name = 'D2'
	at_D2.group = 'Group'
	at_D2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D2')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# ts
	at_ts = MpcAttributeMetaData()
	at_ts.type = MpcAttributeType.Real
	at_ts.name = 'ts'
	at_ts.group = 'Group'
	at_ts.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ts')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# tr
	at_tr = MpcAttributeMetaData()
	at_tr.type = MpcAttributeType.Real
	at_tr.name = 'tr'
	at_tr.group = 'Group'
	at_tr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tr')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# n
	at_n = MpcAttributeMetaData()
	at_n.type = MpcAttributeType.Integer
	at_n.name = 'n'
	at_n.group = 'Group'
	at_n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('n')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# alpha1
	at_alpha1 = MpcAttributeMetaData()
	at_alpha1.type = MpcAttributeType.Real
	at_alpha1.name = 'alpha1'
	at_alpha1.group = 'Group'
	at_alpha1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha1')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# alpha2
	at_alpha2 = MpcAttributeMetaData()
	at_alpha2.type = MpcAttributeType.Real
	at_alpha2.name = 'alpha2'
	at_alpha2.group = 'Group'
	at_alpha2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha2')+'<br/>') +
		html_par('default = 0.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_alpha2.setDefault(0.0)
	
	# mu
	at_mu = MpcAttributeMetaData()
	at_mu.type = MpcAttributeType.Real
	at_mu.name = 'mu'
	at_mu.group = 'Group'
	at_mu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu')+'<br/>') +
		html_par('default = 2.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_mu.setDefault(2.0)
	
	# eta
	at_eta = MpcAttributeMetaData()
	at_eta.type = MpcAttributeType.Real
	at_eta.name = 'eta'
	at_eta.group = 'Group'
	at_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eta')+'<br/>') +
		html_par('default = 1.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_eta.setDefault(1.0)
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'Group'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') +
		html_par('default = 0.5') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_beta.setDefault(0.5)
	
	# gamma
	at_gamma = MpcAttributeMetaData()
	at_gamma.type = MpcAttributeType.Real
	at_gamma.name = 'gamma'
	at_gamma.group = 'Group'
	at_gamma.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') +
		html_par('default = 0.5') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_gamma.setDefault(0.5)
	
	# -PMod
	at_PMod = MpcAttributeMetaData()
	at_PMod.type = MpcAttributeType.Boolean
	at_PMod.name = '-PMod'
	at_PMod.group = 'Group'
	at_PMod.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-PMod')+'<br/>') +
		html_par('to activate a1 and a2') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# a1
	at_a1 = MpcAttributeMetaData()
	at_a1.type = MpcAttributeType.Real
	at_a1.name = 'a1'
	at_a1.group = '-PMod'
	at_a1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a1')+'<br/>') +
		html_par('default = 0.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_a1.setDefault(0.0)
	
	# a2
	at_a2 = MpcAttributeMetaData()
	at_a2.type = MpcAttributeType.Real
	at_a2.name = 'a2'
	at_a2.group = '-PMod'
	at_a2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a2')+'<br/>') +
		html_par('default = 0.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_a2.setDefault(0.0)
	
	# -TMod
	at_TMod = MpcAttributeMetaData()
	at_TMod.type = MpcAttributeType.Boolean
	at_TMod.name = '-TMod'
	at_TMod.group = 'Group'
	at_TMod.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-TMod')+'<br/>') +
		html_par('to activate a1 and a2') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# T
	at_T = MpcAttributeMetaData()
	at_T.type = MpcAttributeType.Real
	at_T.name = 'T'
	at_T.group = '-TMod'
	at_T.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('T')+'<br/>') +
		html_par('default = 23.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_T.setDefault(23.0)
	
	# b1
	at_b1 = MpcAttributeMetaData()
	at_b1.type = MpcAttributeType.Real
	at_b1.name = 'b1'
	at_b1.group = '-TMod'
	at_b1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b1')+'<br/>') +
		html_par('default = 1.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_b1.setDefault(1.0)
	
	# b2
	at_b2 = MpcAttributeMetaData()
	at_b2.type = MpcAttributeType.Real
	at_b2.name = 'b2'
	at_b2.group = '-TMod'
	at_b2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b2')+'<br/>') +
		html_par('default = 0.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_b2.setDefault(0.0)
	
	# b3
	at_b3 = MpcAttributeMetaData()
	at_b3.type = MpcAttributeType.Real
	at_b3.name = 'b3'
	at_b3.group = '-TMod'
	at_b3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b3')+'<br/>') +
		html_par('default = 0.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_b3.setDefault(0.0)
	
	# b4
	at_b4 = MpcAttributeMetaData()
	at_b4.type = MpcAttributeType.Real
	at_b4.name = 'b4'
	at_b4.group = '-TMod'
	at_b4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b4')+'<br/>') +
		html_par('default = 0.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_b4.setDefault(0.0)
	
	# -shearDist
	at_shearDist = MpcAttributeMetaData()
	at_shearDist.type = MpcAttributeType.Boolean
	at_shearDist.name = '-shearDist'
	at_shearDist.group = 'Group'
	at_shearDist.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-shearDist')+'<br/>') +
		html_par('shear distance (optional, default = 0.5)') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# sDratio
	at_sDratio = MpcAttributeMetaData()
	at_sDratio.type = MpcAttributeType.Real
	at_sDratio.name = 'sDratio'
	at_sDratio.group = '-shearDist'
	at_sDratio.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sDratio')+'<br/>') +
		html_par('shear distance (optional, default = 0.5)') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_sDratio.setDefault(0.5)
	
	# -doRayleigh
	at_doRayleigh = MpcAttributeMetaData()
	at_doRayleigh.type = MpcAttributeType.Boolean
	at_doRayleigh.name = '-doRayleigh'
	at_doRayleigh.group = 'Group'
	at_doRayleigh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-doRayleigh')+'<br/>') +
		html_par('to include Rayleigh damping from the bearing (optional, default = no Rayleigh damping contribution)') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# -mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.Boolean
	at_mass.name = '-mass'
	at_mass.group = 'Group'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mass')+'<br/>') +
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.QuantityScalar
	at_m.name = 'm'
	at_m.group = '-mass'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') +
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_m.setDefault(0.0)
	#at_m.dimension = u.M
	
	# -iter
	at_iter = MpcAttributeMetaData()
	at_iter.type = MpcAttributeType.Boolean
	at_iter.name = '-iter'
	at_iter.group = 'Group'
	at_iter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-iter')+'<br/>') +
		html_par('default = 25') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# maxIter
	at_maxIter = MpcAttributeMetaData()
	at_maxIter.type = MpcAttributeType.Integer
	at_maxIter.name = 'maxIter'
	at_maxIter.group = '-iter'
	at_maxIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxIter')+'<br/>') +
		html_par('default = 25') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_maxIter.setDefault(25)
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = '-iter'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('default = 1e-12') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_tol.setDefault(1e-12)
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Group'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'elastomericBearingBoucWenMod'
	xom.addAttribute(at_kInit)
	xom.addAttribute(at_fy)
	xom.addAttribute(at_Gr)
	xom.addAttribute(at_kbulk)
	xom.addAttribute(at_D1)
	xom.addAttribute(at_D2)
	xom.addAttribute(at_ts)
	xom.addAttribute(at_tr)
	xom.addAttribute(at_n)
	xom.addAttribute(at_alpha1)
	xom.addAttribute(at_alpha2)
	xom.addAttribute(at_mu)
	xom.addAttribute(at_eta)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_gamma)
	xom.addAttribute(at_PMod)
	xom.addAttribute(at_a1)
	xom.addAttribute(at_a2)
	xom.addAttribute(at_TMod)
	xom.addAttribute(at_T)
	xom.addAttribute(at_b1)
	xom.addAttribute(at_b2)
	xom.addAttribute(at_b3)
	xom.addAttribute(at_b4)
	xom.addAttribute(at_shearDist)
	xom.addAttribute(at_sDratio)
	xom.addAttribute(at_doRayleigh)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_maxIter)
	xom.addAttribute(at_tol)
	xom.addAttribute(at_orient)
	
	
	# visibility dependencies
	
	# a1, a2-dep
	xom.setVisibilityDependency(at_PMod, at_a1)
	xom.setVisibilityDependency(at_PMod, at_a2)
	
	# T, b1, b2, b3, b4-dep
	xom.setVisibilityDependency(at_TMod, at_T)
	xom.setVisibilityDependency(at_TMod, at_b1)
	xom.setVisibilityDependency(at_TMod, at_b2)
	xom.setVisibilityDependency(at_TMod, at_b3)
	xom.setVisibilityDependency(at_TMod, at_b4)
	
	# sDratio-dep
	xom.setVisibilityDependency(at_shearDist, at_sDratio)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	# maxIter, tol-dep
	xom.setVisibilityDependency(at_iter, at_maxIter)
	xom.setVisibilityDependency(at_iter, at_tol)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	# ElastomericBearingBoucWenMod eleTag iNode jNode kInit fy Gr Kbulk D1 D2 ts tr n alpha1 alpha2
	# mu eta beta gamma <-PMod a1 a2 > <-TMod T b1 b2 b3 b4> <-shearDist sDratio> <-doRayleigh>
	# <-mass m> <-iter maxIter tol> <-orient <x1 x2 x3> y1 y2 y3>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=2): 													#CONTROLLARE: elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral or 
		raise Exception('Error: invalid type of element or number of nodes')	#CONTROLLARE IL FamilyType
	
	
	# mandatory parameters
	kInit_at = xobj.getAttribute('kInit')
	if(kInit_at is None):
		raise Exception('Error: cannot find "kInit" attribute')
	kInit = kInit_at.quantityScalar.value
	
	fy_at = xobj.getAttribute('fy')
	if(fy_at is None):
		raise Exception('Error: cannot find "fy" attribute')
	fy = fy_at.real
	
	Gr_at = xobj.getAttribute('Gr')
	if(Gr_at is None):
		raise Exception('Error: cannot find "Gr" attribute')
	Gr = Gr_at.real
	
	Kbulk_at = xobj.getAttribute('kbulk')
	if(Kbulk_at is None):
		raise Exception('Error: cannot find "kbulk" attribute')
	Kbulk = Kbulk_at.real
	
	D1_at = xobj.getAttribute('D1')
	if(D1_at is None):
		raise Exception('Error: cannot find "D1" attribute')
	D1 = D1_at.real
	
	D2_at = xobj.getAttribute('D2')
	if(D2_at is None):
		raise Exception('Error: cannot find "D2" attribute')
	D2 = D2_at.real
	
	ts_at = xobj.getAttribute('ts')
	if(ts_at is None):
		raise Exception('Error: cannot find "ts" attribute')
	ts = ts_at.real
	
	tr_at = xobj.getAttribute('tr')
	if(tr_at is None):
		raise Exception('Error: cannot find "tr" attribute')
	tr = tr_at.real
	
	n_at = xobj.getAttribute('n')
	if(n_at is None):
		raise Exception('Error: cannot find "n" attribute')
	n = n_at.integer
	
	alpha1_at = xobj.getAttribute('alpha1')
	if(alpha1_at is None):
		raise Exception('Error: cannot find "alpha1" attribute')
	alpha1 = alpha1_at.real
	
	alpha2_at = xobj.getAttribute('alpha2')
	if(alpha2_at is None):
		raise Exception('Error: cannot find "alpha2" attribute')
	alpha2 = alpha2_at.real
	
	mu_at = xobj.getAttribute('mu')
	if(mu_at is None):
		raise Exception('Error: cannot find "mu" attribute')
	mu = mu_at.real
	
	eta_at = xobj.getAttribute('eta')
	if(eta_at is None):
		raise Exception('Error: cannot find "eta" attribute')
	eta = eta_at.real
	
	beta_at = xobj.getAttribute('beta')
	if(beta_at is None):
		raise Exception('Error: cannot find "beta" attribute')
	beta = beta_at.real
	
	gamma_at = xobj.getAttribute('gamma')
	if(gamma_at is None):
		raise Exception('Error: cannot find "gamma" attribute')
	gamma = gamma_at.real
	
	
	# optional parameter
	sopt = ''
	
	PMod_at = xobj.getAttribute('-PMod')
	if(PMod_at is None):
		raise Exception('Error: cannot find "-PMod" attribute')
	if PMod_at.boolean:
		
		a1_at = xobj.getAttribute('a1')
		if(a1_at is None):
			raise Exception('Error: cannot find "a1" attribute')
		a1 = a1_at.real
		
		a2_at = xobj.getAttribute('a2')
		if(a2_at is None):
			raise Exception('Error: cannot find "a2" attribute')
		a2 = a2_at.real
		
		sopt += ' -PMod {} {}'.format(a1, a2)
	
	TMod_at = xobj.getAttribute('-TMod')
	if(TMod_at is None):
		raise Exception('Error: cannot find "-TMod" attribute')
	if TMod_at.boolean:
		T_at = xobj.getAttribute('T')
		if(T_at is None):
			raise Exception('Error: cannot find "T" attribute')
		T = T_at.real
		
		b1_at = xobj.getAttribute('b1')
		if(b1_at is None):
			raise Exception('Error: cannot find "b1" attribute')
		b1 = b1_at.real
		
		b2_at = xobj.getAttribute('b2')
		if(b2_at is None):
			raise Exception('Error: cannot find "b2" attribute')
		b2 = b2_at.real
		
		b3_at = xobj.getAttribute('b3')
		if(b3_at is None):
			raise Exception('Error: cannot find "b3" attribute')
		b3 = b3_at.real
		
		b4_at = xobj.getAttribute('b4')
		if(b4_at is None):
			raise Exception('Error: cannot find "b4" attribute')
		b4 = b4_at.real
		
		sopt += ' -TMod {} {} {} {} {}'.format(T, b1, b2, b3, b4)
	
	shearDist_at = xobj.getAttribute('-shearDist')
	if(shearDist_at is None):
		raise Exception('Error: cannot find "-shearDist" attribute')
	if shearDist_at.boolean:
		sDratio_at = xobj.getAttribute('sDratio')
		if(sDratio_at is None):
			raise Exception('Error: cannot find "sDratio" attribute')
		sDratio = sDratio_at.real
		
		sopt += ' -shearDist {}'.format(sDratio)
	
	doRayleigh_at = xobj.getAttribute('-doRayleigh')
	if(doRayleigh_at is None):
		raise Exception('Error: cannot find "-doRayleigh" attribute')
	if doRayleigh_at.boolean:
		
		sopt += ' -doRayleigh'
	
	mass_at = xobj.getAttribute('-mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "-mass" attribute')
	if mass_at.boolean:
		m_at = xobj.getAttribute('m')
		if(m_at is None):
			raise Exception('Error: cannot find "m" attribute')
		m = m_at.quantityScalar
		
		sopt += ' -mass {}'.format(m.value)
	
	iter_at = xobj.getAttribute('-iter')
	if(iter_at is None):
		raise Exception('Error: cannot find "-iter" attribute')
	if iter_at.boolean:
		maxIter_at = xobj.getAttribute('maxIter')
		if(maxIter_at is None):
			raise Exception('Error: cannot find "maxIter" attribute')
		maxIter = maxIter_at.integer
		
		tol_at = xobj.getAttribute('tol')
		if(tol_at is None):
			raise Exception('Error: cannot find "tol" attribute')
		tol = tol_at.real
		
		sopt += ' -iter {} {}'.format(maxIter, tol)
	
	orient_at = xobj.getAttribute('-orient')
	if(orient_at is None):
		raise Exception('Error: cannot find "-orient" attribute')
	if orient_at.boolean:
		vect_x=elem.orientation.computeOrientation().col(0)
		vect_y=elem.orientation.computeOrientation().col(1)
		
		sopt += ' -orient {} {} {} {} {} {}'.format (vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	
	
	str_tcl = '{}element ElastomericBearingBoucWenMod {}{} {} {} {} {} {} {} {} {} {}{}\n'.format(
				pinfo.indent, tag, nstr, kInit, fy, Gr, Kbulk, D1, D2, ts, tr, n, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)