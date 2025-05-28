# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *
from opensees.utils.override_utils import get_function_from_module

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import math
import importlib

def _err(msg):
	return 'Error in ASDSteel1D: {}'.format(msg)

def _geta(xobj, name):
	at = xobj.getAttribute(name)
	if at is None:
		raise Exception(_err('cannot find "{}" attribute'.format(name)))
	return at

_onEditBegin = get_function_from_module(__name__, 'onEditBegin')
def onEditBegin(editor, xobj):
	if _onEditBegin: _onEditBegin(editor, xobj)
	onAttributeChanged(editor, xobj, 'Buckling')

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name in ['Buckling', 'Bond-Slip', 'Optional']:
		is_buck = _geta(xobj, 'Buckling').boolean
		is_slip = _geta(xobj, 'Bond-Slip').boolean
		_geta(xobj, 'Buckling Length').visible = is_buck
		_geta(xobj, 'Anchorage Length').visible = is_slip
		_geta(xobj, 'Slip Material Tag').visible = is_slip
		_geta(xobj, 'Radius').visible = is_buck or is_slip
		is_optional = _geta(xobj, 'Optional').boolean
		_geta(xobj, 'K_alpha').visible = is_optional
		_geta(xobj, 'max_iter').visible = is_optional
		_geta(xobj, 'tolU').visible = is_optional
		_geta(xobj, 'tolR').visible = is_optional
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
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/material/uniaxialMaterials/ASDSteel1D.html','ASDSteel1D')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	E = mka("Young's modulus", "Elasticity", "The Young's modulus", MpcAttributeType.QuantityScalar, adim = u.F/u.L/u.L)
	
	sy = mka("sy", "Plasticity", "Yield stress", MpcAttributeType.QuantityScalar, adim = u.F/u.L/u.L)
	su = mka("su", "Plasticity", "Ultimate stress", MpcAttributeType.QuantityScalar, adim = u.F/u.L/u.L)
	eu = mka("eu", "Plasticity", "Ultimate strain", MpcAttributeType.QuantityScalar)
	
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
	
	# let's write a better description for the following attributes
	optional = mka("Optional", "Misc", 
				"Optional", 
				MpcAttributeType.Boolean, dval = False)
	K_alpha = mka("K_alpha", "Misc",
				("It is a factor that combines the tangent stiffness matrix with the initial stiffness matrix, to avoid convergence issues. "
				"K = K_alpha * K_tangent + (1-K_alpha) * K_initial"),
				MpcAttributeType.QuantityScalar, dval = 0.5)
	max_iter = mka("max_iter", "Misc",
				 "It is the maximum number of iterations for the Newton-Raphson method used in the return-mapping algorithm for steel.", 
				 MpcAttributeType.Integer, dval = 100)
	tolU = mka("tolU", "Misc", 
			"It is the tolerance for the strain convergence in the return-mapping algorithm for steel.", 
			MpcAttributeType.QuantityScalar, dval = 1.0e-6)
	tolR = mka("tolR", "Misc", 
			"It is the tolerance for the residual convergence in the return-mapping algorithm for steel.", 
			MpcAttributeType.QuantityScalar, dval = 1.0e-6)
	
	frac = mka('Fracture', 'Reinforcing steel features', 
		'If selected, the material will exhibit damage resulting in strength and stiffness degradation, if the total strain exceeds the utlimate strain',
		MpcAttributeType.Boolean,
		dval = False)
	
	buck = mka('Buckling', 'Reinforcing steel features', 
		'If selected, the material will account for buckling',
		MpcAttributeType.Boolean,
		dval = False)
	slip = mka('Bond-Slip', 'Reinforcing steel features', 
		'If selected, the material will account for bond-slip',
		MpcAttributeType.Boolean,
		dval = False)
	b_lch = mka('Buckling Length', 'Reinforcing steel features',
		'The characteristic length for buckling',
		MpcAttributeType.QuantityScalar,
		dval = 0.0)
	
	s_tag = mka('Slip Material Tag', 'Reinforcing steel features',
		'A previously defined uniaxial material tag for the bond-slip model',
		MpcAttributeType.Index)
	s_tag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	s_tag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	lch_anc = mka('Anchorage Length', 'Reinforcing steel features',
		'The anchorage length for slip',
		MpcAttributeType.QuantityScalar,
		dval = 0.0)
	radius = mka('Radius', 'Reinforcing steel features',
		'The rebar radius',
		MpcAttributeType.QuantityScalar,
		dval = 0.0)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDSteel1D'
	xom.Xgroup = 'ASDEASoftware'
	
	xom.addAttribute(E)
	xom.addAttribute(sy)
	xom.addAttribute(su)
	xom.addAttribute(eu)
	xom.addAttribute(algo)
	xom.addAttribute(optional)
	xom.addAttribute(K_alpha)
	xom.addAttribute(max_iter)
	xom.addAttribute(tolU)
	xom.addAttribute(tolR)
	xom.addAttribute(frac)
	xom.addAttribute(buck)
	xom.addAttribute(slip)
	xom.addAttribute(b_lch)
	xom.addAttribute(lch_anc)
	xom.addAttribute(s_tag)
	xom.addAttribute(radius)

	return xom

def writeTcl(pinfo):
	
	'''
	uniaxialMaterial ASDSteel1D $tag $E $sy $su $eu  
	<-implex>  
	<-buckling  $lch < $r>> 
	<-fracture> 
	<-slip $matTag $lch_anc <$r>> 
	<-K_alpha $K_alpha> <-max_iter $max_iter> <-tolU $tolU> <-tolR $tolR>
	'''

	# xobject and material tag
	current_prop = pinfo.phys_prop
	xobj = current_prop.XObject
	tag = xobj.parent.componentId
	
	# get mandatory parameters
	E = _geta(xobj, "Young's modulus").quantityScalar.value
	if E <= 0.0:
		raise Exception(_err('Young\'s modulus must be greater than zero'))
	sy = _geta(xobj, "sy").quantityScalar.value
	if sy <= 0.0:
		raise Exception(_err('yield stress must be greater than zero'))
	su = _geta(xobj, "su").quantityScalar.value
	if su <= sy:
		raise Exception(_err('ultimate stress must be greater than yield stress'))
	eu = _geta(xobj, "eu").quantityScalar.value
	if eu < sy/E:
		raise Exception(_err('ultimate strain must be greater than yield strain'))
	implex = ' -implex' if _geta(xobj, 'Integration').string == 'IMPL-EX' else ''

	opt = ''
	if _geta(xobj, 'Optional').boolean:
		K_alpha = _geta(xobj, 'K_alpha').quantityScalar.value
		if K_alpha < 0.0 or K_alpha > 1.0:
			raise Exception(_err('K_alpha must be in the range [0, 1]'))	
		max_iter = _geta(xobj, 'max_iter').integer
		tolU = _geta(xobj, 'tolU').quantityScalar.value
		tolR = _geta(xobj, 'tolR').quantityScalar.value
		opt = ' -K_alpha {} -max_iter {} -tolU {} -tolR {}'.format(K_alpha, max_iter, tolU, tolR)

	frac = ' -fracture' if _geta(xobj, 'Fracture').boolean else ''
	
	radius = _geta(xobj, 'Radius').quantityScalar.value
	
	radius_written = False
	buck = ''
	if _geta(xobj, 'Buckling').boolean:
		b_lch = _geta(xobj, 'Buckling Length').quantityScalar.value
		if b_lch <= 0.0:
			raise Exception(_err('buckling length must be greater than zero'))
		buck = ' -buckling {} {}'.format(b_lch, radius)
		radius_written = True
	slip = ''
	if _geta(xobj, 'Bond-Slip').boolean:
		slip_tag = _geta(xobj, 'Slip Material Tag').index
		if slip_tag == 0:
			raise Exception(_err('slip material tag is not defined'))
		
		# if the PhysicalProperty identfied by s_tag has an XObject of type 'ASDBondSlip1D'
		# we can:
		# - temporarily change the '-autoRegularization' attribute to True
		# - temprarily change its tag to the maximum tag + 1
		# - write that XObject
		# - restore the original values (s_tag, old_reg, pinfo.phys_prop)
		s_prop = App.caeDocument().getPhysicalProperty(slip_tag)
		s_xobj = s_prop.XObject
		if s_xobj.name == 'ASDBondSlip':
			# temporarily change the '-autoRegularization' attribute to True
			reg_at = s_xobj.getAttribute('autoRegularization')
			old_reg = reg_at.boolean
			old_slip_tag = slip_tag
			try:
				reg_at.boolean = True
				# temporarily change its tag to the maximum tag + 1
				slip_tag = pinfo.next_physicalProperties_id
				pinfo.next_physicalProperties_id += 1
				s_xobj.parent.id = slip_tag
				# write that XObject
				s_module_name = 'opensees.physical_properties.{}.{}'.format(s_xobj.Xnamespace, s_xobj.name)
				s_module = importlib.import_module(s_module_name)
				if hasattr(s_module, 'writeTcl'):
					pinfo.phys_prop = s_prop
					s_module.writeTcl(pinfo)
			finally:
				# restore the original values
				s_xobj.parent.id = old_slip_tag
				reg_at.boolean = old_reg
				pinfo.phys_prop = current_prop

		lch_anc = _geta(xobj, 'Anchorage Length').quantityScalar.value
		if lch_anc < 0.0:
			raise Exception(_err('anchorage length must be greater than or equal to zero'))
		slip = ' -slip {} {}'.format(slip_tag, lch_anc)
		if not radius_written:
			radius_written = True
			radius = _geta(xobj, 'Radius').quantityScalar.value
			if radius <= 0.0:
				raise Exception(_err('radius must be greater than zero'))
			slip += ' {}'.format(radius)
	
	if radius_written:
		if radius <= 0.0:
			raise Exception(_err('radius must be greater than zero'))

	# write the material command
	pinfo.out_file.write('{}uniaxialMaterial ASDSteel1D {} {} {} {} {}{}{}{}{}{}\n'.format(
		pinfo.indent, tag, E, sy, su, eu, implex, frac, buck, slip, opt))
	
	