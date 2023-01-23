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
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/material/ndMaterials/Series3D.html','Series3D')+'<br/>') +
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
	
	# advanced settings
	use_settings = mka("Use Settings", "Advanced Settings", "If checked, you can defined some advanced settings", MpcAttributeType.Boolean)
	mite = mka("Max Iterations", "Advanced Settings", "The maximum number of iterations to impose the iso-stress condition, optional, default = 10", MpcAttributeType.Integer, dval=10)
	rtol = mka("Relative Tolerance", "Advanced Settings", "The relative stress tolerance for the iso-stress condition, optional, default = 1.0e-4", MpcAttributeType.Real, dval=1.0e-4)
	atol = mka("Absolute Tolerance", "Advanced Settings", "The absolute stress tolerance for the iso-stress condition, optional, default = 1.0e-8", MpcAttributeType.Real, dval=1.0e-8)
	verbose = mka("Verbose", "Advanced Settings", "Activates the verbosity. Use for debug purposed", MpcAttributeType.Boolean)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Series3D'
	xom.Xgroup = 'Other nD Materials'
	
	xom.addAttribute(materials)
	xom.addAttribute(use_weights)
	xom.addAttribute(weights)
	xom.addAttribute(use_settings)
	xom.addAttribute(mite)
	xom.addAttribute(rtol)
	xom.addAttribute(atol)
	xom.addAttribute(verbose)
	
	xom.setVisibilityDependency(use_weights, weights)
	xom.setVisibilityDependency(use_settings, mite)
	xom.setVisibilityDependency(use_settings, rtol)
	xom.setVisibilityDependency(use_settings, atol)
	xom.setVisibilityDependency(use_settings, verbose)
	
	return xom

def writeTcl(pinfo):
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	FMT = pinfo.get_double_formatter()
	
	# get materials
	materials = _geta(xobj, 'Materials').indexVector
	if len(materials) == 0:
		raise Exception('Series3D Error: "Materials" vector is empty')
	for i in range(len(materials)):
		if materials[i] == 0:
			raise Exception('Series3D Error: "Materials[{}]" is NULL'.format(i))
	materials_str = ' '.join(str(i) for i in materials)
	
	# get weights
	if _geta(xobj, 'Use Weights').boolean:
		weights = _geta(xobj, 'Weights').quantityVector
		if len(weights) != len(materials):
			raise Exception('Series3D Error: Length of "Materials" and "Weights" vector must match')
		for i in range(len(weights)):
			if weights.referenceValueAt(i) == 0.0:
				raise Exception('Series3D Error: "Weights[{}]" is 0.0'.format(i))
		weights_str = '-weights ' + ' '.join(FMT(weights.referenceValueAt(i)) for i in range(len(weights)))
	else:
		weights_str = ''
	
	# advanced settings
	if _geta(xobj, 'Use Settings').boolean:
		mite = _geta(xobj, 'Max Iterations').integer
		rtol = _geta(xobj, 'Relative Tolerance').real
		atol = _geta(xobj, 'Absolute Tolerance').real
		opt_str = '-maxIter {} -relTol {} -absTol {}'.format(mite, FMT(rtol), FMT(atol))
		if _geta(xobj, 'Verbose').boolean:
			opt_str += ' -verbose'
	else:
		opt_str = ''
	
	# now write the string into the file
	pinfo.out_file.write("{}nDMaterial Series3D {}   {}   {}   {}\n".format(pinfo.indent, tag, materials_str, weights_str, opt_str))
