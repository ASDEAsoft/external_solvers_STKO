import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Model'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par('choose between 2D and 3D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Model'
	at_2D.editable = False
	
	# 3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Model'
	at_3D.editable = False
	
	# kinematics
	at_kin = MpcAttributeMetaData()
	at_kin.type = MpcAttributeType.String
	at_kin.name = 'Kinematics'
	at_kin.group = 'Formulation'
	at_kin.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kinematics')+'<br/>') + 
		html_par(
			'choose between Linear (geometrically linear, a truss or truss section will be created) '
			'and Corotational (geometrically non-linear, a corotTruss or corotTruss section will be created)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_kin.sourceType = MpcAttributeSourceType.List
	at_kin.setSourceList(['Linear', 'Corotational'])
	at_kin.setDefault('Linear')
	
	# -rho
	at_use_rho = MpcAttributeMetaData()
	at_use_rho.type = MpcAttributeType.Boolean
	at_use_rho.name = '-rho'
	at_use_rho.group = 'Optional'
	at_use_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-rho')+'<br/>') +
		html_par('check it to use rho') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Optional'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') +
		html_par('mass per unit length, optional, default = 0.0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	at_rho.setDefault(0.0)
	# at_rho.dimension = u.M/u.l
	
	# -cMass
	at_cMass = MpcAttributeMetaData()
	at_cMass.type = MpcAttributeType.Boolean
	at_cMass.name = '-cMass'
	at_cMass.group = 'Optional'
	at_cMass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-cMass')+'<br/>') +
		html_par('check it to activate consistent mass, default = lumped') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	
	#-doRayleigh
	at_doRayleigh = MpcAttributeMetaData()
	at_doRayleigh.type = MpcAttributeType.Boolean
	at_doRayleigh.name = '-doRayleigh'
	at_doRayleigh.group = 'Optional'
	at_doRayleigh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-doRayleigh')+'<br/>') +
		html_par('check it to activate rayleigh damping, default = no rayleigh damping') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Truss_Element','Truss Element')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Corotational_Truss_Element','Corotational Truss Element')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'truss'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_kin)
	xom.addAttribute(at_use_rho)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_cMass)
	xom.addAttribute(at_doRayleigh)
	
	
	# visibility dependencies
	
	# rho-dep
	xom.setVisibilityDependency(at_use_rho, at_rho)
	
	
	# auto-exclusive dependencies
	
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
	
	# element truss $eleTag $iNode $jNode $A $matTag <-rho $rho> <-cMass $cFlag> <-doRayleigh $rFlag>
	
	elem = pinfo.elem
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line or len(elem.nodes)!=2):
		raise Exception('Error: invalid type of element or number of nodes')
		
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	# secTag = phys_prop.id
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
	
	namePh=phys_prop.XObject.Xnamespace
	if (namePh!='special_purpose'):
		raise Exception('Error: physical property must be "special_purpose" and not: "{}"'.format(namePh))
	
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
	
	kin_at = xobj.getAttribute('Kinematics')
	if kin_at is None:
		raise Exception('Error: cannot find "Kinematics" attribute')
	if kin_at.string == 'Linear':
		prefix = 'truss'
	else:
		prefix = 'corotTruss'
	
	type_at = phys_prop.XObject.getAttribute('truss')
	type = type_at.boolean
	
	if type:
		uniTag_at = phys_prop.XObject.getAttribute('uniTag/truss')
		uniTag = uniTag_at.index
	
		at_Section = phys_prop.XObject.getAttribute('elastic_Section')
		if(at_Section is None):
			raise Exception('Error: cannot find "elastic_Section" attribute')
		Section = at_Section.customObject
		A = Section.properties.area
		
		str_tcl = '{}element {} {}{} {} {}{}\n'.format(pinfo.indent, prefix, tag, nstr, A, uniTag, sopt)
		
	else :
		secTag_at = phys_prop.XObject.getAttribute('secTag/truss')
		secTag = secTag_at.index
		str_tcl = '{}element {}Section {}{} {}{}\n'.format(pinfo.indent, prefix, tag, nstr, secTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
