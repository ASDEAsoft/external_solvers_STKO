import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.physical_properties.sections.offset_utils as ofu

def _geta(xobj, name):
	x = xobj.getAttribute(name)
	if x is None:
		raise Exception('Cannot find "{}" attribute'.format(name))
	return x

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
	
	# use_uniaxial
	at_use_uniaxial = MpcAttributeMetaData()
	at_use_uniaxial.type = MpcAttributeType.Boolean
	at_use_uniaxial.name = 'Use Uniaxial Materials'
	at_use_uniaxial.group = 'Material properties'
	at_use_uniaxial.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Use Uniaxial Materials')+'<br/>') + 
		html_par('Tick this value to use custom uniaxial materials instead of elastic constants. This will turn the Elastic Section into a section aggregator') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_use_uniaxial.setDefault(False)
	# material_Em
	at_material_Em = MpcAttributeMetaData()
	at_material_Em.type = MpcAttributeType.Index
	at_material_Em.name = 'Em material'
	at_material_Em.group = 'Material properties'
	at_material_Em.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Em material')+'<br/>') + 
		html_par('tag of previously-defined UniaxialMaterial objects (stress-strain for axial behavior)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_material_Em.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_material_Em.indexSource.addAllowedNamespace('materials.uniaxial')
	# material_Eb
	at_material_Eb = MpcAttributeMetaData()
	at_material_Eb.type = MpcAttributeType.Index
	at_material_Eb.name = 'Eb material'
	at_material_Eb.group = 'Material properties'
	at_material_Eb.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Em material')+'<br/>') + 
		html_par('tag of previously-defined UniaxialMaterial objects (stress-strain for bending behavior)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_material_Eb.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_material_Eb.indexSource.addAllowedNamespace('materials.uniaxial')
	# material_G
	at_material_G = MpcAttributeMetaData()
	at_material_G.type = MpcAttributeType.Index
	at_material_G.name = 'G material'
	at_material_G.group = 'Material properties'
	at_material_G.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('G material')+'<br/>') + 
		html_par('tag of previously-defined UniaxialMaterial objects (stress-strain for shear/torsion behavior)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
		html_end()
		)
	at_material_G.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_material_G.indexSource.addAllowedNamespace('materials.uniaxial')
	
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
	xom.addAttribute(at_use_uniaxial)
	xom.addAttribute(at_E)
	xom.addAttribute(at_G_2D)
	xom.addAttribute(at_G_3D)
	xom.addAttribute(at_material_Em)
	xom.addAttribute(at_material_Eb)
	xom.addAttribute(at_material_G)
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

def onEditBegin(editor, xobj):
	onAttributeChanged(editor, xobj, 'Use Uniaxial Materials')

def onAttributeChanged(editor, xobj, attribute_name):
	uni =_geta(xobj, 'Use Uniaxial Materials').boolean
	d2 = _geta(xobj, '2D').boolean
	opt = _geta(xobj, 'Optional').boolean
	_geta(xobj, 'E').visible = not uni
	_geta(xobj, 'G/2D').visible = (not uni) and (d2 and opt)
	_geta(xobj, 'G/3D').visible = (not uni) and (not d2)
	_geta(xobj, 'Em material').visible = uni
	_geta(xobj, 'Eb material').visible = uni
	_geta(xobj, 'G material').visible = uni and ((not d2) or (d2 and opt))

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
	
	# utils
	def next_id():
		id = pinfo.next_physicalProperties_id
		pinfo.next_physicalProperties_id += 1
		return id
	
	# xobj and tag
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# dimension
	b2D = _geta(xobj, '2D').boolean
	b3D = _geta(xobj, '3D').boolean
	if b2D == b3D:
		raise Exception('Cannot set both 2D and 3D flags to the same value in Elastic section')
	
	# section properties
	Section = _geta(xobj, 'Section').customObject
	if Section is None:
		raise Exception('Error in Elastic section: Section is not defined')
	Izz_modifier = _geta(xobj, 'Izz_modifier').real
	Iyy_modifier = _geta(xobj, 'Iyy_modifier').real
	alphaZ = Section.properties.alphaZ
	alphaY = Section.properties.alphaY
	A = Section.properties.area
	Iz = Section.properties.Izz * Izz_modifier
	Iy = Section.properties.Iyy * Iyy_modifier
	J = Section.properties.J
	
	# material properties
	E = _geta(xobj, 'E').quantityScalar.value
	if b2D:
		G = _geta(xobj, 'G/2D').quantityScalar.value
	else:
		G = _geta(xobj, 'G/3D').quantityScalar.value
		
	# shear deformability option
	Optional = _geta(xobj, 'Optional').boolean
	
	# custom uniaxial for conversion to aggregator
	use_uniaxial = _geta(xobj, 'Use Uniaxial Materials').boolean
	if use_uniaxial:
		Em = _geta(xobj, 'Em material').index
		Eb = _geta(xobj, 'Eb material').index
		GG = _geta(xobj, 'G material').index
		if Em == 0:
			raise Exception('Error in Elastic section: Missing uniaxial material for axial response "Em"')
		if Eb == 0:
			raise Exception('Error in Elastic section: Missing uniaxial material for bending response "Eb"')
		if (b2D and Optional) or b3D:
			if GG == 0:
				raise Exception('Error in Elastic section: Missing uniaxial material for shear/torsion response "G"')
	
	# update model builder
	if not use_uniaxial:
		if b2D:
			ndm = 2
			ndf = 3
		else:
			ndm = 3
			ndf = 6
		pinfo.updateModelBuilder(ndm, ndf)
	
	# write section
	if b2D:
		if use_uniaxial:
			# aggregator 2D
			P = next_id()
			pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, P, Em, A))
			Mz = next_id()
			pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, Mz, Eb, Iz))
			data = [P, 'P', Mz, 'Mz']
			if Optional:
				Vy = next_id()
				pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, Vy, GG, A*alphaY))
				data.append(Vy)
				data.append('Vy')
			str_tcl = '{}section Aggregator {} {}\n'.format(pinfo.indent, tag, ' '.join(str(i) for i in data))
			
		else:
			# elastic section 2D
			sopt = ''
			if Optional:
				sopt = ' {} {}'.format(G, alphaY)
			str_tcl = '\n{}section Elastic {} {} {} {}{}\n'.format(pinfo.indent, tag, E, A, Iz, sopt)
	
	else:
		if use_uniaxial:
			# aggregator 3D
			P = next_id()
			pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, P, Em, A))
			Mz = next_id()
			pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, Mz, Eb, Iz))
			My = next_id()
			pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, My, Eb, Iy))
			T = next_id()
			pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, T, GG, J))
			data = [P, 'P', Mz, 'Mz', My, 'My', T, 'T']
			if Optional:
				Vy = next_id()
				pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, Vy, GG, A*alphaY))
				data.append(Vy)
				data.append('Vy')
				Vz = next_id()
				pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, Vz, GG, A*alphaZ))
				data.append(Vz)
				data.append('Vz')
			str_tcl = '{}section Aggregator {} {}\n'.format(pinfo.indent, tag, ' '.join(str(i) for i in data))
			
		else:
			# elastic section 3D
			sopt = ''
			if Optional:
				sopt = ' {} {}'.format(alphaY, alphaZ)
			str_tcl = '\n{}section Elastic {} {} {} {} {} {} {}{}\n'.format(pinfo.indent, tag, E, A, Iz, Iy, G, J, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)