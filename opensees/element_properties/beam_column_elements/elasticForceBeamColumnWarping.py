import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.element_properties.beam_column_elements.internalBeamColumnElement as internalBeamColumnElement

def makeXObjectMetaData():
	
	#Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Group'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') +
		html_par('choose between 2D and 3D') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('3D')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Group'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') +
		html_par('') +
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
		html_end()
		)
	at_3D.editable = False
	
	# -iter
	at_iter = MpcAttributeMetaData()
	at_iter.type = MpcAttributeType.Boolean
	at_iter.name = '-iter'
	at_iter.group = 'Group'
	at_iter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-iter')+'<br/>') +
		html_par('') +
		html_end()
		)
	
	# maxIters
	at_maxIters = MpcAttributeMetaData()
	at_maxIters.type = MpcAttributeType.Integer
	at_maxIters.name = 'maxIters'
	at_maxIters.group = '-iter'
	at_maxIters.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxIters')+'<br/>') +
		html_par('maximum number of iterations to undertake to satisfy element compatibility (optional, default=10)') +
		html_end()
		)
	at_maxIters.setDefault(10)
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = '-iter'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('tolerance for satisfaction of element compatibility (optional, default=10e-12)') +
		html_end()
		)
	at_tol.setDefault(10e-12)
	
	# massType
	# -cMass
	at_cMass = MpcAttributeMetaData()
	at_cMass.type = MpcAttributeType.Boolean
	at_cMass.name = '-cMass'
	at_cMass.group = 'Group'
	at_cMass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-cMass')+'<br/>') +
		html_par('to form consistent mass matrix (optional, default = lumped mass matrix)') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'elasticForceBeamColumnWarping'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_maxIters)
	xom.addAttribute(at_tol)
	xom.addAttribute(at_cMass)
	
	internalBeamColumnElement.internalBeamFunction(xom)
	
	# maxIters, tol-dep
	xom.setVisibilityDependency(at_iter, at_maxIters)
	xom.setVisibilityDependency(at_iter, at_tol)
	
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	return xom

def getNodalSpatialDim(xobj):
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
	
	# element elasticForceBeamColumnWarping $eleTag $iNode $jNode $transfTag "IntegrationType arg1 arg2 ..." <-mass $massDens> <-iter $maxIters $tol>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	secTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	if Dimension2_at.boolean:
		ndm = 2
		ndf = 3
	else:
		ndm = 3
		ndf = 6
	
	pinfo.updateModelBuilder(ndm, ndf)
	
	sopt = ''
	
	cMass_at = xobj.getAttribute('-cMass')
	if(cMass_at is None):
		raise Exception('Error: cannot find "-cMass" attribute')
	if cMass_at.boolean:
		sopt += ' -cMass'
	
	iter_at = xobj.getAttribute('-iter')
	if(iter_at is None):
		raise Exception('Error: cannot find "-iter" attribute')
	iter = iter_at.boolean
	if iter:
		maxIters_at = xobj.getAttribute('maxIters')
		if(maxIters_at is None):
			raise Exception('Error: cannot find "maxIters" attribute')
		maxIters = maxIters_at.integer
		
		tol_at = xobj.getAttribute('tol')
		if(tol_at is None):
			raise Exception('Error: cannot find "tol" attribute')
		tol = tol_at.real
		
		sopt+= ' -iter {} {}'.format(maxIters, tol)
	
	internalBeamColumnElement.writeTcl_internalBeamFunction(pinfo, sopt)