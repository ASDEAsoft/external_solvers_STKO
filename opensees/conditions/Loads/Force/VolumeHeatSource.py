import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *
from opensees.conditions.utils import SpatialFunctionEval

def makeXObjectMetaData():
	'''
	fill the 3d vector data. set the pressure value
	at the z component, since the orientation is set to local
	'''
	
	# Mode
	at_Mode = MpcAttributeMetaData()
	at_Mode.type = MpcAttributeType.String
	at_Mode.name = 'Mode'
	at_Mode.group = 'Group'
	at_Mode.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') +
		html_par('choose between "constant" and "function"') +
		html_end()
		)
	at_Mode.sourceType = MpcAttributeSourceType.List
	at_Mode.setSourceList(['constant', 'function'])
	at_Mode.setDefault('constant')
	
	# constant
	at_constant = MpcAttributeMetaData()
	at_constant.type = MpcAttributeType.Boolean
	at_constant.name = 'constant'
	at_constant.group = 'Data'
	at_constant.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('constant')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_constant.editable = False
	
	# function
	at_function = MpcAttributeMetaData()
	at_function.type = MpcAttributeType.Boolean
	at_function.name = 'function'
	at_function.group = 'Data'
	at_function.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('function')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_function.editable = False
	
	# Q
	at_Q = MpcAttributeMetaData()
	at_Q.type = MpcAttributeType.QuantityScalar
	at_Q.name = 'Q'
	at_Q.group = 'Data'
	at_Q.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Q')+'<br/>') + 
		html_par('The Heat Source') +
		html_end()
		)
	at_Q.setDefault(1.0)
	
	# Qf
	at_Qf = MpcAttributeMetaData()
	at_Qf.type = MpcAttributeType.String
	at_Qf.name = 'Qf'
	at_Qf.group = 'Data'
	at_Qf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Qf')+'<br/>') + 
		html_par('f(x) e.g.:') +
		html_par('(x**2+y**2)**0.5') +
		html_end()
		)
	at_Qf.setDefault('0')
	
	xom = MpcXObjectMetaData()
	xom.name = 'VolumeHeatSource'
	xom.addAttribute(at_Mode)
	xom.addAttribute(at_constant)
	xom.addAttribute(at_function)
	xom.addAttribute(at_Q)
	xom.addAttribute(at_Qf)
	
	# visibility dependencies
	
	# constant-dep
	xom.setVisibilityDependency(at_constant, at_Q)
	
	# function-dep
	xom.setVisibilityDependency(at_function, at_Qf)

	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(at_Mode, at_constant)
	xom.setBooleanAutoExclusiveDependency(at_Mode, at_function)
	
	return xom


def fillConditionRepresentationData(xobj, pos, data):
	'''
	Fills the 3D vector data.
	
	Set the pressure value
	at the z component, since the orientation is set to local
	'''
	Q = xobj.getAttribute('Q').quantityScalar.value
	Mode = xobj.getAttribute('Mode').string
	
	sQf = xobj.getAttribute('Qf').string
	
	if (Mode == 'function'):
		seval = SpatialFunctionEval(pos)
		dx = seval.make(sQf)		#spatial function Q
		data[0] = dx
	
	else:
		data[0] = Q

def makeConditionRepresentationData(xobj):
	'''
	Create the condition representation data for STKO.
	Here we want an arrow (vector) representation in local
	coordinate system, that can be applied only on faces.
	We need to allocate a 3d vector for the data attribute.
	The components of this vector will be set using
	@ref fillConditionRepresentationData
	'''
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Arrows
	
	d.data = Math.double_array([0.0])
	d.on_vertices = False
	d.on_edges = False
	d.on_faces = False
	d.on_solids = True
	d.on_interactions = False
	return d

def __process_load (doc, pinfo, all_geom, Mode, Q, is_partitioned, process_id, process_block_count, sQf):
	first_done = False
	for geom, subset in all_geom.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		for i in subset.solids:
			domain = mesh_of_geom.solids[i]
			for elem in domain.elements:
			
				if is_partitioned :
					if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
						continue
			
				n = len(elem.nodes)
				ngp = len(elem.integrationRule.integrationPoints)
					
				#elem_ = elem.nodes[:]
				#elem_[8], elem_[9] = elem_[9], elem_[8]

				# obtain nodal values of the distributed condition
				nodal_values = [[0.0] for i in range(n)]
				if Mode == 'function':
					for i in range(n):
						nodei = elem.nodes[i]
						seval = SpatialFunctionEval(nodei.position)
						nodal_values[i][0] = seval.make(sQf)
				else:
					for i in range(n):
						nodal_values[i][0] = Q
				
				# do nodal lumping
				nodal_lumped_values = [[0.0, 0.0] for i in range(n)]
				for gp in range(ngp):
					gauss_point = elem.integrationRule.integrationPoints[gp]
					N = elem.shapeFunctionsAt(gauss_point)
					det_J = elem.jacobianAt(gauss_point).det()
					W = gauss_point.w
					
					# interpolate nodal value at this gp
					qf = 0.0
					for i in range(n):
						Ni = N[i]
						qf += Ni * nodal_values[i][0]
					
					for i in range(n):
						# fact = N[i] * det_J * W
						fact = N[i] * det_J * W * 6
						lump = nodal_lumped_values[i]
						lump[0] = elem.nodes[i].id
						lump[1] += qf * fact
				
				for i in range(n):
					lump = nodal_lumped_values[i]
					str_tcl = []
					
					if (lump[0] in pinfo.node_to_model_map):
					
						if is_partitioned :
							if not first_done:
								if process_block_count == 0:
									pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
								else:
									pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
								first_done = True
					
						spatial_info = pinfo.node_to_model_map[lump[0]]
						node_ndm = spatial_info[0]
						node_ndf = spatial_info[1]
					else :
						raise Exception('Error: node without assigned element')
					str_tcl.append('{}load {} {}'.format(pinfo.indent, lump[0], lump[1]))
					# now write the string into the file
					pinfo.out_file.write('\n'.join(str_tcl))
					pinfo.out_file.write('\n')
					
	if is_partitioned :
		if first_done:
			process_block_count += 1
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count

def writeTcl_Force(pinfo, xobj):
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	
	Mode_at = xobj.getAttribute('Mode')
	if(Mode_at is None):
		raise Exception('Error: cannot find "Mode" attribute')
	Mode = Mode_at.string
	
	Q_at = xobj.getAttribute('Q')
	if(Q_at is None):
		raise Exception('Error: cannot find "Q" attribute')
	Q = Q_at.quantityScalar.value
	
	Qf_at = xobj.getAttribute('Qf')
	if(Qf_at is None):
		raise Exception('Error: cannot find "Qf" attribute')
	Qf = Qf_at.string

	sQf = 0
	
	if (Mode == 'function'):
		sfx = Qf
	
	doc = App.caeDocument()
	
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			process_block_count = __process_load (doc, pinfo, all_geom, Mode, Q, is_partitioned, process_id, process_block_count, sQf)
	else :
		__process_load (doc, pinfo, all_geom, Mode, Q, is_partitioned, 0, 0, sQf)