# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# tag
	at_tag = MpcAttributeMetaData()
	at_tag.type = MpcAttributeType.IndexVector
	at_tag.name = 'tag'
	at_tag.group = 'Identifications'
	at_tag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tag')+'<br/>') + 
		html_par('identification tag of materials making up the material model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Series_Material','Series Material')+'<br/>') +
		html_end()
		)
	at_tag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_tag.indexSource.addAllowedNamespaceList(["materials.uniaxial", "material.nD"])
	
	xom = MpcXObjectMetaData()
	xom.name = 'Series'
	xom.Xgroup = 'Some Standard Uniaxial Materials'
	xom.addAttribute(at_tag)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Series $matTag $tag1 $tag2 ...
	
	xobj = pinfo.phys_prop.XObject
	matTag = xobj.parent.componentId
	
	# mandatory parameters
	tag_at = xobj.getAttribute('tag')
	if(tag_at is None):
		raise Exception('Error: cannot find "tag" attribute')
	tag = tag_at.indexVector
	if len(tag) == 0:
		raise Exception('Error: the list of materials for the parallel material is empty')
	
	# build command string
	str_tcl = '{}uniaxialMaterial Series {} '.format(pinfo.indent, matTag)
	
	# append all sub-material tags
	n = 1
	for i in range(len(tag)):
		if (i == (3*n)):
			str_tcl += '\\\n{}\t'.format(pinfo.indent)
			n += 1
		if (i != len(tag)-1):
			str_tcl += '{} '.format(tag[i])
		else:
			str_tcl += '{}'.format(tag[i])
	str_tcl += '\n'
	
	# write command
	pinfo.out_file.write(str_tcl)