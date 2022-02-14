import importlib
import opensees.utils.tcl_input as tclin
from opensees.utils.tcl_input import element_nodal_dims as element_nodal_dims_t
import PyMpc
import PyMpc.App

def __make_list(ndf):
	'''
	the second item in nodal space descriptor (NDF) can be either a scalar or a list.
	this function makes sure it is a list
	'''
	if isinstance(ndf, list):
		return ndf
	else:
		return [ndf]

def __intersection(a, b):
	'''
	creates an a list which is intersection between a and b.
	in the new list the order is the same as in the input items in a
	'''
	return [i for i in a if i in b]

def fill_node_mass_map(doc, pinfo):
	'''
	fill the map of the masses
	'''
	print('pre-process masses...')
	for item_id, item in doc.conditions.items():
		xobj = item.XObject
		if(xobj is None):
			raise Exception('null XObject in conditions object')
		module_name = 'opensees.conditions.{}.{}'.format(xobj.Xnamespace, xobj.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'fillNodeMassMap'):
			pinfo.condition = item
			module.fillNodeMassMap(pinfo)

def __postprocess_domain_collection_nodes(pinfo):

	# block durations for progress monitoring
	# this method is called by anothe one, its duration is 50% of the calling
	# one.
	duration_post = 0.5
	num_elem = len(pinfo.element_nodal_dims_list)
	num_elem *= 3 # the first loop typically converges in 2 iterations, the secon one in 1
	increment = 0.5/max(num_elem, 1)
	PyMpc.App.monitor().setAutoIncrement(increment)
	if num_elem > 20:
		PyMpc.App.monitor().setDisplayIncrement(duration_post/20)
	else:
		PyMpc.App.monitor().setDisplayIncrement(0.0)

	# here we do some while(true) loops. they should work and stop correctly,
	# but just to make sure they will not run indefinitely, we use a max counter
	max_iter = 0
	for elem in pinfo.element_nodal_dims_list:
		max_iter += len(elem.nodes)
	max_iter *= 10 # just some more room

	# this first loop builds the pinfo.node_to_model_map starting for info in 
	# pinfo.element_nodal_dims_list.
	# if there are elements that support multiple dofs we make intersection
	# of ndf (lists) at nodes.
	iter = 0
	while(True):
		change_counter = 0
		iter += 1
		for elem in pinfo.element_nodal_dims_list:
			for i in range(len(elem.nodes)):
				node = elem.nodes[i]
				dim = elem.dims[i]
				dim = (dim[0], __make_list(dim[1]))
				dof = dim[1]
				if node in pinfo.node_to_model_map:
					prev_dim = pinfo.node_to_model_map[node]
					if prev_dim[0] != dim[0]:
						raise Exception('Error: Different dimensions on same node (node = {}, {}-{}). You cannot mix 2D and 3D models!'.format(node, prev_dim[0], dim[0]))
					prev_dof = __make_list(prev_dim[1])
					if dof == prev_dof:
						continue
					int_dof = __intersection(prev_dof, dof)
					l_nd = len(int_dof)
					if l_nd == 0:
						raise Exception('Error: Different NDF on same node (node = {}, NDF1 = {}, NDF2 = {})'.format(node, dof, prev_dof))
					else:
						pinfo.node_to_model_map[node] = (dim[0], int_dof)
					elem.dims[i] = pinfo.node_to_model_map[node]
					change_counter += 1
				else:
					pinfo.node_to_model_map[node] = dim
					change_counter += 1
			if iter < 3:
				PyMpc.App.monitor().sendAutoIncrement()

		if change_counter == 0:
			break
		if iter > max_iter:
			raise Exception('cannot terminate the loop in the maximum number of iterations')
	PyMpc.App.monitor().sendMessage('loop 1 finished in {} iterations.'.format(iter))
	
	# here we make sure that each element that has multiple dofs in its nodes,
	# can find an intersection between them
	iter = 0
	while(True):
		change_counter = 0
		iter += 1
		for elem in pinfo.element_nodal_dims_list:
			for i in range(len(elem.nodes)):
				node = elem.nodes[i]
				common_dim = elem.dims[i] # todo: rename to local_dim
				dim = pinfo.node_to_model_map[node] # global dim in pinfo map
				# note: dimension are unique, not lists, so make sure the local one
				# is equal to one in pinfo
				if common_dim[0] != dim[0]:
					raise Exception('incompatible moodel dimension for node {}'.format(node))
				dof = dim[1]
				common_dof = common_dim[1]
				int_dof = __intersection(common_dof, dof)
				# we are going to replace the dofs in pinfo with the intersection with 
				# the local ones (int_dofs). do it only if they are different, and so increment the change_counter
				if dof != int_dof:
					pinfo.node_to_model_map[node] = (common_dim[0], int_dof)
					change_counter += 1
			if iter < 2:
				PyMpc.App.monitor().sendAutoIncrement()
		if change_counter == 0:
			break
		if iter > max_iter:
			raise Exception('cannot terminate the loop in the maximum number of iterations')
	PyMpc.App.monitor().sendMessage('loop 2 finished in {} iterations.'.format(iter))
	PyMpc.App.monitor().setDisplayIncrement(0.0)
	
	# if there are some some remaining multiple dofs we choose the first one.
	# in fact, if some element or condition support multiple dof-sets per node,
	# it should place them in order, (i.e. the one they preder goes first).
	# then we transform each list in the ndm/ndf tuple in a integer
	# '''
	for node_id, dim in pinfo.node_to_model_map.items():
		ndf = dim[1]
		if isinstance(ndf, list):
			dim = (dim[0], ndf[0])
			# note: here we are updating the value (not the key)
			pinfo.node_to_model_map[node_id] = dim

def __map_domain_nodes(pinfo, domain, elem_prop, phys_prop):
	'''
	fill a list of elements with nodal ids and their spatial dims.
	'''
	# a null element property is not and error, it means: don't write this element
	# (for example boundary elements)
	# we don't do any check on the phys_prop prop, it's up to the element formulation to check
	# whether it should be non-null
	if(elem_prop is None):
		return

	# get elem formulation elem_module
	xobj = elem_prop.XObject
	if(xobj is None):
		raise Exception('null XObject in element property object')
	elem_module_name = 'opensees.element_properties.{}.{}'.format(xobj.Xnamespace, xobj.name)
	elem_module = importlib.import_module(elem_module_name)
	if not hasattr(elem_module, 'getNodalSpatialDim'):
		return
	
	xobj_pp = None
	if phys_prop is not None:
		xobj_pp = phys_prop.XObject
	
	# get nodal dims for each node in element. make the dofs in dim a list
	node_dims = elem_module.getNodalSpatialDim(xobj, xobj_pp)
	for elem in domain.elements:
		elem_node_dim = []
		elem_node_id = []
		num_nodes = len(elem.nodes)
		#
		# Massimo: changed 11/10/2021 to support element properties with
		# variable number of nodes. they can use the maximum allowed
		#if num_nodes != len(node_dims):
		if num_nodes > len(node_dims):
			raise Exception((
				'the nodal spatial dimension vector obtained from the element module\n'
				'must have the same size as the number of nodes in the element.\n'
				'The element module expects {} nodes, but the mesh element has {} nodes.\n'
				'This happens when an element module is assigned to a wrong mesh type.'
				.format(len(node_dims), num_nodes)
				))
		for j in range(num_nodes):
			# get the original tuple, make a copy with the dof converted to a list
			original_dims = node_dims[j]
			copyed_dims = (original_dims[0], __make_list(original_dims[1]))
			elem_node_dim.append(copyed_dims)
			elem_node_id.append(elem.nodes[j].id)
		# fill list
		pinfo.element_nodal_dims_list.append(element_nodal_dims_t(elem_node_id, elem_node_dim))
		PyMpc.App.monitor().sendAutoIncrement()

def __map_domain_collection_nodes(pinfo, domain_collection, elem_prop_asn_on, phys_prop_asn_on):
	'''
	fill a list of elements with nodal ids and their spatial dims.
	this function is for geometries
	'''
	# for each domain (i.e. for each subshape of geom)
	for domain_id in range(len(domain_collection)):
		domain = domain_collection[domain_id]
		# get physical and element property assigned to this domain
		elem_prop = elem_prop_asn_on[domain_id]
		phys_prop = phys_prop_asn_on[domain_id]
		__map_domain_nodes(pinfo, domain, elem_prop, phys_prop)

def node_map_ndm_ndf (doc, pinfo):

	# block durations
	duration_mapping = 0.45
	duration_cond = 0.05
	duration_post = 0.5
	current_percentage = 0.0

	# first block: mapping of nodal ndm/ndf based on element
	# formulation (about 45% of the work)
	# for each geometry ...
	num_elem = len(doc.mesh.elements)
	increment = 0.5/max(num_elem, 1)
	PyMpc.App.monitor().setAutoIncrement(increment)
	if num_elem > 20:
		PyMpc.App.monitor().setDisplayIncrement(duration_mapping/20)
	else:
		PyMpc.App.monitor().setDisplayIncrement(0.0)
	for geom_id, geom in doc.geometries.items():
		# get the mesh of this geometry
		mesh_of_geom = doc.mesh.meshedGeometries[geom_id]
		if (mesh_of_geom is None):
			raise Exception('null mesh of geom')
		# get physical and element property assignments
		phys_prop_asn = geom.physicalPropertyAssignment
		elem_prop_asn = geom.elementPropertyAssignment
		# map nodes of all domains
		__map_domain_collection_nodes(pinfo, mesh_of_geom.edges, elem_prop_asn.onEdges, phys_prop_asn.onEdges)
		__map_domain_collection_nodes(pinfo, mesh_of_geom.faces, elem_prop_asn.onFaces, phys_prop_asn.onFaces)
		__map_domain_collection_nodes(pinfo, mesh_of_geom.solids, elem_prop_asn.onSolids, phys_prop_asn.onSolids)
	# for each interaction
	for inter_id, inter in doc.interactions.items():
		mesh_of_inter = doc.mesh.meshedInteractions[inter_id]
		elem_prop = inter.elementProperty
		phys_prop = inter.physicalProperty
		__map_domain_nodes(pinfo, mesh_of_inter, elem_prop, phys_prop)
	current_percentage += duration_mapping
	PyMpc.App.monitor().setDisplayIncrement(0.0)
	PyMpc.App.monitor().sendPercentage(current_percentage)

	# some conditions may need to impose a model dimension to some nodes...
	# see for example the master node in rigidDiaphragm.
	# (about 5% of the work)
	for cond_id, cond in doc.conditions.items():
		xobj = cond.XObject
		if(xobj is None):
			raise Exception('null XObject in element property object')
		cond_module_name = 'opensees.conditions.{}.{}'.format(xobj.Xnamespace, xobj.name)
		cond_module = importlib.import_module(cond_module_name)
		if hasattr(cond_module, 'getRequestedNodalSpatialDim'):
			requested_node_dim_map = cond_module.getRequestedNodalSpatialDim(xobj)
			# note here we interpret the whole condition as a monolithic element...
			elem_node_dim = []
			elem_node_id = []
			for node_id, node_dim in requested_node_dim_map.items():
				# make the dofs in dim a list
				elem_node_dim.append((node_dim[0], __make_list(node_dim[1])))
				elem_node_id.append(node_id)
			# fill list
			pinfo.element_nodal_dims_list.append(element_nodal_dims_t(elem_node_id, elem_node_dim))
	current_percentage += duration_cond
	PyMpc.App.monitor().sendPercentage(current_percentage)

	# post process mapped nodes/dims
	# (about 50% of the work)
	__postprocess_domain_collection_nodes(pinfo)
	current_percentage += duration_post
	PyMpc.App.monitor().sendPercentage(current_percentage)

def lagrangian_node(doc, pinfo):
	
	# some elements need to create lagrangian nodes that are not
	# generated by the pre-processor model.
	# their position is not relevant, so we place them outside
	# the bounding box of the real model.
	# in this way it's easy for the user to hide them in the post processor
	for node_id, node in doc.mesh.nodes.items():
		if node.x > pinfo.lagrangian_node_xyz[0]:
			pinfo.lagrangian_node_xyz[0] = node.x
		
		if node.y > pinfo.lagrangian_node_xyz[1]:
			pinfo.lagrangian_node_xyz[1] = node.y
		
		if node.z > pinfo.lagrangian_node_xyz[2]:
			pinfo.lagrangian_node_xyz[2] = node.z
		
		if node_id > pinfo.next_node_id:
			pinfo.next_node_id = node_id
	for i in range(3):
		pinfo.lagrangian_node_xyz[i] *= 1.1
	pinfo.next_node_id += 1

def short_map(doc, pinfo):
	'''
	inverse map. key = (ndm,ndf), value = (node, age)
	'''
	
	for k, v in pinfo.node_to_model_map.items():			# k = node_id, v = (ndm, ndf)
		if not v in pinfo.inv_map:
			pinfo.inv_map[v] = [tclin.node_with_age(k, 0)] 		# init with default 0 age
		else:
			pinfo.inv_map[v].append(tclin.node_with_age(k, 0)) 	# init with default 0 age
	'''
	sort the values map
	'''
	for _, v in pinfo.inv_map.items():
		v.sort(key=lambda a:a.id)

def __write_mass_and_node(pinfo, node, node_id, node_file, indent, do_mass = True):
	FMT = pinfo.get_double_formatter()
	mass = ''
	if pinfo.ndm == 2: # 2D
		# evaluate the mass option if we have masses on this node
		if do_mass and (node_id in pinfo.mass_to_node_map):
			mv6 = pinfo.mass_to_node_map[node_id] # get mass vector (6-components)
			if pinfo.ndf == 2: # U
				mass = ' -mass {} {}'.format(FMT(mv6[0]), FMT(mv6[1]))
			elif pinfo.ndf == 3: # U or UP or UR
				mass = ' -mass {} {} {}'.format(FMT(mv6[0]), FMT(mv6[1]), FMT(mv6[5]))
		# write node command
		node_file.write('{}{}node {} {} {}{}\n'.format(pinfo.indent, indent, node_id, FMT(node.x), FMT(node.y), mass))
	else: # 3D
		# evaluate the mass option if we have masses on this node
		if do_mass and (node_id in pinfo.mass_to_node_map):
			mv6 = pinfo.mass_to_node_map[node_id] # get mass vector (6-components)
			if pinfo.ndf == 3: # U
				mass = ' -mass {} {} {}'.format(FMT(mv6[0]), FMT(mv6[1]), FMT(mv6[2]))
			elif pinfo.ndf == 4: # UP
				mass = ' -mass {} {} {} 0.0'.format(FMT(mv6[0]), FMT(mv6[1]), FMT(mv6[2]))
			elif pinfo.ndf == 6: # UR
				mass = ' -mass {} {} {} {} {} {}'.format(FMT(mv6[0]), FMT(mv6[1]), FMT(mv6[2]),   FMT(mv6[3]), FMT(mv6[4]), FMT(mv6[5]))
		# write node command
		node_file.write('{}{}node {} {} {} {}{}\n'.format(pinfo.indent, indent, node_id, FMT(node.x), FMT(node.y), FMT(node.z), mass))
	pinfo.loaded_node_subset.add(node_id) # mark as written
	PyMpc.App.monitor().sendAutoIncrement()

def write_node (doc, pinfo, node_file):
	'''
	write node
	'''
	for k, v in pinfo.inv_map.items():
		pinfo.updateModelBuilder(k[0], k[1])
		if k[0] == 3:
			node_file.write('{}# tag x y z\n'.format(pinfo.indent))
		else:
			node_file.write('{}# tag x y\n'.format(pinfo.indent))
		for node_with_age in v:
			node_id = node_with_age.id
			if (pinfo.node_subset is not None) and (node_id not in pinfo.node_subset):
				continue # skip it in case of staged models if not in current stage
			node = doc.mesh.nodes[node_id]
			__write_mass_and_node(pinfo, node, node_id, node_file, pinfo.indent)

def write_node_partition (doc, pinfo, node_file):
	'''
	write node
	'''
	
	process_block_count = 0
	for process_id in range(len(doc.mesh.partitionData.partitions)):
		pinfo.setProcessId(process_id)
		first_done = False
		for k, v in pinfo.inv_map.items():
			is_model_builder_already_updated = False
			for node_with_age in v:
				node_id = node_with_age.id
				if not doc.mesh.partitionData.isNodeOnParition(node_id, process_id):
					continue # skip it, the node is not in this partition
				if (pinfo.node_subset is not None) and (node_id not in pinfo.node_subset):
					continue # skip it in case of staged models if not in current stage
				do_write_mass = (process_id == doc.mesh.partitionData.nodePartition(node_id))
				node = doc.mesh.nodes[node_id]
				if not first_done:
					if process_block_count == 0:
						node_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
					else:
						node_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
					if k[0] == 3:
						node_file.write('{}# tag x y z\n'.format(pinfo.indent))
					else:
						node_file.write('{}# tag x y\n'.format(pinfo.indent))
					first_done = True
				if not is_model_builder_already_updated:
					pinfo.updateModelBuilder(k[0], k[1])
					is_model_builder_already_updated = True
				__write_mass_and_node(pinfo, node, node_id, node_file, pinfo.tabIndent, do_mass = do_write_mass)
			if first_done:
				process_block_count += 1
		if process_block_count > 0 and first_done:
			node_file.write('{}{}'.format(pinfo.indent, '}'))
		# back to default
		pinfo.setProcessId(0) 

def __check_model (write_node_not_assigned_boolean, node_file, pinfo, comment = 0):
	if write_node_not_assigned_boolean:
		if comment == 0:
			print('Writing nodes belonging to geometries without element property assignment ...')
			node_file.write('\n')
			node_file.write('# nodes that belongs to geometries without element property assignment.\n'
							'# note that by default their model is set to ndm=3 - ndf=3.')
		# note: by default they are set to 3-3
		pinfo.updateModelBuilder(3, 3)

def __write_mass_and_node_not_assigned (pinfo, node_id, node, node_file, indent, do_mass = True):
	FMT = pinfo.get_double_formatter()
	mass = ''
	if do_mass and (node_id in pinfo.mass_to_node_map):
		mv6 = pinfo.mass_to_node_map[node_id] # get mass vector (6-components)
		mass = ' -mass {} {} {}'.format(FMT(mv6[0]), FMT(mv6[1]), FMT(mv6[2]))
	node_file.write('{}{}node {} {} {} {}{}\n'.format(pinfo.indent, indent, node_id, FMT(node.x), FMT(node.y), FMT(node.z), mass))
	pinfo.loaded_node_subset.add(node_id) # mark as written

def write_node_not_assigned (doc, pinfo, node_file):
	'''
	write node not assigned, at the end of the nodes assigned
	'''
	done_first = False
	write_node_not_assigned_boolean = True
	for node_id, node in doc.mesh.nodes.items():
		if not node_id in pinfo.node_to_model_map:
			if (pinfo.node_subset is not None) and (node_id not in pinfo.node_subset):
				continue # skip it in case of staged models if not in current stage
			__check_model (write_node_not_assigned_boolean, node_file, pinfo)
			write_node_not_assigned_boolean = False
			if not done_first:
				node_file.write('{}{} {} {} {} {}\n'.format(pinfo.indent, '#', 'tag', 'x', 'y', 'z'))
				done_first = True
			__write_mass_and_node_not_assigned(pinfo, node_id, node, node_file, pinfo.indent)

def write_node_not_assigned_partition (doc, pinfo, node_file):
	'''
	write node not assigned, at the end of the nodes assigned
	'''
	process_block_count = 0
	for process_id in range(len(doc.mesh.partitionData.partitions)):
		pinfo.setProcessId(process_id)
		first_done = False
		write_node_not_assigned_boolean = True
		for node_id, node in doc.mesh.nodes.items():
			if not node_id in pinfo.node_to_model_map:
				if not doc.mesh.partitionData.isNodeOnParition(node_id, process_id):
					continue # skip it, the node is not in this partition
				if (pinfo.node_subset is not None) and (node_id not in pinfo.node_subset):
					continue # skip it in case of staged models if not in current stage
				do_write_mass = (process_id == doc.mesh.partitionData.nodePartition(node_id))
				if not first_done:
					if process_block_count == 0:
						node_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
						node_file.write('{}{} {} {} {} {}\n'.format(pinfo.indent, '#', 'tag', 'x', 'y', 'z'))
						__check_model (write_node_not_assigned_boolean, node_file, pinfo, process_block_count)
					else:
						node_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
						node_file.write('{}{} {} {} {} {}\n'.format(pinfo.indent, '#', 'tag', 'x', 'y', 'z'))
						__check_model (write_node_not_assigned_boolean, node_file, pinfo, process_block_count)
					first_done = True
					write_node_not_assigned_boolean = False
				__write_mass_and_node_not_assigned(pinfo, node_id, node, node_file, pinfo.tabIndent, do_mass = do_write_mass)
			if first_done:
				process_block_count += 1
		if process_block_count > 0 and first_done:
			node_file.write('{}{}'.format(pinfo.indent, '}'))
		# back to default
		pinfo.setProcessId(0)
	# set them all to 3-3
	for node_id in doc.mesh.nodes:
		if not node_id in pinfo.node_to_model_map:
			pinfo.node_to_model_map[node_id] = (3, 3)