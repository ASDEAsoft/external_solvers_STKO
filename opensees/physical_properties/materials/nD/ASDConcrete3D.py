# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *
from opensees.utils.override_utils import get_function_from_module

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import math

####################################################################################
# Utilities
####################################################################################

def _geta(xobj, name):
	at = xobj.getAttribute(name)
	if at is None:
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return at

def _bezier3 (xi,   x0, x1, x2,   y0, y1, y2):
	A = x0 - 2.0 * x1 + x2
	B = 2.0 * (x1 - x0)
	C = x0 - xi
	if abs(A) < 1.0e-12:
		x1 = x1 + 1.0E-6 * (x2 - x0)
		A = x0 - 2.0 * x1 + x2
		B = 2.0 * (x1 - x0)
		C = x0 - xi
	if A == 0.0:
		return 0.0
	D = B * B - 4.0 * A * C
	t = (math.sqrt(D) - B) / (2.0 * A)
	return (y0 - 2.0 * y1 + y2) * t * t + 2.0 * (y1 - y0) * t + y0

def _make_hl_concrete_plain(xobj):
	# minimal parameters
	E = _geta(xobj, 'E').quantityScalar.value
	fc = _geta(xobj, 'fcp').quantityScalar.value
	# tensile strength
	ft = fc / 10.0
	# fracture energies
	Gt = 0.073 * (fc**0.18)
	Gc = ((fc/ft)**2) * Gt * 4.0
	# Tensile law
	ft1 = ft * 0.7
	ft2 = ft * 0.1
	ft3 = ft * 1.0e-6
	e0 = ft / E
	e1 = e0 * 1.001
	G1 = ft * e0 / 2.0
	G2 = max(G1 * 1.0e-4, Gt-G1)
	G21 = 0.8 * G2
	G22 = G2 - G21
	e2 = e0 + G21 / (ft2 + (ft1-ft2)/2.0)
	e3 = e2 + 2.0*G22/ft2
	Te = [0.0,  e0,   e1,  e2,  e3, e3*1.1]
	Ts = [0.0,  ft,  ft1, ft2, ft3,    ft3]
	Td = [0.0, 0.0,  1.0, 1.0, 0.9,    0.9]
	# Compressive Law
	damage_c_end = 0.9
	damage_c_peak = 0.3
	ec = 2.0*fc/E
	fc0 = fc/2.0
	ec0 = fc0/E
	ec1 = fc/E
	fcr = fc/10.0
	ec_pl = max(0.0, ec - fc/((1.0 - damage_c_peak)*E))
	Gc1 = fc*(ec-ec_pl)/2.0
	Gc2 = max(Gc1*1.0e-2, Gc-Gc1)
	decr = Gc2*2.0/fc
	decu = (fc-fcr)/fc*decr
	ecr = ec + decr - decu
	Cs = [0.0, fc0]
	Ce = [0.0, ec0]
	Cd = [0.0, 0.0]
	nc = 5
	dec = (ec-ec0)/(nc-1)
	for i in range(nc-1):
		iec = ec0+(i+1.0)*dec
		Ce.append(iec)
		Cs.append(_bezier3(iec,  ec0, ec1, ec,  fc0, fc, fc))
		ratio = (i+1.0)/(nc-1.0)
		Cd.append((1.0-ratio) + damage_c_peak*(ratio))
	Ce.append(ecr)
	Ce.append(ecr+ec0)
	Cs.append(fcr)
	Cs.append(fcr)
	Cd.append(damage_c_end)
	Cd.append(damage_c_end)
	return (Te, Ts, Td, Ce, Cs, Cd)

def _make_hl_user(xobj):
	return (
		_geta(xobj, 'Te').quantityVector.value,
		_geta(xobj, 'Ts').quantityVector.value,
		_geta(xobj, 'Td').quantityVector.value,
		_geta(xobj, 'Ce').quantityVector.value,
		_geta(xobj, 'Cs').quantityVector.value,
		_geta(xobj, 'Cd').quantityVector.value)

class _globals:
	hl_t_targets = ('Te','Ts','Td')
	hl_c_targets = ('Ce','Cs','Cd')
	presets = {
		"Concrete (Plain)" : _make_hl_concrete_plain,
		"User-Defined" : _make_hl_user,
		}

####################################################################################
# CHECKS for user-interaction
####################################################################################

def _check_implex(xobj):
	is_implex = xobj.getAttribute('integration').string == 'IMPL-EX'
	xobj.getAttribute('implexCheckError').visible = is_implex
	do_check = xobj.getAttribute('implexCheckError').boolean
	xobj.getAttribute('implexErrorTolerance').visible = is_implex and do_check
	xobj.getAttribute('implexErrorTimeReductionLimit').visible = is_implex and do_check

def _check_cplanes(xobj):
	cplanes = xobj.getAttribute('-crackPlanes').boolean
	xobj.getAttribute('nct').visible = cplanes
	xobj.getAttribute('ncc').visible = cplanes
	xobj.getAttribute('smoothingAngle').visible = cplanes

def _check_presets(xobj):
	ptype = xobj.getAttribute('Preset').string
	is_user = ptype == list(_globals.presets.keys())[-1]
	for i in _globals.hl_t_targets:
		xobj.getAttribute(i).visible = is_user
	for i in _globals.hl_c_targets:
		xobj.getAttribute(i).visible = is_user
	xobj.getAttribute('fcp').visible = not is_user

def _check_hl_consistency(xobj, at, targets):
	if at is None:
		at = xobj.getAttribute(targets[0])
		for i in range(1, len(targets)):
			iat = xobj.getAttribute(targets[i])
			if len(iat.quantityVector.referenceValue) > len(at.quantityVector.referenceValue):
				at = iat
	n = len(at.quantityVector.referenceValue)
	for i in targets:
		iat = xobj.getAttribute(i)
		ival = iat.quantityVector.referenceValue
		if len(ival) != n:
			new_ival = Math.vec(n)
			nmin = min(n, len(ival))
			for j in range(nmin):
				new_ival[j] = ival[j]
			iat.quantityVector.referenceValue = new_ival

def _check_tensile_hl_consistency(xobj, at):
	_check_hl_consistency(xobj, at, _globals.hl_t_targets)

def _check_compressive_hl_consistency(xobj, at):
	_check_hl_consistency(xobj, at, _globals.hl_c_targets)

_onEditBegin = get_function_from_module(__name__, 'onEditBegin')
def onEditBegin(editor, xobj):
	if _onEditBegin: _onEditBegin(editor, xobj)
	_check_implex(xobj)
	_check_cplanes(xobj)
	_check_tensile_hl_consistency(xobj, None)
	_check_compressive_hl_consistency(xobj, None)
	_check_presets(xobj)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name == 'integration' or attribute_name == 'implexCheckError':
		_check_implex(xobj)
	elif attribute_name == '-crackPlanes':
		_check_cplanes(xobj)
	elif attribute_name in _globals.hl_t_targets:
		_check_tensile_hl_consistency(xobj, xobj.getAttribute(attribute_name))
	elif attribute_name in _globals.hl_c_targets:
		_check_compressive_hl_consistency(xobj, xobj.getAttribute(attribute_name))
	elif attribute_name == 'Preset':
		_check_presets(xobj)

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
			html_par(html_href('https://asdeasoft.net/?stko-support','DamageTC3D')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	# mass
	rho = mka("rho", "Mass", "Density", MpcAttributeType.QuantityScalar, adim=((u.F/(u.L/u.t**2))/u.L**3))
	# elasticity
	E = mka("E", "Elasticity", "Young's modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	v = mka("v", "Elasticity", "Poisson's ratio", MpcAttributeType.Real)
	# viscosity
	eta  = mka("eta", "Misc", "Viscosity parameter", MpcAttributeType.Real, dval=0.0)
	# implex
	algo = mka("integration", "Integration", ("Integration type.<br/>"
		"(Default) Implicit: A standard Backward-Euler integration scheme.<br/>"
		"IMPL-EX: A mixed IMPLicit-EXplicit integration scheme. The resulting response is "
		"step-wise linear with a positive-definite tangent stiffnes matrix due to the explicit extrapolation of the internal variables.<br/>"
		"However the time-step should be smaller than the one used for an implicit scheme"), 
		MpcAttributeType.String, dval="Implicit")
	algo.sourceType = MpcAttributeSourceType.List
	algo.setSourceList(['Implicit', 'IMPL-EX'])
	implex_check = mka("implexCheckError", "Integration", "Check the IMPL-EX error making sure it is kept under a user-defined tolerance", MpcAttributeType.Boolean, dval=False)
	implex_tol = mka("implexErrorTolerance", "Integration", "The maximum allowed relative IMPL-EX error", MpcAttributeType.Real, dval=0.05)
	implex_red = mka("implexErrorTimeReductionLimit", "Integration", "The pseudo-time-step reduction limit under which the implex error check is not performed", MpcAttributeType.Real, dval=0.01)
	# misc
	reg = mka("autoRegularization", "Misc", ("When this flag is True (Default), the input fracture energies (Gt and Gc) "
		"will be divided by the element characteristic length, in order to obtain a response which is mesh-size independent.<br/>"
		"If turn this flag Off, the input fracture energies will be used as they are."), 
		MpcAttributeType.Boolean, dval=True)
	ctype = mka("constitutiveTensorType", "Misc", ("Constitutive Tensor Tyope.<br/>"
		"Tangent: The algorithmic tangent tensor.<br/>"
		"(Default) Secant: The secant tensor.<br/>"), 
		MpcAttributeType.String, dval="Secant")
	ctype.sourceType = MpcAttributeSourceType.List
	ctype.setSourceList(['Tangent', 'Secant'])
	# crack planes
	cplanes = mka("-crackPlanes", "Crack Planes", "Activates the anisotropy of internal variables on multiple crack-planes", MpcAttributeType.Boolean, dval=False)
	cplanes_nct = mka("nct", "Crack Planes", "Number of crack planes for the tensile behavior", MpcAttributeType.Integer, dval=4)
	cplanes_ncc = mka("ncc", "Crack Planes", "Number of crack planes for the compressive behavior", MpcAttributeType.Integer, dval=4)
	cplanes_angle = mka("smoothingAngle", "Crack Planes", "Smoothing angle (in degress) for smoothing the internal variables", MpcAttributeType.Real, dval=90.0)
	
	# hardening laws - manual (by points) ...
	Te = mka("Te", "Tension", "Tensile Hardening Law (Strain)", MpcAttributeType.QuantityVector)
	Ts = mka("Ts", "Tension", "Tensile Hardening Law (Stress)", MpcAttributeType.QuantityVector)
	Td = mka("Td", "Tension", "Tensile Hardening Law (Damage)", MpcAttributeType.QuantityVector)
	Ce = mka("Ce", "Compression", "Compressive Hardening Law (Strain)", MpcAttributeType.QuantityVector)
	Cs = mka("Cs", "Compression", "Compressive Hardening Law (Stress)", MpcAttributeType.QuantityVector)
	Cd = mka("Cd", "Compression", "Compressive Hardening Law (Damage)", MpcAttributeType.QuantityVector)
	
	# ... or by minimal parameters
	fcp = mka("fcp", "Preset", "Peak Compressive Strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	
	# input type
	all_presets = list(_globals.presets.keys())
	itype = mka("Preset", "Preset", ("Choose one of the built-in presets with minimal input parameters, "
		"or define manually the hardening laws"),
		MpcAttributeType.String, dval=all_presets[0])
	itype.sourceType = MpcAttributeSourceType.List
	itype.setSourceList(all_presets)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDConcrete3D'
	xom.Xgroup = 'ASDEASoftware'
	
	# Mass
	xom.addAttribute(rho)
	# Elasticity
	xom.addAttribute(E)
	xom.addAttribute(v)
	# Preset
	xom.addAttribute(itype)
	xom.addAttribute(fcp)
	# Tension
	xom.addAttribute(Te)
	xom.addAttribute(Ts)
	xom.addAttribute(Td)
	# Compression
	xom.addAttribute(Ce)
	xom.addAttribute(Cs)
	xom.addAttribute(Cd)
	# Integration
	xom.addAttribute(algo)
	xom.addAttribute(implex_check)
	xom.addAttribute(implex_tol)
	xom.addAttribute(implex_red)
	# crack planes
	xom.addAttribute(cplanes)
	xom.addAttribute(cplanes_nct)
	xom.addAttribute(cplanes_ncc)
	xom.addAttribute(cplanes_angle)
	# misc
	xom.addAttribute(eta)
	xom.addAttribute(reg)
	xom.addAttribute(ctype)
	
	return xom

def writeTcl(pinfo):
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# get basic parameters
	E = _geta(xobj, 'E').quantityScalar.value
	v = _geta(xobj, 'v').real
	rho = _geta(xobj, 'rho').quantityScalar.value
	eta = _geta(xobj, 'eta').real
	
	# obtain the hardening points
	Te,Ts,Td,Ce,Cs,Cd = _globals.presets[_geta(xobj, 'Preset').string](xobj)
	def to_tcl(x):
		return ' '.join(str(i) for i in x)
	
	# command format
	command = ("{0}nDMaterial ASDConcrete3D {1} {2} {3} \\\n"
		"{0}\t-Te {6} \\\n"
		"{0}\t-Ts {7} \\\n"
		"{0}\t-Td {8} \\\n"
		"{0}\t-Ce {9} \\\n"
		"{0}\t-Cs {10} \\\n"
		"{0}\t-Cd {11} \\\n"
		"{0}\t-rho {4} -eta {5}").format(pinfo.indent, tag, E, v, rho, eta, 
			to_tcl(Te), to_tcl(Ts), to_tcl(Td), to_tcl(Ce), to_tcl(Cs), to_tcl(Cd))
	
	if _geta(xobj, 'integration').string == 'IMPL-EX':
		if _geta(xobj, 'implexCheckError').boolean:
			command += ' \\\n{}\t-implex -implexControl {} {}'.format(
				pinfo.indent,
				_geta(xobj, 'implexErrorTolerance').real,
				_geta(xobj, 'implexErrorTimeReductionLimit').real)
		else:
			command += ' \\\n{}\t-implex'.format(pinfo.indent)
	
	if _geta(xobj, '-crackPlanes').boolean:
		command += ' \\\n{}\t-crackPlanes {} {} {}'.format(pinfo.indent, 
			_geta(xobj, 'nct').integer,
			_geta(xobj, 'ncc').integer,
			_geta(xobj, 'smoothingAngle').real)
	
	if _geta(xobj, 'constitutiveTensorType').string == 'Tangent':
		command += ' \\\n{}\t-tangent'.format(pinfo.indent)
	
	if _geta(xobj, 'autoRegularization').boolean:
		command += ' \\\n{}\t-autoRegularization'.format(pinfo.indent)
	
	command += '\n'
	
	print(command)

	#"{0}\t<-implex> <-implexControl $implexErrorTolerance $implexTimeReductionLimit> \\\n"
	#"{0}\t<-crackPlanes $nct $ncc $smoothingAngle> \\\n"
	#"{0}\t <-tangent> <-autoRegularization>\n"
	
	
	# now write the string into the file
	pinfo.out_file.write(command)
