# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# tag
	at_tag = MpcAttributeMetaData()
	at_tag.type = MpcAttributeType.Index
	at_tag.name = 'tag'
	at_tag.group = 'Non-linear'
	at_tag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tag')+'<br/>') + 
		html_par('Unique material object integer tag for the material that is being wrapped') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fatigue_Material','Fatigue Material')+'<br/>') +
		html_end()
		)
	at_tag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_tag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# -E0
	at_use_E0 = MpcAttributeMetaData()
	at_use_E0.type = MpcAttributeType.Boolean
	at_use_E0.name = '-E0'
	at_use_E0.group = 'Non-linear'
	at_use_E0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-E0')+'<br/>') + 
		html_par('Value of strain at which one cycle will cause failure (default 0.191)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fatigue_Material','Fatigue Material')+'<br/>') +
		html_end()
		)
	
	# E0
	at_E0 = MpcAttributeMetaData()
	at_E0.type = MpcAttributeType.Real
	at_E0.name = 'E0'
	at_E0.group = '-E0'
	at_E0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E0')+'<br/>') + 
		html_par('Value of strain at which one cycle will cause failure (default 0.191)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fatigue_Material','Fatigue Material')+'<br/>') +
		html_end()
		)
	at_E0.setDefault(0.191)
	
	# -m
	at_use_m = MpcAttributeMetaData()
	at_use_m.type = MpcAttributeType.Boolean
	at_use_m.name = '-m'
	at_use_m.group = 'Non-linear'
	at_use_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-m')+'<br/>') + 
		html_par('Slope of Coffin-Manson curve in log-log space (default -0.458)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fatigue_Material','Fatigue Material')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.Real
	at_m.name = 'm'
	at_m.group = '-m'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') + 
		html_par('Slope of Coffin-Manson curve in log-log space (default -0.458)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fatigue_Material','Fatigue Material')+'<br/>') +
		html_end()
		)
	at_m.setDefault(-0.458)
	
	# -min
	at_use_min = MpcAttributeMetaData()
	at_use_min.type = MpcAttributeType.Boolean
	at_use_min.name = '-min'
	at_use_min.group = 'Non-linear'
	at_use_min.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-min')+'<br/>') + 
		html_par('Global minimum value for strain or deformation (default -1e16)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fatigue_Material','Fatigue Material')+'<br/>') +
		html_end()
		)
	
	# min
	at_min = MpcAttributeMetaData()
	at_min.type = MpcAttributeType.Real
	at_min.name = 'min'
	at_min.group = '-min'
	at_min.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('min')+'<br/>') + 
		html_par('Global minimum value for strain or deformation (default -1e16)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fatigue_Material','Fatigue Material')+'<br/>') +
		html_end()
		)
	at_min.setDefault(-1e16)
	
	# -max
	at_use_max = MpcAttributeMetaData()
	at_use_max.type = MpcAttributeType.Boolean
	at_use_max.name = '-max'
	at_use_max.group = 'Non-linear'
	at_use_max.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-max')+'<br/>') + 
		html_par('Global maximum value for strain or deformation (default 1e16)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fatigue_Material','Fatigue Material')+'<br/>') +
		html_end()
		)
	
	# max
	at_max = MpcAttributeMetaData()
	at_max.type = MpcAttributeType.Real
	at_max.name = 'max'
	at_max.group = '-max'
	at_max.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('max')+'<br/>') + 
		html_par('Global maximum value for strain or deformation (default 1e16)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fatigue_Material','Fatigue Material')+'<br/>') +
		html_end()
		)
	at_max.setDefault(1e16)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Fatigue'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_tag)
	xom.addAttribute(at_use_E0)
	xom.addAttribute(at_E0)
	xom.addAttribute(at_use_m)
	xom.addAttribute(at_m)
	xom.addAttribute(at_use_min)
	xom.addAttribute(at_min)
	xom.addAttribute(at_use_max)
	xom.addAttribute(at_max)
	
	# E0-dep
	xom.setVisibilityDependency(at_use_E0, at_E0)
	
	# m-dep
	xom.setVisibilityDependency(at_use_m, at_m)
	
	# min-dep
	xom.setVisibilityDependency(at_use_min, at_min)
	
	# max-dep
	xom.setVisibilityDependency(at_use_max, at_max)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Fatigue $matTag $tag <-E0 $E0> <-m $m> <-min $min> <-max $max>
	
	xobj = pinfo.phys_prop.XObject
	matTag = xobj.parent.componentId
	
	# mandatory parameters
	tag_at = xobj.getAttribute('tag')
	if(tag_at is None):
		raise Exception('Error: cannot find "tag" attribute')
	tag = tag_at.index
	
	
	# optional paramters
	sopt = ''
	
	use_E0_at = xobj.getAttribute('-E0')
	if(use_E0_at is None):
		raise Exception('Error: cannot find "-E0" attribute')
	use_E0 = use_E0_at.boolean
	if use_E0:
		E0_at = xobj.getAttribute('E0')
		if(E0_at is None):
			raise Exception('Error: cannot find "E0" attribute')
		E0 = E0_at.real
		
		sopt += '-E0 {}'.format(E0)
	
	use_m_at = xobj.getAttribute('-m')
	if(use_m_at is None):
		raise Exception('Error: cannot find "-m" attribute')
	use_m = use_m_at.boolean
	if use_m:
		m_at = xobj.getAttribute('m')
		if(m_at is None):
			raise Exception('Error: cannot find "m" attribute')
		m = m_at.real
		
		sopt += ' -m {}'.format(m)
	
	use_min_at = xobj.getAttribute('-min')
	if(use_min_at is None):
		raise Exception('Error: cannot find "-min" attribute')
	use_min = use_min_at.boolean
	if use_min:
		min_at = xobj.getAttribute('min')
		if(min_at is None):
			raise Exception('Error: cannot find "min" attribute')
		min = min_at.real
		
		sopt += ' -min {}'.format(min)
	
	use_max_at = xobj.getAttribute('-max')
	if(use_max_at is None):
		raise Exception('Error: cannot find "-max" attribute')
	use_max = use_max_at.boolean
	if use_max:
		max_at = xobj.getAttribute('max')
		if(max_at is None):
			raise Exception('Error: cannot find "max" attribute')
		max = max_at.real
		
		sopt += ' -max {}'.format(max)
	
	
	str_tcl = '{}uniaxialMaterial Fatigue {} {}\n'.format(pinfo.indent, matTag, tag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)