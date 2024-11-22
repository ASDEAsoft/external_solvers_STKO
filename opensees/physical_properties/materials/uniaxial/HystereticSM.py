# enable default 1D tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *
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

####################################################################################
# CHECKS for user-interaction
####################################################################################
def _cpsize(x, n):
	n0 = len(x)
	if n==n0: return x
	y = Math.vec(n)
	for i in range(min(n0, n)):
		y[i] = x[i]
	return y
def _check_env(xobj, se, ss, what=None):
	qe = _geta(xobj, se).quantityVector
	qs = _geta(xobj, ss).quantityVector
	ep = qe.referenceValue
	sp = qs.referenceValue
	if len(ep) < 2: qe.referenceValue = ep = _cpsize(ep, 2)
	if len(sp) < 2: qs.referenceValue = sp = _cpsize(sp, 2)
	if len(ep) > 7: qe.referenceValue = ep = _cpsize(ep, 7)
	if len(sp) > 7: qs.referenceValue = sp = _cpsize(sp, 7)
	ne = len(ep)
	ns = len(sp)
	if what == 1:
		qs.referenceValue = _cpsize(sp, ne)
	elif what == 2:
		qe.referenceValue = _cpsize(ep, ns)
	else:
		if ne > ns: sp = qs.referenceValue = _cpsize(sp, ne)
		elif ns > ne: ep = qe.referenceValue = _cpsize(ep, ns)
def _check_posenv(xobj, what=None):
	_check_env(xobj, 'ep', 'sp', what=what)
def _check_negenv(xobj, what=None):
	_check_env(xobj, 'en', 'sn', what=what)
def _vis_negenv(xobj):
	v = _geta(xobj, '-negEnv').boolean
	_geta(xobj, 'en').visible = v
	_geta(xobj, 'sn').visible = v
def _vis_pinch(xobj):
	v = _geta(xobj, '-pinch').boolean
	_geta(xobj, 'pinchX').visible = v
	_geta(xobj, 'pinchY').visible = v
def _vis_dam(xobj):
	v = _geta(xobj, '-damage').boolean
	_geta(xobj, 'damage1').visible = v
	_geta(xobj, 'damage2').visible = v
def _vis_beta(xobj):
	v = _geta(xobj, '-beta').boolean
	_geta(xobj, 'beta').visible = v
def _vis_degenv(xobj):
	v = _geta(xobj, '-degEnv').boolean
	_geta(xobj, 'degEnvP').visible = v
	_geta(xobj, 'degEnvN').visible = v
def _vis_lse(xobj):
	v = _geta(xobj, '-defoLimitStates').boolean
	_geta(xobj, 'eLS').visible = v
def _vis_lss(xobj):
	v = _geta(xobj, '-forceLimitStates').boolean
	_geta(xobj, 'sLS').visible = v

_onEditBegin = get_function_from_module(__name__, 'onEditBegin')
def onEditBegin(editor, xobj):
	if _onEditBegin: _onEditBegin(editor, xobj)
	_check_posenv(xobj)
	_check_negenv(xobj)
	_vis_negenv(xobj)
	_vis_pinch(xobj)
	_vis_dam(xobj)
	_vis_beta(xobj)
	_vis_degenv(xobj)
	_vis_lse(xobj)
	_vis_lss(xobj)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name == 'ep': _check_posenv(xobj, what=1)
	elif attribute_name == 'sp': _check_posenv(xobj, what=2)
	elif attribute_name == 'en': _check_negenv(xobj, what=1)
	elif attribute_name == 'sn': _check_negenv(xobj, what=2)
	elif attribute_name == '-negEnv': _vis_negenv(xobj)
	elif attribute_name == '-pinch': _vis_pinch(xobj)
	elif attribute_name == '-damage': _vis_dam(xobj)
	elif attribute_name == '-beta': _vis_beta(xobj)
	elif attribute_name == '-degEnv': _vis_degenv(xobj)
	elif attribute_name == '-defoLimitStates': _vis_lse(xobj)
	elif attribute_name == '-forceLimitStates': _vis_lss(xobj)

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
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/material/uniaxialMaterials/HystereticSM.html','HystereticSM')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	# posEnv
	ep = mka('ep', 'Positive Envelope', 'strain (or deformation) points of the positive envelope (2 to 7 points)(positive values)', MpcAttributeType.QuantityVector)
	sp = mka('sp', 'Positive Envelope', 'stress (or force) points of the positive envelope (2 to 7 points)(positive values)', MpcAttributeType.QuantityVector)
	# negEnv
	do_neg = mka('-negEnv', 'Negative Envelope', 'Define a negative enevelope, otherwise the positive will be used', MpcAttributeType.Boolean, dval=False)
	en = mka('en', 'Negative Envelope', 'strain (or deformation) points of the negative envelope (2 to 7 points)(negative values)', MpcAttributeType.QuantityVector)
	sn = mka('sn', 'Negative Envelope', 'stress (or force) points of the negative envelope (2 to 7 points)(negative values)', MpcAttributeType.QuantityVector)
	# pinching
	do_pinc = mka('-pinch', 'Pinching', 'Define pinching values', MpcAttributeType.Boolean, dval=False)
	pinchX = mka('pinchX', 'Pinching', 'pinching factor for strain (or deformation) during reloading', MpcAttributeType.Real)
	pinchY = mka('pinchY', 'Pinching', 'pinching factor for stress (or force) during reloading', MpcAttributeType.Real)
	# damage
	do_damage = mka('-damage', 'Damage', 'Define damage parameters', MpcAttributeType.Boolean, dval=False)
	damage1 = mka('damage1', 'Damage', 'damage due to ductility: D1(mu-1)', MpcAttributeType.Real)
	damage2 = mka('damage2', 'Damage', 'damage due to energy: D2(Eii/Eult)', MpcAttributeType.Real)
	do_beta = mka('-beta', 'Damage', 'Define beta parameter', MpcAttributeType.Boolean, dval=False)
	beta = mka('beta', 'Damage', 'power used to determine the degraded unloading stiffness based on ductility, mu-beta (optional, default=0.0)', MpcAttributeType.Real, dval=0.0)
	do_degEnv = mka('-degEnv', 'Damage', 'Define damage parameters for envelopes', MpcAttributeType.Boolean, dval=False)
	degEnvP = mka('degEnvP', 'Damage', 'envelope-degredation factor. This factor works with the damage parameters to degrade the POSITIVE envelope. A positive value degrades both strength and strain values, a negative values degrades only strength. The factor is applied to points 3+ (optional, default=0.0)', MpcAttributeType.Real, dval=0.0)
	degEnvN = mka('degEnvN', 'Damage', 'envelope-degredation factor. This factor works with the damage parameters to degrade the NEGATIVE envelope. A positive value degrades both strength and strain values, a negative values degrades only strength. The factor is applied to points 3+ (optional, default=degEnvP, if defined, =0. otherwise)', MpcAttributeType.Real, dval=0.0)
	# limit state
	do_eLS = mka('-defoLimitStates', 'Limit State', 'Define deformation limit states', MpcAttributeType.Boolean, dval=False)
	eLS = mka('eLS', 'Limit State', 'list of user-defined strain/deformation limits for computing deformation DCRs (optional)', MpcAttributeType.QuantityVector)
	do_sLS = mka('-forceLimitStates', 'Limit State', 'Define force limit states', MpcAttributeType.Boolean, dval=False)
	sLS = mka('sLS', 'Limit State', 'list of user-defined stress/force limits for computing force DCRs (optional)', MpcAttributeType.QuantityVector)
	# misc
	print_in = mka('-printInput', 'Misc', 'Print input', MpcAttributeType.Boolean, dval=False)
	
	# xom
	xom = MpcXObjectMetaData()
	xom.name = 'HystereticSM'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	
	# posEnv
	xom.addAttribute(ep)
	xom.addAttribute(sp)
	# negEnv
	xom.addAttribute(do_neg)
	xom.addAttribute(en)
	xom.addAttribute(sn)
	# pinching
	xom.addAttribute(do_pinc)
	xom.addAttribute(pinchX)
	xom.addAttribute(pinchY)
	# damage
	xom.addAttribute(do_damage)
	xom.addAttribute(damage1)
	xom.addAttribute(damage2)
	xom.addAttribute(do_beta)
	xom.addAttribute(beta)
	xom.addAttribute(do_degEnv)
	xom.addAttribute(degEnvP)
	xom.addAttribute(degEnvN)
	# limit state
	xom.addAttribute(do_eLS)
	xom.addAttribute(eLS)
	xom.addAttribute(do_sLS)
	xom.addAttribute(sLS)
	# misc
	xom.addAttribute(print_in)
	
	# done
	return xom

def writeTcl(pinfo):
	
	from io import StringIO
	
	# xobject and tag
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# build tcl string
	stream = StringIO()
	
	# tag
	stream.write('{}uniaxialMaterial HystereticSM {}'.format(pinfo.indent, tag))
	
	# envelopes
	stream.write(' -posEnv')
	ep = _geta(xobj, 'ep').quantityVector
	sp = _geta(xobj, 'sp').quantityVector
	for i in range(len(ep)):
		stream.write(' {} {}'.format(sp.valueAt(i), ep.valueAt(i)))
	if _geta(xobj, '-negEnv').boolean:
		stream.write(' -negEnv')
		en = _geta(xobj, 'en').quantityVector
		sn = _geta(xobj, 'sn').quantityVector
		for i in range(len(en)):
			stream.write(' {} {}'.format(sn.valueAt(i), en.valueAt(i)))
	# pinch
	if _geta(xobj, '-pinch').boolean:
		stream.write(' -pinch {} {}'.format(
			_geta(xobj, 'pinchX').real,
			_geta(xobj, 'pinchY').real))
	
	# damage
	if _geta(xobj, '-damage').boolean:
		stream.write(' -damage {} {}'.format(
			_geta(xobj, 'damage1').real,
			_geta(xobj, 'damage2').real))
	
	# beta
	if _geta(xobj, '-beta').boolean:
		stream.write(' -beta {}'.format(
			_geta(xobj, 'beta').real))
	
	# degEnv
	if _geta(xobj, '-degEnv').boolean:
		stream.write(' -degEnv {} {}'.format(
			_geta(xobj, 'degEnvP').real,
			_geta(xobj, 'degEnvN').real))
	
	# defoLimitStates
	if _geta(xobj, '-defoLimitStates').boolean:
		ls = _geta(xobj, 'eLS').quantityVector
		if len(ls) > 0:
			stream.write(' -defoLimitStates')
			for i in range(len(ls)):
				stream.write(' {}'.format(ls.valueAt(i)))
	
	# forceLimitStates
	if _geta(xobj, '-forceLimitStates').boolean:
		ls = _geta(xobj, 'sLS').quantityVector
		if len(ls) > 0:
			stream.write(' -forceLimitStates')
			for i in range(len(ls)):
				stream.write(' {}'.format(ls.valueAt(i)))
	# misc
	if _geta(xobj, '-printInput').boolean:
		stream.write(' -printInput')
	
	# done
	stream.write('\n')
	# now write the string into the file
	pinfo.out_file.write(stream.getvalue())
