import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.element_properties.utils.geomTransf as gtran

class my_data:
	def __init__(self):
		# attributes will be set in the __control method
		pass

def makeXObjectMetaData():
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Group'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') +
		html_par('choose between 2D and 3D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('3D')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Group'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	at_2D.editable = False
	
	# 3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Group'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# transType
	at_transfType = gtran.makeAttribute('Group', name = 'transfType')
	
	# -alpha
	at_use_alpha = MpcAttributeMetaData()
	at_use_alpha.type = MpcAttributeType.Boolean
	at_use_alpha.name = '-alpha'
	at_use_alpha.group = 'Group'
	at_use_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-alpha')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = '-alpha'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-alpha')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	
	# -depth
	at_use_depth = MpcAttributeMetaData()
	at_use_depth.type = MpcAttributeType.Boolean
	at_use_depth.name = '-depth'
	at_use_depth.group = 'Group'
	at_use_depth.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-depth')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	
	# depth
	at_depth = MpcAttributeMetaData()
	at_depth.type = MpcAttributeType.Real
	at_depth.name = 'depth'
	at_depth.group = '-depth'
	at_depth.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-depth')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	
	# -mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.Boolean
	at_mass.name = '-mass'
	at_mass.group = 'Group'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mass')+'<br/>') +
		html_par('element mass per unit length (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	
	# massDens
	at_massDens = MpcAttributeMetaData()
	at_massDens.type = MpcAttributeType.QuantityScalar
	at_massDens.name = 'massDens'
	at_massDens.group = '-mass'
	at_massDens.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('massDens')+'<br/>') +
		html_par('element mass per unit length (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	at_massDens.setDefault(0.0)
	#at_massDens.dimension = u.M/u.L**3
	
	# -cMass
	at_cMass = MpcAttributeMetaData()
	at_cMass.type = MpcAttributeType.Boolean
	at_cMass.name = '-cMass'
	at_cMass.group = 'Group'
	at_cMass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-cMass')+'<br/>') +
		html_par('to form consistent mass matrix (optional, default = lumped mass matrix)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Beam_Column_Element','Elastic Beam Column Element')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'elasticBeamColumn'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_transfType)
	xom.addAttribute(at_use_alpha)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_use_depth)
	xom.addAttribute(at_depth)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_massDens)
	xom.addAttribute(at_cMass)
	
	
	# visibility dependencies
	
	# alpha-dep
	xom.setVisibilityDependency(at_use_alpha, at_alpha)
	
	# depth-dep
	xom.setVisibilityDependency(at_use_depth, at_depth)
	
	# massDens-dep
	xom.setVisibilityDependency(at_mass, at_massDens)
	
	# 2D-dep
	xom.setVisibilityDependency(at_2D, at_use_alpha)
	xom.setVisibilityDependency(at_2D, at_alpha)
	xom.setVisibilityDependency(at_2D, at_use_depth)
	xom.setVisibilityDependency(at_2D, at_depth)
	
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	d = __control(xobj)
	
	if d.Dimension2:
		ndm = 2
		ndf = 3
	
	else:
		ndm = 3
		ndf = 6
	return [(ndm,ndf),(ndm,ndf)]

def __control(xobj):
	
	d = my_data()
	
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	d.Dimension2 = Dimension2_at.boolean
	
	Dimension3_at = xobj.getAttribute('3D')
	if(Dimension3_at is None):
		raise Exception('Error: cannot find "3D" attribute')
	d.Dimension3 = Dimension3_at.boolean
	
	return d

def writeTcl(pinfo):
	
	#2D
	#element elasticBeamColumn $eleTag $iNode $jNode $A $E $Iz $transfTag <-alpha alpha> <-depth depth> <-mass $massDens> <-cMass>
	
	#3D
	#element elasticBeamColumn $eleTag $iNode $jNode $A $E $G $J $Iy $Iz $transfTag <-mass $massDens> <-cMass>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh = phys_prop.XObject.Xnamespace
	if (namePh != 'sections'):
		raise Exception('Error: physical property must be "sections" and not: "{}"'.format(namePh))
	
	nameSection = phys_prop.XObject.name
	if(nameSection != 'Elastic'):
		raise Exception('Error: section must be "Elastic" and not "{}"'.format(nameSection))
	
	d = __control(xobj)
	
	at_Dimension = xobj.getAttribute('Dimension')
	if(at_Dimension is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	Dimension = at_Dimension.string
	
	at_Dimension_Section = phys_prop.XObject.getAttribute('Dimension')
	if(at_Dimension_Section is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	Dimension_Section = at_Dimension_Section.string
	
	if(Dimension != Dimension_Section):
		raise Exception('Error: different dimension between physical property and "Element Property"')
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line or len(node_vect)!=2):
		raise Exception('Error: invalid type of element or number of nodes')
	
	
	# mandatory parameters
	at_Section = phys_prop.XObject.getAttribute('Section')
	if(at_Section is None):
		raise Exception('Error: cannot find "Section" attribute')
	Section = at_Section.customObject
	if Section is None:
		raise Exception('Error: Section is None')
	
	at_Izz_modifier = phys_prop.XObject.getAttribute('Izz_modifier')
	if(at_Izz_modifier is None):
		raise Exception('Error: cannot find "Izz_modifier" attribute')
	Izz_modifier = at_Izz_modifier.real
	
	at_Iyy_modifier = phys_prop.XObject.getAttribute('Iyy_modifier')
	if(at_Iyy_modifier is None):
		raise Exception('Error: cannot find "Iyy_modifier" attribute')
	Iyy_modifier = at_Iyy_modifier.real
	
	param = ''
	
	A = Section.properties.area
	
	at_E = phys_prop.XObject.getAttribute('E')
	if(at_E is None):
		raise Exception('Error: cannot find "E" attribute')
	E = at_E.quantityScalar
	
	param += '{} {}'.format(A, E.value)
	
	if d.Dimension3:
		
		at_G = phys_prop.XObject.getAttribute('G/3D')
		if(at_G is None):
			raise Exception('Error: cannot find "G" attribute')
		G = at_G.quantityScalar.value
		
		J = Section.properties.J
		Iy = Section.properties.Iyy * Iyy_modifier
		
		param += ' {} {} {}'.format(G, J, Iy)
	
	Iz = Section.properties.Izz * Izz_modifier
	param += ' {}'.format(Iz)
	
	# optional paramters
	sopt = ''
	
	if d.Dimension2:
		use_alpha_at = xobj.getAttribute('-alpha')
		if(use_alpha_at is None):
			raise Exception('Error: cannot find "-alpha" attribute')
		use_alpha = use_alpha_at.boolean
		if use_alpha:
			alpha_at = xobj.getAttribute('alpha')
			if(alpha_at is None):
				raise Exception('Error: cannot find "alpha" attribute')
			alpha = alpha_at.real
			
			sopt += ' -alpha {}'.format(alpha)
		
		use_depth_at = xobj.getAttribute('-depth')
		if(use_depth_at is None):
			raise Exception('Error: cannot find "-depth" attribute')
		use_depth = use_depth_at.boolean
		if use_depth:
			depth_at = xobj.getAttribute('depth')
			if(depth_at is None):
				raise Exception('Error: cannot find "depth" attribute')
			depth = depth_at.real
			
			sopt += ' -depth {}'.format(depth)
	
	mass_at = xobj.getAttribute('-mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "-mass" attribute')
	mass = mass_at.boolean
	if mass:
		massDens_at = xobj.getAttribute('massDens')
		if(massDens_at is None):
			raise Exception('Error: cannot find "massDens" attribute')
		massDens = massDens_at.quantityScalar.value
		
		sopt += ' -mass {}'.format(massDens)
	
	cMass_at = xobj.getAttribute('-cMass')
	if(cMass_at is None):
		raise Exception('Error: cannot find "-cMass" attribute')
	cMass = cMass_at.boolean
	if cMass:
		sopt += ' -cMass'
	
	if d.Dimension2:
		ndm = 2
		ndf = 3
	else:
		ndm = 3
		ndf = 6
	
	pinfo.updateModelBuilder(ndm, ndf)
	
	# geometric transformation command
	pinfo.out_file.write(gtran.writeGeomTransf(pinfo, (not d.Dimension2), name = 'transfType'))
	
	# now write the string into the file
	str_tcl = '{}element elasticBeamColumn {}{} {} {}{}\n'.format(pinfo.indent, tag, nstr, param, tag, sopt)
	pinfo.out_file.write(str_tcl)