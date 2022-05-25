import importlib
import PyMpc
import PyMpc.App

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
