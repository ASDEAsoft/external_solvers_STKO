import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Group'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') +
		html_par('choose between 2D and 3D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Group'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
		html_end()
		)
	at_2D.editable = False
	
	# 3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Group'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# kInit
	at_kInit = MpcAttributeMetaData()
	at_kInit.type = MpcAttributeType.QuantityScalar
	at_kInit.name = 'kInit'
	at_kInit.group = 'Group'
	at_kInit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kInit')+'<br/>') +
		html_par('initial elastic stiffness in local shear direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
		html_end()
		)
	at_kInit.dimension = u.F/u.L
	
	# qd
	at_qd = MpcAttributeMetaData()
	at_qd.type = MpcAttributeType.Real
	at_qd.name = 'qd'
	at_qd.group = 'Group'
	at_qd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('qd')+'<br/>') +
		html_par('characteristic strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
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
		html_par('post yield stiffness ratio of linear hardening component') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
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
		html_par('post yield stiffness ratio of non-linear hardening component') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
		html_end()
		)
	
	# mu
	at_mu = MpcAttributeMetaData()
	at_mu.type = MpcAttributeType.Real
	at_mu.name = 'mu'
	at_mu.group = 'Group'
	at_mu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu')+'<br/>') +
		html_par('exponent of non-linear hardening component') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
		html_end()
		)
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Group'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
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
		html_par('shear distance from iNode as a fraction of the element length (optional, default = 0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
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
		html_par('shear distance from iNode as a fraction of the element length (optional, default = 0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastomeric_Bearing_(Plasticity)_Element','Elastomeric Bearing (Plasticity) Element')+'<br/>') +
		html_end()
		)
	at_m.setDefault(0.0)
	#at_m.dimension = u.M
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'elastomericBearingPlasticity'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_kInit)
	xom.addAttribute(at_qd)
	xom.addAttribute(at_alpha1)
	xom.addAttribute(at_alpha2)
	xom.addAttribute(at_mu)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_shearDist)
	xom.addAttribute(at_sDratio)
	xom.addAttribute(at_doRayleigh)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	
	
	# visibility dependencies
	
	# sDratio-dep
	xom.setVisibilityDependency(at_shearDist, at_sDratio)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	Dimension2 = Dimension2_at.boolean
	
	if Dimension2:
		ndm = 2
		ndf = 3
	else:
		ndm = 3
		ndf = 6
	
	return [(ndm,ndf),(ndm,ndf)]

def writeTcl(pinfo):
	
	# 2D
	# element elastomericBearingPlasticity $eleTag $iNode $jNode $kInit $qd $alpha1 $alpha2 $mu
	# -P $matTag -Mz $matTag <-orient $x1 $x2 $x3 $y1 $y2 $y3> <-shearDist $sDratio> <-doRayleigh> <-mass $m>
	
	# 3D
	# element elastomericBearingPlasticity $eleTag $iNode $jNode $kInit $qd $alpha1 $alpha2 $mu
	# -P $matTag -T $matTag -My $matTag -Mz $matTag <-orient <$x1 $x2 $x3> $y1 $y2 $y3> <-shearDist $sDratio> <-doRayleigh> <-mass $m>
	
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
	Dimension3_at = xobj.getAttribute('3D')
	if(Dimension3_at is None):
		raise Exception('Error: cannot find "3D" attribute')
	Dimension3 = Dimension3_at.boolean
	
	kInit_at = xobj.getAttribute('kInit')
	if(kInit_at is None):
		raise Exception('Error: cannot find "kInit" attribute')
	kInit = kInit_at.quantityScalar.value
	
	qd_at = xobj.getAttribute('qd')
	if(qd_at is None):
		raise Exception('Error: cannot find "qd" attribute')
	qd = qd_at.real
	
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
	
	
	Dimension_at = xobj.getAttribute('Dimension')
	if(Dimension_at is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	Dimension = Dimension_at.string
	
	# optional paramters
	sopt = ''
	
	# ***special_purpose***
	if phys_prop.XObject.name != 'elastomericBearingMaterial':
		raise Exception('Wrong material type for elastomericBearingMaterial element. Expected: elastomericBearingMaterial, given: {}'.format(phys_prop.XObject.name))
	
	
	DimensionMat_at = phys_prop.XObject.getAttribute('Dimension')
	if(DimensionMat_at is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	DimensionMat = DimensionMat_at.string
	
	if(Dimension != DimensionMat ):
		raise Exception('Error: different dimension between "elastomericBearingPlasticity" element and "elastomericBearingMaterial"')
	
	matTagP_at = phys_prop.XObject.getAttribute('matTagP')
	if(matTagP_at is None):
		raise Exception('Error: cannot find "matTagP" attribute')
	matTagP = matTagP_at.index
	
	sopt += ' -P {}'.format(matTagP)
	
	if Dimension3:
		matTagT_at = phys_prop.XObject.getAttribute('matTagT')
		if(matTagT_at is None):
			raise Exception('Error: cannot find "matTagT" attribute')
		matTagT = matTagT_at.index
		
		matTagMy_at = phys_prop.XObject.getAttribute('matTagMy')
		if(matTagMy_at is None):
			raise Exception('Error: cannot find "matTagMy" attribute')
		matTagMy = matTagMy_at.index
		
		sopt += ' -T {} -My {}'.format(matTagT, matTagMy)
	
	matTagMz_at = phys_prop.XObject.getAttribute('matTagMz')
	if(matTagMz_at is None):
		raise Exception('Error: cannot find "matTagMz" attribute')
	matTagMz = matTagMz_at.index
	
	sopt += ' -Mz {}'.format(matTagMz)
	#***end "special_purpose"***
	
	
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
	
	
	str_tcl = '{}element elastomericBearingPlasticity {}{} {} {} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, kInit, qd, alpha1, alpha2, mu, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)