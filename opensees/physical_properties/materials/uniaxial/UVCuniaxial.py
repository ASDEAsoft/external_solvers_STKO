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
			html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/UVCuniaxial_(Updated_Voce-Chaboche)','UVCuniaxial')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# uniaxialMaterial UVCuniaxial tag? E? fy? QInf? b? DInf? a? N? C1? gamma1? <C2? gamma2? C3? gamma3? ... C8? gamma8?>
	E = mka("E", "Group", "Elastic modulus of the steel material", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	fy = mka("fy", "Group", "Initial yield stress of the steel material", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	QInf = mka("QInf", "Group", "Maximum increase in yield stress due to cyclic hardening (isotropic hardening)", MpcAttributeType.Real)
	b = mka("b", "Group", "Saturation rate of QInf, b > 0", MpcAttributeType.Real)
	DInf = mka("DInf", "Group", "Decrease in the initial yield stress, to neglect the model updates set DInf = 0", MpcAttributeType.Real)
	a = mka("a", "Group", "Saturation rate of DInf, a > 0. If DInf == 0, then a is arbitrary (but still a > 0)", MpcAttributeType.Real)

	C = mka("C", "Group", "Kinematic hardening parameter associated with backstress component (min 1 max 8)", MpcAttributeType.QuantityVector)
	gamma = mka("gamma", "Group", "Saturation rate of kinematic hardening associated with backstress component (min 1 max 8)", MpcAttributeType.QuantityVector)

	xom = MpcXObjectMetaData()
	xom.name = 'UVCuniaxial'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'

	xom.addAttribute(E)
	xom.addAttribute(fy)
	xom.addAttribute(QInf)
	xom.addAttribute(b)
	xom.addAttribute(DInf)
	xom.addAttribute(a)

	xom.addAttribute(C)
	xom.addAttribute(gamma)

	return xom

def writeTcl(pinfo):
	
	# uniaxialMaterial UVCuniaxial tag? E? fy? QInf? b? DInf? a? N? C1? gamma1? <C2? gamma2? C3? gamma3? ... C8? gamma8?>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId

	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	C = geta('C').quantityVector
	gamma = geta('gamma').quantityVector
	if len(C) != len(gamma):
		raise Exception('Error: (C vector) Kinematic hardening parameter associated with backstress component and '
		'(gamma vector) Saturation rate of kinematic hardening associated with backstress component vectors must have the same length')

	N = len(C)
	if N < 1:
		raise Exception('Error: (C vector) Kinematic hardening parameter associated with backstress component and '
		'(gamma vector) Saturation rate of kinematic hardening associated with backstress component vectors must have at least one argument')

	if N > 8:
		raise Exception('Error: (C vector) Kinematic hardening parameter associated with backstress component and '
		'(gamma vector) Saturation rate of kinematic hardening associated with backstress component vectors must have at max 8 argument')
	sopt = ''
	for i in range(N):
		sopt += ' {} {}'.format(C.valueAt(i), gamma.valueAt(i))

	# uniaxialMaterial UVCuniaxial tag? E? fy? QInf? b? DInf? a? N? C1? gamma1? <C2? gamma2? C3? gamma3? ... C8? gamma8?>
	str_tcl = '{}uniaxialMaterial UVCuniaxial {} {} {} {} {} {} {} {}{}\n'.format(
		pinfo.indent,
		tag,
		geta('E').quantityScalar.value,
		geta('fy').quantityScalar.value,
		geta('QInf').real,
		geta('b').real,
		geta('DInf').real,
		geta('a').real,
		N,
		sopt
		)

	pinfo.out_file.write(str_tcl)