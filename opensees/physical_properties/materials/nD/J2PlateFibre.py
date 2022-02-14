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
			html_par(html_href('','J2PlateFibre')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	E = mka("E", "Group", "Young's modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	v = mka("v", "Group", "Poisson's ratio", MpcAttributeType.Real)
	sigmaY = mka("sigmaY", "Group", "yield stress", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Hiso = mka("Hiso", "Group", "isotropic hardening modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Hkin = mka("Hkin", "Group", "kinematic hardening modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	use_rho = mka("use_rho", "Optional parameters", "Saturated mass density", MpcAttributeType.Boolean)
	rho = mka("rho", "Optional parameters", "Saturated mass density", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)

	xom = MpcXObjectMetaData()
	xom.name = 'J2PlateFibre'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(E)
	xom.addAttribute(v)
	xom.addAttribute(sigmaY)
	xom.addAttribute(Hiso)
	xom.addAttribute(Hkin)
	
	xom.addAttribute(use_rho)
	xom.addAttribute(rho)
	
	#use_rho-dep
	xom.setVisibilityDependency(use_rho, rho)
	return xom

def writeTcl(pinfo):
	# nDMaterial J2PlateFibre $tag $E $v $sigmaY $Hiso $Hkin <$rho>
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
	
	use_rho_at = xobj.getAttribute('use_rho')
	if(use_rho_at is None):
		raise Exception('Error: cannot find "use_rho" attribute')
	use_rho = use_rho_at.boolean
	if use_rho:
		rho_at = xobj.getAttribute('rho')
		if(rho_at is None):
			raise Exception('Error: cannot find "rho" attribute')
		rho = rho_at.quantityScalar
		
		sopt += ' {}'.format(rho.value)

	# nDMaterial J2PlateFibre $tag $E $v $sigmaY $Hiso $Hkin <$rho>
	str_tcl = '{}nDMaterial J2PlateFibre {} {} {} {} {} {}{}\n'.format(
			pinfo.indent,
			tag,
			geta('E').quantityScalar.value,
			geta('v').real,
			geta('sigmaY').quantityScalar.value,
			geta('Hiso').quantityScalar.value,
			geta('Hkin').quantityScalar.value,
			sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)