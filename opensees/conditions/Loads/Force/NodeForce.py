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
	
	# F
	at_F = MpcAttributeMetaData()
	at_F.type = MpcAttributeType.QuantityVector3
	at_F.name = 'F'
	at_F.group = 'Data'
	at_F.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('F')+'<br/>') + 
		html_par('The 3d force vector') +
		html_end()
		)
	at_F.dimension = u.F/u.L**2
	
	# Fx
	at_Fx = MpcAttributeMetaData()
	at_Fx.type = MpcAttributeType.String
	at_Fx.name = 'Fx'
	at_Fx.group = 'Data'
	at_Fx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fx')+'<br/>') + 
		html_par('f(x) e.g.:') +
		html_par('(x**2+y**2)**0.5') +
		html_end()
		)
	at_Fx.setDefault('0')
	
	# Fy
	at_Fy = MpcAttributeMetaData()
	at_Fy.type = MpcAttributeType.String
	at_Fy.name = 'Fy'
	at_Fy.group = 'Data'
	at_Fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fy')+'<br/>') + 
		html_par('f(y) e.g.:') +
		html_par('(y**2+y**2)**0.5') +
		html_end()
		)
	at_Fy.setDefault('0')
	
	# Fz
	at_Fz = MpcAttributeMetaData()
	at_Fz.type = MpcAttributeType.String
	at_Fz.name = 'Fz'
	at_Fz.group = 'Data'
	at_Fz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fz')+'<br/>') + 
		html_par('f(z) e.g.:') +
		html_par('(z**2+y**2)**0.5') +
		html_end()
		)
	at_Fz.setDefault('0')
	
	xom = MpcXObjectMetaData()
	xom.name = 'NodeForce'
	xom.addAttribute(at_Mode)
	xom.addAttribute(at_constant)
	xom.addAttribute(at_function)
	xom.addAttribute(at_F)
	xom.addAttribute(at_Fx)
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_Fz)
	# visibility dependencies
	
	# constant-dep
	xom.setVisibilityDependency(at_constant, at_F)
	
	# function-dep
	xom.setVisibilityDependency(at_function, at_Fx)
	xom.setVisibilityDependency(at_function, at_Fy)
	xom.setVisibilityDependency(at_function, at_Fz)
	
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
	F = xobj.getAttribute('F').quantityVector3.value
	Mode = xobj.getAttribute('Mode').string
	
	sfx = Fx_at = xobj.getAttribute('Fx').string
	sfy = Fy_at = xobj.getAttribute('Fy').string
	sfz = Fz_at = xobj.getAttribute('Fz').string
	
	if (Mode == 'function'):
		
		seval = SpatialFunctionEval(pos)
		
		dx = seval.make(sfx)		#spatial function x
		dy = seval.make(sfy)		#spatial function y
		dz = seval.make(sfz)		#spatial function z
		
		data[0] = dx
		data[1] = dy
		data[2] = dz
	
	else:
		data[0] = F.x
		data[1] = F.y
		data[2] = F.z

def makeConditionRepresentationData(xobj):
	'''
	Create the condition representation data for STKO.
	Here we want an arrow (vector) representation in global
	coordinate system, that can be applied only on faces.
	We need to allocate a 3d vector for the data attribute.
	The components of this vector will be set using
	@ref fillConditionRepresentationData
	'''
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Arrows
	d.orientation = MpcConditionVRepOrientation.Global
	
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = True
	d.on_edges = False
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = False
	return d

def __process_load (pinfo, domain, Mode, F, node_id, sfx, sfy, sfz):
	
	if (Mode == 'function'):
		seval = SpatialFunctionEval(domain)
		dx = seval.make(sfx)
		dy = seval.make(sfy)
		dz = seval.make(sfz)
	else:
		dx = F.x
		dy = F.y
		dz = F.z
	str_tcl = []
	sopt = '{} {}'.format(dx, dy)
	if (node_id in pinfo.node_to_model_map):
		spatial_info = pinfo.node_to_model_map[node_id]
		node_ndm = spatial_info[0]
		node_ndf = spatial_info[1]
		if (node_ndm == 2):
			if (node_ndf == 3):
				sopt += ' 0.0'
		else:
			sopt += ' {}'.format(dz)
			if (node_ndf == 4):
				sopt += ' 0.0'
			elif (node_ndf == 6):
					sopt += ' 0.0 0.0 0.0'
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
	
	F_at = xobj.getAttribute('F')
	if(F_at is None):
		raise Exception('Error: cannot find "F" attribute')
	F = F_at.quantityVector3.value
	
	Fx_at = xobj.getAttribute('Fx')
	if(Fx_at is None):
		raise Exception('Error: cannot find "Fx" attribute')
	Fx = Fx_at.string
	
	Fy_at = xobj.getAttribute('Fy')
	if(Fy_at is None):
		raise Exception('Error: cannot find "Fy" attribute')
	Fy = Fy_at.string
	
	Fz_at = xobj.getAttribute('Fz')
	if(Fz_at is None):
		raise Exception('Error: cannot find "Fz" attribute')
	Fz = Fz_at.string
	
	sfx = Fx
	sfy = Fy
	sfz = Fz
	
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
					__process_load (pinfo, domain, Mode, F, node_id, sfx, sfy, sfz)
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
					__process_load (pinfo, domain, Mode, F, node_id, sfx, sfy, sfz)