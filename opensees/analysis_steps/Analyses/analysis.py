from PyMpc import *
from mpc_utils_html import *

def analysisCommand(xom):
	
	'''
	analysis analysisType?
	'''
	
	# analysisCommand
	at_analysisType = MpcAttributeMetaData()
	at_analysisType.type = MpcAttributeType.String
	at_analysisType.name = 'analysisType'
	at_analysisType.group = 'analysis'
	at_analysisType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('analysisCommand')+'<br/>') + 
		html_par('char string identifying type of analysis object to be constructed. Currently 3 valid options:') +
		html_par('1. Static - for static analysis') +
		html_par('2. Transient - for transient analysis with constant time step') +
		html_par('3. VariableTransient - for transient analysis with variable time step') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Analysis_Command','Analysis Command')+'<br/>') +
		html_end()
		)
	at_analysisType.sourceType = MpcAttributeSourceType.List
	at_analysisType.setSourceList(['Static', 'Transient'])
	at_analysisType.setDefault('Static')
	
	# VariableTransient
	# at_VariableTransient = MpcAttributeMetaData()
	# at_VariableTransient.type = MpcAttributeType.Boolean
	# at_VariableTransient.name = 'VariableTransient'
	# at_VariableTransient.group = 'analysis'
	# at_VariableTransient.description = (
		# html_par(html_begin()) +
		# html_par(html_boldtext('VariableTransient')+'<br/>') +
		# html_par('for transient analysis with variable time step') +
		# html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Analysis_Command','Analysis Command')+'<br/>') +
		# html_end()
		# )
	
	
	xom.addAttribute(at_analysisType)
	# xom.addAttribute(at_VariableTransient)

def writeTcl_analysis(pinfo, xobj):
	
	# analysis analysisType?
	
	sopt = ''
	
	analysisType_at = xobj.getAttribute('analysisType')
	if(analysisType_at is None):
		raise Exception('Error: cannot find "VariableTransient" attribute')
	analysisType = analysisType_at.string
	
	Transient_at = xobj.getAttribute('Transient')
	if(Transient_at is None):
		raise Exception('Error: cannot find "Transient" attribute')
	# if Transient_at.boolean:
		# VariableTransient_at = xobj.getAttribute('VariableTransient')
		# if(VariableTransient_at is None):
			# raise Exception('Error: cannot find "VariableTransient" attribute')
		# if VariableTransient_at.boolean:
			# sopt += 'Variable'
	
	str_tcl = '{}analysis {}{}\n'.format(pinfo.indent, sopt, analysisType)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)