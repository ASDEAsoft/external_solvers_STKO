import PyMpc.Units as u
from PyMpc import *
import PyMpc.App
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import shutil
import os
import glob
import sys

class _monitor_globals:
	
	STR_ARGS = 'step_id dt T n_iter norm perc STKO_VAR_process_id STKO_VAR_is_parallel'
	STR_ARGS_REF = ' '.join(['${}'.format(w) for w in STR_ARGS.split(' ')])
	
	MAP_COMP_T = {'X':1, 'Y':2, 'Z':3}
	MAP_COMP_R = {'X':4, 'Y':5, 'Z':6}
	MAP_RES_COMP = ({
		'Displacement':('nodeDisp', MAP_COMP_T),
		'Rotation':('nodeDisp', MAP_COMP_R),
		'Velocity':('nodeVel', MAP_COMP_T),
		'Angular Velocity':('nodeVel', MAP_COMP_R),
		'Acceleration':('nodeAccel', MAP_COMP_T),
		'Angular Acceleration':('nodeAccel', MAP_COMP_R),
		'Reaction Force':('nodeReaction', MAP_COMP_T),
		'Reaction Moment':('nodeReaction', MAP_COMP_R),
	})
	
	# Massimo: added 5/11/2021. When a node is in more that 1 partition,
	# each partition value, by default, is accumulated to the others (SUM).
	# this is fine for results such as reactions in a domain decomposition,
	# but not for results such as displacements!
	MAP_RES_PARALLEL_AVG = ('nodeDisp', 'nodeVel', 'nodeAccel')

def __get_domain_nodes(domain, tags):
	for element in domain.elements:
		for node in element.nodes:
			tags.append(node.id)

def __get_set_nodes(doc, sset):
	tags = []
	for geometry_id, geometry_subset in sset.geometries.items():
		mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
		for domain_id in geometry_subset.edges:
			domain = mesh_of_geom.edges[domain_id]
			__get_domain_nodes(domain, tags)
		for domain_id in geometry_subset.faces:
			domain = mesh_of_geom.faces[domain_id]
			__get_domain_nodes(domain, tags)
		for domain_id in geometry_subset.solids:
			domain = mesh_of_geom.solids[domain_id]
			__get_domain_nodes(domain, tags)
		for domain_id in geometry_subset.vertices:
			node = mesh_of_geom.vertices[domain_id]
			tags.append(node.id)
	tags = list(set(tags))
	return tags

def makeXObjectMetaData():
	
	# do_plot Boolean
	# crea attributo int NODE_ID; DOF_ID (1-nnn); RESULT
	# plot
	at_plot = MpcAttributeMetaData()
	at_plot.type = MpcAttributeType.Boolean
	at_plot.name = 'Monitor Plot'
	at_plot.group = 'Monitor Plot'
	
	# custom-name
	at_cname_use = MpcAttributeMetaData()
	at_cname_use.type = MpcAttributeType.Boolean
	at_cname_use.name = 'Use Custom Name'
	at_cname_use.group = 'Custom Name'
	at_cname_use.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Use Custom Name')+'<br/>') + 
		html_par('If this flag is set to False (Default) the monitor output files will have the following default name:<br/>.'
				'STKO_plot_monitorX.plt, where X is the ID of the monitor AnalysisStep in STKO.<br/>Otherwise you can specify a custom name')+
		html_end()
		)
	at_cname_use.setDefault(False)
	at_cname = MpcAttributeMetaData()
	at_cname.type = MpcAttributeType.String
	at_cname.name = 'Custom Name'
	at_cname.group = 'Custom Name'
	at_cname.setDefault('MonitorCustomName')
	
	# typeXPlot
	at_typeXPlot = MpcAttributeMetaData()
	at_typeXPlot.type = MpcAttributeType.String
	at_typeXPlot.name = 'Type/X'
	at_typeXPlot.group = 'Plot X Axis'
	at_typeXPlot.sourceType = MpcAttributeSourceType.List
	at_typeXPlot.setSourceList(['Time Step ID', 'Pseudo Time', 'Results X Axis Plot'])
	at_typeXPlot.setDefault('Time Step ID')
	#boolean Results Xplot
	at_resultsXPlot = MpcAttributeMetaData()
	at_resultsXPlot.type = MpcAttributeType.Boolean
	at_resultsXPlot.name = 'Results X Axis Plot'
	at_resultsXPlot.group = 'Plot X Axis'
	at_resultsXPlot.editable = False
	#type Xresult
	at_typeXResult = MpcAttributeMetaData()
	at_typeXResult.type = MpcAttributeType.String
	at_typeXResult.name = 'Result/X'
	at_typeXResult.group = 'Plot X Axis'
	at_typeXResult.sourceType = MpcAttributeSourceType.List
	at_typeXResult.setSourceList(['Displacement', 'Rotation', 'Velocity', 'Angular Velocity', 'Acceleration', 'Angular Acceleration', 'Reaction Force', 'Reaction Moment'])
	at_typeXResult.setDefault('Displacement')
	#node plot X
	at_node_idX = MpcAttributeMetaData()
	at_node_idX.type = MpcAttributeType.Index
	at_node_idX.name = 'Selection Set/X'
	at_node_idX.group = 'Plot X Axis'
	at_node_idX.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	#component X
	at_DOFXResult = MpcAttributeMetaData()
	at_DOFXResult.type = MpcAttributeType.String
	at_DOFXResult.name = 'Component/X'
	at_DOFXResult.group = 'Plot X Axis'
	at_DOFXResult.sourceType = MpcAttributeSourceType.List
	at_DOFXResult.setSourceList(['X', 'Y', 'Z'])
	at_DOFXResult.setDefault('X')
	#operation X
	at_operationX = MpcAttributeMetaData()
	at_operationX.type = MpcAttributeType.String
	at_operationX.name = 'Operation/X'
	at_operationX.group = 'Plot X Axis'
	at_operationX.sourceType = MpcAttributeSourceType.List
	at_operationX.setSourceList(['Sum', 'Average', 'Maximum', 'Minimum'])
	at_operationX.setDefault('Sum')
	# Scale factor X
	at_scaleX = MpcAttributeMetaData()
	at_scaleX.type = MpcAttributeType.Real
	at_scaleX.name = 'ScaleFactor/X'
	at_scaleX.group = 'Plot X Axis'
	at_scaleX.setDefault(1.0)
	# Add X axis
	at_addX = MpcAttributeMetaData()
	at_addX.type = MpcAttributeType.Real
	at_addX.name = 'Add/X'
	at_addX.group = 'Plot X Axis'
	at_addX.setDefault(0.0)

	# typeYPlot
	at_typeYPlot = MpcAttributeMetaData()
	at_typeYPlot.type = MpcAttributeType.String
	at_typeYPlot.name = 'Type/Y'
	at_typeYPlot.group = 'Plot Y Axis'
	at_typeYPlot.sourceType = MpcAttributeSourceType.List
	at_typeYPlot.setSourceList(['Time Step ID', 'Pseudo Time', 'Results Y Axis Plot'])
	at_typeYPlot.setDefault('Results Y Axis Plot')
	#boolean Results Yplot
	at_resultsYPlot = MpcAttributeMetaData()
	at_resultsYPlot.type = MpcAttributeType.Boolean
	at_resultsYPlot.name = 'Results Y Axis Plot'
	at_resultsYPlot.group = 'Plot Y Axis'
	at_resultsYPlot.editable = False
	#type Yresult
	at_typeYResult = MpcAttributeMetaData()
	at_typeYResult.type = MpcAttributeType.String
	at_typeYResult.name = 'Result/Y'
	at_typeYResult.group = 'Plot Y Axis'
	at_typeYResult.sourceType = MpcAttributeSourceType.List
	at_typeYResult.setSourceList(['Displacement', 'Rotation', 'Velocity', 'Angular Velocity', 'Acceleration', 'Angular Acceleration', 'Reaction Force','Reaction Moment'])
	at_typeYResult.setDefault('Displacement')
	#node plot
	at_node_idY = MpcAttributeMetaData()
	at_node_idY.type = MpcAttributeType.Index
	at_node_idY.name = 'Selection Set/Y'
	at_node_idY.group = 'Plot Y Axis'
	at_node_idY.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	#dof
	at_DOFYResult = MpcAttributeMetaData()
	at_DOFYResult.type = MpcAttributeType.String
	at_DOFYResult.name = 'Component/Y'
	at_DOFYResult.group = 'Plot Y Axis'
	at_DOFYResult.sourceType = MpcAttributeSourceType.List
	at_DOFYResult.setSourceList(['X', 'Y', 'Z'])
	at_DOFYResult.setDefault('X')
	#operation Y
	at_operationY = MpcAttributeMetaData()
	at_operationY.type = MpcAttributeType.String
	at_operationY.name = 'Operation/Y'
	at_operationY.group = 'Plot Y Axis'
	at_operationY.sourceType = MpcAttributeSourceType.List
	at_operationY.setSourceList(['Sum', 'Average', 'Maximum', 'Minimum'])
	at_operationY.setDefault('Sum')
	# Scale factor Y
	at_scaleY = MpcAttributeMetaData()
	at_scaleY.type = MpcAttributeType.Real
	at_scaleY.name = 'ScaleFactor/Y'
	at_scaleY.group = 'Plot Y Axis'
	at_scaleY.setDefault(1.0)
	# Add Y axis
	at_addY = MpcAttributeMetaData()
	at_addY.type = MpcAttributeType.Real
	at_addY.name = 'Add/Y'
	at_addY.group = 'Plot Y Axis'
	at_addY.setDefault(0.0)

	#background Plot
	at_BackPlot = MpcAttributeMetaData()
	at_BackPlot.type = MpcAttributeType.Boolean
	at_BackPlot.name = 'Background Plot'
	at_BackPlot.group = 'Background Plot'
	at_XBackPlot = MpcAttributeMetaData()
	at_XBackPlot.type = MpcAttributeType.QuantityVector
	at_XBackPlot.name = 'X Axis'
	at_XBackPlot.group = 'Background Plot'
	at_YBackPlot = MpcAttributeMetaData()
	at_YBackPlot.type = MpcAttributeType.QuantityVector
	at_YBackPlot.name = 'Y Axis'
	at_YBackPlot.group = 'Background Plot'
	
	# Misc
	at_XLabelAppend = MpcAttributeMetaData()
	at_XLabelAppend.type = MpcAttributeType.String
	at_XLabelAppend.name = 'XLabelAppend'
	at_XLabelAppend.group = 'Misc'
	at_YLabelAppend = MpcAttributeMetaData()
	at_YLabelAppend.type = MpcAttributeType.String
	at_YLabelAppend.name = 'YLabelAppend'
	at_YLabelAppend.group = 'Misc'

	#attribute Plot X
	xom = MpcXObjectMetaData()
	xom.name = 'monitor'
	xom.addAttribute(at_plot)
	
	xom.addAttribute(at_cname_use)
	xom.addAttribute(at_cname)
	xom.setVisibilityDependency(at_plot, at_cname_use)
	xom.setVisibilityDependency(at_plot, at_cname)
	xom.setVisibilityDependency(at_cname_use, at_cname)

	xom.addAttribute(at_typeXPlot)
	xom.addAttribute(at_resultsXPlot)
	xom.addAttribute(at_typeXResult)
	xom.addAttribute(at_DOFXResult)
	xom.addAttribute(at_node_idX)
	xom.addAttribute(at_operationX)
	xom.addAttribute(at_scaleX)
	xom.addAttribute(at_addX)

	xom.addAttribute(at_typeYPlot)
	xom.addAttribute(at_resultsYPlot)
	xom.addAttribute(at_typeYResult)
	xom.addAttribute(at_DOFYResult)
	xom.addAttribute(at_node_idY)
	xom.addAttribute(at_operationY)
	xom.addAttribute(at_scaleY)
	xom.addAttribute(at_addY)

	xom.addAttribute(at_BackPlot)
	xom.addAttribute(at_XBackPlot)
	xom.addAttribute(at_YBackPlot)
	
	xom.addAttribute(at_XLabelAppend)
	xom.addAttribute(at_YLabelAppend)

	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Type/X'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Result/X'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Component/X'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Selection Set/X'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Operation/X'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('ScaleFactor/X'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Add/X'))

	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Type/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Result/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Component/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Selection Set/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Operation/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('ScaleFactor/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Add/Y'))

	xom.setVisibilityDependency(xom.getAttribute('Monitor Plot'), xom.getAttribute('Background Plot'))

	xom.setBooleanAutoExclusiveDependency(at_typeXPlot, at_resultsXPlot)
	xom.setVisibilityDependency(xom.getAttribute('Results X Axis Plot'), xom.getAttribute('Result/X'))
	xom.setVisibilityDependency(xom.getAttribute('Results X Axis Plot'), xom.getAttribute('Component/X'))
	xom.setVisibilityDependency(xom.getAttribute('Results X Axis Plot'), xom.getAttribute('Selection Set/X'))
	xom.setVisibilityDependency(xom.getAttribute('Results X Axis Plot'), xom.getAttribute('Operation/X'))
	xom.setVisibilityDependency(xom.getAttribute('Results X Axis Plot'), xom.getAttribute('ScaleFactor/X'))
	xom.setVisibilityDependency(xom.getAttribute('Results X Axis Plot'), xom.getAttribute('Add/X'))

	xom.setBooleanAutoExclusiveDependency(at_typeYPlot, at_resultsYPlot)
	xom.setVisibilityDependency(xom.getAttribute('Results Y Axis Plot'), xom.getAttribute('Result/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Results Y Axis Plot'), xom.getAttribute('Component/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Results Y Axis Plot'), xom.getAttribute('Selection Set/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Results Y Axis Plot'), xom.getAttribute('Operation/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Results Y Axis Plot'), xom.getAttribute('ScaleFactor/Y'))
	xom.setVisibilityDependency(xom.getAttribute('Results Y Axis Plot'), xom.getAttribute('Add/Y'))

	xom.setVisibilityDependency(xom.getAttribute('Background Plot'), xom.getAttribute('X Axis'))
	xom.setVisibilityDependency(xom.getAttribute('Background Plot'), xom.getAttribute('Y Axis'))

	return xom


def _get_plot_name(xobj):
	if xobj.getAttribute('Use Custom Name').boolean:
		name = xobj.getAttribute('Custom Name').string
		if name.strip():
			return name
		else:
			raise Exception('STKOMonitor Error: Please provide a valid (non empty) Custom Name')
	else:
		return 'STKO_plot_monitor{}'.format(xobj.parent.componentId)

def writeTcl(pinfo):
	
	# first checks
	
	xobj = pinfo.analysis_step.XObject
	
	doc = PyMpc.App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	is_par = (pinfo.process_count > 1)
	
	# some utilities
	
	def geta(name):
		a = xobj.getAttribute(name)
		if a is None:
			raise Exception('Cannot find attribute "{}"'.format(name))
		return a
	
	def writeBackgroundPlot(xLabel, yLabel):
		with open("{}/{}.pltbg".format(pinfo.out_dir, _get_plot_name(xobj)), "w") as f:
			f.write('{}\t{}\n'.format(xLabel, yLabel))
			for i in range (n):
				f.write('{}\t {}\n'.format(xAxis.valueAt(i), yAxis.valueAt(i)))
	
	def nodePartitions(node_id):
		partitions = []
		for process_id in range(pinfo.process_count):
			if doc.mesh.partitionData.isNodeOnParition(node_id, process_id):
				partitions.append(process_id)
		return partitions
	
	def nodePartitionsPairString(node_id):
		partitions = nodePartitions(node_id)
		return '{} {{{}}}'.format(node_id, ' '.join( [str(pid) for pid in partitions] ))
	
	# quick return
	if not geta("Monitor Plot").boolean:
		return
	
	# get monitor ID equal to the analysis_step id
	id_monitor = xobj.parent.componentId
	
	# get x y types and data
	type_nameX = geta('Type/X').string
	tcl_resX = ''
	tcl_componentX = ''
	xLabel = type_nameX
	xLabelAppend = geta('XLabelAppend').string
	if type_nameX == 'Results X Axis Plot':
		result = geta ('Result/X').string
		DOFX = geta ('Component/X').string
		xLabel = '{} ({})'.format(result, DOFX)
		tcl_cmd_comp_tuple_x = _monitor_globals.MAP_RES_COMP[result]
		tcl_resX = tcl_cmd_comp_tuple_x[0]
		tcl_componentX = tcl_cmd_comp_tuple_x[1][DOFX]
	type_nameY = geta('Type/Y').string
	tcl_resY = ''
	tcl_componentY = ''
	yLabel = type_nameY
	yLabelAppend = geta('YLabelAppend').string
	if type_nameY == 'Results Y Axis Plot':
		result = geta ('Result/Y').string
		DOFY = geta ('Component/Y').string
		yLabel = '{} ({})'.format(result, DOFY)
		tcl_cmd_comp_tuple_y = _monitor_globals.MAP_RES_COMP[result]
		tcl_resY = tcl_cmd_comp_tuple_y[0]
		tcl_componentY = tcl_cmd_comp_tuple_y[1][DOFY]
	if geta('Background Plot').boolean:
		xAxis = geta('X Axis').quantityVector
		nX = len(xAxis)
		yAxis = geta('Y Axis').quantityVector
		nY = len(yAxis)
		n = min (nX,nY)
		if n > 0:
			writeBackgroundPlot(xLabel + ' ' + xLabelAppend, yLabel + ' ' + yLabelAppend)

	# since we need them in a loop
	type_name = {'X':type_nameX, 'Y':type_nameY}
	tcl_res = {'X':tcl_resX, 'Y':tcl_resY}
	tcl_component = {'X':tcl_componentX, 'Y':tcl_componentY}
	
	# the output file
	f = pinfo.out_file
	
	# write a comment
	f.write('\n# Monitor Actor [{}]\n'.format(id_monitor))
	
	# write nodes and partitions here outside the monitor actor function
	# for each component...
	for COMP in ['X', 'Y']:
		itype = type_name[COMP]
		if itype == 'Results {} Axis Plot'.format(COMP):
			# get nodes from all selection set entitites
			sset_at = geta('Selection Set/{}'.format(COMP))
			sset = doc.selectionSets[sset_at.index]
			tags = __get_set_nodes(doc, sset)
			# write nodes and partition map if necessary
			f.write('set nodes_{}_{} {{{}}}\n'.format(COMP, id_monitor, ' '.join([ str(node_id) for node_id in tags ])))
			if is_par:
				f.write('set nodes_partitions_{}_{} [dict create {} ]\n'.format(
					COMP, id_monitor, ' '.join( [nodePartitionsPairString(node_id) for node_id in tags ])
				))
	
	# open the monitor actor function
	f.write('set MonitorActor{}_once_flag 0\n'.format(id_monitor))
	for COMP in ['X', 'Y']:
		itype = type_name[COMP]
		if itype == 'Time Step ID':
			f.write('set last_step_id_previous_stage_{0}_{1} 0\n'.format(COMP,id_monitor))
			f.write('set previous_step_id_{0}_{1} 1\n'.format(COMP,id_monitor))
			f.write('set previous_monitor_value_{0}_{1} 1\n'.format(COMP,id_monitor))
	f.write('proc MonitorActor{} {{{}}} {{\n'.format(id_monitor, _monitor_globals.STR_ARGS))
	f.write('\tglobal MonitorActor{}_once_flag\n'.format(id_monitor))
	
	# write commands for opening files and optionally computing reactions
	def plot_begin(indent):
		return (
			'{0}\tif {{$MonitorActor{1}_once_flag == 0}} {{\n'
			'{0}\t\tset MonitorActor{1}_once_flag 1\n'
			'{0}\t\tset STKO_plot_00 [open "./{4}.plt" w+]\n'
			'{0}\t\tputs $STKO_plot_00 "{2}\t{3}"\n'
			'{0}\t}} else {{\n'
			'{0}\t\tset STKO_plot_00 [open "./{4}.plt" a+]\n'
			'{0}\t}}\n'
		).format(indent, id_monitor, xLabel + ' ' + xLabelAppend.replace("[","\["), yLabel + ' ' + yLabelAppend.replace("[","\["), _get_plot_name(xobj))
	if is_par:
		f.write('\tif {$STKO_VAR_process_id == 0} {\n')
		f.write(plot_begin('\t'))
		f.write('\t}\n')
	else:
		f.write(plot_begin(''))
	if tcl_resX == 'nodeReaction' or tcl_resY == 'nodeReaction':
		f.write('\treactions\n')
	
	# write cmd for creating X Y data in TCL
	# for each component...
	for COMP in ['X', 'Y']:
		itype = type_name[COMP]
		if itype == 'Pseudo Time':
			f.write('\tset monitor_value_{} [getTime "%e"]\n'.format(COMP))
		elif itype == 'Time Step ID':
			# f.write('\tset monitor_value_{0} $step_id\n'.format(COMP,id_monitor))
			# just for plotting we plot in order all steps not returning to 0 at each new stage
			f.write('\tglobal last_step_id_previous_stage_{0}_{1}\n'.format(COMP,id_monitor))
			f.write('\tglobal previous_step_id_{0}_{1}\n'.format(COMP,id_monitor))
			f.write('\tglobal previous_monitor_value_{0}_{1}\n'.format(COMP,id_monitor))
			f.write('\tif {{$step_id < $previous_step_id_{0}_{1}}} {{\n'.format(COMP,id_monitor))
			f.write('\t\t# It means a new stage has started\n')
			f.write('\t\tset last_step_id_previous_stage_{0}_{1} $previous_monitor_value_{0}_{1}\n'.format(COMP,id_monitor))
			f.write('\t}\n')
			f.write('\tset monitor_value_{0} [expr $step_id + $last_step_id_previous_stage_{0}_{1}]\n'.format(COMP,id_monitor))
			f.write('\tset previous_step_id_{0}_{1} $step_id\n'.format(COMP,id_monitor))
			f.write('\tset previous_monitor_value_{0}_{1} $monitor_value_{0}\n'.format(COMP,id_monitor))
		elif itype == 'Results {} Axis Plot'.format(COMP):
			# initialize output variable (only in process 0)
			operation = geta('Operation/{}'.format(COMP)).string
			# Scaling factor 
			scale = geta('ScaleFactor/{}'.format(COMP)).real
			# Add constant factor
			add = geta('Add/{}'.format(COMP)).real
			# Initialize variable
			if is_par:
				f.write('\tif {$STKO_VAR_process_id == 0} {\n')
				f.write('\t\tset monitor_value_{} 0.0\n'.format(COMP))
				if operation == 'Maximum' or operation == 'Minimum':
					f.write('\t\tset monitor_value_{}_set 0\n'.format(COMP))
				f.write('\t}\n')
			else:
				f.write('\tset monitor_value_{} 0.0\n'.format(COMP))
				if operation == 'Maximum' or operation == 'Minimum':
					f.write('\tset monitor_value_{}_set 0\n'.format(COMP))
			# begin node loop...
			f.write('\tglobal nodes_{0}_{1}\n'.format(COMP, id_monitor))
			if is_par:
				f.write('\tglobal nodes_partitions_{0}_{1}\n'.format(COMP, id_monitor))
			f.write('\tforeach node_id $nodes_{}_{} {{\n'.format(COMP, id_monitor))
			# get node value, sequential or parallel on each processor,
			# and in parallel version send them to process 0
			if is_par:
				f.write('\t\t# get node value.\n\t\t# initialize accumulated value on P0\n')
				f.write('\t\tif {$STKO_VAR_process_id == 0} {\n')
				f.write('\t\t\tset node_value 0.0\n')
				f.write('\t\t}\n')
				f.write('\t\tset inode_partitions [dict get $nodes_partitions_{}_{} $node_id]\n'.format(COMP, id_monitor))
				f.write('\t\tforeach node_pid $inode_partitions {\n')
				# partition loop begin
				f.write((
					'\t\t\t# obtain p_process_value\n'
					'\t\t\tif {{$node_pid == $STKO_VAR_process_id}} {{\n'
					'\t\t\t\tset p_node_value [{0} $node_id {1}]\n'
					'\t\t\t}}\n'
					'\t\t\t# accumulate on node_value\n'
					'\t\t\tif {{$node_pid == $STKO_VAR_process_id}} {{\n'
					'\t\t\t\tif {{$STKO_VAR_process_id != 0}} {{\n'
					'\t\t\t\t\tsend -pid 0 $p_node_value\n'
					'\t\t\t\t}} else {{\n'
					'\t\t\t\t\tset node_value [expr $node_value + $p_node_value]\n'
					'\t\t\t\t}}\n'
					'\t\t\t}} else {{\n'
					'\t\t\t\tif {{$STKO_VAR_process_id == 0}} {{\n'
					'\t\t\t\t\trecv -pid $node_pid p_node_value\n'
					'\t\t\t\t\tset node_value [expr $node_value + $p_node_value]\n'
					'\t\t\t\t}}\n'
					'\t\t\t}}\n'
				).format(tcl_res[COMP], tcl_component[COMP]))
				# partition loop end
				f.write('\t\t}\n')
				# based on the result type we may need to do an average from the partition loop
				if tcl_res[COMP] in _monitor_globals.MAP_RES_PARALLEL_AVG:
					f.write((
						'\t\t# average value from partitions ({0})\n'
						'\t\tif {{$STKO_VAR_process_id == 0}} {{\n'
						'\t\t\tset node_value [expr $node_value/[llength $inode_partitions].0]\n'
						'\t\t}}\n'
					).format(tcl_res[COMP]))
			else:
				f.write('\t\t# get node value\n')
				f.write('\t\tset node_value [{} $node_id {}]\n'.format(tcl_res[COMP], tcl_component[COMP]))
			# write by operation type only on process 0
			if is_par:
				f.write('\t\tif {$STKO_VAR_process_id == 0} {\n')
			def _pwrite(what):
				if is_par:
					f.write('\t{}'.format(what))
				else:
					f.write(what)
			if operation == 'Sum':
				_pwrite('\t\tset monitor_value_{0} [expr $monitor_value_{0} + $node_value]\n'.format(COMP))
			elif operation == 'Average':
				_pwrite('\t\tset monitor_value_{0} [expr $monitor_value_{0} + $node_value]\n'.format(COMP))
			elif operation == 'Maximum':
				_pwrite('\t\tif {{$monitor_value_{0}_set == 0}} {{\n'.format(COMP))
				_pwrite('\t\t\tset monitor_value_{0} $node_value\n'.format(COMP))
				_pwrite('\t\t\tset monitor_value_{0}_set 1\n'.format(COMP))
				_pwrite('\t\t} else {\n')
				_pwrite('\t\t\tset monitor_value_{0} [expr max ($monitor_value_{0} , $node_value)]\n'.format(COMP))
				_pwrite('\t\t}\n')
			elif operation == 'Minimum':
				_pwrite('\t\tif {{$monitor_value_{0}_set == 0}} {{\n'.format(COMP))
				_pwrite('\t\t\tset monitor_value_{0} $node_value\n'.format(COMP))
				_pwrite('\t\t\tset monitor_value_{0}_set 1\n'.format(COMP))
				_pwrite('\t\t} else {\n')
				_pwrite('\t\t\tset monitor_value_{0} [expr min ($monitor_value_{0} , $node_value)]\n'.format(COMP))
				_pwrite('\t\t}\n')
			if is_par:
				f.write('\t\t}\n')
			f.write('\t}\n') # end node loop
			# Scale and Add results only on process 0
			if is_par:
				f.write('\tif {$STKO_VAR_process_id == 0} {\n')
			if operation == 'Average':
				_pwrite('\tset monitor_value_{0} [expr $monitor_value_{0}/[llength $nodes_{0}_{1}]]\n'.format(COMP,id_monitor))
			_pwrite('\tset monitor_value_{} [expr {} * $monitor_value_{} + {}]\n'.format(COMP,scale,COMP,add))
			if is_par:
				f.write('\t}\n')
	
	# write values
	if is_par:
		f.write('\tif {$STKO_VAR_process_id == 0} {\n')
		f.write('\t\tputs $STKO_plot_00 "$monitor_value_X\t$monitor_value_Y"\n')
		f.write('\t\tclose $STKO_plot_00\n')
		f.write('\t}\n')
	else:
		f.write('\tputs $STKO_plot_00 "$monitor_value_X\t$monitor_value_Y"\n')
		f.write('\tclose $STKO_plot_00\n')
	
	# open the monitor actor function
	f.write('}\n')
	f.write('lappend STKO_VAR_MonitorFunctions "MonitorActor{}"\n'.format(id_monitor))

def initializeMonitor(pinfo):
	
	# check that all monitors with custom names
	used_names = {}
	doc = App.caeDocument()
	for id, step in doc.analysisSteps.items():
		xobj = step.XObject
		if xobj.name == 'monitor':
			name = _get_plot_name(xobj)
			if name in used_names:
				other = used_names[name]
				raise Exception('Monitor [{}] has a name ("{}") which is already used by Monitor [{}].\nPlease provide unique names'.format(id, name, other))
			else:
				used_names[name] = id
	
	# this block was moved into the main writer
	# remove all stats, plt, pltbg
	#for ext in ['plt', 'pltbg', 'stats']:
	#for f in glob.glob('{}/*.{}'.format(pinfo.out_dir, ext)):
	#print('remove: ', f)
	#os.remove(f)
	
	# copy the STKOMonitor python app from the external_solver directory
	# to the current output directory
	source_dir = Utils.get_external_solvers_dir() + os.sep + "STKOMonitor"
	dest_dir = pinfo.out_dir + os.sep + "STKOMonitor"
	# remove any existent STKOMonitor folder from the out dir
	if os.path.exists(dest_dir):
		shutil.rmtree(dest_dir)
	shutil.copytree(source_dir, dest_dir)
	
	# outout file
	f = pinfo.out_file
	
	# write tcl command to run the monitor
	#f.write('\n# run the monitor\n')
	#f.write('if {$STKO_VAR_process_id == 0} {\n')
	#f.write('\tif {[catch {exec "./STKOMonitor/STKOMonitor.bat" &}]} {puts "Failed running monitor"}\n')
	if sys.platform == 'win32':
		with open('{}/LaunchSTKOMonitor.bat'.format(pinfo.out_dir), 'w+') as fmon:
			fmon.write('.\\STKOMonitor\\STKOMonitor.bat')
	elif sys.platform == 'linux':
		launcher_name = '{}/LaunchSTKOMonitor.sh'.format(pinfo.out_dir)
		with open(launcher_name, 'w+') as fmon:
			fmon.write('./STKOMonitor/STKOMonitor.sh')
		os.chmod(launcher_name, 0o777)
	#f.write('}\n')
	
	# write the stats monitor actor
	f.write('\n# Statistics monitor actor\n')
	f.write('set MonitorActorStatistics_once_flag 0\n')
	f.write('proc MonitorActorStatistics {{{}}} {{\n'.format(_monitor_globals.STR_ARGS))
	f.write('\tglobal MonitorActorStatistics_once_flag\n')
	f.write('\t# Statistics\n')
	f.write('\tif {$STKO_VAR_process_id == 0} {\n')
	f.write('\t\tif {$MonitorActorStatistics_once_flag == 0} {\n')
	f.write('\t\t\tset MonitorActorStatistics_once_flag 1\n')
	f.write('\t\t\tset STKO_monitor_statistics [open "./STKO_monitor_statistics.stats"  w+]\n')
	f.write('\t\t} else {\n')
	f.write('\t\t\tset STKO_monitor_statistics [open "./STKO_monitor_statistics.stats"  a+]\n')
	f.write('\t\t}\n')
	f.write('\t\tputs $STKO_monitor_statistics "$step_id $dt $T $n_iter $norm $perc"\n')
	f.write('\t\tclose $STKO_monitor_statistics\n')
	f.write('\t}\n')
	f.write('}\n')
	f.write('lappend STKO_VAR_MonitorFunctions "MonitorActorStatistics"\n')
	
	# write the timer monitor actor
	f.write('\n# Timing monitor actor\n')
	f.write('set monitor_actor_time_0 [clock seconds]\n')
	f.write('proc MonitorActorTiming {{{}}} {{\n'.format(_monitor_globals.STR_ARGS))
	f.write('\tglobal monitor_actor_time_0\n')
	f.write('\tif {$STKO_VAR_process_id == 0} {\n')
	f.write('\t\tset STKO_time [open "./STKO_time_monitor.tim" w+]\n')
	f.write('\t\tset current_time [clock seconds]\n')
	f.write('\t\tputs $STKO_time $monitor_actor_time_0\n')
	f.write('\t\tputs $STKO_time $current_time\n')
	f.write('\t\tclose $STKO_time\n')
	f.write('\t}\n')
	f.write('}\n')
	f.write('lappend STKO_VAR_MonitorFunctions "MonitorActorTiming"\n')
	f.write('')
