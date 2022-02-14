from PyMpc import *
from mpc_utils_html import *

def wipeAnalysisCommand(xom):
	
	'''
	wipeAnalysis
	'''
	
	# wipeAnalysis
	at_wipeAnalysis = MpcAttributeMetaData()
	at_wipeAnalysis.type = MpcAttributeType.Boolean
	at_wipeAnalysis.name = 'wipeAnalysis'
	at_wipeAnalysis.group = 'wipeAnalysis'
	at_wipeAnalysis.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('wipeAnalysis')+'<br/>') +
		html_par('If selected (default), STKO will add a wipeAnalysis command at the end of the analysis in order to destroy all components of the Analysis object') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/WipeAnalysis_Command','wipeAnalysis')+'<br/>') +
		html_end()
		)
	at_wipeAnalysis.setDefault(True)
	
	xom.addAttribute(at_wipeAnalysis)

def writeTcl_wipeAnalysis(pinfo, xobj):
	
	# wipeAnalysis 
	
	sopt =''
	
	wipeAnalysis_at = xobj.getAttribute('wipeAnalysis')
	if(wipeAnalysis_at is None):
		raise Exception('Error: cannot find "wipeAnalysis" attribute')
	if wipeAnalysis_at.boolean:
		str_tcl = '{}wipeAnalysis\n'.format(pinfo.indent)
	
		# now write the string into the file
		pinfo.out_file.write(str_tcl)