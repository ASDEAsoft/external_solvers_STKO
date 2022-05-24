import importlib
import PyMpc
import PyMpc.App
from opensees.analysis_steps.Misc_commands.monitor import _monitor_globals

def write_analysis_steps(doc, pinfo):
	PyMpc.App.monitor().sendMessage('writing analysis_steps...')
	for item_id, item in doc.analysisSteps.items():
		xobj = item.XObject
		if(xobj is None):
			raise Exception('null XObject in analysis_steps object')
		module_name = 'opensees.analysis_steps.{}.{}'.format(xobj.Xnamespace, xobj.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl'):
			pinfo.analysis_step = item
			module.writeTcl(pinfo)
		PyMpc.App.monitor().sendAutoIncrement()
	pinfo.out_file.write('\n# Done!\n')
	pinfo.out_file.write('puts "ANALYSIS SUCCESSFULLY FINISHED"\n')

def initialize_custom_functions(doc, pinfo):
	
	# outout file
	f = pinfo.out_file
	
	# write the CustomFunctionCaller
	f.write('\n# the main custom function caller that will call all actors in $all_monitor_actors and in $all_custom_functions list\n')
	f.write('proc CustomFunctionCaller {{{}}} {{\n'.format(_monitor_globals.STR_ARGS))
	f.write('\tglobal all_monitor_actors\n')
	f.write('\tglobal all_custom_functions\n')
	f.write('\t# Call monitors: we pass the parameters needed\n')
	f.write('\tforeach p $all_monitor_actors {\n')
	f.write('\t\t$p {}\n'.format(_monitor_globals.STR_ARGS_REF))
	f.write('\t}\n')
	f.write('\t# Call all other custom functions\n')
	f.write('\tforeach p $all_custom_functions {\n')
	f.write('\t\t$p\n')
	f.write('\t}\n')
	f.write('}\n')

def initialize_first_monitor(doc, monitor_step, pinfo):
	xobj = monitor_step.XObject
	if(xobj is None):
		raise Exception('null XObject in analysis_steps object')
	module_name = 'opensees.analysis_steps.{}.{}'.format(xobj.Xnamespace, xobj.name)
	module = importlib.import_module(module_name)
	if xobj.name == 'monitor':
		if hasattr(module, 'initializeMonitor'):
			pinfo.analysis_step = monitor_step
			module.initializeMonitor(pinfo)
			pinfo.analysis_step = None
