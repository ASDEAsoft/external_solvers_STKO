import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	# ModelType
	at_ModelType = MpcAttributeMetaData()
	at_ModelType.type = MpcAttributeType.String
	at_ModelType.name = 'ModelType'
	at_ModelType.group = 'Group'
	at_ModelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ModelType')+'<br/>') + 
		html_par('choose between "U (Displacement)" and "U-R (Displacement+Rotation)"') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_ModelType.sourceType = MpcAttributeSourceType.List
	at_ModelType.setSourceList(['U (Displacement)', 'U-R (Displacement+Rotation)'])
	at_ModelType.setDefault('U (Displacement)')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Group'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# D
	at_D = MpcAttributeMetaData()
	at_D.type = MpcAttributeType.Boolean
	at_D.name = 'U (Displacement)'
	at_D.groD = 'Constraint'
	at_D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U (Displacement)')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_D.editable = False
	
	# UR
	at_UR = MpcAttributeMetaData()
	at_UR.type = MpcAttributeType.Boolean
	at_UR.name = 'U-R (Displacement+Rotation)'
	at_UR.group = 'Constraint'
	at_UR.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U-R (Displacement+Rotation)')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_UR.editable = False
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Group'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# -pDelta
	at_pDelta = MpcAttributeMetaData()
	at_pDelta.type = MpcAttributeType.Boolean
	at_pDelta.name = '-pDelta'
	at_pDelta.group = 'Group'
	at_pDelta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-pDelta')+'<br/>') +
		html_par('P-Delta moment contribution ratios') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# Mratios
	at_Mratios = MpcAttributeMetaData()
	at_Mratios.type = MpcAttributeType.QuantityVector
	at_Mratios.name = 'Mratios'
	at_Mratios.group = '-pDelta'
	at_Mratios.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mratios')+'<br/>') +
		html_par('P-Delta moment contribution ratios, size of ratio vector is 2 for 2D-case and 4 for 3D-case') +
		html_par('(entries: [My_iNode, My_jNode, Mz_iNode, Mz_jNode]) My_iNode + My_jNode <= 1.0, Mz_iNode + Mz_jNode <= 1.0.') +
		html_par('Remaining P-Delta moments are resisted by shear couples. (optional)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# -shearDist
	at_shearDist = MpcAttributeMetaData()
	at_shearDist.type = MpcAttributeType.Boolean
	at_shearDist.name = '-shearDist'
	at_shearDist.group = 'Group'
	at_shearDist.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-shearDist')+'<br/>') +
		html_par('shear distances from iNode as a fraction of the element length') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# sDratios
	at_sDratios = MpcAttributeMetaData()
	at_sDratios.type = MpcAttributeType.QuantityVector
	at_sDratios.name = 'sDratios'
	at_sDratios.group = '-shearDist'
	at_sDratios.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sDratios')+'<br/>') +
		html_par('shear distances from iNode as a fraction of the element length, size of ratio vector is 1 for 2D-case and 2 for 3D-case') +
		html_par('(entries: [dy_iNode, dz_iNode] (optional, default = [0.5 0.5])') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# -doRayleigh
	at_doRayleigh = MpcAttributeMetaData()
	at_doRayleigh.type = MpcAttributeType.Boolean
	at_doRayleigh.name = '-doRayleigh'
	at_doRayleigh.group = 'Group'
	at_doRayleigh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-doRayleigh')+'<br/>') +
		html_par('to include Rayleigh damping from the element (optional, default = no Rayleigh damping contribution)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
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
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.QuantityScalar
	at_m.name = 'm'
	at_m.group = '-mass'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') +
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_m.setDefault(0.0)
	# at_m.dimension = u.M
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'twoNodeLink'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_ModelType)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_D)
	xom.addAttribute(at_UR)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_pDelta)
	xom.addAttribute(at_Mratios)
	xom.addAttribute(at_shearDist)
	xom.addAttribute(at_sDratios)
	xom.addAttribute(at_doRayleigh)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	
	
	# Mratios-dep
	xom.setVisibilityDependency(at_pDelta, at_Mratios)
	
	# sDratios-dep
	xom.setVisibilityDependency(at_shearDist, at_sDratios)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	# 2D or 2D Beam or 3D or 3D Beam
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_D)
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_UR)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	
	d = __control(xobj)
	
	if d.Dimension2:
		ndm = 2
		if d.D:
			ndf = 2
		else:
			ndf = 3
	else:
		ndm = 3
		if d.D:
			ndf = 3
		else:
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
	
	D_at = xobj.getAttribute('U (Displacement)')
	if(D_at is None):
		raise Exception('Error: cannot find "U (Displacement)" attribute')
	d.D = D_at.boolean
	
	
	UR_at = xobj.getAttribute('U-R (Displacement+Rotation)')
	if(UR_at is None):
		raise Exception('Error: cannot find "U-R (Displacement+Rotation)" attribute')
	d.UR = UR_at.boolean
	
	return d

def writeTcl(pinfo):
	
	# element twoNodeLink $eleTag $iNode $jNode -mat $matTags -dir $dirs <-orient <$x1 $x2 $x3> $y1 $y2 $y3>
	# <-pDelta (4 $Mratio)> <-shearDist (2 $sDratios)> <-doRayleigh> <-mass $m>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	d = __control(xobj)
	
	if d.Dimension2:
		ndm = 2
		if d.D:
			ndf = 2
		else:
			ndf = 3
	else:
		ndm = 3
		if d.D:
			ndf = 3
		else:
			ndf = 6
	
	# getSpatialDim
	pinfo.updateModelBuilder(ndm, ndf)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	if (elem.topologyType().name) != MpcElementTopologyType.Interaction.name:
		raise Exception('Error: element must be "Interaction" and not "{}"'.format(elem.topologyType().name))
	
	Dimension_at = xobj.getAttribute('Dimension')
	if(Dimension_at is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	Dimension = Dimension_at.string
	
	# ***special_purpose***
	if phys_prop.XObject.name != 'twoNodeLinkMaterial':
		raise Exception('Wrong material type for twoNodeLink element. Expected: "twoNodeLinkMaterial", given: "{}"'.format(phys_prop.XObject.name))
	
	DimensionMat_at = phys_prop.XObject.getAttribute('Dimension')
	if(DimensionMat_at is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	DimensionMat = DimensionMat_at.string
	
	DMat_at = phys_prop.XObject.getAttribute('U (Displacement)')
	if(DMat_at is None):
		raise Exception('Error: cannot find "U (Displacement)" attribute')
	DMat = DMat_at.boolean
	
	if(Dimension != DimensionMat or d.D != DMat):
		raise Exception('Error: different dimension between "twoNodeLink" element and "twoNodeLinkMaterial"')
	
	mat_string = '-mat'
	dir_string = '-dir'
	mat_counter = 0
	
	
	if d.Dimension2:
		if d.D:
			nMat = 2
		else:
			nMat = 3
	else:
		if d.D:
			nMat = 3
		else:
			nMat = 6
	
	for i in range(1, nMat+1):
		dir_att_name = 'dir{}'.format(i)
		mat_tag_att_name = 'matTag{}'.format(i)
		dir_at = phys_prop.XObject.getAttribute(dir_att_name)
		if(dir_at is None):
			dir_att_name += '/{}'.format(Dimension)
			dir_at = phys_prop.XObject.getAttribute(dir_att_name)
			if(dir_at is None):
				raise Exception('Error: cannot find "{}" attribute'.format(dir_att_name))
		
		if dir_at.boolean:
			matTag_at = phys_prop.XObject.getAttribute(mat_tag_att_name)
			if(matTag_at is None):
				mat_tag_att_name += '/{}'.format(Dimension)
				matTag_at = phys_prop.XObject.getAttribute(mat_tag_att_name)
				if(matTag_at is None):
					raise Exception('Error: cannot find "{}" attribute'.format(mat_tag_att_name))
			mat_tag = matTag_at.index
			if mat_tag > 0:
				mat_counter += 1
				mat_string += ' {}'.format(mat_tag)
				dir_string += ' {}'.format(i)
	if mat_counter == 0:
		raise Exception ('Error: invalid number of materials')	#******
	# ***end special_purpose***
	
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=2):
		raise Exception('Error: invalid number of nodes')
	
	
	# optional paramters
	sopt = ''
	
	orient_at = xobj.getAttribute('-orient')
	if(orient_at is None):
		raise Exception('Error: cannot find "-orient" attribute')
	if orient_at.boolean:
		vect_x=elem.orientation.computeOrientation().col(0)
		vect_y=elem.orientation.computeOrientation().col(1)
		
		sopt += ' -orient {} {} {} {} {} {}'.format (vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	
	pDelta_at = xobj.getAttribute('-pDelta')
	if(pDelta_at is None):
		raise Exception('Error: cannot find "-pDelta" attribute')
	if pDelta_at.boolean:
		Mratios_at = xobj.getAttribute('Mratios')
		if(Mratios_at is None):
			raise Exception('Error: cannot find "Mratios" attribute')
		Mratios = Mratios_at.quantityVector
		
		if (d.Dimension2 and len(Mratios)!=2):
			raise Exception ('Error: size of "Mratios" vector is 2 for 2D-case')
		
		elif (d.Dimension3 and len(Mratios)!=4):
			raise Exception ('Error: size of "Mratios" vector is 4 for 3D-case')
		
		vect_Mratios = ''
		for i in range(len(Mratios)):
			vect_Mratios += ' {}'.format(Mratios.valueAt(i))
		
		sopt += ' -pDelta{}'.format(vect_Mratios)
	
	shearDist_at = xobj.getAttribute('-shearDist')
	if(shearDist_at is None):
		raise Exception('Error: cannot find "-shearDist" attribute')
	if shearDist_at.boolean:
		sDratios_at = xobj.getAttribute('sDratios')
		if(sDratios_at is None):
			raise Exception('Error: cannot find "sDratios" attribute')
		sDratios = sDratios_at.quantityVector
		
		if (d.Dimension2 and len(sDratios)!=1):
			raise Exception ('size of "sDratios" vector is 1 for 2D-case')
		
		elif (d.Dimension3 and len(sDratios)!=2):
			raise Exception ('Error: size of "sDratios" vector is 2 for 3D-case')
		
		vect_sDratios = ''
		for i in range(len(sDratios)):
			vect_sDratios += ' {}'.format(sDratios.valueAt(i))
		
		sopt += ' -shearDist{}'.format(vect_sDratios)
	
	doRayleigh_at = xobj.getAttribute('-doRayleigh')
	if(doRayleigh_at is None):
		raise Exception('Error: cannot find "-doRayleigh" attribute')
	if doRayleigh_at.boolean:
		
		sopt += ' -doRayleigh'
	
	
	mass_at = xobj.getAttribute('-mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "-mass" attribute')
	if mass_at.boolean:
		
		m_at = xobj.getAttribute('m')
		if(m_at is None):
			raise Exception('Error: cannot find "m" attribute')
		m = m_at.quantityScalar.value
		
		sopt += ' -mass {}'.format(m)
	
	
	str_tcl = '{}element twoNodeLink {}{} {} {}{}\n'.format(pinfo.indent, tag, nstr, mat_string, dir_string, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)