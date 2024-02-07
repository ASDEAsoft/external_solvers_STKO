import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

class DofSet:

	def __init__(self):
		self.ndm = 0
		self.Ux = False
		self.Uy = False
		self.Uz = False
		self.Rx = False
		self.Ry = False
		self.Rz = False
		self.P = False
		
	def copyFrom(self, other, ndf):
		self.ndm = other.ndm
		self.Ux = other.Ux
		self.Uy = other.Uy
		if self.ndm == 2:
			if ndf == 3:
				self.Rz = other.Rz
				self.P = other.P
		elif self.ndm == 3:
			self.Uz = other.Uz
			if ndf == 4:
				self.P = other.P
			elif ndf == 6:
				self.Rx = other.Rx
				self.Ry = other.Ry
				self.Rz = other.Rz
		
	def switchOffInvalid(self, ndf):
		if self.ndm == 2:
			if ndf == 2:
				self.P = False
				self.Rz = False
		elif self.ndm == 3:
			if ndf == 3:
				self.Rx = False
				self.Ry = False
				self.Rz = False
				self.P = False
			elif ndf == 4:
				self.Rx = False
				self.Ry = False
				self.Rz = False
				
	def toIndexedString(self):
		if self.ndm == 2:
			aux = [self.Ux, self.Uy, (self.P or self.Rz)]
			return ' '.join( [ str(i+1) for i in range(len(aux)) if aux[i] ] )
		elif self.ndm == 3:
			if self.P:
				aux = [self.Ux, self.Uy, self.Uz, self.P]
				return ' '.join( [ str(i+1) for i in range(len(aux)) if aux[i] ] )
			else:
				aux = [self.Ux, self.Uy, self.Uz, self.Rx, self.Ry, self.Rz]
				return ' '.join( [ str(i+1) for i in range(len(aux)) if aux[i] ] )
			
def makeXObjectMetaData():
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Constraint'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	# ModelType
	at_ModelType = MpcAttributeMetaData()
	at_ModelType.type = MpcAttributeType.String
	at_ModelType.name = 'ModelType'
	at_ModelType.group = 'Constraint'
	at_ModelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ModelType')+'<br/>') + 
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	at_ModelType.sourceType = MpcAttributeSourceType.List
	at_ModelType.setSourceList(['U (Displacement)', 'U-P (Displacement+Pressure)', 'U-R (Displacement+Rotation)'])
	at_ModelType.setDefault('U (Displacement)')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Constraint'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') + 
		html_par('Dx Constraint') +
		html_end()
		)
	at_2D.editable = False
	
	# 3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Constraint'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') + 
		html_par('Dx Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# D
	at_D = MpcAttributeMetaData()
	at_D.type = MpcAttributeType.Boolean
	at_D.name = 'U (Displacement)'
	at_D.group = 'Constraint'
	at_D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U (Displacement)')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	at_D.editable = False
	
	# UP
	at_UP = MpcAttributeMetaData()
	at_UP.type = MpcAttributeType.Boolean
	at_UP.name = 'U-P (Displacement+Pressure)'
	at_UP.group = 'Constraint'
	at_UP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U-P (Displacement+Pressure)')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	at_UP.editable = False
	
	# Beam
	at_Beam = MpcAttributeMetaData()
	at_Beam.type = MpcAttributeType.Boolean
	at_Beam.name = 'U-R (Displacement+Rotation)'
	at_Beam.group = 'Constraint'
	at_Beam.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U-R (Displacement+Rotation)')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	at_Beam.editable = False
	
	# Ux
	at_Ux = MpcAttributeMetaData()
	at_Ux.type = MpcAttributeType.Boolean
	at_Ux.name = 'Ux'
	at_Ux.group = 'dof'
	at_Ux.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ux')+'<br/>') + 
		html_par('Ux Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	# Uy
	at_Uy = MpcAttributeMetaData()
	at_Uy.type = MpcAttributeType.Boolean
	at_Uy.name = 'Uy'
	at_Uy.group = 'dof'
	at_Uy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uy')+'<br/>') + 
		html_par('Uy Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	# Uz
	at_Uz = MpcAttributeMetaData()
	at_Uz.type = MpcAttributeType.Boolean
	at_Uz.name = 'Uz'
	at_Uz.group = 'dof'
	at_Uz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uz')+'<br/>') + 
		html_par('Uz Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	# Rx
	at_Rx = MpcAttributeMetaData()
	at_Rx.type = MpcAttributeType.Boolean
	at_Rx.name = 'Rx'
	at_Rx.group = 'dof'
	at_Rx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rx')+'<br/>') + 
		html_par('Rx Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	# Ry
	at_Ry = MpcAttributeMetaData()
	at_Ry.type = MpcAttributeType.Boolean
	at_Ry.name = 'Ry'
	at_Ry.group = 'dof'
	at_Ry.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ry')+'<br/>') + 
		html_par('Ry Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	# Rz_2D
	at_Rz_2D = MpcAttributeMetaData()
	at_Rz_2D.type = MpcAttributeType.Boolean
	at_Rz_2D.name = 'Rz/2D'
	at_Rz_2D.group = 'dof'
	at_Rz_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rz')+'<br/>') + 
		html_par('Rz Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	# Rz_3D
	at_Rz_3D = MpcAttributeMetaData()
	at_Rz_3D.type = MpcAttributeType.Boolean
	at_Rz_3D.name = 'Rz/3D'
	at_Rz_3D.group = 'dof'
	at_Rz_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rz')+'<br/>') + 
		html_par('Rz Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	# P_2D
	at_P_2D = MpcAttributeMetaData()
	at_P_2D.type = MpcAttributeType.Boolean
	at_P_2D.name = 'P/2D'
	at_P_2D.group = 'dof'
	at_P_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('P')+'<br/>') + 
		html_par('P Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	# P_3D
	at_P_3D = MpcAttributeMetaData()
	at_P_3D.type = MpcAttributeType.Boolean
	at_P_3D.name = 'P/3D'
	at_P_3D.group = 'dof'
	at_P_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('P')+'<br/>') + 
		html_par('P Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	# ctype
	at_ctype = MpcAttributeMetaData()
	at_ctype.type = MpcAttributeType.Integer
	at_ctype.visible = False;
	at_ctype.editable = False;
	at_ctype.name = 'ctype_constraint'
	at_ctype.group = 'Constraint'
	at_ctype.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ctype')+'<br/>') + 
		html_par('ctype') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EqualDOF_command','EqualDOF command')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'equalDOF'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_ModelType)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_D)
	xom.addAttribute(at_UP)
	xom.addAttribute(at_Beam)
	xom.addAttribute(at_Ux)
	xom.addAttribute(at_Uy)
	xom.addAttribute(at_Uz)
	xom.addAttribute(at_Rx)
	xom.addAttribute(at_Ry)
	xom.addAttribute(at_Rz_2D)
	xom.addAttribute(at_Rz_3D)
	xom.addAttribute(at_P_2D)
	xom.addAttribute(at_P_3D)
	xom.addAttribute(at_ctype)
	
	
	# visibility dependencies
	
	#2D
	# P_2D-dep
	xom.setVisibilityDependency(at_2D, at_P_2D)
	xom.setVisibilityDependency(at_UP, at_P_2D)
	
	# Rz_2D-dep
	xom.setVisibilityDependency(at_2D, at_Rz_2D)
	xom.setVisibilityDependency(at_Beam, at_Rz_2D)
	
	#3D
	# uz-dep
	xom.setVisibilityDependency(at_3D, at_Uz)
	
	# P_3D-dep
	xom.setVisibilityDependency(at_3D, at_P_3D)
	xom.setVisibilityDependency(at_UP, at_P_3D)
	
	# Rx-dep
	xom.setVisibilityDependency(at_3D, at_Rx)
	xom.setVisibilityDependency(at_Beam, at_Rx)
	
	# Ry-dep
	xom.setVisibilityDependency(at_3D, at_Ry)
	xom.setVisibilityDependency(at_Beam, at_Ry)
	
	# Rz-dep
	xom.setVisibilityDependency(at_3D, at_Rz_3D)
	xom.setVisibilityDependency(at_Beam, at_Rz_3D)
	
	
	# auto-exclusive dependencies
	
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	# 2D or 2D UP or 2D Beam or 3D or 3D UP or 3D Beam
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_D)
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_UP)
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_Beam)
	
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
	
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	Dimension2 = Dimension2_at.boolean
	
	UP_at = xobj.getAttribute('U-P (Displacement+Pressure)')
	if(UP_at is None):
		raise Exception('Error: cannot find "U-P (Displacement+Pressure)" attribute')
	UP = UP_at.boolean
	
	UR_at = xobj.getAttribute('U-R (Displacement+Rotation)')
	if(UR_at is None):
		raise Exception('Error: cannot find "U-R (Displacement+Rotation)" attribute')
	UR = UR_at.boolean
	
	if Dimension2:
		ndm = 2
		if UP or UR:
			ndf = [3, 2] # user-defined goes first
		else:
			ndf = [2, 3] # standard
		
	else:
		ndm = 3
		if UP:
			ndf = [4, 3, 6] # user-defined goes first
		elif UR:
			ndf = [6, 3, 4] # user-defined goes first
		else:
			ndf = [3, 4, 6] # standard
	
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
			requested_node_dim_map[mid] = (ndm, ndf)
	
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
				if doc.mesh.partitionData.isNodeOnParition(slave_id, process_id):
					if not process_id in master_parts:
						master_parts.append(process_id)

def __process_equalDOF (doc, pinfo, is_partitioned, all_inter, process_id, process_block_count, ds, dsc):
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
				if not doc.mesh.partitionData.isNodeOnParition(slave_id, process_id):
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
					raise Exception('Error: master and slave nodes must have the same NDM. master NDM = {}, slave NDM = {}'.format(ndm_master, ndm_slave))
				if (ds.ndm != ndm_master):
					raise Exception('Error: condition and master/slave nodes must have the same NDM. master/slave NDM = {}, condition NDM = {}'.format(ndm_master, ds.ndm))
				
				# take minimum ndf for intersection
				ndf_min = min(ndf_master, ndf_slave)
				# copy dofset from user-defined condition
				dsc.copyFrom(ds, ndf_min)
				dsc.switchOffInvalid(ndf_min)
				
				# now write the string into the file
				edof_opt = dsc.toIndexedString()
				if len(edof_opt) > 0:
					pinfo.out_file.write('{}equalDOF {} {}   {}\n'.format(pinfo.indent, master_id, slave_id, edof_opt))
				
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
	
	# get data
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	Dimension2 = geta('2D').boolean
	UP = geta('U-P (Displacement+Pressure)').boolean
	UR = geta('U-R (Displacement+Rotation)').boolean
	
	ds = DofSet()
	ds.Ux = geta('Ux').boolean
	ds.Uy = geta('Uy').boolean
	ds.Uz = geta('Uz').boolean
	ds.Rx = geta('Rx').boolean
	ds.Ry = geta('Ry').boolean
	if Dimension2:
		ds.ndm = 2
		ds.Rz = geta('Rz/2D').boolean
		ds.P = geta('P/2D').boolean
	else:
		ds.ndm = 3
		ds.Rz = geta('Rz/3D').boolean
		ds.P = geta('P/3D').boolean
	
	dsc = DofSet() # a pre-allocated variable to hold the modified copy os ds (optimization)
	
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
			process_block_count = __process_equalDOF (doc, pinfo, is_partitioned, all_inter, process_id, process_block_count, ds, dsc)
	else :
		__process_equalDOF (doc, pinfo, is_partitioned, all_inter, 0, 0, ds, dsc)