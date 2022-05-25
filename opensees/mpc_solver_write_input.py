import os
import glob
import shutil
import importlib
import sys
import subprocess
import pkgutil
import PyMpc
import PyMpc.App
import opensees
import opensees.utils.tcl_input as tclin
import opensees.utils.write_physical_properties as write_physical_properties
import opensees.utils.write_analysis_steps as write_analysis_steps
import opensees.utils.write_definitions as write_definitions
import opensees.utils.write_element as write_element
import opensees.utils.write_node as write_node
from io import StringIO

def write_tcl_int(out_dir):
	
	# define block durations
	duration_mapping = 0.3
	duration_definitions = 0.005
	duration_materials = 0.005
	duration_sections = 0.015
	duration_mass = 0.025
	duration_nodes = 0.2
	duration_elements = 0.3
	duration_steps = 0.15
	current_percentage = 0.0

	print('writing tcl input files in "{}"'.format(out_dir))
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	# document
	doc = PyMpc.App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	# check mesh
	if doc.mesh is None:
		raise Exception('The model has not been meshed. Please run the "Build mesh" command before running the analyses')
	for item_id, item in doc.geometries.items():
		item_mesh = doc.mesh.getMeshedGeometry(item_id)
		if item_mesh is None:
			raise Exception('The geometry [{}]"{}" has not been meshed.  Please run the "Build mesh" command before running the analyses'.format(item_id, item.name))
	for item_id, item in doc.interactions.items():
		item_mesh = doc.mesh.getMeshedInteraction(item_id)
		if item_mesh is None:
			raise Exception('The interaction [{}]"{}" has not been meshed.  Please run the "Build mesh" command before running the analyses'.format(item_id, item.name))
	
	# create process info
	pinfo = tclin.process_info()
	pinfo.out_dir = out_dir
	
	# remove all residual data from a Monitor
	# remove all stats, plt, pltbg
	for ext in ['plt', 'pltbg', 'stats']:
		for f in glob.glob('{}/*.{}'.format(pinfo.out_dir, ext)):
			os.remove(f)
	monitor_dir = '{}/STKOMonitor'.format(pinfo.out_dir)
	if os.path.exists(monitor_dir) and os.path.isdir(monitor_dir):
		shutil.rmtree(monitor_dir)
	monitor_runner = '{}/LaunchSTKOMonitor'.format(pinfo.out_dir)
	if sys.platform == 'win32':
		monitor_runner += '.bat'
	elif sys.platform == 'linux':
		monitor_runner += '.sh'
	if os.path.exists(monitor_runner) and os.path.isfile(monitor_runner):
		os.remove(monitor_runner)
	
	# let's see if we have a partitioned model
	is_partitioned = False
	process_count = len(doc.mesh.partitionData.partitions)
	if process_count > 1:
		is_partitioned = True
		pinfo.setProcessCount(process_count)
	
	# create the main script
	main_file_name = '{}{}main.tcl'.format(out_dir, os.sep)
	PyMpc.App.monitor().sendMessage('creating main script: "{}" ...'.format(main_file_name))
	PyMpc.App.monitor().sendPercentage(current_percentage)
	main_file = open(main_file_name, 'w+')
	# the initial wipe
	main_file.write('wipe\n\n')
	# write STKO_VAR_*** stuff
	main_file.write('{}# =================================================================================\n'.format(pinfo.indent))
	main_file.write('{}# STKO COMMON VARIABLES (STKO_VAR_***)\n'.format(pinfo.indent))
	main_file.write('{}# =================================================================================\n\n'.format(pinfo.indent))
	main_file.write('{}# The current process id (from 0 to NP-1)\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_process_id [getPID]\n'.format(pinfo.indent))
	main_file.write('{}# A boolean flag for parallel processing (True if NP > 1)\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_is_parallel {}\n'.format(pinfo.indent, int(is_partitioned)))
	main_file.write('{}# The result from analyze command  (0 if succesfull)\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_analyze_done 0\n'.format(pinfo.indent, int(is_partitioned)))
	main_file.write('{}# The increment counter in the current stage\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_increment 0\n'.format(pinfo.indent))
	main_file.write('{}# The current time\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_time 0.0\n'.format(pinfo.indent))
	main_file.write('{}# The current time increment\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_time_increment 0.0\n'.format(pinfo.indent))
	main_file.write('{}# The current stage percentage\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_percentage 0.0\n'.format(pinfo.indent))
	main_file.write('{}# The last number of iterations\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_num_iter 0\n'.format(pinfo.indent))
	main_file.write('{}# The last error norm\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_error_norm 0.0\n'.format(pinfo.indent))
	main_file.write('{}# A list of custom functions called before solving the current time step\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_OnBeforeAnalyze_CustomFunctions {{}}\n'.format(pinfo.indent))
	main_file.write('{}# A list of custom functions called after solving the current time step\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_OnAfterAnalyze_CustomFunctions {{}}\n'.format(pinfo.indent))
	main_file.write('{}# A list of monitor functions\n'.format(pinfo.indent))
	main_file.write('{}set STKO_VAR_MonitorFunctions {{}}\n'.format(pinfo.indent))
	main_file.write('{}# for backward compatibility (STKO version < 3.1.0).\n'.format(pinfo.indent))
	main_file.write('{}# It is now deprecated and will be removed in future versions.\n'.format(pinfo.indent))
	main_file.write('{}set all_custom_functions {{}}\n'.format(pinfo.indent))
	
	main_file.write('{}# Call functions before the analyze command.\n'.format(pinfo.indent))
	main_file.write('{}proc STKO_CALL_OnBeforeAnalyze {{}} {{\n'.format(pinfo.indent))
	main_file.write('{}\tglobal STKO_VAR_OnBeforeAnalyze_CustomFunctions\n'.format(pinfo.indent))
	main_file.write('{}\tforeach item $STKO_VAR_OnBeforeAnalyze_CustomFunctions {{\n'.format(pinfo.indent))
	main_file.write('{}\t\t$item\n'.format(pinfo.indent))
	main_file.write('{}\t}}\n'.format(pinfo.indent))
	main_file.write('{}}}\n'.format(pinfo.indent))
	
	main_file.write('{}# Call functions after the analyze command.\n'.format(pinfo.indent))
	main_file.write('{}proc STKO_CALL_OnAfterAnalyze {{}} {{\n'.format(pinfo.indent))
	main_file.write('{}\tglobal STKO_VAR_analyze_done\n'.format(pinfo.indent))
	main_file.write('{}\tglobal STKO_VAR_OnAfterAnalyze_CustomFunctions\n'.format(pinfo.indent))
	main_file.write('{}\tglobal all_custom_functions\n'.format(pinfo.indent))
	main_file.write('{}\tglobal STKO_VAR_MonitorFunctions\n'.format(pinfo.indent))
	main_file.write('{}\tforeach item $STKO_VAR_OnAfterAnalyze_CustomFunctions {{\n'.format(pinfo.indent))
	main_file.write('{}\t\t$item\n'.format(pinfo.indent))
	main_file.write('{}\t}}\n'.format(pinfo.indent))
	main_file.write('{}\tif {{$STKO_VAR_analyze_done == 0}} {{\n'.format(pinfo.indent))
	main_file.write('{}\t\tforeach item $all_custom_functions {{\n'.format(pinfo.indent))
	main_file.write('{}\t\t\t$item\n'.format(pinfo.indent))
	main_file.write('{}\t\t}}\n'.format(pinfo.indent))
	main_file.write('{}\t\tforeach item $STKO_VAR_MonitorFunctions {{\n'.format(pinfo.indent))
	main_file.write('{}\t\t\t$item\n'.format(pinfo.indent))
	main_file.write('{}\t\t}}\n'.format(pinfo.indent))
	main_file.write('{}\t}}\n'.format(pinfo.indent))
	main_file.write('{}}}\n'.format(pinfo.indent))
	
	main_file.write('\n{}# =================================================================================\n'.format(pinfo.indent))
	main_file.write('{}# SOURCING\n'.format(pinfo.indent))
	main_file.write('{}# =================================================================================\n\n'.format(pinfo.indent))
	
	# set the main file as the current output file
	pinfo.out_file = main_file
	
	# evaluate, for each node, the NDM/NDF pair
	# using the elements connected to that node.
	pinfo.inv_map = {}
	PyMpc.App.monitor().sendMessage('creating NDM/NDF pairs for each node...')
	PyMpc.App.monitor().setRange(current_percentage, current_percentage + duration_mapping)
	write_node.node_map_ndm_ndf(doc, pinfo)
	write_node.lagrangian_node(doc, pinfo)
	write_node.short_map(doc, pinfo)
	if pinfo.inv_map:
		# write the first model builder
		(ndm, ndf) = next(iter(pinfo.inv_map))
		pinfo.updateModelBuilder(ndm, ndf)
	else:
		# in this case we have only nodes without assignments
		# let's use a default 3D 3DOFS
		pinfo.updateModelBuilder(3,3)
	current_percentage += duration_mapping
	PyMpc.App.monitor().setRange(0.0, 1.0)
	PyMpc.App.monitor().sendPercentage(current_percentage)

	# initialize the next ids for nodes, elements and physical properties.
	# they will used by some elements that will need to generate extra elements/nodes/materials...
	pinfo.next_node_id = doc.mesh.nodes.getlastkey(0)+1
	pinfo.next_elem_id = doc.mesh.elements.getlastkey(0)+1
	pinfo.next_physicalProperties_id = doc.physicalProperties.getlastkey(0)+1
	pinfo.next_definitions_id = doc.definitions.getlastkey(0)+1
	pinfo.next_conditions_id = doc.conditions.getlastkey(0)+1
	pinfo.next_analysis_step_id = doc.analysisSteps.getlastkey(0)+1

	# definitions.
	# create a single file named definitions.tcl.
	# write all definitions there, and then source it in the main script
	definitions_file_name = 'definitions.tcl'
	PyMpc.App.monitor().sendMessage('writing definitions...')
	definitions_file = open('{}{}{}'.format(out_dir, os.sep, definitions_file_name), 'w+')
	pinfo.out_file = definitions_file
	write_definitions.write_definitions(doc.definitions, pinfo)
	definitions_file.close()
	current_percentage += duration_definitions
	PyMpc.App.monitor().sendPercentage(current_percentage)
	
	# materials.
	# create a single file named materials.tcl.
	# write all physical properties of type (uniaxial/nD) there, and then source it in the main script
	physical_properties_name = 'materials.tcl'
	PyMpc.App.monitor().sendMessage('writing materials...')
	physical_properties_file = open('{}{}{}'.format(out_dir, os.sep, physical_properties_name), 'w+')
	pinfo.out_file = physical_properties_file
	write_physical_properties.write_physical_properties(doc.physicalProperties, pinfo, 'materials')
	physical_properties_file.close()
	current_percentage += duration_materials
	PyMpc.App.monitor().sendPercentage(current_percentage)
	
	# sections.
	# create a single file named sections.tcl.
	# write all physical properties of type (section) there, and then source it in the main script
	sections_file_name = 'sections.tcl'
	PyMpc.App.monitor().sendMessage('writing sections...')
	sections_file = open('{}{}{}'.format(out_dir, os.sep, sections_file_name), 'w+')
	pinfo.out_file = sections_file
	write_physical_properties.write_physical_properties(doc.physicalProperties, pinfo, 'sections')
	sections_file.close()
	current_percentage += duration_sections
	PyMpc.App.monitor().sendPercentage(current_percentage)
	
	# read mass data to create mass_to_node_map.
	write_node.fill_node_mass_map(doc, pinfo)
	current_percentage += duration_mass
	PyMpc.App.monitor().sendPercentage(current_percentage)

	# check whether the user used some modelSubset command,
	# otherwise write directly the entire model here
	has_model_subsets = False
	for astep_id, astep in doc.analysisSteps.items():
		xobj = astep.XObject
		if (xobj is not None) and (xobj.name == 'modelSubset'):
			has_model_subsets = True
			break
	if has_model_subsets:
		print('Found at least 1 user defined model subset.')
	else:
		print('No model subset found. The entire model will be written at the beginning.')
	
	# nodes.
	# create a single file named nodes.tcl.
	# write all nodes there, and then source it in the main script
	# note that if we have hanging nodes they will be written at the end of the
	# nodes.tcl file.
	node_file_name = 'nodes.tcl'
	PyMpc.App.monitor().sendMessage('writing nodes...')
	node_file = open('{}{}{}'.format(out_dir, os.sep, node_file_name), 'w+')
	pinfo.out_file = node_file
	PyMpc.App.monitor().setRange(current_percentage, current_percentage + duration_nodes)
	if not has_model_subsets:
		num_items = len(doc.mesh.nodes)
		increment = duration_nodes / max(num_items, 1)
		PyMpc.App.monitor().setAutoIncrement(increment)
		if num_items > 20:
			PyMpc.App.monitor().setDisplayIncrement(duration_nodes/20)
		else:
			PyMpc.App.monitor().setDisplayIncrement(0.0)
		if is_partitioned:
			write_node.write_node_partition (doc, pinfo, node_file)
			write_node.write_node_not_assigned_partition (doc, pinfo, node_file)
		else:
			write_node.write_node (doc, pinfo, node_file)
			write_node.write_node_not_assigned (doc, pinfo, node_file)
	current_percentage += duration_nodes
	PyMpc.App.monitor().setDisplayIncrement(0.0)
	PyMpc.App.monitor().setRange(0.0, 1.0)
	PyMpc.App.monitor().sendPercentage(current_percentage)
	node_file.close()
	
	# begin pre process elements ========================================================
	# we need to pre-process elements here, after materials,sections and nodes
	# but before actual elements.
	# however we need to source it later on. so instead of setting the pinfo.out_file to
	# the main file, we set it to a temporary StringIO buffer
	pre_proc_ele_buffer = StringIO()
	pinfo.out_file = pre_proc_ele_buffer
	PyMpc.App.monitor().sendMessage('pre-processing elements...')
	dir_external_solvers = PyMpc.Utils.get_external_solvers_dir()
	elem_modules_path = '{0}{1}opensees{1}element_properties'.format(dir_external_solvers, os.sep)
	for path, subdirs, files in os.walk(elem_modules_path):
		for _, imodule_name, _ in pkgutil.iter_modules([ path ]):
			rpath = os.path.relpath(path, dir_external_solvers)
			rpath = rpath.replace('/', '.')
			rpath = rpath.replace('\\', '.')
			imodule = importlib.import_module('{}.{}'.format(rpath, imodule_name))
			if hasattr(imodule, 'preProcessElements'):
				print('pre-processing module: {}'.format(imodule_name))
				imodule.preProcessElements(pinfo)
	# end  pre process elements =========================================================
	
	# elements.
	# create a single file named elements.tcl.
	# write all elements there, and then source it in the main script
	element_file_name = 'elements.tcl'
	PyMpc.App.monitor().sendMessage('writing elements...')
	element_file = open('{}{}{}'.format(out_dir, os.sep, element_file_name), 'w+')
	pinfo.out_file = element_file
	PyMpc.App.monitor().setRange(current_percentage, current_percentage + duration_elements)
	if not has_model_subsets:
		num_items = len(doc.mesh.elements)
		increment = duration_elements / max(num_items, 1)
		PyMpc.App.monitor().setAutoIncrement(increment)
		if num_items > 20:
			PyMpc.App.monitor().setDisplayIncrement(duration_elements/20)
		else:
			PyMpc.App.monitor().setDisplayIncrement(0.0)
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
	current_percentage += duration_elements
	PyMpc.App.monitor().setDisplayIncrement(0.0)
	PyMpc.App.monitor().setRange(0.0, 1.0)
	PyMpc.App.monitor().sendPercentage(current_percentage)
	
	# analysis_steps.
	# create a single file named analysis_steps.tcl.
	# write all analysis_steps there, and then source it in the main script
	analysis_steps_file_name = 'analysis_steps.tcl'
	PyMpc.App.monitor().sendMessage('writing analysis steps...')
	analysis_steps_file = open('{}{}{}'.format(out_dir, os.sep, analysis_steps_file_name), 'w+')
	pinfo.out_file = analysis_steps_file
	
	# search for all monitors (if any) and do the first monitor initialization.
	# if at least a monitor is defined, all analyses will have a monitor.
	# for analyses without their own monitor, the application initializes the first monitor in the following function
	for _, step in doc.analysisSteps.items() :
		if step.XObject.name == 'monitor':
			# pinfo.monitor = True # It is not needed because now I always call customFunction
			write_analysis_steps.initialize_first_monitor(doc, step, pinfo)
			break
			
	PyMpc.App.monitor().setRange(current_percentage, current_percentage + duration_steps)
	num_items = len(doc.analysisSteps)
	increment = duration_steps / max(num_items, 1)
	PyMpc.App.monitor().setAutoIncrement(increment)
	if num_items > 20:
		PyMpc.App.monitor().setDisplayIncrement(duration_steps/20)
	else:
		PyMpc.App.monitor().setDisplayIncrement(0.0)
	write_analysis_steps.write_analysis_steps(doc, pinfo)
	analysis_steps_file.close()
	current_percentage += duration_steps
	PyMpc.App.monitor().setDisplayIncrement(0.0)
	PyMpc.App.monitor().setRange(0.0, 1.0)
	PyMpc.App.monitor().sendPercentage(current_percentage)

	# we do not write it here because the first call to pinfo.updateModelBuilder writes it anyway
	# source definitions
	# main_file.write('# source definitions\n')
	# main_file.write('source {}\n'.format(definitions_file_name)) 

	# source materials
	main_file.write('# source materials\n')
	main_file.write('source {}\n'.format(physical_properties_name))

	# source sections
	main_file.write('# source sections\n')
	main_file.write('source {}\n'.format(sections_file_name))

	# source node
	main_file.write('# source node\n')
	main_file.write('source {}\n'.format(node_file_name))
	
	# pre-processes elements
	ppebuff = pre_proc_ele_buffer.getvalue()
	if ppebuff:
		main_file.write('# begin sourcing files for pre-processing of automatic element assemblies...\n')
		main_file.write(ppebuff)
	
	# source element
	main_file.write('# source element\n')
	main_file.write('source {}\n'.format(element_file_name))

	# source analysis_steps
	main_file.write('# source analysis_steps\n')
	main_file.write('source {}\n'.format(analysis_steps_file_name))
	
	# clear all
	main_file.write('\nwipe\n')
	
	# close the main script
	main_file.close()
	
	# update mpco cdata
	pinfo.updateMpcoCdataFiles()
	
	# done
	PyMpc.App.monitor().sendMessage('Done.Input file correctly written!')

def write_tcl(out_dir):
	'''
	Use this code block to just run the process of writing input files
	without profiling
	'''
	write_tcl_int(out_dir)
	'''
	Use this code block to profile the process of writing input files
	to look for possible bottlenecks.
	'''
	#import cProfile
	#import pstats
	#stats_file = out_dir + os.sep + 'stats.dat'
	#cProfile.runctx('write_tcl_int(out_dir)', globals(), {'out_dir':out_dir}, stats_file)
	#p = pstats.Stats(stats_file)
	#p.sort_stats('cumulative').print_stats()
