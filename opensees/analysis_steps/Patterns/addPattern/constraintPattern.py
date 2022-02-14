import PyMpc.Units as u
import PyMpc.App
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import importlib

def makeXObjectMetaData():
	
	# sp
	at_sp = MpcAttributeMetaData()
	at_sp.type = MpcAttributeType.IndexVector
	at_sp.name = 'sp'
	at_sp.group = 'Constraint pattern'
	at_sp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sp')+'<br/>') + 
		html_par('command to generate sp constraint')+
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_sp.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_sp.indexSource.addAllowedNamespace("Constraints.sp")
	
	# mp
	at_mp = MpcAttributeMetaData()
	at_mp.type = MpcAttributeType.IndexVector
	at_mp.name = 'mp'
	at_mp.group = 'Constraint pattern'
	at_mp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mp')+'<br/>') + 
		html_par('command to generate mp constraint')+
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_mp.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_mp.indexSource.addAllowedNamespace("Constraints.mp")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'constraintPattern'
	xom.addAttribute(at_sp)
	xom.addAttribute(at_mp)
	
	return xom

def writeTcl(pinfo):
	
	xobj = pinfo.analysis_step.XObject
	
	doc = PyMpc.App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
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
		pinfo.condition = doc.conditions.get(i)
		xobj_sp = pinfo.condition.XObject
		module_name = 'opensees.conditions.{}.{}'.format(xobj_sp.Xnamespace, xobj_sp.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl_spConstraints'):
			module.writeTcl_spConstraints(pinfo)
	
	'''
	mp
	'''
	mp_at = xobj.getAttribute('mp')
	if(mp_at is None):
		raise Exception('Error: cannot find "mp" attribute')
	mp = mp_at.indexVector
	
	for i in mp:
		if i == 0: continue
		item = doc.conditions[i]
		pinfo.condition = doc.conditions.get(i)
		xobj_mp = pinfo.condition.XObject
		module_name = 'opensees.conditions.{}.{}'.format(xobj_mp.Xnamespace, xobj_mp.name)
		module = importlib.import_module(module_name)
		if hasattr(module, 'writeTcl_mpConstraints'):
			module.writeTcl_mpConstraints(pinfo)