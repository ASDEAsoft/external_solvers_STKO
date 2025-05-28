# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *
from opensees.utils.override_utils import get_function_from_module

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import math
from scipy.optimize import least_squares

def _err(msg):
	return 'Error in ASDBondSlip: {}'.format(msg)

def _geta(xobj, name):
	at = xobj.getAttribute(name)
	if at is None:
		raise Exception(_err('cannot find "{}" attribute'.format(name)))
	return at

class _globals:
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
	concrete_format = ('{0}uniaxialMaterial ASDConcrete1D {1} {2} \\\n'
		'{0}\t-Te {4} \\\n'
		'{0}\t-Ts {5} \\\n'
		'{0}\t-Td {6} \\\n'
		'{0}\t-Ce {7} \\\n'
		'{0}\t-Cs {8} \\\n'
		'{0}\t-Cd {9} \\\n'
		'{0}\t -eta {3}{10}{11}{12}\n')

class _mc2020:
	alpha = 0.4
	tolerance = 1.0e-4
	def _discretize(tmax, ymax, s1):
		# input: ymax can be < tmax in case of splitting failure
		def _tau_fun(x): return tmax*(x/s1)**_mc2020.alpha
		def _tau_inv(t): return (t/tmax)**(1.0/_mc2020.alpha)*s1
		def _tau_tan(x): return _mc2020.alpha*_tau_fun(x)/x
		# According to the mc2020, the unloading modulus is 6*tmax:
		#   try to find the abscissa that match 6.tmax tangent
		Ed = 6*tmax
		x1 = least_squares(lambda x : _tau_tan(x) - Ed, 1.0e-8, bounds = (1.0e-8, s1)).x[0]
		y1 = _tau_fun(x1)
		# if this first point is >= ymax, do not discretize... the peak point will be added anyway
		if y1 >= ymax*0.99:
			return ([], [])
		# dicretize the range y1-ymax
		Y = [0.0, y1]
		DY = ymax - y1
		dY = 0.2*ymax
		Ndiv = int(round(DY/dY))
		if Ndiv > 1:
			dY = DY/Ndiv
			for i in range(Ndiv-1):
				Y.append(Y[-1]+dY)
		X = [_tau_inv(ti) for ti in Y]
		return (X,Y)
	def _make_po_good(fc, cclear):
		tmax = 2.5*math.sqrt(fc)
		s1 = 1.0
		s2 = 2.0
		s3 = cclear if cclear > s2 else s2+0.01
		tu = 0.4*tmax
		X,Y = _mc2020._discretize(tmax, tmax, s1)
		X.extend([s1, s2, s3])
		Y.extend([tmax, tmax, tu])
		return (X,Y)
	def _make_po_poor(fc, cclear):
		tmax = 1.25*math.sqrt(fc)
		s1 = 1.8
		s2 = 3.6
		s3 = cclear if cclear > s2 else s2+0.01
		tu = 0.4*tmax
		X,Y = _mc2020._discretize(tmax, tmax, s1)
		X.extend([s1, s2, s3])
		Y.extend([tmax, tmax, tu])
		return (X,Y)
	def _make_sp_good_u(fc, cclear):
		# same as good in po...
		tmax_po = 2.5*math.sqrt(fc)
		s1_po = 1.0
		# eval tsplit and its abscissa s1 following curve in po...
		tmax = 7.0*(fc/25.0)**0.25 # tbu,split
		s1 = (tmax/tmax_po)**(1/_mc2020.alpha)*s1_po # s1 = s(tbu,split)
		s2 = s1*1.00001
		s3 = 1.2*s1_po # todo: not mentioned...
		tu = tmax*_mc2020.tolerance
		X,Y = _mc2020._discretize(tmax_po, tmax, s1_po)
		X.extend([s1, s2, s3])
		Y.extend([tmax, tmax, tu])
		return (X,Y)
	def _make_sp_good_c(fc, cclear):
		# same as good in po...
		tmax_po = 2.5*math.sqrt(fc)
		s1_po = 1.0
		# eval tsplit and its abscissa s1 following curve in po...
		tmax = 8.0*(fc/25.0)**0.25 # tbu,split
		s1 = (tmax/tmax_po)**(1/_mc2020.alpha)*s1_po # s1 = s(tbu,split)
		s2 = s1*1.00001
		s3 = 0.5*cclear
		if s3 <= s2: s3 = s2+0.01
		tu = 0.4*tmax
		X,Y = _mc2020._discretize(tmax_po, tmax, s1_po)
		X.extend([s1, s2, s3])
		Y.extend([tmax, tmax, tu])
		return (X,Y)
	def _make_sp_poor_u(fc, cclear):
		# same as good in po...
		tmax_po = 1.25*math.sqrt(fc)
		s1_po = 1.8
		# eval tsplit and its abscissa s1 following curve in po...
		tmax = 5.0*(fc/25.0)**0.25 # tbu,split
		s1 = (tmax/tmax_po)**(1/_mc2020.alpha)*s1_po # s1 = s(tbu,split)
		s2 = s1*1.00001
		s3 = 1.2*s1_po # todo: not mentioned...
		tu = tmax*_mc2020.tolerance
		X,Y = _mc2020._discretize(tmax_po, tmax, s1_po)
		X.extend([s1, s2, s3])
		Y.extend([tmax, tmax, tu])
		return (X,Y)
	def _make_sp_poor_c(fc, cclear):
		# same as good in po...
		tmax_po = 1.25*math.sqrt(fc)
		s1_po = 1.8
		# eval tsplit and its abscissa s1 following curve in po...
		tmax = 5.5*(fc/25.0)**0.25 # tbu,split
		s1 = (tmax/tmax_po)**(1/_mc2020.alpha)*s1_po # s1 = s(tbu,split)
		s2 = s1*1.00001
		s3 = 0.5*cclear
		if s3 <= s2: s3 = s2+0.01
		tu = 0.4*tmax
		X,Y = _mc2020._discretize(tmax_po, tmax, s1_po)
		X.extend([s1, s2, s3])
		Y.extend([tmax, tmax, tu])
		return (X,Y)
	def make(pull_out, good_bond, confined, fc, cclear):
		# obtain discrete points of the total backbone curve
		if pull_out:
			if good_bond:
				X1,Y1 = _mc2020._make_po_good(fc, cclear)
			else:
				X1,Y1 = _mc2020._make_po_poor(fc, cclear)
		else:
			if good_bond:
				if confined:
					X1,Y1 = _mc2020._make_sp_good_c(fc, cclear)
				else:
					X1,Y1 = _mc2020._make_sp_good_u(fc, cclear)
			else:
				if confined:
					X1,Y1 = _mc2020._make_sp_poor_c(fc, cclear)
				else:
					X1,Y1 = _mc2020._make_sp_poor_u(fc, cclear)
		# get peak and residual forces
		tpeak = Y1[-2]
		tu = Y1[-1]
		# obtain the tolerance for zero-stress and the factor for the parallel material
		stress_null = tpeak*_mc2020.tolerance
		factor = 1.0-tu/tpeak
		# compute the X2 and Y2 removing the last point (i.e. remove softening)
		X2 = X1[:-1]
		Y2 = Y1[:-1]
		# remove the residual part from the first component
		Y1[-1] = 0.0
		D1 = [0.0]*len(X1)
		D2 = [0.0]*len(X2)
		# done
		return (X1, Y1, X2, Y2, D1, D2, stress_null, factor)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name == 'Failure Mode':
		is_splitting = _geta(xobj, attribute_name).string == 'Splitting(SP)'
		_geta(xobj, 'Confinement').visible = is_splitting
	return None

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
			#html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/material/uniaxialMaterials/ASDConcrete1D.html','ASDConcrete1D')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	fail_type = mka('Failure Mode', 'Bond-Slip', 
		'''<p>"<strong>Pull-out failure</strong>" is valid for well-confined concrete (concrete cover&nbsp;&ge; 5&Oslash;, clear spacing between bars &ge; 10&Oslash;), or suitable confining reinforcement.</p>
<p><span style="color: #3366ff;"><em>Ref: fib Model Code 2020; 20.5.1.1 (pag. 308, Table 20.5-1)</em></span></p>''', 
		MpcAttributeType.String, dval='Splitting(SP)')
	fail_type.sourceType = MpcAttributeSourceType.List
	fail_type.setSourceList(['Splitting(SP)', 'Pull-out(PO)'])
	
	bond_type = mka('Bond conditions', 'Bond-Slip',
'''<p>"<strong>Good</strong>" bond conditions are defined as:</p>
<ul>
<li>bars with an inclination less than 45&deg; to the horizontal which are up to 300 mm from the bottom of the formwork&nbsp;or at least 300 mm below the free surface during concreting.</li>
</ul>
<p>Otherwise "<strong>Poor</strong>" bond conditions should be assumed.</p>
<p><span style="color: #3366ff;"><em>Ref: fib Model Code 2020; 20.2.2.1 (pag. 280)</em></span></p>''',
		MpcAttributeType.String, dval='Poor')
	bond_type.sourceType = MpcAttributeSourceType.List
	bond_type.setSourceList(['Good', 'Poor'])
	
	conf_type = mka('Confinement', 'Bond-Slip', 
		'''<p>"<strong>Unconfined</strong>" or "<strong>Sitrrups</strong>" options available only for "<strong>Splitting (SP)</strong>" failure mode.</p>
<p><span style="color: #3366ff;"><em>Ref: fib Model Code 2020; 20.5.1.1 (pag. 308, Table 20.5-1)</em></span></p>''', 
		MpcAttributeType.String, dval='Unconfined')
	conf_type.sourceType = MpcAttributeSourceType.List
	conf_type.setSourceList(['Unconfined', 'Stirrups'])
	
	fc = mka('fc', 'Bond-Slip', 
		'''<p>Concrete compressive strength</p>
<p><span style="color: #3366ff;"><em>Ref: fib Model Code 2020; 20.5.1.1 (pag. 308, Table 20.5-1)</em></span></p>''', 
		MpcAttributeType.QuantityScalar, adim=u.F/u.L**2, dval=0.0)
	
	cclear = mka('cclear', 'Bond-Slip', 
		'''<p>The clear distance between ribs</p>
<p><span style="color: #3366ff;"><em>Ref: fib Model Code 2020; 20.5.1.1 (pag. 308, Table 20.5-1)</em></span></p>''', 
		MpcAttributeType.QuantityScalar, adim=u.L, dval=0.0)
	
	Lunit = mka('L. unit', 'Units', 'Unit of measurement used for Length', MpcAttributeType.String, dval="mm")
	Lunit.sourceType = MpcAttributeSourceType.List
	Lunit.setSourceList(list(_globals.L_units.keys()))
	
	Funit = mka('F. unit', 'Units', 'Unit of measurement used for Force', MpcAttributeType.String, dval="N")
	Funit.sourceType = MpcAttributeSourceType.List
	Funit.setSourceList(list(_globals.F_units.keys()))
	
	algo = mka('Integration', 'Misc', '''<p>The integration algorithm</p>
<ul>
<li><strong>Implicit</strong>: A standard Backward-Euler integration scheme.</li>
<li><strong>IMPL-EX</strong>:&nbsp;A mixed IMPLicit-EXplicit integration scheme. The resulting response is&nbsp;step-wise linear with a positive-definite tangent stiffness matrix due to the explicit extrapolation of the internal variables.&nbsp;However, the time-step should be smaller than the one used for an implicit scheme.</li>
</ul>
<p><span style="color: #3366ff;"><em>Ref: Oliver, J., Huespe, A. E., &amp; Cante, J. C. (2008). &ldquo;An implicit/explicit integration scheme to increase computability of non-linear material and contact/friction problems&rdquo; Computer Methods in Applied Mechanics and Engineering, 197(21-24), 1865-1889</em></span></p>
<p><span style="color: #3366ff;"><em><a href="https://core.ac.uk/download/pdf/325948712.pdf">Link to article</a></em></span></p>''', 
		MpcAttributeType.String, dval='Implicit')
	algo.sourceType = MpcAttributeSourceType.List
	algo.setSourceList(['Implicit', 'IMPL-EX'])
	
	ctype = mka('Constitutive Tensor Type', 'Misc', '''<p>Constitutive tensor type</p>
<ul>
<li><strong>Tangent</strong>: The algorithmic tangent tensor.</li>
<li><strong>Secant</strong>: The secant tensor.</li>
</ul>
<p>&nbsp;</p>''', 
		MpcAttributeType.String, dval='Secant')
	ctype.sourceType = MpcAttributeSourceType.List
	ctype.setSourceList(['Tangent', 'Secant'])
	
	eta  = mka('eta', 'Misc', 'Viscosity parameter', MpcAttributeType.Real, dval=0.0)
	
	reg = mka("autoRegularization", "Regularization", ("When this flag is True (Default), the hardening/softening laws (in case of strain-softening) "
		"will be regularized according to the characteristic length of the parent element, so that the response is independent from the mesh size.<br/>"
		"If turn this flag Off, the input fracture energies will be used as they are."), 
		MpcAttributeType.Boolean, dval=False)
	reg.editable = False
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDBondSlip'
	xom.Xgroup = 'ASDEASoftware'
	
	xom.addAttribute(fail_type)
	xom.addAttribute(bond_type)
	xom.addAttribute(conf_type)
	xom.addAttribute(fc)
	xom.addAttribute(cclear)
	xom.addAttribute(Lunit)
	xom.addAttribute(Funit)
	xom.addAttribute(eta)
	xom.addAttribute(algo)
	xom.addAttribute(ctype)
	xom.addAttribute(reg)
	
	return xom

def writeTcl(pinfo):
	
	# xobject and material tag
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# get basic parameters
	pull_out = _geta(xobj, 'Failure Mode').string == 'Pull-out(PO)'
	good_bond = _geta(xobj, 'Bond conditions').string == 'Good'
	confined = _geta(xobj, 'Confinement').string == 'Stirrups'
	fc = _geta(xobj, 'fc').quantityScalar.value
	cclear = _geta(xobj, 'cclear').quantityScalar.value
	eta = _geta(xobj, 'eta').real
	tangent = _geta(xobj, 'Constitutive Tensor Type').string == 'Tangent'
	implex = _geta(xobj, 'Integration').string == 'IMPL-EX'
	reg = _geta(xobj, 'autoRegularization').boolean
	
	# checks
	if fc <= 0.0:
		raise Exception(_err('fc should be strictly positive (>=0)'))
	if cclear <= 0.0:
		raise Exception(_err('cclear should be strictly positive (>=0)'))
	
	# units
	L = _globals.L_units[_geta(xobj, 'L. unit').string]
	F = _globals.F_units[_geta(xobj, 'F. unit').string]
	mm = L # to mm, from mm = 1/mm
	MPa = F/L/L # to MPa, from MPa = 1/MPa
	
	# convert inputs to N-m
	fc = fc*MPa
	cclear = cclear*mm
	
	# define basic points according to MC2020
	X1, Y1, X2, Y2, D1, D2, stress_null, factor = _mc2020.make(pull_out, good_bond, confined, fc, cclear)
	
	# convert back to original units
	X1 = [ix/mm for ix in X1]
	X2 = [ix/mm for ix in X2]
	Y1 = [iy/MPa for iy in Y1]
	Y2 = [iy/MPa for iy in Y2]
	stress_null /= MPa
	
	# define null backbone points
	E1 = Y1[1]/X1[1]
	E2 = Y2[1]/X2[1]
	strain_null = stress_null/E1
	X_null = [0.0, strain_null, strain_null*2]
	Y_null = [0.0, stress_null, stress_null]
	D_null = [1.0, 1.0, 1.0]
	def to_tcl(x):
		return ' '.join(str(i) for i in x)
	
	# define 3 extra material IDs
	def next_id():
		id = pinfo.next_physicalProperties_id
		if id == tag:
			# this can happen only while testing a property in new command (on empty doc)
			id += 1
			pinfo.next_physicalProperties_id += 1
		pinfo.next_physicalProperties_id += 1
		return id
	id_pos = next_id()
	id_neg = next_id()
	id_res = next_id()
	
	# write comment
	pinfo.out_file.write('{}# ASDBondSlip [{}]\n'.format(pinfo.indent, tag))
	
	# positive pinching material
	pinfo.out_file.write(_globals.concrete_format.format(
		pinfo.indent, id_pos, E1, eta, 
		to_tcl(X1), to_tcl(Y1), to_tcl(D1),
		to_tcl(X_null), to_tcl(Y_null), to_tcl(D_null),
		' -tangent' if tangent else '',
		' -implex' if implex else '',
		' -autoRegularization 1.0' if reg else ''))
	# negative pinching material
	pinfo.out_file.write(_globals.concrete_format.format(
		pinfo.indent, id_neg, E1, eta, 
		to_tcl(X_null), to_tcl(Y_null), to_tcl(D_null),
		to_tcl(X1), to_tcl(Y1), to_tcl(D1),
		' -tangent' if tangent else '',
		' -implex' if implex else '',
		' -autoRegularization 1.0' if reg else ''))
	# frictional material
	pinfo.out_file.write(_globals.concrete_format.format(
		pinfo.indent, id_res, E2, eta, 
		to_tcl(X2), to_tcl(Y2), to_tcl(D2),
		to_tcl(X2), to_tcl(Y2), to_tcl(D2),
		' -tangent' if tangent else '',
		' -implex' if implex else '',
		' -autoRegularization 1.0' if reg else ''))
	# combine
	pinfo.out_file.write('{}uniaxialMaterial Parallel {}  {} {} {} -factors {} {} {}\n'.format(pinfo.indent, tag, id_pos, id_neg, id_res, factor, factor, 1.0-factor))
