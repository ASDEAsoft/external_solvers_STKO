import os
from PyMpc import *
from mpc_utils_html import *
from itertools import groupby, count
import opensees.utils.tcl_input as tclin
import opensees.utils.write_element as write_element
import opensees.utils.write_node as write_node

def makeXObjectMetaData():
	
	at_SelectionSets = MpcAttributeMetaData()
	at_SelectionSets.type = MpcAttributeType.IndexVector
	at_SelectionSets.name = 'SelectionSets'
	at_SelectionSets.group = 'Data'
	at_SelectionSets.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Model Subsets')+'<br/>') + 
		html_par(
			'Select one or more Selection Sets.<br/>'
			'Nodes and elements contained in the selected Selection Sets will be written at the location this Analysis Step is used.<br/>'
			'Notes:<br/>'
			'If the selected Selection Sets are overlapping, elements contained in more than one Set are written only once.'
			'If the selected Selection Sets contain elements or nodes that were already written by a previous instance of this command, such nodes and elements are not written again.') +
		html_end()
		)
	at_SelectionSets.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	xom = MpcXObjectMetaData()
	xom.name = 'modelSubset'
	xom.addAttribute(at_SelectionSets)
	
	return xom

def __process_domain(pinfo, domain):
	# process all elements
	for elem in domain.elements:
		# skip if already written
		if elem.id in pinfo.loaded_element_subset:
			continue
		# add current element
		pinfo.element_subset.add(elem.id)
		# process all nodes of this element
		for node in elem.nodes:
			# skip if already written
			if node.id in pinfo.loaded_node_subset:
				continue
			# add current node
			pinfo.node_subset.add(node.id)

def writeTcl(pinfo):
	
	# get xobject and its parent component id
	xobj = pinfo.analysis_step.XObject
	id = xobj.parent.componentId
	
	# write a comment
	pinfo.out_file.write('\n{}# modelSubset [{}] {}\n'.format(pinfo.indent, id, xobj.parent.componentName))
	
	# get selection set attribute
	SelectionSets_at = xobj.getAttribute('SelectionSets')
	if(SelectionSets_at is None):
		raise Exception('Error: cannot find "SelectionSets" attribute')
	SelectionSets = SelectionSets_at.indexVector
	
	# get the document
	doc = App.caeDocument()
	is_partitioned = (len(doc.mesh.partitionData.partitions) > 1)
	
	# merge the user defined selection sets (nodes and elements) 
	# into the pinfo subsets, without including items that were already processed.
	pinfo.node_subset = set()
	pinfo.element_subset = set()
	for selection_set_id in SelectionSets:
		selection_set = doc.selectionSets[selection_set_id]
		# process all geometry subsets
		for geometry_id, geometry_subset in selection_set.geometries.items():
			# get associated mesh
			mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
			# process all vertices
			for vertex_id in geometry_subset.vertices:
				node = mesh_of_geom.vertices[vertex_id]
				# skip if already written
				if node.id in pinfo.loaded_node_subset:
					continue
				# add current node
				pinfo.node_subset.add(node.id)
			# process all edges
			for domain_id in geometry_subset.edges:
				domain = mesh_of_geom.edges[domain_id];
				__process_domain(pinfo, domain)
			# process all faces
			for domain_id in geometry_subset.faces:
				domain = mesh_of_geom.faces[domain_id]
				__process_domain(pinfo, domain)
			# process all solids
			for domain_id in geometry_subset.solids:
				domain = mesh_of_geom.solids[domain_id]
				__process_domain(pinfo, domain)
		# process all interaction subsets
		for interaction_id in selection_set.interactions:
			# get associated mesh
			mesh_of_inter = doc.mesh.meshedInteractions[interaction_id]
			# even if it is not a domain, in the __process_domain we only access the "elements" property
			# which is present also in mesh_of_inter
			__process_domain(pinfo, mesh_of_inter)
	
	# save current out_file, to be restore later on
	current_out_file = pinfo.out_file
	
	# write nodes.
	# create a single file named nodes.tcl.
	# write all nodes there, and then source it in the main script
	# note that if we have hanging nodes they will be written at the end of the
	# nodes.tcl file.
	node_file_name = 'nodes_subset_{}.tcl'.format(id)
	node_file = open('{}{}{}'.format(pinfo.out_dir, os.sep, node_file_name), 'w+', encoding='utf-8')
	pinfo.out_file = node_file
	if is_partitioned:
		write_node.write_node_partition (doc, pinfo, node_file)
		write_node.write_node_not_assigned_partition (doc, pinfo, node_file)
	else:
		write_node.write_node (doc, pinfo, node_file)
		write_node.write_node_not_assigned (doc, pinfo, node_file)
	node_file.close()
	
	# write elements.
	# create a single file named elements.tcl.
	# write all elements there, and then source it in the main script
	element_file_name = 'elements_subset_{}.tcl'.format(id)
	element_file = open('{}{}{}'.format(pinfo.out_dir, os.sep, element_file_name), 'w+', encoding='utf-8')
	pinfo.out_file = element_file
	if is_partitioned:
		write_element.write_geom_partition(doc, pinfo, element_file)
		write_element.write_inter_partition(doc, pinfo, element_file)
	else:
		write_element.write_geom(doc, pinfo)
		write_element.write_inter(doc, pinfo)
	element_file.close()
	pinfo.elem = None
	pinfo.phys_prop = None
	pinfo.elem_prop = None
	pinfo.node_subset = None
	pinfo.element_subset = None
	
	# restore previous out file
	pinfo.out_file = current_out_file
	pinfo.out_file.write('\n{}source {}\n'.format(pinfo.indent, node_file_name))
	pinfo.out_file.write('\n{}source {}\n'.format(pinfo.indent, element_file_name))
	pinfo.out_file.write('\n{}domainChange\n'.format(pinfo.indent))
	
	# done
	pinfo.out_file.write('\n')