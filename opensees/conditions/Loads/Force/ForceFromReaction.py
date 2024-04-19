import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Fx
	at_Fx = MpcAttributeMetaData()
	at_Fx.type = MpcAttributeType.Boolean
	at_Fx.name = 'Fx'
	at_Fx.group = 'dof'
	at_Fx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fx')+'<br/>') + 
		html_par('load node_id [nodeReaction node_id 1]') +
		html_end()
		)
	at_Fx.setDefault(True)
	
	# Uy
	at_Fy = MpcAttributeMetaData()
	at_Fy.type = MpcAttributeType.Boolean
	at_Fy.name = 'Fy'
	at_Fy.group = 'dof'
	at_Fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fy')+'<br/>') + 
		html_par('load node_id [nodeReaction node_id 2]') +
		html_end()
		)
	at_Fy.setDefault(True)
	
	# Uz
	at_Fz = MpcAttributeMetaData()
	at_Fz.type = MpcAttributeType.Boolean
	at_Fz.name = 'Fz'
	at_Fz.group = 'dof'
	at_Fz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fz')+'<br/>') + 
		html_par('load node_id [nodeReaction node_id 3]') +
		html_end()
		)
	at_Fz.setDefault(True)
	
	# Rx
	at_Rx = MpcAttributeMetaData()
	at_Rx.type = MpcAttributeType.Boolean
	at_Rx.name = 'Rx'
	at_Rx.group = 'dof'
	at_Rx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rx')+'<br/>') + 
		html_par('load node_id [nodeReaction node_id 4]') +
		html_end()
		)
	at_Rx.setDefault(True)
	
	# Ry
	at_Ry = MpcAttributeMetaData()
	at_Ry.type = MpcAttributeType.Boolean
	at_Ry.name = 'Ry'
	at_Ry.group = 'dof'
	at_Ry.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ry')+'<br/>') + 
		html_par('load node_id [nodeReaction node_id 5]') +
		html_end()
		)
	at_Ry.setDefault(True)
	
	# Rz_3D
	at_Rz = MpcAttributeMetaData()
	at_Rz.type = MpcAttributeType.Boolean
	at_Rz.name = 'Rz'
	at_Rz.group = 'dof'
	at_Rz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rz')+'<br/>') + 
		html_par('for model ndm 2') +
		html_par('load node_id [nodeReaction node_id 3]') +
		html_par('for model ndm 3') +
		html_par('load node_id [nodeReaction node_id 6]') +
		html_end()
		)
	at_Rz.setDefault(True)
	
	# ctype
	# at_ctype = MpcAttributeMetaData()
	# at_ctype.type = MpcAttributeType.Integer
	# at_ctype.visible = False;
	# at_ctype.editable = False;
	# at_ctype.name = 'ctype_constraint'
	# at_ctype.group = 'Constraint'
	# at_ctype.description = (
		# html_par(html_begin()) +
		# html_par(html_boldtext('ctype')+'<br/>') + 
		# html_par('ctype') +
		# html_end()
		# )
	
	xom = MpcXObjectMetaData()
	xom.name = 'ForceFromReaction'
	
	xom.addAttribute(at_Fx)
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_Fz)
	xom.addAttribute(at_Rx)
	xom.addAttribute(at_Ry)
	xom.addAttribute(at_Rz)
	# xom.addAttribute(at_ctype)
	
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
	d.on_vertices = True
	d.on_edges = True
	d.on_faces = True
	d.on_solids = True
	d.on_interactions = False
	
	return d

def __process_load (pinfo, i, Fx, Fy, Fz, Rx, Ry, Rz):
	
	strFx = ' 0.0'
	strFy = ' 0.0'
	strFz = ' 0.0'
	strRx = ' 0.0'
	strRy = ' 0.0'
	strRz = ' 0.0'
	
	model_info = pinfo.node_to_model_map[i]
	ndm = model_info[0]
	ndf = model_info[1]
	
	if Fx:
		strFx = (' {} {} {}').format('[nodeReaction' , i, '1]')
	if Fy:
		strFy = (' {} {} {}').format('[nodeReaction' , i, '2]')
	if Fz:
		strFz = (' {} {} {}').format('[nodeReaction' , i, '3]')
	if Rx:
		strRx = (' {} {} {}').format('[nodeReaction' , i, '4]')
	if Ry:
		strRy = (' {} {} {}').format('[nodeReaction' , i, '5]')
	if Rz:
		if (ndm == 2):
			strRz = (' {} {} {}').format('[nodeReaction' , i, '3]')
		else:
			strRz = (' {} {} {}').format('[nodeReaction' , i, '6]')
	
	if (ndm == 2):
		if ndf == 2:
			pinfo.out_file.write('{}{}load {}{}{}\n'.format(pinfo.indent, pinfo.tabIndent, i, strFx, strFy))
		if ndf == 3:
			pinfo.out_file.write('{}{}load {}{}{}{}\n'.format(pinfo.indent, pinfo.tabIndent, i, strFx, strFy, strRz))
	if (ndm == 3):
		if ndf == 3:
			pinfo.out_file.write('{}{}load {}{}{}{}\n'.format(pinfo.indent, pinfo.tabIndent, i, strFx, strFy, strFz))
		if ndf == 4:
			pinfo.out_file.write('{}{}load {}{}{}{}{}\n'.format(pinfo.indent, pinfo.tabIndent, i, strFx, strFy, strFz, strRx))
		if ndf == 6:
			pinfo.out_file.write('{}{}load {}{}{}{}{}{}{}\n'.format(pinfo.indent, pinfo.tabIndent, i, strFx, strFy, strFz, strRx, strRy, strRz))

def writeTcl_Force(pinfo, xobj):
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	elem = pinfo.elem
	
	Fx_at = xobj.getAttribute('Fx')
	if(Fx_at is None):
		raise Exception('Error: cannot find "Fx" attribute')
	Fx = Fx_at.boolean
	
	Fy_at = xobj.getAttribute('Fy')
	if(Fy_at is None):
		raise Exception('Error: cannot find "Fy" attribute')
	Fy = Fy_at.boolean
	
	Fz_at = xobj.getAttribute('Fz')
	if(Fz_at is None):
		raise Exception('Error: cannot find "Fz" attribute')
	Fz = Fz_at.boolean
	
	Rx_at = xobj.getAttribute('Rx')
	if(Rx_at is None):
		raise Exception('Error: cannot find "Rx" attribute')
	Rx = Rx_at.boolean
	
	Ry_at = xobj.getAttribute('Ry')
	if(Ry_at is None):
		raise Exception('Error: cannot find "Ry" attribute')
	Ry = Ry_at.boolean
	
	Rz_at = xobj.getAttribute('Rz')
	if(Rz_at is None):
		raise Exception('Error: cannot find "Rz" attribute')
	Rz = Rz_at.boolean
	
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	node_id = []
	for geom, subset in all_geom.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		for i in subset.faces:
			domain = mesh_of_geom.faces[i]
			for elem in domain.elements:
				n = len(elem.nodes)
				for i in range(n):
					node_id.append(elem.nodes[i].id)
		for i in subset.edges:
			domain = mesh_of_geom.edges[i]
			for elem in domain.elements:
				n = len(elem.nodes)
				for i in range(n):
					node_id.append(elem.nodes[i].id)
		for i in subset.vertices:
			domain = mesh_of_geom.vertices[i]
			node_id.append(domain.id)
		for i in subset.solids:
			domain = mesh_of_geom.solids[i]
			for elem in domain.elements:
				n = len(elem.nodes)
				for i in range(n):
					node_id.append(elem.nodes[i].id)
	node_id = list(set(node_id))
	
	pinfo.out_file.write('reactions\n')
	
	if pinfo.process_count > 1:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			first_done = False
			for i in node_id:
				# if doc.mesh.partitionData.nodePartition(i) != process_id:
					# continue
				if not doc.mesh.partitionData.isNodeOnPartition(i, process_id):
					continue
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
					first_done = True
				__process_load (pinfo, i, Fx, Fy, Fz, Rx, Ry, Rz)
			if first_done:
				process_block_count += 1
			if process_block_count > 0 and first_done:
				pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
	else:
		for i in node_id:
			__process_load(pinfo, i, Fx, Fy, Fz, Rx, Ry, Rz)
