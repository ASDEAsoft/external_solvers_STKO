import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.physical_properties.sections.offset_utils as ofu
import opensees.physical_properties.sections.extrusion_utils as exutils

def makeXObjectMetaData():
	
	# P
	at_P = MpcAttributeMetaData()
	at_P.type = MpcAttributeType.Boolean
	at_P.name = 'P'
	at_P.group = 'dof'
	at_P.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('P')+'<br/>') + 
		html_par('P Axial force-deformation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	
	#matTagP
	at_matTagP = MpcAttributeMetaData()
	at_matTagP.type = MpcAttributeType.Index
	at_matTagP.name = 'matTagP'
	at_matTagP.group = 'Material'
	at_matTagP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagP')+'<br/>') + 
		html_par('tag of previously-defined UniaxialMaterial objects') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_matTagP.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagP.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# Mz
	at_Mz = MpcAttributeMetaData()
	at_Mz.type = MpcAttributeType.Boolean
	at_Mz.name = 'Mz'
	at_Mz.group = 'dof'
	at_Mz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mz')+'<br/>') + 
		html_par('the force-deformation quantity to be modeled by this section object.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	
	# matTagMz
	at_matTagMz = MpcAttributeMetaData()
	at_matTagMz.type = MpcAttributeType.Index
	at_matTagMz.name = 'matTagMz'
	at_matTagMz.group = 'Material'
	at_matTagMz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagMz')+'<br/>') + 
		html_par('tag of previously-defined UniaxialMaterial objects') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_matTagMz.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagMz.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# Vy
	at_Vy = MpcAttributeMetaData()
	at_Vy.type = MpcAttributeType.Boolean
	at_Vy.name = 'Vy'
	at_Vy.group = 'dof'
	at_Vy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Vy')+'<br/>') + 
		html_par('the force-deformation quantity to be modeled by this section object.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	
	# matTagVy
	at_matTagVy = MpcAttributeMetaData()
	at_matTagVy.type = MpcAttributeType.Index
	at_matTagVy.name = 'matTagVy'
	at_matTagVy.group = 'Material'
	at_matTagVy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagVy')+'<br/>') + 
		html_par('tag of previously-defined UniaxialMaterial objects') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_matTagVy.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagVy.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# My
	at_My = MpcAttributeMetaData()
	at_My.type = MpcAttributeType.Boolean
	at_My.name = 'My'
	at_My.group = 'dof'
	at_My.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('My')+'<br/>') + 
		html_par('the force-deformation quantity to be modeled by this section object.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	
	# matTagMy
	at_matTagMy = MpcAttributeMetaData()
	at_matTagMy.type = MpcAttributeType.Index
	at_matTagMy.name = 'matTagMy'
	at_matTagMy.group = 'Material'
	at_matTagMy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagMy')+'<br/>') + 
		html_par('tag of previously-defined UniaxialMaterial objects') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_matTagMy.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagMy.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# Vz
	at_Vz = MpcAttributeMetaData()
	at_Vz.type = MpcAttributeType.Boolean
	at_Vz.name = 'Vz'
	at_Vz.group = 'dof'
	at_Vz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Vz')+'<br/>') + 
		html_par('the force-deformation quantity to be modeled by this section object.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	
	# matTagVz
	at_matTagVz = MpcAttributeMetaData()
	at_matTagVz.type = MpcAttributeType.Index
	at_matTagVz.name = 'matTagVz'
	at_matTagVz.group = 'Material'
	at_matTagVz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagVz')+'<br/>') + 
		html_par('tag of previously-defined UniaxialMaterial objects') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_matTagVz.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagVz.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# T
	at_T = MpcAttributeMetaData()
	at_T.type = MpcAttributeType.Boolean
	at_T.name = 'T'
	at_T.group = 'dof'
	at_T.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('T')+'<br/>') + 
		html_par('the force-deformation quantity to be modeled by this section object.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	
	# matTagT
	at_matTagT = MpcAttributeMetaData()
	at_matTagT.type = MpcAttributeType.Index
	at_matTagT.name = 'matTagT'
	at_matTagT.group = 'Material'
	at_matTagT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagT')+'<br/>') + 
		html_par('tag of previously-defined UniaxialMaterial objects') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_matTagT.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagT.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# sectionTag
	at_sectionTag = MpcAttributeMetaData()
	at_sectionTag.type = MpcAttributeType.Index
	at_sectionTag.name = 'sectionTag'
	at_sectionTag.group = '-section'
	at_sectionTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sectionTag')+'<br/>') + 
		html_par('tag of previously-defined Section object to which the UniaxialMaterial objects are aggregated as additional force-deformation relationships') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_sectionTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_sectionTag.indexSource.addAllowedNamespace('sections')
	at_sectionTag.indexSource.addAllowedClass('Elastic')
	at_sectionTag.indexSource.addAllowedClass('Fiber')
	at_sectionTag.indexSource.addAllowedClass('RectangularFiberSection')
	
	# UseSectionTag
	at_UseSectionTag = MpcAttributeMetaData()
	at_UseSectionTag.type = MpcAttributeType.Boolean
	at_UseSectionTag.name = 'UseSectionTag'
	at_UseSectionTag.group = 'Optional parameters'
	at_UseSectionTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('UseSectionTag')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_UseSectionTag.editable = False
	
	# DoNotUseSectionTag
	at_DoNotUseSectionTag = MpcAttributeMetaData()
	at_DoNotUseSectionTag.type = MpcAttributeType.Boolean
	at_DoNotUseSectionTag.name = 'DoNotUseSectionTag'
	at_DoNotUseSectionTag.group = 'Optional parameters'
	at_DoNotUseSectionTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('DoNotUseSectionTag')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_DoNotUseSectionTag.editable = False
	
	# -section
	at_section = MpcAttributeMetaData()
	at_section.type = MpcAttributeType.String
	at_section.name = '-section'
	at_section.group = 'Optional parameters'
	at_section.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-section')+'<br/>') + 
		html_par('Choose between UseSectionTag and DoNotUseSectionTag') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Section_Aggregator','Section Aggregator')+'<br/>') +
		html_end()
		)
	at_section.sourceType = MpcAttributeSourceType.List
	at_section.setSourceList(['UseSectionTag', 'DoNotUseSectionTag'])
	at_section.setDefault('DoNotUseSectionTag')
	
	xom = MpcXObjectMetaData()
	xom.name = 'Aggregator'
	xom.addAttribute(at_P)
	xom.addAttribute(at_matTagP)
	xom.addAttribute(at_Mz)
	xom.addAttribute(at_matTagMz)
	xom.addAttribute(at_Vy)
	xom.addAttribute(at_matTagVy)
	xom.addAttribute(at_My)
	xom.addAttribute(at_matTagMy)
	xom.addAttribute(at_Vz)
	xom.addAttribute(at_matTagVz)
	xom.addAttribute(at_T)
	xom.addAttribute(at_matTagT)
	xom.addAttribute(at_DoNotUseSectionTag)
	xom.addAttribute(at_UseSectionTag)
	xom.addAttribute(at_sectionTag)
	xom.addAttribute(at_section)
	
	
	# visibility dependencies
	
	# dof1-dep
	xom.setVisibilityDependency(at_P, at_matTagP)
	# dof2-dep
	xom.setVisibilityDependency(at_Mz, at_matTagMz)
	# dof3-dep
	xom.setVisibilityDependency(at_Vy, at_matTagVy)
	# dof4-dep
	xom.setVisibilityDependency(at_My, at_matTagMy)
	# dof5-dep
	xom.setVisibilityDependency(at_Vz, at_matTagVz)
	# dof6-dep
	xom.setVisibilityDependency(at_T, at_matTagT)
	
	# P_Mz_My-dep
	xom.setVisibilityDependency(at_DoNotUseSectionTag, at_P)
	xom.setVisibilityDependency(at_DoNotUseSectionTag, at_matTagP)
	xom.setVisibilityDependency(at_DoNotUseSectionTag, at_Mz)
	xom.setVisibilityDependency(at_DoNotUseSectionTag, at_matTagMz)
	xom.setVisibilityDependency(at_DoNotUseSectionTag, at_My)
	xom.setVisibilityDependency(at_DoNotUseSectionTag, at_matTagMy)
	
	# sectionTag-dep
	xom.setVisibilityDependency(at_UseSectionTag, at_sectionTag)
	
	
	# auto-exclusive dependencies
	# UseSectionTag or DoNotUseSectionTag
	xom.setBooleanAutoExclusiveDependency(at_section, at_DoNotUseSectionTag)
	xom.setBooleanAutoExclusiveDependency(at_section, at_UseSectionTag)
	
	return xom

def __get_section_prop(xobj):
	UseSectionTag_at = xobj.getAttribute('UseSectionTag')
	if(UseSectionTag_at is None):
		raise Exception('Error: cannot find "UseSectionTag" attribute')
	if not UseSectionTag_at.boolean:
		return None
	sectionTag_at = xobj.getAttribute('sectionTag')
	if(sectionTag_at is None):
		raise Exception('Error: cannot find "sectionTag" attribute')
	sectionTag = sectionTag_at.index
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
	prop = doc.getPhysicalProperty(sectionTag)
	return prop
	
def makeExtrusionBeamDataCompoundInfo(xobj):
	
	info = MpcSectionExtrusionBeamDataCompoundInfo()
	'''
	here the property that has the extrusion source (MpcBeamFiberSection)
	is the property whose id is stored in the attribute 'sectionTag', and not
	this property (Aggregator). So we first get the attribute and check
	whether the user decided to use a fiber beam cross section for the P-My-Mz part
	of the Aggregator. If so, get the indexed property from the document. That
	will be the one containing the extrusion source. See the opensees.physical_properties.sections.Fiber.py module.
	'''
	prop = __get_section_prop(xobj)
	if prop:
		info_item = exutils.getExtrusionDataSingleItem(prop)
	else:
		# use parent propery of this aggregator
		# and make a fake info_item
		info_item = MpcSectionExtrusionBeamDataCompoundInfoItem()
		info_item.property = xobj.parent
	info.add(info_item.property, 1.0, True, False, info_item.yOffset, info_item.zOffset)
	
	return info

def getSectionOffset(xobj):
	prop = __get_section_prop(xobj)
	offset_y = 0.0
	offset_z = 0.0
	odata = ofu.getOffsetData(prop.XObject)
	if odata:
		offset_y = odata.y
		offset_z = odata.z
	return offset_y, offset_z

def writeTcl(pinfo):
	
	#section Aggregator $secTag $matTag1 $dof1 $matTag2 $dof2 ....... <-section $sectionTag>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	sopt = ''
	
	DoNotUseSectionTag_at = xobj.getAttribute('DoNotUseSectionTag')
	if(DoNotUseSectionTag_at is None):
		raise Exception('Error: cannot find "DoNotUseSectionTag" attribute')
	DoNotUseSectionTag = DoNotUseSectionTag_at.boolean
	
	UseSectionTag_at = xobj.getAttribute('UseSectionTag')
	if(UseSectionTag_at is None):
		raise Exception('Error: cannot find "UseSectionTag" attribute')
	UseSectionTag = UseSectionTag_at.boolean
	
	P_at = xobj.getAttribute('P')
	if(P_at is None):
		raise Exception('Error: cannot find "P" attribute')
	P = P_at.boolean
	if (P and DoNotUseSectionTag):
		matTagP_at = xobj.getAttribute('matTagP')
		if(matTagP_at is None):
			raise Exception('Error: cannot find "matTagP" attribute')
		sopt += ' {} P'.format(matTagP_at.index)
	
	Mz_at = xobj.getAttribute('Mz')
	if(Mz_at is None):
		raise Exception('Error: cannot find "Mz" attribute')
	Mz = Mz_at.boolean
	if (Mz and DoNotUseSectionTag):
		matTagMz_at = xobj.getAttribute('matTagMz')
		if(matTagMz_at is None):
			raise Exception('Error: cannot find "matTagMz" attribute')
		sopt += ' {} Mz'.format(matTagMz_at.index)
	
	Vy_at = xobj.getAttribute('Vy')
	if(Vy_at is None):
		raise Exception('Error: cannot find "Vy" attribute')
	Vy = Vy_at.boolean
	if Vy:
		matTagVy_at = xobj.getAttribute('matTagVy')
		if(matTagVy_at is None):
			raise Exception('Error: cannot find "matTagVy" attribute')
		sopt += ' {} Vy'.format(matTagVy_at.index)
	
	My_at = xobj.getAttribute('My')
	if(My_at is None):
		raise Exception('Error: cannot find "My" attribute')
	My = My_at.boolean
	if (My and DoNotUseSectionTag):
		matTagMy_at = xobj.getAttribute('matTagMy')
		if(matTagMy_at is None):
			raise Exception('Error: cannot find "matTagMy" attribute')
		sopt += ' {} My'.format(matTagMy_at.index)
	
	Vz_at = xobj.getAttribute('Vz')
	if(Vz_at is None):
		raise Exception('Error: cannot find "Vz" attribute')
	Vz = Vz_at.boolean
	if Vz:
		matTagVz_at = xobj.getAttribute('matTagVz')
		if(matTagVz_at is None):
			raise Exception('Error: cannot find "matTagVz" attribute')
		sopt += ' {} Vz'.format(matTagVz_at.index)
		
	T_at = xobj.getAttribute('T')
	if(T_at is None):
		raise Exception('Error: cannot find "T" attribute')
	T = T_at.boolean
	if T:
		matTagT_at = xobj.getAttribute('matTagT')
		if(matTagT_at is None):
			raise Exception('Error: cannot find "matTagT" attribute')
		sopt += ' {} T'.format(matTagT_at.index)
	
	if UseSectionTag:
		sectionTag_at = xobj.getAttribute('sectionTag')
		if(sectionTag_at is None):
			raise Exception('Error: cannot find "sectionTag" attribute')
		sectionTag = sectionTag_at.index
		sopt += ' -section {}'.format(sectionTag)
	
	str_tcl = '{}section Aggregator {}{}\n'.format(pinfo.indent, tag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)