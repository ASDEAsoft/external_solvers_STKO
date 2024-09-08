# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	def mka(type, name, group, description):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(description) +
			html_end()
			)
		return a
	
	# material
	material = mka(MpcAttributeType.Index, 'material', 'Source', 
		'integer tag of previously defined 3d material')
	material.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	material.indexSource.addAllowedNamespace('materials.nD')
	
	# initial strain
	eps0 = mka(MpcAttributeType.Real, 'eps0', 'Initial strain',
		'The scalar strain component for epsXX epsYY and epsZZ')
	
	xom = MpcXObjectMetaData()
	xom.name = 'InitStrain'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(material)
	xom.addAttribute(eps0)
	
	return xom

def writeTcl(pinfo):
	# nDMaterial InitStrain tag? otherTag? eps0
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
		
	# mandatory parameters
	material = geta('material').index
	eps0 = geta('eps0').real
	
	# TODO: check parameters...
	str_tcl = '{}nDMaterial InitStrain {} {} {}\n'.format(
		pinfo.indent, tag, material, eps0)
	print(str_tcl)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
	