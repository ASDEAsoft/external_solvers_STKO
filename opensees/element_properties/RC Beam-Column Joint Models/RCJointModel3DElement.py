import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import os
import traceback

def __geta(xobj, name):
	a = xobj.getAttribute(name)
	if(a is None):
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return a

def makeXObjectMetaData():
	
	def descr(title, text):
		return (
			html_par(html_begin()) +
			html_par(html_boldtext(title)+'<br/>') +
			html_par(text) +
			#html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLength_Element','ZeroLength Element')+'<br/>') +
			html_end()
			)
	
	# Lx
	at_Lx = MpcAttributeMetaData()
	at_Lx.type = MpcAttributeType.QuantityScalar
	at_Lx.name = 'Lx'
	at_Lx.group = 'Geometry'
	at_Lx.description = descr('Lx', 'Dimension along the local X direction')
	at_Lx.dimension = u.L
	
	# Ly
	at_Ly = MpcAttributeMetaData()
	at_Ly.type = MpcAttributeType.QuantityScalar
	at_Ly.name = 'Ly'
	at_Ly.group = 'Geometry'
	at_Ly.description = descr('Ly', 'Dimension along the local Y direction')
	at_Ly.dimension = u.L
	
	# Lx
	at_Lz = MpcAttributeMetaData()
	at_Lz.type = MpcAttributeType.QuantityScalar
	at_Lz.name = 'Lz'
	at_Lz.group = 'Geometry'
	at_Lz.description = descr('Lz', 'Dimension along the local Z direction')
	at_Lz.dimension = u.L
	
	xom = MpcXObjectMetaData()
	xom.name = 'RCJointModel3DElement'
	xom.addAttribute(at_Lx)
	xom.addAttribute(at_Ly)
	xom.addAttribute(at_Lz)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]

class RCJointModel3DElementInfo:
	def __init__(self, geom_id, vertex_id, n1, n2, vx, vy, vz, lx, ly, lz, K, mat_x, mat_y):
		# the source geometry (vertex) id
		self.geom_id = geom_id
		self.vertex_id = vertex_id
		# the source node of the column-column joint
		self.source_node = n1
		# the duplicated node for the joint, where beam elements will be attached
		self.other_node = n2
		# the directors of the joint local axes
		self.vx = vx
		self.vy = vy
		self.vz = vz
		# the joint dimensions in local coordinates
		self.lx = lx
		self.ly = ly
		self.lz = lz
		# materials
		self.K = K
		self.mat_x = mat_x
		self.mat_y = mat_y

# a manager class for custom pre processing
class RCJointModel3DElementInfoManager:
	
	def __init__(self):
		self.items = {}
	
	def toString(self):
		from io import StringIO
		ss = StringIO()
		ss.write('RCJointModel3DElementInfoManager Data:\n')
		for _, info in self.items.items():
			ss.write('{\n')
			ss.write('   GID: {}\n'.format(info.geom_id))
			ss.write('   VID: {}\n'.format(info.vertex_id))
			ss.write('   N1: {}\n'.format(info.source_node))
			ss.write('   N2: {}\n'.format(info.other_node))
			m = Math.mat3(info.vx, info.vy, info.vz)
			ss.write('   Vx | Vy | Vz\n{}'.format(m))
			ss.write('   Size: {} x {} x {}\n'.format(info.lx, info.ly, info.lz))
			ss.write('   K: {}\n'.format(info.K))
			ss.write('   Mx: {}\n'.format(info.mat_x))
			ss.write('   My: {}\n'.format(info.mat_y))
			ss.write('}\n')
		return ss.getvalue()
	
	def adjustBeamConnectivity(self, pinfo, elem, node_id_vec):
		# node_id_vec = vector of ids with source nodes
		# here we use the nodes in elem to check whether this element
		# converges in a joint, and if it is aligned with one of the joint directions.
		# If so, change its connectivity (not really, only in node_id_vec)
		
		def err(X):
			return "Error while adjusting beam connectivity for joint:\n{}\n".format(X)
		
		def next_node_id():
			i = pinfo.next_node_id
			pinfo.next_node_id += 1
			return i
		
		# checks
		if elem is None:
			raise Exception(err("Input element is NULL"))
		if len(elem.nodes) != len(node_id_vec):
			raise Exception(err("len(elem.nodes) != len(node_id_vec)"))
		if len(elem.nodes) != 2:
			raise Exception(err("RCJointModel3D works only with 2-node elements"))
		
		# formatter for doubles
		FMT = pinfo.get_double_formatter()
		
		# bugfix: 16/7/2020
		# assume that on enter, node_id_vec is equal to the ids in elem.nodes
		for i in range(len(elem.nodes)):
			ni = elem.nodes[i]
			nid = node_id_vec[i]
			if ni.id != nid:
				raise Exception("RC Joint Model 3D Element - Internal Error: nodes.id != node_id_vec on enter")
		
		# output
		# we may need to return the offset of the generated nodes
		#node_pos_out = [Math.vec3(0.0, 0.0, 0.0), Math.vec3(0.0, 0.0, 0.0)]
		# bugfix: 16/7/2020
		# node_pos_out should be initialized with the initial positions, not 0, otherwise, if one of the nodes
		# is not in this Joint group, it will default to 000.
		node_pos_out = [elem.nodes[0].position, elem.nodes[1].position]
		
		# an auxiliary tuple for next node id
		aux_next = (0, 1, 0)
		# process each node
		for i in range(len(elem.nodes)):
			node = elem.nodes[i]
			nid = node_id_vec[i]
			dx = None
			if nid in self.items:
				
				# get joint data (RCJointModel3DElementInfo)
				joint = self.items[nid]
				# get beam axis direction
				if dx is None:
					dx = elem.nodes[1].position - elem.nodes[0].position
					dx.normalize()
				
				# if the beam axis is aligned with the joint local Z direction, it is a column,
				# so we don't need to change its connectivity at this node
				if abs(dx.dot(joint.vz)) > 0.99:
					bdir = joint.vz
					blen = joint.lz
					# found a column.
					# let's start assuming that the joint offset in this direction is 0
					# in this case the modified node will be the source_node in the joint
					# note that this other_node has already been written for all processes the
					# source node belong to!
					nid_mod = joint.source_node
					# if the joint offset is greater than 0, then we need to create another
					# note and link it with the source_node by means of rigid links!
					if blen > 0.0:
						# the offset vector with respect to the current node
						next_node = elem.nodes[aux_next[i+1]]
						offset = (next_node.position - node.position).normalized() * (blen/2.0)
						offset_node_pos = node.position + offset
						offset_node_id = next_node_id()
						# save for output
						node_pos_out[i] = offset_node_pos
						# we don't need to check for partiton
						# because the calling element is already on its own partition
						# therefore this other node and the rigid link will be on the current partition!
						# make a 3D-6DOF model
						pinfo.updateModelBuilder(3,6)
						pinfo.node_to_model_map[offset_node_id] = (3, 6)
						pinfo.out_file.write('\n\n{}# RCJointModel3D at Geometry = {} (Sub-Vertex = {}), with Mesh Node = {} (auxiliary for element {})\n'.format(
							pinfo.indent, joint.geom_id, joint.vertex_id, joint.source_node, elem.id))
						pinfo.out_file.write('{}node {} {} {} {}\n'.format(pinfo.indent, offset_node_id, FMT(offset_node_pos.x), FMT(offset_node_pos.y), FMT(offset_node_pos.z)))
						pinfo.out_file.write('{}rigidLink beam {} {}\n'.format(pinfo.indent, joint.source_node, offset_node_id))
						nid_mod = offset_node_id
						
					# change the node id, and  break the j loop
					node_id_vec[i] = nid_mod
				
				# the other 2 directions (vx, and vy) are for beams
				# check them in a loop
				bdir_tuple = (joint.vx, joint.vy)
				blen_tuple = (joint.lx, joint.ly)
				for j in range(2):
					bdir = bdir_tuple[j]
					blen = blen_tuple[j]
					# if it is aligned with the j-th direction it is a beam converging in this joint
					if abs(dx.dot(bdir)) > 0.99:
						
						# found a beam.
						# let's start assuming that the joint offset in this direction is 0
						# in this case the modified node will be the other_node in the joint
						# note that this other_node has already been written for all processes the
						# source node belong to!
						nid_mod = joint.other_node
						
						# if the joint offset is greater than 0, then we need to create another
						# note and link it with the other_node by means of rigid links!
						if blen > 0.0:
							# the offset vector with respect to the current node
							next_node = elem.nodes[aux_next[i+1]]
							offset = (next_node.position - node.position).normalized() * (blen/2.0)
							offset_node_pos = node.position + offset
							offset_node_id = next_node_id()
							# save for output
							node_pos_out[i] = offset_node_pos
							# we don't need to check for partiton
							# because the calling element is already on its own partition
							# therefore this other node and the rigid link will be on the current partition!
							# make a 3D-6DOF model
							pinfo.updateModelBuilder(3,6)
							pinfo.node_to_model_map[offset_node_id] = (3, 6)
							pinfo.out_file.write('\n\n{}# RCJointModel3D at Geometry = {} (Sub-Vertex = {}), with Mesh Node = {} (auxiliary for element {})\n'.format(
								pinfo.indent, joint.geom_id, joint.vertex_id, joint.source_node, elem.id))
							pinfo.out_file.write('{}node {} {} {} {}\n'.format(pinfo.indent, offset_node_id, FMT(offset_node_pos.x), FMT(offset_node_pos.y), FMT(offset_node_pos.z)))
							pinfo.out_file.write('{}rigidLink beam {} {}\n'.format(pinfo.indent, joint.other_node, offset_node_id))
							nid_mod = offset_node_id
							
						# change the node id, and  break the j loop
						node_id_vec[i] = nid_mod
						break
		
		# done
		return node_pos_out

def preProcessElements(pinfo):
	
	# utils
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
	
	# document
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	# create the info manager
	manager = RCJointModel3DElementInfoManager()
	
	# Find all geometries (only vertices)
	# whose physical property and element property are 
	# RCJointModel3D and RCJointModel3DElement respectively.
	for geom_id, geom in doc.geometries.items():
		# get the mesh of this geometry
		mesh_of_geom = doc.mesh.meshedGeometries[geom_id]
		# get physical and element property assignments
		phys_prop_asn = geom.physicalPropertyAssignment.onVertices
		elem_prop_asn = geom.elementPropertyAssignment.onVertices
		# process all mesh nodes of vertices
		all_nodes = mesh_of_geom.vertices
		for domain_id in range(len(all_nodes)):
			node = all_nodes[domain_id]
			# get physical and element property assigned to this domain (node)
			phys_prop = phys_prop_asn[domain_id]
			elem_prop = elem_prop_asn[domain_id]
			if (phys_prop is None) or (elem_prop is None):
				continue
			if (phys_prop.XObject is None) or (elem_prop.XObject is None):
				continue
			if (phys_prop.XObject.name != 'RCJointModel3D') or (elem_prop.XObject.name != 'RCJointModel3DElement'):
				continue
			# get element property attributes
			lx = __geta(elem_prop.XObject, 'Lx').quantityScalar.value
			ly = __geta(elem_prop.XObject, 'Ly').quantityScalar.value
			lz = __geta(elem_prop.XObject, 'Lz').quantityScalar.value
			# get node local axes vectors
			vx = Math.vec3()
			vy = Math.vec3()
			vz = Math.vec3()
			geom.getLocalAxesOnVertex(domain_id, vx, vy, vz)
			# original and duplicated node ids
			n1 = node.id
			n2 = next_node_id()
			# penalty stiffness
			K = __geta(phys_prop.XObject, 'K (penalty)').real
			mat_x = __geta(phys_prop.XObject, 'X Material').index
			mat_y = __geta(phys_prop.XObject, 'Y Material').index
			# add the joint info for this node, use the source node id as key
			manager.items[n1] = RCJointModel3DElementInfo(geom_id, domain_id, n1, n2, vx, vy, vz, lx, ly, lz, K, mat_x, mat_y)
	#print(manager.toString())
	
	# quick return
	if len(manager.items) == 0:
		return
	App.monitor().sendMessage('Pre-processing RCJointModel3DElement elements...')
	
	# formatter for doubles
	FMT = pinfo.get_double_formatter()
	
	# now we can write a RCJointModel3D.tcl file to source before the elements
	joint_file = open('{}{}{}'.format(pinfo.out_dir, os.sep, 'RCJointModel3D.tcl'), 'w+')
	save_file = pinfo.out_file
	pinfo.out_file = joint_file
	
	# utility for writing
	def write_joint(joint, do_spring=True, indent=''):
		# make a 3D-6DOF model
		pinfo.updateModelBuilder(3,6)
		# write the other_node
		node = doc.mesh.getNode(joint.source_node)
		pinfo.node_to_model_map[joint.other_node] = (3, 6)
		pinfo.out_file.write('\n{}{}# RCJointModel3D at Geometry = {} (Sub-Vertex = {}), with Mesh Node = {}\n'.format(pinfo.indent, indent, joint.geom_id, joint.vertex_id, joint.source_node))
		pinfo.out_file.write('{}{}node {} {} {} {}\n'.format(pinfo.indent, indent, joint.other_node, FMT(node.x), FMT(node.y), FMT(node.z)))
		# write the spring
		if do_spring:
			# stiff material
			stiff_mat = next_prop_id()
			#uniaxialMaterial Elastic $matTag $E
			pinfo.out_file.write('{}{}uniaxialMaterial Elastic {} {}\n'.format(pinfo.indent, indent, stiff_mat, joint.K))
			#element zeroLength $eleTag $iNode $jNode -mat $matTag1 $matTag2 ... -dir $dir1 $dir2 ...<-doRayleigh $rFlag> <-orient $x1 $x2 $x3 $yp1 $yp2 $yp3>
			pinfo.out_file.write(
				'{0}{1}element zeroLength {2}   {3} {4}   -mat {7} {7} {7} {5} {6} {7}   -dir 1 2 3 4 5 6   -orient {8} {9} {10}   {11} {12} {13}\n'.format(
					pinfo.indent, indent, # 0 1
					next_elem_id(), joint.source_node, joint.other_node,  # 2 3 4
					joint.mat_x, joint.mat_y, stiff_mat, # 5 6 7
					joint.vx[0], joint.vx[1], joint.vx[2], # 8 9 10
					joint.vy[0], joint.vy[1], joint.vy[2], # 11 12 13
					))
	
	# process all nodes based on sequential/partitoned mesh
	if pinfo.process_count > 1:
		# split domain elements by partition (use source node partition)
		for processor_id in range(pinfo.process_count):
			pid_count = 0 # number of joints processed in this partition
			# process each joint
			for _, joint in manager.items.items():
				if doc.mesh.partitionData.isNodeOnParition(joint.source_node, processor_id):
					# this joint can be processed on this partition
					# open process scope (only for the first one in this processor)
					if pid_count == 0:
						pinfo.setProcessId(processor_id)
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', processor_id, '} {'))
					# write this joint
					write_joint(joint, do_spring = (doc.mesh.partitionData.nodePartition(joint.source_node)==processor_id), indent=pinfo.tabIndent)
					pid_count += 1
			# close process scope
			if pid_count > 0:
				pinfo.out_file.write('{}{}\n'.format(pinfo.indent, '}'))
		# back to default processor
		pinfo.setProcessId(0) 
	else:
		# process each joint
		for _, joint in manager.items.items():
			write_joint(joint)
	
	# save manager
	pinfo.custom_data['RCJointModel3D'] = manager
	
	# reset out file and close new file
	pinfo.out_file = save_file
	joint_file.close()
	
	# source it
	pinfo.out_file.write('source RCJointModel3D.tcl\n')

def writeTcl(pinfo):
	pass