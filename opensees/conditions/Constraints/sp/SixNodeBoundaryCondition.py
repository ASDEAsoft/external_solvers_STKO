import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	def mka(name, type, group, descr, dval=None, dim=None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(descr) +
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/SixNodeBoundaryCondition.html','SixNodeBoundaryCondition')+'<br/>') +
			html_end()
			)
		if dval:
			a.setDefault(dval)
		if dim:
			a.dimension = dim
		return a
	
	betaS = mka('betaS', MpcAttributeType.QuantityScalar, 'Default', 'BetaS', dval = 0.0, dim = u.F/u.L**3)
	R = mka('R', MpcAttributeType.QuantityScalar, 'Default', 'Heat from the suns radiation absorbed by the concrete', dval = 0.0, dim = u.F/u.L**3)
	tamb = mka('tamb', MpcAttributeType.QuantityScalar, 'Default', 'Room temperature', dval = 20.0, dim = u.F/u.L**3)
	th = mka('th', MpcAttributeType.QuantityScalar, 'Default', 'Element thickness', dval = 1.0, dim = u.F/u.L**3)
	
	xom = MpcXObjectMetaData()
	xom.name = 'SixNodeBoundaryCondition'
	xom.addAttribute(betaS)
	xom.addAttribute(R)
	xom.addAttribute(tamb)
	xom.addAttribute(th)
	
	return xom

def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.ConstraintGlyph
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = False
	d.on_faces = True
	d.on_solids = False
	d.on_interactions = False
	return d

def getRequestedNodalSpatialDim(xobj):
	def _get_nodes(condition):
		doc = App.caeDocument()
		all_geom = condition.assignment.geometries
		nodes = []
		for geom, subset in all_geom.items():
			mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
			for i in subset.faces:
				domain = mesh_of_geom.faces[i]
				for elem in domain.elements:
					for node in elem.nodes:
						nodes.append(node.id)
		nodes = list(set(nodes))
		return nodes
	requested_node_dim_map = {}
	condition = xobj.parent
	nodes = _get_nodes(condition)
	for node_id in nodes:
		requested_node_dim_map[node_id] = (3, 1)
	return requested_node_dim_map

def writeTcl_spConstraints(pinfo):
	
	# element SixNodeBoundaryCondition eleTag? Node1? Node2? Node3? Node4? Node5? Node6? <$betaS $R $tamb $th>
	xobj = pinfo.condition.XObject
	
	# paramters
	def geta(name):
		a = xobj.getAttribute(name)
		if a is None:
			raise Exception('Error in SixNodeBoundaryCondition: cannot find "{}" attribute'.format(name))
		return a
	betaS = geta('betaS').quantityScalar.value
	R = geta('R').quantityScalar.value
	tamb = geta('tamb').quantityScalar.value
	th = geta('th').quantityScalar.value
	sopt = '{} {} {} {}'.format(betaS, R, tamb, th)
	
	# before writing all elements in this condition
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# get all elements and split by partition
	doc = App.caeDocument()
	all_geom = pinfo.condition.assignment.geometries
	if pinfo.process_count > 1:
		elements = [[] for i in range(pinfo.process_count)]
		for geom, subset in all_geom.items():
			mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
			for face_id in subset.faces:
				domain = mesh_of_geom.faces[face_id]
				for elem in domain.elements:
					# check
					if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Triangle or len(elem.nodes)!=6:
						raise Exception('Error: invalid type of element or number of nodes for SixNodeBoundaryCondition')
					elements[doc.mesh.partitionData.elementPartition(elem.id)].append(elem)
	else:
		elements = []
		for geom, subset in all_geom.items():
			mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
			for face_id in subset.faces:
				domain = mesh_of_geom.faces[face_id]
				for elem in domain.elements:
					# check
					if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Triangle or len(elem.nodes)!=6:
						raise Exception('Error: invalid type of element or number of nodes for SixNodeBoundaryCondition')
					elements.append(elem)
	
	def internal(current_indent, elements):
		# we already have checked the elements
		for elem in elements:
			nstr = ' '.join(str(node.id) for node in elem.nodes)
			str_tcl = '{}element SixNodeBoundryCondition {} {} {}\n'.format(current_indent, elem.id, nstr, sopt)
			pinfo.out_file.write(str_tcl)
	
	if pinfo.process_count > 1:
		for process_id in range(pinfo.process_count):
			process_elements = elements[process_id]
			if len(process_elements) > 0:
				pinfo.setProcessId(process_id)
				pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
				internal(pinfo.indent + pinfo.tabIndent, process_elements)
				pinfo.out_file.write('{}{}\n'.format(pinfo.indent, '}'))
	else:
		internal(pinfo.indent, elements)