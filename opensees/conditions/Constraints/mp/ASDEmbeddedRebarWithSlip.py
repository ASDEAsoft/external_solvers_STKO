import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.utils.tcl_input as tclin
import math
from opensees.conditions.Constraints.mp.ASDEmbeddedNodeElementUtils import ASDEmbeddedNodeElementUtils as ebu
import os

def _err(id, msg):
	return 'Error in "ASDEmbeddedRebarWithSlip" at "Condition {}":\n{}'.format(id, msg)
def _geta(xobj, name):
	a = xobj.getAttribute(name)
	if a is None:
		raise Exception(_err(xobj.parent.componentId, 'cannot find "{}" attribute'.format(name)))
	return a

def makeXObjectMetaData():
	
	dp = 'https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/ASDEmbeddedNodeElement.html'
	
	# stiffness
	K = MpcAttributeMetaData()
	K.type = MpcAttributeType.QuantityScalar
	K.name = 'K (Penalty)'
	K.group = 'Default'
	K.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K (Penalty)')+'<br/>') + 
		html_par(
			"A penalty stiffness value used to enforce the constraint.<br/>"
			"This value should be large enough to enforce the constraint, but not too large, otherwise the system may become ill-conditioned.<br/>"
			"It is possible to estimate this value to be approximately 3 or 4 orders of magnitude greater than the Young's modulus of the embedding material.<br/>"
			"Also note that this value will be automatically scaled by the volume of the embedding element, so it should be independent from the element size."
			) +
		html_par(html_href(dp,'ASDEmbeddedRebarWithSlip')+'<br/>') +
		html_end()
		)
	K.dimension = u.F/u.L/u.L
	K.setDefault(1.0e12)
	
	# ignore outside
	son = MpcAttributeMetaData()
	son.type = MpcAttributeType.Boolean
	son.name = 'Ignore Nodes Outside'
	son.group = 'Default'
	son.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-rot')+'<br/>') + 
		html_par(
			"If True, all the nodes that are outside of the embedding domain will be skipped without generating any error.<br/>"
			"If, instead, you want to make sure that all nodes are properly constrained, you can turn this flag Off.<br/>"
			"In this case, when a node is outside the embedding domain of more than 1 % of the embedding domain size, and error will be generated."
			) +
		html_par(html_href(dp,'ASDEmbeddedRebarWithSlip')+'<br/>') +
		html_end()
		)
	son.setDefault(True)
	
	mat = MpcAttributeMetaData()
	mat.type = MpcAttributeType.Index
	mat.name = 'Bar-Slip Material'
	mat.group = 'Default'
	mat.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Bar-Slip Material')+'<br/>') + 
		html_par(
			"A previously defined uniaxial material to represent the bar-slip behavior.<br/>"
			"It should be given as a Stress-Displacement law."
			) +
		html_par(html_href(dp,'ASDEmbeddedRebarWithSlip')+'<br/>') +
		html_end()
		)
	mat.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	mat.indexSource.addAllowedNamespace("materials.uniaxial")
	
	dia = MpcAttributeMetaData()
	dia.type = MpcAttributeType.QuantityScalar
	dia.name = 'Rebar Diameter'
	dia.group = 'Default'
	dia.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rebar Diameter')+'<br/>') + 
		html_par(
			"The diameter of the rebar."
			) +
		html_par(html_href(dp,'ASDEmbeddedRebarWithSlip')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDEmbeddedRebarWithSlip'
	xom.addAttribute(K)
	xom.addAttribute(son)
	xom.addAttribute(mat)
	xom.addAttribute(dia)
	
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

def writeTcl_mpConstraints(pinfo):
	'''
	This is a combination of:
	- extra node N2
	- zero-length aligned with the beam axis, all DOFs but the axial one are stiff
	- axial dof = material
	- extra node N2 linked to master element with ASDEmbeddedNodeElement
	'''
	# element ASDEmbeddedNodeElement $Tag  $Cnode   $Rnode1 $Rnode2 $Rnode3 <$Rnode4>   <-K $K> <-rot> <-p> <-KP $KP>
	
	# Utility functions ====================================================================================
	
	import numpy as np
	
	# the XObject
	xobj = pinfo.condition.XObject
	
	# the document
	doc = App.caeDocument()
	if(doc is None):
		raise Exception(_err(pinfo.condition.id, 'null cae document'))
	
	# get all interactions with this condition
	all_inter = pinfo.condition.assignment.interactions
	if len(all_inter) == 0:
		return
	
	# check partition
	is_partitioned = (pinfo.process_count > 1)
	
	# get XObject's arguments
	K = _geta(xobj, 'K (Penalty)').quantityScalar.value
	rot = '-rot'
	ignore_outside = _geta(xobj, 'Ignore Nodes Outside').boolean
	slip_tag = _geta(xobj, 'Bar-Slip Material').index
	dia = _geta(xobj, 'Rebar Diameter').quantityScalar.value
	
	# some stats
	stats = [0, 0]
	
	# prepare vectors for slave nodes
	# make a dict(slave_node_id, [Vx, Vy, L])
	interaction_slave_node_map = {}
	for inter in all_inter:
		slave_node_map = {}
		interaction_slave_node_map[inter.id] = slave_node_map
		for slave_item in inter.items.slaves:
			# make sure the slave geometry is an edge
			if slave_item.subshapeType != MpcSubshapeType.Edge:
				raise Exception(_err(pinfo.condition.id, 
					'Slave geometries in Interaction "{}" [{}] should be only edges.\nFound Invalid slave: Geometry: {} - Subshape: {} {}'.format(
						inter.name, inter.id, inter.type, slave_item.geometry.id, slave_item.subshapeId, slave_item.subshapeType)
						))
			# get meshed geometry and domain
			mog = doc.mesh.getMeshedGeometry(slave_item.geometry.id)
			domain = mog.edges[slave_item.subshapeId]
			for elem in domain.elements:
				orientation = elem.orientation.computeOrientation()
				Vx = Math.vec3(orientation[0,0], orientation[1,0], orientation[2,0])
				lump_factors = elem.computeLumpingFactors()
				for node, length in zip(elem.nodes, lump_factors):
					slave_data = slave_node_map.get(node.id, None)
					if slave_data is None:
						slave_data = [Math.vec3(0.0,0.0,0.0), Math.vec3(0.0,0.0,0.0), 0.0]
						slave_node_map[node.id] = slave_data
					slave_data[0] += Vx
					slave_data[2] += length
		# normalize tangent vectors and compute Vy vectors
		for slave_id, slave_data in slave_node_map.items():
			Vx = slave_data[0]
			Vx.normalize()
			if abs(Vx[2]) > 0.99:
				temp = Math.vec3(1.0, 0.0, 0.0)
			else:
				temp = Math.vec3(0.0, 0.0, 1.0)
			slave_data[1] = temp.cross(Vx).normalized()
	# print some checks
	#for inter_id, slave_node_map in interaction_slave_node_map.items():
	#	cumlen = 0.0
	#	for slave_id, slave_data in slave_node_map.items():
	#		Vx = slave_data[0]
	#		Vy = slave_data[1]
	#		L = slave_data[2]
	#		cumlen += L
	#		print(' %d : | %.3e, %.3e, %.3e | %.3e, %.3e, %.3e | %.3e' % (slave_id, Vx.x, Vx.y, Vx.z, Vy.x, Vy.y, Vy.z, L ))
	#	print(cumlen)
	
	# formatter
	FMT = pinfo.get_double_formatter()
	
	# get tags
	def next_node_id():
		i = pinfo.next_node_id
		pinfo.next_node_id += 1
		return i
	def next_elem_id():
		i = pinfo.next_elem_id
		pinfo.next_elem_id += 1
		return i
	def next_prop_id():
		i = pinfo.next_physicalProperties_id
		pinfo.next_physicalProperties_id += 1
		return i
	
	# internal function to process all interactions
	def internal(process_id, process_block_count):
		# first-done flag for partitioned process
		first_done = False
		# process each interaction
		for inter in all_inter:
			CUMA = 0.0
			# get info about master geometry and do some checks
			if inter.type != MpcInteractionType.NodeToElement:
				raise Exception(_err(pinfo.condition.id, 
					'Interaction "{}" [{}] should be a Node-to-Element interaction, not {}.'.format(
						inter.name, inter.id, inter.type)
						))
			# get slave node data
			slave_node_map = interaction_slave_node_map[inter.id]
			# process all link elements
			moi = doc.mesh.getMeshedInteraction(inter.id)
			for elem in moi.elements:
				# skip elements not on this partition
				if is_partitioned:
					if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
						continue
				# number of retained nodes and constrained nodes
				NN = len(elem.nodes)
				NM = elem.numberOfMasterNodes()
				NS = NN - NM
				if NS != 1:
					raise Exception(_err(pinfo.condition.id, 'Link element should have only 1 constrained node'))
				# the constrained node
				Cnode = elem.nodes[-1]
				Cpos = np.asarray([[Cnode.x],[Cnode.y], [Cnode.z]])
				# get source element
				source_elem = elem.sourceElement
				if source_elem is None:
					raise Exception(_err(pinfo.condition.id, 'Link element should have a valid source element'))
				# check source element and extract embedding sub-simplex (3-node triangle or 4-node tetrahedron)
				retained_nodes = []
				distance = 1.0e10
				family = source_elem.geometryFamilyType()
				if family == MpcElementGeometryFamilyType.Triangle:
					# for any triangle, the first 3 nodes are the corner ones
					retained_nodes = [source_elem.nodes[i] for i in range(3)]
					_, distance = ebu.lct3(retained_nodes, Cpos)
				elif family == MpcElementGeometryFamilyType.Tetrahedron:
					# for any tetrahedron, the first 4 nodes are the corner ones
					retained_nodes = [source_elem.nodes[i] for i in range(4)]
					_, distance = ebu.lct4(retained_nodes, Cpos)
				elif family == MpcElementGeometryFamilyType.Quadrilateral:
					# for any quadrilateral, the first 4 nodes are the corner ones.
					# we need to find the closest sub-simplex
					aux = []
					for sub in ebu.QSubs:
						trial_nodes = [source_elem.nodes[i] for i in sub]
						_, trial_distance = ebu.lct3(trial_nodes, Cpos)
						aux.append((trial_nodes, trial_distance))
					aux = sorted(aux, key = lambda variable: variable[1])
					retained_nodes = aux[0][0]
					distance = aux[0][1]
				elif family == MpcElementGeometryFamilyType.Hexahedron:
					# for any hexahedron, the first 8 nodes are the corner ones.
					# we need to find the closest sub-simplex
					aux = []
					for sub in ebu.HSubs:
						trial_nodes = [source_elem.nodes[i] for i in sub]
						_, trial_distance = ebu.lct4(trial_nodes, Cpos)
						aux.append((trial_nodes, trial_distance))
					aux = sorted(aux, key = lambda variable: variable[1])
					retained_nodes = aux[0][0]
					distance = aux[0][1]
				else:
					# unsupported element type
					raise Exception(_err(pinfo.condition.id, 
						'The source element (master geometry) of the Link element {} '
						'has a wrong family type ({})'.format(elem.id, family)
						))
				# check distance
				if distance > 1.0e-2:
					if ignore_outside:
						stats[1] += 1
						continue
					else:
						raise Exception(_err(pinfo.condition.id, 
							'The constrained node of the Link element {} '
							'is outside the embedding domain (error = {} %; Max allowed error = 1.0 %)'.format(elem.id, distance*100.0)
							))
				# open process if-statement block
				block_indent = ''
				if is_partitioned:
					block_indent = pinfo.tabIndent
					if not first_done:
						if process_block_count == 0:
							pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
						else:
							pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
						first_done = True
				# get slave node data
				Cnode_data = slave_node_map[Cnode.id]
				# make auxiliary node
				cnode_ndm, cnode_ndf = pinfo.node_to_model_map[Cnode.id]
				if cnode_ndm != 2 and cnode_ndm != 3:
					raise Exception(_err(pinfo.condition.id,
						'The constrained node must be either 2D or 3D, not {}D'.format(cnode_ndm)))
				if cnode_ndm == 2:
					if cnode_ndf != 2 and cnode_ndf != 3:
						raise Exception(_err(pinfo.condition.id,
							'The constrained node in 2D can have {} or {} DOFs, not {}'.format(cnode_ndf)))
				else:
					if cnode_ndf != 3 and cnode_ndf != 6:
						raise Exception(_err(pinfo.condition.id,
							'The constrained node in 3D can have {} or {} DOFs, not {}'.format(cnode_ndf)))
				pinfo.updateModelBuilder(cnode_ndm, cnode_ndf)
				aux_node_id = next_node_id()
				pos_str = ' '.join(FMT(Cnode.position[i]) for i in range(cnode_ndm))
				pinfo.out_file.write('\n{}{}node {}   {}\n'.format(pinfo.indent, block_indent, aux_node_id, pos_str))
				# get lumping factor and source slip material tag. Make a multiplier material
				circum = math.pi * dia
				tributary_length = Cnode_data[2]
				tributary_area = tributary_length * circum
				CUMA += tributary_area
				aux_mat_id = next_prop_id()
				pinfo.out_file.write('{}{}uniaxialMaterial Multiplier {} {} {}\n'.format(pinfo.indent, block_indent, aux_mat_id, slip_tag, FMT(tributary_area)))
				# make the zero-length element
				# element zeroLength $eleTag $iNode $jNode -mat $matTag1 $matTag2 ... -dir $dir1 $dir2 ... <-orient $x1 $x2 $x3 $yp1 $yp2 $yp3>
				Vx = Cnode_data[0]
				Vy = Cnode_data[1]
				mat_str = '{} '.format(aux_mat_id) + ' '.join(str(stiff_tag) for i in range(cnode_ndf-1))
				dir_str = ' '.join(str(i+1) for i in range(cnode_ndf))
				pinfo.out_file.write('{}{}element zeroLength {}   {} {}   -mat {} -dir {} -orient {} {} {}  {} {} {}\n'.format(
					pinfo.indent, block_indent, next_elem_id(), Cnode.id, aux_node_id, mat_str, dir_str,
					FMT(Vx[0]), FMT(Vx[1]), FMT(Vx[2]), FMT(Vy[0]), FMT(Vy[1]), FMT(Vy[2])))
				# write this element
				pinfo.out_file.write(
					'{}{}element ASDEmbeddedNodeElement {}  {}   {}   -K {} {}\n'.format(
						pinfo.indent, block_indent, elem.id, aux_node_id, 
						' '.join(str(Rnode.id) for Rnode in retained_nodes),
						FMT(K), rot
						)
					)
				stats[0] += 1
				
			#print(CUMA)
		# end-for-each-interaction
		# update process block count
		if is_partitioned:
			if first_done:
				process_block_count += 1
			if process_block_count > 0 and first_done:
				pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count
	
	# write description
	description = '\n{}# ASDEmbeddedRebarWithSlip at Condition: {}\n'.format(pinfo.indent, pinfo.condition.id)
	pinfo.out_file.write(description)
	# make a stiff material
	pinfo.out_file.write('\n{}# A stiff material for the non-slip DOFs\n'.format(pinfo.indent))
	stiff_tag = next_prop_id()
	pinfo.out_file.write('{}uniaxialMaterial Elastic {} {}\n'.format(pinfo.indent, stiff_tag, FMT(K)))
	
	# call the internal function based on partitions
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			pinfo.setProcessId(process_id)
			process_block_count = internal(process_id, process_block_count)
	else:
		internal(0, 0)
	
	# print stats
	print('Processed "ASDEmbeddedRebarWithSlip" at "Condition {}":'.format(pinfo.condition.id))
	print('   {} nodes correctly embedded\n   {} nodes ignored because outside the embedding domain'.format(*stats))
	