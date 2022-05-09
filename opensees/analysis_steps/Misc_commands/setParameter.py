import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def _err(msg):
	return 'Error in "setParameter" :\n{}'.format(msg)

def _geta(xobj, name):
	a = xobj.getAttribute(name)
	if a is None:
		raise Exception('Error in setParameter: cannot find "{}" attribute'.format(name))
	return a

def makeXObjectMetaData():
	
	def mka(type, name, group, descr):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parameter_Command','Parameter command')+'<br/>') +
			html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parameter_Command','Parameter command')+'<br/>') +
			html_end()
			)
		return a
	
	sset = mka(MpcAttributeType.IndexVector, 'SelectionSets', 'Selection',
		'All selection sets whose elements are to be used for the parameter command.')
	sset.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	auto_gen = mka(MpcAttributeType.Boolean, 'Include Auto-Generated Elements', 'Selection',
		('Some automations in STKO will automatically generate extra elements not visible in STKO (see for example the HingedBeam).<br/>'
		'When this flag is True (Default), the auto-generated elements will be considered.'))
	auto_gen.setDefault(True)
	
	
	pmode = mka(MpcAttributeType.String, 'Parameter Mode', 'Parameter',
		('The approach for updating the parameter:<br/>'
		'<ul>'
		'<li><strong>Constant</strong>: You can specify the parameter name and a constant value</li>'
		'<li><strong>From Table</strong>: You can specify a Random Material Table file, with material points. Each element will have the parameters of the nearest point.</li>'
		'</ul>'))
	pmode.sourceType = MpcAttributeSourceType.List
	pmode.setSourceList(['Constant','From Table'])
	pmode.setDefault('Constant')
	param = mka(MpcAttributeType.String, 'Parameter Name', 'Parameter',
		'The parameter name you want to update')
	value = mka(MpcAttributeType.Real, 'Parameter New Value', 'Parameter',
		'The new value of the parameter')
	table = mka(MpcAttributeType.String, 'Table File', 'Parameter', 'The random material table file')
	table.stringType = 'OpenFilePath All supported files (*.rmt *.txt);;Random Material Table (*.rmt);;Text files (*.txt);;All files (*.* *)'
	
	xom = MpcXObjectMetaData()
	xom.name = 'setParameter'
	xom.addAttribute(sset)
	xom.addAttribute(auto_gen)
	xom.addAttribute(pmode)
	xom.addAttribute(param)
	xom.addAttribute(value)
	xom.addAttribute(table)
	return xom

def onEditBegin(editor, xobj):
	onAttributeChanged(editor, xobj, 'Parameter Mode')

def onAttributeChanged(editor, xobj, attribute_name):
	attribute = _geta(xobj, attribute_name)
	if attribute:
		if attribute.name == 'Parameter Mode':
			table = _geta(xobj, 'Table File')
			param = _geta(xobj, 'Parameter Name')
			value = _geta(xobj, 'Parameter New Value')
			type = attribute.string
			if type == 'From Table':
				table.visible = True
				param.visible = False
				value.visible = False
			elif type == 'Constant':
				table.visible = False
				param.visible = True
				value.visible = True

def writeTcl(pinfo):
	
	from io import StringIO
	import opensees.utils.RandomMaterialTable as RMT
	import os
	from datetime import datetime
	import numpy as np
	
	# get document
	doc = App.caeDocument()
	
	# get input
	xobj = pinfo.analysis_step.XObject
	sset = _geta(xobj, 'SelectionSets').indexVector
	auto_gen = _geta(xobj, 'Include Auto-Generated Elements').boolean
	pmode = _geta(xobj, 'Parameter Mode').string
	
	# get elements from selection sets
	parameter_map_elem = [] # elements for parameter updating
	auto_gen_elements_pid_map = {} # maps auto-generated elements to source-element process id
	auto_gen_elements_conn_map = {} # maps auto-generated elements to their connectivity (if provided)
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
					num_eles = len(aux_elements.elements)
					num_conn = len(aux_elements.elements_connectivity)
					for aux_ele_counter in range(num_eles):
						aux_ele_id = aux_elements.elements[aux_ele_counter]
						# add this element to parametrized elements
						parameter_map_elem.append(aux_ele_id)
						# save its process id = source element process id
						if pinfo.process_count > 1:
							auto_gen_elements_pid_map[aux_ele_id] = source_pid
						# save its connectivity
						if num_eles == num_conn:
							auto_gen_elements_conn_map[aux_ele_id] =  aux_elements.elements_connectivity[aux_ele_counter]
	for selection_set_id in sset:
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
		for interaction_id in selection_set.interactions:
			mesh_of_inter = doc.mesh.meshedInteractions[interaction_id]
			add_elements_to_param(mesh_of_inter.elements)
	
	# split elements by partitions if necessary
	pid_element_map = {}
	if pinfo.process_count > 1:
		for ele_id in parameter_map_elem:
			if not ele_id in auto_gen_elements_pid_map:
				pid = doc.mesh.partitionData.elementPartition(ele_id)
				pid_values = pid_element_map.get(pid, None)
				if pid_values is None:
					pid_values = []
					pid_element_map[pid] = pid_values
				pid_values.append(ele_id)
		for ele_id, pid in auto_gen_elements_pid_map.items():
			pid_values = pid_element_map.get(pid, None)
			if pid_values is None:
				pid_values = []
				pid_element_map[pid] = pid_values
			pid_values.append(ele_id)
	else:
		pid_element_map[0] = parameter_map_elem
	
	# process based on parameter mode
	if pmode == 'From Table':
		
		# get parameters
		fname = _geta(xobj, 'Table File').string
		
		# comment
		pinfo.out_file.write('\n{}# setParameter ({})\n'.format(pinfo.indent, fname))
		
		# create the RMT
		if not os.path.isabs(fname):
			fname = os.path.join(pinfo.out_dir, fname)
		rmt = RMT.RMT(fname)
		
		# compute element centers
		# in a numpy Nx3 matrix
		NC = len(parameter_map_elem)
		EC = np.zeros((NC, 3))
		for i in range(NC):
			ele_id = parameter_map_elem[i]
			element = doc.mesh.getElement(ele_id)
			if element:
				# the element exists in STKO
				ic = element.computeCenter()
				EC[i,0] = ic.x
				EC[i,1] = ic.y
				EC[i,2] = ic.z
			else:
				# it can be an auto-generated element
				econn = auto_gen_elements_conn_map.get(ele_id, None)
				if econn and len(econn) > 0: # otherwise leave zeros...
					icx = 0.0
					icy = 0.0
					icz = 0.0
					for nid, npos in econn:
						icx += npos[0]
						icy += npos[1]
						icz += npos[2]
					nconn = float(len(econn))
					icx /= nconn
					icy /= nconn
					icz /= nconn
					EC[i,0] = icx
					EC[i,1] = icy
					EC[i,2] = icz
		
		# find, for each center, the 0-based position of the nearest material point
		print('setParameter ({})'.format(pinfo.analysis_step.id))
		print('    Finding nearest material points. This may take a while...')
		T1 = datetime.now()
		_, nearest_pos = rmt.tree.query(EC)
		T2 = datetime.now()
		print('    Elapsed time: {} seconds'.format((T2-T1).total_seconds()))
		
		# create a map from ele_id to nearest_pos
		ele_nearest_pos_map = {}
		for i in range(NC):
			ele_id = parameter_map_elem[i]
			ele_nearest_pos = nearest_pos[i]
			ele_nearest_pos_map[ele_id] = ele_nearest_pos
		
		# map rmt material ids to material data
		mat_map = {}
		for i in range(len(rmt.mat_id)):
			mat_map[rmt.mat_id[i]] = rmt.mat_data[i]
		
		# arguments
		args = rmt.args
		nargs = len(args)
		
		# create an auxiliary file
		param_file_name = 'setParameter_{}.tcl'.format(pinfo.analysis_step.id)
		pinfo.out_file.write('{}source {}\n'.format(pinfo.indent, param_file_name))
		with open('{}/{}'.format(pinfo.out_dir, param_file_name), 'w+') as param_file:
			# check partitions
			if pinfo.process_count > 1:
				for pid, elements in pid_element_map.items():
					if len(elements) > 0:
						param_file.write('if {{$process_id == {}}} {{\n'.format(pid))
						for ele_id in elements:
							ele_nearest_pos = ele_nearest_pos_map[ele_id]
							mat_values = mat_map[rmt.mat_point_ids[ele_nearest_pos]]
							for i in range(nargs):
								iarg = args[i]
								ival = mat_values[i]
								param_file.write('{}setParameter -val {} -ele {} "{}"\n'.format(pinfo.tabIndent, ival, ele_id, iarg))
						param_file.write('}\n')
			else:
				elements = pid_element_map[0]
				for ele_id in elements:
					ele_nearest_pos = ele_nearest_pos_map[ele_id]
					mat_values = mat_map[rmt.mat_point_ids[ele_nearest_pos]]
					for i in range(nargs):
						iarg = args[i]
						ival = mat_values[i]
						param_file.write('setParameter -val {} -ele {} "{}"\n'.format(ival, ele_id, iarg))
		
	else:
		
		# get parameters
		param = _geta(xobj, 'Parameter Name').string
		value = _geta(xobj, 'Parameter New Value').real
		
		# make command string
		def commandstring(eles, indent, param, value):
			stream = StringIO()
			stream.write('{}setParameter -val {} -ele \\\n'.format(indent, value))
			count = 0
			n = len(eles)
			for i in range(n):
				count += 1
				if count == 1:
					stream.write('{}{}'.format(indent, pinfo.tabIndent))
				stream.write('{} '.format(eles[i]))
				if count == 10 and i < n-1:
					count = 0
					stream.write('\\\n')
			stream.write(' {}\n'.format(param))
			return stream.getvalue()
		
		# comment
		pinfo.out_file.write('\n{}# setParameter ({}) = {}\n'.format(pinfo.indent, param, value))
		
		# check partitions
		if pinfo.process_count > 1:
			for pid, values in pid_element_map.items():
				if len(values) > 0:
					pinfo.out_file.write('{}if {{$process_id == {}}} {{\n'.format(pinfo.indent, pid))
					pinfo.out_file.write(commandstring(values, pinfo.indent+pinfo.tabIndent, param, value))
					pinfo.out_file.write('{}}}\n'.format(pinfo.indent))
		else:
			values = pid_element_map[0]
			if len(values) > 0:
				pinfo.out_file.write(commandstring(values, pinfo.indent, param, value))