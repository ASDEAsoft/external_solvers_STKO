import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.utils.tcl_input as tclin
import math
import os

def makeXObjectMetaData():
	
	dp = 'file:///{}/ASDAbsorbingBoundaryElement.pdf'.format(os.path.dirname(os.path.realpath(__file__)))
	def mka(name, type, description, group, dimension = None, default = None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(description) +
			html_par(html_href(dp,'ASDAbsorbingBoundary3D')+'<br/>') +
			html_end()
			)
		if dimension:
			a.dimension = dimension
		if default:
			a.setDefault(default)
		return a
	
	fx = mka('Base Action X', MpcAttributeType.Index,
		('The time series used as velocity input at the bottom boundary along the X direction.\n'
		'It will be automatically multipled by:\n'
		'1) The Vs wave velocity\n'
		'2) The mass density\n'
		'3) 2, to compensate the half portion absorbed by the dashpots'),
		'Input', default = 0)
	fy = mka('Base Action Y', MpcAttributeType.Index,
		('The time series used as velocity input at the bottom boundary along the Y direction.\n'
		'It will be automatically multipled by:\n'
		'1) The Vs wave velocity\n'
		'2) The mass density\n'
		'3) 2, to compensate the half portion absorbed by the dashpots'),
		'Input', default = 0)
	fz = mka('Base Action Z', MpcAttributeType.Index,
		('The time series used as velocity input at the bottom boundary along the Z direction.\n'
		'It will be automatically multipled by:\n'
		'1) The Vp wave velocity\n'
		'2) The mass density\n'
		'3) 2, to compensate the half portion absorbed by the dashpots'),
		'Input', default = 0)
	fx.indexSource.type = MpcAttributeIndexSourceType.Definition
	fx.indexSource.addAllowedNamespace('timeSeries')
	fy.indexSource.type = MpcAttributeIndexSourceType.Definition
	fy.indexSource.addAllowedNamespace('timeSeries')
	fz.indexSource.type = MpcAttributeIndexSourceType.Definition
	fz.indexSource.addAllowedNamespace('timeSeries')
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDAbsorbingBoundary3DAuto'
	xom.addAttribute(fx)
	xom.addAttribute(fy)
	xom.addAttribute(fz)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,[3,4,6]),(3,[3,4,6]),(3,[3,4,6]),(3,[3,4,6])]

class _globals:
	# boundary type
	B = 1
	L = 2
	R = 3
	F = 4
	K = 5
	# boundary type to extrusion vector
	boundary_vectors = {
		B : ( 0.0, 0.0,-1.0),
		L : (-1.0, 0.0, 0.0),
		R : ( 1.0, 0.0, 0.0),
		F : ( 0.0,-1.0, 0.0),
		K : ( 0.0, 1.0, 0.0)
		}
	# boundary tangent for global direction upon fixing distorsion
	# (make sure the undistored element is globally aligned XYZ)
	# bugfix in not finding the initial permutation
	boundary_tangents = {
		B : ( 1.0, 0.0, 0.0),
		L : ( 0.0,-1.0, 0.0),
		R : ( 0.0, 1.0, 0.0),
		F : ( 1.0, 0.0, 0.0),
		K : (-1.0, 0.0, 0.0)
		}
	# permutations Q4
	perms = (
		(0,1,2,3),
		(1,2,3,0),
		(2,3,0,1),
		(3,0,1,2))

# boundary type to string
def _btype_to_string(b):
	if b == _globals.B: return 'B'
	if b == _globals.L: return 'L'
	if b == _globals.R: return 'R'
	if b == _globals.F: return 'F'
	if b == _globals.K: return 'K'
	raise Exception('invalid boundary type')

def _geta(xobj, name):
	at = xobj.getAttribute(name)
	if(at is None):
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return at

def _err(msg):
	return 'Error in "ASDAbsorbingBoundary3D" :\n{}'.format(msg)

class _position_t:
	def __init__(self, x, y, z, tol):
		self.x = x
		self.y = y
		self.z = z
		self.tolerance = tol
	def copy(self):
		return _position_t(self.x, self.y, self.z, self.tolerance)
	def __hash__(self):
		return hash((self.x, self.y, self.z))
	def __eq__(self, other):
		if abs(self.x - other.x) > self.tolerance: return False
		if abs(self.y - other.y) > self.tolerance: return False
		if abs(self.z - other.z) > self.tolerance: return False
		return True
	def __ne__(self, other):
		return not(self == other)
	def __str__(self):
		return str((self.x, self.y, self.z))
	def __repr__(self):
		return str(self)

class ASDAbsorbingBoundary3DInfoManager:
	def __init__(self):
		self.pmax = Math.vec3(0.0,0.0,0.0)
		self.pmin = Math.vec3(0.0,0.0,0.0)
		self.extrusion_size = 0.0
		self.tolerance = 1.0e-12
		self.nodes = {} #key = _position_t, value = node_id
		self.elements = {} #key = partition, value = element ids
	def getBoundaryType(self, elem):
		p = Math.vec3(0.0,0.0,0.0)
		for node in elem.nodes:
			p += node.position
		p /= float(len(elem.nodes))
		btype = ''
		if p.x < self.pmin.x + self.tolerance:
			btype = _globals.L
		elif p.x > self.pmax.x - self.tolerance:
			btype = _globals.R
		if p.y < self.pmin.y + self.tolerance:
			btype = _globals.F
		elif p.y > self.pmax.y - self.tolerance:
			btype = _globals.K
		elif p.z < self.pmin.z + self.tolerance:
			btype = _globals.B
		return btype

def preProcessElements(pinfo):
	
	# modules
	from itertools import combinations
	verbose = False
	
	# utils
	def next_node_id():
		i = pinfo.next_node_id
		pinfo.next_node_id += 1
		return i
	
	# document
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	# Find all geometries (only faces)
	# whose element property is ASDAbsorbingBoundary2D
	# 1) collect all faces in a list
	# 2) compute bounds
	source_elements = []
	bbox = FxBndBox()
	reference_count = 0
	for geom_id, geom in doc.geometries.items():
		# get the mesh of this geometry
		mesh_of_geom = doc.mesh.meshedGeometries[geom_id]
		# get element property assignments
		elem_prop_asn = geom.elementPropertyAssignment.onFaces
		# process all mesh domains of faces
		all_faces = mesh_of_geom.faces
		for face_id in range(len(all_faces)):
			face = all_faces[face_id]
			# get element property assigned to this face
			elem_prop = elem_prop_asn[face_id]
			if elem_prop is None:
				continue
			if elem_prop.XObject is None:
				continue
			if elem_prop.XObject.name != 'ASDAbsorbingBoundary3DAuto':
				continue
			# process all elements
			reference_count += 1
			for elem in face.elements:
				# check element
				if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Quadrilateral or len(elem.nodes)!=4:
					raise Exception(_err('invalid type of element or number of nodes, It should be a Quadrilateral with 4 nodes, not a {} with {} nodes'
						.format(elem.geometryFamilyType(), len(elem.nodes))))
				# collect element
				source_elements.append(elem)
				# update bbox
				for node in elem.nodes:
					bbox.add(node.position)
	
	# quick return
	if reference_count == 0:
		return
	App.monitor().sendMessage('Pre-processing ASDAbsorbingBoundary3D elements...')
	
	# make manager and save it
	manager = ASDAbsorbingBoundary3DInfoManager()
	pinfo.custom_data['ASDAbsorbingBoundary3D'] = manager
	
	# get bounds
	manager.pmin = bbox.minPoint
	manager.pmax = bbox.maxPoint
	manager.extrusion_size = bbox.maxSize * 0.05
	if manager.extrusion_size == 0.0:
		raise Exception(_err('The soil domain seems to have an empty bounding box'))
	manager.tolerance = max(1.0e-12, 1.0e-4*bbox.maxSize)
	
	# map face nodes to their boundary type and process_id (from elements)
	# key = node_id
	# value = map with:
	#         key = boundary type
	#         value = set of partitions for that boundary type
	node_info = {}
	for elem in source_elements:
		pid = doc.mesh.partitionData.elementPartition(elem.id)
		center = (elem.nodes[0].position + elem.nodes[1].position + elem.nodes[2].position + elem.nodes[3].position)/4.0
		x = center.x
		y = center.y
		z = center.z
		for node in elem.nodes:
			info = node_info.get(node.id, None)
			if info is None:
				info = {}
				node_info[node.id] = info
			if x < manager.pmin.x + manager.tolerance:
				item = info.get(_globals.L, None)
				if item is None:
					item = set()
					info[_globals.L] = item
				item.add(pid)
			elif x > manager.pmax.x - manager.tolerance:
				item = info.get(_globals.R, None)
				if item is None:
					item = set()
					info[_globals.R] = item
				item.add(pid)
			if y < manager.pmin.y + manager.tolerance:
				item = info.get(_globals.F, None)
				if item is None:
					item = set()
					info[_globals.F] = item
				item.add(pid)
			elif y > manager.pmax.y - manager.tolerance:
				item = info.get(_globals.K, None)
				if item is None:
					item = set()
					info[_globals.K] = item
				item.add(pid)
			if z < manager.pmin.z + manager.tolerance:
				item = info.get(_globals.B, None)
				if item is None:
					item = set()
					info[_globals.B] = item
				item.add(pid)
	# second pass. on multi-btype, add condition of lowest btype
	for _, info in node_info.items():
		if len(info) > 1:
			all_keys = sorted(info.keys())
			lowest = all_keys[0]
			lowest_partitions = info[lowest]
			for i in range(1,len(all_keys)):
				item = info[all_keys[i]]
				for other_partition in lowest_partitions:
					item.add(other_partition)
	if verbose:
		print('> Builing node info...')
		for node, info in node_info.items():
			print('   Node: {}'.format(node))
			for btype, bpart in info.items():
				print('      Boundary: {} -> {}'.format(_btype_to_string(btype), bpart))
	
	# extrude nodes and put them in their own partition for writing.
	# map - key = partiton_id
	#     - val = list of extra nodes (id, _position_t(x,y))
	# at the same time, save nodes and position in the manager
	if verbose:
		print('> Creating extruded nodes...')
	part_nodes = {}
	for source_node_id, info in node_info.items():
		source_node = doc.mesh.getNode(source_node_id)
		# get btype in a list
		btypes = list(info.keys())
		# create combinations of btypes
		combos = []
		for i in range(len(btypes)):
			nset = i+1
			icombos = combinations(btypes, nset)
			for icombo in icombos:
				# append it as a sorted list, because we need the lowest btype at first place
				combos.append(sorted(list(icombo)))
		# for each combination we can compute the vector (or combined vector)
		# for extrustion. then we can extrude the node and place it on the partitions it belongs to
		if verbose:
			print('   Combinations for node {}'.format(source_node_id))
		for icombo in combos:
			# extrusion vector
			vx = 0.0
			vy = 0.0
			vz = 0.0
			for btype in icombo:
				vector = _globals.boundary_vectors[btype]
				vx += vector[0]
				vy += vector[1]
				vz += vector[2]
			vx *= manager.extrusion_size
			vy *= manager.extrusion_size
			vz *= manager.extrusion_size
			# target partitons
			icombo_partitions = info[icombo[0]]
			if verbose:
				combo_name = ''.join(_btype_to_string(i) for i in icombo)
				print('   {} {} - partitions: {}'.format(combo_name, (vx,vy,vz), icombo_partitions))
			# extrude
			new_node_id = next_node_id()
			new_node_pos = _position_t(source_node.x + vx, source_node.y + vy, source_node.z + vz, manager.tolerance)
			# put it node to model map
			pinfo.node_to_model_map[new_node_id] = (3, 3)
			# put it in the manager
			manager.nodes[new_node_pos] = new_node_id
			# put it part_nodes
			for ipar in icombo_partitions:
				ipar_nodes = part_nodes.get(ipar, None)
				if ipar_nodes is None:
					ipar_nodes = []
					part_nodes[ipar] = ipar_nodes
				ipar_nodes.append((new_node_id, new_node_pos))
	if verbose:
		for ipart, inodes in part_nodes.items():
			print('   Partition {} -> {}'.format(ipart, inodes))
		print('> Manager nodes:')
		for pos, id in manager.nodes.items():
			print('   [{}] {}'.format(id, pos))
	
	# formatter for doubles
	FMT = pinfo.get_double_formatter()
	
	# now we can write a ASDAbsorbingBoundary2D.tcl file to source before the elements
	the_file = open('{}{}{}'.format(pinfo.out_dir, os.sep, 'ASDAbsorbingBoundary3D.tcl'), 'w+', encoding='utf-8')
	save_file = pinfo.out_file
	pinfo.out_file = the_file
	
	# process all nodes for each partition
	def write_nodes(items, indent):
		for id, pos in items:
			pinfo.out_file.write('{}node {}    {} {} {}\n'.format(indent, id, FMT(pos.x), FMT(pos.y), FMT(pos.z)))
	if pinfo.process_count > 1:
		indent = pinfo.indent + pinfo.tabIndent
		for partition_id, partition_nodes in part_nodes.items():
			pinfo.setProcessId(partition_id)
			pinfo.out_file.write('{}if {{$STKO_VAR_process_id == {}}} {{\n'.format(pinfo.indent, partition_id))
			pinfo.updateModelBuilder(3, 3)
			write_nodes(partition_nodes, indent)
			pinfo.out_file.write('{}}}\n'.format(pinfo.indent))
	else:
		indent = pinfo.indent
		pinfo.updateModelBuilder(3, 3)
		write_nodes(part_nodes[0], indent)
	
	# reset out file and close new file
	pinfo.out_file = save_file
	the_file.close()
	
	# source it
	pinfo.out_file.write('source ASDAbsorbingBoundary3D.tcl\n')

def _q4_remove_distortion(nodes, btype):
	import numpy as np
	# position matrix
	P = np.zeros((3,4))
	for j in range(4):
		nj = nodes[j]
		P[0,j] = nj.x
		P[1,j] = nj.y
		P[2,j] = nj.z
	# jacobian at center
	dN = np.asarray([[-0.25,-0.25], [0.25,-0.25], [0.25,0.25], [-0.25,0.25]])
	J0 = np.matmul(P, dN)
	dx = J0[:,0]
	dy = J0[:,1]
	def npnormalize(x):
		xn = np.linalg.norm(x)
		if xn == 0.0:
			raise Exception('ASDAbsorbingBoundary3D: Element has a singular jacobian. Make sure the element is not excessively distorted!')
		return x/xn
	dx = npnormalize(dx)
	dy = npnormalize(dy)
	dz = npnormalize(np.cross(dx, dy))
	#if abs(dz[0]) > 0.99:
	#	dx = np.asarray([0.0,1.0,0.0])
	#else:
	#	dy = np.asarray([1.0,0.0,0.0])
	#dy = npnormalize(np.cross(dz, dx))
	# bugfix for global alignement (after computing z)
	dx = np.asarray(_globals.boundary_tangents[btype])
	dy = npnormalize(np.cross(dz, dx))
	RT = np.asarray((dx,dy,dz))
	J0 = np.matmul(RT, J0)
	J0 = J0[0:2,0:2]
	detJ0 = np.linalg.det(J0)
	v0 = detJ0*4.0
	# modified jacobian
	J = np.zeros((2,2))
	Jnorms = [0.0, 0.0]
	for j in range(2):
		jn = np.linalg.norm(J0[:,j])
		J[:,j] = J0[:,j]/jn
		Jnorms[j] = jn
	for i in range(2):
		imax = abs(J[i,0])
		imax_id = 0
		jval = abs(J[i,1])
		if jval > imax:
			imax = jval
			imax_id = 1
		for j in range(2):
			if j != i:
				J[j,imax_id] = 0.0
	for j in range(2):
		jn = Jnorms[j]
		for i in range(2):
			J[i,j] *= jn
	detJ = np.linalg.det(J)
	v = detJ*4.0
	scale = math.sqrt(v0/v)
	J *= scale
	J = np.matmul(RT.transpose(), np.hstack([np.vstack([J, np.zeros((1,2))]), np.zeros((3,1))]))
	# centroid
	C = np.zeros((3,1))
	for j in range(4):
		pj = P[:,j]
		for i in range(3):
			C[i] += pj[i]/4.0
	# un-distored points of an equivalent-volume element
	P0 = np.asarray([[0.0, 1.0, 1.0, 0.0], [0.0, 0.0, 1.0, 1.0], [0.5, 0.5, 0.5, 0.5]])*2.0-1.0
	PE = np.tile(C, (1,4)) + np.matmul(J, P0)
	# done
	for j in range(4):
		nj = nodes[j]
		nj.x = PE[0,j]
		nj.y = PE[1,j]
		nj.z = PE[2,j]

def writeTcl(pinfo):
	
	# element ASDAbsorbingBoundary3D $Tag  $n1 $n2 $n3 $n4 $n5 $n6 $n7 $n8 $G $rho $btype <-fx $fx> <-fy $fy> <-fz $fz>
	
	# element
	elem = pinfo.elem
	elem_prop = pinfo.elem_prop
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Quadrilateral or len(elem.nodes)!=4:
		raise Exception(_err('invalid type of element or number of nodes, It should be a Quadrilateral with 4 nodes, not a {} with {} nodes'
			.format(elem.geometryFamilyType(), len(elem.nodes))))
	xobj = elem_prop.XObject
	
	# material
	mat_prop = pinfo.phys_prop
	if mat_prop is None:
		raise Exception(_err('Physical Property of type ASDAbsorbingBoundary3DMaterial must be provided'))
	xobjm = mat_prop.XObject
	if xobjm.name != 'ASDAbsorbingBoundary3DMaterial':
		raise Exception(_err('Physical Property of type ASDAbsorbingBoundary3DMaterial must be provided'))
	
	# info
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# get manager
	manager = pinfo.custom_data['ASDAbsorbingBoundary3D']
	
	# get parameters
	tag = elem.id
	G = _geta(xobjm, 'G').quantityScalar.value
	v = _geta(xobjm, 'v').real
	rho = _geta(xobjm, 'rho').quantityScalar.value
	btype = manager.getBoundaryType(elem)
	opt = ''
	if btype == _globals.B:
		fx = _geta(xobj, 'Base Action X').index
		fy = _geta(xobj, 'Base Action Y').index
		fz = _geta(xobj, 'Base Action Z').index
		if fx != 0:
			opt += ' -fx {}'.format(fx)
		if fy != 0:
			opt += ' -fy {}'.format(fy)
		if fz != 0:
			opt += ' -fz {}'.format(fz)
	
	# get extrusion vector
	vx, vy, vz = _globals.boundary_vectors[btype]
	vx *= manager.extrusion_size
	vy *= manager.extrusion_size
	vz *= manager.extrusion_size
	
	# get source nodes and reverse nodes if necessary (copy them! because we will handle any distortion!)
	def copynode(n):
		return MpcNode(n.id, n.x, n.y, n.z)
	P1 = copynode(elem.nodes[0])
	P2 = copynode(elem.nodes[1])
	P3 = copynode(elem.nodes[2])
	P4 = copynode(elem.nodes[3])
	_q4_remove_distortion((P1,P2,P3,P4), btype)
	N = (P2.position-P1.position).cross(P3.position-P1.position).normalized()
	FN = Math.vec3(vx, vy, vz).normalized()
	if N.dot(FN) < 0.0:
		P2,P4 = P4,P2
	# compute element bounding box
	bbox = FxBndBox()
	bbox.add(P1.position)
	bbox.add(P2.position)
	bbox.add(P3.position)
	bbox.add(P4.position)
	# permute for an easy processing
	if btype == _globals.L or btype == _globals.R:
		aux = [P1,P2,P3,P4]
		found = False
		for iper in _globals.perms:
			auxperm = [aux[i] for i in iper]
			firstpoint = auxperm[0]
			y = firstpoint.y
			z = firstpoint.z
			if y > bbox.maxPoint.y - manager.tolerance and z < bbox.minPoint.z + manager.tolerance:
				P1, P2, P3, P4 = auxperm
				found = True
				break
		if not found:
			raise Exception('Cannot find initial permutation')
	elif btype == _globals.B:
		aux = [P1,P2,P3,P4]
		found = False
		for iper in _globals.perms:
			auxperm = [aux[i] for i in iper]
			firstpoint = auxperm[0]
			x = firstpoint.x
			y = firstpoint.y
			if x < bbox.minPoint.x + manager.tolerance and y < bbox.minPoint.y + manager.tolerance:
				P1, P2, P3, P4 = auxperm
				found = True
				break
		if not found:
			raise Exception('Cannot find initial permutation')
	# get nodal ids
	N1 = P1.id
	N2 = P2.id
	N3 = P3.id
	N4 = P4.id
	# after sorting we can go back to real nodes
	PMAP = {}
	for node in elem.nodes:
		PMAP[node.id] = node
	P1 = PMAP[N1]
	P2 = PMAP[N2]
	P3 = PMAP[N3]
	P4 = PMAP[N4]
	# also revert the bbox
	bbox = FxBndBox()
	bbox.add(P1.position)
	bbox.add(P2.position)
	bbox.add(P3.position)
	bbox.add(P4.position)
	
	# compute first 4 points _position_t
	P1 = _position_t(P1.x, P1.y, P1.z, manager.tolerance)
	P2 = _position_t(P2.x, P2.y, P2.z, manager.tolerance)
	P3 = _position_t(P3.x, P3.y, P3.z, manager.tolerance)
	P4 = _position_t(P4.x, P4.y, P4.z, manager.tolerance)
	
	# get element partition
	doc = App.caeDocument()
	if doc is None:
		raise Exception(_err('Null document'))
	this_partition = doc.mesh.partitionData.elementPartition(tag)
	
	# create the data for auto-generated elements
	auto_gen_data = tclin.auto_generated_element_data()
	
	# utility to extrude P1,P2,P3,P4 along (Nx, Ny, Nz)
	def extrude(etag, bcode, Nx, Ny, Nz):
		# bcode to string
		if isinstance(bcode, tuple):
			sbtype = ''.join(_btype_to_string(i) for i in sorted(set(bcode)))
		else:
			sbtype = _btype_to_string(bcode)
		# get extra nodes by extrusion
		P5 = _position_t(P1.x + Nx, P1.y + Ny, P1.z + Nz, manager.tolerance)
		P6 = _position_t(P2.x + Nx, P2.y + Ny, P2.z + Nz, manager.tolerance)
		P7 = _position_t(P3.x + Nx, P3.y + Ny, P3.z + Nz, manager.tolerance)
		P8 = _position_t(P4.x + Nx, P4.y + Ny, P4.z + Nz, manager.tolerance)
		N5 = manager.nodes[P5]
		N6 = manager.nodes[P6]
		N7 = manager.nodes[P7]
		N8 = manager.nodes[P8]
		# if this is and extra element not generated by STKO...
		if etag != tag:
			auto_gen_data.elements.append(etag)
			auto_gen_data.elements_connectivity.append([
				(N1, (P1.x, P1.y, P1.z)),
				(N2, (P2.x, P2.y, P2.z)),
				(N3, (P3.x, P3.y, P3.z)),
				(N4, (P4.x, P4.y, P4.z)),
				(N5, (P5.x, P5.y, P5.z)),
				(N6, (P6.x, P6.y, P6.z)),
				(N7, (P7.x, P7.y, P7.z)),
				(N8, (P8.x, P8.y, P8.z))
			])
		# get connectivity
		conn = [N1, N2, N3, N4, N5, N6, N7, N8]
		# now write the string into the file
		pinfo.out_file.write(
			'{}element ASDAbsorbingBoundary3D {}   {} {} {} {} {} {} {} {}   {} {} {} {}{}\n'.format(
				pinfo.indent, etag, *conn, G, v, rho, sbtype, opt))
		# register element
		reg_value = manager.elements.get(this_partition, None)
		if reg_value is None:
			reg_value = []
			manager.elements[this_partition] = reg_value
		reg_value.append(etag)
		# return generated objects
		return (P5, N5, P6, N6, P7, N7, P8, N8)
	
	# make primary element
	P5,N5,P6,N6,P7,N7,P8,N8 = extrude(tag, btype, vx, vy, vz)
	
	# copy primary element
	CP = tuple(i.copy() for i in (P1,P2,P3,P4,P5,P6,P7,P8))
	CN = (N1,N2,N3,N4,N5,N6,N7,N8)
	
	# make secondary element if necessary
	def next_elem_id():
		i = pinfo.next_elem_id
		pinfo.next_elem_id += 1
		return i
	if btype == _globals.L:
		if bbox.minPoint.y < manager.pmin.y + manager.tolerance:
			# LF
			P1,P2,P3,P4 = P6,P2,P3,P7
			N1,N2,N3,N4 = N6,N2,N3,N7
			N = _globals.boundary_vectors[_globals.F]
			extrude(next_elem_id(), (_globals.L, _globals.F), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
			# restore
			P1,P2,P3,P4,P5,P6,P7,P8 = CP
			N1,N2,N3,N4,N5,N6,N7,N8 = CN
		if bbox.maxPoint.y > manager.pmax.y - manager.tolerance:
			# LK
			P1,P2,P3,P4 = P1,P5,P8,P4
			N1,N2,N3,N4 = N1,N5,N8,N4
			N = _globals.boundary_vectors[_globals.K]
			extrude(next_elem_id(), (_globals.L, _globals.K), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
			# restore
			P1,P2,P3,P4,P5,P6,P7,P8 = CP
			N1,N2,N3,N4,N5,N6,N7,N8 = CN
	elif btype == _globals.R:
		if bbox.minPoint.y < manager.pmin.y + manager.tolerance:
			# RF
			P1,P2,P3,P4 = P4,P8,P7,P3
			N1,N2,N3,N4 = N4,N8,N7,N3
			N = _globals.boundary_vectors[_globals.F]
			extrude(next_elem_id(), (_globals.R, _globals.F), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
			# restore
			P1,P2,P3,P4,P5,P6,P7,P8 = CP
			N1,N2,N3,N4,N5,N6,N7,N8 = CN
		if bbox.maxPoint.y > manager.pmax.y - manager.tolerance:
			# RK
			P1,P2,P3,P4 = P5,P1,P2,P6
			N1,N2,N3,N4 = N5,N1,N2,N6
			N = _globals.boundary_vectors[_globals.K]
			extrude(next_elem_id(), (_globals.R, _globals.K), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
			# restore
			P1,P2,P3,P4,P5,P6,P7,P8 = CP
			N1,N2,N3,N4,N5,N6,N7,N8 = CN
	elif btype == _globals.B:
		if bbox.minPoint.x < manager.pmin.x + manager.tolerance:
			# BL
			P1,P2,P3,P4 = P6,P5,P1,P2
			N1,N2,N3,N4 = N6,N5,N1,N2
			N = _globals.boundary_vectors[_globals.L]
			P5,N5,P6,N6,P7,N7,P8,N8 = extrude(next_elem_id(), (_globals.B, _globals.L), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
			# copy secondary element
			CP2 = tuple(i.copy() for i in (P1,P2,P3,P4,P5,P6,P7,P8))
			CN2 = (N1,N2,N3,N4,N5,N6,N7,N8)
			if bbox.minPoint.y < manager.pmin.y + manager.tolerance:
				# BLF
				P1,P2,P3,P4 = P6,P2,P3,P7
				N1,N2,N3,N4 = N6,N2,N3,N7
				N = _globals.boundary_vectors[_globals.F]
				extrude(next_elem_id(), (_globals.B, _globals.L, _globals.F), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
				# restore
				P1,P2,P3,P4,P5,P6,P7,P8 = CP2
				N1,N2,N3,N4,N5,N6,N7,N8 = CN2
			if bbox.maxPoint.y > manager.pmax.y - manager.tolerance:
				# BLK
				P1,P2,P3,P4 = P1,P5,P8,P4
				N1,N2,N3,N4 = N1,N5,N8,N4
				N = _globals.boundary_vectors[_globals.K]
				extrude(next_elem_id(), (_globals.B, _globals.L, _globals.K), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
				# restore
				P1,P2,P3,P4,P5,P6,P7,P8 = CP2
				N1,N2,N3,N4,N5,N6,N7,N8 = CN2
			# restore
			P1,P2,P3,P4,P5,P6,P7,P8 = CP
			N1,N2,N3,N4,N5,N6,N7,N8 = CN
		if bbox.maxPoint.x > manager.pmax.x - manager.tolerance:
			# BR
			P1,P2,P3,P4 = P8,P7,P3,P4
			N1,N2,N3,N4 = N8,N7,N3,N4
			N = _globals.boundary_vectors[_globals.R]
			P5,N5,P6,N6,P7,N7,P8,N8 = extrude(next_elem_id(), (_globals.B, _globals.R), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
			# copy secondary element
			CP2 = tuple(i.copy() for i in (P1,P2,P3,P4,P5,P6,P7,P8))
			CN2 = (N1,N2,N3,N4,N5,N6,N7,N8)
			if bbox.minPoint.y < manager.pmin.y + manager.tolerance:
				# BLF
				P1,P2,P3,P4 = P1,P5,P8,P4
				N1,N2,N3,N4 = N1,N5,N8,N4
				N = _globals.boundary_vectors[_globals.F]
				extrude(next_elem_id(), (_globals.B, _globals.R, _globals.F), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
				# restore
				P1,P2,P3,P4,P5,P6,P7,P8 = CP2
				N1,N2,N3,N4,N5,N6,N7,N8 = CN2
			if bbox.maxPoint.y > manager.pmax.y - manager.tolerance:
				# BLK
				P1,P2,P3,P4 = P6,P2,P3,P7
				N1,N2,N3,N4 = N6,N2,N3,N7
				N = _globals.boundary_vectors[_globals.K]
				extrude(next_elem_id(), (_globals.B, _globals.R, _globals.K), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
				# restore
				P1,P2,P3,P4,P5,P6,P7,P8 = CP2
				N1,N2,N3,N4,N5,N6,N7,N8 = CN2
			# restore
			P1,P2,P3,P4,P5,P6,P7,P8 = CP
			N1,N2,N3,N4,N5,N6,N7,N8 = CN
		if bbox.minPoint.y < manager.pmin.y + manager.tolerance:
			# BF
			P1,P2,P3,P4 = P5,P8,P4,P1
			N1,N2,N3,N4 = N5,N8,N4,N1
			N = _globals.boundary_vectors[_globals.F]
			extrude(next_elem_id(), (_globals.B, _globals.F), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
			# restore
			P1,P2,P3,P4,P5,P6,P7,P8 = CP
			N1,N2,N3,N4,N5,N6,N7,N8 = CN
		if bbox.maxPoint.y > manager.pmax.y - manager.tolerance:
			# BK
			P1,P2,P3,P4 = P7,P6,P2,P3
			N1,N2,N3,N4 = N7,N6,N2,N3
			N = _globals.boundary_vectors[_globals.K]
			extrude(next_elem_id(), (_globals.B, _globals.K), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size, N[2]*manager.extrusion_size)
			# restore
			P1,P2,P3,P4,P5,P6,P7,P8 = CP
			N1,N2,N3,N4,N5,N6,N7,N8 = CN
	
	# store auto-generated elements if any
	if len(auto_gen_data.elements) > 0:
		pinfo.auto_generated_element_data_map[tag] = auto_gen_data