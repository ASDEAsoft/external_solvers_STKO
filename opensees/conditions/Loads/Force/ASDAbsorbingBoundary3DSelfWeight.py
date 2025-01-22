import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *

def makeXObjectMetaData():
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.QuantityVector3
	at_b.name = 'b'
	at_b.group = 'Data'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b')+'<br/>') + 
		html_par('The body force vector') +
		html_end()
		)
	at_b.dimension = u.F/u.L**3
	xom = MpcXObjectMetaData()
	xom.name = 'ASDAbsorbingBoundary3DSelfWeight'
	xom.addAttribute(at_b)
	return xom

def fillConditionRepresentationData(xobj, pos, data):
	b = xobj.getAttribute('b').quantityVector3.value
	data[0] = b.x
	data[1] = b.y
	data[2] = b.z

def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Arrows
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = False
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = False
	return d

def __process_load(doc, pinfo, manager, ele_data, b, is_partitioned, process_id, process_block_count):
	first_done = False
	# process all elements in this partition
	for etag, ex_volume, conn, bcode in ele_data:
		#mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		#for i in subset.solids:
		#	domain = mesh_of_geom.solids[i]
		#	for elem in domain.elements:
			
				if is_partitioned :
					if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
						continue
			
				n = len(elem.nodes)
				ngp = len(elem.integrationRule.integrationPoints)
				
				if not is_Global:
					FT = elem.orientation.quaternion.rotate(F)
				else:
					FT = F
				
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
							F_function = elem.orientation.quaternion.rotate(vec3(nodal_values[i][0], nodal_values[i][1], nodal_values[i][2]))
							nodal_values[i][0] = F_function[0]
							nodal_values[i][1] = F_function[1]
							nodal_values[i][2] = F_function[2]
						
				else:
					for i in range(n):
						nodal_values[i][0] = FT.x
						nodal_values[i][1] = FT.y
						nodal_values[i][2] = FT.z
				
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
					
					sopt = ('\n'.join(['{} {}'.format(lump[1], lump[2])]))
					if (lump[0] in pinfo.node_to_model_map):
					
						if is_partitioned :
							if not first_done:
								if process_block_count == 0:
									pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
								else:
									pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
								first_done = True
					
						spatial_info = pinfo.node_to_model_map[lump[0]]
						node_ndm = spatial_info[0]
						node_ndf = spatial_info[1]
						if (node_ndm == 2):
							if (node_ndf == 3):
								# sopt += ' 0.0'
								sopt += ('\n'.join([' 0.0']))
						else:
							sopt += ('\n'.join([' {}'.format( lump[3])]))
							if (node_ndf == 4):
								# sopt += ' 0.0'
								sopt += ('\n'.join([' 0.0']))
							elif (node_ndf == 6):
								# sopt += ' 0.0 0.0 0.0'
								sopt += ('\n'.join([' 0.0 0.0 0.0']))
					else :
						raise Exception('Error: node without assigned element')
					str_tcl.append('{}load {} {}'.format(pinfo.indent, lump[0], sopt))
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
	
	b_at = xobj.getAttribute('b')
	if(b_at is None):
		raise Exception('Error: cannot find "b" attribute')
	b = b_at.quantityVector3.value
	
	manager = pinfo.custom_data.get('ASDAbsorbingBoundary3D', None)
	if manager is None:
		raise Exception("Cannot find ASDAbsorbingBoundary3D, probably you didn't use ASDAbsorbingBoundary3DAuto elements")
	
	doc = App.caeDocument()
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	
	# pre-process all nodes where each auto-generated bnd element should put self-weight.
	# here manager.element_volumes already contains either L-R-F-K or corners.
	# for the single bcode we can lump load at the nodes not in STKO mesh (i.e outer 4 nodes).
	# for corners, only at the outer-most 2 nodes, not shared by the pure sides!
	map_nodes_by_sides = {}
	for pid, ele_data in manager.element_volumes.items():
		for etag, ex_volume, conn, bcode in ele_data:
			if isinstance(bcode, int): # pure side
				nodes_on_sides = map_nodes_by_sides.get(bcode, None)
				if nodes_on_sides is None:
					nodes_on_sides = set()
					map_nodes_by_sides[bcode] = nodes_on_sides
				for inode in conn:
					if inode not in doc.mesh.nodes:
						nodes_on_sides.add(inode)
	
	for pid, ele_data in manager.element_volumes.items():
		# open partition-if-block
		if is_partitioned:
			pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', pid, '} {'))
		
		# process each absorbing element auto-generated on this partition
		for etag, ex_volume, conn, bcode in ele_data:
			# extract only nodes that should be loaded
			# we assume 
			if isinstance(bcode, int):
				allowed = map_nodes_by_sides[bcode]
				ex_nodes = [i for i in conn if i in allowed]
			else:
				allowed_1 = map_nodes_by_sides[bcode[0]]
				allowed_2 = map_nodes_by_sides[bcode[1]]
				ex_nodes = [i for i in conn if (i not in allowed_1 and i not in allowed_2 and i not in doc.mesh.nodes)]
			dV = ex_volume / float(len(ex_nodes))
			for inode in ex_nodes:
				pinfo.out_file.write('{}load {} {:.12g} {:.12g} {:.12g}\n'.format(pinfo.indent, inode, b[0]*dV, b[1]*dV, b[2]*dV))
		# close partition-if-block
		if is_partitioned:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
	
	#if is_partitioned:
	#	process_block_count = 0
	#	for process_id in range(pinfo.process_count):
	#		process_block_count = __process_load(doc, pinfo, all_geom, b, is_partitioned, process_id, process_block_count, sfx, sfy, sfz, is_Global)
	#else :
	#	__process_load(doc, pinfo, all_geom, Mode, F, is_partitioned, 0, 0, sfx, sfy, sfz, is_Global)