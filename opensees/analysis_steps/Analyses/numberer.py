from PyMpc import *
from mpc_utils_html import *

def numbererCommand(xom):
	
	'''
	numberer numbererType? arg1? ...
	'''
	
	# numbererType
	at_numbererType = MpcAttributeMetaData()
	at_numbererType.type = MpcAttributeType.String
	at_numbererType.name = 'numbererType'
	at_numbererType.group = 'numberer'
	at_numbererType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numbererType')+'<br/>') + 
		html_par('The following contain information about numbererType and the args required for each of the available dof numberer types:') +
		html_par('1. Plain Numberer') +
		html_par('2. Reverse Cuthill-McKee Numberer') +
		html_par('3. Alternative_Minimum_Degree Numberer') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Numberer_Command','Numberer Command')+'<br/>') +
		html_end()
		)
	at_numbererType.sourceType = MpcAttributeSourceType.List
	at_numbererType.setSourceList(['Plain Numberer', 'Reverse Cuthill-McKee Numberer', 'Alternative_Minimum_Degree Numberer', 'Parallel Reverse Cuthill-McKee Numberer'])
	at_numbererType.setDefault('Reverse Cuthill-McKee Numberer')
	
	xom.addAttribute(at_numbererType)

def writeTcl_numberer(pinfo, xobj):
	
	'''
	numberer Plain
	numberer RCM
	numberer AMD
	numberer ParallelRCM
	'''
	
	sopt = ''
	
	numbererType_at = xobj.getAttribute('numbererType')
	if(numbererType_at is None):
		raise Exception('Error: cannot find "numbererType" attribute')
	numbererType = numbererType_at.string
	
	if numbererType == 'Plain Numberer':
		str_tcl = '{}numberer Plain\n'.format(pinfo.indent)
	
	elif numbererType == 'Reverse Cuthill-McKee Numberer':
		str_tcl = '{}numberer RCM\n'.format(pinfo.indent)
	
	elif numbererType == 'Alternative_Minimum_Degree Numberer':
		str_tcl = '{}numberer AMD\n'.format(pinfo.indent)
		
	elif numbererType == 'Parallel Reverse Cuthill-McKee Numberer':
		str_tcl = '{}numberer ParallelRCM\n'.format(pinfo.indent)
	
	if pinfo.process_count > 1 and numbererType != 'Parallel Reverse Cuthill-McKee Numberer':
		IO.write_cerr('Warning : partitioned model, "Numberer" (in AnalysesCommand) different from "Parallel Reverse Cuthill-McKee Numberer" attribute, there may be some problems\n')
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)