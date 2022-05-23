import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	# matTag
	at_matTag = MpcAttributeMetaData()
	at_matTag.type = MpcAttributeType.Index
	at_matTag.name = 'matTag'
	at_matTag.group = 'Group'
	at_matTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') +
		html_par('A previously-defined UniaxialMaterial that defines the Tau-Slip behavior along the UX DOF in the local coordinate system.') +
		html_end()
		)
	at_matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag.indexSource.addAllowedNamespace("materials.uniaxial")

	# K
	at_K = MpcAttributeMetaData()
	at_K.type = MpcAttributeType.Real
	at_K.name = 'K (penalty)'
	at_K.group = 'Group'
	at_K.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K (penalty)')+'<br/>') +
		html_par('K (Penalty) A penalty value to enforce continuity in the other DOFs in the local coordinate system.') +
		html_end()
		)
	at_K.setDefault(1.0e18)
	
	xom = MpcXObjectMetaData()
	xom.name = 'beamToSolidBarSlip'
	xom.addAttribute(at_matTag)
	xom.addAttribute(at_K)
	return xom

def getRequestedNodalSpatialDim(xobj):
	'''
	similar to the def getNodalSpatialDim(xobj, xobj_phys_prop) method in element properties,
	but with a conceptual difference. getNodalSpatialDim returns a list of (ndm,ndf) pair
	whose length is equal to the number of nodes for that element, following the local
	numbering of each element.
	Here instead we return a map, where the key is the ID of the (only) nodes where
	the condition requires a specific dimension (here for example the master node)
	'''
	requested_node_dim_map = {}
	condition = xobj.parent
	all_inter = condition.assignment.interactions
	doc = App.caeDocument()
	for inter in all_inter:
		moi = doc.mesh.getMeshedInteraction(inter.id)
		for elem in moi.elements:
			if (len(elem.nodes) < 2 or elem.numberOfMasterNodes() != 1):
				raise Exception('wrong master-slave connectivity, expected: 1 master, N(>0) slaves, given: {} masters, {} slaves'.format(elem.numberOfMasterNodes(), elem.numberOfSlaveNodes()))
			mid = elem.nodes[0].id
			requested_node_dim_map[mid] = (3, 6)
	
	return requested_node_dim_map

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
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = True
	
	return d

class extra_node_data_t:
	def __init__(self):
		self.area = 0.0

def __beamToSolidBarSlip (doc, all_inter, pinfo, type, is_partitioned, process_id, process_block_count, matTag, K, indent):
	
	# utils
	def next_elem_id():
		i = pinfo.next_elem_id
		pinfo.next_elem_id += 1
		return i
	def next_prop_id():
		i = pinfo.next_physicalProperties_id
		pinfo.next_physicalProperties_id += 1
		return i

	first_done =False
	FMT = pinfo.get_double_formatter()

	str_tcl = ('{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}'.format(
		indent,
		"#	node tag x y z\n",
		"#	rigidLink beam node_i node_j\n",
		"#	node tag x y z\n",
		"#	equalDOF node_i node_j 1 2 3\n",
		"#	equalDOF node_i node_j      4 5 6\n",
		"#	uniaxialMaterial Parallel\n"
		"#	uniaxialMaterial Elastic\n",
		"#	element zeroLength\n"))
	
	# map node to direction
	map_node_dir ={}
	for inter in all_inter:
		for master in inter.items.masters:
			if str(master.subshapeType) != 'Edge':
				continue
			geom_id = master.geometry.id
			geom = doc.mesh.getMeshedGeometry(geom_id)
			for edge in geom.edges:
				for elem in edge.elements:
					for node in elem.nodes:
						orientation_matrix = elem.orientation.quaternion.toRotationMatrix()
						vecX = orientation_matrix.col(0)
						if not node.id in map_node_dir:
							map_node_dir[node.id] = vecX
						else:
							map_node_dir[node.id] += vecX

	for k, v in map_node_dir.items():
		map_node_dir[k] = v.normalized()

	for inter in all_inter:
		extra_node_data = {}
		for slave in inter.items.slaves:
			if str(slave.subshapeType) != 'Face':
				continue
			geom_id = slave.geometry.id
			geom = doc.mesh.getMeshedGeometry(geom_id)
			for elem in geom.faces[slave.subshapeId].elements:
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
							new_node_data = extra_node_data_t()
							new_node_data.area = fact
							extra_node_data[inode.id] = new_node_data
						else:
							# accumulate
							prev_node_data = extra_node_data[inode.id]
							prev_node_data.area += fact

		moi = doc.mesh.getMeshedInteraction(inter.id)
		for elem in moi.elements:
			if (len(elem.nodes) < 2 or elem.numberOfMasterNodes() != 1):
				raise Exception('wrong master-slave connectivity, expected: 1 master, N(>0) slaves, given: {} masters, {} slaves'.format(elem.numberOfMasterNodes(), elem.numberOfSlaveNodes()))
			mid = elem.nodes[0].id
			sid = elem.nodes[1].id

			if (mid in pinfo.node_to_model_map):
				ndm_map = pinfo.node_to_model_map[mid][0]
				ndf_map = pinfo.node_to_model_map[mid][1]
				if (ndm_map != 3 or ndf_map != 6):
					raise Exception('Error: The beamToSolidBarSlip command works only for problems in 3 ndm and 6 ndf for master node')
			if is_partitioned:
				if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
					continue
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
					first_done = True
			for i in range(1, len(elem.nodes)):
				if (elem.nodes[i].id in pinfo.node_to_model_map):
					ndm_map = pinfo.node_to_model_map[elem.nodes[i].id][0]
					ndf_map = pinfo.node_to_model_map[elem.nodes[i].id][1]
					if (ndm_map != 3 or (ndf_map != 3 and ndf_map != 4)):
						raise Exception('Error: The beamToSolidBarSlip command works only for problems in 3 ndm and 3 or 4 ndf for slave nodes')
			if not is_partitioned:
				pinfo.out_file.write("\n{}# beamToSolidBarSlip\n".format(indent))
				if not first_done:
					pinfo.out_file.write(str_tcl)
					first_done = True
			else:
				if first_done:
					pinfo.out_file.write("\n{}# beamToSolidBarSlip\n".format(indent))
					pinfo.out_file.write(str_tcl)
			
			mat_dir = "0"
			isPenaltyMaterial = False
			for i in range(1, len(elem.nodes)):
				pinfo.updateModelBuilder(3, 6)
				node_extra = pinfo.next_node_id
				dir_node = map_node_dir[mid]
				dirX = abs(dir_node.x)
				dirY = abs(dir_node.y)
				dirZ = abs(dir_node.z)
				if dirX > 0.999:
					mat_dir = "1"
					str_edof = '2 3 4 5 6'
				elif dirY > 0.999:
					mat_dir = "2"
					str_edof = '1 3 4 5 6'
				elif dirZ > 0.999:
					mat_dir = "3"
					str_edof = '1 2 4 5 6'
				else:
					isPenaltyMaterial = True
					mat_dir = "1 2 3"
					str_edof = '4 5 6'

				pinfo.out_file.write("{0}#	connect master node {1} and slave node {2}\n\n".format(indent, mid, elem.nodes[i].id))
				node_N1 = doc.mesh.nodes[elem.nodes[i].id]
				coordinateN1 = ' {} {} {}'.format(FMT(node_N1.x), FMT(node_N1.y), FMT(node_N1.z))
				pinfo.out_file.write('{}{}node {}{}\n'.format(pinfo.indent, indent, node_extra, coordinateN1))
				pinfo.out_file.write('{}{}rigidLink {} {} {}\n'.format(pinfo.indent, indent, type, mid, node_extra)) 
				pinfo.next_node_id += 1
				node_extra_1 = pinfo.next_node_id
				pinfo.out_file.write('{}{}node {}{}\n'.format(pinfo.indent, indent, node_extra_1, coordinateN1))
				pinfo.out_file.write('{}{}equalDOF {} {} {}\n'.format(pinfo.indent, indent, node_extra_1, elem.nodes[i].id,  "1 2 3"))
				pinfo.out_file.write('{}{}equalDOF {} {} {}\n'.format(pinfo.indent, indent, node_extra, node_extra_1, str_edof))
				
				#mat_tag = next_prop_id()
				mat_tag_parallel = next_prop_id() # auto-generated parallel material
				str_mat_tag = '{}'.format(mat_tag_parallel)
				#print("area: ", extra_node_data[sid].area)
				pinfo.out_file.write('{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, mat_tag_parallel, matTag, extra_node_data[sid].area))
				#uniaxialMaterial Elastic $matTag $E
				#pinfo.out_file.write('{}{}uniaxialMaterial Elastic {} {}\n'.format(pinfo.indent, indent, mat_tag, E.value))
				if isPenaltyMaterial:
					mat_tag1 = next_prop_id()
					pinfo.out_file.write('{}{}uniaxialMaterial Elastic {} {}\n'.format(pinfo.indent, indent, mat_tag1, K))
					mat_tag2 = next_prop_id()
					pinfo.out_file.write('{}{}uniaxialMaterial Elastic {} {}\n'.format(pinfo.indent, indent, mat_tag2, K))
					if (dirZ < dirX > dirY ):
						str_mat_tag = '{} {} {}'.format(mat_tag_parallel, mat_tag1, mat_tag2)
					elif (dirZ < dirY> dirX ):
						str_mat_tag = '{} {} {}'.format(mat_tag1, mat_tag_parallel, mat_tag2)
					elif (dirX < dirZ > dirY ):
						str_mat_tag = '{} {} {}'.format(mat_tag2, mat_tag1, mat_tag_parallel)

				#element zeroLength $eleTag $iNode $jNode -mat $matTag1 $matTag2 ... -dir $dir1 $dir2 ...<-doRayleigh $rFlag> <-orient $x1 $x2 $x3 $yp1 $yp2 $yp3>
				# orientation vectors
				vect_x=elem.orientation.computeOrientation().col(0)
				vect_y=elem.orientation.computeOrientation().col(1)
				pinfo.out_file.write(
				'{0}{1}element zeroLength {2} {3} {4} -mat {5} -dir {6} -orient {7} {8} {9} {10} {11} {12}\n'.format(
					pinfo.indent, indent, # 0 1
					next_elem_id(), node_extra, node_extra_1,  # 2 3 4
					str_mat_tag, mat_dir, # 5 5
					vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
					)
				pinfo.next_node_id += 1
	if is_partitioned:
		if first_done:
			process_block_count += 1
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count

def writeTcl_mpConstraints(pinfo):
	
	# node tag x y z	(first)							node generate coordinate == coordinate node original
	# rigidLink											node_master = node original			node_slave = first node generate
	# node tag x y z	(second)						node generate coordinate == coordinate node original
	# equalDOF node_master node_slave 1 2 3				node_master = second node generate		node_slave = node original
	# equalDOF node_master node_slave 1 2 3 . . .		node_master = first node generate		node_slave = second node generate
	# uniaxialMaterial Elastic
	# if penalty -> uniaxialMaterial Elastic
	# if penalty -> uniaxialMaterial Elastic
	# element zeroLength								node_master = first node generate		node_slave = second node generate

	xobj = pinfo.condition.XObject
	tag = pinfo.next_elem_id
	
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	all_inter = pinfo.condition.assignment.interactions
	if len(all_inter) == 0:
		return

	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
		
	type = 'beam' # geta('type').string
	matTag = geta('matTag').index
	K = geta('K (penalty)').real

	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			pinfo.setProcessId(process_id)
			process_block_count = __beamToSolidBarSlip (doc, all_inter, pinfo, type, is_partitioned, process_id, process_block_count, matTag, K, pinfo.tabIndent)
	else:
		__beamToSolidBarSlip (doc, all_inter, pinfo, type, is_partitioned, 0, 0, matTag, K, pinfo.indent)