# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# source
	source = MpcAttributeMetaData()
	source.type = MpcAttributeType.Index
	source.name = 'Source Material Tag'
	source.group = 'Source'
	source.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Source Material Tag')+'<br/>') + 
		html_par('integer tag of previously defined 3d nDMaterial material') +
		html_end()
		)
	source.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	source.indexSource.addAllowedNamespace('materials.nD')
	
	# sig0
	sig0 = MpcAttributeMetaData()
	sig0.type = MpcAttributeType.QuantityScalar
	sig0.name = 'sig0'
	sig0.group = 'Initial Conditions'
	sig0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sig0')+'<br/>') + 
		html_par('Scalar initial stress.<br/>'
			'The initial strain eps0 will be computed from a stress tensor = I*sig0.<br/>'
			'Finally the stress is computed as  stress = f(strain + eps0)') +
		html_end()
		)
	sig0.dimension = u.F/u.L**2
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'InitStress'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(source)
	xom.addAttribute(sig0)
	return xom

def writeTcl(pinfo):
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	source = geta('Source Material Tag').index
	sig0 = geta('sig0').quantityScalar.value
	str_tcl = '{}nDMaterial InitStress {} {} {}\n'.format(pinfo.indent, tag, source, sig0)
	pinfo.out_file.write(str_tcl)
	