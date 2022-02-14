# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester2DPlaneStress import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin


def makeXObjectMetaData():
	
	# threeDtag
	at_threeDtag = MpcAttributeMetaData()
	at_threeDtag.type = MpcAttributeType.Index
	at_threeDtag.name = 'threeDtag'
	at_threeDtag.group = 'Non-linear'
	at_threeDtag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('threeDtag')+'<br/>') + 
		html_par('tag of previously defined 3d ndMaterial material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Material','Plane Stress Material')+'<br/>') +
		html_end()
		)
	at_threeDtag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_threeDtag.indexSource.addAllowedNamespace('materials.nD')
	
	xom = MpcXObjectMetaData()
	xom.name = 'PlaneStress'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_threeDtag)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial PlaneStress $matTag $threeDtag
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	threeDtag_at = xobj.getAttribute('threeDtag')
	if(threeDtag_at is None):
		raise Exception('Error: cannot find "threeDtag" attribute')
	threeDtag = threeDtag_at.index
	
	str_tcl = '{}nDMaterial PlaneStress {} {}\n'.format(pinfo.indent, tag, threeDtag)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)