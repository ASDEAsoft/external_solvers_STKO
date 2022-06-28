import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Constraint'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	# ModelType
	at_ModelType = MpcAttributeMetaData()
	at_ModelType.type = MpcAttributeType.String
	at_ModelType.name = 'ModelType'
	at_ModelType.group = 'Constraint'
	at_ModelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ModelType')+'<br/>') + 
		html_par('choose between "U (Displacement)" and "U-R (Displacement+Rotation)"') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_ModelType.sourceType = MpcAttributeSourceType.List
	at_ModelType.setSourceList(['U (Displacement)', 'U-R (Displacement+Rotation)'])
	at_ModelType.setDefault('U (Displacement)')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Constraint'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') + 
		html_par('Dx Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_2D.editable = False
	
	# 3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Constraint'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') + 
		html_par('Dx Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# -rho
	at_use_rho = MpcAttributeMetaData()
	at_use_rho.type = MpcAttributeType.Boolean
	at_use_rho.name = '-rho'
	at_use_rho.group = 'Group'
	at_use_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-rho')+'<br/>') +
		html_par('mass per unit length, optional, default = 0.0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = '-rho'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') +
		html_par('mass per unit length, optional, default = 0.0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_rho.setDefault(0.0)
	# at_rho.dimension = u.M/u.l
	
	# -cMass
	at_cMass = MpcAttributeMetaData()
	at_cMass.type = MpcAttributeType.Boolean
	at_cMass.name = '-cMass'
	at_cMass.group = 'Group'
	at_cMass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-cMass')+'<br/>') +
		html_par('consistent mass flag, optional, default = 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	
	# cFlag
	at_cFlag = MpcAttributeMetaData()
	at_cFlag.type = MpcAttributeType.Integer
	at_cFlag.name = 'cFlag'
	at_cFlag.group = '-cMass'
	at_cFlag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cFlag')+'<br/>') +
		html_par('consistent mass flag, optional, default = 0') +
		html_par('cFlag = 0 lumped mass matrix (default)') +
		html_par('cFlag = 1 consistent mass matrix') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_cFlag.sourceType = MpcAttributeSourceType.List
	at_cFlag.setSourceList([0, 1])
	at_cFlag.setDefault(0)
	
	#-doRayleigh
	at_doRayleigh = MpcAttributeMetaData()
	at_doRayleigh.type = MpcAttributeType.Boolean
	at_doRayleigh.name = '-doRayleigh'
	at_doRayleigh.group = 'Group'
	at_doRayleigh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-doRayleigh')+'<br/>') +
		html_par('Rayleigh damping flag, optional, default = 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	
	# rFlag
	at_rFlag = MpcAttributeMetaData()
	at_rFlag.type = MpcAttributeType.Integer
	at_rFlag.name = 'rFlag'
	at_rFlag.group = '-doRayleigh'
	at_rFlag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rFlag')+'<br/>') +
		html_par('Rayleigh damping flag, optional, default = 0') +
		html_par('rFlag = 0 NO RAYLEIGH DAMPING (default)') +
		html_par('rFlag = 1 include Rayleigh damping') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_rFlag.sourceType = MpcAttributeSourceType.List
	at_rFlag.setSourceList([0, 1])
	at_rFlag.setDefault(0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'corotTrussSection'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_ModelType)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_use_rho)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_cMass)
	xom.addAttribute(at_cFlag)
	xom.addAttribute(at_doRayleigh)
	xom.addAttribute(at_rFlag)
	
	# visibility dependencies
	
	# rho-dep
	xom.setVisibilityDependency(at_use_rho, at_rho)
	
	# cFlag-dep
	xom.setVisibilityDependency(at_cMass, at_cFlag)
	
	# rFlag-dep
	xom.setVisibilityDependency(at_doRayleigh, at_rFlag)
	
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	Dimension2 = Dimension2_at.boolean
	
	if Dimension2:
		ndm = 2
		ndf = [2, 3]
	else:
		ndm = 3
		ndf = [3, 6]
	return [(ndm,ndf),(ndm,ndf)]

def writeTcl(pinfo):
	
	#element corotTrussSection $eleTag $iNode $jNode $secTag <-rho $rho> <-cMass $cFlag> <-doRayleigh $rFlag>
	
	elem = pinfo.elem
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line or len(elem.nodes)!=2):
		raise Exception('Error: invalid type of element or number of nodes')
		
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	secTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	if Dimension2_at.boolean:
		ndm = 2
		node_1_id = elem.nodes[0].id
		if not node_1_id in pinfo.node_to_model_map:
			raise Exception('first node of truss is not in the model map')
		value = pinfo.node_to_model_map[node_1_id]
		ndf = value[1]
		if ndm != value[0]:
			raise Exception('inconsistency in the model map. 2D truss with 3D model')
	else:
		ndm = 3
		node_1_id = elem.nodes[0].id
		if not node_1_id in pinfo.node_to_model_map:
			raise Exception('first node of truss is not in the model map')
		value = pinfo.node_to_model_map[node_1_id]
		ndf = value[1]
		if ndm != value[0]:
			raise Exception('inconsistency in the model map. 3D truss with 2D model')
	
	# set node ids
	n1 = elem.nodes[0].id
	n2 = elem.nodes[1].id
	
	# if dofs are different at the 2 end nodes
	# take the smaller one and make edof
	ndf1 = pinfo.node_to_model_map[n1][1]
	ndf2 = pinfo.node_to_model_map[n2][1]
	if ndf1 != ndf2:
		# get the next node id
		extra_node_id = pinfo.next_node_id
		# update model builder for extra node
		pinfo.next_node_id += 1
		if ndm == 2:
			pinfo.updateModelBuilder(2, 2)
			edof_args = '1 2'
		elif ndm == 3:
			pinfo.updateModelBuilder(3, 3)
			edof_args = '1 2 3'
		else:
			raise Exception('Error: Unexpected NDM {}'.format(ndm))
		# ...
		if ndf1 < ndf2:
			edof_n1 = n2
			edof_n2 = extra_node_id
			n2 = extra_node_id
			inode = elem.nodes[1]
		else:
			edof_n1 = n1
			edof_n2 = extra_node_id
			n1 = extra_node_id
			inode = elem.nodes[0]
		# write extra node
		FMT = pinfo.get_double_formatter()
		pinfo.out_file.write('{}node {} {} {} {}\n'.format(pinfo.indent, extra_node_id, FMT(inode.x), FMT(inode.y), FMT(inode.z)))
		# write edof
		pinfo.out_file.write('{}equalDOF {} {} {}\n'.format(pinfo.indent, edof_n1, edof_n2, edof_args))
	# nodes
	nstr = ' {} {}'.format(n1, n2)
	
	# update
	pinfo.updateModelBuilder(ndm, ndf)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh = phys_prop.XObject.Xnamespace
	if (namePh!='sections'):
		raise Exception('Error: physical property must be "sections" and not: "{}"'.format(namePh))
	
	# optional paramters
	sopt = ''
	
	use_rho_at = xobj.getAttribute('-rho')
	if(use_rho_at is None):
		raise Exception('Error: cannot find "-rho" attribute')
	use_rho = use_rho_at.boolean
	if use_rho:
		rho_at = xobj.getAttribute('rho')
		if(rho_at is None):
			raise Exception('Error: cannot find "rho" attribute')
		rho = rho_at.quantityScalar
		
		sopt += ' -rho {}'.format(rho.value)
	
	cMass_at = xobj.getAttribute('-cMass')
	if(cMass_at is None):
		raise Exception('Error: cannot find "-cMass" attribute')
	cMass = cMass_at.boolean
	if cMass:
		
		sopt += ' -cMass 1'
	
	doRayleigh_at = xobj.getAttribute('-doRayleigh')
	if(doRayleigh_at is None):
		raise Exception('Error: cannot find "-doRayleigh" attribute')
	doRayleigh = doRayleigh_at.boolean
	if doRayleigh:
		
		sopt += ' -doRayleigh 1'
	
	str_tcl = '{}element corotTrussSection {}{} {}{}\n'.format(pinfo.indent, tag, nstr, secTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
