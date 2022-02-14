import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.physical_properties.special_purpose.beam_section_utils as bsutils
import opensees.physical_properties.sections.extrusion_utils as exutils

def makeXObjectMetaData():
	
	# integration
	at_integration = MpcAttributeMetaData()
	at_integration.type = MpcAttributeType.Boolean
	at_integration.name = '-integration'
	at_integration.group = 'Group'
	at_integration.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-integration')+'<br/>') +
		html_par('optional (available options = \'Lobatto\', \'Legendre\', \'Radau\', \'NewtonCotes\', \'Trapezoidal\' or \'CompositeSimpson\'; default = \'Legendre\')') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# IntegrationType
	at_IntegrationType = MpcAttributeMetaData()
	at_IntegrationType.type = MpcAttributeType.String
	at_IntegrationType.name = 'IntegrationType'
	at_IntegrationType.group = '-integration'
	at_IntegrationType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('optional (available options = \'Lobatto\', \'Legendre\', \'Radau\', \'NewtonCotes\', \'Trapezoidal\' or \'CompositeSimpson\'; default = \'Legendre\')') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_IntegrationType.sourceType = MpcAttributeSourceType.List
	at_IntegrationType.setSourceList(['Lobatto', 'Legendre', 'Radau', 'NewtonCotes', 'Trapezoidal', 'CompositeSimpson'])
	at_IntegrationType.setDefault('Lobatto')
	
	# section
	at_section = MpcAttributeMetaData()
	at_section.type = MpcAttributeType.String
	at_section.name = '-section'
	at_section.group = 'Group'
	at_section.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-section')+'<br/>') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_section.sourceType = MpcAttributeSourceType.List
	at_section.setSourceList(['Constant section', 'Multiple sections'])
	at_section.setDefault('Constant section')
	
	# Constant_section
	at_Constant_section = MpcAttributeMetaData()
	at_Constant_section.type = MpcAttributeType.Boolean
	at_Constant_section.name = 'Constant section'
	at_Constant_section.group = '-section'
	at_Constant_section.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Constant section')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_Constant_section.editable = False
	
	# Multiple_section
	at_Multiple_sections = MpcAttributeMetaData()
	at_Multiple_sections.type = MpcAttributeType.Boolean
	at_Multiple_sections.name = 'Multiple sections'
	at_Multiple_sections.group = '-section'
	at_Multiple_sections.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Multiple sections')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_Multiple_sections.editable = False
	
	# numIntgrPts
	at_numIntgrPts = MpcAttributeMetaData()
	at_numIntgrPts.type = MpcAttributeType.Integer
	at_numIntgrPts.name = 'numIntgrPts'
	at_numIntgrPts.group = 'Group'
	at_numIntgrPts.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIntgrPts')+'<br/>') +
		html_end()
		)
	at_numIntgrPts.setDefault(5)
	
	# secTag
	at_secTag = MpcAttributeMetaData()
	at_secTag.type = MpcAttributeType.Index
	at_secTag.name = 'secTag'
	at_secTag.group = '-section'
	at_secTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTag')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_secTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTag.indexSource.addAllowedNamespace("sections")
	
	
	# secTag_n
	at_secTag_n = MpcAttributeMetaData()
	at_secTag_n.type = MpcAttributeType.IndexVector
	at_secTag_n.name = 'secTag/n'
	at_secTag_n.group = '-section'
	at_secTag_n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTag')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_secTag_n.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTag_n.indexSource.addAllowedNamespace("sections")
	
	xom = MpcXObjectMetaData()
	xom.name = 'BeamSectionProperty(old)'
	xom.Xgroup = 'Beam-Column'
	xom.addAttribute(at_integration)
	xom.addAttribute(at_IntegrationType)
	xom.addAttribute(at_section)
	xom.addAttribute(at_Constant_section)
	xom.addAttribute(at_Multiple_sections)
	xom.addAttribute(at_secTag_n)
	xom.addAttribute(at_secTag)
	xom.addAttribute(at_numIntgrPts)
	
	xom.setVisibilityDependency(at_Constant_section, at_secTag)
	xom.setVisibilityDependency(at_Constant_section, at_numIntgrPts)
	xom.setVisibilityDependency(at_Multiple_sections, at_secTag_n)
	
	xom.setVisibilityDependency(at_integration, at_IntegrationType)
	
	xom.setBooleanAutoExclusiveDependency(at_section, at_Constant_section)
	xom.setBooleanAutoExclusiveDependency(at_section, at_Multiple_sections)
	
	return xom

def makeExtrusionBeamDataCompoundInfo(xobj):
	
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
	
	info = MpcSectionExtrusionBeamDataCompoundInfo()
	'''
	here we may have 1 or multiple cross sections. 
	If we have only 1 cross section return an info with just 1 item, 
	regardless of the integration rule
	since this is fine for visualization purposes (i.e. the cross section does not change along
	the curve).
	If we have multiple cross section we also need to get information
	about the integraton rule to give a meaningful representation of the
	variation of the cross section along the curve.
	Note that the references properties may or may not have a cross section
	representation (they have it if they are for example Elastic Fiber or Aggregator with Fiber).
	To make sure the referenced properties have a representation, we check for the 
	makeExtrusionBeamDataCompoundInfo in their xobject
	'''
	at_Constant_section = xobj.getAttribute('Constant section')
	if(at_Constant_section is None):
		raise Exception('Error: cannot find "Constant section" attribute')
	Constant_section = at_Constant_section.boolean
	
	if Constant_section:
		'''
		case 1: single section
		'''
		at_secTag = xobj.getAttribute('secTag')
		if(at_secTag is None):
			raise Exception('Error: cannot find "secTag" attribute')
		secTag = at_secTag.index
		prop = doc.getPhysicalProperty(secTag)
		info_item = exutils.getExtrusionDataSingleItem(prop)
		info.add(info_item.property, 1.0, True, False, info_item.yOffset, info_item.zOffset)
	else :
		'''
		case 2: multiple sections
		'''
		at_secTag_n = xobj.getAttribute('secTag/n')
		if(at_secTag_n is None):
			raise Exception('Error: cannot find "secTag/n" attribute')
		secTag_n = at_secTag_n.indexVector
		n = len(secTag_n) # number of cross sections
		if n == 0:
			return info # quick return
		'''
		here we allow some of the n properties to be None. but not all of them!
		'''
		num_valid = 0
		processed_info_items = [None]*n
		for i in range(n):
			prop = doc.getPhysicalProperty(secTag_n[i])
			info_item = exutils.getExtrusionDataSingleItem(prop)
			processed_info_items[i] = info_item
			if info_item is not None:
				num_valid += 1
		if num_valid == 0:
			return info # quick return
		'''
		get integration weights
		'''
		at_IntegrationType = xobj.getAttribute('IntegrationType')
		if(at_IntegrationType is None):
			raise Exception('Error: cannot find "IntegrationType" attribute')
		IntegrationType = at_IntegrationType.string
		weights = bsutils.integration_rule_registry.STANDARD_RULES[IntegrationType].get_weights(n)
		'''
		fill info
		'''
		exutils.checkOffsetCompatibility(processed_info_items)
		for i in range(n):
			info_item = processed_info_items[i]
			info.add(info_item.property, weights[i], True, False, info_item.yOffset, info_item.zOffset)
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