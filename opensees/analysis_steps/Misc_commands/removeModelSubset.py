import os
from PyMpc import *
from mpc_utils_html import *
from itertools import groupby, count
import opensees.utils.tcl_input as tclin
import opensees.utils.write_element as write_element
import opensees.utils.write_node as write_node

'''
@TODO:
- we do not consider auto-generated-element data. It will be included as soon as we also add nodes
  to auto-generated-element data.
'''

def makeXObjectMetaData():
	
	remove_set = MpcAttributeMetaData()
	remove_set.type = MpcAttributeType.IndexVector
	remove_set.name = 'Remove'
	remove_set.group = 'Data'
	remove_set.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Remove')+'<br/>') + 
		html_par(
			'Select one or more Selection Sets.<br/>'
			'All elements in this selection set will be removed.<br/>'
			'Nodes in this selection set will be removed if they do not belong to any '
			'Selection Set in "Keep"') +
		html_end()
		)
	remove_set.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	keep_set = MpcAttributeMetaData()
	keep_set.type = MpcAttributeType.IndexVector
	keep_set.name = 'Keep'
	keep_set.group = 'Data'
	keep_set.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Remove')+'<br/>') + 
		html_par(
			'Select one or more Selection Sets.<br/>'
			'Nodes in this selection will not be removed even if they '
			'belong to some Selection Set in "Remove"') +
		html_end()
		)
	keep_set.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	xom = MpcXObjectMetaData()
	xom.name = 'removeModelSubset'
	xom.addAttribute(remove_set)
	xom.addAttribute(keep_set)
	
	return xom

def _process_sets(doc, sets):
	nodes = []
	eles = []
	# process a list of elements
	def process_domain(domain):
		for elem in domain.elements:
			# add current element
			if not elem.id in eles:
				eles.append(elem.id)
			# process all nodes of this element
			for node in elem.nodes:
				if not node.id in nodes:
					nodes.append(node.id)
	# process all selection sets
	for selection_set_id in sets:
		selection_set = doc.selectionSets[selection_set_id]
		# process all geometry subsets
		for geometry_id, geometry_subset in selection_set.geometries.items():
			# get associated mesh
			mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
			# process all vertices
			for vertex_id in geometry_subset.vertices:
				node = mesh_of_geom.vertices[vertex_id]
				if not node.id in nodes:
					nodes.append(node.id)
			# process all edges
			for domain_id in geometry_subset.edges:
				domain = mesh_of_geom.edges[domain_id];
				process_domain(domain)
			# process all faces
			for domain_id in geometry_subset.faces:
				domain = mesh_of_geom.faces[domain_id]
				process_domain(domain)
			# process all solids
			for domain_id in geometry_subset.solids:
				domain = mesh_of_geom.solids[domain_id]
				process_domain(domain)
		# process all interaction subsets
		for interaction_id in selection_set.interactions:
			# get associated mesh
			mesh_of_inter = doc.mesh.meshedInteractions[interaction_id]
			# even if it is not a domain, in the process_domain we only access the "elements" property
			# which is present also in mesh_of_inter
			process_domain(mesh_of_inter)
	# done
	return (nodes, eles)

def _write(f, indent, nodes, eles):
	# write a list of elements
	if(len(eles) > 0):
		f.write('{0}# elements to be removed\n'.format(indent))
		f.write('{0}set remove_elements {{\\\n{0}{0}'.format(indent))
		counter = 0
		n = len(eles)
		for j in range(n):
			i = eles[j]
			f.write(' {}'.format(i))
			counter += 1
			if counter == 10 and j != n-1:
				f.write('\\\n{0}{0}'.format(indent))
				counter = 0
		f.write('}}\n'.format(indent))
		f.write('{}foreach ele_id $remove_elements {{ remove element $ele_id }}\n'.format(indent))
	# write a list of nodes
	if(len(nodes) > 0):
		f.write('{0}# nodes to be removed\n'.format(indent))
		f.write('{0}set remove_nodes {{\\\n{0}{0}'.format(indent))
		counter = 0
		n = len(nodes)
		for j in range(n):
			i = nodes[j]
			f.write(' {}'.format(i))
			counter += 1
			if counter == 10 and j != n-1:
				f.write('\\\n{0}{0}'.format(indent))
				counter = 0
		f.write('}}\n'.format(indent))
		f.write('{}foreach node_id $remove_nodes {{ remove node $node_id }}\n'.format(indent))

def writeTcl(pinfo):
	
	# get xobject and its parent component id
	xobj = pinfo.analysis_step.XObject
	
	# get the document
	doc = App.caeDocument()
	pdata = doc.mesh.partitionData
	is_partitioned = (len(pdata.partitions) > 1)
	
	# write a comment
	pinfo.out_file.write('\n{}# removeModelSubset [{}] {}\n'.format(
		pinfo.indent, xobj.parent.componentId, xobj.parent.componentName))
	
	# sets to be removed
	remove_sets = xobj.getAttribute('Remove')
	if(remove_sets is None):
		raise Exception('Error: cannot find "Remove" attribute')
	
	# sets to be kept
	keep_sets = xobj.getAttribute('Keep')
	if(keep_sets is None):
		raise Exception('Error: cannot find "Keep" attribute')
	
	# a list of nodes to be kept
	keep_nodes, _ = _process_sets(doc, keep_sets.indexVector)
	
	# a list of elements and nodes to be removed
	rem_nodes, rem_eles = _process_sets(doc, remove_sets.indexVector)
	
	# remove nodes to be kept
	rem_nodes = [i for i in rem_nodes if not i in keep_nodes]
	
	# quick return
	if len(rem_nodes) == 0 and len(rem_eles) == 0:
		return
	
	# write for sequential or partitioned models
	if is_partitioned:
		for process_id in range(len(pdata.partitions)):
			rem_nodes_p = [i for i in rem_nodes if pdata.isNodeOnParition(i, process_id)]
			rem_eles_p = [i for i in rem_eles if pdata.elementPartition(i) == process_id]
			if len(rem_nodes_p) + len(rem_eles_p) > 0:
				pinfo.setProcessId(process_id)
				pinfo.out_file.write('{}if {{$process_id == {}}} {{\n'.format(pinfo.indent, process_id))
				_write(pinfo.out_file, '{}{}'.format(pinfo.indent, pinfo.tabIndent), rem_nodes_p, rem_eles_p)
				pinfo.out_file.write('{}}}\n'.format(pinfo.indent))
				pinfo.setProcessId(0)
	else:
		_write(pinfo.out_file, pinfo.indent, rem_nodes, rem_eles)
	
	# done, run a domainChange in all partitions
	pinfo.out_file.write('\n{}domainChange\n'.format(pinfo.indent))