import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# vertMatTag
	at_vertMatTag = MpcAttributeMetaData()
	at_vertMatTag.type = MpcAttributeType.Index
	at_vertMatTag.name = 'vertMatTag'
	at_vertMatTag.group = 'Group'
	at_vertMatTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vertMatTag')+'<br/>') +
		html_par('Pre-defined material tag for COMPRESSION behavior of the bearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_vertMatTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_vertMatTag.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# rotZMatTag
	at_rotZMatTag = MpcAttributeMetaData()
	at_rotZMatTag.type = MpcAttributeType.Index
	at_rotZMatTag.name = 'rotZMatTag'
	at_rotZMatTag.group = 'Group'
	at_rotZMatTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rotZMatTag')+'<br/>') +
		html_par('Pre-defined material tags for rotational behavior about 3-axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_rotZMatTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_rotZMatTag.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# rotXMatTag
	at_rotXMatTag = MpcAttributeMetaData()
	at_rotXMatTag.type = MpcAttributeType.Index
	at_rotXMatTag.name = 'rotXMatTag'
	at_rotXMatTag.group = 'Group'
	at_rotXMatTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rotXMatTag')+'<br/>') +
		html_par('Pre-defined material tags for rotational behavior about 1-axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_rotXMatTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_rotXMatTag.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# rotYMatTag
	at_rotYMatTag = MpcAttributeMetaData()
	at_rotYMatTag.type = MpcAttributeType.Index
	at_rotYMatTag.name = 'rotYMatTag'
	at_rotYMatTag.group = 'Group'
	at_rotYMatTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rotYMatTag')+'<br/>') +
		html_par('Pre-defined material tags for rotational behavior about 2-axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_rotYMatTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_rotYMatTag.indexSource.addAllowedNamespace("materials.uniaxial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'TripleFrictionPendulumMaterial'
	xom.Xgroup = 'Bearing Material'
	xom.addAttribute(at_vertMatTag)
	xom.addAttribute(at_rotZMatTag)
	xom.addAttribute(at_rotXMatTag)
	xom.addAttribute(at_rotYMatTag)
	
	
	return xom