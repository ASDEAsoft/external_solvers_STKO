import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.utils.tcl_input as tclin
import math

def makeXObjectMetaData():
	
	def mka(name, type, description, dimension = None, default = None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = 'Default'
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(description) +
			#html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RigidLink_command','ASDAbsorbingBoundary3D')+'<br/>') +
			html_end()
			)
		if dimension:
			a.dimension = dimension
		if default:
			a.setDefault(default)
		return a
	
	G = mka('G', MpcAttributeType.QuantityScalar, 'The shear modulus of the soil domain', dimension = u.F/u.L/u.L)
	v = mka('v', MpcAttributeType.Real, "The Poisson's ratio of the soil domain")
	rho = mka('rho', MpcAttributeType.QuantityScalar, 'The mass density of the soil domain', dimension = u.F*u.t*u.t/u.L/u.L/u.L/u.L)
	
	# material
	material = mka('material', MpcAttributeType.Index, 'integer tag of previously defined 3d material (WARNING: under beta testing...)')
	material.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	material.indexSource.addAllowedNamespace('materials.nD')
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDAbsorbingBoundary3DMaterial'
	xom.Xgroup = 'absorbingBoundary'
	xom.addAttribute(G)
	xom.addAttribute(v)
	xom.addAttribute(rho)
	xom.addAttribute(material)
	
	return xom