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
	at_2D.group = 'Section'
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
	at_3D.group = 'Section'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') + 
		html_par('Analysis 3D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Section'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par('Choose between 2D and 3D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('3D')
	
	# Section
	at_Section = MpcAttributeMetaData()
	at_Section.type = MpcAttributeType.CustomAttributeObject
	at_Section.name = 'Section'
	at_Section.group = 'Section'
	at_Section.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Section')+'<br/>') + 
		html_par('Press the edit button to edit the cross section') +
		html_end()
		)
	at_Section.customObjectPrototype = MpcBeamSection()
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Material properties'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('Young\'s Modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# G_2D
	at_G_2D = MpcAttributeMetaData()
	at_G_2D.type = MpcAttributeType.QuantityScalar
	at_G_2D.name = 'G/2D'
	at_G_2D.group = 'Material properties'
	at_G_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('G')+'<br/>') + 
		html_par('Shear Modulus (optional for 2D analysis)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_G_2D.dimension = u.F/u.L**2
	
	# G_3D
	at_G_3D = MpcAttributeMetaData()
	at_G_3D.type = MpcAttributeType.QuantityScalar
	at_G_3D.name = 'G/3D'
	at_G_3D.group = 'Material properties'
	at_G_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('G')+'<br/>') + 
		html_par('Shear Modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_G_3D.dimension = u.F/u.L**2
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Options'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('Tick this value to use optional parameters (&lt;alphaY&gt; for 2D or &lt;alphaY, alphaZ&gt; for 3D)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	
	# Izz_modifier
	at_Izz_modifier = MpcAttributeMetaData()
	at_Izz_modifier.type = MpcAttributeType.Real
	at_Izz_modifier.name = 'Izz_modifier'
	at_Izz_modifier.group = 'Stiffness modifiers'
	at_Izz_modifier.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Izz_modifier')+'<br/>') + 
		html_par('Scale factor for bending stiffness about Z local axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_Izz_modifier.setDefault(1.0)
	
	# Iyy_modifier
	at_Iyy_modifier = MpcAttributeMetaData()
	at_Iyy_modifier.type = MpcAttributeType.Real
	at_Iyy_modifier.name = 'Iyy_modifier'
	at_Iyy_modifier.group = 'Stiffness modifiers'
	at_Iyy_modifier.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Iyy_modifier')+'<br/>') + 
		html_par('Scale factor for bending stiffness about Y local axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_Iyy_modifier.setDefault(1.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Elastic'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_Section)
	#material params
	xom.addAttribute(at_E)
	xom.addAttribute(at_G_2D)
	xom.addAttribute(at_G_3D)
	# options
	xom.addAttribute(at_Optional)
	# modifiers
	xom.addAttribute(at_Izz_modifier)
	xom.addAttribute(at_Iyy_modifier)
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_G_2D)
	
	# 2D-dep
	xom.setVisibilityDependency(at_2D, at_G_2D)
	# 3D-dep
	xom.setVisibilityDependency(at_3D, at_G_3D)
	xom.setVisibilityDependency(at_3D, at_Iyy_modifier)
	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	# add offset
	ofu.addOffsetMetaData(xom, dep_3d = at_3D)
	
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
	here the property that has the extrusion source (MpcBeamSection)
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

def writeTcl(pinfo):
	
	#2D
	#section Elastic $secTag $E $A $Iz <$G $alphaY>
	
	#3D
	#section Elastic $secTag $E $A $Iz $Iy $G $J <$alphaY $alphaZ>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	at_E = xobj.getAttribute('E')
	if(at_E is None):
		raise Exception('Error: cannot find "E" attribute')
	E = at_E.quantityScalar
	
	at_Optional = xobj.getAttribute('Optional')
	if(at_Optional is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = at_Optional.boolean
	
	at_2D = xobj.getAttribute('2D')
	if(at_2D is None):
		raise Exception('Error: cannot find "2D" attribute')
	b2D = at_2D.boolean
	
	at_3D = xobj.getAttribute('3D')
	if(at_3D is None):
		raise Exception('Error: cannot find "3D" attribute')
	b3D = at_3D.boolean
	
	at_Section = xobj.getAttribute('Section')
	if(at_Section is None):
		raise Exception('Error: cannot find "Section" attribute')
	Section = at_Section.customObject
	if Section is None:
		raise Exception('Error: Section is None')
	
	at_Izz_modifier = xobj.getAttribute('Izz_modifier')
	if(at_Izz_modifier is None):
		raise Exception('Error: cannot find "Izz_modifier" attribute')
	Izz_modifier = at_Izz_modifier.real
	
	at_Iyy_modifier = xobj.getAttribute('Iyy_modifier')
	if(at_Iyy_modifier is None):
		raise Exception('Error: cannot find "Iyy_modifier" attribute')
	Iyy_modifier = at_Iyy_modifier.real
	
	# getSpatialDim
	if b2D:
		ndm = 2
		ndf = 3
		
	else:
		ndm = 3
		ndf = 6
	
	pinfo.updateModelBuilder(ndm, ndf)
	
	
	A = Section.properties.area
	Iz = Section.properties.Izz * Izz_modifier
	
	if b2D:
		
		# Analysis 2D
		# optional paramters
		sopt = ''
		
		if Optional:
			G_at_2D = xobj.getAttribute('G/2D')
			if(G_at_2D is None):
				raise Exception('Error: cannot find "G" attribute')
			G_2D = G_at_2D.quantityScalar
			
			alphaY = Section.properties.alphaY
			
			sopt += ' {} {}'.format(G_2D.value, alphaY)
		
		str_tcl = '\n{}section Elastic {} {} {} {}{}\n'.format(pinfo.indent, tag, E.value, A, Iz, sopt)
	
	elif b3D:
		# Analysis 3D
		
		Iy = Section.properties.Iyy * Iyy_modifier
		
		G_3D_at = xobj.getAttribute('G/3D')
		if(G_3D_at is None):
			raise Exception('Error: cannot find "G" attribute')
		G_3D = G_3D_at.quantityScalar
		
		J = Section.properties.J
		
		# optional paramters
		sopt = ''
		
		if Optional:
			alphaY = Section.properties.alphaY
			alphaZ = Section.properties.alphaZ
			sopt += ' {} {}'.format(alphaY, alphaZ)
	
		str_tcl = '\n{}section Elastic {} {} {} {} {} {} {}{}\n'.format(pinfo.indent, tag, E.value, A, Iz, Iy, G_3D.value, J, sopt)
	
	else:
		raise Exception('both 2D and 3D options are set to false')
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)