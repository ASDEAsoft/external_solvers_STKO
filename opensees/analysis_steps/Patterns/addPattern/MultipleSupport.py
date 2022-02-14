import PyMpc.Units as u
from PyMpc import *
import PyMpc.App
import importlib
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# groundMotion
	at_groundMotion = MpcAttributeMetaData()
	at_groundMotion.type = MpcAttributeType.IndexVector
	at_groundMotion.name = 'groundMotion'
	at_groundMotion.group = 'Group'
	at_groundMotion.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('groundMotion')+'<br/>') + 
		html_par('ground motion') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Multi-Support_Excitation_Pattern','Multi-Support Excitation Pattern')+'<br/>') +
		html_end()
		)
	at_groundMotion.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_groundMotion.indexSource.addAllowedNamespace("Ground_Motion")
	
	xom = MpcXObjectMetaData()
	xom.name = 'MultipleSupport'
	xom.addAttribute(at_groundMotion)
	
	
	return xom

def writeTcl(pinfo):
	
	xobj = pinfo.analysis_step.XObject
	tag = xobj.parent.componentId
	
	# now write the string into the file
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	pinfo.out_file.write('{}pattern MultipleSupport {} {}\n'.format(pinfo.indent, tag, '{'))
	
	'''
	groundMotion
	'''
	groundMotion_at = xobj.getAttribute('groundMotion')
	if(groundMotion_at is None):
		raise Exception('Error: cannot find "groundMotion" attribute')
	groundMotion_index = groundMotion_at.indexVector
	
	doc = PyMpc.App.caeDocument()
	
	for i in groundMotion_index:
		if i == 0: continue
		gmTag = i
		item = doc.conditions[i]
		xobj_gm = item.XObject		# xobj groundMotion
		if(xobj_gm is None):
			raise Exception('null XObject in Patterns object')
		module_name = 'opensees.conditions.{}.{}'.format(xobj_gm.Xnamespace, xobj_gm.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl_groundMotion'):
			pinfo.condition = item
			module.writeTcl_groundMotion(pinfo, xobj_gm, gmTag)
	
	
	pinfo.out_file.write('{}{}\n'.format(pinfo.indent, '}'))