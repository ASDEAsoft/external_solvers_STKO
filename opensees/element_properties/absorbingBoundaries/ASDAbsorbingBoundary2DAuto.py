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
			html_par(html_href(dp,'ASDAbsorbingBoundary2D')+'<br/>') +
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
		'3) The thickness\n'
		'4) 2, to compensate the half portion absorbed by the dashpots'),
		'Input', default = 0)
	fy = mka('Base Action Y', MpcAttributeType.Index,
		('The time series used as velocity input at the bottom boundary along the Y direction.\n'
		'It will be automatically multipled by:\n'
		'1) The Vp wave velocity\n'
		'2) The mass density\n'
		'3) The thickness\n'
		'4) 2, to compensate the half portion absorbed by the dashpots'),
		'Input', default = 0)
	fx.indexSource.type = MpcAttributeIndexSourceType.Definition
	fx.indexSource.addAllowedNamespace('timeSeries')
	fy.indexSource.type = MpcAttributeIndexSourceType.Definition
	fy.indexSource.addAllowedNamespace('timeSeries')
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDAbsorbingBoundary2DAuto'
	xom.addAttribute(fx)
	xom.addAttribute(fy)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,[2,3]),(2,[2,3])]

class _globals:
	# boundary type
	B = 1
	L = 2
	R = 3
	# boundary type to extrusion vector
	boundary_vectors = {
		B : ( 0.0,-1.0),
		L : (-1.0, 0.0),
		R : ( 1.0, 0.0)}

# boundary type to string
def _btype_to_string(b):
	if b == _globals.B: return 'B'
	if b == _globals.L: return 'L'
	if b == _globals.R: return 'R'
	raise Exception('invalid boundary type')

def _geta(xobj, name):
	at = xobj.getAttribute(name)
	if(at is None):
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return at

def _err(msg):
	return 'Error in "ASDAbsorbingBoundary2D" :\n{}'.format(msg)

class _position_t:
	def __init__(self, x, y, tol):
		self.x = x
		self.y = y
		self.tolerance = tol
	def __hash__(self):
		return hash((self.x, self.y))
	def __eq__(self, other):
		if abs(self.x - other.x) > self.tolerance: return False
		if abs(self.y - other.y) > self.tolerance: return False
		return True
	def __ne__(self, other):
		return not(self == other)
	def __str__(self):
		return str((self.x, self.y))
	def __repr__(self):
		return str(self)

class ASDAbsorbingBoundary2DInfoManager:
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
		elif p.y < self.pmin.y + self.tolerance:
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
	
	# Find all geometries (only edges)
	# whose element property is ASDAbsorbingBoundary2D
	# 1) collect all edges in a list
	# 2) compute bounds
	source_elements = []
	bbox = FxBndBox()
	reference_count = 0
	for geom_id, geom in doc.geometries.items():
		# get the mesh of this geometry
		mesh_of_geom = doc.mesh.meshedGeometries[geom_id]
		# get element property assignments
		elem_prop_asn = geom.elementPropertyAssignment.onEdges
		# process all mesh domains of edges
		all_edges = mesh_of_geom.edges
		for edge_id in range(len(all_edges)):
			edge = all_edges[edge_id]
			# get element property assigned to this edge
			elem_prop = elem_prop_asn[edge_id]
			if elem_prop is None:
				continue
			if elem_prop.XObject is None:
				continue
			if elem_prop.XObject.name != 'ASDAbsorbingBoundary2DAuto':
				continue
			# process all elements
			reference_count += 1
			for elem in edge.elements:
				# check element
				if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Line or len(elem.nodes)!=2:
					raise Exception(_err('invalid type of element or number of nodes, It should be a Line with 2 nodes, not a {} with {} nodes'
						.format(elem.geometryFamilyType(), len(elem.nodes))))
				# collect element
				source_elements.append(elem)
				# update bbox
				for node in elem.nodes:
					bbox.add(node.position)
	
	# quick return
	if reference_count == 0:
		return
	App.monitor().sendMessage('Pre-processing ASDAbsorbingBoundary2D elements...')
	
	# make manager and save it
	manager = ASDAbsorbingBoundary2DInfoManager()
	pinfo.custom_data['ASDAbsorbingBoundary2D'] = manager
	
	# get bounds
	manager.pmin = bbox.minPoint
	manager.pmax = bbox.maxPoint
	manager.extrusion_size = bbox.maxSize * 0.05
	if manager.extrusion_size == 0.0:
		raise Exception(_err('The soil domain seems to have an empty bounding box'))
	manager.tolerance = max(1.0e-12, 1.0e-8*bbox.maxSize)
	
	# map edge nodes to their boundary type and process_id (from elements)
	# key = node_id
	# value = map with:
	#         key = boundary type
	#         value = set of partitions for that boundary type
	node_info = {}
	for elem in source_elements:
		pid = doc.mesh.partitionData.elementPartition(elem.id)
		center = (elem.nodes[0].position + elem.nodes[1].position)/2.0
		x = center.x
		y = center.y
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
			for btype in icombo:
				vector = _globals.boundary_vectors[btype]
				vx += vector[0]
				vy += vector[1]
			vx *= manager.extrusion_size
			vy *= manager.extrusion_size
			# target partitons
			icombo_partitions = info[icombo[0]]
			if verbose:
				combo_name = ''.join(_btype_to_string(i) for i in icombo)
				print('   {} {} - partitions: {}'.format(combo_name, (vx,vy), icombo_partitions))
			# extrude
			new_node_id = next_node_id()
			new_node_pos = _position_t(source_node.x + vx, source_node.y + vy, manager.tolerance)
			# put it node to model map
			pinfo.node_to_model_map[new_node_id] = (2, 2)
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
	the_file = open('{}{}{}'.format(pinfo.out_dir, os.sep, 'ASDAbsorbingBoundary2D.tcl'), 'w+')
	save_file = pinfo.out_file
	pinfo.out_file = the_file
	
	# process all nodes for each partition
	def write_nodes(items, indent):
		for id, pos in items:
			pinfo.out_file.write('{}node {}    {} {}\n'.format(indent, id, FMT(pos.x), FMT(pos.y)))
	if pinfo.process_count > 1:
		indent = pinfo.indent + pinfo.tabIndent
		for partition_id, partition_nodes in part_nodes.items():
			pinfo.setProcessId(partition_id)
			pinfo.out_file.write('{}if {{$STKO_VAR_process_id == {}}} {{\n'.format(pinfo.indent, partition_id))
			pinfo.updateModelBuilder(2, 2)
			write_nodes(partition_nodes, indent)
			pinfo.out_file.write('{}}}\n'.format(pinfo.indent))
	else:
		indent = pinfo.indent
		pinfo.updateModelBuilder(2, 2)
		write_nodes(part_nodes[0], indent)
	
	# reset out file and close new file
	pinfo.out_file = save_file
	the_file.close()
	
	# source it
	pinfo.out_file.write('source ASDAbsorbingBoundary2D.tcl\n')

def writeTcl(pinfo):
	
	# element ASDAbsorbingBoundary2D $Tag  $n1 $n2 $n3 $n4 $G $rho $thickness $btype
	
	# element
	elem = pinfo.elem
	elem_prop = pinfo.elem_prop
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Line or len(elem.nodes)!=2:
		raise Exception(_err('invalid type of element or number of nodes, It should be a Line with 2 nodes, not a {} with {} nodes'
			.format(elem.geometryFamilyType(), len(elem.nodes))))
	xobj = elem_prop.XObject
	
	# material
	mat_prop = pinfo.phys_prop
	if mat_prop is None:
		raise Exception(_err('Physical Property of type ASDAbsorbingBoundary2DMaterial must be provided'))
	xobjm = mat_prop.XObject
	if xobjm.name != 'ASDAbsorbingBoundary2DMaterial':
		raise Exception(_err('Physical Property of type ASDAbsorbingBoundary2DMaterial must be provided'))
	
	# info
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# get manager
	manager = pinfo.custom_data['ASDAbsorbingBoundary2D']
	
	# get parameters
	tag = elem.id
	G = _geta(xobjm, 'G').quantityScalar.value
	v = _geta(xobjm, 'v').real
	rho = _geta(xobjm, 'rho').quantityScalar.value
	thickness = _geta(xobjm, 'thickness').quantityScalar.value
	btype = manager.getBoundaryType(elem)
	opt = ''
	if btype == _globals.B:
		fx = _geta(xobj, 'Base Action X').index
		fy = _geta(xobj, 'Base Action Y').index
		if fx != 0:
			opt += ' -fx {}'.format(fx)
		if fy != 0:
			opt += ' -fy {}'.format(fy)
	
	# get extrusion vector
	vx, vy = _globals.boundary_vectors[btype]
	vx *= manager.extrusion_size
	vy *= manager.extrusion_size
	
	# get source nodes and reverse nodes if necessary
	P1 = elem.nodes[0]
	P2 = elem.nodes[1]
	T = (P2.position - P1.position).normalized()
	N = Math.vec3(vx, vy, 0.0)
	Vz = T.cross(N)
	if Vz[2] < 0.0:
		P1, P2 = P2, P1
	N1 = P1.id
	N2 = P2.id
	
	# compute P1 P2 _position_t
	P1 = _position_t(P1.x, P1.y, manager.tolerance)
	P2 = _position_t(P2.x, P2.y, manager.tolerance)
	
	# get element partition
	doc = App.caeDocument()
	if doc is None:
		raise Exception(_err('Null document'))
	this_partition = doc.mesh.partitionData.elementPartition(tag)
	
	# create the data for auto-generated elements
	auto_gen_data = tclin.auto_generated_element_data()
	
	# utility to extrude P1 and P2 along (Nx, Ny)
	def extrude(etag, bcode, Nx, Ny):
		# bcode to string
		if isinstance(bcode, tuple):
			sbtype = ''.join(_btype_to_string(i) for i in sorted(set(bcode)))
		else:
			sbtype = _btype_to_string(bcode)
		# get extra nodes by extrusion
		P3 = _position_t(P2.x + Nx, P2.y + Ny, manager.tolerance)
		P4 = _position_t(P1.x + Nx, P1.y + Ny, manager.tolerance)
		N3 = manager.nodes[P3]
		N4 = manager.nodes[P4]
		# if this is and extra element not generated by STKO...
		if etag != tag:
			auto_gen_data.elements.append(etag)
			auto_gen_data.elements_connectivity.append([
				(N1, (P1.x, P1.y, 0.0)),
				(N2, (P2.x, P2.y, 0.0)),
				(N3, (P3.x, P3.y, 0.0)),
				(N4, (P4.x, P4.y, 0.0))
			])
		# get connectivity
		conn = [N1, N2, N3, N4]
		# now write the string into the file
		pinfo.out_file.write(
			'{}element ASDAbsorbingBoundary2D {}   {} {} {} {}   {} {} {} {} {}{}\n'.format(
				pinfo.indent, etag, *conn, G, v, rho, thickness, sbtype, opt))
		# register element
		reg_value = manager.elements.get(this_partition, None)
		if reg_value is None:
			reg_value = []
			manager.elements[this_partition] = reg_value
		reg_value.append(etag)
		# return generated objects
		return (P3, N3, P4, N4)
	
	# make primary element
	P3, N3, P4, N4 = extrude(tag, btype, vx, vy)
	
	# make secondary element if necessary
	def next_elem_id():
		i = pinfo.next_elem_id
		pinfo.next_elem_id += 1
		return i
	if btype == _globals.B:
		bbox = FxBndBox()
		for node in elem.nodes:
			bbox.add(node.position)
		if bbox.minPoint.x < manager.pmin.x + manager.tolerance:
			# BL
			P1 = P3
			N1 = N3
			N = _globals.boundary_vectors[_globals.L]
			extrude(next_elem_id(), (_globals.B, _globals.L), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size)
		elif bbox.maxPoint.x > manager.pmax.x - manager.tolerance:
			#BR
			P2 = P4
			N2 = N4
			N = _globals.boundary_vectors[_globals.R]
			extrude(next_elem_id(), (_globals.B, _globals.R), N[0]*manager.extrusion_size, N[1]*manager.extrusion_size)
	
	# store auto-generated elements if any
	if len(auto_gen_data.elements) > 0:
		pinfo.auto_generated_element_data_map[tag] = auto_gen_data