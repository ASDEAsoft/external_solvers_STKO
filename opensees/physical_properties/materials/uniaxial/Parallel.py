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
	at_tag.group = 'Materials'
	at_tag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tag')+'<br/>') + 
		html_par('identification tags of materials making up the material model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parallel_Material','Parallel Material')+'<br/>') +
		html_end()
		)
	at_tag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_tag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# -factors
	at_factors = MpcAttributeMetaData()
	at_factors.type = MpcAttributeType.Boolean
	at_factors.name = '-factors'
	at_factors.group = 'Optional parameters'
	at_factors.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-factors')+'<br/>') + 
		html_par('factor to create a linear combination of the specified materials. Factor can be negative to subtract one material from an other. (optional, default = 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parallel_Material','Parallel Material')+'<br/>') +
		html_end()
		)
	
	# fact
	at_fact = MpcAttributeMetaData()
	at_fact.type = MpcAttributeType.QuantityVector
	at_fact.name = 'fact'
	at_fact.group = '-factors'
	at_fact.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fact')+'<br/>') + 
		html_par('factor to create a linear combination of the specified materials. Factor can be negative to subtract one material from an other. (optional, default = 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parallel_Material','Parallel Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Parallel'
	xom.Xgroup = 'Some Standard Uniaxial Materials'
	xom.addAttribute(at_tag)
	xom.addAttribute(at_factors)
	xom.addAttribute(at_fact)
	
	# factors-dep
	xom.setVisibilityDependency(at_factors, at_fact)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Parallel $matTag $tag1 $tag2 ... <-factors $fact1 $fact2 ...>
	
	xobj = pinfo.phys_prop.XObject
	matTag = xobj.parent.componentId
	
	# mandatory parameters
	tag_at = xobj.getAttribute('tag')
	if(tag_at is None):
		raise Exception('Error: cannot find "tag" attribute')
	tag = tag_at.indexVector
	
	#set list TCL
	tag_str = ''
	
	for i in range(len(tag)):
		tag_str += ' {}'.format(tag[i])
	
	# optional paramters
	fact_str = ''
	
	factors_at = xobj.getAttribute('-factors')
	if(factors_at is None):
		raise Exception('Error: cannot find "-factors" attribute')
	factors = factors_at.boolean
	if factors:
		fact_at = xobj.getAttribute('fact')
		if(fact_at is None):
			raise Exception('Error: cannot find "fact" attribute')
		fact = fact_at.quantityVector
		
		if(len(fact)!=len(tag)):
			raise Exception('Error: different length of vectors')
		
		#set list TCL
		fact_str = ' -factors'
		for i in range(len(tag)):
			fact_str += ' {}'.format(fact.valueAt(i))
	
	str_tcl = '{}uniaxialMaterial Parallel {}{}{}\n'.format(pinfo.indent, matTag, tag_str, fact_str)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
