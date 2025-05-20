import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.physical_properties.sections.offset_utils as ofu

'''
Version 1:
'''
class _internals:
	version = 1 # the current version

def _geta(xobj, name):
	x = xobj.getAttribute(name)
	if x is None:
		raise Exception('Cannot find "{}" attribute'.format(name))
	return x

def makeXObjectMetaData():
	
	def mka(type:MpcAttributeType, name:str, group:str, desc:str):
		at = MpcAttributeMetaData()
		at.type = type
		at.name = name
		at.group = group
		at.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(desc) +
			html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Section','Elastic Section')+'<br/>') +
			html_end()
			)
		return at
	
	at_Dimension = mka(MpcAttributeType.String, 'Dimension', 'Section', 'Choose between 2D and 3D')
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('3D')
	
	at_Section = mka(MpcAttributeType.CustomAttributeObject, 'Section', 'Section', 'Press the edit button to edit the cross section')
	at_Section.customObjectPrototype = MpcBeamSection()
	

	at_shear_def = mka(MpcAttributeType.Boolean, 'Shear Deformable', 'Options', 
				   'Tick this value to use make the section shear-deformable (uses <alphaY> for 2D or <alphaY, alphaZ> for 3D, from the section object)')


	at_E = mka(MpcAttributeType.QuantityScalar, 'E', 'Material properties', 'Young\'s Modulus')
	at_E.dimension = u.F/u.L**2
	
	at_G = mka(MpcAttributeType.QuantityScalar, 'G', 'Material properties', 'Shear Modulus')
	at_G.dimension = u.F/u.L**2
	


	at_use_uniaxial = mka(MpcAttributeType.Boolean, 'Use Uniaxial Materials', 'Material properties', 
					   'Tick this value to use custom uniaxial materials instead of elastic constants. This will turn the Elastic Section into a section aggregator')
	at_use_uniaxial.setDefault(False)
	
	at_material_Em = mka(MpcAttributeType.Index, 'Em material', 'Material properties',
		'tag of previously-defined UniaxialMaterial objects (stress-strain for axial behavior)')
	at_material_Em.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_material_Em.indexSource.addAllowedNamespace('materials.uniaxial')

	at_material_Eb = mka(MpcAttributeType.Index, 'Eb material', 'Material properties',
		'tag of previously-defined UniaxialMaterial objects (stress-strain for bending behavior)')
	at_material_Eb.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_material_Eb.indexSource.addAllowedNamespace('materials.uniaxial')
	
	at_material_G = mka(MpcAttributeType.Index, 'G material', 'Material properties',
		'tag of previously-defined UniaxialMaterial objects (stress-strain for shear/torsion behavior)')
	at_material_G.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_material_G.indexSource.addAllowedNamespace('materials.uniaxial')
	
	
	at_A_modifier = mka(MpcAttributeType.Real, 'A_modifier', 'Stiffness modifiers',
		'Scale factor for axial stiffness')
	at_A_modifier.setDefault(1.0)

	at_Asy_modifier = mka(MpcAttributeType.Real, 'Asy_modifier', 'Stiffness modifiers',
		'Scale factor for shear stiffness along Y local axis')
	at_Asy_modifier.setDefault(1.0)

	at_Asz_modifier = mka(MpcAttributeType.Real, 'Asz_modifier', 'Stiffness modifiers',
		'Scale factor for shear stiffness along Z local axis')
	at_Asz_modifier.setDefault(1.0)
	
	at_Izz_modifier = mka(MpcAttributeType.Real, 'Izz_modifier', 'Stiffness modifiers',
		'Scale factor for bending stiffness about Z local axis')
	at_Izz_modifier.setDefault(1.0)
	
	at_Iyy_modifier = mka(MpcAttributeType.Real, 'Iyy_modifier', 'Stiffness modifiers',
		'Scale factor for bending stiffness about Y local axis')
	at_Iyy_modifier.setDefault(1.0)

	at_J_modifier = mka(MpcAttributeType.Real, 'J_modifier', 'Stiffness modifiers',
		'Scale factor for torsional stiffness')
	at_J_modifier.setDefault(1.0)
	

	xom = MpcXObjectMetaData()
	xom.name = 'Elastic'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_Section)
	# options
	xom.addAttribute(at_shear_def)
	#material params
	xom.addAttribute(at_use_uniaxial)
	xom.addAttribute(at_E)
	xom.addAttribute(at_G)
	xom.addAttribute(at_material_Em)
	xom.addAttribute(at_material_Eb)
	xom.addAttribute(at_material_G)
	# modifiers
	xom.addAttribute(at_A_modifier)
	xom.addAttribute(at_Asy_modifier)
	xom.addAttribute(at_Asz_modifier)
	xom.addAttribute(at_Izz_modifier)
	xom.addAttribute(at_Iyy_modifier)
	xom.addAttribute(at_J_modifier)
	
	# add a last attribute for versioning
	av = MpcAttributeMetaData()
	av.type = MpcAttributeType.Integer
	av.name = 'version'
	av.setDefault(_internals.version)
	av.editable = False
	xom.addAttribute(av)
	
	# add offset
	ofu.addOffsetMetaData(xom)
	
	return xom

def onEditBegin(editor, xobj):
	# just call one attribute... we update all visibility here...
	onAttributeChanged(editor, xobj, 'Use Uniaxial Materials')

def onAttributeChanged(editor, xobj, attribute_name):
	uni =_geta(xobj, 'Use Uniaxial Materials').boolean
	d2 = _geta(xobj, 'Dimension').string == '2D'
	shear_def = _geta(xobj, 'Shear Deformable').boolean
	_geta(xobj, 'E').visible = not uni
	_geta(xobj, 'G').visible = not uni and ((not d2) or (d2 and shear_def))
	_geta(xobj, 'Em material').visible = uni
	_geta(xobj, 'Eb material').visible = uni
	_geta(xobj, 'G material').visible = uni and ((not d2) or (d2 and shear_def))
	_geta(xobj, 'Iyy_modifier').visible = not d2
	_geta(xobj, 'Asz_modifier').visible = not d2 and shear_def
	_geta(xobj, 'Asy_modifier').visible = shear_def
	_geta(xobj, 'J_modifier').visible = not d2
	ofu.updateVisibility(not d2, xobj)

def onConvertOldVersion(xobj, old_xobj):
	'''
	try to convert objects from old versions to the current one.
	'''
	
	version = 0 # default one
	av = old_xobj.getAttribute('version')
	if av:
		version = av.integer
	
	# just a safety check
	cav = xobj.getAttribute('version')
	if cav is None:
		IO.write_cerr('Cannot find "version" attribute in AnalysesCommand\n')
		return
	cav.integer = _internals.version
	
	# check version
	if version == 0:
		# the old Optional attribute is now called Shear Deformable (from version 1 on)
		old_shear_def = old_xobj.getAttribute('Optional').boolean
		xobj.getAttribute('Shear Deformable').boolean = old_shear_def
		# G/2D and G/3D are now called G, get them based on the old dimension
		old_dim = old_xobj.getAttribute('Dimension').string
		if old_dim == '2D':
			old_G = old_xobj.getAttribute('G/2D').quantityScalar.value
			xobj.getAttribute('G').quantityScalar.value = old_G
		else:
			old_G = old_xobj.getAttribute('G/3D').quantityScalar.value
			xobj.getAttribute('G').quantityScalar.value = old_G

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
	b2D = _geta(xobj, 'Dimension').string == '2D'
	b3D = not b2D
	
	# get section
	Section = _geta(xobj, 'Section').customObject
	if Section is None:
		raise Exception('Error in Elastic section: Section is not defined')
	
	# get section modifiers
	def _get_mod(xobj, name):
		try:
			return _geta(xobj, name).real
		except:
			return 1.0
	A_modifier = _get_mod(xobj, 'A_modifier')
	Asy_modifier = _get_mod(xobj, 'Asy_modifier')
	Asz_modifier = _get_mod(xobj, 'Asz_modifier')
	Izz_modifier = _get_mod(xobj, 'Izz_modifier')
	Iyy_modifier = _get_mod(xobj, 'Iyy_modifier')
	J_modifier = _get_mod(xobj, 'J_modifier')

	# get section properties
	alphaZ = Section.properties.alphaZ
	alphaY = Section.properties.alphaY
	A = Section.properties.area * A_modifier
	Asy = Section.properties.area * alphaY * Asy_modifier
	Asz = Section.properties.area * alphaZ * Asz_modifier
	Iz = Section.properties.Izz * Izz_modifier
	Iy = Section.properties.Iyy * Iyy_modifier
	J = Section.properties.J * J_modifier
	
	# material properties
	E = _geta(xobj, 'E').quantityScalar.value
	if b2D:
		G = _geta(xobj, 'G/2D').quantityScalar.value
	else:
		G = _geta(xobj, 'G/3D').quantityScalar.value
		
	# shear deformability option
	shear_def = _geta(xobj, 'Shear Deformable').boolean
	
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
		if (b2D and shear_def) or b3D:
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
			if shear_def:
				Vy = next_id()
				pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, Vy, GG, Asy))
				data.append(Vy)
				data.append('Vy')
			str_tcl = '{}section Aggregator {} {}\n'.format(pinfo.indent, tag, ' '.join(str(i) for i in data))
			
		else:
			# elastic section 2D
			sopt = ''
			if shear_def:
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
			if shear_def:
				Vy = next_id()
				pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, Vy, GG, Asy))
				data.append(Vy)
				data.append('Vy')
				Vz = next_id()
				pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, Vz, GG, Asz))
				data.append(Vz)
				data.append('Vz')
			str_tcl = '{}section Aggregator {} {}\n'.format(pinfo.indent, tag, ' '.join(str(i) for i in data))
			
		else:
			# elastic section 3D
			sopt = ''
			if shear_def:
				sopt = ' {} {}'.format(alphaY, alphaZ)
			str_tcl = '\n{}section Elastic {} {} {} {} {} {} {}{}\n'.format(pinfo.indent, tag, E, A, Iz, Iy, G, J, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)