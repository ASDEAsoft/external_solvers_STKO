# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

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
			html_par(html_href('https://asdeasoft.net/?stko-support','DamageTC3D')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	rho = mka("rho", "Mass", "Density", MpcAttributeType.QuantityScalar, adim=((u.F/(u.L/u.t**2))/u.L**3))	
	E = mka("E", "Elasticity", "Young's modulus", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	v = mka("v", "Elasticity", "Poisson's ratio", MpcAttributeType.Real)
	ft = mka("ft", "Tension", "Tensile strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Gt = mka("Gt", "Tension", ("Tensile fracture energy.<br/>"
		"It should be per unit area, and it will be automatically regularized "
		"if the flag autoRegularization is set to True (Default).<br/>"
		"Otherwise it should be input as specific fracture energy (per unit volume)."), 
		MpcAttributeType.QuantityScalar, adim=u.F/u.L)
	fc0 = mka("fc0", "Compression", "Compressive elastic limit", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	fcp = mka("fcp", "Compression", "Compressive peak strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	fcr = mka("fcr", "Compression", "Compressive residual strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	ep = mka("ep", "Compression", "Compressive strain at peak strength", MpcAttributeType.Real)
	Gc = mka("Gc", "Compression", ("Compressive fracture energy.<br/>"
		"It should be per unit area, and it will be automatically regularized "
		"if the flag autoRegularization is set to True (Default).<br/>"
		"Otherwise it should be input as specific fracture energy (per unit volume)."), 
		MpcAttributeType.QuantityScalar, adim=u.F/u.L)
	c1  = mka("c1", "Compression", "Compressive law shape parameter", MpcAttributeType.Real, dval=0.65)
	c2  = mka("c2", "Compression", "Compressive law shape parameter", MpcAttributeType.Real, dval=0.50)
	c3  = mka("c3", "Compression", "Compressive law shape parameter", MpcAttributeType.Real, dval=1.50)
	surf_t = mka("surf_t", "Misc", "Tensile surface: Rankine or Lubliner", MpcAttributeType.String)
	surf_t.sourceType = MpcAttributeSourceType.List
	surf_t.setSourceList(['Lubliner', 'Rankine'])
	surf_t.setDefault('Rankine')
	bm = mka("bm", "Misc", "Compressive biaxial strength factor", MpcAttributeType.Real, dval=1.16)
	m1 = mka("m1", "Misc", "Shear-Compression reduction factor in range [0, 1]", MpcAttributeType.Real, dval=0.16)
	Kc = mka("Kc", "Misc", "Triaxial-Compression shape factor", MpcAttributeType.Real, dval=2.0/3.0)
	eta  = mka("eta", "Misc", "Viscosity parameter", MpcAttributeType.Real, dval=0.0)
	pdf_t = mka("pdf_t", "Misc", "Plastic-Damage factor for tensile response in range [0 (full damage) ... (mixed) ... 1 (full plasticity)]", MpcAttributeType.Real, dval=0.0)
	pdf_c = mka("pdf_c", "Misc", "Plastic-Damage factor for compressive response in range [0 (full damage) ... (mixed) ... 1 (full plasticity)]", MpcAttributeType.Real, dval=0.7)
	algo = mka("integration", "Misc", ("Integration type.<br/>"
		"(Default) Implicit: A standard Backward-Euler integration scheme.<br/>"
		"IMPL-EX: A mixed IMPLicit-EXplicit integration scheme. The resulting response is "
		"step-wise linear with a positive-definite tangent stiffnes matrix due to the explicit extrapolation of the internal variables.<br/>"
		"However the time-step should be smaller than the one used for an implicit scheme"), 
		MpcAttributeType.String, dval="Implicit")
	algo.sourceType = MpcAttributeSourceType.List
	algo.setSourceList(['Implicit', 'IMPL-EX'])
	implex_check = mka("implexCheckError", "Misc", "Check the IMPL-EX error making sure it is kept under a user-defined tolerance", MpcAttributeType.Boolean, dval=False)
	implex_tol = mka("implexErrorTolerance", "Misc", "The maximum allowed relative IMPL-EX error (normalized w.r.t. ft)", MpcAttributeType.Real, dval=0.1)
	reg = mka("autoRegularization", "Misc", ("When this flag is True (Default), the input fracture energies (Gt and Gc) "
		"will be divided by the element characteristic length, in order to obtain a response which is mesh-size independent.<br/>"
		"If turn this flag Off, the input fracture energies will be used as they are."), 
		MpcAttributeType.Boolean, dval=True)
	ctype = mka("constitutiveTensorType", "Misc", ("Constitutive Tensor Tyope.<br/>"
		"(Default) Tangent: The algorithmic tangent tensor.<br/>"
		"TangentPerturbation: The algorithmic tangent tensor computed with numerical differentiation.<br/>"
		"Secant: The secant tensor.<br/>"), 
		MpcAttributeType.String, dval="Tangent")
	ctype.sourceType = MpcAttributeSourceType.List
	ctype.setSourceList(['Tangent', 'TangentPerturbation', 'Secant'])
	
	xom = MpcXObjectMetaData()
	xom.name = 'DamageTC3D'
	xom.Xgroup = 'ASDEASoftware'
	
	# Mass
	xom.addAttribute(rho)
	# Elasticity
	xom.addAttribute(E)
	xom.addAttribute(v)
	# Tension
	xom.addAttribute(ft)
	xom.addAttribute(Gt)
	# Compression
	xom.addAttribute(fc0)
	xom.addAttribute(fcp)
	xom.addAttribute(fcr)
	xom.addAttribute(ep)
	xom.addAttribute(Gc)
	xom.addAttribute(c1)
	xom.addAttribute(c2)
	xom.addAttribute(c3)
	# Misc
	xom.addAttribute(surf_t)
	xom.addAttribute(bm)
	xom.addAttribute(m1)
	xom.addAttribute(Kc)
	xom.addAttribute(eta)
	xom.addAttribute(pdf_t)
	xom.addAttribute(pdf_c)
	xom.addAttribute(algo)
	xom.addAttribute(implex_check)
	xom.addAttribute(implex_tol)
	xom.addAttribute(reg)
	xom.addAttribute(ctype)
	
	return xom

def _check_implex(xobj):
	is_implex = xobj.getAttribute('integration').string == 'IMPL-EX'
	xobj.getAttribute('implexCheckError').visible = is_implex
	xobj.getAttribute('implexErrorTolerance').visible = is_implex

def onEditBegin(editor, xobj):
	_check_implex(xobj)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name == 'integration':
		_check_implex(xobj)

def writeTcl(pinfo):
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	def getCtype(value):
		if value == 'TangentPerturbation':
			return 1
		elif value == 'Secant':
			return 2
		else:
			return 0
	
	# get parameters
	params = ([
		('rho',geta('rho').quantityScalar.value),
		('E', geta('E').quantityScalar.value), 
		('nu', geta('v').real), 
		('ft', geta('ft').quantityScalar.value), 
		('Gt', geta('Gt').quantityScalar.value), 
		('fc0', geta('fc0').quantityScalar.value), 
		('fcp', geta('fcp').quantityScalar.value), 
		('fcr', geta('fcr').quantityScalar.value), 
		('ep', geta('ep').real), 
		('Gc', geta('Gc').quantityScalar.value), 
		('c1', geta('c1').real), 
		('c2', geta('c2').real), 
		('c3', geta('c3').real), 
		('surf_t', 0 if geta('surf_t').string == 'Lubliner' else 1), 
		('bm', geta('bm').real),
		('m1', geta('m1').real),
		('Kc', geta('Kc').real),
		('eta', geta('eta').real), 
		('pdf_t', geta('pdf_t').real), 
		('pdf_c', geta('pdf_c').real), 
		('implex', (0 if geta('integration').string == 'Implicit' else 1)), 
		('implexCheckError', (1 if geta('implexCheckError').boolean else 0)), 
		('implexErrorTolerance', geta('implexErrorTolerance').real), 
		('autoRegularization', (1 if geta('autoRegularization').boolean else 0)),
		('constitutiveTensorType', getCtype(geta('constitutiveTensorType').string))
	])
	
	# todo: pre check parameters
	
	# now write the string into the file
	pinfo.out_file.write(
		'{}nDMaterial plugin {} pdm DamageTC3D {}\n'.format(
			pinfo.indent, tag, 
			' '.join( ['-{} {}'.format(item[0], item[1]) for item in params] ))
		)