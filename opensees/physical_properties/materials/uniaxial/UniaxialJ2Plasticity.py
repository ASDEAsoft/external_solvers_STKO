# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

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
			html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/UniaxialJ2Plasticity_Material','UniaxialJ2Plasticity')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# uniaxialMaterial UniaxialJ2Plasticity $matTag $E $sigmaY $Hkin $Hiso
	E = mka("E", "Group", "Initial tangent stiffness", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	sigmaY = mka("sigmaY", "Group", "Yield stress (or force)", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Hkin = mka("Hkin", "Group", "kinematic hardening Modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Hiso = mka("Hiso", "Group", "Isotropic hardening Modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)

	xom = MpcXObjectMetaData()
	xom.name = 'UniaxialJ2Plasticity'
	xom.Xgroup = 'Other Uniaxial Materials'

	xom.addAttribute(E)
	xom.addAttribute(sigmaY)
	xom.addAttribute(Hkin)
	xom.addAttribute(Hiso)


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

	# uniaxialMaterial UniaxialJ2Plasticity $matTag $E $sigmaY $Hkin $Hiso
	str_tcl = '{}uniaxialMaterial UniaxialJ2Plasticity {} {} {} {} {}\n'.format(
		pinfo.indent,
		tag,
		geta('E').quantityScalar.value,
		geta('sigmaY').quantityScalar.value,
		geta('Hkin').quantityScalar.value,
		geta('Hiso').quantityScalar.value,
		)

	# uniaxialMaterial UniaxialJ2Plasticity $matTag $E $sigmaY $Hkin $Hiso
	pinfo.out_file.write(str_tcl)