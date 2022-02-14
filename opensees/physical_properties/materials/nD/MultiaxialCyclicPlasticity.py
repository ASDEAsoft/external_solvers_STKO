from opensees.physical_properties.utils.tester.EnableTester2DPlaneStrain import *
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
			html_par(html_href('https://opensees.berkeley.edu/OpenSees/manuals/usermanual/4192.htm ','MultiaxialCyclicPlasticity')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# nDMaterial MultiaxialCyclicPlasticity tag? rho? K? G? Su? Ho? h? m? beta? KCoeff? <eta?>
	rho = mka("rho", "Group", "Mass density", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	K = mka("K", "Group", "Bulk modulus", MpcAttributeType.Real)
	G = mka("G", "Group", " Maximum (small strain) Shear modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Su = mka("Su", "Group", "Undrained shear strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Ho = mka("Ho", "Group", "Linear kinematic hardening parameter of bounding surface", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	h = mka("h", "Group", "Exponential hardening parameter", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	m = mka("m", "Group", "Exponential hardening parameter", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	beta = mka("beta", "Group", "Integration parameter (use $beta=0.5 for midpoint rule)", MpcAttributeType.Real)
	KCoeff = mka("KCoeff", "Group", "Coefficient of horizontal earth pressure (not used at this moment)", MpcAttributeType.Real)

	# optional parameter
	use_Optional = mka("Optional", "Optional parameters", "", MpcAttributeType.Boolean)
	eta = mka("eta", "Optional parameters", "", MpcAttributeType.Real)

	xom = MpcXObjectMetaData()
	xom.name = 'MultiaxialCyclicPlasticity'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(rho)
	xom.addAttribute(K)
	xom.addAttribute(G)
	xom.addAttribute(Su)
	xom.addAttribute(Ho)
	xom.addAttribute(h)
	xom.addAttribute(m)
	xom.addAttribute(beta)
	xom.addAttribute(KCoeff)
	# optional parameter
	xom.addAttribute(use_Optional)
	xom.addAttribute(eta)
	# use optional paramiter
	xom.setVisibilityDependency(use_Optional, eta)

	return xom

def writeTcl(pinfo):

	# nDMaterial MultiaxialCyclicPlasticity tag? rho? K? G? Su? Ho? h? m? beta? KCoeff? <eta?>
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
		sopt += ' {}'.format(geta('eta').real)

	# nDMaterial MultiaxialCyclicPlasticity tag? rho? K? G? Su? Ho? h? m? beta? KCoeff? <eta?>
	str_tcl = '{}nDMaterial MultiaxialCyclicPlasticity {} {} {} {} {} {} {} {} {} {}{}\n'.format(
			pinfo.indent,
			tag,
			geta('rho').quantityScalar.value,
			geta('K').real,
			geta('G').quantityScalar.value,
			geta('Su').quantityScalar.value,
			geta('Ho').quantityScalar.value,
			geta('h').quantityScalar.value,
			geta('m').quantityScalar.value,
			geta('beta').real,
			geta('KCoeff').real,
			sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)