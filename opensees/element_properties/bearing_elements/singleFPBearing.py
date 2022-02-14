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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# frnMdlTag
	at_frnMdlTag = MpcAttributeMetaData()
	at_frnMdlTag.type = MpcAttributeType.Index
	at_frnMdlTag.name = 'frnMdlTag'
	at_frnMdlTag.group = 'Group'
	at_frnMdlTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('frnMdlTag')+'<br/>') +
		html_par('tag associated with previously-defined ' + html_href('http://opensees.berkeley.edu/wiki/index.php/FrictionModel_Command','FrictionModel')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_frnMdlTag.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_frnMdlTag.indexSource.addAllowedNamespace("frictionModel")
	
	# Reff
	at_Reff = MpcAttributeMetaData()
	at_Reff.type = MpcAttributeType.QuantityScalar
	at_Reff.name = 'Reff'
	at_Reff.group = 'Group'
	at_Reff.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Reff')+'<br/>') +
		html_par('effective radius of concave sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_Reff.dimension = u.L
	
	# kInit
	at_kInit = MpcAttributeMetaData()
	at_kInit.type = MpcAttributeType.QuantityScalar
	at_kInit.name = 'kInit'
	at_kInit.group = 'Group'
	at_kInit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kInit')+'<br/>') +
		html_par('initial elastic stiffness in local shear direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_kInit.dimension = u.F/u.L
	
	# matTagP
	at_matTagP = MpcAttributeMetaData()
	at_matTagP.type = MpcAttributeType.Index
	at_matTagP.name = 'matTag/P'
	at_matTagP.group = '-P'
	at_matTagP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') +
		html_par('tag associated with previously-defined UniaxialMaterial in axial direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_matTagP.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagP.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# matTagT
	at_matTagT = MpcAttributeMetaData()
	at_matTagT.type = MpcAttributeType.Index
	at_matTagT.name = 'matTag/T'
	at_matTagT.group = '-T'
	at_matTagT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') +
		html_par('tag associated with previously-defined UniaxialMaterial in torsional direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_matTagT.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagT.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# matTagMy
	at_matTagMy = MpcAttributeMetaData()
	at_matTagMy.type = MpcAttributeType.Index
	at_matTagMy.name = 'matTag/My'
	at_matTagMy.group = '-My'
	at_matTagMy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') +
		html_par('tag associated with previously-defined UniaxialMaterial in moment direction around local y-axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_matTagMy.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagMy.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# matTagMz
	at_matTagMz = MpcAttributeMetaData()
	at_matTagMz.type = MpcAttributeType.Index
	at_matTagMz.name = 'matTag/Mz'
	at_matTagMz.group = '-Mz'
	at_matTagMz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') +
		html_par('tag associated with previously-defined UniaxialMaterial in moment direction around local z-axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_matTagMz.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagMz.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Optional parameters'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	
	# -shearDist
	at_shearDist = MpcAttributeMetaData()
	at_shearDist.type = MpcAttributeType.Boolean
	at_shearDist.name = '-shearDist'
	at_shearDist.group = 'Optional parameters'
	at_shearDist.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-shearDist')+'<br/>') +
		html_par('shear distance from iNode as a fraction of the element length (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
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
		html_par('shear distance from iNode as a fraction of the element length (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_sDratio.setDefault(0.0)
	
	# -doRayleigh
	at_doRayleigh = MpcAttributeMetaData()
	at_doRayleigh.type = MpcAttributeType.Boolean
	at_doRayleigh.name = '-doRayleigh'
	at_doRayleigh.group = 'Optional parameters'
	at_doRayleigh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-doRayleigh')+'<br/>') +
		html_par('to include Rayleigh damping from the bearing (optional, default = no Rayleigh damping contribution)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	# VertDisp
	at_inclVertDisp = MpcAttributeMetaData()
	at_inclVertDisp.type = MpcAttributeType.Boolean
	at_inclVertDisp.name = '-inclVertDisp'
	at_inclVertDisp.group = 'Optional parameters'
	at_inclVertDisp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-inclVertDisp')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
		
	# -mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.Boolean
	at_mass.name = '-mass'
	at_mass.group = 'Optional parameters'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mass')+'<br/>') +
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_m.setDefault(0.0)
	#at_m.dimension = u.M
	
	# -iter
	at_iter = MpcAttributeMetaData()
	at_iter.type = MpcAttributeType.Boolean
	at_iter.name = '-iter'
	at_iter.group = 'Optional parameters'
	at_iter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-iter')+'<br/>') +
		html_par('to activate maxIter and tol') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
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
		html_par('maximum number of iterations to undertake to satisfy element equilibrium (optional, default = 20)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_maxIter.setDefault(20)
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = '-iter'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('convergence tolerance to satisfy element equilibrium (optional, default = 1E-8)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Single_Friction_Pendulum_Bearing_Element','Single Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_tol.setDefault(1e-8)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'singleFPBearing'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_frnMdlTag)
	xom.addAttribute(at_Reff)
	xom.addAttribute(at_kInit)
	xom.addAttribute(at_matTagP)
	xom.addAttribute(at_matTagT)
	xom.addAttribute(at_matTagMy)
	xom.addAttribute(at_matTagMz)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_shearDist)
	xom.addAttribute(at_sDratio)
	xom.addAttribute(at_doRayleigh)
	xom.addAttribute(at_inclVertDisp)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_maxIter)
	xom.addAttribute(at_tol)
	
	
	# visibility dependencies
	
	# matTag-dep
	xom.setVisibilityDependency(at_3D, at_matTagT)
	xom.setVisibilityDependency(at_3D, at_matTagMy)
	
	# sDratio-dep
	xom.setVisibilityDependency(at_shearDist, at_sDratio)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	# maxIter, tol-dep
	xom.setVisibilityDependency(at_iter, at_maxIter)
	xom.setVisibilityDependency(at_iter, at_tol)
	
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
	
	#2D
	# singleFPBearing eleTag iNode jNode frnMdlTag Reff kInit -P matTag -Mz matTag <-orient x1 x2 x3 y1 y2 y3> <-shearDist sDratio> <-doRayleigh> <-inclVertDisp><-mass m> <-iter maxIter tol>	
	#3D
	# singleFPBearing eleTag iNode jNode frnMdlTag Reff kInit -P matTag -T matTag -My matTag -Mz matTag <-orient <x1 x2 x3> y1 y2 y3> <-shearDist sDratio> <-doRayleigh> <-inclVertDsip> <-mass m> <-iter maxIter tol>	
	
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	# matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	Dimension3_at = xobj.getAttribute('3D')
	if(Dimension3_at is None):
		raise Exception('Error: cannot find "3D" attribute')
	Dimension3 = Dimension3_at.boolean
	
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += '{} '.format(node.id)
	
	if (len(node_vect)!=2): 													#CONTROLLARE: elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral or 
		raise Exception('Error: invalid type of element or number of nodes')	#CONTROLLARE IL FamilyType
	
	
	# mandatory parameters
	frnMdlTag_at = xobj.getAttribute('frnMdlTag')
	if(frnMdlTag_at is None):
		raise Exception('Error: cannot find "frnMdlTag" attribute')
	frnMdlTag = frnMdlTag_at.index
	
	Reff_at = xobj.getAttribute('Reff')
	if(Reff_at is None):
		raise Exception('Error: cannot find "Reff" attribute')
	Reff = Reff_at.quantityScalar.value
	
	kInit_at = xobj.getAttribute('kInit')
	if(kInit_at is None):
		raise Exception('Error: cannot find "kInit" attribute')
	kInit = kInit_at.quantityScalar.value

	sopt1 = ''
	
	matTagP_at = xobj.getAttribute('matTag/P')
	if(matTagP_at is None):
		raise Exception('Error: cannot find "matTagP" attribute')
	matTagP = matTagP_at.index
	
	sopt1 += ' -P {}'.format(matTagP)
	
	if Dimension3:
	
		matTagT_at = xobj.getAttribute('matTag/T')
		if(matTagT_at is None):
			raise Exception('Error: cannot find "matTagT" attribute')
		matTagT = matTagT_at.index
		
		sopt1 += ' -T {}'.format(matTagT)
	
		matTagMy_at = xobj.getAttribute('matTag/My')
		if(matTagMy_at is None):
			raise Exception('Error: cannot find "matTagMy" attribute')
		matTagMy = matTagMy_at.index
		
		sopt1 += ' -My {}'.format(matTagMy)
	

	matTagMz_at = xobj.getAttribute('matTag/Mz')
	if(matTagMz_at is None):
		raise Exception('Error: cannot find "matTagMz" attribute')
	matTagMz = matTagMz_at.index
	
	sopt1 += ' -Mz {}'.format(matTagMz)
	
	
	# optional paramters
	sopt2 = ''
	
	orient_at = xobj.getAttribute('-orient')
	if(orient_at is None):
		raise Exception('Error: cannot find "-orient" attribute')
	if orient_at.boolean:
		vect_x=elem.orientation.computeOrientation().col(0)
		vect_y=elem.orientation.computeOrientation().col(1)
		
		sopt2 += ' -orient {} {} {} {} {} {}'.format (vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	
	
	shearDist_at = xobj.getAttribute('-shearDist')
	if(shearDist_at is None):
		raise Exception('Error: cannot find "-shearDist" attribute')
	shearDist = shearDist_at.boolean
	if shearDist:
		sDratio_at = xobj.getAttribute('sDratio')
		if(sDratio_at is None):
			raise Exception('Error: cannot find "sDratio" attribute')
		sDratio = sDratio_at.real
		
		sopt2 += ' -shearDist {}'.format(sDratio)
	
	
	doRayleigh_at = xobj.getAttribute('-doRayleigh')
	if(doRayleigh_at is None):
		raise Exception('Error: cannot find "-doRayleigh" attribute')
	doRayleigh = doRayleigh_at.boolean
	if doRayleigh:
		
		sopt2 += ' -doRayleigh'
	
	
	inclVertDisp_at = xobj.getAttribute('-inclVertDisp')
	if(inclVertDisp_at is None):
		raise Exception('Error: cannot find "-inclVertDisp" attribute')
	inclVertDisp = inclVertDisp_at.boolean
	if inclVertDisp:
		
		sopt2 += ' -inclVertDisp'
	
	mass_at = xobj.getAttribute('-mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "-mass" attribute')
	mass = mass_at.boolean
	if mass:
		m_at = xobj.getAttribute('m')
		if(m_at is None):
			raise Exception('Error: cannot find "m" attribute')
		m = m_at.quantityScalar
		
		sopt2 += ' -mass {}'.format(m.value)
	
	
	iter_at = xobj.getAttribute('-iter')
	if(iter_at is None):
		raise Exception('Error: cannot find "-iter" attribute')
	iter = iter_at.boolean
	if iter:
		maxIter_at = xobj.getAttribute('maxIter')
		if(maxIter_at is None):
			raise Exception('Error: cannot find "maxIter" attribute')
		maxIter = maxIter_at.integer
		
		tol_at = xobj.getAttribute('tol')
		if(tol_at is None):
			raise Exception('Error: cannot find "tol" attribute')
		tol = tol_at.real
		
		sopt2 += ' -iter {} {}'.format(maxIter, tol)
	
	
	str_tcl = '{}element singleFPBearing {} {}{} {} {}{}{}\n'.format(
				pinfo.indent, tag, nstr, frnMdlTag, Reff, kInit, sopt1, sopt2)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)