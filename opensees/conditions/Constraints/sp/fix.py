import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

class my_data:
	def __init__(self):
		# attributes will be set in the __control method
		pass

def makeXObjectMetaData():
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Constraint'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	# ModelType
	at_ModelType = MpcAttributeMetaData()
	at_ModelType.type = MpcAttributeType.String
	at_ModelType.name = 'ModelType'
	at_ModelType.group = 'Constraint'
	at_ModelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ModelType')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_ModelType.sourceType = MpcAttributeSourceType.List
	at_ModelType.setSourceList(['U (Displacement)', 'U-P (Displacement+Pressure)', 'U-R (Displacement+Rotation)'])
	at_ModelType.setDefault('U (Displacement)')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Constraint'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') + 
		html_par('Dx Constraint') +
		html_end()
		)
	at_2D.editable = False
	
	# 3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Constraint'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') + 
		html_par('Dx Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# D
	at_D = MpcAttributeMetaData()
	at_D.type = MpcAttributeType.Boolean
	at_D.name = 'U (Displacement)'
	at_D.group = 'Constraint'
	at_D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U (Displacement)')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	at_D.editable = False
	
	# UP
	at_UP = MpcAttributeMetaData()
	at_UP.type = MpcAttributeType.Boolean
	at_UP.name = 'U-P (Displacement+Pressure)'
	at_UP.group = 'Constraint'
	at_UP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U-P (Displacement+Pressure)')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	at_UP.editable = False
	
	# Beam
	at_Beam = MpcAttributeMetaData()
	at_Beam.type = MpcAttributeType.Boolean
	at_Beam.name = 'U-R (Displacement+Rotation)'
	at_Beam.group = 'Constraint'
	at_Beam.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U-R (Displacement+Rotation)')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	at_Beam.editable = False
	
	# Ux
	at_Ux = MpcAttributeMetaData()
	at_Ux.type = MpcAttributeType.Boolean
	at_Ux.name = 'Ux'
	at_Ux.group = 'dof'
	at_Ux.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ux')+'<br/>') + 
		html_par('Ux Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
	# Uy
	at_Uy = MpcAttributeMetaData()
	at_Uy.type = MpcAttributeType.Boolean
	at_Uy.name = 'Uy'
	at_Uy.group = 'dof'
	at_Uy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uy')+'<br/>') + 
		html_par('Uy Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
	# Uz
	at_Uz = MpcAttributeMetaData()
	at_Uz.type = MpcAttributeType.Boolean
	at_Uz.name = 'Uz'
	at_Uz.group = 'dof'
	at_Uz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uz')+'<br/>') + 
		html_par('Uz Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
	# Rx
	at_Rx = MpcAttributeMetaData()
	at_Rx.type = MpcAttributeType.Boolean
	at_Rx.name = 'Rx'
	at_Rx.group = 'dof'
	at_Rx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rx')+'<br/>') + 
		html_par('Rx Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
	# Ry
	at_Ry = MpcAttributeMetaData()
	at_Ry.type = MpcAttributeType.Boolean
	at_Ry.name = 'Ry'
	at_Ry.group = 'dof'
	at_Ry.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ry')+'<br/>') + 
		html_par('Ry Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
	# Rz_2D
	at_Rz_2D = MpcAttributeMetaData()
	at_Rz_2D.type = MpcAttributeType.Boolean
	at_Rz_2D.name = 'Rz/2D'
	at_Rz_2D.group = 'dof'
	at_Rz_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rz')+'<br/>') + 
		html_par('Rz Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
	# Rz_3D
	at_Rz_3D = MpcAttributeMetaData()
	at_Rz_3D.type = MpcAttributeType.Boolean
	at_Rz_3D.name = 'Rz/3D'
	at_Rz_3D.group = 'dof'
	at_Rz_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rz')+'<br/>') + 
		html_par('Rz Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
	# P_2D
	at_P_2D = MpcAttributeMetaData()
	at_P_2D.type = MpcAttributeType.Boolean
	at_P_2D.name = 'P/2D'
	at_P_2D.group = 'dof'
	at_P_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('P')+'<br/>') + 
		html_par('P Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
	# P_3D
	at_P_3D = MpcAttributeMetaData()
	at_P_3D.type = MpcAttributeType.Boolean
	at_P_3D.name = 'P/3D'
	at_P_3D.group = 'dof'
	at_P_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('P')+'<br/>') + 
		html_par('P Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fix_command','Fix command')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'fix'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_ModelType)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_D)
	xom.addAttribute(at_UP)
	xom.addAttribute(at_Beam)
	xom.addAttribute(at_Ux)
	xom.addAttribute(at_Uy)
	xom.addAttribute(at_Uz)
	xom.addAttribute(at_Rx)
	xom.addAttribute(at_Ry)
	xom.addAttribute(at_Rz_2D)
	xom.addAttribute(at_Rz_3D)
	xom.addAttribute(at_P_2D)
	xom.addAttribute(at_P_3D)
	xom.addAttribute(at_ctype)
	
	
	# visibility dependencies
	
	#2D
	# P_2D-dep
	xom.setVisibilityDependency(at_2D, at_P_2D)
	xom.setVisibilityDependency(at_UP, at_P_2D)
	
	# Rz_2D-dep
	xom.setVisibilityDependency(at_2D, at_Rz_2D)
	xom.setVisibilityDependency(at_Beam, at_Rz_2D)
	
	#3D
	# uz-dep
	xom.setVisibilityDependency(at_3D, at_Uz)
	
	# P_3D-dep
	xom.setVisibilityDependency(at_3D, at_P_3D)
	xom.setVisibilityDependency(at_UP, at_P_3D)
	
	# Rx-dep
	xom.setVisibilityDependency(at_3D, at_Rx)
	xom.setVisibilityDependency(at_Beam, at_Rx)
	
	# Ry-dep
	xom.setVisibilityDependency(at_3D, at_Ry)
	xom.setVisibilityDependency(at_Beam, at_Ry)
	
	# Rz-dep
	xom.setVisibilityDependency(at_3D, at_Rz_3D)
	xom.setVisibilityDependency(at_Beam, at_Rz_3D)
	
	
	# auto-exclusive dependencies
	
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	# 2D or 2D UP or 2D Beam or 3D or 3D UP or 3D Beam
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_D)
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_UP)
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_Beam)
	
	return xom

def __control(xobj):
	
	d = my_data()
	
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	d.Dimension2 = Dimension2_at.boolean
	
	Dimension3_at = xobj.getAttribute('3D')
	if(Dimension3_at is None):
		raise Exception('Error: cannot find "3D" attribute')
	d.Dimension3 = Dimension3_at.boolean
	
	D_at = xobj.getAttribute('U (Displacement)')
	if(D_at is None):
		raise Exception('Error: cannot find "U (Displacement)" attribute')
	d.D = D_at.boolean
	
	UP_at = xobj.getAttribute('U-P (Displacement+Pressure)')
	if(UP_at is None):
		raise Exception('Error: cannot find "U-P (Displacement+Pressure)" attribute')
	d.UP = UP_at.boolean
	
	UR_at = xobj.getAttribute('U-R (Displacement+Rotation)')
	if(UR_at is None):
		raise Exception('Error: cannot find "U-R (Displacement+Rotation)" attribute')
	d.UR = UR_at.boolean
	
	Ux_at = xobj.getAttribute('Ux')
	if(Ux_at is None):
		raise Exception('Error: cannot find "Ux" attribute')
	d.Ux = Ux_at.boolean
	
	Uy_at = xobj.getAttribute('Uy')
	if(Uy_at is None):
		raise Exception('Error: cannot find "Uy" attribute')
	d.Uy = Uy_at.boolean
	
	Uz_at = xobj.getAttribute('Uz')
	if(Uz_at is None):
		raise Exception('Error: cannot find "Uz" attribute')
	d.Uz = Uz_at.boolean
	
	Rx_at = xobj.getAttribute('Rx')
	if(Rx_at is None):
		raise Exception('Error: cannot find "Rx" attribute')
	d.Rx = Rx_at.boolean
	
	Ry_at = xobj.getAttribute('Ry')
	if(Ry_at is None):
		raise Exception('Error: cannot find "Ry" attribute')
	d.Ry = Ry_at.boolean
	
	Rz_2D_at = xobj.getAttribute('Rz/2D')
	if(Rz_2D_at is None):
		raise Exception('Error: cannot find "Rz" attribute')
	d.Rz_2D = Rz_2D_at.boolean
	
	Rz_3D_at = xobj.getAttribute('Rz/3D')
	if(Rz_3D_at is None):
		raise Exception('Error: cannot find "Rz" attribute')
	d.Rz_3D = Rz_3D_at.boolean
	
	P_2D_at = xobj.getAttribute('P/2D')
	if(P_2D_at is None):
		raise Exception('Error: cannot find "P" attribute')
	d.P_2D = P_2D_at.boolean
	
	P_3D_at = xobj.getAttribute('P/3D')
	if(P_3D_at is None):
		raise Exception('Error: cannot find "P" attribute')
	d.P_3D = P_3D_at.boolean
	
	return d

def __get_nodes(condition):
	doc = App.caeDocument()
	all_geom = condition.assignment.geometries
	nodes = []
	for geom, subset in all_geom.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		for i in subset.edges:
			domain = mesh_of_geom.edges[i]
			for elem in domain.elements:
				for node in elem.nodes:
					nodes.append(node.id)
		for i in subset.faces:
			domain = mesh_of_geom.faces[i]
			for elem in domain.elements:
				for node in elem.nodes:
					nodes.append(node.id)
		for i in subset.solids:
			domain = mesh_of_geom.solids[i]
			for elem in domain.elements:
				for node in elem.nodes:
					nodes.append(node.id)
		for i in subset.vertices:
			node = mesh_of_geom.vertices[i]
			nodes.append(node.id)
	nodes = list(set(nodes))
	return nodes

def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.ConstraintGlyph
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = True
	d.on_edges = True
	d.on_faces = True
	d.on_solids = True
	d.on_interactions = False
	
	return d

def getRequestedNodalSpatialDim(xobj):
	'''
	similar to the def getNodalSpatialDim(xobj, xobj_phys_prop) method in element properties,
	but with a conceptual difference. getNodalSpatialDim returns a list of (ndm,ndf) pair
	whose length is equal to the number of nodes for that element, following the local
	numbering of each element.
	Here instead we return a map, where the key is the ID of the (only) nodes where
	the condition requires a specific dimension (here for example the master node)
	
	Update 6/2/2020:
	We want to allow:
	1) master and slave to have different dofs
	2) the master node can have a different dofset than the one of the condition
		- we give here more than one dofset
		- the first one is the one in this conditon because, if the node is floating,
		it will take the first one
	'''
	
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	Dimension2 = Dimension2_at.boolean
	
	UP_at = xobj.getAttribute('U-P (Displacement+Pressure)')
	if(UP_at is None):
		raise Exception('Error: cannot find "U-P (Displacement+Pressure)" attribute')
	UP = UP_at.boolean
	
	UR_at = xobj.getAttribute('U-R (Displacement+Rotation)')
	if(UR_at is None):
		raise Exception('Error: cannot find "U-R (Displacement+Rotation)" attribute')
	UR = UR_at.boolean
	
	if Dimension2:
		ndm = 2
		if UP or UR:
			ndf = [3, 2] # user-defined goes first
		else:
			ndf = [2, 3] # standard
		
	else:
		ndm = 3
		if UP:
			ndf = [4, 3, 6] # user-defined goes first
		elif UR:
			ndf = [6, 3, 4] # user-defined goes first
		else:
			ndf = [3, 4, 6] # standard
	
	requested_node_dim_map = {}
	condition = xobj.parent
	nodes = __get_nodes(condition)
	for node_id in nodes:
		requested_node_dim_map[node_id] = (ndm, ndf)
	
	return requested_node_dim_map

def SP_getNodesAndDofs(pinfo):
	'''
	each module in namespace opensees.conditions.SP MUST have this function!
	this function return a list of fixed dofs (1 to ndf) 
	@node: pinfo MUST contain the current condition. then we get the xobj from the condition
	'''
	d = __control(pinfo.condition.XObject)
	
	nodes = __get_nodes(pinfo.condition)
	dofs = []
	
	if d.Ux:
		dofs.append(1)
	if d.Uy:
		dofs.append(2)
	if d.Dimension2:
		if (d.UP and d.P_2D) or (d.UR and d.Rz_2D):
			dofs.append(3)
	else:
		if d.Uz:
			dofs.append(3)
		if (d.UP and d.P_3D) or (d.UR and d.Rx) :
			dofs.append(4)
		if (d.UR and d.Ry):
			dofs.append(5)
		if (d.UR and d.Rz_3D):
			dofs.append(6)
	
	return (nodes, dofs)

def __build_fix_string(node_ndf, ndf, indent, tabIndent, node_id, sopt):
	'''
	builds the fix command string taking care of consistency between
	the NDF of the current node and the NDF of the SP constraint
	@note: in string like this: sopt[:node_ndf*2]))
	the *2 factor is there because sopt is string with 1 and 0, with white spaces in between
	'''
	if(node_ndf == ndf):
		# simple case, just use the whole sopt
		# note: there is only one singular behavior here
		# when we are in 2D with 3 dofs:
		# even if both node_ndf and ndf = 3, it may happen that
		# the user selected 2D U-P for node and 2D U-R for constraint.
		return '{}{}fix {}{}\n'.format(indent, tabIndent, node_id , sopt)
	elif(node_ndf < ndf):
		# get only the first node_ndf fix flags
		if(node_ndf == 4):
			# avoid considering Rx as P (only with node = 3DUP -> SP = 3DUR)
			return '{}{}fix {}{} 0\n'.format(indent, tabIndent, node_id ,sopt[:(node_ndf-1)*2])
		# any other case
		return '{}{}fix {}{}\n'.format(indent, tabIndent, node_id , sopt[:node_ndf*2])
	elif(node_ndf > ndf):
		# fill the difference with zero flags
		ndf_diff = node_ndf - ndf # general case 4-3 6-3
		trim = 0
		if ndf == 4: # avoid considering Rx as P
			ndf_diff += 1
			trim = 1
		s = '{} {}'.format(sopt[:len(sopt)-2*trim], ' '.join(['0']*ndf_diff))
		return '{}{}fix {}{}\n'.format(indent, tabIndent, node_id , s)
		
def writeTcl_spConstraints(pinfo):
	
	# fix $nodeTag (ndf $constrValues)
	
	xobj = pinfo.condition.XObject
	
	FileName = xobj.name
	if pinfo.currentDescription != FileName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, FileName))
		pinfo.currentDescription = FileName
	
	d = __control(xobj)
	
	sopt = ''
	
	if d.Ux:
		sopt += ' 1'
	else :
		sopt += ' 0'
	if d.Uy:
		sopt += ' 1'
	else :
		sopt += ' 0'
		
	if d.Dimension2:
		ndm = 2
		ndf = 2
		if not d.D:
			ndf = 3
			if (d.UP and d.P_2D) or (d.UR and d.Rz_2D):
				sopt += ' 1'
			else :
				sopt += ' 0'
	else:
		ndm = 3
		ndf = 3
		if d.Uz :
			sopt += ' 1'
		else :
			sopt += ' 0'
		if not d.D:
			ndf = 4
			if (d.UP and d.P_3D) or (d.UR and d.Rx) :
				sopt += ' 1'
			else :
				sopt += ' 0'
			if d.UR :
				ndf = 6
				if d.Ry:
					sopt += ' 1'
				else :
					sopt += ' 0'
				if d.Rz_3D :
					sopt += ' 1'
				else :
					sopt += ' 0'
	
	if not sopt:
		raise Exception ('Error: insufficient number of attributes')
	
	# fixed 6/2/2020. not used in opensees
	#pinfo.updateModelBuilder(ndm, ndf)
	
	nodes = __get_nodes(pinfo.condition)
	
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	if pinfo.process_count > 1:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			first_done = False
			
			str_tcl = []
			for node_id in nodes:
				if (node_id in pinfo.node_to_model_map):
				
					if not doc.mesh.partitionData.isNodeOnParition(node_id, process_id):
						continue
					if not first_done:
						if process_block_count == 0:
							pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
						else:
							pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
						first_done = True
				
					spatial_info = pinfo.node_to_model_map[node_id]
					node_ndm = spatial_info[0]
					node_ndf = spatial_info[1]
					if (ndm != node_ndm) :
						raise Exception('Error: condition and node have different NDM')
				else :
					raise Exception('Error: node without assigned element')		#nodo senza elemento assegnato
				pinfo.out_file.write(__build_fix_string(node_ndf, ndf, pinfo.indent, pinfo.tabIndent, node_id, sopt))
			
			if first_done:
				process_block_count += 1
			if process_block_count > 0 and first_done:
				pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		pinfo.out_file.write('\n')
	else:
		str_tcl = []
		for node_id in nodes:
			if (node_id in pinfo.node_to_model_map):
				spatial_info = pinfo.node_to_model_map[node_id]
				node_ndm = spatial_info[0]
				node_ndf = spatial_info[1]
				if (ndm != node_ndm) :
					raise Exception('Error: condition and node have different NDM')
			else :
				raise Exception('Error: node without assigned element')		#nodo senza elemento assegnato
			pinfo.out_file.write(__build_fix_string(node_ndf, ndf, pinfo.indent, pinfo.tabIndent, node_id, sopt))
		
		# now write the string into the file
		pinfo.out_file.write(''.join(str_tcl))