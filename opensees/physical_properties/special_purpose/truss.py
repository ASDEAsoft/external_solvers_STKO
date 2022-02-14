import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.physical_properties.special_purpose.beam_section_utils as bsutils
import opensees.physical_properties.sections.extrusion_utils as exutils

def makeXObjectMetaData():
	
	# type
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.String
	at_type.name = 'type'
	at_type.group = 'Group'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') + 
		html_par('select "trussSection" or "truss"') +
		html_par('This command is used to construct a pysical property for the truss element object.<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList(['trussSection', 'truss'])
	at_type.setDefault('trussSection')
	
	# truss
	at_truss = MpcAttributeMetaData()
	at_truss.type = MpcAttributeType.Boolean
	at_truss.name = 'truss'
	at_truss.group = 'Group'
	at_truss.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('truss')+'<br/>') + 
		html_end()
		)
	at_truss.editable = False
	
	# trussSection
	at_trussSection = MpcAttributeMetaData()
	at_trussSection.type = MpcAttributeType.Boolean
	at_trussSection.name = 'trussSection'
	at_trussSection.group = 'Group'
	at_trussSection.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('trussSection')+'<br/>') + 
		html_end()
		)
	at_trussSection.editable = False
	
	# secTag
	at_secTag = MpcAttributeMetaData()
	at_secTag.type = MpcAttributeType.Index
	at_secTag.name = 'secTag/truss'
	at_secTag.group = 'Group'
	at_secTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('section')+'<br/>') +
		html_par('Select a previously defined section') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')+'<br/>') +
		html_end()
		)
	at_secTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTag.indexSource.addAllowedNamespace("sections")
	
	# elastic_Section
	at_elastic_Section = MpcAttributeMetaData()
	at_elastic_Section.type = MpcAttributeType.CustomAttributeObject
	at_elastic_Section.name = 'elastic_Section'
	at_elastic_Section.group = 'Section'
	at_elastic_Section.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('elastic_Section')+'<br/>') + 
		html_par('Press the edit button to edit the cross section.<br/>This section will be used only to compute the Area of the truss.<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')+'<br/>') +
		html_end()
		)
	at_elastic_Section.customObjectPrototype = MpcBeamSection()
	
	# uniTag
	at_uniTag = MpcAttributeMetaData()
	at_uniTag.type = MpcAttributeType.Index
	at_uniTag.name = 'uniTag/truss'
	at_uniTag.group = 'Group'
	at_uniTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('uniTag')+'<br/>') +
		html_par('Select a previously defined uniaxial material.<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')+'<br/>') +
		html_end()
		)
	at_uniTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_uniTag.indexSource.addAllowedNamespace("materials.uniaxial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'truss'
	xom.Xgroup = 'truss'
	xom.addAttribute(at_type)
	xom.addAttribute(at_truss)
	xom.addAttribute(at_trussSection)
	xom.addAttribute(at_elastic_Section)
	xom.addAttribute(at_secTag)
	xom.addAttribute(at_uniTag)
	
	xom.setVisibilityDependency(at_trussSection, at_secTag)
	
	xom.setVisibilityDependency(at_truss, at_uniTag)
	xom.setVisibilityDependency(at_truss, at_elastic_Section)
	
	xom.setBooleanAutoExclusiveDependency(at_type, at_truss)
	xom.setBooleanAutoExclusiveDependency(at_type, at_trussSection)
	
	return xom

def makeExtrusionBeamDataCompoundInfo(xobj):
	
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
	
	info = MpcSectionExtrusionBeamDataCompoundInfo()
	'''
	here the property that has the extrusion source (MpcBeamSection)
	is the xobject parent itself
	'''
	
	use_truss = xobj.getAttribute('truss')
	if(use_truss is None):
		raise Exception('Error: cannot find "truss" attribute')
	if use_truss.boolean:
		if xobj.parent is not None:
			parent_id = xobj.parent.componentId
			prop = doc.getPhysicalProperty(parent_id)
			if prop is not None:
				info.add(prop, 1.0)
	else:
		at_secTag = xobj.getAttribute('secTag/truss')
		if(at_secTag is None):
			raise Exception('Error: cannot find "secTag/truss" attribute')
		secTag = at_secTag.index
		prop = doc.getPhysicalProperty(secTag)
		info_item = exutils.getExtrusionDataSingleItem(prop)
		if info_item is not None:
			info.add(info_item.property, 1.0, True, False, info_item.yOffset, info_item.zOffset)
	
	return info