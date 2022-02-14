import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# use_Mat
	at_use_Mat = MpcAttributeMetaData()
	at_use_Mat.type = MpcAttributeType.Boolean
	at_use_Mat.name = 'use_Mat'
	at_use_Mat.group = 'Group'
	at_use_Mat.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_Mat')+'<br/>') +
		html_par('to activate Mat1, Mat2, Mat3 and Mat4') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Joint2D_Element','Joint2D Element')+'<br/>') +
		html_end()
		)
	
	# Mat1
	at_Mat1 = MpcAttributeMetaData()
	at_Mat1.type = MpcAttributeType.Index
	at_Mat1.name = 'Mat1'
	at_Mat1.group = 'Optional parameters'
	at_Mat1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat1')+'<br/>') +
		html_par('uniaxial material tag for interface rotational spring at node 1. Use a zero tag to indicate the case that a beam-column element is rigidly framed to the joint. (optional)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Joint2D_Element','Joint2D Element')+'<br/>') +
		html_end()
		)
	at_Mat1.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat1.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat2
	at_Mat2 = MpcAttributeMetaData()
	at_Mat2.type = MpcAttributeType.Index
	at_Mat2.name = 'Mat2'
	at_Mat2.group = 'Optional parameters'
	at_Mat2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat2')+'<br/>') +
		html_par('uniaxial material tag for interface rotational spring at node 2. Use a zero tag to indicate the case that a beam-column element is rigidly framed to the joint. (optional)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Joint2D_Element','Joint2D Element')+'<br/>') +
		html_end()
		)
	at_Mat2.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat2.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat3
	at_Mat3 = MpcAttributeMetaData()
	at_Mat3.type = MpcAttributeType.Index
	at_Mat3.name = 'Mat3'
	at_Mat3.group = 'Optional parameters'
	at_Mat3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat3')+'<br/>') +
		html_par('uniaxial material tag for interface rotational spring at node 3. Use a zero tag to indicate the case that a beam-column element is rigidly framed to the joint. (optional)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Joint2D_Element','Joint2D Element')+'<br/>') +
		html_end()
		)
	at_Mat3.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat3.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat4
	at_Mat4 = MpcAttributeMetaData()
	at_Mat4.type = MpcAttributeType.Index
	at_Mat4.name = 'Mat4'
	at_Mat4.group = 'Optional parameters'
	at_Mat4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat4')+'<br/>') +
		html_par('uniaxial material tag for interface rotational spring at node 4. Use a zero tag to indicate the case that a beam-column element is rigidly framed to the joint. (optional)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Joint2D_Element','Joint2D Element')+'<br/>') +
		html_end()
		)
	at_Mat4.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat4.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# MatC
	at_MatC = MpcAttributeMetaData()
	at_MatC.type = MpcAttributeType.Index
	at_MatC.name = 'MatC'
	at_MatC.group = 'Group'
	at_MatC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('MatC')+'<br/>') +
		html_par('uniaxial material tag for rotational spring of the central node that describes shear panel behavior') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Joint2D_Element','Joint2D Element')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'Joint2DMaterial'
	xom.Xgroup = 'Joint Material'
	xom.addAttribute(at_use_Mat)
	xom.addAttribute(at_Mat1)
	xom.addAttribute(at_Mat2)
	xom.addAttribute(at_Mat3)
	xom.addAttribute(at_Mat4)
	xom.addAttribute(at_MatC)
	
	
	# Mat1, Mat2, Mat3 and Mat4-dep
	xom.setVisibilityDependency(at_use_Mat, at_Mat1)
	xom.setVisibilityDependency(at_use_Mat, at_Mat2)
	xom.setVisibilityDependency(at_use_Mat, at_Mat3)
	xom.setVisibilityDependency(at_use_Mat, at_Mat4)
	
	
	return xom