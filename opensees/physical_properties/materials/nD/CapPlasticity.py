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
			html_par(html_href('','CapPlasticity')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# nDMaterial CapPlasticity $tag $ndm $rho $G $K $X $D $W $R $lambda $theta $beta $alpha $T $tol
	ndm = mka("ndm", "Group", "Number of dimensions, 2 for plane-strain, and 3 for 3D analysis.", MpcAttributeType.Integer)
	ndm.sourceType = MpcAttributeSourceType.List
	ndm.setSourceList([2, 3])
	ndm.setDefault(2)
	rho = mka("rho", "Group", "Mass density", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	G = mka("G", "Group", "Maximum (small strain) Shear modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	K = mka("K", "Group", "Bulk modulus", MpcAttributeType.Real)
	X = mka("X", "Group", "Bulk modulus", MpcAttributeType.Real)
	D = mka("D", "Group", "", MpcAttributeType.Real)
	W = mka("W", "Group", "", MpcAttributeType.Real)
	R = mka("R", "Group", "", MpcAttributeType.Real)
	lambda_ = mka("lambda", "Group", "", MpcAttributeType.Real)
	theta = mka("theta", "Group", "", MpcAttributeType.Real)
	beta = mka("beta", "Group", "", MpcAttributeType.Real)
	alpha = mka("alpha", "Group", "", MpcAttributeType.Real)
	T = mka("T", "Group", "", MpcAttributeType.Real)
	tol = mka("tol", "Group", "", MpcAttributeType.Real)

	xom = MpcXObjectMetaData()
	xom.name = 'CapPlasticity'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(ndm)
	xom.addAttribute(rho)
	xom.addAttribute(G)
	xom.addAttribute(K)
	xom.addAttribute(X)
	xom.addAttribute(D)
	xom.addAttribute(W)
	xom.addAttribute(R)
	xom.addAttribute(lambda_)
	xom.addAttribute(theta)
	xom.addAttribute(beta)
	xom.addAttribute(alpha)
	xom.addAttribute(T)
	xom.addAttribute(tol)

	return xom

def writeTcl(pinfo):

	# nDMaterial CapPlasticity $tag $ndm $rho $G $K $X $D $W $R $lambda $theta $beta $alpha $T $tol
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId

	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	# nDMaterial CapPlasticity $tag $ndm $rho $G $K $X $D $W $R $lambda $theta $beta $alpha $T $tol
	str_tcl = '{}nDMaterial CapPlasticity {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent,
			tag,
			geta('ndm').integer,
			geta('rho').quantityScalar.value,
			geta('G').quantityScalar.value,
			geta('K').real,
			geta('X').real,
			geta('D').real,
			geta('W').real,
			geta('R').real,
			geta('lambda').real,
			geta('theta').real,
			geta('beta').real,
			geta('alpha').real,
			geta('T').real,
			geta('tol').real)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)