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
			html_par(html_href('https://opensees.berkeley.edu/OpenSees/manuals/usermanual/2426.htm','Steel03')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# uniaxialMaterial Steel03 $matTag $Fy $E $b $R0 $cR1 $cR2 $a1 $a2 $a3 $a4
	Fy = mka("Fy", "Group", "yield strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	E = mka("E", "Group", "", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	b = mka("b", "Group", "Strain-hardening ratio (ratio between post-yield tangent and initial elastic tangent)", MpcAttributeType.Real)
	R0 = mka("R0", "Group", "Initial elastic tangent", MpcAttributeType.Real)
	cR1 = mka("cR1", "Group", "Initial elastic tangent", MpcAttributeType.Real)
	cR2 = mka("cR2", "Group", "Initial elastic tangent", MpcAttributeType.Real)

	Optional = mka("Optional", "Optional parameters", "", MpcAttributeType.Boolean)
	a1 = mka("a1", "Optional parameters", "Isotropic hardening parameter, increase of compression yield envelope as proportion of yield strength after a plastic strain of a2*(Fy/E0).", MpcAttributeType.Real)
	a1.setDefault(0.0)
	a2 = mka("a2", "Optional parameters", "Isotropic hardening parameter (see explanation under a1). (optional default = 1.0).", MpcAttributeType.Real)
	a2.setDefault(1.0)
	a3 = mka("a3", "Optional parameters", "Isotropic hardening parameter, increase of tension yield envelope as proportion of yield strength after a plastic strain of a4*(Fy/E0).", MpcAttributeType.Real)
	a3.setDefault(0.0)
	a4 = mka("a4", "Optional parameters", "Isotropic hardening parameter (see explanation under a3). (optional default = 1.0)", MpcAttributeType.Real)
	a4.setDefault(1.0)

	xom = MpcXObjectMetaData()
	xom.name = 'Steel03'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(Fy)
	xom.addAttribute(E)
	xom.addAttribute(b)
	xom.addAttribute(R0)
	xom.addAttribute(cR1)
	xom.addAttribute(cR2)

	# use_Optional-dep
	xom.addAttribute(Optional)
	xom.addAttribute(a1)
	xom.addAttribute(a2)
	xom.addAttribute(a3)
	xom.addAttribute(a4)

	# use_Optional-dep
	xom.setVisibilityDependency(Optional, a1)
	xom.setVisibilityDependency(Optional, a2)
	xom.setVisibilityDependency(Optional, a3)
	xom.setVisibilityDependency(Optional, a4)

	return xom

def writeTcl(pinfo):
	# uniaxialMaterial Steel03 $matTag $Fy $E $b $R0 $cR1 $cR2 $a1 $a2 $a3 $a4
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	# uniaxialMaterial Steel03 $matTag $Fy $E $b $R0 $cR1 $cR2 $a1 $a2 $a3 $a4
	# optional paramters
	sopt = ''
	if geta('Optional').boolean:
		sopt += ' {} {} {} {}'.format(geta('a1').real,
		geta('a2').real,
		geta('a3').real,
		geta('a4').real)

	str_tcl = '{}uniaxialMaterial Steel03 {} {} {} {} {} {} {}{}\n'.format(
			pinfo.indent,
			tag,
			geta('Fy').quantityScalar.value,
			geta('E').quantityScalar.value,
			geta('b').real,
			geta('R0').real,
			geta('cR1').real,
			geta('cR2').real,
			sopt
			)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)