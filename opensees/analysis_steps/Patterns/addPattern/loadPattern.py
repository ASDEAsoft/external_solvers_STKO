import PyMpc.Units as u
import PyMpc.App
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import importlib

def makeXObjectMetaData():
	
	# tsTagAccel
	at_tsTag = MpcAttributeMetaData()
	at_tsTag.type = MpcAttributeType.Index
	at_tsTag.name = 'tsTag'
	at_tsTag.group = 'Load pattern'
	at_tsTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tsTag')+'<br/>') + 
		html_par('the tag of the time series to be used in the load pattern '+
		html_href('http://opensees.berkeley.edu/wiki/index.php/Time_Series_Command','timeSeries')+' command') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_Pattern','Plain Pattern')+'<br/>') +
		html_end()
		)
	at_tsTag.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_tsTag.indexSource.addAllowedNamespace("timeSeries")
	
	# -fact
	at_fact = MpcAttributeMetaData()
	at_fact.type = MpcAttributeType.Boolean
	at_fact.name = '-fact'
	at_fact.group = 'Load pattern'
	at_fact.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fact')+'<br/>') +
		html_par('constant factor (optional, default=1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_Pattern','Plain Pattern')+'<br/>') +
		html_end()
		)
	
	# alphaS/lagrangeMultipliers
	at_cFactor = MpcAttributeMetaData()
	at_cFactor.type = MpcAttributeType.Real
	at_cFactor.name = 'cFactor'
	at_cFactor.group = 'Load pattern'
	at_cFactor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cFactor')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_Pattern','Plain Pattern')+'<br/>') +
		html_end()
		)
	at_cFactor.setDefault(1.0)
	
	# load
	at_load = MpcAttributeMetaData()
	at_load.type = MpcAttributeType.IndexVector
	at_load.name = 'load'
	at_load.group = 'Load pattern'
	at_load.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('load')+'<br/>') + 
		html_par('command to load')+
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_Pattern','Plain Pattern')+'<br/>') +
		html_end()
		)
	at_load.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_load.indexSource.addAllowedNamespace("Loads.Force")
	
	# eleLoad
	at_eleLoad = MpcAttributeMetaData()
	at_eleLoad.type = MpcAttributeType.IndexVector
	at_eleLoad.name = 'eleLoad'
	at_eleLoad.group = 'Load pattern'
	at_eleLoad.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eleLoad')+'<br/>') + 
		html_par('command to generate elemental load')+
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_Pattern','Plain Pattern')+'<br/>') +
		html_end()
		)
	at_eleLoad.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_eleLoad.indexSource.addAllowedNamespace("Loads.eleLoad")
	
	# sp
	at_sp = MpcAttributeMetaData()
	at_sp.type = MpcAttributeType.IndexVector
	at_sp.name = 'sp'
	at_sp.group = 'Load pattern'
	at_sp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sp')+'<br/>') + 
		html_par('command to generate single-point constraint')+
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_Pattern','Plain Pattern')+'<br/>') +
		html_end()
		)
	at_sp.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_sp.indexSource.addAllowedNamespace("Loads.sp")
	
	# genericLoad
	at_genericLoad = MpcAttributeMetaData()
	at_genericLoad.type = MpcAttributeType.IndexVector
	at_genericLoad.name = 'genericLoad'
	at_genericLoad.group = 'Load pattern'
	at_genericLoad.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('genericLoad')+'<br/>') + 
		html_par('command to generate generic load (.e.g surface load)')+
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plain_Pattern','Plain Pattern')+'<br/>') +
		html_end()
		)
	at_genericLoad.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_genericLoad.indexSource.addAllowedNamespace("Loads.Generic")
	xom = MpcXObjectMetaData()
	xom.name = 'loadPattern'
	xom.addAttribute(at_tsTag)
	
	xom.addAttribute(at_load)
	xom.addAttribute(at_eleLoad)
	xom.addAttribute(at_sp)
	xom.addAttribute(at_genericLoad)
	
	xom.addAttribute(at_fact)
	xom.addAttribute(at_cFactor)
	
	# VisibilityDependency
	xom.setVisibilityDependency(at_fact, at_cFactor)
	
	return xom

def writeTcl(pinfo):
	
	xobj = pinfo.analysis_step.XObject
	
	'''
	pattern Plain $patternTag $tsTag <-fact $cFactor> {
	load ...
	eleLoad ...
	sp ...
	...
	}
	'''
	doc = PyMpc.App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	sopt = ''
	tsTag_at = xobj.getAttribute('tsTag')
	if(tsTag_at is None):
		raise Exception('Error: cannot find "tsTag" attribute')
	tsTag = tsTag_at.index
	
	at_fact = xobj.getAttribute('-fact')
	if(at_fact is None):
		raise Exception('Error: cannot find "fact" attribute')
	fact = at_fact.boolean
	if fact:
		at_cFactor = xobj.getAttribute('cFactor')
		if(at_cFactor is None):
			raise Exception('Error: cannot find "cFactor" attribute')
		cFactor = at_cFactor.real
		
		sopt += ' -fact {}'.format(cFactor)
	
	str_tcl = '{}pattern Plain {} {}{} {}\n'.format(pinfo.indent, tag, tsTag, sopt, '{')
	pinfo.out_file.write(str_tcl)
	
	'''
	load
	'''
	load_at = xobj.getAttribute('load')
	if(load_at is None):
		raise Exception('Error: cannot find "load" attribute')
	load = load_at.indexVector
	
	for i in load:
		if i == 0: continue
		item = doc.conditions[i]
		xobj_load = item.XObject
		if(xobj_load is None):
			raise Exception('null XObject in Patterns object')
		module_name = 'opensees.conditions.{}.{}'.format(xobj_load.Xnamespace, xobj_load.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl_Force'):
			pinfo.condition = item
			module.writeTcl_Force(pinfo, xobj_load)
	
	'''
	eleLoad
	'''
	eleLoad_at = xobj.getAttribute('eleLoad')
	if(eleLoad_at is None):
		raise Exception('Error: cannot find "eleLoad" attribute')
	eleLoad = eleLoad_at.indexVector
	
	for i in eleLoad:
		if i == 0: continue
		item = doc.conditions[i]
		xobj_eleLoad = item.XObject
		if(xobj_eleLoad is None):
			raise Exception('null XObject in Patterns object')
		module_name = 'opensees.conditions.{}.{}'.format(xobj_eleLoad.Xnamespace, xobj_eleLoad.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl_eleLoad'):
			pinfo.condition = item
			module.writeTcl_eleLoad(pinfo, xobj_eleLoad)
	
	'''
	sp
	'''
	sp_at = xobj.getAttribute('sp')
	if(sp_at is None):
		raise Exception('Error: cannot find "sp" attribute')
	sp = sp_at.indexVector
	
	for i in sp:
		if i == 0: continue
		item = doc.conditions[i]
		xobj_sp = item.XObject
		if(xobj_sp is None):
			raise Exception('null XObject in Patterns object')
		module_name = 'opensees.conditions.{}.{}'.format(xobj_sp.Xnamespace, xobj_sp.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl_sp'):
			pinfo.condition = item
			module.writeTcl_sp(pinfo, xobj_sp)
			
	'''
	genericLoad
	'''
	genericLoad_at = xobj.getAttribute('genericLoad')
	if(genericLoad_at is None):
		raise Exception('Error: cannot find "genericLoad" attribute')
	genericLoad = genericLoad_at.indexVector
	
	for i in genericLoad:
		if i == 0: continue
		item = doc.conditions[i]
		xobj_genericLoad = item.XObject
		if(xobj_genericLoad is None):
			raise Exception('null XObject in Patterns object')
		module_name = 'opensees.conditions.{}.{}'.format(xobj_genericLoad.Xnamespace, xobj_genericLoad.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl_Load'):
			pinfo.condition = item
			module.writeTcl_Load(pinfo, xobj_genericLoad)
	
	str_tcl = '{}{}\n'.format(pinfo.indent, '}')
	pinfo.out_file.write(str_tcl)
