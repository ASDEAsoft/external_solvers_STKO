import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *
import os

def makeXObjectMetaData():
	
	def mka(name, type, group, description, dval=None, dim=None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(description) +
			html_end()
			)
		if dval:
			a.setDefault(dval)
		if dim:
			a.dimension = dim
		return a
	
	ap = mka('Axle positions', MpcAttributeType.QuantityVector, 'Vehicle', 
		'List of axle positions.'
		'The first object corresponds to the rearmost axle, '
		'the last one to the frontmost axle',
		dim = u.L)
	
	am = mka('Axle masses', MpcAttributeType.QuantityVector, 'Vehicle', 
		'List of axle masses (nodal mass values corresponding to each axle).'
		'The first object corresponds to the rearmost axle, '
		'the last one to the frontmost axle',
		dim = (u.F*u.t**2)/u.L)
	
	vel = mka('Velocity', MpcAttributeType.QuantityScalar, 'Vehicle transit information', 
		'The velocity of the vehicle',
		dim = u.L/u.t)
	
	per = mka('Period', MpcAttributeType.QuantityScalar, 'Vehicle transit information', 
		'The time between the passage of one vehicle and the next.'
		'If Period is set to 0, only 1 vehicle will be considered (i.e. period will be set to infinity)',
		dim = u.t,
		dval = 0.0)
	
	t0 = mka('Start time', MpcAttributeType.QuantityScalar, 'Vehicle transit information',
		'The time in which the frontmost axle of the vehicle enters the first point of the path',
		dim = u.t,
		dval = 0.0)
	
	g = mka('Gravity acceleration', MpcAttributeType.QuantityScalar, 'Misc',
		'The gravity acceleration (positive)', dim = u.L/u.t**2,
		dval = 9.81)
	
	xom = MpcXObjectMetaData()
	xom.name = 'MovingLoad'
	xom.addAttribute(ap)
	xom.addAttribute(am)
	xom.addAttribute(vel)
	xom.addAttribute(per)
	xom.addAttribute(t0)
	xom.addAttribute(g)
	
	return xom

def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.ConstraintGlyph
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = True
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = True
	return d

def _err(xobj, msg):
	return 'Error in MovingLoad (Condition {}): {}'.format(xobj.parent.componentId, msg)

def _geta(xobj, name):
	a = xobj.getAttribute(name)
	if a is None:
		raise Exception(_err(xobj, 'Cannot find attribute "{}"'.format(name)))
	return a

def _check_vectors(xobj, source = None):
	wp = _geta(xobj, 'Axle positions').quantityVector
	wm = _geta(xobj, 'Axle masses').quantityVector
	if source:
		if source == 'Axle positions':
			a,b = wp,wm
		else:
			a,b = wm,wp
	else:
		if len(wp) > len(wm):
			a,b = wp,wm
		else:
			a,b = wm,wp
	if len(a) != len(b):
		b.resize(len(a))

def onEditBegin(editor, xobj):
	_check_vectors(xobj)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name in ['Axle positions', 'Axle masses']:
		_check_vectors(xobj, attribute_name)

def _mapNodesToElements(doc, condition):
	def _process_element(ele):
		if len(ele.nodes) != 2:
			raise Exception(_err(condition.XObject,
			"Only 2-node line elements are allowed.\n"
			"Please use Linear order in Mesh Controls."))
		for node in ele.nodes:
			connected_elements = map_node_eles.get(node.id, None)
			if connected_elements is None:
				connected_elements = []
				map_node_eles[node.id] = connected_elements
			connected_elements.append(ele)
			if len(connected_elements) > 2:
				raise Exception(_err(condition.XObject,
				"Found a node connected "
				"to more than 2 edges (this is not allowed)"))
	map_node_eles = {}
	for geom, subset in condition.assignment.geometries.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		for eid in subset.edges:
			edge = mesh_of_geom.edges[eid]
			for ele in edge.elements:
				_process_element(ele)
	for inter in condition.assignment.interactions:
		mesh_of_inter = doc.mesh.getMeshedInteraction(inter.id)
		for ele in mesh_of_inter.elements:
			_process_element(ele)
	return map_node_eles

def _findPathBoundaries(condition, map_node_eles):
	first_node = None
	last_node = None
	def _err_bnd(nstr):
		return (_err(condition.XObject,
			("Found more than 1 {}-node.\n"
			"This can happen if the edges forming the wire of your path are:\n"
			"   1) not connected to each other, or\n"
			"   2) have opposite directions (local x axis)").format(nstr)))
	for nid, connected_elements in map_node_eles.items():
		if len(connected_elements) == 1:
			ele = connected_elements[0]
			if nid == ele.nodes[0].id:
				if first_node:
					raise Exception(_err_bnd('start'))
				first_node = ele.nodes[0]
			elif nid == ele.nodes[1].id:
				if last_node:
					raise Exception(_err_bnd('end'))
				last_node = ele.nodes[1]
	if first_node is None or last_node is None:
		raise Exception(_err(condition.XObject,
		"Cannot find first and last node of the path.\n"
		"Make sure the path does not form a closed loop."))
	return (first_node, last_node)

def _buildPath(condition, first_node, last_node, map_node_eles):
	nodes = [first_node]
	positions = [0.0]
	current_position = 0.0
	current_node = first_node
	connected_elements = map_node_eles[current_node.id]
	while True:
		next_node = None
		for ele in connected_elements:
			if ele.nodes[0].id == current_node.id:
				next_node = ele.nodes[1]
		if next_node is None:
			raise Exception(_err(condition.XObject, "Cannot find next node"))
		distance = (next_node.position - current_node.position).norm()
		current_node = next_node
		current_position += distance
		connected_elements = map_node_eles[current_node.id]
		nodes.append(current_node)
		positions.append(current_position)
		if current_node.id == last_node.id:
			break
	return (nodes, positions)

def _writeTclList(pinfo, lname, values, fmt, nmax=10):
	pinfo.out_file.write('{}set {} [list '.format(pinfo.indent, lname))
	count = nmax
	for i in values:
		count += 1
		if count > nmax:
			pinfo.out_file.write('\\\n{}{}'.format(pinfo.indent, pinfo.tabIndent))
			count = 1
		pinfo.out_file.write(fmt.format(i))
	pinfo.out_file.write(']\n')
def _writeTclVar(pinfo, lname, value, fmt):
	pinfo.out_file.write('{}set {} {}\n'.format(pinfo.indent, lname, fmt.format(value)))

class _writeTclCounter:
	processed = []
def writeTcl_MovingLoad(pinfo, condition, var_pat_ts):
	
	# check unique utilization
	if condition.id in _writeTclCounter.processed:
		raise Exception(_err(condition.XObject, "This condition cannot be used in multiple patterns. Please create copies of this condition"))
	_writeTclCounter.processed.append(condition.id)
	
	# the document
	doc = App.caeDocument()
	
	# the xobj
	xobj = condition.XObject
	
	# write a begin-description
	pinfo.out_file.write('\n{}# Condition: {} {} [{}]\n'.format(
		pinfo.indent, xobj.Xnamespace, xobj.name, condition.id))
	
	# attributes for 1 vehicle
	ap = _geta(xobj, 'Axle positions').quantityVector.value
	am = _geta(xobj, 'Axle masses').quantityVector.value
	vel = _geta(xobj, 'Velocity').quantityScalar.value
	per = _geta(xobj, 'Period').quantityScalar.value
	t0 = _geta(xobj, 'Start time').quantityScalar.value
	g = _geta(xobj, 'Gravity acceleration').quantityScalar.value
	
	# check values
	if len(ap) == 0:
		raise Exception(_err(condition.XObject, "Empty axle position list"))
	if len(ap) != len(am):
		raise Exception(_err(condition.XObject, "axle position and mass lists have different sizes"))
	# @todo
	
	# make sure ap is centered
	ac = (ap[len(ap)-1]+ap[0])/2.0
	ap = [i-ac for i in ap]
	af = [-i*g for i in am]
	
	# map node to elements
	map_node_eles = _mapNodesToElements(doc, condition)
	
	# find boundaries
	first_node, last_node = _findPathBoundaries(condition, map_node_eles)
	
	# build path positions with distances
	path_nodes, path_positions = _buildPath(condition, first_node, last_node, map_node_eles)
	
	# if we are in a partitioned model we also need a vector of process ids
	path_partitions = [doc.mesh.partitionData.nodePartition(node.id) for node in path_nodes]
	
	# build ndf per nodes
	path_ndf = [pinfo.node_to_model_map[inode.id][1] for inode in path_nodes]
	
	# the prefix for variables local to this condition
	var_prefix = 'STKO_ML_{}_'.format(condition.id)
	var_path_nodes = var_prefix + 'path_nodes'
	var_path_nodes_ndf = var_prefix + 'path_nodes_ndf'
	var_path_positions = var_prefix + 'path_positions'
	var_path_partitions = var_prefix + 'path_nodes_pid'
	var_axle_positions = var_prefix + 'axle_positions'
	var_axle_masses = var_prefix + 'axle_masses'
	var_axle_forces = var_prefix + 'axle_forces'
	var_pattern = var_prefix + 'pattern'
	var_modified_nodes = var_prefix + 'modified_nodes'
	var_function_before = var_prefix + 'function_before'
	var_function_after = var_prefix + 'function_after'
	
	# write them
	pinfo.out_file.write('{0}#\n{0}# variables for path data\n'.format(pinfo.indent))
	_writeTclList(pinfo, var_path_nodes, [node.id for node in path_nodes], '{} ')
	_writeTclList(pinfo, var_path_positions, path_positions, '{:.10g} ')
	_writeTclList(pinfo, var_path_partitions, path_partitions, '{} ')
	_writeTclList(pinfo, var_path_nodes_ndf, path_ndf, '{} ')
	_writeTclList(pinfo, var_axle_positions, ap, '{:.10g} ')
	_writeTclList(pinfo, var_axle_masses, am, '{:.10g} ')
	_writeTclList(pinfo, var_axle_forces, af, '{:.10g} ')
	pat_tag = pinfo.next_analysis_step_id
	pinfo.next_analysis_step_id += 1
	pinfo.out_file.write('{}set {} {}\n'.format(pinfo.indent, var_pattern, pat_tag))
	pinfo.out_file.write('{}pattern Plain ${} ${} {{}}\n'.format(pinfo.indent, var_pattern, var_pat_ts))
	pinfo.out_file.write('{}set {} [list]\n'.format(pinfo.indent, var_modified_nodes))
	
	# make the function
	pinfo.out_file.write('{0}#\n{0}# custom function for the moving load\n'.format(pinfo.indent))
	this_dir = os.path.dirname(__file__)
	with open('{}/MovingLoadFunctionTemplate.tcl'.format(this_dir), 'r') as f:
		for line in f.read().splitlines():
			line = (line
				.replace('__function_before__', var_function_before)
				.replace('__function_after__', var_function_after)
				.replace('__pattern__', var_pattern)
				.replace('__ts__', var_pat_ts)
				.replace('__path_nodes__', var_path_nodes)
				.replace('__path_nodes_ndf__', var_path_nodes_ndf)
				.replace('__path_partitions__', var_path_partitions)
				.replace('__path_positions__', var_path_positions)
				.replace('__axle_positions__', var_axle_positions)
				.replace('__axle_masses__', var_axle_masses)
				.replace('__axle_forces__', var_axle_forces)
				.replace('__modified_nodes__', var_modified_nodes)
				.replace('__velocity__', '{:.10g}'.format(vel))
				.replace('__period__', '{:.10g}'.format(per))
				.replace('__t0__', '{:.10g}'.format(t0))
				)
			pinfo.out_file.write(pinfo.indent)
			pinfo.out_file.write(line)
			pinfo.out_file.write('\n')
	#pinfo.out_file.write('for {set xxx 0} {$xxx < 100} {incr xxx} {\n')
	pinfo.out_file.write('{}lappend STKO_VAR_OnBeforeAnalyze_CustomFunctions {}\n'.format(pinfo.indent, var_function_before))
	pinfo.out_file.write('{}lappend STKO_VAR_OnAfterAnalyze_CustomFunctions {}\n'.format(pinfo.indent, var_function_after))
	#pinfo.out_file.write('}\n')