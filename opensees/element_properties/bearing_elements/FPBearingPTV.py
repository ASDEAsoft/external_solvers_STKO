import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# MuRef
	at_MuRef = MpcAttributeMetaData()
	at_MuRef.type = MpcAttributeType.Real
	at_MuRef.name = 'MuRef'
	at_MuRef.group = 'Group'
	at_MuRef.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('MuRef')+'<br/>') +
		html_par('Reference coefficient of friction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	
	# IsPressureDependent
	at_IsPressureDependent = MpcAttributeMetaData()
	at_IsPressureDependent.type = MpcAttributeType.Real
	at_IsPressureDependent.name = 'IsPressureDependent'
	at_IsPressureDependent.group = 'Group'
	at_IsPressureDependent.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IsPressureDependent')+'<br/>') +
		html_par('1.0 if the coefficient of friction is a function of instantaneous axial pressure') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	
	# pRef
	at_pRef = MpcAttributeMetaData()
	at_pRef.type = MpcAttributeType.QuantityScalar
	at_pRef.name = 'pRef'
	at_pRef.group = 'Group'
	at_pRef.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pRef')+'<br/>') +
		html_par('Reference axial pressure (the bearing pressure under static loads)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_pRef.dimension = u.F/u.L**2
	
	# IsTemperatureDependent
	at_IsTemperatureDependent = MpcAttributeMetaData()
	at_IsTemperatureDependent.type = MpcAttributeType.Real
	at_IsTemperatureDependent.name = 'IsTemperatureDependent'
	at_IsTemperatureDependent.group = 'Group'
	at_IsTemperatureDependent.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IsTemperatureDependent')+'<br/>') +
		html_par('1.0 if the coefficient of friction is a function of instantaneous temperature at the sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	
	# Diffusivity
	at_Diffusivity = MpcAttributeMetaData()
	at_Diffusivity.type = MpcAttributeType.QuantityScalar
	at_Diffusivity.name = 'Diffusivity'
	at_Diffusivity.group = 'Group'
	at_Diffusivity.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Diffusivity')+'<br/>') +
		html_par('Thermal diffusivity of steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_Diffusivity.dimension = u.L**2/u.t
	
	# Conductivity
	at_Conductivity = MpcAttributeMetaData()
	at_Conductivity.type = MpcAttributeType.QuantityScalar
	at_Conductivity.name = 'Conductivity'
	at_Conductivity.group = 'Group'
	at_Conductivity.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Conductivity')+'<br/>') +
		html_par('Thermal conductivity of steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	
	# IsVelocityDependent
	at_IsVelocityDependent = MpcAttributeMetaData()
	at_IsVelocityDependent.type = MpcAttributeType.Real
	at_IsVelocityDependent.name = 'IsVelocityDependent'
	at_IsVelocityDependent.group = 'Group'
	at_IsVelocityDependent.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IsVelocityDependent')+'<br/>') +
		html_par('1.0 if the coefficient of friction is a function of instantaneous velocity at the sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	
	# rateParameter
	at_rateParameter = MpcAttributeMetaData()
	at_rateParameter.type = MpcAttributeType.Real
	at_rateParameter.name = 'rateParameter'
	at_rateParameter.group = 'Group'
	at_rateParameter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rateParameter')+'<br/>') +
		html_par('The exponent that determines the shape of the coefficient of friction vs. sliding velocity curve') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	
	# ReffectiveFP
	at_ReffectiveFP = MpcAttributeMetaData()
	at_ReffectiveFP.type = MpcAttributeType.QuantityScalar
	at_ReffectiveFP.name = 'ReffectiveFP'
	at_ReffectiveFP.group = 'Group'
	at_ReffectiveFP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ReffectiveFP')+'<br/>') +
		html_par('Effective radius of curvature of the sliding surface of the FPbearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_ReffectiveFP.dimension = u.L
	
	# Radius_Contact
	at_Radius_Contact = MpcAttributeMetaData()
	at_Radius_Contact.type = MpcAttributeType.QuantityScalar
	at_Radius_Contact.name = 'Radius_Contact'
	at_Radius_Contact.group = 'Group'
	at_Radius_Contact.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Radius_Contact')+'<br/>') +
		html_par('Radius of contact area at the sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_Radius_Contact.dimension = u.L
	
	# kInitial
	at_kInitial = MpcAttributeMetaData()
	at_kInitial.type = MpcAttributeType.QuantityScalar
	at_kInitial.name = 'kInitial'
	at_kInitial.group = 'Group'
	at_kInitial.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kInitial')+'<br/>') +
		html_par('Lateral stiffness of the sliding bearing before sliding begins') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_kInitial.dimension = u.F/u.L
	
	# shearDist
	at_shearDist = MpcAttributeMetaData()
	at_shearDist.type = MpcAttributeType.QuantityScalar
	at_shearDist.name = 'shearDist'
	at_shearDist.group = 'Group'
	at_shearDist.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('shearDist')+'<br/>') +
		html_par('Shear distance from iNode as a fraction of the length of the element') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_shearDist.dimension = u.L
	
	# doRayleigh
	at_doRayleigh = MpcAttributeMetaData()
	at_doRayleigh.type = MpcAttributeType.Boolean
	at_doRayleigh.name = 'doRayleigh'
	at_doRayleigh.group = 'Group'
	at_doRayleigh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('doRayleigh')+'<br/>') +
		html_par('To include Rayleigh damping from the bearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	
	# mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.QuantityScalar
	at_mass.name = 'mass'
	at_mass.group = 'Group'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mass')+'<br/>') +
		html_par('Element mass') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	# at_mass.dimension = u.M
	
	# iter
	at_iter = MpcAttributeMetaData()
	at_iter.type = MpcAttributeType.Integer
	at_iter.name = 'iter'
	at_iter.group = 'Group'
	at_iter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('iter')+'<br/>') +
		html_par('Maximum number of iterations to satisfy the equilibrium of element') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = 'Group'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('Convergence tolerance to satisfy the equilibrium of the element') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	
	at_unit = MpcAttributeMetaData()
	at_unit.type = MpcAttributeType.Integer
	at_unit.name = 'unit'
	at_unit.group = 'Group'
	at_unit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('unit')+'<br/>') +
		html_par('Tag to identify the unit from the list below') +
		html_par('1: N, m, s, C') +
		html_par('2: kN, m, s, C') +
		html_par('3: N, mm, s, C') +
		html_par('4: kN, mm, s, C') +
		html_par('5: lb, in, s, C') +
		html_par('6: kip, in, s, C') +
		html_par('7: lb, ft, s, C') +
		html_par('8: kip, ft, s, C') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_unit.sourceType = MpcAttributeSourceType.List
	at_unit.setSourceList([1,2,3,4,5,6,7,8])
	at_unit.setDefault(1)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'FPBearingPTV'
	xom.addAttribute(at_MuRef)
	xom.addAttribute(at_IsPressureDependent)
	xom.addAttribute(at_pRef)
	xom.addAttribute(at_IsTemperatureDependent)
	xom.addAttribute(at_Diffusivity)
	xom.addAttribute(at_Conductivity)
	xom.addAttribute(at_IsVelocityDependent)
	xom.addAttribute(at_rateParameter)
	xom.addAttribute(at_ReffectiveFP)
	xom.addAttribute(at_Radius_Contact)
	xom.addAttribute(at_kInitial)
	xom.addAttribute(at_shearDist)
	xom.addAttribute(at_doRayleigh)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_tol)
	xom.addAttribute(at_unit)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]	#[(ndm, ndf),(ndm, ndf)]

def writeTcl(pinfo):
	
	# element FPBearingPTV $eleTag $iNode $jNode $MuRef $IsPressureDependent $pRef $isTemperatureDependent $Diffusivity $Conductivity $IsVelocityDependent $rateParameter 
	# $ReffectiveFP $Radius_Contact $kInitial $theMaterialA $theMaterialB $theMaterialC $theMaterialD $x1 $x2 $x3 $y1 $y2 $y3 $shearDist $doRayleigh $mass $iter $tol $unit
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	pinfo.updateModelBuilder(3,6)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += '{} '.format(node.id)
	
	if (len(node_vect)!=2): 
		raise Exception('Error: invalid type of element or number of nodes')
	
	
	# mandatory parameters
	MuRef_at = xobj.getAttribute('MuRef')
	if(MuRef_at is None):
		raise Exception('Error: cannot find "MuRef" attribute')
	MuRef = MuRef_at.real
	
	IsPressureDependent_at = xobj.getAttribute('IsPressureDependent')
	if(IsPressureDependent_at is None):
		raise Exception('Error: cannot find "IsPressureDependent" attribute')
	IsPressureDependent = IsPressureDependent_at.real
	
	pRef_at = xobj.getAttribute('pRef')
	if(pRef_at is None):
		raise Exception('Error: cannot find "pRef" attribute')
	pRef = pRef_at.quantityScalar.value
	
	IsTemperatureDependent_at = xobj.getAttribute('IsTemperatureDependent')
	if(IsTemperatureDependent_at is None):
		raise Exception('Error: cannot find "IsTemperatureDependent" attribute')
	IsTemperatureDependent = IsTemperatureDependent_at.real
	
	Diffusivity_at = xobj.getAttribute('Diffusivity')
	if(Diffusivity_at is None):
		raise Exception('Error: cannot find "Diffusivity" attribute')
	Diffusivity = Diffusivity_at.quantityScalar.value
	
	Conductivity_at = xobj.getAttribute('Conductivity')
	if(Conductivity_at is None):
		raise Exception('Error: cannot find "Conductivity" attribute')
	Conductivity = Conductivity_at.quantityScalar.value
	
	IsVelocityDependent_at = xobj.getAttribute('IsVelocityDependent')
	if(IsVelocityDependent_at is None):
		raise Exception('Error: cannot find "IsVelocityDependent" attribute')
	IsVelocityDependent = IsVelocityDependent_at.real
	
	rateParameter_at = xobj.getAttribute('rateParameter')
	if(rateParameter_at is None):
		raise Exception('Error: cannot find "rateParameter" attribute')
	rateParameter = rateParameter_at.real
	
	ReffectiveFP_at = xobj.getAttribute('ReffectiveFP')
	if(ReffectiveFP_at is None):
		raise Exception('Error: cannot find "ReffectiveFP" attribute')
	ReffectiveFP = ReffectiveFP_at.quantityScalar.value
	
	Radius_Contact_at = xobj.getAttribute('Radius_Contact')
	if(Radius_Contact_at is None):
		raise Exception('Error: cannot find "Radius_Contact" attribute')
	Radius_Contact = Radius_Contact_at.quantityScalar.value
	
	Radius_Contact_at = xobj.getAttribute('kInitial')
	if(Radius_Contact_at is None):
		raise Exception('Error: cannot find "kInitial" attribute')
	kInitial = Radius_Contact_at.quantityScalar.value
	
	
	# ***special_purpose***
	if phys_prop.XObject.name != 'FPBearingPTVMaterial':
		raise Exception('Wrong material type for FPBearingPTV element. Expected: FPBearingPTVMaterial, given: {}'.format(phys_prop.XObject.name))
	
	theMaterialA_at = phys_prop.XObject.getAttribute('theMaterialA')
	if(theMaterialA_at is None):
		raise Exception('Error: cannot find "theMaterialA" attribute')
	theMaterialA = theMaterialA_at.index
	
	theMaterialB_at = phys_prop.XObject.getAttribute('theMaterialB')
	if(theMaterialB_at is None):
		raise Exception('Error: cannot find "theMaterialB" attribute')
	theMaterialB = theMaterialB_at.index
	
	theMaterialC_at = phys_prop.XObject.getAttribute('theMaterialC')
	if(theMaterialC_at is None):
		raise Exception('Error: cannot find "theMaterialC" attribute')
	theMaterialC = theMaterialC_at.index
	
	theMaterialD_at = phys_prop.XObject.getAttribute('theMaterialD')
	if(theMaterialD_at is None):
		raise Exception('Error: cannot find "theMaterialD" attribute')
	theMaterialD = theMaterialD_at.index
	# ***end special_purpose***
	
	
	vect_x = elem.orientation.computeOrientation().col(0)
	vect_y = elem.orientation.computeOrientation().col(1)
	
	sopt = ' {} {} {} {} {} {}'.format (vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	
	shearDist_at = xobj.getAttribute('shearDist')
	if(shearDist_at is None):
		raise Exception('Error: cannot find "shearDist" attribute')
	shearDist = shearDist_at.quantityScalar.value
	
	doRayleigh_at = xobj.getAttribute('doRayleigh')
	if(doRayleigh_at is None):
		raise Exception('Error: cannot find "doRayleigh" attribute')
	if doRayleigh_at.boolean: 
		doRayleigh=1
	else:
		doRayleigh=0
	
	mass_at = xobj.getAttribute('mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "mass" attribute')
	mass = mass_at.quantityScalar.value
	
	iter_at = xobj.getAttribute('iter')
	if(iter_at is None):
		raise Exception('Error: cannot find "iter" attribute')
	iter = iter_at.integer
	
	tol_at = xobj.getAttribute('tol')
	if(tol_at is None):
		raise Exception('Error: cannot find "tol" attribute')
	tol = tol_at.real
	
	unit_at = xobj.getAttribute('unit')
	if(unit_at is None):
		raise Exception('Error: cannot find "unit" attribute')
	unit = unit_at.integer
	
	
	str_tcl = '{}element FPBearingPTV {} {}{} {} {} {} {} {} {} {} {} {} {} {} {} {} {}{} {} {} {} {} {} {}\n'.format(
				pinfo.indent, tag, nstr, MuRef, IsPressureDependent, pRef, IsTemperatureDependent, Diffusivity,
				Conductivity, IsVelocityDependent, rateParameter, ReffectiveFP, Radius_Contact,
				kInitial, theMaterialA, theMaterialB, theMaterialC, theMaterialD, sopt, shearDist, doRayleigh,
				mass, iter, tol, unit)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)