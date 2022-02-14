import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import re

def makeXObjectMetaData():
	
	# approach
	at_approach = MpcAttributeMetaData()
	at_approach.type = MpcAttributeType.String
	at_approach.name = 'approach'
	at_approach.group = 'Group'
	at_approach.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('approach')+'<br/>') + 
		html_par('choose between "-user" and "-source"') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#BeamThermal3D','eleLoad_beamThermal3D')+'<br/>') +
		html_end()
		)
	at_approach.sourceType = MpcAttributeSourceType.List
	at_approach.setSourceList(['-user', '-source'])
	at_approach.setDefault('-user')
	
	# -user
	at_user = MpcAttributeMetaData()
	at_user.type = MpcAttributeType.Boolean
	at_user.name = '-user'
	at_user.group = 'Group'
	at_user.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-user')+'<br/>') +
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#BeamThermal3D','eleLoad_beamThermal3D')+'<br/>') +
		html_end()
		)
	at_user.editable = False
	
	# -source
	at_source = MpcAttributeMetaData()
	at_source.type = MpcAttributeType.Boolean
	at_source.name = '-source'
	at_source.group = 'Group'
	at_source.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-source')+'<br/>') +
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#BeamThermal3D','eleLoad_beamThermal3D')+'<br/>') +
		html_end()
		)
	at_source.editable = False
	
	# -node
	at_node = MpcAttributeMetaData()
	at_node.type = MpcAttributeType.Boolean
	at_node.name = '-node'
	at_node.group = '-source'
	at_node.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-node')+'<br/>') +
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#BeamThermal3D','eleLoad_beamThermal3D')+'<br/>') +
		html_end()
		)
	
	# fileName
	at_fileName = MpcAttributeMetaData()
	at_fileName.type = MpcAttributeType.String
	at_fileName.name = 'fileName'
	at_fileName.group = '-source'
	at_fileName.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fileName')+'<br/>') +
		html_par('external file') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#BeamThermal3D','eleLoad_beamThermal3D')+'<br/>') +
		html_end()
		)
	at_fileName.setDefault('.dat')
	
	# T
	at_T = MpcAttributeMetaData()
	at_T.type = MpcAttributeType.QuantityVector
	at_T.name = 'T'
	at_T.group = '-user'
	at_T.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('T')+'<br/>') +
		html_par('case1: T are the temperatures from T1 and T5') +
		html_par('case2: T are the temperatures from T1 to T15, 3D I section') +
		html_par('case3: T add to file') +
		html_par('case4: T add to file') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#BeamThermal3D','eleLoad_beamThermal3D')+'<br/>') +
		html_end()
		)
	
	# y
	at_y = MpcAttributeMetaData()
	at_y.type = MpcAttributeType.QuantityVector
	at_y.name = 'y'
	at_y.group = 'Group'
	at_y.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('y')+'<br/>') +
		html_par('case1: y are the coordinates from y1 and y5') +
		html_par('case2: y are the coordinates from y1 to y5, 3D I section') +
		html_par('case3: y are the coordinates from y1 and y2') +
		html_par('case4: y are the coordinates from y1 and y2') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#BeamThermal3D','eleLoad_beamThermal3D')+'<br/>') +
		html_end()
		)
	
	# z
	at_z = MpcAttributeMetaData()
	at_z.type = MpcAttributeType.QuantityVector
	at_z.name = 'z'
	at_z.group = 'Group'
	at_z.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('z')+'<br/>') +
		html_par('case1: without z') +
		html_par('case2: z are the coordinates from z1 to z5, 3D I section') +
		html_par('case3: z are the coordinates from z1 and z2') +
		html_par('case4: z are the coordinates from z1 and z2') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#BeamThermal3D','eleLoad_beamThermal3D')+'<br/>') +
		html_end()
		)
	
	# ctype
	at_ctype = MpcAttributeMetaData()
	at_ctype.type = MpcAttributeType.Integer
	at_ctype.editable = False;
	at_ctype.name = 'ctype_constraint'
	at_ctype.group = 'Group'
	at_ctype.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ctype')+'<br/>') +
		html_par('ctype') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#BeamThermal3D','eleLoad_beamThermal3D')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'eleLoad_beamThermal3D'
	xom.addAttribute(at_approach)
	xom.addAttribute(at_user)
	xom.addAttribute(at_source)
	xom.addAttribute(at_node)
	xom.addAttribute(at_fileName)
	xom.addAttribute(at_T)
	xom.addAttribute(at_y)
	xom.addAttribute(at_z)
	xom.addAttribute(at_ctype)
	
	
	# source-dep
	xom.setVisibilityDependency(at_source, at_fileName)
	xom.setVisibilityDependency(at_source, at_node)
	
	# user-dep
	xom.setVisibilityDependency(at_user, at_T)
	
	# auto-exclusive dependencies
	
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_approach, at_user)
	xom.setBooleanAutoExclusiveDependency(at_approach, at_source)
	
	return xom

def fillConditionRepresentationData(xobj, pos, data):
	'''
	Fills the 3D vector data.
	
	Set the pressure value
	at the z component, since the orientation is set to local
	'''
	
	data[0] = 1
	data[1] = 1
	data[2] = 1

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
	d.type = MpcConditionVRepType.Points
	d.orientation = MpcConditionVRepOrientation.Local
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = True
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = False
	return d

def __regex(parameter):
	
	parameter = re.sub(r'\\+', '/', parameter)
	parameter = re.sub(r'/+', '/', parameter)
	
	return parameter


def __processEleLoadBeamThemal3D(pinfo, xobj, user, T, y, tag, eleTag, z, indent):

	if user:
		if((len(T)!=15 or len(y)!=5 or len(z)!=5) and (len(T)!=9 or len(y)!=9) and (len(T)!=2 or len(y)!=2)):
				raise Exception('Error: invalid number of aguments')
		
		if(len(T)==15 and len(y)==5 and len(z)==5):
			str_tcl = '{}{}eleLoad -ele{} -type -beamThermal {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
				pinfo.indent, indent, tag,  T.valueAt(0), y.valueAt(0), T.valueAt(1), y.valueAt(1), T.valueAt(2), y.valueAt(2),
									T.valueAt(3), y.valueAt(3), T.valueAt(4), y.valueAt(4), T.valueAt(5), T.valueAt(6),
									z.valueAt(0), T.valueAt(7), T.valueAt(8), z.valueAt(1), T.valueAt(9), T.valueAt(10),
									z.valueAt(2), T.valueAt(11), T.valueAt(12), z.valueAt(3), T.valueAt(13), T.valueAt(14),
									z.valueAt(4))
		else:
			str_tcl = '{}{}eleLoad -ele{} -type -beamThermal {} {} {} {}\n'.format(pinfo.indent, indent, eleTag, T.valueAt(0), y.valueAt(0), T.valueAt(1), y.valueAt(1))
	
	else:
		# -source
		# optional paramters
		sopt = ''
		
		node_at = xobj.getAttribute('-node')
		if(node_at is None):
			raise Exception('Error: cannot find "-node" attribute')
		node = node_at.boolean
		if node:
			sopt += ' -node'

		
		fileName_at = xobj.getAttribute('fileName')
		if(fileName_at is None):
			raise Exception('Error: cannot find "fileName" attribute')
		fileName = __regex(fileName_at.string)
		
		
		#set list TCL
		y_str = ''
		z_str = ''
		
		nLettersY = len(y_str)
		nLettersZ = len(z_str)
		
		nTabY = nLettersY // 4
		nTabZ = nLettersZ // 4
		
		n = 1
		for i in range(len(y)):
			if (i == (10*n)):
				y_str += '\\\n{}{}'.format(pinfo.indent, tclin.utils.nIndent(nTabY))
				z_str += '\\\n{}{}'.format(pinfo.indent, tclin.utils.nIndent(nTabZ))
				n += 1
			if (i!=len(y)-1):
				y_str += '{} '.format(y.valueAt(i))
				z_str += '{} '.format(z.valueAt(i))
			else:
				y_str += '{}'.format(y.valueAt(i))
				z_str += '{}'.format(z.valueAt(i))
		
		#end list TCL
		
		str_tcl = '{}{}eleLoad -ele{} -type -beamThermal -source{} {} {} {}\n'.format(pinfo.indent,indent, eleTag, sopt, fileName, y_str, z_str)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)

def writeTcl_eleLoad(pinfo, xobj):
	
	#eleLoad -ele $eleTag -type -beamThermal t1, locY1, t2, locY2, t3, locY3, t4, locY4, t5, locY5, t6, t7, locZ1, t8, t9, locZ2, t10, t11, locZ3, t12, t13, locZ4, t14, t15, locZ5;
	#eleLoad -ele $eleTag -type -beamThermal $y1 $y5 $T1 $T5;
	#eleLoad -ele $eleTag -type -beamThermal -source $fileName $y1 $y2 $z1 $z2;
	#eleLoad -ele $eleTag -type -beamThermal -source -node $fileName $y1 $y2 $z1 $z2;
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	
	# mandatory parameters
	user_at = xobj.getAttribute('-user')
	if(user_at is None):
		raise Exception('Error: cannot find "-user" attribute')
	user = user_at.boolean
	
	source_at = xobj.getAttribute('-source')
	if(source_at is None):
		raise Exception('Error: cannot find "-source" attribute')
	source = source_at.boolean
	
	T_at = xobj.getAttribute('T')
	if(T_at is None):
		raise Exception('Error: cannot find "T" attribute')
	T = T_at.quantityVector
	
	y_at = xobj.getAttribute('y')
	if(y_at is None):
		raise Exception('Error: cannot find "y" attribute')
	y = y_at.quantityVector
	
	z_at = xobj.getAttribute('z')
	if(z_at is None):
		raise Exception('Error: cannot find "z" attribute')
	z = z_at.quantityVector
	
	doc = App.caeDocument()
	
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			first_done = False
			for geom, item in all_geom.items():
				mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
				domain_collection = mesh_of_geom.edges
				eleTag = ''
				for i in item.edges:
					domain = domain_collection[i]
					for element in domain.elements:
						if doc.mesh.partitionData.elementPartition(element.id)!= process_id:
							continue
						if not first_done :
							if process_block_count == 0:
								pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
							else:
								pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
							first_done = True
						eleTag += ' {}'.format(element.id)
				if eleTag:
					__processEleLoadBeamThemal3D(pinfo, xobj, user, T, y, tag, eleTag, z, pinfo.tabIndent)
			if is_partitioned :
				if first_done:
					process_block_count += 1
				if process_block_count > 0 and first_done:
					pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
	else:
		for geom, item in all_geom.items():
			mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
			domain_collection = mesh_of_geom.edges
			eleTag = ''
			for i in item.edges:
				domain = domain_collection[i]
				for element in domain.elements:
					eleTag += ' {}'.format(element.id)
			__processEleLoadBeamThemal3D(pinfo, xobj, user, T, y, tag, eleTag, z, pinfo.indent)