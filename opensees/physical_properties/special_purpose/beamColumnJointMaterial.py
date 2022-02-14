import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# Mat1
	at_Mat1 = MpcAttributeMetaData()
	at_Mat1.type = MpcAttributeType.Index
	at_Mat1.name = 'Mat1'
	at_Mat1.group = 'Group'
	at_Mat1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat1')+'<br/>') +
		html_par('uniaxial material tag for left bar-slip spring at node 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat1.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat1.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat2
	at_Mat2 = MpcAttributeMetaData()
	at_Mat2.type = MpcAttributeType.Index
	at_Mat2.name = 'Mat2'
	at_Mat2.group = 'Group'
	at_Mat2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat2')+'<br/>') +
		html_par('uniaxial material tag for right bar-slip spring at node 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat2.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat2.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat3
	at_Mat3 = MpcAttributeMetaData()
	at_Mat3.type = MpcAttributeType.Index
	at_Mat3.name = 'Mat3'
	at_Mat3.group = 'Group'
	at_Mat3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat3')+'<br/>') +
		html_par('uniaxial material tag for interface-shear spring at node 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat3.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat3.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat4
	at_Mat4 = MpcAttributeMetaData()
	at_Mat4.type = MpcAttributeType.Index
	at_Mat4.name = 'Mat4'
	at_Mat4.group = 'Group'
	at_Mat4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat4')+'<br/>') +
		html_par('uniaxial material tag for lower bar-slip spring at node 2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat4.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat4.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat5
	at_Mat5 = MpcAttributeMetaData()
	at_Mat5.type = MpcAttributeType.Index
	at_Mat5.name = 'Mat5'
	at_Mat5.group = 'Group'
	at_Mat5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat5')+'<br/>') +
		html_par('uniaxial material tag for upper bar-slip spring at node 2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat5.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat5.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat6
	at_Mat6 = MpcAttributeMetaData()
	at_Mat6.type = MpcAttributeType.Index
	at_Mat6.name = 'Mat6'
	at_Mat6.group = 'Group'
	at_Mat6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat6')+'<br/>') +
		html_par('uniaxial material tag for interface-shear spring at node 2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat6.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat6.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat7
	at_Mat7 = MpcAttributeMetaData()
	at_Mat7.type = MpcAttributeType.Index
	at_Mat7.name = 'Mat7'
	at_Mat7.group = 'Group'
	at_Mat7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat7')+'<br/>') +
		html_par('uniaxial material tag for left bar-slip spring at node 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat7.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat7.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat8
	at_Mat8 = MpcAttributeMetaData()
	at_Mat8.type = MpcAttributeType.Index
	at_Mat8.name = 'Mat8'
	at_Mat8.group = 'Group'
	at_Mat8.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat8')+'<br/>') +
		html_par('uniaxial material tag for right bar-slip spring at node 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat8.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat8.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat9
	at_Mat9 = MpcAttributeMetaData()
	at_Mat9.type = MpcAttributeType.Index
	at_Mat9.name = 'Mat9'
	at_Mat9.group = 'Group'
	at_Mat9.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat9')+'<br/>') +
		html_par('uniaxial material tag for interface-shear spring at node 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat9.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat9.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat10
	at_Mat10 = MpcAttributeMetaData()
	at_Mat10.type = MpcAttributeType.Index
	at_Mat10.name = 'Mat10'
	at_Mat10.group = 'Group'
	at_Mat10.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat10')+'<br/>') +
		html_par('uniaxial material tag for lower bar-slip spring at node 4') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat10.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat10.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat11
	at_Mat11 = MpcAttributeMetaData()
	at_Mat11.type = MpcAttributeType.Index
	at_Mat11.name = 'Mat11'
	at_Mat11.group = 'Group'
	at_Mat11.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat11')+'<br/>') +
		html_par('uniaxial material tag for upper bar-slip spring at node 4') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat11.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat11.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat12
	at_Mat12 = MpcAttributeMetaData()
	at_Mat12.type = MpcAttributeType.Index
	at_Mat12.name = 'Mat12'
	at_Mat12.group = 'Group'
	at_Mat12.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat12')+'<br/>') +
		html_par('uniaxial material tag for interface-shear spring at node 4') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat12.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat12.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Mat13
	at_Mat13 = MpcAttributeMetaData()
	at_Mat13.type = MpcAttributeType.Index
	at_Mat13.name = 'Mat13'
	at_Mat13.group = 'Group'
	at_Mat13.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mat13')+'<br/>') +
		html_par('uniaxial material tag for shear-panel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_Mat13.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Mat13.indexSource.addAllowedNamespace("materials.uniaxial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'beamColumnJointMaterial'
	xom.Xgroup = 'Joint Material'
	xom.addAttribute(at_Mat1)
	xom.addAttribute(at_Mat2)
	xom.addAttribute(at_Mat3)
	xom.addAttribute(at_Mat4)
	xom.addAttribute(at_Mat5)
	xom.addAttribute(at_Mat6)
	xom.addAttribute(at_Mat7)
	xom.addAttribute(at_Mat8)
	xom.addAttribute(at_Mat9)
	xom.addAttribute(at_Mat10)
	xom.addAttribute(at_Mat11)
	xom.addAttribute(at_Mat12)
	xom.addAttribute(at_Mat13)
	
	
	return xom