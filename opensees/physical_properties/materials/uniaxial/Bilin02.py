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
			html_par(html_href('','Bilin02')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	Ke = mka("Ke", "Elasticity", "Elastic stiffness", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	AsPos = mka("AsPos", "Non-linear", "Strain hardening ratio for positive loading direction", MpcAttributeType.Real)
	AsNeg = mka("AsNeg", "Non-linear", "Strain hardening ratio for negative loading direction", MpcAttributeType.Real)
	My_pos = mka("My_pos", "Non-linear", "Effective yield strength for positive loading direction", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	My_neg = mka("My_neg", "Non-linear", "Effective yield strength for negative loading direction (negative value)", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	LamdaS = mka("LamdaS", "Non-linear", "Cyclic deterioration parameter for strength deterioration [E_t=Lamda_S*M_y; set Lamda_S = 0 to disable this mode of deterioration]", MpcAttributeType.Real)
	LamdaD = mka("LamdaD", "Non-linear", "Cyclic deterioration parameter for post-capping strength deterioration [E_t=LamdaD*M_y; set LamdaD = 0 to disable this mode of deterioration]", MpcAttributeType.Real)
	LamdaA = mka("LamdaA", "Non-linear", "Cyclic deterioration parameter for acceleration reloading stiffness deterioration (is not a deterioration mode for a component with Bilinear hysteretic response) [Input value is required, but not used; set LamdaA = 0]", MpcAttributeType.Real)
	LamdaK = mka("LamdaK", "Non-linear", "Cyclic deterioration parameter for unloading stiffness deterioration [E_t=LamdaK*M_y; set LamdaK = 0 to disable this mode of deterioration]", MpcAttributeType.Real)
	Cs = mka("Cs", "Non-linear", "Rate of strength deterioration. The default value is 1.0.", MpcAttributeType.Real)
	Cs.setDefault(1.0)
	Cd = mka("Cd", "Non-linear", "Rate of post-capping strength deterioration. The default value is 1.0.", MpcAttributeType.Real)
	Cd.setDefault(1.0)
	Ca = mka("Ca", "Non-linear", "Rate of accelerated reloading deterioration. The default value is 1.0.", MpcAttributeType.Real)
	Ca.setDefault(1.0)
	Ck = mka("Ck", "Non-linear", "Rate of unloading stiffness deterioration. The default value is 1.0.", MpcAttributeType.Real)
	Ck.setDefault(1.0)
	Thetap_pos = mka("Thetap_pos", "Non-linear", "Pre-capping rotation for positive loading direction (often noted as plastic rotation capacity)", MpcAttributeType.Real)
	Thetap_neg = mka("Thetap_neg", "Non-linear", "Pre-capping rotation for negative loading direction (often noted as plastic rotation capacity) (positive value)", MpcAttributeType.Real)
	Thetapc_pos = mka("Thetapc_pos", "Non-linear", "Post-capping rotation for positive loading direction", MpcAttributeType.Real)
	Thetapc_neg = mka("Thetapc_neg", "Non-linear", "Post-capping rotation for negative loading direction (positive value)", MpcAttributeType.Real)
	KPos = mka("KPos", "Non-linear", "Residual strength ratio for positive loading direction", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	KNeg = mka("KNeg", "Non-linear", "Residual strength ratio for negative loading direction (positive value)", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Thetau_pos = mka("Thetau_pos", "Non-linear", "Ultimate rotation capacity for positive loading direction", MpcAttributeType.Real)
	Thetau_neg = mka("Thetau_neg", "Non-linear", "Ultimate rotation capacity for negative loading direction (positive value)", MpcAttributeType.Real)
	PDPlus = mka("PDPlus", "Non-linear", "Rate of cyclic deterioration in the positive loading direction (this parameter is used to create assymetric hysteretic behavior for the case of a composite beam). For symmetric hysteretic response use 1.0.", MpcAttributeType.Real)
	PDNeg = mka("PDNeg", "Non-linear", "Rate of cyclic deterioration in the negative loading direction (this parameter is used to create assymetric hysteretic behavior for the case of a composite beam). For symmetric hysteretic response use 1.0.", MpcAttributeType.Real)
	
	# Optional parameters
	use_nFactor = mka("use_nFactor", "Optional parameters", "Elastic stiffness amplification factor, mainly for use with concentrated plastic hinge elements (optional, default = 0).", MpcAttributeType.Boolean)
	nFactor = mka("nFactor", "Optional parameters", "Elastic stiffness amplification factor, mainly for use with concentrated plastic hinge elements (optional, default = 0).", MpcAttributeType.Real)
	nFactor.setDefault(0.0)

	# uniaxialMaterial Bilin02 tag? Ke? AsPos? AsNeg? My_pos? My_neg? LamdaS?
	# LamdaD?  LamdaA? LamdaK? Cs? Cd? Ca? Ck? Thetap_pos? Thetap_neg? Thetapc_pos? Thetapc_neg? KPos? 
	# KNeg? Thetau_pos? Thetau_neg? PDPlus?  PDNeg?

	xom = MpcXObjectMetaData()
	xom.name = 'Bilin02'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(Ke)
	xom.addAttribute(AsPos)
	xom.addAttribute(AsNeg)
	xom.addAttribute(My_pos)
	xom.addAttribute(My_neg)
	xom.addAttribute(LamdaS)
	xom.addAttribute(LamdaD)
	xom.addAttribute(LamdaA)
	xom.addAttribute(LamdaK)
	xom.addAttribute(Cs)
	xom.addAttribute(Cd)
	xom.addAttribute(Ca)
	xom.addAttribute(Ck)
	xom.addAttribute(Thetap_pos)
	xom.addAttribute(Thetap_neg)
	xom.addAttribute(Thetapc_pos)
	xom.addAttribute(Thetapc_neg)
	xom.addAttribute(KPos)
	xom.addAttribute(KNeg)
	xom.addAttribute(Thetau_pos)
	xom.addAttribute(Thetau_neg)
	xom.addAttribute(PDPlus)
	xom.addAttribute(PDNeg)
	xom.addAttribute(use_nFactor)
	xom.addAttribute(nFactor)
	
	# nFactor-dep
	xom.setVisibilityDependency(use_nFactor, nFactor)

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

	# optional paramters
	sopt = ''
	if geta('use_nFactor').boolean:
		sopt += ' {}'.format(geta('nFactor').real)

	# uniaxialMaterial Bilin02 tag? Ke? AsPos? AsNeg? My_pos? My_neg? LamdaS?
	# LamdaD?  LamdaA? LamdaK? Cs? Cd? Ca? Ck? Thetap_pos? Thetap_neg? Thetapc_pos? Thetapc_neg? KPos? 
	# KNeg? Thetau_pos? Thetau_neg? PDPlus?  PDNeg?

	str_tcl = '{}uniaxialMaterial Bilin02 {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}{}\n'.format(
			pinfo.indent,
			tag,
			geta('Ke').quantityScalar.value,
			geta('AsPos').real,
			geta('AsNeg').real,
			geta('My_pos').quantityScalar.value,
			geta('My_neg').quantityScalar.value,
			geta('LamdaS').real,
			geta('LamdaD').real,
			geta('LamdaA').real,
			geta('LamdaK').real,
			geta('Cs').real,
			geta('Cd').real,
			geta('Ca').real,
			geta('Ck').real,
			geta('Thetap_pos').real,
			geta('Thetap_neg').real,
			geta('Thetapc_pos').real,
			geta('Thetapc_neg').real,
			geta('KPos').quantityScalar.value,
			geta('KNeg').quantityScalar.value,
			geta('Thetau_pos').real,
			geta('Thetau_neg').real,
			geta('PDPlus').real,
			geta('PDNeg').real,
			sopt)

	# uniaxialMaterial Bilin02 tag? Ke? AsPos? AsNeg? My_pos? My_neg? LamdaS?
	# LamdaD?  LamdaA? LamdaK? Cs? Cd? Ca? Ck? Thetap_pos? Thetap_neg? Thetapc_pos? Thetapc_neg? KPos? 
	# KNeg? Thetau_pos? Thetau_neg? PDPlus?  PDNeg?

	# now write the string into the file
	pinfo.out_file.write(str_tcl)