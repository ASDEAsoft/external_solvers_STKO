import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# auto
	at_auto = MpcAttributeMetaData()
	at_auto.type = MpcAttributeType.Boolean
	at_auto.name = 'auto'
	at_auto.group = 'Constraint'
	at_auto.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('auto')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidDiaphragm_command','RigidDiaphragm command')+'<br/>') +
		html_end()
		)
	at_auto.editable = False
	
	# user
	at_user = MpcAttributeMetaData()
	at_user.type = MpcAttributeType.Boolean
	at_user.name = 'user defined'
	at_user.group = 'Constraint'
	at_user.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('user defined')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidDiaphragm_command','RigidDiaphragm command')+'<br/>') +
		html_end()
		)
	at_user.editable = False
	
	# perpDirn
	at_perpDirn = MpcAttributeMetaData()
	at_perpDirn.type = MpcAttributeType.Integer
	at_perpDirn.name = 'perpDirn'
	at_perpDirn.group = 'Constraint'
	at_perpDirn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('perpDirn')+'<br/>') + 
		html_par('direction perpendicular to the rigid plane (i.e. direction 3 corresponds to the 1-2 plane)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidDiaphragm_command','RigidDiaphragm command')+'<br/>') +
		html_end()
		)
	at_perpDirn.sourceType = MpcAttributeSourceType.List
	at_perpDirn.setSourceList([1, 2, 3])
	at_perpDirn.setDefault(1)
	
	# ctype
	at_ctype = MpcAttributeMetaData()
	at_ctype.type = MpcAttributeType.Integer
	at_ctype.editable = False;
	at_ctype.name = 'ctype_constraint'
	at_ctype.group = 'Constraint'
	at_ctype.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ctype')+'<br/>') + 
		html_par('ctype') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidDiaphragm_command','RigidDiaphragm command')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'rigidDiaphragm'
	xom.addAttribute(at_perpDirn)
	xom.addAttribute(at_ctype)
	
	
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
			for node in elem.nodes:
				requested_node_dim_map[node.id] = (3, 6)
	
	return requested_node_dim_map

def __process_rigidDiaphram (doc, pinfo, perpDirn, is_partitioned, all_inter, process_id, process_block_count, indent):
	first_done = False
	for inter in all_inter:
		moi = doc.mesh.getMeshedInteraction(inter.id)
		for elem in moi.elements:
			
			# in parallel mode: skipe elements not in this process_id
			if is_partitioned:
				if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
					continue
			
			# check invalid elements
			if (len(elem.nodes) < 2 or elem.numberOfMasterNodes() != 1):
				raise Exception('wrong master-slave connectivity, expected: 1 master, N(>0) slaves, given: {} masters, {} slaves'.format(elem.numberOfMasterNodes(), elem.numberOfSlaveNodes()))
			
			# init string of slave nodes
			node_slave = ''
			
			# get master node
			mid = elem.nodes[0].id
			if (mid in pinfo.node_to_model_map):
				ndm_map = pinfo.node_to_model_map[mid][0]
				ndf_map = pinfo.node_to_model_map[mid][1]
				if (ndm_map != 3 or ndf_map != 6):
					raise Exception('Error: The rigidDiaphragm command works only for problems in 3 ndm and 6 ndf')
			
			# in parallel mode: check whether we have to open the if/elseif block (do it only before first element)
			# the choise of if or elseif comes from process_block_count
			if is_partitioned:
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
					first_done = True
			
			# compute string of slave nodes
			n=1 # variable to handle line length
			for i in range(1, len(elem.nodes)):
				inode_id = elem.nodes[i].id
				if (inode_id in pinfo.node_to_model_map):
					ndm_map = pinfo.node_to_model_map[inode_id][0]
					ndf_map = pinfo.node_to_model_map[inode_id][1]
					if (ndm_map != 3 or ndf_map != 6):
						raise Exception('Error: The rigidDiaphragm command works only for problems in 3 ndm and 6 ndf')
				
				if (i == (15*n)):
					node_slave += ' \\\n    {}'.format(inode_id)
					n += 1
				else:
					node_slave += ' {}'.format(inode_id)

			# now write the string into the file
			pinfo.updateModelBuilder(3, 6)
			str_tcl = '{}{}rigidDiaphragm {} {}{}\n'.format(pinfo.indent, indent, perpDirn, mid, node_slave)
			pinfo.out_file.write(str_tcl)
		
	if is_partitioned:
		if first_done: # if at least 1 element has been processed in this process_id...
			process_block_count += 1 # increment block count to see if we have to use if or elseif
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
	return process_block_count

def writeTcl_mpConstraints(pinfo):
	
	# rigidDiaphragm $perpDirn $masterNodeTag $slaveNodeTag1 $slaveNodeTag2 ...
	
	xobj = pinfo.condition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	perpDirn_at = xobj.getAttribute('perpDirn')
	if(perpDirn_at is None):
		raise Exception('Error: cannot find "perpDirn" attribute')
	perpDirn  = perpDirn_at.integer
	
	# pinfo.updateModelBuilder(3, 6)
	
	if pinfo.condition is None:
		raise Exception('Error: the current condition is None')
	
	all_inter = pinfo.condition.assignment.interactions
	if len(all_inter) == 0:
		return
	
	doc = App.caeDocument()
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			pinfo.setProcessId(process_id)
			process_block_count = __process_rigidDiaphram (doc, pinfo, perpDirn, is_partitioned, all_inter, process_id, process_block_count, pinfo.tabIndent)
	
	else:
		__process_rigidDiaphram (doc, pinfo, perpDirn, is_partitioned, all_inter, 0, 0, pinfo.indent)