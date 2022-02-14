import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# K
	at_name = MpcAttributeMetaData()
	at_name.type = MpcAttributeType.String
	at_name.name = 'ClassName'
	at_name.group = 'Default'
	at_name.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ClassName')+'<br/>') + 
		html_par('The custom material name') +
		html_end()
		)
	
	# data
	at_data = MpcAttributeMetaData()
	at_data.type = MpcAttributeType.StringVector
	at_data.name = 'Parameters'
	at_data.group = 'Default'
	at_data.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Parameters')+'<br/>') + 
		html_par('A list of material parameters') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'CustomMaterial'
	xom.Xgroup = 'Custom'
	xom.addAttribute(at_name)
	xom.addAttribute(at_data)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial $ClassName $Parameters
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	name_at = xobj.getAttribute('ClassName')
	if(name_at is None):
		raise Exception('Error: cannot find "ClassName" attribute')
	name = name_at.string
	
	data_at = xobj.getAttribute('Parameters')
	if(data_at is None):
		raise Exception('Error: cannot find "Parameters" attribute')
	data = data_at.stringVector
	
	str_tcl = '{}nDMaterial {} {} {}\n'.format(pinfo.indent, name, tag, ' '.join([p for p in data]))
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)