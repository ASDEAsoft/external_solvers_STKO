# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester2DPlaneStrain import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# threeDTag
	at_threeDTag = MpcAttributeMetaData()
	at_threeDTag.type = MpcAttributeType.Index
	at_threeDTag.name = 'threeDTag'
	at_threeDTag.group = 'Non-linear'
	at_threeDTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('threeDTag')+'<br/>') + 
		html_par('integer tag of previously defined 3d ndMaterial material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Strain_Material','Plane Strain Material')+'<br/>') +
		html_end()
		)
	at_threeDTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_threeDTag.indexSource.addAllowedNamespace('materials.nD')
	
	xom = MpcXObjectMetaData()
	xom.name = 'PlaneStrain'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_threeDTag)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial PlaneStrain $matTag $threeDtag
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	threeDtag_at = xobj.getAttribute('threeDTag')
	if(threeDtag_at is None):
		raise Exception('Error: cannot find "threeDTag" attribute')
	threeDtag = threeDtag_at.index
	
	str_tcl = '{}nDMaterial PlaneStrain {} {}\n'.format(pinfo.indent, tag, threeDtag)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)