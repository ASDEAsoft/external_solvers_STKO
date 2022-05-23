import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
from opensees.conditions.utils import SpatialFunctionEval

def makeXObjectMetaData():
	
	# Mode
	at_Mode = MpcAttributeMetaData()
	at_Mode.type = MpcAttributeType.String
	at_Mode.name = 'Mode'
	at_Mode.group = 'Group'
	at_Mode.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mode')+'<br/>') +
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
	
	# M
	at_M = MpcAttributeMetaData()
	at_M.type = MpcAttributeType.QuantityVector3
	at_M.name = 'M'
	at_M.group = 'Data'
	at_M.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('M')+'<br/>') + 
		html_par('The 3d couple vector') +
		html_end()
		)
	at_M.dimension = u.F * u.L
	
	# Mx
	at_Mx = MpcAttributeMetaData()
	at_Mx.type = MpcAttributeType.String
	at_Mx.name = 'Mx'
	at_Mx.group = 'Data'
	at_Mx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mx')+'<br/>') + 
		html_par('f(x) e.g.:') +
		html_par('(x**2+y**2)**0.5') +
		html_end()
		)
	at_Mx.setDefault('0')
	
	# My
	at_My = MpcAttributeMetaData()
	at_My.type = MpcAttributeType.String
	at_My.name = 'My'
	at_My.group = 'Data'
	at_My.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('My')+'<br/>') + 
		html_par('f(y) e.g.:') +
		html_par('(y**2+y**2)**0.5') +
		html_end()
		)
	at_My.setDefault('0')
	
	# Mz
	at_Mz = MpcAttributeMetaData()
	at_Mz.type = MpcAttributeType.String
	at_Mz.name = 'Mz'
	at_Mz.group = 'Data'
	at_Mz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mz')+'<br/>') + 
		html_par('f(z) e.g.:') +
		html_par('(z**2+y**2)**0.5') +
		html_end()
		)
	at_Mz.setDefault('0')
	
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Mass_Command','Mass Command')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'NodeCouple'
	xom.addAttribute(at_Mode)
	xom.addAttribute(at_constant)
	xom.addAttribute(at_function)
	xom.addAttribute(at_M)
	xom.addAttribute(at_Mx)
	xom.addAttribute(at_My)
	xom.addAttribute(at_Mz)
	xom.addAttribute(at_ctype)
	
	
	# constant-dep
	xom.setVisibilityDependency(at_constant, at_M)
	
	# function-dep
	xom.setVisibilityDependency(at_function, at_Mx)
	xom.setVisibilityDependency(at_function, at_My)
	xom.setVisibilityDependency(at_function, at_Mz)
	
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
	M = xobj.getAttribute('M').quantityVector3.value
	Mode = xobj.getAttribute('Mode').string
	
	sfx = xobj.getAttribute('Mx').string
	sfy = xobj.getAttribute('My').string
	sfz = xobj.getAttribute('Mz').string
	
	if (Mode == 'function'):
		
		seval = SpatialFunctionEval(pos)
		
		dx = seval.make(sfx)		#spatial function x
		dy = seval.make(sfy)		#spatial function y
		dz = seval.make(sfz)		#spatial function z
		
		data[0] = dx
		data[1] = dy
		data[2] = dz
	
	else:
		data[0] = M.x
		data[1] = M.y
		data[2] = M.z

def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.DoubleArrows
	d.orientation = MpcConditionVRepOrientation.Global
	
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = True
	d.on_edges = False
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = False
	
	return d

def __process_couple (pinfo, domain, ClassName, Mode, M, node_id, sfx, sfy, sfz):
	
	if (Mode == 'function'):
		seval = SpatialFunctionEval(domain)
		dx = seval.make(sfx)
		dy = seval.make(sfy)
		dz = seval.make(sfz)
	else:
		dx = M.x
		dy = M.y
		dz = M.z
	
	str_tcl = []
	
	if (node_id in pinfo.node_to_model_map):
		spatial_info = pinfo.node_to_model_map[node_id]
		node_ndm = spatial_info[0]
		node_ndf = spatial_info[1]
		if (node_ndm == 2):
			if (node_ndf == 3):
				sopt = ('\n'.join(['0.0 0.0 {}'.format(dz)]))
			else:
				# ndm: 2; ndf: 2
				raise Exception('Error: ndm/ndf pair is incompatible with "{}". node: {}; ndm: {}; ndf: {}'.format(ClassName, node_id, node_ndm, node_ndf))
		else:
			if (node_ndf == 6):
					sopt = ('\n'.join(['0.0 0.0 0.0 {} {} {}'.format(dx, dy, dz)]))
			else:
				# ndm: 3; ndf: 4 or ndm: 3; ndf: 6
				raise Exception('Error: ndm/ndf pair is incompatible with "{}". node: {}; ndm: {}; ndf: {}'.format(ClassName, node_id, node_ndm, node_ndf))
	else :
		raise Exception('Error: node without assigned element')
	
	# now write the string into the file
	str_tcl.append('{}{}load {} {}'.format(pinfo.indent, pinfo.tabIndent, node_id, sopt))
	pinfo.out_file.write('\n'.join(str_tcl))
	pinfo.out_file.write('\n')

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
	
	M_at = xobj.getAttribute('M')
	if(M_at is None):
		raise Exception('Error: cannot find "M" attribute')
	M = M_at.quantityVector3.value
	
	Mx_at = xobj.getAttribute('Mx')
	if(Mx_at is None):
		raise Exception('Error: cannot find "Mx" attribute')
	Mx = Mx_at.string
	
	My_at = xobj.getAttribute('My')
	if(My_at is None):
		raise Exception('Error: cannot find "My" attribute')
	My = My_at.string
	
	Mz_at = xobj.getAttribute('Mz')
	if(Mz_at is None):
		raise Exception('Error: cannot find "Mz" attribute')
	Mz = Mz_at.string
	
	sfx = 0
	sfy = 0
	sfz = 0
	
	if (Mode == 'function'):
		sfx = Mx
		sfy = My
		sfz = Mz
	
	doc = App.caeDocument()
	
	if pinfo.process_count > 1:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			first_done = False
			for geom, subset in all_geom.items():
				mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
				for i in subset.vertices:
					domain = mesh_of_geom.vertices[i]
					node_id = domain.id
					if doc.mesh.partitionData.nodePartition(node_id) != process_id:
						continue
					if not first_done:
						if process_block_count == 0:
							pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
						else:
							pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
						first_done = True
					__process_couple (pinfo, domain, ClassName, Mode, M, node_id, sfx, sfy, sfz)
				if first_done:
					process_block_count += 1
			if process_block_count > 0 and first_done:
				pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
	else:
		for geom, subset in all_geom.items():
				mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
				for i in subset.vertices:
					domain = mesh_of_geom.vertices[i]
					node_id = domain.id
					__process_couple (pinfo, domain, ClassName, Mode, M, node_id, sfx, sfy, sfz)