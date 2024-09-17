import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def _err(msg):
	return 'Error in AutoEdgeMass: {}'.format(msg)

def makeXObjectMetaData():
	
	def mka(name, type, descr, group = 'Default', dim = None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext('name')+'<br/>') +
			html_par(descr) +
			html_end()
			)
		if dim:
			a.dimension = dim
		return a
	
	rho = mka('rho', MpcAttributeType.QuantityScalar,
		descr = (
		'Mass density (mass per unit volume).<br/>'
		'This condition will automatically obtain the cross-section area from the assigned properties.<br/>'
		'Note that only some physical properties provide a cross-section area (Elastic, Fiber, RectangularFiberSection)'),
		group = 'Mass'
		)
	
	toload = mka('Convert to load', MpcAttributeType.Boolean,
		descr = (
		'If True, you can also use this condition in a load pattern to convert this density to a self-weight.<br/>'
		'In the load pattern, you can put it either under "load" to convert it to equivalent nodal loads, or under "eleLoad" to convert it to distributed beam loads.'),
		group = 'Load'
		)
	gx = mka('gx', MpcAttributeType.QuantityScalar,
		descr = 'Component of the gravity acceleration vector in global X direction',
		group = 'Load'
		)
	gy = mka('gy', MpcAttributeType.QuantityScalar,
		descr = 'Component of the gravity acceleration vector in global Y direction',
		group = 'Load'
		)
	gz = mka('gz', MpcAttributeType.QuantityScalar,
		descr = 'Component of the gravity acceleration vector in global Z direction',
		group = 'Load'
		)
	gz.setDefault(-9.81)
	
	type = mka('Type', MpcAttributeType.String,
		descr = (
		'The load type:'
		'<ul>'
		'  <li><b>load</b>: convert to equivalent nodal loads</li>'
		'  <li><b>eleLoad</b>: convert to distributed beam loads</li>'
		'</ul>'),
		group = 'Load'
		)
	type.sourceType = MpcAttributeSourceType.List
	type.setSourceList(['load', 'eleLoad'])
	type.setDefault('load')
	
	xom = MpcXObjectMetaData()
	xom.name = 'AutoEdgeMass'
	xom.addAttribute(rho)
	xom.addAttribute(toload)
	xom.addAttribute(gx)
	xom.addAttribute(gy)
	xom.addAttribute(gz)
	xom.addAttribute(type)
	
	return xom

def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Points
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = True
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = False
	return d

def _check_visibility(xobj):
	b = xobj.getAttribute('Convert to load').boolean
	xobj.getAttribute('gx').visible = b
	xobj.getAttribute('gy').visible = b
	xobj.getAttribute('gz').visible = b
	xobj.getAttribute('Type').visible = b

def onEditBegin(editor, xobj):
	_check_visibility(xobj)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name == 'Convert to load':
		_check_visibility(xobj)

# An internal function to get the cross section
# area from known properties.
# It returns 0 if none of the referenced properties has
# an area.
# Otherwise, it returns the average of the areas.
def _getCrossArea(prop):
	if prop is None:
		raise Exception(_err('No Physical property assigned'))
	if prop.XObject is None:
		raise Exception(_err('No XObject in physical property'))
	referenced = App.getReferencedComponents(prop)
	all_props = [prop]
	all_props.extend(referenced)
	A = 0.0
	N = 0.0
	for ip in all_props:
		xobj = ip.XObject
		if xobj.completeName == 'sections.Elastic':
			sec = xobj.getAttribute('Section').customObject
			A += sec.properties.area
			N += 1.0
		elif xobj.completeName == 'sections.Fiber':
			sec = xobj.getAttribute('Fiber section').customObject
			A += sec.toElasticSection().properties.area
			N += 1.0
		elif xobj.completeName == 'sections.RectangularFiberSection':
			A += xobj.getAttribute('Width').quantityScalar.value * xobj.getAttribute('Height').quantityScalar.value
			N += 1.0
	if N > 0.0:
		A = A/N
	return A

# The ele_callback function for nodal masses
class _massEleCallback:
	def callback(self, pinfo, elem, MA):
		n = len(elem.nodes)
		ngp = len(elem.integrationRule.integrationPoints)
		# obtain nodal values of the distributed condition
		nodal_values = [[0.0, 0.0, 0.0] for i in range(n)]
		for i in range(n):
			nodal_values[i][0] = MA
			nodal_values[i][1] = MA
			nodal_values[i][2] = MA
		# do nodal lumping
		nodal_lumped_values = [[0.0, 0.0, 0.0, 0.0] for i in range(n)]
		for gp in range(ngp):
			gauss_point = elem.integrationRule.integrationPoints[gp]
			N = elem.shapeFunctionsAt(gauss_point)
			det_J = elem.jacobianAt(gauss_point).det()
			W = gauss_point.w
			# interpolate nodal value at this gp
			fx = 0.0
			fy = 0.0
			fz = 0.0
			for i in range(n):
				Ni = N[i]
				fx += Ni * nodal_values[i][0]
				fy += Ni * nodal_values[i][1]
				fz += Ni * nodal_values[i][2]
			for i in range(n):
				fact = N[i] * det_J * W
				lump = nodal_lumped_values[i]
				lump[0] = elem.nodes[i].id
				lump[1] += fx * fact
				lump[2] += fy * fact
				lump[3] += fz * fact
		# assign lumped mass at nodes
		for i in range(n):
			lump = nodal_lumped_values[i]
			node_id = elem.nodes[i].id
			mass_value = [lump[1], lump[2], lump[3], 0.0, 0.0, 0.0]
			# accumulate to existing mass values
			if node_id in pinfo.mass_to_node_map:
				for j in range(len(pinfo.mass_to_node_map[node_id])):
					pinfo.mass_to_node_map[node_id][j]+= mass_value[j]
			else:
				pinfo.mass_to_node_map[node_id] = mass_value

# The ele_callback function for ele load
class _eleLoadEleCallback:
	def __init__(self, g):
		self.g = g
		self.is_partitioned = False
		self.process_id = 0
		self.process_block_count = 0
		self.first_done = False
	def callback(self, pinfo, elem, MA):
		# quick return
		if self.is_partitioned:
			if App.caeDocument().mesh.partitionData.elementPartition(elem.id) != self.process_id:
				return
		# force in global coordinates
		FT = self.g * MA
		# in global coordinates for the load
		WT = elem.orientation.quaternion.conjugate().rotate(FT)
		# parallel if-else block
		if self.is_partitioned :
			if not self.first_done:
				if self.process_block_count == 0:
					pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', self.process_id, '} {'))
				else:
					pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', self.process_id, '} {'))
				self.first_done = True
		# check dimension
		n1 = elem.nodes[0].id
		if not n1 in pinfo.node_to_model_map:
			raise Exception(_err('node without assigned element'))
		spatial_info = pinfo.node_to_model_map[n1]
		node_ndm = spatial_info[0]
		if node_ndm == 2:
			# 2D
			pinfo.out_file.write('{}eleLoad -ele {} -type -beamUniform {} {} {}\n'.format(pinfo.indent, elem.id, WT.y, WT.x))
		elif node_ndm == 3:
			# 3D
			pinfo.out_file.write('{}eleLoad -ele {} -type -beamUniform {} {} {}\n'.format(pinfo.indent, elem.id, WT.y, WT.z, WT.x))
		else:
			raise Exception(_err('invalid NMD {}'.format(node_ndm)))

# The ele_callback function for load
class _loadEleCallback:
	def __init__(self, g):
		self.g = g
		self.is_partitioned = False
		self.process_id = 0
		self.process_block_count = 0
		self.first_done = False
	def callback(self, pinfo, elem, MA):
		# quick return
		if self.is_partitioned:
			if App.caeDocument().mesh.partitionData.elementPartition(elem.id) != self.process_id:
				return
		# size
		n = len(elem.nodes)
		ngp = len(elem.integrationRule.integrationPoints)
		# force
		FT = self.g * MA
		# obtain nodal values of the distributed condition
		nodal_values = [[0.0, 0.0, 0.0] for i in range(n)]
		for i in range(n):
			nodal_values[i][0] = FT.x
			nodal_values[i][1] = FT.y
			nodal_values[i][2] = FT.z
		# do nodal lumping
		nodal_lumped_values = [[0.0, 0.0, 0.0, 0.0] for i in range(n)]
		for gp in range(ngp):
			gauss_point = elem.integrationRule.integrationPoints[gp]
			N = elem.shapeFunctionsAt(gauss_point)
			det_J = elem.jacobianAt(gauss_point).det()
			W = gauss_point.w
			# interpolate nodal value at this gp
			fx = 0.0
			fy = 0.0
			fz = 0.0
			for i in range(n):
				Ni = N[i]
				fx += Ni * nodal_values[i][0]
				fy += Ni * nodal_values[i][1]
				fz += Ni * nodal_values[i][2]
			for i in range(n):
				fact = N[i] * det_J * W
				lump = nodal_lumped_values[i]
				lump[0] = elem.nodes[i].id
				lump[1] += fx * fact
				lump[2] += fy * fact
				lump[3] += fz * fact
		# assign lumped mass at nodes
		for i in range(n):
			lump = nodal_lumped_values[i]
			lump[0] = elem.nodes[i].id
			if (lump[0] in pinfo.node_to_model_map):
				# parallel if-else block
				if self.is_partitioned :
					if not self.first_done:
						if self.process_block_count == 0:
							pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', self.process_id, '} {'))
						else:
							pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', self.process_id, '} {'))
						self.first_done = True
				# check spatial info
				spatial_info = pinfo.node_to_model_map[lump[0]]
				node_ndm = spatial_info[0]
				node_ndf = spatial_info[1]
				# build force string
				fstring = None
				if (node_ndm == 2):
					if (node_ndf == 3) or (node_ndf == 33):
						fstring = '{} {} 0.0'.format(lump[1], lump[2])
					else:
						fstring = '{} {}'.format(lump[1], lump[2])
				else:
					if (node_ndf == 3):
						fstring = '{} {} {}'.format(lump[1], lump[2], lump[3])
					elif (node_ndf == 4):
						fstring = '{} {} {} 0.0'.format(lump[1], lump[2], lump[3])
					elif (node_ndf == 6):
						fstring = '{} {} {} 0.0 0.0 0.0'.format(lump[1], lump[2], lump[3])
				if fstring is None:
					raise Exception(_err('NDM {} - NDF {} not supported'.format(node_ndm, node_ndf)))
				# write
				pinfo.out_file.write('{}{}load {} {}\n'.format(pinfo.indent, pinfo.tabIndent, lump[0] , fstring))
			else :
				raise Exception(_err('node without assigned element'))

# The common internal main function
def _internalMainFunction(pinfo, rho, ele_callback):
	# document
	doc = App.caeDocument()
	# geometries
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	# parse all geometries
	for geom, subset in all_geom.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		pasn = geom.physicalPropertyAssignment
		# parse all edges
		for i in subset.edges:
			domain = mesh_of_geom.edges[i]
			# get cross sectional area from property
			prop = pasn.onEdges[i]
			A = _getCrossArea(prop)
			MA = rho*A
			# process all elements
			for elem in domain.elements:
				ele_callback(pinfo, elem, MA)

# The Interface function for Mass
def fillNodeMassMap(pinfo):
	xobj = pinfo.condition.XObject
	rho = xobj.getAttribute('rho').quantityScalar.value
	_internalMainFunction(pinfo, rho, _massEleCallback().callback)

# The Interface function for Load
def convertToLoad(pinfo, xobj):
	# quick return
	toload = xobj.getAttribute('Convert to load').boolean
	if not toload:
		return None
	# get args
	rho = xobj.getAttribute('rho').quantityScalar.value
	gx = xobj.getAttribute('gx').quantityScalar.value
	gy = xobj.getAttribute('gy').quantityScalar.value
	gz = xobj.getAttribute('gz').quantityScalar.value
	g = Math.vec3(gx, gy, gz)
	type = xobj.getAttribute('Type').string
	# create callback object
	if type == 'eleLoad':
		cobj = _eleLoadEleCallback(g)
	else:
		cobj = _loadEleCallback(g)
	# check parallel
	if pinfo.process_count > 1:
		cobj.is_partitioned = True
	if cobj.is_partitioned:
		for process_id in range(pinfo.process_count):
			# per process call (to minimize the number of process if-else statements...
			cobj.process_id = process_id
			cobj.first_done = False
			_internalMainFunction(pinfo, rho, cobj.callback)
			# finalize this process
			if cobj.first_done:
				cobj.process_block_count += 1
			if cobj.process_block_count > 0 and cobj.first_done:
				pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
	else :
		# simple call
		_internalMainFunction(pinfo, rho, cobj.callback)