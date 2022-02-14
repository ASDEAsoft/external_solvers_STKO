import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# frnMdlTag
	at_frnMdlTag = MpcAttributeMetaData()
	at_frnMdlTag.type = MpcAttributeType.Index
	at_frnMdlTag.name = 'frnMdlTag'
	at_frnMdlTag.group = 'Group'
	at_frnMdlTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('frnMdlTag')+'<br/>') +
		html_par('tag associated with previously-defined '+html_href('http://opensees.berkeley.edu/wiki/index.php/FrictionModel_Command','FrictionModel')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
		html_end()
		)
	at_frnMdlTag.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_frnMdlTag.indexSource.addAllowedNamespace("frictionModel")
	
	# kInit
	at_kInit = MpcAttributeMetaData()
	at_kInit.type = MpcAttributeType.QuantityScalar
	at_kInit.name = 'kInit'
	at_kInit.group = 'Group'
	at_kInit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kInit')+'<br/>') +
		html_par('initial elastic stiffness in local shear direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
		html_end()
		)
	at_kInit.dimension = u.F/u.L
	
	# k2
	at_k2 = MpcAttributeMetaData()
	at_k2.type = MpcAttributeType.QuantityScalar
	at_k2.name = 'k2'
	at_k2.group = 'Group'
	at_k2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k2')+'<br/>') +
		html_par('post yield stiffness of linear hardening component (MER spring)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
		html_end()
		)
	at_k2.dimension = u.F/u.L
	
	# k3
	at_k3 = MpcAttributeMetaData()
	at_k3.type = MpcAttributeType.QuantityScalar
	at_k3.name = 'k3'
	at_k3.group = 'Group'
	at_k3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k3')+'<br/>') +
		html_par('post yield stiffness of non-linear hardening component (MER spring)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
		html_end()
		)
	at_k3.dimension = u.F/u.L
	
	# eta
	at_eta = MpcAttributeMetaData()
	at_eta.type = MpcAttributeType.Real
	at_eta.name = 'eta'
	at_eta.group = 'Group'
	at_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eta')+'<br/>') +
		html_par('exponent of non-linear hardening component') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
		html_end()
		)
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Optional parameters'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RJ-Watson_EQS_Bearing_Element','RJ-Watson EQS Bearing Element')+'<br/>') +
		html_end()
		)
	at_tol.setDefault(1e-8)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'RJWatsonEqsBearing'
	xom.addAttribute(at_frnMdlTag)
	xom.addAttribute(at_kInit)
	xom.addAttribute(at_k2)
	xom.addAttribute(at_k3)
	xom.addAttribute(at_eta)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_shearDist)
	xom.addAttribute(at_sDratio)
	xom.addAttribute(at_doRayleigh)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_maxIter)
	xom.addAttribute(at_tol)
	
	
	# visibility dependencies
	
	# sDratio-dep
	xom.setVisibilityDependency(at_shearDist, at_sDratio)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	# maxIter, tol-dep
	xom.setVisibilityDependency(at_iter, at_maxIter)
	xom.setVisibilityDependency(at_iter, at_tol)
	
	return xom