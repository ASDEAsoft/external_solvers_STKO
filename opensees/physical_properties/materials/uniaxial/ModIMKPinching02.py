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
			html_par(html_href('','ModIMKPinching02')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	Ke = mka("Ke", "Elasticity", "Elastic stiffness", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	alfaPos = mka("alfaPos", "Non-linear", "Strain hardening ratio for positive loading direction", MpcAttributeType.Real)
	alfaNeg = mka("alfaNeg", "Non-linear", "Strain hardening ratio for negative loading direction", MpcAttributeType.Real)
	My_pos = mka("My_pos", "Non-linear", "Effective yield strength for positive loading direction", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	My_neg = mka("My_neg", "Non-linear", "Effective yield strength for negative loading direction (negative value)", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	
	FprPos = mka("FprPos", "Non-linear", "Ratio of the force at which reloading begins to force corresponding to the maximum historic deformation demand (positive loading direction)", MpcAttributeType.Real)
	FprNeg = mka("FprNeg", "Non-linear", "Ratio of the force at which reloading begins to force corresponding to the absolute maximum historic deformation demand (negative loading direction)", MpcAttributeType.Real)
	A_pinch = mka("A_pinch", "Non-linear", "Ratio of reloading stiffness", MpcAttributeType.Real)
	
	Ls = mka("Ls", "Non-linear", "Cyclic deterioration parameter for strength deterioration [E_t=Ls*M_y; set Ls = 0 to disable this mode of deterioration]", MpcAttributeType.Real)
	Ld = mka("Ld", "Non-linear", "Cyclic deterioration parameter for post-capping strength deterioration [E_t=Ld*M_y; set Ld = 0 to disable this mode of deterioration]", MpcAttributeType.Real)
	La = mka("La", "Non-linear", "Cyclic deterioration parameter for accelerated reloading stiffness deterioration [E_t=La*M_y, see Lignos and Krawinkler (2011); set La = 0 to disable this mode of deterioration]", MpcAttributeType.Real)
	Lk = mka("Lk", "Non-linear", "Cyclic deterioration parameter for unloading stiffness deterioration [E_t=Lk*M_y; set Lk = 0 to disable this mode of deterioration]", MpcAttributeType.Real)
	Cs = mka("Cs", "Non-linear", "Rate of strength deterioration. The default value is 1.0.", MpcAttributeType.Real)
	Cs.setDefault(1.0)
	Cd = mka("Cd", "Non-linear", "Rate of post-capping strength deterioration. The default value is 1.0.", MpcAttributeType.Real)
	Cd.setDefault(1.0)
	Ca = mka("Ca", "Non-linear", "Rate of accelerated reloading deterioration. The default value is 1.0.", MpcAttributeType.Real)
	Ca.setDefault(1.0)
	Ck = mka("Ck", "Non-linear", "Rate of unloading stiffness deterioration. The default value is 1.0.", MpcAttributeType.Real)
	Ck.setDefault(1.0)
	thetaPpos = mka("thetaPpos", "Non-linear", "Pre-capping rotation for positive loading direction (often noted as plastic rotation capacity)", MpcAttributeType.Real)
	thetaPneg = mka("thetaPneg", "Non-linear", "Pre-capping rotation for negative loading direction (often noted as plastic rotation capacity) (positive value)", MpcAttributeType.Real)
	thetaPCpos = mka("thetaPCpos", "Non-linear", "Post-capping rotation for positive loading direction", MpcAttributeType.Real)
	thetaPCneg = mka("thetaPCneg", "Non-linear", "Post-capping rotation for negative loading direction (positive value)", MpcAttributeType.Real)
	ResfacPos = mka("ResfacPos", "Non-linear", "Residual strength ratio for positive loading direction", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	ResfacNeg = mka("ResfacNeg", "Non-linear", "Residual strength ratio for negative loading direction (positive value)", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	fracDispPos = mka("fracDispPos", "Non-linear", "Ultimate rotation capacity for positive loading direction", MpcAttributeType.Real)
	fracDispNeg = mka("fracDispNeg", "Non-linear", "Ultimate rotation capacity for negative loading direction (positive value)", MpcAttributeType.Real)
	DPos = mka("DPos", "Non-linear", "Rate of cyclic deterioration in the positive loading direction (this parameter is used to create assymetric hysteretic behavior for the case of a composite beam). For symmetric hysteretic response use 1.0.", MpcAttributeType.Real)
	DNeg = mka("DNeg", "Non-linear", "Rate of cyclic deterioration in the negative loading direction (this parameter is used to create assymetric hysteretic behavior for the case of a composite beam). For symmetric hysteretic response use 1.0.", MpcAttributeType.Real)
	
	# Optional parameters
	use_nFactor = mka("use_nFactor", "Optional parameters", "Elastic stiffness amplification factor, mainly for use with concentrated plastic hinge elements (optional, default = 0).", MpcAttributeType.Boolean)
	nFactor = mka("nFactor", "Optional parameters", "Elastic stiffness amplification factor, mainly for use with concentrated plastic hinge elements (optional, default = 0).", MpcAttributeType.Real)
	nFactor.setDefault(0.0)

	# uniaxialMaterial ModIMKPinching02 tag? Ke?, alfaPos?, alfaNeg?, My_pos?, My_neg?"
	# FprPos?, FprNeg?, A_pinch?, Ls?, Ld?, La?, Lk?, Cs?, Cd?, Ca?, Ck?, thetaPpos?, thetaPneg?"
	# thetaPCpos?, thetaPCneg?, ResfacPos?, ResfacNeg?, fracDispPos?, fracDispNeg?,DPos?, DNeg?, <nFactor?>"

	xom = MpcXObjectMetaData()
	xom.name = 'ModIMKPinching02'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(Ke)
	xom.addAttribute(alfaPos)
	xom.addAttribute(alfaNeg)
	xom.addAttribute(My_pos)
	xom.addAttribute(My_neg)
	xom.addAttribute(FprPos)
	xom.addAttribute(FprNeg)
	xom.addAttribute(A_pinch)
	xom.addAttribute(Ls)
	xom.addAttribute(Ld)
	xom.addAttribute(La)
	xom.addAttribute(Lk)
	xom.addAttribute(Cs)
	xom.addAttribute(Cd)
	xom.addAttribute(Ca)
	xom.addAttribute(Ck)
	xom.addAttribute(thetaPpos)
	xom.addAttribute(thetaPneg)
	xom.addAttribute(thetaPCpos)
	xom.addAttribute(thetaPCneg)
	xom.addAttribute(ResfacPos)
	xom.addAttribute(ResfacNeg)
	xom.addAttribute(fracDispPos)
	xom.addAttribute(fracDispNeg)
	xom.addAttribute(DPos)
	xom.addAttribute(DNeg)
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

	# uniaxialMaterial ModIMKPinching02 tag? Ke?, alfaPos?, alfaNeg?, My_pos?, My_neg?"
	# FprPos?, FprNeg?, A_pinch?, Ls?, Ld?, La?, Lk?, Cs?, Cd?, Ca?, Ck?, thetaPpos?, thetaPneg?"
	# thetaPCpos?, thetaPCneg?, ResfacPos?, ResfacNeg?, fracDispPos?, fracDispNeg?,DPos?, DNeg?, <nFactor?>"

	str_tcl = '{}uniaxialMaterial ModIMKPinching02 {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}{}\n'.format(
			pinfo.indent,
			tag,
			geta("Ke").quantityScalar.value, 
			geta("alfaPos").real,
			geta("alfaNeg").real,
			geta("My_pos").quantityScalar.value,
			geta("My_neg").quantityScalar.value,
			geta("FprPos").real,
			geta("FprNeg").real,
			geta("A_pinch").real,
			geta("Ls").real,
			geta("Ld").real,
			geta("La").real,
			geta("Lk").real,
			geta("Cs").real,
			geta("Cd").real,
			geta("Ca").real,
			geta("Ck").real,
			geta("thetaPpos").real,
			geta("thetaPneg").real,
			geta("thetaPCpos").real,
			geta("thetaPCneg").real,
			geta("ResfacPos").quantityScalar.value,
			geta("ResfacNeg").quantityScalar.value,
			geta("fracDispPos").real,
			geta("fracDispNeg").real,
			geta("DPos").real,
			geta("DNeg").real,
			sopt)

	# uniaxialMaterial ModIMKPinching02 tag? Ke?, alfaPos?, alfaNeg?, My_pos?, My_neg?"
	# FprPos?, FprNeg?, A_pinch?, Ls?, Ld?, La?, Lk?, Cs?, Cd?, Ca?, Ck?, thetaPpos?, thetaPneg?"
	# thetaPCpos?, thetaPCneg?, ResfacPos?, ResfacNeg?, fracDispPos?, fracDispNeg?,DPos?, DNeg?, <nFactor?>"

	# now write the string into the file
	pinfo.out_file.write(str_tcl)