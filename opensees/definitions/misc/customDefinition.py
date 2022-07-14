from PyMpc import *
from mpc_utils_html import *
from itertools import groupby, count

def makeXObjectMetaData():
	
	# at_script
	at_script = MpcAttributeMetaData()
	at_script.type = MpcAttributeType.String
	at_script.name = 'TCLscript'
	at_script.group = 'Group'
	at_script.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('TCL Script')+'<br/>') + 
		html_par((
			'Here you can write your own TCL code.<br/>'
			'A custom TCL code is useful to insert custom variables and functions.'
			)) +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_script.stringType = 'TCLscript'
	
	xom = MpcXObjectMetaData()
	xom.name = 'customDefinition'
	xom.addAttribute(at_script)
	
	return xom

def writeTcl(pinfo):
	
	xobj = pinfo.definition.XObject
	at_script = xobj.getAttribute('TCLscript')
	if(at_script is None):
		raise Exception('Error: cannot find "TCLscript" attribute')
	if at_script.string:
		# write a comment with the name of the document components this xobject belongs to.
		pinfo.out_file.write('\n{}#TCL script: {}\n'.format(pinfo.indent, xobj.parent.componentName))
		# pinfo.out_file.write('{}{}'.format(pinfo.indent, at_script.string))
		# the custom string comes from a scintilla edit. on windows there is \r\n.
		# now python (on windows) converts \n into \r\n, ... but if we have \r\n then 
		# it will be converted into \r\r\n
		pinfo.out_file.write('{}{}\n'.format(pinfo.indent, at_script.string.replace('\r', '')))
