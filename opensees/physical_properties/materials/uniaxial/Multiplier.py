# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	def mka(name, type, description):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = 'Default'
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(description) +
			#html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Parallel_Material','Parallel Material')+'<br/>') +
			html_end()
			)
		return a
	
	# otherTag
	at_otherTag = mka('otherTag', MpcAttributeType.Index, 'The tag of a previously defined uniaxial material')
	at_otherTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_otherTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# multiplier
	at_multiplier = mka('multiplier', MpcAttributeType.Real, 'The multiplier factor, such that sigma = multiplier * sigma_other_material')
	at_multiplier.setDefault(1.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Multiplier'
	xom.Xgroup = 'Some Standard Uniaxial Materials'
	xom.addAttribute(at_otherTag)
	xom.addAttribute(at_multiplier)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Multiplier $matTag $otherTag $multiplier
	
	xobj = pinfo.phys_prop.XObject
	matTag = xobj.parent.componentId
	
	# parameters
	
	at_otherTag = xobj.getAttribute('otherTag')
	if at_otherTag is None:
		raise Exception('Error: cannot find "otherTag" attribute')
	otherTag = at_otherTag.index
	
	at_multiplier = xobj.getAttribute('multiplier')
	if at_multiplier is None:
		raise Exception('Error: cannot find "multiplier" attribute')
	multiplier = at_multiplier.real
	
	str_tcl = '{}uniaxialMaterial Multiplier {} {} {}\n'.format(pinfo.indent, matTag, otherTag, multiplier)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
