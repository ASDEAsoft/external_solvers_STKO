import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.physical_properties.sections.offset_utils as ofu

def makeXObjectMetaData():
	
	#2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Fiber section'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') + 
		html_par('Analysis 2D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_2D.editable = False
	
	#3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Fiber section'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') + 
		html_par('Analysis 3D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fiber_Section','Fiber Section')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Fiber section'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par('Choose between 2D and 3D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fiber_Section','Fiber Section')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('3D')
	
	# Section
	at_Section = MpcAttributeMetaData()
	at_Section.type = MpcAttributeType.CustomAttributeObject
	at_Section.name = 'Fiber section'
	at_Section.group = 'Fiber section'
	at_Section.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Section')+'<br/>') + 
		html_par('Press the edit button to edit the fiber cross section') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fiber_Section','Fiber Section')+'<br/>') +
		html_end()
		)
	at_Section.customObjectPrototype = MpcBeamFiberSection()
	at_Section.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Section.indexSource.addAllowedNamespace('materials.uniaxial') # we want uniaxial materials for fibers
	
	# -GJ
	at_use_GJ = MpcAttributeMetaData()
	at_use_GJ.type = MpcAttributeType.Boolean
	at_use_GJ.name = '-GJ'
	at_use_GJ.group = 'Optional parameters'
	at_use_GJ.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-GJ')+'<br/>') + 
		html_par('use linear-elastic torsional') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fiber_Section','Fiber Section')+'<br/>') +
		html_end()
		)
	at_use_GJ.visible = False
	at_use_GJ.editable = False
	at_use_GJ.setDefault(True)
	
	# -torsion
	at_use_torsion = MpcAttributeMetaData()
	at_use_torsion.type = MpcAttributeType.Boolean
	at_use_torsion.name = '-torsion'
	at_use_torsion.group = 'Optional parameters'
	at_use_torsion.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-torsion')+'<br/>') + 
		html_par('Specify a uniaxial material for torsion') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fiber_Section','Fiber Section')+'<br/>') +
		html_end()
		)
	at_use_torsion.visible = False
	at_use_torsion.editable = False
	at_use_torsion.setDefault(False)
	
	# Torsion
	at_Torsion = MpcAttributeMetaData()
	at_Torsion.type = MpcAttributeType.String
	at_Torsion.name = 'Torsion'
	at_Torsion.group = 'Optional parameters'
	at_Torsion.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Torsion')+'<br/>') + 
		html_par('Choose between -GJ and -torsion') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fiber_Section','Fiber Section')+'<br/>') +
		html_end()
		)
	at_Torsion.sourceType = MpcAttributeSourceType.List
	at_Torsion.setSourceList(['-GJ', '-torsion'])
	at_Torsion.setDefault('-GJ')
	# GJ
	at_GJ = MpcAttributeMetaData()
	at_GJ.type = MpcAttributeType.QuantityScalar
	at_GJ.name = 'GJ'
	at_GJ.group = 'Optional parameters'
	at_GJ.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('GJ')+'<br/>') + 
		html_par('linear-elastic torsional stiffness assigned to the section') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fiber_Section','Fiber Section')+'<br/>') +
		html_end()
		)
	at_GJ.dimension = u.F/u.L**2 * u.L**4
	
	# torsionMatTag
	at_mat_torsion = MpcAttributeMetaData()
	at_mat_torsion.type = MpcAttributeType.Index
	at_mat_torsion.name = 'torsionMatTag'
	at_mat_torsion.group = 'Optional parameters'
	at_mat_torsion.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('torsionMatTag')+'<br/>') + 
		html_par('uniaxialMaterial tag assigned to the section for torsional response (can be nonlinear)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fiber_Section','Fiber Section')+'<br/>') +
		html_end()
		)
	at_mat_torsion.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_mat_torsion.indexSource.addAllowedNamespace("materials.uniaxial")
 
	xom = MpcXObjectMetaData()
	xom.name = 'Fiber'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_Section)
	xom.addAttribute(at_use_GJ)
	xom.addAttribute(at_use_torsion)
	xom.addAttribute(at_Torsion)
	xom.addAttribute(at_GJ)
	xom.addAttribute(at_mat_torsion)
	
	# auto-exclusive dependencies
	# Dimension
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	# Torsion
	xom.setBooleanAutoExclusiveDependency(at_Torsion, at_use_GJ)
	xom.setBooleanAutoExclusiveDependency(at_Torsion, at_use_torsion)
	
	# add offset
	ofu.addOffsetMetaData(xom, dep_3d = at_3D)
	
	# visibility dependencies
	xom.setVisibilityDependency(at_use_GJ, at_GJ)
	xom.setVisibilityDependency(at_use_torsion, at_mat_torsion)
	return xom

def makeExtrusionBeamDataCompoundInfo(xobj):
	
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
	
	# common
	is_param = True
	is_gap = False
	offset_y, offset_z = getSectionOffset(xobj)
	
	info = MpcSectionExtrusionBeamDataCompoundInfo()
	'''
	here the property that has the extrusion source (MpcBeamFiberSection)
	is the xobject parent itself
	'''
	if xobj.parent is not None:
		parent_id = xobj.parent.componentId
		prop = doc.getPhysicalProperty(parent_id)
		if prop is not None:
			info.add(prop, 1.0, is_param, is_gap, offset_y, offset_z)
	
	return info

def getSectionOffset(xobj):
	offset_y = 0.0
	offset_z = 0.0
	odata = ofu.getOffsetData(xobj)
	if odata:
		offset_y = odata.y
		offset_z = odata.z
	return offset_y, offset_z

def writeTcl (pinfo):
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	sopt = ''
	
	at_use_GJ = xobj.getAttribute('-GJ')
	if(at_use_GJ is None):
		raise Exception('Error: cannot find "-GJ" attribute')
	if at_use_GJ.boolean:
		at_GJ = xobj.getAttribute('GJ')
		if(at_GJ is None):
			raise Exception('Error: cannot find "GJ" attribute')
		GJ = at_GJ.quantityScalar
		
		sopt = ' -GJ {}'.format(GJ.value)
	at_use_torsion = xobj.getAttribute('-torsion')
	if(at_use_torsion is None):
		raise Exception('Error: cannot find "-torsion" attribute')
	if at_use_torsion.boolean:
		at_mat_torsion = xobj.getAttribute('torsionMatTag')
		if(at_mat_torsion is None):
			raise Exception('Error: cannot find "torsionMatTag" attribute')
		torsionMatTag = at_mat_torsion.index
		
		sopt = ' -torsion {}'.format(torsionMatTag)
	
	at_Section = xobj.getAttribute('Fiber section')
	if(at_Section is None):
		raise Exception('Error: cannot find "Fiber section" attribute')
	Section = at_Section.customObject
	
	if Section is None:
		raise Exception('Error: Section is None')
	
	cx = Section.centroid.x
	cy = Section.centroid.y
	sopt1 = ''
	for group in Section.punctualFibers:
		for fiber in group.fibers.fibers:
			sopt1 +='\nfiber {} {} {} {}'.format(fiber.x-cx, fiber.y-cy, fiber.area, group.material.id)
	sopt2 = ''
	for group in Section.surfaceFibers:
		for fiber in group.fibers.fibers:
			sopt2 +='\nfiber {} {} {} {}'.format(fiber.x-cx, fiber.y-cy, fiber.area, group.material.id)
	sopt3 = ''
	for group in Section.linearFibers:
		for fiber in group.fibers.fibers:
			sopt3 +='\nfiber {} {} {} {}'.format(fiber.x-cx, fiber.y-cy, fiber.area, group.material.id)
	
	str_tcl = '\n{}section Fiber {}{}'.format(pinfo.indent, tag, sopt)
	str_tcl += '{}{}{}{}{}\n'.format(' {',sopt1,sopt2,sopt3,'}')
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)