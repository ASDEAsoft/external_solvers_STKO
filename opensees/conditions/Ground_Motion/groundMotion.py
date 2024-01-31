import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import PyMpc.App

def makeXObjectMetaData():
	
	# type
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.String
	at_type.name = 'type'
	at_type.group = 'groundMotion'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/GroundMotion_Command','GroundMotion Command')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList(['Plain', 'Interpolated'])
	at_type.setDefault('Plain')
	
	# Plain
	at_Plain = MpcAttributeMetaData()
	at_Plain.type = MpcAttributeType.Boolean
	at_Plain.name = 'Plain'
	at_Plain.group = 'groundMotion'
	at_Plain.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Plain')+'<br/>') +
		html_par('Plain') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	at_Plain.editable = False
	
	# Interpolated
	at_Interpolated = MpcAttributeMetaData()
	at_Interpolated.type = MpcAttributeType.Boolean
	at_Interpolated.name = 'Interpolated'
	at_Interpolated.group = 'groundMotion'
	at_Interpolated.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Interpolated')+'<br/>') +
		html_par('Interpolated') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Interpolated_GroundMotion','Interpolated GroundMotion')+'<br/>') +
		html_end()
		)
	at_Interpolated.editable = False
	
	
	''' --------------------------------------------------- Plain GroundMotion --------------------------------------------------- '''
	
	# -accel
	at_accel = MpcAttributeMetaData()
	at_accel.type = MpcAttributeType.Boolean
	at_accel.name = '-accel'
	at_accel.group = 'Plain'
	at_accel.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-accel')+'<br/>') +
		html_par('acceleration') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	
	# tsTagAccel
	at_tsTagAccel = MpcAttributeMetaData()
	at_tsTagAccel.type = MpcAttributeType.Index
	at_tsTagAccel.name = 'tsTagAccel'
	at_tsTagAccel.group = 'Plain'
	at_tsTagAccel.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tsTagAccel')+'<br/>') + 
		html_par('tag of TimeSeries object created using '+html_href('http://opensees.berkeley.edu/wiki/index.php/Time_Series_Command','timeSeries')+' command') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	at_tsTagAccel.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_tsTagAccel.indexSource.addAllowedNamespace("timeSeries")
	
	# -vel
	at_vel = MpcAttributeMetaData()
	at_vel.type = MpcAttributeType.Boolean
	at_vel.name = '-vel'
	at_vel.group = 'Plain'
	at_vel.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-vel')+'<br/>') +
		html_par('velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	
	# tsTagVel
	at_tsTagVel = MpcAttributeMetaData()
	at_tsTagVel.type = MpcAttributeType.Index
	at_tsTagVel.name = 'tsTagVel'
	at_tsTagVel.group = 'Plain'
	at_tsTagVel.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tsTagVel')+'<br/>') + 
		html_par('tag of TimeSeries object created using '+html_href('http://opensees.berkeley.edu/wiki/index.php/Time_Series_Command','timeSeries')+' command') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	at_tsTagVel.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_tsTagVel.indexSource.addAllowedNamespace("timeSeries")
	
	# -disp
	at_disp = MpcAttributeMetaData()
	at_disp.type = MpcAttributeType.Boolean
	at_disp.name = '-disp'
	at_disp.group = 'Plain'
	at_disp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-disp')+'<br/>') +
		html_par('displacement') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	
	# tsTagDisp
	at_tsTagDisp = MpcAttributeMetaData()
	at_tsTagDisp.type = MpcAttributeType.Index
	at_tsTagDisp.name = 'tsTagDisp'
	at_tsTagDisp.group = 'Plain'
	at_tsTagDisp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tsTagDisp')+'<br/>') + 
		html_par('tag of TimeSeries object created using '+html_href('http://opensees.berkeley.edu/wiki/index.php/Time_Series_Command','timeSeries')+' command') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	at_tsTagDisp.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_tsTagDisp.indexSource.addAllowedNamespace("timeSeries")
	
	# -int
	at_int = MpcAttributeMetaData()
	at_int.type = MpcAttributeType.Boolean
	at_int.name = '-int'
	at_int.group = 'Plain'
	at_int.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-int')+'<br/>') +
		html_par('Trapezoidal or Simpson numerical integration method (optional, default=Trapezoidal). See NOTES') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	
	# IntegratorType
	at_IntegratorType = MpcAttributeMetaData()
	at_IntegratorType.type = MpcAttributeType.String
	at_IntegratorType.name = 'IntegratorType'
	at_IntegratorType.group = 'Plain'
	at_IntegratorType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegratorType')+'<br/>') + 
		html_par('Trapezoidal or Simpson numerical integration method (optional, default=Trapezoidal). See NOTES') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	at_IntegratorType.sourceType = MpcAttributeSourceType.List
	at_IntegratorType.setSourceList(['Trapezoidal', 'Simpson'])
	at_IntegratorType.setDefault('Trapezoidal')
	
	# -fact
	at_fact_Plain = MpcAttributeMetaData()
	at_fact_Plain.type = MpcAttributeType.Boolean
	at_fact_Plain.name = '-fact'
	at_fact_Plain.group = 'Plain'
	at_fact_Plain.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-fact')+'<br/>') +
		html_par('constant factor (optional, default=1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	
	# cFactor
	at_cFactor = MpcAttributeMetaData()
	at_cFactor.type = MpcAttributeType.Real
	at_cFactor.name = 'cFactor'
	at_cFactor.group = 'Plain'
	at_cFactor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cFactor')+'<br/>') + 
		html_par('constant factor (optional, default=1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_GroundMotion','Plain GroundMotion')+'<br/>') +
		html_end()
		)
	at_cFactor.setDefault(1.0)
	
	''' --------------------------------------------------- Plain GroundMotion --------------------------------------------------- '''
	
	
	''' ----------------------------------------------- Interpolated GroundMotion ------------------------------------------------ '''
	
	# gmTag
	at_gmTag = MpcAttributeMetaData()
	at_gmTag.type = MpcAttributeType.IndexVector
	at_gmTag.name = 'gmTag'
	at_gmTag.group = 'Interpolated'
	at_gmTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gmTag')+'<br/>') + 
		html_par('the tags of existing ground motions in pattern to be used for interpolation.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Interpolated_GroundMotion','Interpolated GroundMotion')+'<br/>') +
		html_end()
		)
	at_gmTag.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_gmTag.indexSource.addAllowedNamespace("GroundMotion")
	
	# fact
	at_fact_Interpolated = MpcAttributeMetaData()
	at_fact_Interpolated.type = MpcAttributeType.QuantityVector
	at_fact_Interpolated.name = 'fact/Interpolated'
	at_fact_Interpolated.group = 'Interpolated'
	at_fact_Interpolated.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fact')+'<br/>') + 
		html_par('the interpolation factors') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Interpolated_GroundMotion','Interpolated GroundMotion')+'<br/>') +
		html_end()
		)
	
	''' ----------------------------------------------- Interpolated GroundMotion ------------------------------------------------ '''
	
	
	''' --------------------------------------------- Extra Data for imposedMotion ----------------------------------------------- '''
	
	# dx
	at_dx = MpcAttributeMetaData()
	at_dx.type = MpcAttributeType.Boolean
	at_dx.name = 'dx'
	at_dx.group = 'imposedMotion'
	at_dx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dx')+'<br/>') +
		html_par('dof of enforced response') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/imposedMotion_Command','imposedMotion Command')+'<br/>') +
		html_end()
		)
	
	# dy
	at_dy = MpcAttributeMetaData()
	at_dy.type = MpcAttributeType.Boolean
	at_dy.name = 'dy'
	at_dy.group = 'imposedMotion'
	at_dy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dy')+'<br/>') +
		html_par('dof of enforced response') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/imposedMotion_Command','imposedMotion Command')+'<br/>') +
		html_end()
		)
	
	# dz
	at_dz = MpcAttributeMetaData()
	at_dz.type = MpcAttributeType.Boolean
	at_dz.name = 'dz'
	at_dz.group = 'imposedMotion'
	at_dz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dz')+'<br/>') +
		html_par('dof of enforced response') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/imposedMotion_Command','imposedMotion Command')+'<br/>') +
		html_end()
		)
	
	# Rx
	at_Rx = MpcAttributeMetaData()
	at_Rx.type = MpcAttributeType.Boolean
	at_Rx.name = 'Rx'
	at_Rx.group = 'imposedMotion'
	at_Rx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rx')+'<br/>') +
		html_par('dof of enforced response') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/imposedMotion_Command','imposedMotion Command')+'<br/>') +
		html_end()
		)
	
	# Ry
	at_Ry = MpcAttributeMetaData()
	at_Ry.type = MpcAttributeType.Boolean
	at_Ry.name = 'Ry'
	at_Ry.group = 'imposedMotion'
	at_Ry.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ry')+'<br/>') +
		html_par('dof of enforced response') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/imposedMotion_Command','imposedMotion Command')+'<br/>') +
		html_end()
		)
	
	# Rz
	at_Rz = MpcAttributeMetaData()
	at_Rz.type = MpcAttributeType.Boolean
	at_Rz.name = 'Rz'
	at_Rz.group = 'imposedMotion'
	at_Rz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rz')+'<br/>') +
		html_par('dof of enforced response') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/imposedMotion_Command','imposedMotion Command')+'<br/>') +
		html_end()
		)
	
	''' --------------------------------------------- Extra Data for imposedMotion ----------------------------------------------- '''
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'groundMotion'
	xom.addAttribute(at_type)
	xom.addAttribute(at_Plain)
	xom.addAttribute(at_Interpolated)
	# Plain
	xom.addAttribute(at_accel)
	xom.addAttribute(at_tsTagAccel)
	xom.addAttribute(at_vel)
	xom.addAttribute(at_tsTagVel)
	xom.addAttribute(at_disp)
	xom.addAttribute(at_tsTagDisp)
	xom.addAttribute(at_int)
	xom.addAttribute(at_IntegratorType)
	xom.addAttribute(at_fact_Plain)
	xom.addAttribute(at_cFactor)
	# Interpolated
	xom.addAttribute(at_gmTag)
	xom.addAttribute(at_fact_Interpolated)
	# imposedMotion
	xom.addAttribute(at_dx)
	xom.addAttribute(at_dy)
	xom.addAttribute(at_dz)
	xom.addAttribute(at_Rx)
	xom.addAttribute(at_Ry)
	xom.addAttribute(at_Rz)
	
	
	# visibility dependencies
	# Plain
	xom.setVisibilityDependency(at_Plain, at_accel)
	xom.setVisibilityDependency(at_Plain, at_tsTagAccel)
	xom.setVisibilityDependency(at_Plain, at_vel)
	xom.setVisibilityDependency(at_Plain, at_tsTagVel)
	xom.setVisibilityDependency(at_Plain, at_disp)
	xom.setVisibilityDependency(at_Plain, at_tsTagDisp)
	xom.setVisibilityDependency(at_Plain, at_int)
	xom.setVisibilityDependency(at_Plain, at_IntegratorType)
	xom.setVisibilityDependency(at_Plain, at_fact_Plain)
	xom.setVisibilityDependency(at_Plain, at_cFactor)
	
	xom.setVisibilityDependency(at_accel, at_tsTagAccel)
	xom.setVisibilityDependency(at_vel, at_tsTagVel)
	xom.setVisibilityDependency(at_disp, at_tsTagDisp)
	xom.setVisibilityDependency(at_int, at_IntegratorType)
	xom.setVisibilityDependency(at_fact_Plain, at_cFactor)
	
	# Interpolated
	xom.setVisibilityDependency(at_Interpolated, at_gmTag)
	xom.setVisibilityDependency(at_Interpolated, at_fact_Interpolated)
	
	
	# auto-exclusive dependencies
	# type
	xom.setBooleanAutoExclusiveDependency(at_type, at_Plain)
	xom.setBooleanAutoExclusiveDependency(at_type, at_Interpolated)
	
	
	return xom

def makeConditionRepresentationData(xobj):
	
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Points
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = True
	d.on_edges = True
	d.on_faces = True
	d.on_solids = True
	d.on_interactions = False
	return d

class _dofmap:
	def __init__(self, labels, ids):
		self.labels = labels
		self.ids = ids
class _gstore:
	def make_2DU():  return _dofmap(['dx', 'dy'], [1,2])
	def make_2DUR(): return _dofmap(['dx', 'dy', 'Rz'], [1,2,3])
	def make_3DU():  return _dofmap(['dx', 'dy', 'dz'], [1,2,3])
	def make_3DUR(): return _dofmap(['dx', 'dy', 'dz', 'Rx', 'Ry', 'Rz'], [1,2,3,4,5,6])
	MAP = {
		2 : {
			2 : make_2DU(),
			3 : make_2DUR()
			},
		3 : {
			3 : make_3DU(),
			4 : make_3DU(),
			6 : make_3DUR()
			}
		}

def writeTcl_groundMotion(pinfo, xobj, tag):
	
	# utility to get the attribute
	def geta(name):
		a = xobj.getAttribute(name)
		if a is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return a
	
	# write a description
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# type
	type = geta('type').string
	
	# Plain
	# groundMotion $tag Plain <-accel $tsTag> <-vel $tsTag> <-disp $tsTag> <-int (IntegratorType intArgs)> <-fact $cFactor>
	if type == 'Plain':
		sopt = ''
		if geta('-accel').boolean:
			sopt += ' -accel {}'.format(geta('tsTagAccel').index)
		if geta('-vel').boolean:
			sopt += ' -vel {}'.format(geta('tsTagVel').index)
		if geta('-disp').boolean:
			sopt += ' -disp {}'.format(geta('tsTagDisp').index)
		if geta('-int').boolean:
			sopt += ' -int {}'.format(geta('IntegratorType').string)
		if geta('-fact').boolean:
			sopt += ' -fact {}'.format(geta('cFactor').real)
		pinfo.out_file.write('{}{}groundMotion {} Plain{}\n'.format(pinfo.indent, pinfo.tabIndent, tag, sopt))
	
	# Interpolated
	# groundMotion $tag Interpolated $gmTag1 $gmTag2 ... -fact $fact1 $fact2 ...
	elif type == 'Interpolated':
		gmTag = geta('gmTag').indexVector
		fact = geta('fact/Interpolated').quantityVector
		if(len(gmTag) != len(fact)):
			raise Exception('Error: different length of vectors between "gmTag" and "fact"')
		gmTag_str = ''
		fact_str = ''
		for i in range(len(gmTag)):
			gmTag_str += ' {}'.format(gmTag[i])
			fact_str += ' {}'.format(fact.valueAt(i))
		pinfo.out_file.write('{}{}groundMotion {} Interpolated{} -fact{}\n'.format(pinfo.indent, pinfo.tabIndent, tag, gmTag_str, fact_str))
	
	# imposedMotion
	# imposedMotion $nodeTag $dirn $gMotionTag
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	
	# get document
	doc = App.caeDocument()
	
	# process all geometries and map nodes to their process id
	pcount = pinfo.process_count
	if pcount > 1:
		partition_data = doc.mesh.partitionData
		nodes = [[] for i in range(pcount)]
	else:
		partition_data = None
		nodes = []
	# utility to append the node_id to its proper list
	def append_node(node_id):
		if pcount > 1:
			for pid in range(pcount):
				if partition_data.isNodeOnParition(node_id, pid):
					nodes[pid].append(node_id)
		else:
			nodes.append(node_id)
	# process nodes in the selection
	for geom, subset in all_geom.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		for i in subset.vertices:
			domain = mesh_of_geom.vertices[i]
			append_node(domain.id)
		sset = [subset.edges, subset.faces, subset.solids]
		gset = [mesh_of_geom.edges, mesh_of_geom.faces, mesh_of_geom.solids]
		for gid in range(len(sset)):
			set_item = sset[gid]
			geo_item = gset[gid]
			for domain_id in set_item:
				domain = geo_item[domain_id]
				for element in domain.elements:
					for node in element.nodes:
						append_node(node.id)
	# avoid duplicates
	if pcount > 1:
		for pid in range(pcount):
			nodes[pid] = list(set(nodes[pid]))
	else:
		nodes = list(set(nodes))
	
	# utility to write imposedMotion on a node
	def write_im_node(node_id, extra_indent = ''):
		ndm, ndf = pinfo.node_to_model_map[node_id]
		map = _gstore.MAP[ndm][ndf]
		for j in range(len(map.labels)):
			dof_label = map.labels[j]
			if geta(dof_label).boolean:
				pinfo.out_file.write('{}{}{}imposedMotion {} {} {}\n'.format(pinfo.indent, pinfo.tabIndent, extra_indent, node_id, map.ids[j], tag))
	
	# write imposedMotion commands
	if pcount > 1:
		etab = pinfo.tabIndent
		for pid in range(pcount):
			pnodes = nodes[pid]
			if len(pnodes) > 0:
				pinfo.out_file.write('{}{}if {{$STKO_VAR_process_id == {}}} {{\n'.format(pinfo.indent, etab, pid))
				for inode in pnodes:
					write_im_node(inode, etab)
				pinfo.out_file.write('{}{}}}\n'.format(pinfo.indent, etab))
	else:
		for inode in nodes:
			write_im_node(inode)