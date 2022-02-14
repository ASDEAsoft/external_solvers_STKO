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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MinMax_Material','MinMax Material')+'<br/>') +
		html_end()
		)
	at_otherTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_otherTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# -min
	at_min = MpcAttributeMetaData()
	at_min.type = MpcAttributeType.Boolean
	at_min.name = '-min'
	at_min.group = 'Non-linear'
	at_min.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-min')+'<br/>') + 
		html_par('minimum value of strain. optional default = -1.0e16.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MinMax_Material','MinMax Material')+'<br/>') +
		html_end()
		)
	
	# minStrain
	at_minStrain = MpcAttributeMetaData()
	at_minStrain.type = MpcAttributeType.Real
	at_minStrain.name = 'minStrain'
	at_minStrain.group = '-min'
	at_minStrain.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('minStrain')+'<br/>') + 
		html_par('minimum value of strain. optional default = -1.0e16.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MinMax_Material','MinMax Material')+'<br/>') +
		html_end()
		)
	at_minStrain.setDefault(-1.0e16)
	
	# -max
	at_max = MpcAttributeMetaData()
	at_max.type = MpcAttributeType.Boolean
	at_max.name = '-max'
	at_max.group = 'Non-linear'
	at_max.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-max')+'<br/>') + 
		html_par('max value of strain. optional default = 1.0e16.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MinMax_Material','MinMax Material')+'<br/>') +
		html_end()
		)
	
	# maxStrain
	at_maxStrain = MpcAttributeMetaData()
	at_maxStrain.type = MpcAttributeType.Real
	at_maxStrain.name = 'maxStrain'
	at_maxStrain.group = '-max'
	at_maxStrain.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxStrain')+'<br/>') + 
		html_par('max value of strain. optional default = 1.0e16.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MinMax_Material','MinMax Material')+'<br/>') +
		html_end()
		)
	at_maxStrain.setDefault(1.0e16)
	
	xom = MpcXObjectMetaData()
	xom.name = 'MinMax'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_otherTag)
	xom.addAttribute(at_min)
	xom.addAttribute(at_minStrain)
	xom.addAttribute(at_max)
	xom.addAttribute(at_maxStrain)
	
	# minStrain-dep
	xom.setVisibilityDependency(at_min, at_minStrain)
	
	# maxStrain-dep
	xom.setVisibilityDependency(at_max, at_maxStrain)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial MinMax $matTag $otherTag <-min $minStrain> <-max $maxStrain>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	otherTag_at = xobj.getAttribute('otherTag')
	if(otherTag_at is None):
		raise Exception('Error: cannot find "otherTag" attribute')
	otherTag = otherTag_at.index
	
	
	# optional paramters
	sopt = ''
	
	min_at = xobj.getAttribute('-min')
	if(min_at is None):
		raise Exception('Error: cannot find "-min" attribute')
	min = min_at.boolean
	if min:
		minStrain_at = xobj.getAttribute('minStrain')
		if(minStrain_at is None):
			raise Exception('Error: cannot find "minStrain" attribute')
		minStrain = minStrain_at.real
		
		sopt += ' -min {}'.format(minStrain)
	
	max_at = xobj.getAttribute('-max')
	if(max_at is None):
		raise Exception('Error: cannot find "-max" attribute')
	max = max_at.boolean
	if max:
		maxStrain_at = xobj.getAttribute('maxStrain')
		if(maxStrain_at is None):
			raise Exception('Error: cannot find "maxStrain" attribute')
		maxStrain = maxStrain_at.real
		
		sopt += ' -max {}'.format(maxStrain)
	
	
	str_tcl = '{}uniaxialMaterial MinMax {} {}{}\n'.format(pinfo.indent, tag, otherTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)