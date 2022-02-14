import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.element_properties.beam_column_elements.internalBeamColumnElement as internalBeamColumnElement

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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement-Based_Beam-Column_Element','Displacement-Based Beam-Column Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement-Based_Beam-Column_Element','Displacement-Based Beam-Column Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement-Based_Beam-Column_Element','Displacement-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# -cMass
	at_cMass = MpcAttributeMetaData()
	at_cMass.type = MpcAttributeType.Boolean
	at_cMass.name = '-cMass'
	at_cMass.group = 'Group'
	at_cMass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-cMass')+'<br/>') +
		html_par('to form consistent mass matrix (optional, default = lumped mass matrix)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement-Based_Beam-Column_Element','Displacement-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'dispBeamColumn'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_cMass)
	
	internalBeamColumnElement.internalBeamFunction(xom)
	
	# auto-exclusive dependencies
	
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
	xobj = pinfo.elem_prop.XObject
	
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
	
	cMass_at = xobj.getAttribute('-cMass')
	if(cMass_at is None):
		raise Exception('Error: cannot find "-cMass" attribute')
	if cMass_at.boolean:
		cMass = ' -cMass'
		# writeTcl_internalBeamFunction
		internalBeamColumnElement.writeTcl_internalBeamFunction(pinfo, cMass)
	else:
		# writeTcl_internalBeamFunction
		internalBeamColumnElement.writeTcl_internalBeamFunction(pinfo)