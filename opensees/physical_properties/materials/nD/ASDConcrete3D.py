# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *
from opensees.utils.override_utils import get_function_from_module

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import math

# NOTE 1: Don't use implexCheckError... 
# it seems there is a problem in OpenSeesMP when a material fails in computation

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

def _get_lch_ref(E,ft,Gt,fc,ec,Gc):
	'''
	the characteristic length for built-in specific fracture energy
	'''
	
	# min lch for tension
	et_el = ft/E # no damage at peak
	Gt_min = ft*et_el/2.0
	hmin_t = Gt/Gt_min/100.0
	
	# min lch for compression
	ec1 = fc/E
	ec_pl = (ec-ec1)*0.4 + ec1
	Gc_min = fc*(ec-ec_pl)/2.0
	hmin_c = Gc/Gc_min/100.0
	
	# return the minimum
	return min(hmin_t, hmin_c)

def _make_tension_bilin(E, ft, Gt, pscale):
	'''
	a trilinear hardening-softening law for tensile response
	'''
	f0 = ft*0.9
	f1 = ft
	e0 = f0/E
	e1 = ft/E*1.5
	ep = e1-ft/E
	f2 = 0.2*ft
	f3 = 1.0e-3*ft
	w2 = Gt/ft
	w3 = w2/0.2
	e2 = w2 + f2/E + ep
	if e2 <= e1: e2 = e1*1.001
	e3 = w3 + f3/E + ep
	if e3 <= e2: e3 = e2*1.001
	e4 = e3*10.0
	Te = [0.0,  e0,  e1,  e2,  e3,  e4] # total strain points
	Ts = [0.0,  f0,  f1,  f2,  f3,  f3] # nominal stress points
	Td = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # initialize damage list
	Tpl = [0.0, 0.0, ep, e2*0.9, e3*0.8, e3*0.8] # desired values of equivalent plastic strains
	# scale plasticity
	if pscale >= 0.0 and pscale < 1.0:
		for i in range(len(Tpl)):
			Tpl[i] = Tpl[i]*pscale
	for i in range(2, len(Te)):
		xi = Te[i]
		si = Ts[i]
		xipl = Tpl[i]
		xipl_max = xi-si/E
		xipl = min(xipl, xipl_max)
		qi = (xi-xipl)*E
		Td[i] = 1.0-si/qi # compute damage
	return (Te, Ts, Td)

def _make_compression(E, fc, fc0, fcr, ec, Gc, pscale):
	'''
	a quadratic hardening followed by linear softening for compressive response
	'''
	ec0 = fc0/E
	ec1 = fc/E
	ec_pl = (ec-ec1)*0.4 + ec1
	Gc1 = fc*(ec-ec_pl)/2.0
	Gc2 = max(Gc1*1.0e-2, Gc-Gc1)
	ecr = ec + 2.0*Gc2/(fc+fcr)
	Ce = [0.0, ec0] # total strain points
	Cs = [0.0, fc0] # nominal stress points
	Cpl = [0.0, 0.0] # desired values of equivalent plastic strains
	nc = 10
	dec = (ec-ec0)/(nc-1)
	for i in range(nc-1):
		iec = ec0+(i+1.0)*dec
		Ce.append(iec)
		Cs.append(_bezier3(iec,  ec0, ec1, ec,  fc0, fc, fc))
		Cpl.append(Cpl[-1]+(iec-Cpl[-1])*0.7)
	# end of linear softening - begin residual plateau
	Ce.append(ecr)
	Cs.append(fcr)
	Cpl.append(Cpl[-1] + (ecr-Cpl[-1])*0.7)
	# extend to make a plateau
	Ce.append(ecr+ec0)
	Cs.append(fcr)
	Cpl.append(Cpl[-1])
	# scale plasticity
	if pscale >= 0.0 and pscale < 1.0:
		for i in range(len(Cpl)):
			Cpl[i] = Cpl[i]*pscale
	# compute damage now
	Cd = [0.0]*len(Ce)
	for i in range(2, len(Ce)):
		xi = Ce[i]
		si = Cs[i]
		xipl = Cpl[i]
		xipl_max = xi-si/E
		xipl = min(xipl, xipl_max)
		qi = (xi-xipl)*E
		Cd[i] = 1.0-si/qi # compute damage
	# Done
	return (Ce, Cs, Cd)

def _make_hl_concrete_base(xobj, E, ft, fc, fc0, fcr, ec, Gt, Gc, auto_reg, lch_ref, pscalet, pscalec):
	# Tensile law
	Te, Ts, Td = _make_tension_bilin(E, ft, Gt, pscalet)
	# Compressive Law
	Ce, Cs, Cd = _make_compression(E, fc, fc0, fcr, ec, Gc, pscalec)
	# Done
	return (Te, Ts, Td, Ce, Cs, Cd, auto_reg, lch_ref)

def _make_hl_concrete_1p(xobj):
	# minimal parameters
	E = _geta(xobj, 'E').quantityScalar.value
	fc = _geta(xobj, 'fcp').quantityScalar.value
	# bring input in MPa
	L = _globals.L_units[_geta(xobj, 'L. unit').string]
	F = _globals.F_units[_geta(xobj, 'F. unit').string]
	# other compressive parameters
	fc0 = fc/2.0
	fcr = fc/10.0
	ec = 2.0*fc/E
	# tensile strength
	ft = fc / 10.0
	# fracture energies
	Gt = (0.073 * ((fc*F/L/L)**0.18))*L/F # make fc in MPa, then bring it back to user-unit (1/stiffness)
	Gc = 250.0*Gt
	# characteristic length
	auto_reg = True
	lch_ref = _get_lch_ref(E,ft,Gt,fc,ec,Gc)
	gt = Gt/lch_ref
	gc = Gc/lch_ref
	# base concrete
	return _make_hl_concrete_base(xobj, E, ft, fc, fc0, fcr, ec, gt, gc, auto_reg, lch_ref, 1.0, 1.0)
def _make_hl_concrete_4p(xobj):
	# minimal parameters
	E = _geta(xobj, 'E').quantityScalar.value
	fc = _geta(xobj, 'fcp').quantityScalar.value
	# other compressive parameters
	fc0 = fc/2.0
	fcr = fc/10.0
	ec = 2.0*fc/E
	# tensile strength
	ft = _geta(xobj, 'ft').quantityScalar.value
	# fracture energies
	Gt = _geta(xobj, 'Gt').quantityScalar.value
	Gc = _geta(xobj, 'Gc').quantityScalar.value
	# characteristic length
	auto_reg = True
	lch_ref = _get_lch_ref(E,ft,Gt,fc,ec,Gc)
	gt = Gt/lch_ref
	gc = Gc/lch_ref
	# base concrete
	return _make_hl_concrete_base(xobj, E, ft, fc, fc0, fcr, ec, gt, gc, auto_reg, lch_ref, 1.0, 1.0)
def _make_hl_concrete_6p(xobj):
	# minimal parameters
	E = _geta(xobj, 'E').quantityScalar.value
	fc = _geta(xobj, 'fcp').quantityScalar.value
	# other compressive parameters
	fc0 = fc/2.0
	fcr = fc/10.0
	ec = 2.0*fc/E
	# tensile strength
	ft = _geta(xobj, 'ft').quantityScalar.value
	# fracture energies
	Gt = _geta(xobj, 'Gt').quantityScalar.value
	Gc = _geta(xobj, 'Gc').quantityScalar.value
	# characteristic length
	auto_reg = True
	lch_ref = _get_lch_ref(E,ft,Gt,fc,ec,Gc)
	gt = Gt/lch_ref
	gc = Gc/lch_ref
	# pscale factors
	pscalet = _geta(xobj, 'PScale Tension').real
	pscalec = _geta(xobj, 'PScale Compression').real
	# base concrete
	return _make_hl_concrete_base(xobj, E, ft, fc, fc0, fcr, ec, gt, gc, auto_reg, lch_ref, pscalet, pscalec)
def _make_hl_concrete_9p(xobj):
	# minimal parameters
	E = _geta(xobj, 'E').quantityScalar.value
	fc = _geta(xobj, 'fcp').quantityScalar.value
	# other compressive parameters
	fc0 = _geta(xobj, 'fc0').quantityScalar.value
	fcr = _geta(xobj, 'fcr').quantityScalar.value
	ec = _geta(xobj, 'ecp').real
	# tensile strength
	ft = _geta(xobj, 'ft').quantityScalar.value
	# fracture energies
	Gt = _geta(xobj, 'Gt').quantityScalar.value
	Gc = _geta(xobj, 'Gc').quantityScalar.value
	# characteristic length
	auto_reg = True
	lch_ref = _get_lch_ref(E,ft,Gt,fc,ec,Gc)
	gt = Gt/lch_ref
	gc = Gc/lch_ref
	# pscale factors
	pscalet = _geta(xobj, 'PScale Tension').real
	pscalec = _geta(xobj, 'PScale Compression').real
	# base concrete
	return _make_hl_concrete_base(xobj, E, ft, fc, fc0, fcr, ec, gt, gc, auto_reg, lch_ref, pscalet, pscalec)
def _make_hl_user(xobj):
	return (
		_geta(xobj, 'Te').quantityVector.value,
		_geta(xobj, 'Ts').quantityVector.value,
		_geta(xobj, 'Td').quantityVector.value,
		_geta(xobj, 'Ce').quantityVector.value,
		_geta(xobj, 'Cs').quantityVector.value,
		_geta(xobj, 'Cd').quantityVector.value,
		_geta(xobj, 'autoRegularization').boolean,
		_geta(xobj, 'LchRef').quantityScalar.value)

def _check_hl_concrete_1p(xobj):
	for i in _globals.hl_t_targets:
		xobj.getAttribute(i).visible = False
	for i in _globals.hl_c_targets:
		xobj.getAttribute(i).visible = False
	xobj.getAttribute('ft').visible = False
	xobj.getAttribute('fc0').visible = False
	xobj.getAttribute('fcp').visible = True
	xobj.getAttribute('fcr').visible = False
	xobj.getAttribute('ecp').visible = False
	xobj.getAttribute('Gt').visible = False
	xobj.getAttribute('Gc').visible = False
	xobj.getAttribute('L. unit').visible = True
	xobj.getAttribute('F. unit').visible = True
	xobj.getAttribute('autoRegularization').visible = False
	xobj.getAttribute('LchRef').visible = False
	xobj.getAttribute('PScale Tension').visible = False
	xobj.getAttribute('PScale Compression').visible = False
def _check_hl_concrete_4p(xobj):
	_check_hl_concrete_1p(xobj)
	xobj.getAttribute('ft').visible = True
	xobj.getAttribute('Gt').visible = True
	xobj.getAttribute('Gc').visible = True
	xobj.getAttribute('L. unit').visible = False
	xobj.getAttribute('F. unit').visible = False
def _check_hl_concrete_6p(xobj):
	_check_hl_concrete_4p(xobj)
	xobj.getAttribute('PScale Tension').visible = True
	xobj.getAttribute('PScale Compression').visible = True
def _check_hl_concrete_9p(xobj):
	_check_hl_concrete_6p(xobj)
	xobj.getAttribute('fc0').visible = True
	xobj.getAttribute('fcr').visible = True
	xobj.getAttribute('ecp').visible = True
def _check_hl_user(xobj):
	for i in _globals.hl_t_targets:
		xobj.getAttribute(i).visible = True
	for i in _globals.hl_c_targets:
		xobj.getAttribute(i).visible = True
	xobj.getAttribute('ft').visible = False
	xobj.getAttribute('fc0').visible = False
	xobj.getAttribute('fcp').visible = False
	xobj.getAttribute('fcr').visible = False
	xobj.getAttribute('ecp').visible = False
	xobj.getAttribute('Gt').visible = False
	xobj.getAttribute('Gc').visible = False
	xobj.getAttribute('L. unit').visible = False
	xobj.getAttribute('F. unit').visible = False
	xobj.getAttribute('autoRegularization').visible = True
	xobj.getAttribute('LchRef').visible = True
	xobj.getAttribute('PScale Tension').visible = False
	xobj.getAttribute('PScale Compression').visible = False

class _globals:
	hl_t_targets = ('Te','Ts','Td')
	hl_c_targets = ('Ce','Cs','Cd')
	presets = {
		"Concrete (1P)" : (_make_hl_concrete_1p, _check_hl_concrete_1p),
		"Concrete (4P)" : (_make_hl_concrete_4p, _check_hl_concrete_4p),
		"Concrete (6P)" : (_make_hl_concrete_6p, _check_hl_concrete_6p),
		"Concrete (9P)" : (_make_hl_concrete_9p, _check_hl_concrete_9p),
		"User-Defined"  : (_make_hl_user, _check_hl_user),
		}
	L_units = {
		'mm' : 1.0,
		'cm' : 10.0,
		'dm' : 100.0,
		'm'  : 1000.0,
		'in' : 25.4,
		'ft' : 304.8,
		}
	F_units = {
		'N': 1.0,
		'daN': 10.0,
		'kN' : 1000.0,
		'lbf' : 4.4482216152605,
		'kip' : 4448.2216152605,
		}

####################################################################################
# CHECKS for user-interaction
####################################################################################

def _check_implex(xobj):
	is_implex = xobj.getAttribute('integration').string == 'IMPL-EX'
	xobj.getAttribute('implexAlpha').visible = is_implex
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
	check_fun = _globals.presets[ptype][1]
	check_fun(xobj)

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
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/material/ndMaterials/ASDConcrete3D.html','ASDConcrete3D')+'<br/>') +
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
	# Kc 
	Kc = mka("Kc", "Misc", ("Triaxial-Compression shape factor.<br/>"
		"It must be in the range [2/3, 1].<br/>"
		"The lower the value, the stronger is the material under increasing confinement"), MpcAttributeType.Real, dval=2.0/3.0)
	# implex
	algo = mka("integration", "Integration", ("Integration type.<br/>"
		"(Default) Implicit: A standard Backward-Euler integration scheme.<br/>"
		"IMPL-EX: A mixed IMPLicit-EXplicit integration scheme. The resulting response is "
		"step-wise linear with a positive-definite tangent stiffnes matrix due to the explicit extrapolation of the internal variables.<br/>"
		"However the time-step should be smaller than the one used for an implicit scheme"), 
		MpcAttributeType.String, dval="Implicit")
	algo.sourceType = MpcAttributeSourceType.List
	algo.setSourceList(['Implicit', 'IMPL-EX'])
	implex_alpha = mka("implexAlpha", "Integration", "The scale factor for IMPL-EX extrapolation in the range (0, 1). Use 0 if you experience instabilities due to the explicit extrapolation", MpcAttributeType.Real, dval=1.0)
	implex_check = mka("implexCheckError", "Integration", "Check the IMPL-EX error making sure it is kept under a user-defined tolerance", MpcAttributeType.Boolean, dval=False)
	implex_tol = mka("implexErrorTolerance", "Integration", "The maximum allowed relative IMPL-EX error", MpcAttributeType.Real, dval=0.05)
	implex_red = mka("implexErrorTimeReductionLimit", "Integration", "The pseudo-time-step reduction limit under which the implex error check is not performed", MpcAttributeType.Real, dval=0.01)
	
	# Note 1
	implex_check.editable = False
	implex_tol.editable = False
	implex_red.editable = False
	
	# misc
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
	cplanes_angle = mka("smoothingAngle", "Crack Planes", "Smoothing angle (in degress) for smoothing the internal variables", MpcAttributeType.Real, dval=45.0)
	
	# hardening laws - manual (by points) ...
	Te = mka("Te", "Tension", "Tensile Hardening Law (Strain)", MpcAttributeType.QuantityVector)
	Ts = mka("Ts", "Tension", "Tensile Hardening Law (Stress)", MpcAttributeType.QuantityVector)
	Td = mka("Td", "Tension", "Tensile Hardening Law (Damage)", MpcAttributeType.QuantityVector)
	Ce = mka("Ce", "Compression", "Compressive Hardening Law (Strain)", MpcAttributeType.QuantityVector)
	Cs = mka("Cs", "Compression", "Compressive Hardening Law (Stress)", MpcAttributeType.QuantityVector)
	Cd = mka("Cd", "Compression", "Compressive Hardening Law (Damage)", MpcAttributeType.QuantityVector)
	
	# ... or by minimal parameters
	fc0 = mka("fc0", "Preset", "Compressive Elastic Limit (must be < fcp)", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	fcp = mka("fcp", "Preset", "Peak Compressive Strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	fcr = mka("fcr", "Preset", "Residual Compressive Strength (must be <= fcp)", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	ecp = mka("ecp", "Preset", "Strain at Peak Compressive Strength (must be > fcp/E)", MpcAttributeType.Real)
	ft = mka("ft", "Preset", "Tensile Strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Gt = mka("Gt", "Preset", "Tensile Fracture Energy (F/L)", MpcAttributeType.QuantityScalar, adim=u.F/u.L)
	Gc = mka("Gc", "Preset", "Compressive Fracture Energy (F/L)", MpcAttributeType.QuantityScalar, adim=u.F/u.L)
	pscalet = mka("PScale Tension", "Preset", "Tensile Plasticity Scale Factor (in range 0-1)", MpcAttributeType.Real, dval=1.0)
	pscalec = mka("PScale Compression", "Preset", "Tensile Plasticity Scale Factor (in range 0-1)", MpcAttributeType.Real, dval=1.0)
	Lunit = mka("L. unit", "Preset", "Unit of measurement used for Length", MpcAttributeType.String, dval="mm")
	Lunit.sourceType = MpcAttributeSourceType.List
	Lunit.setSourceList(list(_globals.L_units.keys()))
	Funit = mka("F. unit", "Preset", "Unit of measurement used for Force", MpcAttributeType.String, dval="N")
	Funit.sourceType = MpcAttributeSourceType.List
	Funit.setSourceList(list(_globals.F_units.keys()))
	
	# regularization
	reg = mka("autoRegularization", "Regularization", ("When this flag is True (Default), the hardening/softening laws (in case of strain-softening) "
		"will be regularized according to the characteristic length of the parent element, so that the response is independent from the mesh size.<br/>"
		"If turn this flag Off, the input fracture energies will be used as they are."), 
		MpcAttributeType.Boolean, dval=True)
	lch_ref = mka("LchRef", "Regularization", ("The reference characteristic length:<br/>"
		"When the strain-hardening/softening laws show strain-softening, the area under then curve is a specific fracture energy (F/L^2), "
		"i.e. a fracture energy (F/L) divided by a size (LchRef)"),
		MpcAttributeType.QuantityScalar, dval=1.0)
	
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
	xom.addAttribute(ft)
	xom.addAttribute(fc0)
	xom.addAttribute(fcp)
	xom.addAttribute(fcr)
	xom.addAttribute(ecp)
	xom.addAttribute(Gt)
	xom.addAttribute(Gc)
	xom.addAttribute(pscalet)
	xom.addAttribute(pscalec)
	xom.addAttribute(Lunit)
	xom.addAttribute(Funit)
	# Tension
	xom.addAttribute(Te)
	xom.addAttribute(Ts)
	xom.addAttribute(Td)
	# Compression
	xom.addAttribute(Ce)
	xom.addAttribute(Cs)
	xom.addAttribute(Cd)
	# Regularization
	xom.addAttribute(reg)
	xom.addAttribute(lch_ref)
	# Integration
	xom.addAttribute(algo)
	xom.addAttribute(implex_alpha)
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
	xom.addAttribute(Kc)
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
	Kc = _geta(xobj, 'Kc').real
	
	# obtain the hardening points
	hl_fun = _globals.presets[_geta(xobj, 'Preset').string][0]
	Te,Ts,Td,Ce,Cs,Cd,auto_reg,lch_ref = hl_fun(xobj)
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
		"{0}\t-rho {4} -eta {5} -Kc {12}").format(pinfo.indent, tag, E, v, rho, eta, 
			to_tcl(Te), to_tcl(Ts), to_tcl(Td), to_tcl(Ce), to_tcl(Cs), to_tcl(Cd), Kc)
	
	if _geta(xobj, 'integration').string == 'IMPL-EX':
		#if _geta(xobj, 'implexCheckError').boolean:
		#	command += ' \\\n{}\t-implex -implexAlpha {} -implexControl {} {}'.format(
		#		pinfo.indent,
		#		_geta(xobj, 'implexAlpha').real,
		#		_geta(xobj, 'implexErrorTolerance').real,
		#		_geta(xobj, 'implexErrorTimeReductionLimit').real)
		#else:
		#	command += ' \\\n{}\t-implex -implexAlpha {}'.format(pinfo.indent, _geta(xobj, 'implexAlpha').real)
		#
		# Note 1
		command += ' \\\n{}\t-implex -implexAlpha {}'.format(pinfo.indent, _geta(xobj, 'implexAlpha').real)
	
	if _geta(xobj, '-crackPlanes').boolean:
		command += ' \\\n{}\t-crackPlanes {} {} {}'.format(pinfo.indent, 
			_geta(xobj, 'nct').integer,
			_geta(xobj, 'ncc').integer,
			_geta(xobj, 'smoothingAngle').real)
	
	if _geta(xobj, 'constitutiveTensorType').string == 'Tangent':
		command += ' \\\n{}\t-tangent'.format(pinfo.indent)
	
	if auto_reg:
		command += ' \\\n{}\t-autoRegularization {}'.format(pinfo.indent, lch_ref)
	
	command += '\n'
	
	# now write the string into the file
	pinfo.out_file.write(command)
