from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute
	
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
			'Select all selection sets whose nodes (or elements) '
			'are to be used for the parameter command.<br/>'
			''
			)) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parameter_Command','Parameter command')+'<br/>') +
		html_end()
		)
	at_SelectionSets.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	# autoGen
	at_autoGen = MpcAttributeMetaData()
	at_autoGen.type = MpcAttributeType.Boolean
	at_autoGen.name = 'Include Auto-Generated Elements'
	at_autoGen.group = 'SelectionSets'
	at_autoGen.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Include Auto-Generated Elements')+'<br/>') +
		html_par((
			'Some automations in STKO will automatically generate extra elements not visible in STKO (see for example the HingedBeam).<br/>'
			'When this flag is True (Default), the auto-generated elements will be considered.'
			''
			)) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parameter_Command','Parameter command')+'<br/>') +
		html_end()
		)
	at_autoGen.setDefault(True)
	
	# Type
	at_Type = MpcAttributeMetaData()
	at_Type.type = MpcAttributeType.String
	at_Type.name = 'Type'
	at_Type.group = 'Data'
	at_Type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Parameter')+'<br/>') + 
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parameter_Command','Parameter command')+'<br/>') +
		html_end()
		)
	at_Type.sourceType = MpcAttributeSourceType.List
	at_Type.setSourceList(['node', 'element'])
	at_Type.setDefault('element')

	# useRandomVariable
	at_useRandomVariable = MpcAttributeMetaData()
	at_useRandomVariable.type = MpcAttributeType.Boolean
	at_useRandomVariable.name = '-randomVariable'
	at_useRandomVariable.group = 'Data'
	at_useRandomVariable.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Parameter')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parameter_Command','Parameter command')+'<br/>') +
		html_end()
		)
	at_useRandomVariable.setDefault(False)

	# randomVariableIndex
	at_rvTag = MpcAttributeMetaData()
	at_rvTag.type = MpcAttributeType.Index
	at_rvTag.name = 'rvTag'
	at_rvTag.group = '-randomVariable'
	at_rvTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Parameter')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parameter_Command','Parameter command')+'<br/>') +
		html_end()
		)
	at_rvTag.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_rvTag.indexSource.addAllowedNamespace("randomVariable")
	
	# Arguments
	at_Arguments = MpcAttributeMetaData()
	at_Arguments.type = MpcAttributeType.String
	at_Arguments.name = 'Specific object arguments'
	at_Arguments.group = 'Data'
	at_Arguments.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Specific object arguments')+'<br/>') + 
		html_par('e.g.:<br/>hPerm') +
		html_end()
		)
	at_Arguments.setDefault('')
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'parameter'
	xom.addAttribute(at_SelectionSets)
	xom.addAttribute(at_autoGen)
	xom.addAttribute(at_Type)
	xom.addAttribute(at_useRandomVariable)
	xom.addAttribute(at_rvTag)
	xom.addAttribute(at_Arguments)
	
	# randomVariable dependency
	xom.setVisibilityDependency(at_useRandomVariable, at_rvTag)
	
	return xom

def writeTcl(pinfo):
	
	# parameter $tag <specific object arguments>
	# addToParameter $tag <specific object arguments>
	
	xobj = pinfo.analysis_step.XObject
	tag_add_to_parameter =  xobj.parent.id
	
	FileName = xobj.name
	if pinfo.currentDescription != FileName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, FileName))
		pinfo.currentDescription = FileName
	doc = App.caeDocument()
	
	Type_at = xobj.getAttribute('Type')
	if(Type_at is None):
		raise Exception('Error: cannot find "Type" attribute')
	Type = Type_at.string

	useRandomVariable = _get_xobj_attribute(xobj,'-randomVariable').boolean
	if useRandomVariable:
		rvTag = _get_xobj_attribute(xobj,'rvTag').index

	Arguments_at = xobj.getAttribute('Specific object arguments')
	if(Arguments_at is None):
		raise Exception('Error: cannot find "Specific object arguments" attribute')
	Arguments = Arguments_at.string
	
	SelectionSets_at = xobj.getAttribute('SelectionSets')
	if(SelectionSets_at is None):
		raise Exception('Error: cannot find "SelectionSets" attribute')
	SelectionSets = SelectionSets_at.indexVector
	
	auto_gen_at = xobj.getAttribute('Include Auto-Generated Elements')
	if auto_gen_at is None:
		raise Exception('Error: cannot find "SInclude Auto-Generated Elements" attribute')
	auto_gen = auto_gen_at.boolean
	
	str_addToParameter = []
	tag = pinfo.tag_parameter
	Indent =  pinfo.tabIndent
	
	# for element
	
	# elements for parameter updating
	parameter_map_elem = []
	# maps auto-generated elements to source-element process id
	auto_gen_elements_pid_map = {}
	def add_elements_to_param(source_elements):
		for elem in source_elements:
			parameter_map_elem.append(elem.id)
			if auto_gen:
				# we need to include auto-generated elements
				aux_elements = pinfo.auto_generated_element_data_map.get(elem.id, None)
				source_pid = 0
				if pinfo.process_count > 1:
					source_pid = doc.mesh.partitionData.elementPartition(elem.id)
				if aux_elements is not None:
					for aux_ele_id in aux_elements.elements:
						# add this element to parametrized elements
						parameter_map_elem.append(aux_ele_id)
						# save its process id = source element process id
						if pinfo.process_count > 1:
							auto_gen_elements_pid_map[aux_ele_id] = source_pid
	if Type == "element":
		for selection_set_id in SelectionSets:
			if not selection_set_id in doc.selectionSets: continue
			selection_set = doc.selectionSets[selection_set_id]
			for geometry_id, geometry_subset in selection_set.geometries.items():
				mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
				for domain_id in geometry_subset.edges:
					domain = mesh_of_geom.edges[domain_id]
					add_elements_to_param(domain.elements)
				for domain_id in geometry_subset.faces:
					domain = mesh_of_geom.faces[domain_id]
					add_elements_to_param(domain.elements)
				for domain_id in geometry_subset.solids:
					domain = mesh_of_geom.solids[domain_id]
					add_elements_to_param(domain.elements)
		
		# parallel
		if pinfo.process_count > 1:
			process_block_count = 0
			pinfo.out_file.write('\n{}# parameter\n'.format(pinfo.indent))
			if useRandomVariable:
				pinfo.out_file.write('{}parameter {} randomVariable {}\n'.format(pinfo.indent, pinfo.tag_parameter, rvTag))
			else:
				pinfo.out_file.write('{}parameter {}\n'.format(pinfo.indent, pinfo.tag_parameter))
			for process_id in range(pinfo.process_count):
				first_done = False
				check = True
				for elem_id in parameter_map_elem:
					if elem_id in auto_gen_elements_pid_map:
						if auto_gen_elements_pid_map[elem_id] != process_id:
							continue
					else:
						if doc.mesh.partitionData.elementPartition(elem_id) != process_id:
							continue
					if (check):
						str_addToParameter.append('\n{}{}# addToParameter\n'.format(pinfo.indent, Indent))
						check = False
					pinfo.map_tag_add_to_parameter_id_partition[tag_add_to_parameter] = (pinfo.tag_parameter)
					if not first_done:
						if process_block_count == 0:
							pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
						else:
							pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
						first_done = True
				
					str_addToParameter.append('{}{}addToParameter {} {} {} {}\n'.format(pinfo.indent, Indent, pinfo.tag_parameter, Type, elem_id, Arguments))
				pinfo.out_file.write(''.join(str_addToParameter))
				str_addToParameter = []
		
				if first_done:
					process_block_count += 1
				if process_block_count > 0 and first_done:
					pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		# not parallel
		else:
			pinfo.out_file.write('\n{}# parameter\n'.format(pinfo.indent))
			if useRandomVariable:
				pinfo.out_file.write('{}parameter {} randomVariable {}\n'.format(pinfo.indent, pinfo.tag_parameter, rvTag))
			else:
				pinfo.out_file.write('{}parameter {}\n'.format(pinfo.indent, pinfo.tag_parameter))
			for elem_id in parameter_map_elem:
				pinfo.map_tag_add_to_parameter_id_partition[tag_add_to_parameter] = (pinfo.tag_parameter)
				str_addToParameter.append('{}addToParameter {} {} {} {}\n'.format(pinfo.indent, pinfo.tag_parameter, Type, elem_id, Arguments))
			pinfo.out_file.write('\n{}# addToParameter\n'.format(pinfo.indent))
			pinfo.out_file.write(''.join(str_addToParameter))
		
	# for node
	parameter_map_node = {}
	if Type == "node":
	
		for selection_set_id in SelectionSets:
			if not selection_set_id in doc.selectionSets: continue
			selection_set = doc.selectionSets[selection_set_id]
			for geometry_id, geometry_subset in selection_set.geometries.items():
				mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
			
				for domain_id in geometry_subset.edges:
					domain = mesh_of_geom.edges[domain_id]
					for elem in domain.elements:
						for node in elem.nodes:
							parameter_map_node[node.id] = tag
							
				for domain_id in geometry_subset.faces:
					domain = mesh_of_geom.faces[domain_id]
					for elem in domain.elements:
						for node in elem.nodes:
							parameter_map_node[node.id] = tag

				for domain_id in geometry_subset.solids:
					domain = mesh_of_geom.solids[domain_id]
					for elem in domain.elements:
						for node in elem.nodes:
							parameter_map_node[node.id] = tag
							
				for domain_id in geometry_subset.vertices:
					node = mesh_of_geom.vertices[domain_id]
					parameter_map_node[node.id] = tag
				
		# parallel
		if pinfo.process_count > 1:
			process_block_count = 0
			pinfo.out_file.write('\n{}# parameter\n'.format(pinfo.indent))
			if useRandomVariable:
				pinfo.out_file.write('{}parameter {} randomVariable {}\n'.format(pinfo.indent, pinfo.tag_parameter, rvTag))
			else:
				pinfo.out_file.write('{}parameter {}\n'.format(pinfo.indent, pinfo.tag_parameter))
			for process_id in range(pinfo.process_count):
				first_done = False
				check = True
				
				for node_id in parameter_map_node:
					if (node_id in pinfo.node_to_model_map):
						if not doc.mesh.partitionData.isNodeOnPartition(node_id, process_id):
							continue
						if (check):
							str_addToParameter.append('\n{}{}# addToParameter\n'.format(pinfo.indent, Indent))
							check = False
						pinfo.map_tag_add_to_parameter_id_partition[tag_add_to_parameter] = (pinfo.tag_parameter)
						if not first_done:
							if process_block_count == 0:
								pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
							else:
								pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
							first_done = True
					
						str_addToParameter.append('{}{}addToParameter {} {} {} {}\n'.format(pinfo.indent, Indent, pinfo.tag_parameter, Type, node_id, Arguments))
				pinfo.out_file.write(''.join(str_addToParameter))
				str_addToParameter = []
			
				if first_done:
					process_block_count += 1
				if process_block_count > 0 and first_done:
					pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		# not parallel
		else:
			pinfo.out_file.write('\n{}# parameter\n'.format(pinfo.indent))
			if useRandomVariable:
				pinfo.out_file.write('{}parameter {} randomVariable {}\n'.format(pinfo.indent, pinfo.tag_parameter, rvTag))
			else:
				pinfo.out_file.write('{}parameter {}\n'.format(pinfo.indent, pinfo.tag_parameter))
			for node_id in parameter_map_node:
				pinfo.map_tag_add_to_parameter_id_partition[tag_add_to_parameter] = (pinfo.tag_parameter)
				str_addToParameter.append('{}addToParameter {} {} {} {}\n'.format(pinfo.indent, pinfo.tag_parameter, Type, node_id, Arguments))
			pinfo.out_file.write('\n{}# addToParameter\n'.format(pinfo.indent))
			pinfo.out_file.write(''.join(str_addToParameter))
			
	pinfo.tag_parameter = tag+1;
