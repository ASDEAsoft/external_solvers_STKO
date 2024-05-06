# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *
from opensees.utils.override_utils import get_function_from_module

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import math

####################################################################################
# Utilities
####################################################################################

def _geta(xobj, name):
	at = xobj.getAttribute(name)
	if at is None:
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return at

def makeXObjectMetaData():
	
	def mka(name, group, descr, atype, adim = None, dval = None):
		a = MpcAttributeMetaData()
		a.type = atype
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/material/ndMaterials/Parallel3D.html','Parallel3D')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	# tags of sub-materials
	materials = mka("Materials", "Default", "A list of sub-materials", MpcAttributeType.IndexVector)
	materials.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	materials.indexSource.addAllowedNamespace('materials.nD')
	
	# weights of sub-materials
	use_weights = mka("Use Weights", "Default", "If checked, you can defined custom weights for each materials, otherwise all weights will be equal to 1", MpcAttributeType.Boolean)
	weights = mka("Weights", "Default", "A list of weights for each sub-material", MpcAttributeType.QuantityVector)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Parallel3D'
	xom.Xgroup = 'Other nD Materials'
	
	xom.addAttribute(materials)
	xom.addAttribute(use_weights)
	xom.addAttribute(weights)
	
	xom.setVisibilityDependency(use_weights, weights)
	
	return xom

def writeTcl(pinfo):
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	FMT = pinfo.get_double_formatter()
	
	# get materials
	materials = _geta(xobj, 'Materials').indexVector
	if len(materials) == 0:
		raise Exception('Parallel3D Error: "Materials" vector is empty')
	for i in range(len(materials)):
		if materials[i] == 0:
			raise Exception('Parallel3D Error: "Materials[{}]" is NULL'.format(i))
	materials_str = ' '.join(str(i) for i in materials)
	
	# get weights
	if _geta(xobj, 'Use Weights').boolean:
		weights = _geta(xobj, 'Weights').quantityVector
		if len(weights) != len(materials):
			raise Exception('Parallel3D Error: Length of "Materials" and "Weights" vector must match')
		for i in range(len(weights)):
			if weights.referenceValueAt(i) == 0.0:
				raise Exception('Parallel3D Error: "Weights[{}]" is 0.0'.format(i))
		weights_str = '-weights ' + ' '.join(FMT(weights.referenceValueAt(i)) for i in range(len(weights)))
	else:
		weights_str = ''
	
	# now write the string into the file
	pinfo.out_file.write("{}nDMaterial Parallel3D {}   {}   {}\n".format(pinfo.indent, tag, materials_str, weights_str))
