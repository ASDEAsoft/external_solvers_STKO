# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# otherTag
	at_otherTag = MpcAttributeMetaData()
	at_otherTag.type = MpcAttributeType.Index
	at_otherTag.name = 'otherTag'
	at_otherTag.group = 'Non-linear'
	at_otherTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('otherTag')+'<br/>') + 
		html_par('tag of the other material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Initial_Strain_Material','Initial Strain Material')+'<br/>') +
		html_end()
		)
	at_otherTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_otherTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# initStrain
	at_initStrain = MpcAttributeMetaData()
	at_initStrain.type = MpcAttributeType.Real
	at_initStrain.name = 'initStrain'
	at_initStrain.group = 'Non-linear'
	at_initStrain.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('initStrain')+'<br/>') + 
		html_par('initial strain') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Initial_Strain_Material','Initial Strain Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'InitStrainMaterial'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_otherTag)
	xom.addAttribute(at_initStrain)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial InitStrainMaterial $matTag $otherTag $initStrain
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	otherTag_at = xobj.getAttribute('otherTag')
	if(otherTag_at is None):
		raise Exception('Error: cannot find "otherTag" attribute')
	otherTag = otherTag_at.index
	
	initStrain_at = xobj.getAttribute('initStrain')
	if(initStrain_at is None):
		raise Exception('Error: cannot find "initStrain" attribute')
	initStrain = initStrain_at.real
	
	
	str_tcl = '{}uniaxialMaterial InitStrainMaterial {} {} {}\n'.format(pinfo.indent, tag, otherTag, initStrain)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)