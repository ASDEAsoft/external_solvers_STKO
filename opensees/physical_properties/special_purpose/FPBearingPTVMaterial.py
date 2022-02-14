import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# theMaterialA
	at_theMaterialA = MpcAttributeMetaData()
	at_theMaterialA.type = MpcAttributeType.Index
	at_theMaterialA.name = 'theMaterialA'
	at_theMaterialA.group = 'Group'
	at_theMaterialA.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theMaterialA')+'<br/>') +
		html_par('Tag for the uniaxial material in the axial direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_theMaterialA.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_theMaterialA.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# theMaterialB
	at_theMaterialB = MpcAttributeMetaData()
	at_theMaterialB.type = MpcAttributeType.Index
	at_theMaterialB.name = 'theMaterialB'
	at_theMaterialB.group = 'Group'
	at_theMaterialB.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theMaterialB')+'<br/>') +
		html_par('Tag for the uniaxial material in the torsional direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_theMaterialB.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_theMaterialB.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# theMaterialC
	at_theMaterialC = MpcAttributeMetaData()
	at_theMaterialC.type = MpcAttributeType.Index
	at_theMaterialC.name = 'theMaterialC'
	at_theMaterialC.group = 'Group'
	at_theMaterialC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theMaterialC')+'<br/>') +
		html_par('Tag for the uniaxial material for rocking about local Y axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_theMaterialC.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_theMaterialC.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# theMaterialD
	at_theMaterialD = MpcAttributeMetaData()
	at_theMaterialD.type = MpcAttributeType.Index
	at_theMaterialD.name = 'theMaterialD'
	at_theMaterialD.group = 'Group'
	at_theMaterialD.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theMaterialD')+'<br/>') +
		html_par('Tag for the uniaxial material for rocking about local Z axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FPBearingPTV','FPBearingPTV')+'<br/>') +
		html_end()
		)
	at_theMaterialD.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_theMaterialD.indexSource.addAllowedNamespace("materials.uniaxial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'FPBearingPTV'
	xom.Xgroup = 'Bearing Material'
	xom.addAttribute(at_theMaterialA)
	xom.addAttribute(at_theMaterialB)
	xom.addAttribute(at_theMaterialC)
	xom.addAttribute(at_theMaterialD)
	
	
	return xom