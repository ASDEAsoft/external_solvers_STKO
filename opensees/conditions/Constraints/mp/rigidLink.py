import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# Dimension
	at_dimension = MpcAttributeMetaData()
	at_dimension.type = MpcAttributeType.String
	at_dimension.name = 'Dimension'
	at_dimension.group = 'Group'
	at_dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidLink_command','RigidLink command')+'<br/>') +
		html_end()
		)
	at_dimension.sourceType = MpcAttributeSourceType.List
	at_dimension.setSourceList(['2D', '3D'])
	at_dimension.setDefault('2D')
	
	# type
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.String
	at_type.name = 'type'
	at_type.group = 'Group'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') + 
		html_par('string-based argument for rigid-link type:') +
		html_par('bar only the translational degree-of-freedom will be constrained to be exactly the same as those at the master node') +
		html_par('beam both the translational and rotational degrees of freedom are constrained.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidLink_command','RigidLink command')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList(['bar', 'beam'])
	at_type.setDefault('bar')
	
	# Bar
	at_bar = MpcAttributeMetaData()
	at_bar.type = MpcAttributeType.Boolean
	at_bar.name = 'bar'
	at_bar.group = 'Constraint'
	at_bar.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bar')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidLink_command','RigidLink command')+'<br/>') +
		html_end()
		)
	at_bar.editable = False
	
	# ModelType
	at_ModelType = MpcAttributeMetaData()
	at_ModelType.type = MpcAttributeType.String
	at_ModelType.name = 'ModelType'
	at_ModelType.group = 'Group'
	at_ModelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ModelType')+'<br/>') + 
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidLink_command','RigidLink command')+'<br/>') +
		html_end()
		)
	at_ModelType.sourceType = MpcAttributeSourceType.List
	at_ModelType.setSourceList(['U (Displacement)', 'U-R (Displacement+Rotation)'])
	at_ModelType.setDefault('U (Displacement)')
	
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidLink_command','RigidLink command')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'rigidLink'
	xom.addAttribute(at_dimension)
	xom.addAttribute(at_type)
	xom.addAttribute(at_ctype)
	xom.addAttribute(at_bar)
	xom.addAttribute(at_ModelType)
	
	# visibility dependencies
	
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_type, at_bar)
	
	# bar
	xom.setVisibilityDependency(at_bar, at_ModelType)
	
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
	
	type_at = xobj.getAttribute('type')
	if(type_at is None):
		raise Exception('Error: cannot find "type" attribute')
	type = type_at.string
	
	dimension_at = xobj.getAttribute('Dimension')
	if(dimension_at is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	dimension = dimension_at.string
	
	modeltype_at = xobj.getAttribute('ModelType')
	if (modeltype_at is None):
		raise Exception('Error: cannot find "ModelType" attribute')
	modeltype = modeltype_at.string
	
	if(dimension == '2D'):
		ndm = 2
		if (type == 'bar'):
			if (modeltype == 'U (Displacement)'):
				ndf = 2
			elif (modeltype == 'U-R (Displacement+Rotation)'):
				ndf = 3
			else:
				ndf = [2,3]
		else:
			ndf = 3
	else:
		ndm = 3
		if (type == 'bar'):
			if (modeltype == 'U (Displacement)'):
				ndf = 3
			elif (modeltype == 'U-R (Displacement+Rotation)'):
				ndf = 6
			else:
				ndf = [3,6]
		else:
			ndf = 6
	
	for inter in all_inter:
		moi = doc.mesh.getMeshedInteraction(inter.id)
		for elem in moi.elements:
			for node in elem.nodes:
				requested_node_dim_map[node.id] = (ndm, ndf)
	
	return requested_node_dim_map

def __process_rigidLink (doc, pinfo, is_partitioned, all_inter, process_id, process_block_count, type, indent):
	first_done = False
	for inter in all_inter:
		if (inter.type == MpcInteractionType.NodeToElement):
			raise Exception('Error: type of interactions must be "NodeToNode" or "GeneralLink" and not "{}"'.format(inter.type))
		moi = doc.mesh.getMeshedInteraction(inter.id)
		for elem in moi.elements:
			if (elem.numberOfMasterNodes() != 1 or elem.numberOfSlaveNodes() == 0):
				raise Exception('wrong master-slave connectivity, expected: 1 master, N>0 slaves, given: {} masters, {} slaves'.format(elem.numberOfMasterNodes(), elem.numberOfSlaveNodes()))
			
			if is_partitioned:
				if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
					continue
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
					first_done = True
			
			master_id = elem.nodes[0].id
			if not master_id in pinfo.node_to_model_map:
				raise Exception('Error: master node without assigned element')		#nodo senza elemento assegnato
			ndm_master_map = pinfo.node_to_model_map[master_id][0]
			ndf_master_map = pinfo.node_to_model_map[master_id][1]
			if (pinfo.ndm != ndm_master_map) or (pinfo.ndf != ndf_master_map):
				raise Exception('Error: different ndm/ndf in master node')		# ndm ed ndf applicati all'elemento devono essere uguali a quelli della mappa
					
			for slave_counter in range(1, len(elem.nodes)):
				slave_id = elem.nodes[slave_counter].id
				if not slave_id in pinfo.node_to_model_map:
					raise Exception('Error: node without assigned element')		#nodo senza elemento assegnato
				ndm_slave_map = pinfo.node_to_model_map[master_id][0]
				ndf_slave_map = pinfo.node_to_model_map[master_id][1]
				if (ndm_master_map != ndm_slave_map) or (ndf_master_map != ndf_slave_map):
					raise Exception('Error: different ndm/ndf between master and node slave')
				if (pinfo.ndm != ndm_slave_map) or (pinfo.ndf != ndf_slave_map):
					raise Exception('Error: diffrent ndm/ndf in slave node')		# ndm ed ndf applicati all'elemento devono essere uguali a quelli della mappa
				
				pinfo.out_file.write('{}{}rigidLink {} {} {}\n'.format(pinfo.indent, indent, type, master_id, slave_id))
				
	if is_partitioned:
		if first_done:
			process_block_count += 1
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count

def writeTcl_mpConstraints(pinfo):
	
	# rigidLink $type $masterNodeTag $slaveNodeTag
	
	xobj = pinfo.condition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	type_at = xobj.getAttribute('type')
	if(type_at is None):
		raise Exception('Error: cannot find "type" attribute')
	type = type_at.string
	
	modeltype_at = xobj.getAttribute('ModelType')
	if (modeltype_at is None):
		raise Exception('Error: cannot find "ModelType" attribute')
	modeltype = modeltype_at.string
	
	dimension_at = xobj.getAttribute('Dimension')
	if(dimension_at is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	dimension = dimension_at.string
	
	if(dimension == '2D'):
		ndm = 2
		if (type == 'bar'):
			if (modeltype == 'U (Displacement)'):
				ndf = 2
			elif (modeltype == 'U-R (Displacement+Rotation)'):
				ndf = 3
		else:
			ndf = 3
	else:
		ndm = 3
		if (type == 'bar'):
			if (modeltype == 'U (Displacement)'):
				ndf = 3
			elif (modeltype == 'U-R (Displacement+Rotation)'):
				ndf = 6
		else:
			ndf = 6
	
	pinfo.updateModelBuilder(ndm, ndf)
	
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
			process_block_count = __process_rigidLink (doc, pinfo, is_partitioned, all_inter, process_id, process_block_count, type, pinfo.tabIndent)
	
	else:
		__process_rigidLink (doc, pinfo, is_partitioned, all_inter, 0, 0, type, pinfo.indent)