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
			html_par(html_href('','PlaneStressSimplifiedJ2')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# nDmaterial PlaneStressSimplifiedJ2 $tag $G $K $sig0 $H_kin $H_iso
	G = mka("G", "Group", "Shear Modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	K = mka("K", "Group", "Bulk modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	sig0 = mka("sig0", "Group", "", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	H_kin = mka("H_kin", "Group", "kinematic hardening Modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	H_iso = mka("H_iso", "Group", "isotropic hardening Modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)


	xom = MpcXObjectMetaData()
	xom.name = 'PlaneStressSimplifiedJ2'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(G)
	xom.addAttribute(K)
	xom.addAttribute(sig0)
	xom.addAttribute(H_kin)
	xom.addAttribute(H_iso)

	return xom

def writeTcl(pinfo):
	# nDmaterial PlaneStressSimplifiedJ2 $tag $G $K $sig0 $H_kin $H_iso
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId

	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	# nDmaterial PlaneStressSimplifiedJ2 $tag $G $K $sig0 $H_kin $H_iso
	str_tcl = '{}nDMaterial PlaneStressSimplifiedJ2 {} {} {} {} {} {}\n'.format(
			pinfo.indent,
			tag,
			geta('G').quantityScalar.value,
			geta('K').real,
			geta('sig0').quantityScalar.value,
			geta('H_kin').quantityScalar.value,
			geta('H_iso').quantityScalar.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)