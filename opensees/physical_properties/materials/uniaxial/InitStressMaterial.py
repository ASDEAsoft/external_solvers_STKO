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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Initial_Stress_Material','Initial Stress Material')+'<br/>') +
		html_end()
		)
	at_otherTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_otherTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# initStress
	at_initStress = MpcAttributeMetaData()
	at_initStress.type = MpcAttributeType.QuantityScalar
	at_initStress.name = 'initStress'
	at_initStress.group = 'Non-linear'
	at_initStress.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('initStress')+'<br/>') + 
		html_par('initial strain') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Initial_Stress_Material','Initial Stress Material')+'<br/>') +
		html_end()
		)
	at_initStress.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'InitStressMaterial'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_otherTag)
	xom.addAttribute(at_initStress)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial InitStressMaterial $matTag $otherTag $initStress
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	otherTag_at = xobj.getAttribute('otherTag')
	if(otherTag_at is None):
		raise Exception('Error: cannot find "otherTag" attribute')
	otherTag = otherTag_at.index
	
	initStress_at = xobj.getAttribute('initStress')
	if(initStress_at is None):
		raise Exception('Error: cannot find "initStress" attribute')
	initStress = initStress_at.quantityScalar
	
	
	str_tcl = '{}uniaxialMaterial InitStressMaterial {} {} {}\n'.format(pinfo.indent, tag, otherTag, initStress.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)