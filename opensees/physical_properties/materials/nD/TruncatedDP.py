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
			html_par(html_href('','TruncatedDP')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	ndm = mka("ndm", "Group", "Number of dimensions, 2 for plane-strain, and 3 for 3D analysis.", MpcAttributeType.Integer)
	ndm.sourceType = MpcAttributeSourceType.List
	ndm.setSourceList([2, 3])
	ndm.setDefault(2)
	rho = mka("rho", "Group", "Saturated mass density", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	G = mka("G", "Group", "Shear Modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	K = mka("K", "Group", "Bulk modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	# optional parameter
	use_Optional = mka("Optional", "Optional parameters", "", MpcAttributeType.Boolean)
	theta = mka("theta", "Optional parameters", "", MpcAttributeType.Real)
	alpha = mka("alpha", "Optional parameters", "", MpcAttributeType.Real)
	T = mka("T", "Optional parameters", "", MpcAttributeType.Real)
	tol = mka("tol", "Optional parameters", "", MpcAttributeType.Real)

	xom = MpcXObjectMetaData()
	xom.name = 'TruncatedDP'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(ndm)
	xom.addAttribute(rho)
	xom.addAttribute(G)
	xom.addAttribute(K)
	xom.addAttribute(use_Optional)
	xom.addAttribute(theta)
	xom.addAttribute(alpha)
	xom.addAttribute(T)
	xom.addAttribute(tol)
	# use optional paramiter
	xom.setVisibilityDependency(use_Optional, theta)
	xom.setVisibilityDependency(use_Optional, alpha)
	xom.setVisibilityDependency(use_Optional, T)
	xom.setVisibilityDependency(use_Optional, tol)

	return xom

def writeTcl(pinfo):
	# nDMaterial LinearCap tag? ndm? rho? G? K? <theta? alpha? T? tol?>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	# optional paramters
	sopt = ''
	if geta('Optional').boolean:
		sopt += ' {}'.format(geta('theta').real)
		sopt += ' {}'.format(geta('alpha').real)
		sopt += ' {}'.format(geta('T').real)
		sopt += ' {}'.format(geta('tol').real)

	# nDMaterial TruncatedDP tag? ndm? rho? G? K? <theta? alpha? T? tol?>
	str_tcl = '{}nDMaterial TruncatedDP {} {} {} {} {}{}\n'.format(
			pinfo.indent,
			tag,
			geta('ndm').integer,
			geta('rho').quantityScalar.value,
			geta('G').quantityScalar.value,
			geta('K').quantityScalar.value,
			sopt
			)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)