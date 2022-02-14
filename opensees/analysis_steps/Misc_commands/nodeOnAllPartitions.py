from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# SelectionSets
	at_SelectionSets = MpcAttributeMetaData()
	at_SelectionSets.type = MpcAttributeType.IndexVector
	at_SelectionSets.name = 'SelectionSets'
	at_SelectionSets.group = 'Group'
	at_SelectionSets.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('SelectionSets')+'<br/>') + 
		html_par((
			'Select one or multiple selection sets.<br/>'
			'All the nodes of the mesh generated form the selected geometries '
			'will be written to all partitions.<br/>'
			'Usually a node is written in a certain partition if and only if '
			'an element that contains the node belongs to that particular partition.<br/>'
			'There are however cases where one may need to force writing a node on all partitions '
			'(e.g. the control node of the dislacement control integrator).'
			)) +
		html_end()
		)
	at_SelectionSets.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	xom = MpcXObjectMetaData()
	xom.name = 'nodeOnAllPartitions'
	xom.addAttribute(at_SelectionSets)
	
	return xom

def writeTcl(pinfo):
	
	# node tag x y z
	
	xobj = pinfo.analysis_step.XObject
	tag_add_to_parameter =  xobj.parent.id
	
	FileName = xobj.name
	if pinfo.currentDescription != FileName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, FileName))
		pinfo.currentDescription = FileName
	doc = App.caeDocument()
	
	SelectionSets_at = xobj.getAttribute('SelectionSets')
	if(SelectionSets_at is None):
		raise Exception('Error: cannot find "SelectionSets" attribute')
	SelectionSets = SelectionSets_at.indexVector
	
	indent =  pinfo.tabIndent
	
	'''
	here we map all the nodes in the selected selection sets
	to avoid duplicates
	'''
	map_node = {}

	for selection_set_id in SelectionSets:
		if not selection_set_id in doc.selectionSets: continue
		selection_set = doc.selectionSets[selection_set_id]
		for geometry_id, geometry_subset in selection_set.geometries.items():
			mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
			for domain_id in geometry_subset.vertices:
				node = mesh_of_geom.vertices[domain_id]
				map_node[node.id] = (node.x, node.y, node.z)
			for domain_id in geometry_subset.edges:
				domain = mesh_of_geom.edges[domain_id]
				for elem in domain.elements:
					for node in elem.nodes:
						map_node[node.id] = (node.x, node.y, node.z)
			for domain_id in geometry_subset.faces:
				domain = mesh_of_geom.faces[domain_id]
				for elem in domain.elements:
					for node in elem.nodes:
						map_node[node.id] = (node.x, node.y, node.z)
			for domain_id in geometry_subset.solids:
				domain = mesh_of_geom.solids[domain_id]
				for elem in domain.elements:
					for node in elem.nodes:
						map_node[node.id] = (node.x, node.y, node.z)
	
	process_block_count = 0
	FMT = pinfo.get_double_formatter()
	for process_id in range(len(doc.mesh.partitionData.partitions)):
		pinfo.setProcessId(process_id)
		first_done = False
		for node_id in map_node:
			if doc.mesh.partitionData.isNodeOnParition(node_id, process_id):
				continue
			else:
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
						pinfo.out_file.write('\n{}{}# nodeOnAllPartitions\n'.format(pinfo.indent, indent))
						pinfo.out_file.write('{}{}{} {} {} {} {}\n'.format(pinfo.indent, indent, '#', 'tag', 'x', 'y', 'z'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
						pinfo.out_file.write('{}{}{} {} {} {} {}\n'.format(pinfo.indent, indent, '#', 'tag', 'x', 'y', 'z'))
					first_done = True
				pinfo.updateModelBuilder(pinfo.node_to_model_map[node_id][0], pinfo.node_to_model_map[node_id][1])
				if (pinfo.node_to_model_map[node_id][0] == 2):
					pinfo.out_file.write('{}{}node {} {} {}\n'.format(pinfo.indent, indent, node_id, FMT(map_node[node_id][0]), FMT(map_node[node_id][1])))
				else :
					pinfo.out_file.write('{}{}node {} {} {} {}\n'.format(pinfo.indent, indent, node_id, FMT(map_node[node_id][0]), FMT(map_node[node_id][1]), FMT(map_node[node_id][2])))
			if first_done:
				process_block_count += 1
				
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))