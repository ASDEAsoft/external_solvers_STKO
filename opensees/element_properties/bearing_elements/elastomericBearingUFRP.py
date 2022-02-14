import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# uy
	at_uy = MpcAttributeMetaData()
	at_uy.type = MpcAttributeType.Real
	at_uy.name = 'uy'
	at_uy.group = 'Group'
	at_uy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('uy')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# a1
	at_a1 = MpcAttributeMetaData()
	at_a1.type = MpcAttributeType.Real
	at_a1.name = 'a1'
	at_a1.group = 'Group'
	at_a1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a1')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# a2
	at_a2 = MpcAttributeMetaData()
	at_a2.type = MpcAttributeType.Real
	at_a2.name = 'a2'
	at_a2.group = 'Group'
	at_a2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a2')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# a3
	at_a3 = MpcAttributeMetaData()
	at_a3.type = MpcAttributeType.Real
	at_a3.name = 'a3'
	at_a3.group = 'Group'
	at_a3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a3')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# a4
	at_a4 = MpcAttributeMetaData()
	at_a4.type = MpcAttributeType.Real
	at_a4.name = 'a4'
	at_a4.group = 'Group'
	at_a4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a4')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# a5
	at_a5 = MpcAttributeMetaData()
	at_a5.type = MpcAttributeType.Real
	at_a5.name = 'a5'
	at_a5.group = 'Group'
	at_a5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a5')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# b
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.Real
	at_b.name = 'b'
	at_b.group = 'Group'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.Real
	at_c.name = 'c'
	at_c.group = 'Group'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
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
	
	# -shearDist
	at_shearDist = MpcAttributeMetaData()
	at_shearDist.type = MpcAttributeType.Boolean
	at_shearDist.name = '-shearDist'
	at_shearDist.group = 'Group'
	at_shearDist.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-shearDist')+'<br/>') +
		html_par('optional, default = 0.5') +
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
		html_par('optional, default = 0.5') +
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
		html_par('default = 0') +
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
		html_par('optional, default = 0.0') +
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
		html_par('optional, default = 0.0') +
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
		html_par('optional') +
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
		html_par('optional, default = 0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_maxIter.setDefault(0)
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = '-iter'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('optional, default = 0.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_tol.setDefault(1e-12)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'elastomericBearingUFRP'
	xom.addAttribute(at_uy)
	xom.addAttribute(at_a1)
	xom.addAttribute(at_a2)
	xom.addAttribute(at_a3)
	xom.addAttribute(at_a4)
	xom.addAttribute(at_a5)
	xom.addAttribute(at_b)
	xom.addAttribute(at_c)
	xom.addAttribute(at_eta)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_gamma)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_shearDist)
	xom.addAttribute(at_sDratio)
	xom.addAttribute(at_doRayleigh)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_maxIter)
	xom.addAttribute(at_tol)
	
	# sDratio-dep
	xom.setVisibilityDependency(at_shearDist, at_sDratio)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	# maxIter, tol-dep
	xom.setVisibilityDependency(at_iter, at_maxIter)
	xom.setVisibilityDependency(at_iter, at_tol)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3)]	#(ndm,ndf)

def writeTcl(pinfo):
	
	# elastomericBearingUFRP eleTag iNode jNode uy a1 a2 a3 a4 a5 b c eta beta gamma -P matTag -Mz matTag
	# <-orient x1 x2 x3 y1 y2 y3> <-shearDist sDratio> <-doRayleigh> <-mass m> <-iter maxIter tol>
	
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
	
	if (len(node_vect)!=2):
		raise Exception('Error: invalid number of nodes')
	
	
	# mandatory parameters
	uy_at = xobj.getAttribute('uy')
	if(uy_at is None):
		raise Exception('Error: cannot find "uy" attribute')
	uy = uy_at.real
	
	a1_at = xobj.getAttribute('a1')
	if(a1_at is None):
		raise Exception('Error: cannot find "a1" attribute')
	a1 = a1_at.real
	
	a2_at = xobj.getAttribute('a2')
	if(a2_at is None):
		raise Exception('Error: cannot find "a2" attribute')
	a2 = a2_at.real
	
	a3_at = xobj.getAttribute('a3')
	if(a3_at is None):
		raise Exception('Error: cannot find "a3" attribute')
	a3 = a3_at.real
	
	a4_at = xobj.getAttribute('a4')
	if(a4_at is None):
		raise Exception('Error: cannot find "a4" attribute')
	a4 = a4_at.real
	
	a5_at = xobj.getAttribute('a5')
	if(a5_at is None):
		raise Exception('Error: cannot find "a5" attribute')
	a5 = a5_at.real
	
	b_at = xobj.getAttribute('b')
	if(b_at is None):
		raise Exception('Error: cannot find "b" attribute')
	b = b_at.real
	
	c_at = xobj.getAttribute('c')
	if(c_at is None):
		raise Exception('Error: cannot find "c" attribute')
	c = c_at.real
	
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
	
	
	# ***special_purpose***
	if phys_prop.XObject.name != 'elastomericBearingMaterial':
		raise Exception('Wrong material type for elastomericBearingMaterial element. Expected: elastomericBearingMaterial, given: {}'.format(phys_prop.XObject.name))
	
	# check if ndm = 2
	Dimension3D_at = phys_prop.XObject.getAttribute('3D')
	if(Dimension3D_at is None):
		raise Exception('Error: cannot find "3D" attribute')
	if Dimension3D_at.boolean:
		raise Exception('Error: "elastomericBearingUFRP" command only works when ndm is 2')
	
	
	matTagP_at = phys_prop.XObject.getAttribute('matTagP')
	if(matTagP_at is None):
		raise Exception('Error: cannot find "matTagP" attribute')
	matTagP = matTagP_at.index
	
	matTagMz_at = phys_prop.XObject.getAttribute('matTagMz')
	if(matTagMz_at is None):
		raise Exception('Error: cannot find "matTagMz" attribute')
	matTagMz = matTagMz_at.index
	#***end "special_purpose"***
	
	
	# optional paramters
	sopt = ''
	
	orient_at = xobj.getAttribute('-orient')
	if(orient_at is None):
		raise Exception('Error: cannot find "-orient" attribute')
	if orient_at.boolean:
		vect_x=elem.orientation.computeOrientation().col(0)
		vect_y=elem.orientation.computeOrientation().col(1)
		
		sopt += ' -orient {} {} {} {} {} {}'.format (vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	
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
		maxIter = maxIter_at.real
		
		tol_at = xobj.getAttribute('tol')
		if(tol_at is None):
			raise Exception('Error: cannot find "tol" attribute')
		tol = tol_at.real
		
		sopt += ' -iter {} {}'.format(maxIter, tol)
	
	
	str_tcl = '{}element elastomericBearingUFRP {}{} {} {} {} {} {} {} {} {} {} {} {} -P {} -Mz {}{}\n'.format(
			pinfo.indent, tag, nstr, uy, a1, a2, a3, a4, a5, b, c, eta, beta, gamma, matTagP, matTagMz, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)