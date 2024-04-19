import PyMpc.Units as u
import PyMpc.App
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import importlib

def makeXObjectMetaData():
	
	conditions = MpcAttributeMetaData()
	conditions.type = MpcAttributeType.IndexVector
	conditions.name = 'Moving loads'
	conditions.group = 'Default'
	conditions.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Moving loads')+'<br/>') +
		html_par('A list of previously defined MovingLoad conditions') +
		html_end()
		)
	conditions.indexSource.type = MpcAttributeIndexSourceType.Condition
	conditions.indexSource.addAllowedNamespace('Loads.Moving')
	
	xom = MpcXObjectMetaData()
	xom.name = 'MovingLoad'
	xom.addAttribute(conditions)
	
	return xom

def writeTcl(pinfo):
	
	# the current xobject
	doc = App.caeDocument()
	xobj = pinfo.analysis_step.XObject
	
	# all conditions
	conditions = []
	try:
		for id in xobj.getAttribute('Moving loads').indexVector:
			c = doc.getCondition(id)
			if c and c.XObject:
				conditions.append(c)
	except:
		pass
	if len(conditions) == 0:
		return None
	
	# write a begin-description
	pinfo.out_file.write('\n{}# BEGIN {} {} [{}]\n'.format(
		pinfo.indent, xobj.Xnamespace, xobj.name, pinfo.analysis_step.id))
	
	# write a constant time series for all moving loads in this pattern
	ts_tag = pinfo.next_definitions_id
	pinfo.next_definitions_id += 1
	pinfo.out_file.write('\n{}# A Constant timeSeries for the moving loads\n'.format(pinfo.indent))
	var_pat_ts = 'STKO_MLP_{}_ts'.format(pinfo.analysis_step.id)
	pinfo.out_file.write('{}set {} {}\n'.format(pinfo.indent, var_pat_ts, ts_tag))
	pinfo.out_file.write('{}timeSeries Constant ${}\n'.format(pinfo.indent, var_pat_ts))
	
	# process all conditions
	for c in conditions:
		module_name = 'opensees.conditions.{}.{}'.format(c.XObject.Xnamespace, c.XObject.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl_MovingLoad'):
			module.writeTcl_MovingLoad(pinfo, c, var_pat_ts)
	
	# write a end-description
	pinfo.out_file.write('\n{}# END {} {} [{}]\n'.format(
		pinfo.indent, xobj.Xnamespace, xobj.name, pinfo.analysis_step.id))