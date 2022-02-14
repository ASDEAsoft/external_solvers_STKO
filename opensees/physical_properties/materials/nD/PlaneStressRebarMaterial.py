# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester2DPlaneStress import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# matTag
	at_matTag = MpcAttributeMetaData()
	at_matTag.type = MpcAttributeType.Index
	at_matTag.name = 'matTag'
	at_matTag.group = 'Default'
	at_matTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') + 
		html_par('tag of previously defined uniaxial material') +
		#html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Material','Plane Stress Material')+'<br/>') +
		html_end()
		)
	at_matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# angle
	at_angle = MpcAttributeMetaData()
	at_angle.type = MpcAttributeType.Real
	at_angle.name = 'angle'
	at_angle.group = 'Default'
	at_angle.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('angle')+'<br/>') + 
		html_par('angle in degrees defining the orientation of the rebar') +
		#html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Material','Plane Stress Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'PlaneStressRebarMaterial'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_matTag)
	xom.addAttribute(at_angle)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial PlaneStressRebarMaterial $tag $matTag
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	matTag_at = xobj.getAttribute('matTag')
	if(matTag_at is None):
		raise Exception('Error: cannot find "matTag" attribute')
	matTag = matTag_at.index
	
	angle_at = xobj.getAttribute('angle')
	if(angle_at is None):
		raise Exception('Error: cannot find "angle" attribute')
	angle = angle_at.real
	
	str_tcl = '{}nDMaterial PlaneStressRebarMaterial {} {} {}\n'.format(pinfo.indent, tag, matTag, angle)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)