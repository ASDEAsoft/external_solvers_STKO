import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *
from opensees.conditions.utils import SpatialFunctionEval

def makeXObjectMetaData():
	'''
	fill the 3d vector data. set the pressure value
	at the z component, since the orientation is set to local
	'''
	
	# Mode
	at_Mode = MpcAttributeMetaData()
	at_Mode.type = MpcAttributeType.String
	at_Mode.name = 'Mode'
	at_Mode.group = 'Group'
	at_Mode.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') +
		html_par('choose between "constant" and "function"') +
		html_end()
		)
	at_Mode.sourceType = MpcAttributeSourceType.List
	at_Mode.setSourceList(['constant', 'function'])
	at_Mode.setDefault('constant')
	
	# constant
	at_constant = MpcAttributeMetaData()
	at_constant.type = MpcAttributeType.Boolean
	at_constant.name = 'constant'
	at_constant.group = 'Data'
	at_constant.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('constant')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_constant.editable = False
	
	# function
	at_function = MpcAttributeMetaData()
	at_function.type = MpcAttributeType.Boolean
	at_function.name = 'function'
	at_function.group = 'Data'
	at_function.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('function')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_function.editable = False
	
	# M
	at_M = MpcAttributeMetaData()
	at_M.type = MpcAttributeType.QuantityVector3
	at_M.name = 'M'
	at_M.group = 'Data'
	at_M.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('M')+'<br/>') + 
		html_par('The 3d force vector') +
		html_end()
		)
	at_M.dimension = u.F/u.L**2
	
	# Mx
	at_Mx = MpcAttributeMetaData()
	at_Mx.type = MpcAttributeType.String
	at_Mx.name = 'Mx'
	at_Mx.group = 'Data'
	at_Mx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mx')+'<br/>') + 
		html_par('f(x) e.g.:') +
		html_par('(x**2+y**2)**0.5') +
		html_end()
		)
	at_Mx.setDefault('0')
	
	# My
	at_My = MpcAttributeMetaData()
	at_My.type = MpcAttributeType.String
	at_My.name = 'My'
	at_My.group = 'Data'
	at_My.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('My')+'<br/>') + 
		html_par('f(y) e.g.:') +
		html_par('(y**2+y**2)**0.5') +
		html_end()
		)
	at_My.setDefault('0')
	
	# Mz
	at_Mz = MpcAttributeMetaData()
	at_Mz.type = MpcAttributeType.String
	at_Mz.name = 'Mz'
	at_Mz.group = 'Data'
	at_Mz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mz')+'<br/>') + 
		html_par('f(z) e.g.:') +
		html_par('(z**2+y**2)**0.5') +
		html_end()
		)
	at_Mz.setDefault('0')
	
	# Orientation
	at_Orientation = MpcAttributeMetaData()
	at_Orientation.type = MpcAttributeType.String
	at_Orientation.name = 'Orientation'
	at_Orientation.group = 'Group'
	at_Orientation.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Orientation')+'<br/>') +
		html_par('Choose between "Global" and "Local". To define components in global coordinate system choose "Global". Otherwise choose "Local" to define components in local coordinate system.') +
		html_end()
		)
	at_Orientation.sourceType = MpcAttributeSourceType.List
	at_Orientation.setSourceList(['Global', 'Local'])
	at_Orientation.setDefault('Global')
	
	# constant
	at_global = MpcAttributeMetaData()
	at_global.type = MpcAttributeType.Boolean
	at_global.name = 'Global'
	at_global.group = 'Data'
	at_global.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('global')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_global.editable = False
	
	xom = MpcXObjectMetaData()
	xom.name = 'VolumeCouple'
	xom.addAttribute(at_Mode)
	xom.addAttribute(at_constant)
	xom.addAttribute(at_function)
	xom.addAttribute(at_M)
	xom.addAttribute(at_Mx)
	xom.addAttribute(at_My)
	xom.addAttribute(at_Mz)
	xom.addAttribute(at_Orientation)
	xom.addAttribute(at_global)
	
	# visibility dependencies
	
	# constant-dep
	xom.setVisibilityDependency(at_constant, at_M)
	
	# function-dep
	xom.setVisibilityDependency(at_function, at_Mx)
	xom.setVisibilityDependency(at_function, at_My)
	xom.setVisibilityDependency(at_function, at_Mz)
	
	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(at_Mode, at_constant)
	xom.setBooleanAutoExclusiveDependency(at_Mode, at_function)
	xom.setBooleanAutoExclusiveDependency(at_Orientation, at_global)
	
	return xom

def fillConditionRepresentationData(xobj, pos, data):
	'''
	Fills the 3D vector data.
	
	Set the pressure value
	at the z component, since the orientation is set to local
	'''
	M = xobj.getAttribute('M').quantityVector3.value
	Mode = xobj.getAttribute('Mode').string
	
	sfx = xobj.getAttribute('Mx').string
	sfy = xobj.getAttribute('My').string
	sfz = xobj.getAttribute('Mz').string
	
	if (Mode == 'function'):
		
		seval = SpatialFunctionEval(pos)
		
		dx = seval.make(sfx)		#spatial function x
		dy = seval.make(sfy)		#spatial function y
		dz = seval.make(sfz)		#spatial function z
		
		data[0] = dx
		data[1] = dy
		data[2] = dz
	
	else:
		data[0] = M.x
		data[1] = M.y
		data[2] = M.z

def makeConditionRepresentationData(xobj):
	'''
	Create the condition representation data for STKO.
	Here we want an arrow (vector) representation in local
	coordinate system, that can be applied only on faces.
	We need to allocate a 3d vector for the data attribute.
	The components of this vector will be set using
	@ref fillConditionRepresentationData
	'''
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.DoubleArrows
	d.orientation = MpcConditionVRepOrientation.Global
	
	at_global = xobj.getAttribute('Global')
	if at_global is not None:
		if not at_global.boolean:
			d.orientation = MpcConditionVRepOrientation.Local
	
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = False
	d.on_faces = False
	d.on_solids = True
	d.on_interactions = False
	return d

def __process_couple (doc, pinfo, ClassName, all_geom, Mode, M, is_partitioned, process_id, process_block_count, sfx, sfy, sfz, is_Global):
	first_done = False
	for geom, subset in all_geom.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		for i in subset.solids:
			domain = mesh_of_geom.solids[i]
			for elem in domain.elements:
			
				if is_partitioned :
					if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
						continue
			
				n = len(elem.nodes)
				ngp = len(elem.integrationRule.integrationPoints)
				
				if not is_Global:
					MT = elem.orientation.quaternion.rotate(M)
				else:
					MT = M
					
				# obtain nodal values of the distributed condition
				nodal_values = [[0.0, 0.0, 0.0] for i in range(n)]
				if Mode == 'function':
					for i in range(n):
						nodei = elem.nodes[i]
						seval = SpatialFunctionEval(nodei.position)
						nodal_values[i][0] = seval.make(sfx)
						nodal_values[i][1] = seval.make(sfy)
						nodal_values[i][2] = seval.make(sfz)
						if not is_Global:
							M_function = elem.orientation.quaternion.rotate(vec3(nodal_values[i][0], nodal_values[i][1], nodal_values[i][2]))
							nodal_values[i][0] = M_function[0]
							nodal_values[i][1] = M_function[1]
							nodal_values[i][2] = M_function[2]
				else:
					for i in range(n):
						nodal_values[i][0] = MT.x
						nodal_values[i][1] = MT.y
						nodal_values[i][2] = MT.z
				
				# do nodal lumping
				nodal_lumped_values = [[0.0, 0.0, 0.0, 0.0] for i in range(n)]
				for gp in range(ngp):
					gauss_point = elem.integrationRule.integrationPoints[gp]
					N = elem.shapeFunctionsAt(gauss_point)
					det_J = elem.jacobianAt(gauss_point).det()
					W = gauss_point.w
					
					# interpolate nodal value at this gp
					fx = 0.0
					fy = 0.0
					fz = 0.0
					for i in range(n):
						Ni = N[i]
						fx += Ni * nodal_values[i][0]
						fy += Ni * nodal_values[i][1]
						fz += Ni * nodal_values[i][2]
					
					for i in range(n):
						fact = N[i] * det_J * W
						lump = nodal_lumped_values[i]
						lump[0] = elem.nodes[i].id
						lump[1] += fx * fact
						lump[2] += fy * fact
						lump[3] += fz * fact
						
				for i in range(n):
					lump = nodal_lumped_values[i]
					lump[0] = elem.nodes[i].id
					
					str_tcl = []
					
					if (lump[0] in pinfo.node_to_model_map):
					
						if is_partitioned :
							if not first_done:
								if process_block_count == 0:
									pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
								else:
									pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
								first_done = True
					
						spatial_info = pinfo.node_to_model_map[lump[0]]
						node_ndm = spatial_info[0]
						node_ndf = spatial_info[1]
						if (node_ndm == 2):
							if (node_ndf == 3):
								sopt = ('\n'.join(['0.0 0.0 {}'.format(lump[3])]))
						else:
							if (node_ndf == 3) or (node_ndf == 4):
								# ndm: 2; ndf: 2
								raise Exception('Error: ndm/ndf pair is incompatible with "{}". node: {}; ndm: {}; ndf: {}'.format(ClassName, lump[0], node_ndm, node_ndf))
							elif (node_ndf == 6):
								sopt = ('\n'.join(['0.0 0.0 0.0 {} {} {}'.format(lump[1], lump[2], lump[3])]))
					else :
						raise Exception('Error: node without assigned element')
					str_tcl.append('{}{}load {} {}'.format(pinfo.indent, pinfo.tabIndent, lump[0], sopt))
					
					# now write the string into the file
					pinfo.out_file.write('\n'.join(str_tcl))
					pinfo.out_file.write('\n')
					
	if is_partitioned :
		if first_done:
			process_block_count += 1
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count

def writeTcl_Force(pinfo, xobj):
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	
	Global_at = xobj.getAttribute('Global')
	if(Global_at is None):
		raise Exception('Error: cannot find "Global" attribute')
	is_Global = Global_at.boolean
	
	Mode_at = xobj.getAttribute('Mode')
	if(Mode_at is None):
		raise Exception('Error: cannot find "Mode" attribute')
	Mode = Mode_at.string
	
	M_at = xobj.getAttribute('M')
	if(M_at is None):
		raise Exception('Error: cannot find "M" attribute')
	M = M_at.quantityVector3.value
	
	Mx_at = xobj.getAttribute('Mx')
	if(Mx_at is None):
		raise Exception('Error: cannot find "Mx" attribute')
	Mx = Mx_at.string
	
	My_at = xobj.getAttribute('My')
	if(My_at is None):
		raise Exception('Error: cannot find "My" attribute')
	My = My_at.string
	
	Mz_at = xobj.getAttribute('Mz')
	if(Mz_at is None):
		raise Exception('Error: cannot find "Mz" attribute')
	Mz = Mz_at.string
	
	sfx = 0
	sfy = 0
	sfz = 0
	
	if (Mode == 'function'):
		sfx = Mx
		sfy = My
		sfz = Mz
	
	doc = App.caeDocument()
	
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			process_block_count = __process_couple (doc, pinfo, ClassName, all_geom, Mode, M, is_partitioned, process_id, process_block_count, sfx, sfy, sfz, is_Global)
	else :
		__process_couple (doc, pinfo, ClassName, all_geom, Mode, M, is_partitioned, 0, 0, sfx, sfy, sfz, is_Global)