import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.String
	at_type.name = 'type'
	at_type.group = 'Group'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') + 
		html_par('string-based argument for rigid-link type:') +
		html_par('beam both the translational and rotational degrees of freedom are constrained.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidLink_command','RigidLink command')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList(['beam'])
	at_type.setDefault('beam')
	at_type.editable = False
	
	xom = MpcXObjectMetaData()
	xom.name = 'beamSolidCoupling'
	xom.addAttribute(at_type)
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

def __beamSolidCoupling (doc, all_inter, pinfo, type, is_partitioned, process_id, process_block_count, indent):
	first_done =False
	FMT = pinfo.get_double_formatter()
	str_tcl = ('{}{}{}{}{}{}{}{}{}{}{}'.format('\n', indent, '# beamSolidCoupling\n', indent, '#	node tag x y z\n', indent, 
				'#	equalDOF node_i node_j 1 2 3\n',indent, '#	rigidLink ', type, ' node_i node_j\n\n'))
	for inter in all_inter:
		node_slave = ''
		moi = doc.mesh.getMeshedInteraction(inter.id)
		for elem in moi.elements:
			if (len(elem.nodes) < 2 or elem.numberOfMasterNodes() != 1):
				raise Exception('wrong master-slave connectivity, expected: 1 master, N(>0) slaves, given: {} masters, {} slaves'.format(elem.numberOfMasterNodes(), elem.numberOfSlaveNodes()))
			
			mid = elem.nodes[0].id
			if (mid in pinfo.node_to_model_map):
				ndm_map = pinfo.node_to_model_map[mid][0]
				ndf_map = pinfo.node_to_model_map[mid][1]
				if (ndm_map != 3 or ndf_map != 6):
					raise Exception('Error: The beamSolidCoupling command works only for problems in 3 ndm and 6 ndf for master node')
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
						raise Exception('Error: The beamSolidCoupling command works only for problems in 3 ndm and 3 or 4 ndf for slave nodes')
			if not is_partitioned:
				pinfo.out_file.write(str_tcl)
			else:
				if first_done:
					pinfo.out_file.write(str_tcl)
				
			for i in range(1, len(elem.nodes)):
				# if is_partitioned:
				pinfo.updateModelBuilder(3, 6)
				
				node_extra = pinfo.next_node_id
				
				node_N1 = doc.mesh.nodes[elem.nodes[i].id]
				coordinateN1 = ' {} {} {}'.format(FMT(node_N1.x), FMT(node_N1.y), FMT(node_N1.z))
				pinfo.out_file.write('{}{}node {}{}\n'.format(pinfo.indent, indent, node_extra, coordinateN1))
				pinfo.out_file.write('{}{}equalDOF {} {} {}\n'.format(pinfo.indent, indent, node_extra, elem.nodes[i].id, '1 2 3'))
				pinfo.out_file.write('{}{}rigidLink {} {} {}\n'.format(pinfo.indent, indent, type, mid, node_extra))
				pinfo.next_node_id += 1
	if is_partitioned:
		if first_done:
			process_block_count += 1
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count

def writeTcl_mpConstraints(pinfo):
	
	# node tag x y z													node generate coordinate == coordinate node original
	# equalDOF node_master node_slave 1 2 3								node_master = node generate		node_slave = node original
	# rigidLink type node_master node_slave								node_master = node beam			node_slave = node generate
	
	# getSpatialDim
	# pinfo.updateModelBuilder(3, 6)
	xobj = pinfo.condition.XObject
	tag = pinfo.next_elem_id
	
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	all_inter = pinfo.condition.assignment.interactions
	if len(all_inter) == 0:
		return
	
	type_at = xobj.getAttribute('type')
	if(type_at is None):
		raise Exception('Error: cannot find "type" attribute')
	type = type_at.string
	
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			pinfo.setProcessId(process_id)
			process_block_count = __beamSolidCoupling (doc, all_inter, pinfo, type, is_partitioned, process_id, process_block_count, pinfo.tabIndent)
	else:
		__beamSolidCoupling (doc, all_inter, pinfo, type, is_partitioned, 0, 0, pinfo.indent)