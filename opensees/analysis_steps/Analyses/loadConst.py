from PyMpc import *
from mpc_utils_html import *

def loadConstCommand(xom):
	
	'''
	loadConst <-time $pseudoTime>
	'''
	
	# loadConst
	at_loadConst = MpcAttributeMetaData()
	at_loadConst.type = MpcAttributeType.Boolean
	at_loadConst.name = 'loadConst'
	at_loadConst.group = 'loadConst'
	at_loadConst.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('loadConst')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LoadConst_Command','loadConst')+'<br/>') +
		html_end()
		)
	
	# pseudoTime
	at_use_pseudoTime = MpcAttributeMetaData()
	at_use_pseudoTime.type = MpcAttributeType.Boolean
	at_use_pseudoTime.name = 'use pseudoTime'
	at_use_pseudoTime.group = 'loadConst'
	at_use_pseudoTime.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIter')+'<br/>') +
		html_par('Time domain is to be set to (optional)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LoadConst_Command','pseudoTime')+'<br/>') +
		html_end()
		)
	
	# pseudoTime
	at_pseudoTime = MpcAttributeMetaData()
	at_pseudoTime.type = MpcAttributeType.Real
	at_pseudoTime.name = 'pseudoTime'
	at_pseudoTime.group = 'loadConst'
	at_pseudoTime.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIter')+'<br/>') +
		html_par('Time domain is to be set to (optional)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LoadConst_Command','pseudoTime')+'<br/>') +
		html_end()
		)
	
	xom.addAttribute(at_loadConst)
	xom.addAttribute(at_use_pseudoTime)
	xom.addAttribute(at_pseudoTime)
	
	xom.setVisibilityDependency(at_loadConst, at_pseudoTime)
	xom.setVisibilityDependency(at_loadConst, at_use_pseudoTime)
	xom.setVisibilityDependency(at_use_pseudoTime, at_pseudoTime)

def writeTcl_loadConst(pinfo, xobj):
	
	# loadConst <-time $pseudoTime>
	
	sopt =''
	
	loadConst_at = xobj.getAttribute('loadConst')
	if(loadConst_at is None):
		raise Exception('Error: cannot find "loadConst" attribute')
	if loadConst_at.boolean:
		pseudoTime_use_at = xobj.getAttribute('use pseudoTime')
		if(pseudoTime_use_at is None):
			raise Exception('Error: cannot find "use pseudoTime" attribute')
		if pseudoTime_use_at.boolean:
			pseudoTime_at = xobj.getAttribute('pseudoTime')
			if(pseudoTime_at is None):
				raise Exception('Error: cannot find "pseudoTime" attribute')
			pseudoTime = pseudoTime_at.real
			sopt += ' -time {}\n'.format(pseudoTime)
		
		str_tcl = '\n{}loadConst{}\n'.format(pinfo.indent, sopt)
	
		# now write the string into the file
		pinfo.out_file.write(str_tcl)