import PyMpc.Units as u
import PyMpc.App
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# remove loadPattern
	at_removeLoadPattern = MpcAttributeMetaData()
	at_removeLoadPattern.type = MpcAttributeType.IndexVector
	at_removeLoadPattern.name = 'remove loadPattern'
	at_removeLoadPattern.group = 'Group'
	at_removeLoadPattern.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('load')+'<br/>') + 
		html_par('command to remove loadPattern')+
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Remove_Command','Remove Command')+'<br/>') +
		html_end()
		)
	at_removeLoadPattern.indexSource.type = MpcAttributeIndexSourceType.AnalysisStep
	at_removeLoadPattern.indexSource.addAllowedNamespace("Patterns.addPattern")
	at_removeLoadPattern.indexSource.addAllowedClassList(["MultipleSupport", "patternPlain", "UniformExcitation", "loadPattern"])
	
	# use_setTime
	at_use_setTime = MpcAttributeMetaData()
	at_use_setTime.type = MpcAttributeType.Boolean
	at_use_setTime.name = 'use_setTime'
	at_use_setTime.group = 'Group'
	at_use_setTime.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_setTime')+'<br/>') +
		html_par('Time domain to be set') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SetTime_Command','setTime')+'<br/>') +
		html_end()
		)
	
	# setTime
	at_setTime = MpcAttributeMetaData()
	at_setTime.type = MpcAttributeType.Real
	at_setTime.name = 'setTime'
	at_setTime.group = 'setTime'
	at_setTime.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('setTime')+'<br/>') +
		html_par('Time domain to be set') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SetTime_Command','setTime')+'<br/>') +
		html_end()
		)
	at_setTime.setDefault(0.0)
	
	# wipeAnalysis
	at_wipeAnalysis = MpcAttributeMetaData()
	at_wipeAnalysis.type = MpcAttributeType.Boolean
	at_wipeAnalysis.name = 'wipeAnalysis'
	at_wipeAnalysis.group = 'Group'
	at_wipeAnalysis.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('wipeAnalysis')+'<br/>') +
		html_par('Time domain to be set') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/WipeAnalysis_Command','wipeAnalysis')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'removeLoadPattern'
	xom.addAttribute(at_removeLoadPattern)
	xom.addAttribute(at_use_setTime)
	xom.addAttribute(at_setTime)
	xom.addAttribute(at_wipeAnalysis)
	
	xom.setVisibilityDependency(at_use_setTime, at_setTime)
	
	
	return xom

def writeTcl(pinfo):
	
	# remove loadPattern $patternTag
	xobj = pinfo.analysis_step.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	removeLoadPattern_at = xobj.getAttribute('remove loadPattern')
	if(removeLoadPattern_at is None):
		raise Exception('Error: cannot find "remove loadPattern" attribute')
	removeLoadPattern = removeLoadPattern_at.indexVector
	
	wipeAnalysis_at = xobj.getAttribute('wipeAnalysis')
	if(wipeAnalysis_at is None):
		raise Exception('Error: cannot find "wipeAnalysis" attribute')
	if wipeAnalysis_at.boolean:
		pinfo.out_file.write('\nwipeAnalysis')
	
	use_setTime_at = xobj.getAttribute('use_setTime')
	if(use_setTime_at is None):
		raise Exception('Error: cannot find "use_setTime" attribute')
	if use_setTime_at.boolean:
		setTime_at = xobj.getAttribute('setTime')
		if(setTime_at is None):
			raise Exception('Error: cannot find "setTime" attribute')
		pinfo.out_file.write('\nsetTime {}'.format(setTime_at.real))
	
	for i in removeLoadPattern:
		pinfo.out_file.write('\nremove loadPattern {}\n'.format(i))