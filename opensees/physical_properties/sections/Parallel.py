import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# tag
	at_tag = MpcAttributeMetaData()
	at_tag.type = MpcAttributeType.IndexVector
	at_tag.name = 'tag'
	at_tag.group = 'Material'
	at_tag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tag')+'<br/>') + 
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_tag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_tag.indexSource.addAllowedNamespace('sections')
	
	xom = MpcXObjectMetaData()
	xom.name = 'Parallel'
	xom.addAttribute(at_tag)
	
	return xom

def writeTcl(pinfo):
	
	#section Parallel tag? tag1? tag2? ...
	
	xobj = pinfo.phys_prop.XObject
	secTag = xobj.parent.componentId
	
	# mandatory parameters
	tag_at = xobj.getAttribute('tag')
	if(tag_at is None):
		raise Exception('Error: cannot find "tag" attribute')
	tag = tag_at.indexVector
	
	#set list TCL
	tag_str = ''
	
	for i in range(len(tag)):
			tag_str += ' {}'.format(tag[i])
	
	str_tcl = '{}section Parallel {}{}\n'.format(pinfo.indent, secTag, tag_str)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)