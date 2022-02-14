import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

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
			html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/MultiYieldSurfaceClay','MultiYieldSurfaceClay')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# nDmaterial MultiYieldSurfaceClay $matTag $nd $rho $G $K $cohesion $peakShearStrain
	nd = mka("nd", "Group", "number of dimensions, 2 for 2-D analysis (plane-strain), and 3 for 3-D analysis", MpcAttributeType.Integer)
	nd.sourceType = MpcAttributeSourceType.List
	nd.setSourceList([2, 3])
	nd.setDefault(2)

	rho = mka("rho", "Group", "Saturated soil mass density", MpcAttributeType.QuantityScalar)
	G = mka("G", "Group", "Reference low-strain shear modulus", MpcAttributeType.QuantityScalar)
	K = mka("K", "Group", "Reference bulk modulus", MpcAttributeType.QuantityScalar)
	cohesion = mka("cohesion", "Group", "Peak shear (apparent cohesion at zero effective confinement)", MpcAttributeType.QuantityScalar)
	peakShearStrain = mka("peakShearStrain", "Group", "Strain at peak shear, i.e., the octahedral shear strain at which the maximum shear strength is reached", MpcAttributeType.Real)


	xom = MpcXObjectMetaData()
	xom.name = 'MultiYieldSurfaceClay'
	xom.Xgroup = 'UC San Diego soil models'
	xom.addAttribute(nd)
	xom.addAttribute(rho)
	xom.addAttribute(G)
	xom.addAttribute(K)
	xom.addAttribute(cohesion)
	xom.addAttribute(peakShearStrain)

	return xom

def writeTcl(pinfo):

	# nDmaterial MultiYieldSurfaceClay $matTag $nd $rho $G $K $cohesion $peakShearStrain
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId

	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	# nDmaterial MultiYieldSurfaceClay $matTag $nd $rho $G $K $cohesion $peakShearStrain
	str_tcl = '{}nDMaterial MultiYieldSurfaceClay {} {} {} {} {} {} {}\n'.format(
			pinfo.indent,
			tag,
			geta('nd').integer,
			geta('rho').quantityScalar.value,
			geta('G').quantityScalar.value,
			geta('K').quantityScalar.value,
			geta('cohesion').quantityScalar.value,
			geta('peakShearStrain').real)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)