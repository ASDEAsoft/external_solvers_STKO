import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Dimension
	type = MpcAttributeMetaData()
	type.type = MpcAttributeType.String
	type.name = 'Type'
	type.group = 'Default'
	type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	type.sourceType = MpcAttributeSourceType.List
	type.setSourceList(['Interface to Fluid', 'Interface to Solid'])
	type.setDefault('Interface to Fluid')
	
	xom = MpcXObjectMetaData()
	xom.name = 'FSICoupling2D'
	xom.addAttribute(type)
	
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
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = True
	
	return d

def getRequestedNodalSpatialDim(xobj):
	'''
	similar to the def getNodalSpatialDim(xobj, xobj_phys_prop) method in element properties,
	but with a conceptual difference. getNodalSpatialDim returns a list of (ndm,ndf) pair
	whose length is equal to the number of nodes for that element, following the local
	numbering of each element.
	Here instead we return a map, where the key is the ID of the (only) nodes where
	the condition requires a specific dimension (here for example the master node)
	
	Update 6/2/2020:
	We want to allow:
	1) master and slave to have different dofs
	2) the master node can have a different dofset than the one of the condition
		- we give here more than one dofset
		- the first one is the one in this conditon because, if the node is floating,
		it will take the first one
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
			requested_node_dim_map[mid] = (2, 3)
	return requested_node_dim_map

def ensureNodesOnPartitions(xobj, pmap):
	# make sure a master node is on every partition a slave node is
	doc = App.caeDocument()
	if doc is None: return
	if doc.mesh is None: return
	process_count = len(doc.mesh.partitionData.partitions)
	if process_count <= 1: return
	all_inter = xobj.parent.assignment.interactions
	for inter in all_inter:
		moi = doc.mesh.getMeshedInteraction(inter.id)
		for elem in moi.elements:
			if (elem.numberOfMasterNodes() != 1 or elem.numberOfSlaveNodes() != 1):
				continue # will raise and error later on
			master_id = elem.nodes[0].id
			slave_id = elem.nodes[1].id
			master_parts = pmap.get(master_id, None)
			if master_parts is None:
				master_parts = []
				pmap[master_id] = master_parts
			for process_id in range(process_count):
				if doc.mesh.partitionData.isNodeOnPartition(slave_id, process_id):
					if not process_id in master_parts:
						master_parts.append(process_id)

def __process_coupling (doc, pinfo, is_partitioned, all_inter, process_id, process_block_count, type):
	first_done = False
	for inter in all_inter:
		moi = doc.mesh.getMeshedInteraction(inter.id)
		for elem in moi.elements:
			if (elem.numberOfMasterNodes() != 1 or elem.numberOfSlaveNodes() != 1):
				raise Exception('wrong master-slave connectivity, expected: 1 master, 1 slave, given: {} masters, {} slaves'.format(elem.numberOfMasterNodes(), elem.numberOfSlaveNodes()))
			
			master_id = elem.nodes[0].id
			slave_id = elem.nodes[1].id
			
			if is_partitioned:
				# if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
					# continue
				# The above does not work good with transformation method. the MP constraint should be in every partition
				# the slave node belongs to. Note that we are sure that also the master node will be in that partition since
				# they belong to a link element in stko mesh.
				if not doc.mesh.partitionData.isNodeOnPartition(slave_id, process_id):
					continue
				
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
					first_done = True
			
			if (master_id in pinfo.node_to_model_map) and (slave_id in pinfo.node_to_model_map):
				
				(ndm_master, ndf_master) = pinfo.node_to_model_map[master_id]
				(ndm_slave, ndf_slave) = pinfo.node_to_model_map[slave_id]
				if (ndm_master != ndm_slave):
					raise Exception('Error in FSICoupling: master and slave nodes must have the same NDM. master NDM = {}, slave NDM = {}'.format(ndm_master, ndm_slave))
				if type == 'Interface to Fluid':
					if ndf_slave != 1:
						raise Exception('Error in FSICoupling: slave node must have 1 DOF')
					pinfo.out_file.write('{}equalDOF_Mixed {} {}   1   3 1\n'.format(pinfo.indent, master_id, slave_id))
				elif type == 'Interface to Solid':
					if ndf_slave < 2:
						raise Exception('Error in FSICoupling: slave node must have at least 2 DOFs')
					pinfo.out_file.write('{}equalDOF {} {}  1 2\n'.format(pinfo.indent, master_id, slave_id))
				
			else :
				raise Exception('Error: node not in domain {} {}'.format((master_id in pinfo.node_to_model_map), (slave_id in pinfo.node_to_model_map)))
			
	if is_partitioned:
		if first_done:
			process_block_count += 1
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count

def writeTcl_mpConstraints(pinfo):
	
	# check
	if pinfo.condition is None:
		raise Exception('the current condition is None')
	
	# xobject
	xobj = pinfo.condition.XObject
	tag = xobj.parent.componentId
	
	# description
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# type
	type = xobj.getAttribute('Type').string
	
	# get all interactions
	all_inter = pinfo.condition.assignment.interactions
	if len(all_inter) == 0:
		return
	
	# document
	doc = App.caeDocument()
	
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			pinfo.setProcessId(process_id)
			process_block_count = __process_coupling(doc, pinfo, is_partitioned, all_inter, process_id, process_block_count, type)
	else :
		__process_coupling(doc, pinfo, is_partitioned, all_inter, 0, 0, type)