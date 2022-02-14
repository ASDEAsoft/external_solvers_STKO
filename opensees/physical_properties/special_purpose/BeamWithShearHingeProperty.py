import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.physical_properties.sections.extrusion_utils as exutils

def makeXObjectMetaData():
	
	# beam
	at_beam = MpcAttributeMetaData()
	at_beam.type = MpcAttributeType.Index
	at_beam.name = 'Beam Property'
	at_beam.group = 'Group'
	at_beam.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Beam Property')+'<br/>') +
		html_par('Choose a valid Beam Physical Property') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_beam.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	
	# Vy
	at_vy = MpcAttributeMetaData()
	at_vy.type = MpcAttributeType.Index
	at_vy.name = 'Vy Material'
	at_vy.group = 'Group'
	at_vy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Vy Material')+'<br/>') +
		html_par(
			'A uniaxial material for the Vy shear response (local Y direction).<br>'
			'It should be a Force-Displacement relationship.') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_vy.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_vy.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# Vz
	at_vz = MpcAttributeMetaData()
	at_vz.type = MpcAttributeType.Index
	at_vz.name = 'Vz Material'
	at_vz.group = 'Group'
	at_vz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Vz Material')+'<br/>') +
		html_par(
			'A uniaxial material for the Vy shear response (local Z direction).<br>'
			'It should be a Force-Displacement relationship.') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_vz.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_vz.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# K
	at_K = MpcAttributeMetaData()
	at_K.type = MpcAttributeType.Real
	at_K.name = 'K'
	at_K.group = 'Group'
	at_K.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K')+'<br/>') +
		html_par(
			'A Penalty stiffness value to enforce continuity in the P-My-Mz-T DOFs.<br>'
			'This value should be large enough to enforce continuity, but not too large otherwise the system will be ill-conditioned.<br>'
			'You can use a value that is 2 or 3 orders of magnitute larger than max(EA, EIyy, EIzz, GJ)') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_K.setDefault(1.0e12)
	
	xom = MpcXObjectMetaData()
	xom.name = 'BeamWithShearHingeProperty'
	xom.Xgroup = 'Beam-Column'
	xom.addAttribute(at_beam)
	xom.addAttribute(at_vy)
	xom.addAttribute(at_vz)
	xom.addAttribute(at_K)
	
	return xom

def makeExtrusionBeamDataCompoundInfo(xobj):
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
	info = MpcSectionExtrusionBeamDataCompoundInfo()
	at_beam = xobj.getAttribute('Beam Property')
	if(at_beam is None):
		raise Exception('Error: cannot find "PP_Beam" attribute')
	beam = at_beam.index
	# get extrusion info for the inner beam property
	inner_items = exutils.getExtrusionDataAllItems(doc.getPhysicalProperty(beam))
	if inner_items and len(inner_items) > 0:
		exutils.checkOffsetCompatibility(inner_items)
		for item in inner_items:
			info.add(item.property, item.weight, item.isParametric, False, item.yOffset, item.zOffset)
	return info

def getSectionOffset(xobj):
	offset_y = 0.0
	offset_z = 0.0
	info = makeExtrusionBeamDataCompoundInfo(xobj)
	if info is not None:
		if len(info.items) > 0:
			item = info.items[0]
			offset_y = item.yOffset
			offset_z = item.zOffset
	return offset_y, offset_z