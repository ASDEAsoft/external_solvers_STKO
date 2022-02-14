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
			html_par(html_href('','DoddRestr')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# uniaxialMaterial DoddRestr $tag Eo? fy? esh? esh1? fsh1? esu? fsu? Pmajor? Pminor? <slcf? tlcf? Dcrit?>
	Eo = mka("Eo", "Group", "", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	fy = mka("fy", "Non-linear", "Yield strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	esh = mka("esh", "Non-linear", "Tensile strain at initiation of strain hardening", MpcAttributeType.Real)
	esh1 = mka("esh1", "Non-linear", "Tensile strain at initiation of strain hardening", MpcAttributeType.Real)
	fsh1 = mka("fsh1", "Non-linear", "ensile stress at point on strain hardening curve corresponding to ESHI", MpcAttributeType.Real)
	esu = mka("esu", "Non-linear", "Tensile strain at the UTS", MpcAttributeType.Real)
	fsu = mka("fsu", "Non-linear", "Ultimate tensile strength (UTS)", MpcAttributeType.Real)
	Pmajor = mka("Pmajor", "Non-linear", "", MpcAttributeType.Real)
	Pminor = mka("Pminor", "Non-linear", "", MpcAttributeType.Real)
	# Optional parameters
	Optional = mka("Optional", "Optional parameters", "", MpcAttributeType.Boolean)
	slcf = mka("slcf", "Non-linear", "", MpcAttributeType.Real)
	tlcf = mka("tlcf", "Non-linear", "", MpcAttributeType.Real)
	Dcrit = mka("Dcrit", "Non-linear", "", MpcAttributeType.Real)

	xom = MpcXObjectMetaData()
	xom.name = 'DoddRestr'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(Eo)
	xom.addAttribute(fy)
	xom.addAttribute(esh)
	xom.addAttribute(esh1)
	xom.addAttribute(fsh1)
	xom.addAttribute(esu)
	xom.addAttribute(fsu)
	xom.addAttribute(Pmajor)
	xom.addAttribute(Pminor)
	# Optional parameters
	xom.addAttribute(Optional)
	xom.addAttribute(slcf)
	xom.addAttribute(tlcf)
	xom.addAttribute(Dcrit)
	
	# use_rho-dep
	xom.setVisibilityDependency(Optional, slcf)
	xom.setVisibilityDependency(Optional, tlcf)
	xom.setVisibilityDependency(Optional, Dcrit)

	return xom

def writeTcl(pinfo):
	# uniaxialMaterial DoddRestr  Eo? fy? esh? esh1? fsh1? esu? fsu? Pmajor? Pminor? <slcf? tlcf? Dcrit?>
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
		sopt += ' {} {} {}'.format(geta('slcf').real,
		geta('tlcf').real,
		geta('Dcrit').real)

	# uniaxialMaterial DoddRestr  Eo? fy? esh? esh1? fsh1? esu? fsu? Pmajor? Pminor? <slcf? tlcf? Dcrit?>
	str_tcl = '{}uniaxialMaterial DoddRestr {} {} {} {} {} {} {} {} {} {}{}\n'.format(
		pinfo.indent,
		tag,
		geta('Eo').quantityScalar.value,
		geta('fy').quantityScalar.value,
		geta('esh').real,
		geta('esh1').real,
		geta('fsh1').real,
		geta('esu').real,
		geta('fsu').real,
		geta('Pmajor').real,
		geta('Pminor').real,
		sopt
		)

	# now write the string into the file
	pinfo.out_file.write(str_tcl)
	# uniaxialMaterial DoddRestr  Eo? fy? esh? esh1? fsh1? esu? fsu? Pmajor? Pminor? <slcf? tlcf? Dcrit?>