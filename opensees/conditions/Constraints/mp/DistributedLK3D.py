import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# C
	at_C = MpcAttributeMetaData()
	at_C.type = MpcAttributeType.Real
	at_C.name = 'C'
	at_C.group = 'Material x'
	at_C.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('C')+'<br/>') + 
		html_par('damping coeficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Viscous_Material','Viscous Material')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Material x'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('power factor (=1 means linear damping)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Viscous_Material','Viscous Material')+'<br/>') +
		html_end()
		)
	
	# C
	at_C_T = MpcAttributeMetaData()
	at_C_T.type = MpcAttributeType.Real
	at_C_T.name = 'C/T'
	at_C_T.group = 'Material y'
	at_C_T.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('C')+'<br/>') + 
		html_par('damping coeficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Viscous_Material','Viscous Material')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alpha_T = MpcAttributeMetaData()
	at_alpha_T.type = MpcAttributeType.Real
	at_alpha_T.name = 'alpha/T'
	at_alpha_T.group = 'Material y'
	at_alpha_T.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('power factor (=1 means linear damping)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Viscous_Material','Viscous Material')+'<br/>') +
		html_end()
		)
	
	# C
	at_C_T2 = MpcAttributeMetaData()
	at_C_T2.type = MpcAttributeType.Real
	at_C_T2.name = 'C/T2'
	at_C_T2.group = 'Material z'
	at_C_T2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('C')+'<br/>') + 
		html_par('damping coeficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Viscous_Material','Viscous Material')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alpha_T2 = MpcAttributeMetaData()
	at_alpha_T2.type = MpcAttributeType.Real
	at_alpha_T2.name = 'alpha/T2'
	at_alpha_T2.group = 'Material z'
	at_alpha_T2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('power factor (=1 means linear damping)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Viscous_Material','Viscous Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'DistributedLK3D'
	xom.addAttribute(at_C)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_C_T)
	xom.addAttribute(at_C_T2)
	xom.addAttribute(at_alpha_T)
	xom.addAttribute(at_alpha_T2)
	
	return xom

def makeConditionRepresentationData(xobj):
	'''
	Create the condition representation data for STKO.
	Here we want an simple points (vector) representation in global
	coordinate system, that can be applied only on interactions.
	'''
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Points
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array()
	d.on_vertices = False
	d.on_edges = False
	d.on_faces = True
	d.on_solids = False
	d.on_interactions = False
	
	return d

class extra_node_data_t:
	def __init__(self):
		self.N1 = None # the id of the fixed node corresponding to the source node (always)
		self.N2 = None # the id of the extra node tied to the source node with the EDOF (sometimes)
		self.area = 0.0
		self.vx = Math.vec3(0.0, 0.0, 0.0)
		self.vy = Math.vec3(0.0, 0.0, 0.0)

def __processEdgeDistributedLK (pinfo, doc, all_geom, alpha, C, alpha_T, C_T,
								C_T2, alpha_T2, is_partitioned, process_id, process_block_count, indent):
	tag = pinfo.next_elem_id
	mat_tag = pinfo.next_physicalProperties_id
	first_done = False
	for geom, subset in all_geom.items():
		extra_node_data = {}
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		for face_id in subset.faces:
			domain = mesh_of_geom.faces[face_id]
			for elem in domain.elements:
				# compute vectors
				orientation_matrix = elem.orientation.quaternion.toRotationMatrix()
				vect_x = orientation_matrix.col(0)
				vect_y = orientation_matrix.col(1)
				# check partitioning
				if is_partitioned :
					if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
						continue
					if not first_done:
						if process_block_count == 0:
							pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
						else:
							pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
						first_done = True
				# do nodal lumping
				n = len(elem.nodes)
				for gauss_point in elem.integrationRule.integrationPoints:
					N = elem.shapeFunctionsAt(gauss_point)
					det_J = elem.jacobianAt(gauss_point).det()
					W = gauss_point.w
					for i in range(n):
						inode = elem.nodes[i]
						fact = N[i] * det_J * W
						if not inode.id in extra_node_data:
							# write new node
							# save node data
							new_node_data = extra_node_data_t()
							new_node_data.N1 = pinfo.next_node_id
							new_node_data.area = fact
							new_node_data.vx = vect_x
							new_node_data.vy = vect_y
							extra_node_data[inode.id] = new_node_data
							spatial_info = pinfo.node_to_model_map[inode.id]
							node_ndm = spatial_info[0]
							node_ndf = spatial_info[1]
							if node_ndm == 2:
								raise Exception('Error: dimensions 2D for condition 3D')
							if node_ndm != node_ndf :
								pinfo.next_node_id += 1
								new_node_data.N2 = pinfo.next_node_id
							pinfo.next_node_id += 1
							
						else:
							# accumulate
							prev_node_data = extra_node_data[inode.id]
							prev_node_data.area += fact
							new_node_data.vx = vect_x
							new_node_data.vy = vect_y
							
		if not is_partitioned:
			pinfo.out_file.write('\n{}{}{}'.format(pinfo.indent, indent, '# distributedLK 3D'))
			pinfo.out_file.write('\n{}{}{}{}{}{}{}{}{}{}{}'.format(pinfo.indent, indent, '#	uniaxialMaterial Viscous\n', indent, '#	node tag x y z\n',
								indent, '#	equalDOF node_i node_j 1 2 3\n', indent, '#	fix tag 1 1 1\n', indent, '#	element zeroLength\n'))
		else:
			if first_done:
				pinfo.out_file.write('\n{}{}{}'.format(pinfo.indent, indent, '# distributedLK 3D'))
				pinfo.out_file.write('\n{}{}{}{}{}{}{}{}{}{}{}'.format(pinfo.indent, indent, '#	uniaxialMaterial Viscous\n', indent, '#	node tag x y z\n',
									indent, '#	equalDOF node_i node_j 1 2 3\n', indent, '#	fix tag 1 1 1\n', indent, '#	element zeroLength\n'))
		
		for source_node_id, node_data in extra_node_data.items():
			# material
			spatial_info = pinfo.node_to_model_map[source_node_id]
			node_ndm = spatial_info[0]
			node_ndf = spatial_info[1]
			pinfo.updateModelBuilder(node_ndm, node_ndm) # ndm, ndm (i.e. ndf = ndm because we always make the duplicated nodes U only, no Pressure)
			mat_T = mat_tag
			mat_T1 = ''
			dirT1  = ''
			mat_T2 = ''
			dirT2  = ''
			pinfo.out_file.write('\n{}{}uniaxialMaterial Viscous {} {} {}\n'.format(pinfo.indent, indent, mat_tag, node_data.area * C, alpha))
			mat_tag = mat_tag + 1
			pinfo.out_file.write('{}{}uniaxialMaterial Viscous {} {} {}\n'.format(pinfo.indent, indent, mat_tag, node_data.area * C_T, alpha_T))
			mat_T1 = ' {}'.format(mat_tag)
			dirT1 = ' {}'.format(2)
			mat_tag = mat_tag + 1
			pinfo.out_file.write('{}{}uniaxialMaterial Viscous {} {} {}\n'.format(pinfo.indent, indent, mat_tag, node_data.area * C_T2, alpha_T2))
			mat_T2 = ' {}'.format(mat_tag)
			dirT2 = ' {}'.format(3)
				
			dir = '{}'.format(' 1 2 3') # 1 2 3
			
			strMat = ' {}{}{}'.format(mat_T, mat_T1, mat_T2)
			# node N1 always created
			Node1 = extra_node_data[source_node_id].N1
			node_N1 = doc.mesh.nodes[source_node_id]
			if node_ndm == 2:
				coordinateN1 = '{} {}'.format(node_N1.x, node_N1.y)
			else:
				coordinateN1 = '{} {} {}'.format(node_N1.x, node_N1.y, node_N1.z)
			pinfo.out_file.write('{}{}node {} {}\n'.format(pinfo.indent, indent, Node1, coordinateN1))
			orient11 = extra_node_data[source_node_id].vx
			orient12 = extra_node_data[source_node_id].vy
			# node N2 check if created
			if extra_node_data[source_node_id].N2 is not None:
				Node2 = extra_node_data[source_node_id].N2
				node_N2 = doc.mesh.nodes[source_node_id]
				orient21 = extra_node_data[source_node_id].vx
				orient22 = extra_node_data[source_node_id].vy
				
				if node_ndm == 2:
					coordinateN2 = '{} {}'.format(node_N2.x, node_N2.y)
				else:
					coordinateN2 = '{} {} {}'.format(node_N2.x, node_N2.y, node_N2.z)
				pinfo.out_file.write('{}{}node {} {}\n'.format(pinfo.indent, indent, Node2, coordinateN2))
				pinfo.out_file.write('{}{}equalDOF {} {} 1 2 3\n'.format(pinfo.indent, indent, source_node_id, extra_node_data[source_node_id].N1))
				pinfo.out_file.write('{}{}fix {} 1 1 1\n'.format(pinfo.indent, indent, Node2))
				pinfo.out_file.write('{}{}element zeroLength {} {} {} -mat{} -dir{} -orient {} {} {} {} {} {}\n'.format(
					pinfo.indent, indent, tag, Node1, Node2, strMat, dir, orient21.x, orient21.y, orient21.z, orient22.x, orient22.y, orient22.z))
			else:
				pinfo.out_file.write('{}{}fix {} 1 1 1\n'.format(pinfo.indent, indent, Node1))
				pinfo.out_file.write('{}{}element zeroLength {} {} {} -mat{} -dir{} -orient {} {} {} {} {} {}\n'.format(
					pinfo.indent, indent, tag, source_node_id, Node1, strMat, dir, orient11.x, orient11.y, orient11.z, orient12.x, orient12.y, orient12.z))
			mat_tag = mat_tag + 1
			tag = tag + 1
			pinfo.next_physicalProperties_id = mat_tag
			pinfo.next_elem_id = tag
			
			auto_gen_data = tclin.auto_generated_element_data()
			auto_gen_data.elements = [tag]
			pinfo.auto_generated_element_data_map[tag] = auto_gen_data
			
	if is_partitioned :
		if first_done:
			process_block_count += 1
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count

def writeTcl_mpConstraints(pinfo):
	
	# uniaxialMaterial Viscous
	# node x y
	# equalDOF node_master node_slave 1 2 3
	# fix 1 1
	# element zeroLength 
	# pinfo.updateModelBuilder(pinfo.ndm, pinfo.ndf)
	
	xobj = pinfo.condition.XObject
	
	C_at = xobj.getAttribute('C')
	if(C_at is None):
		raise Exception('Error: cannot find "C" attribute')
	C = C_at.real
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	C_T_at = xobj.getAttribute('C/T')
	if(C_T_at is None):
		raise Exception('Error: cannot find "C/T" attribute')
	C_T = C_T_at.real
	
	alpha_T_at = xobj.getAttribute('alpha/T')
	if(alpha_T_at is None):
		raise Exception('Error: cannot find "alpha/T" attribute')
	alpha_T = alpha_T_at.real
	
	C_T2_at = xobj.getAttribute('C/T2')
	if(C_T2_at is None):
		raise Exception('Error: cannot find "C/T" attribute')
	C_T2 = C_T2_at.real
	
	alpha_T2_at = xobj.getAttribute('alpha/T2')
	if(alpha_T2_at is None):
		raise Exception('Error: cannot find "alpha/T" attribute')
	alpha_T2 = alpha_T2_at.real
	
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			pinfo.setProcessId(process_id)
			process_block_count = __processEdgeDistributedLK (pinfo, doc, all_geom, alpha, C, alpha_T, C_T,
			C_T2, alpha_T2, is_partitioned, process_id, process_block_count, pinfo.tabIndent)
		pinfo.out_file.write('\n')
	else:
		__processEdgeDistributedLK (pinfo, doc, all_geom, alpha, C, alpha_T, C_T, 
		C_T2, alpha_T2, is_partitioned, 0, 0, pinfo.indent)