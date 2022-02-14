# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# K0
	at_K0 = MpcAttributeMetaData()
	at_K0.type = MpcAttributeType.QuantityScalar
	at_K0.name = 'K0'
	at_K0.group = 'Elasticity'
	at_K0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K0')+'<br/>') + 
		html_par('Elastic stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	at_K0.dimension = u.F/u.L**2
	
	# as_Plus
	at_asPlus = MpcAttributeMetaData()
	at_asPlus.type = MpcAttributeType.Real
	at_asPlus.name = 'as_Plus'
	at_asPlus.group = 'Non-linear'
	at_asPlus.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('as_Plus')+'<br/>') + 
		html_par('Strain hardening ratio for positive loading direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
		
	# as_Neg
	at_asNeg = MpcAttributeMetaData()
	at_asNeg.type = MpcAttributeType.Real
	at_asNeg.name = 'as_Neg'
	at_asNeg.group = 'Non-linear'
	at_asNeg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('as_Neg')+'<br/>') + 
		html_par('Strain hardening ratio for negative loading direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	# My_Plus
	at_MyPlus = MpcAttributeMetaData()
	at_MyPlus.type = MpcAttributeType.QuantityScalar
	at_MyPlus.name = 'My_Plus'
	at_MyPlus.group = 'Non-linear'
	at_MyPlus.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('My_Plus')+'<br/>') + 
		html_par('Effective yield strength for positive loading direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	at_MyPlus.dimension = u.F/u.L**2
	
	# My_Neg
	at_MyNeg = MpcAttributeMetaData()
	at_MyNeg.type = MpcAttributeType.QuantityScalar
	at_MyNeg.name = 'My_Neg'
	at_MyNeg.group = 'Non-linear'
	at_MyNeg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('My_Neg')+'<br/>') + 
		html_par('Effective yield strength for negative loading direction (negative value)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	at_MyNeg.dimension = u.F/u.L**2
	
	# Lamda_S
	at_LamdaS = MpcAttributeMetaData()
	at_LamdaS.type = MpcAttributeType.Real
	at_LamdaS.name = 'Lamda_S'
	at_LamdaS.group = 'Non-linear'
	at_LamdaS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Lamda_S')+'<br/>') + 
		html_par('Cyclic deterioration parameter for strength deterioration [E_t=Lamda_S*M_y, see Lignos and Krawinkler (2011); set Lamda_S = 0 to disable this mode of deterioration]') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
		
	# Lamda_C
	at_LamdaC = MpcAttributeMetaData()
	at_LamdaC.type = MpcAttributeType.Real
	at_LamdaC.name = 'Lamda_C'
	at_LamdaC.group = 'Non-linear'
	at_LamdaC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Lamda_C')+'<br/>') + 
		html_par('Cyclic deterioration parameter for post-capping strength deterioration [E_t=Lamda_C*M_y, see Lignos and Krawinkler (2011); set Lamda_C = 0 to disable this mode of deterioration]') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	# Lamda_A
	at_LamdaA = MpcAttributeMetaData()
	at_LamdaA.type = MpcAttributeType.Real
	at_LamdaA.name = 'Lamda_A'
	at_LamdaA.group = 'Non-linear'
	at_LamdaA.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Lamda_S')+'<br/>') + 
		html_par('Cyclic deterioration parameter for accelerated reloading stiffness deterioration [E_t=Lamda_A*M_y, see Lignos and Krawinkler (2011); set Lamda_A = 0 to disable this mode of deterioration]') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
		
	# Lamda_K
	at_LamdaK = MpcAttributeMetaData()
	at_LamdaK.type = MpcAttributeType.Real
	at_LamdaK.name = 'Lamda_K'
	at_LamdaK.group = 'Non-linear'
	at_LamdaK.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Lamda_K')+'<br/>') + 
		html_par('Cyclic deterioration parameter for unloading stiffness deterioration [E_t=Lamda_K*M_y, see Lignos and Krawinkler (2011); set Lamda_K = 0 to disable this mode of deterioration]') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	# c_S
	at_cS = MpcAttributeMetaData()
	at_cS.type = MpcAttributeType.Real
	at_cS.name = 'c_S'
	at_cS.group = 'Non-linear'
	at_cS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c_S')+'<br/>') + 
		html_par('rate of strength deterioration. The default value is 1.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	at_cS.setDefault(1.0)
	
	# c_C
	at_cC = MpcAttributeMetaData()
	at_cC.type = MpcAttributeType.Real
	at_cC.name = 'c_C'
	at_cC.group = 'Non-linear'
	at_cC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c_C')+'<br/>') + 
		html_par('Rate of post-capping strength deterioration. The default value is 1.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	at_cC.setDefault(1.0)
	
	# c_A
	at_cA = MpcAttributeMetaData()
	at_cA.type = MpcAttributeType.Real
	at_cA.name = 'c_A'
	at_cA.group = 'Non-linear'
	at_cA.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c_A')+'<br/>') + 
		html_par('Rate of accelerated reloading deterioration. The default value is 1.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	at_cA.setDefault(1.0)
	
	# c_K
	at_cK = MpcAttributeMetaData()
	at_cK.type = MpcAttributeType.Real
	at_cK.name = 'c_K'
	at_cK.group = 'Non-linear'
	at_cK.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c_K')+'<br/>') + 
		html_par('Rate of unloading stiffness deterioration. The default value is 1.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	at_cK.setDefault(1.0)
	
	# theta_p_Plus
	at_thetapPlus = MpcAttributeMetaData()
	at_thetapPlus.type = MpcAttributeType.Real
	at_thetapPlus.name = 'theta_p_Plus'
	at_thetapPlus.group = 'Non-linear'
	at_thetapPlus.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theta_p_Plus')+'<br/>') + 
		html_par('Pre-capping rotation for positive loading direction (often noted as plastic rotation capacity)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	# theta_p_Neg
	at_thetapNeg = MpcAttributeMetaData()
	at_thetapNeg.type = MpcAttributeType.Real
	at_thetapNeg.name = 'theta_p_Neg'
	at_thetapNeg.group = 'Non-linear'
	at_thetapNeg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theta_p_Neg')+'<br/>') + 
		html_par('Pre-capping rotation for negative loading direction (often noted as plastic rotation capacity) (must be defined as a positive value)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	# theta_pc_Plus
	at_thetapcPlus = MpcAttributeMetaData()
	at_thetapcPlus.type = MpcAttributeType.Real
	at_thetapcPlus.name = 'theta_pc_Plus'
	at_thetapcPlus.group = 'Non-linear'
	at_thetapcPlus.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theta_pc_Plus')+'<br/>') + 
		html_par('Post-capping rotation for positive loading direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	# theta_pc_Neg
	at_thetapcNeg = MpcAttributeMetaData()
	at_thetapcNeg.type = MpcAttributeType.Real
	at_thetapcNeg.name = 'theta_pc_Neg'
	at_thetapcNeg.group = 'Non-linear'
	at_thetapcNeg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theta_pc_Neg')+'<br/>') + 
		html_par('Post-capping rotation for negative loading direction (must be defined as a positive value)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
		
	# Res_Pos
	at_ResPos = MpcAttributeMetaData()
	at_ResPos.type = MpcAttributeType.QuantityScalar
	at_ResPos.name = 'Res_Pos'
	at_ResPos.group = 'Non-linear'
	at_ResPos.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Res_Pos')+'<br/>') + 
		html_par('Residual strength ratio for positive loading direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	at_ResPos.dimension = u.F/u.L**2
	
	# Res_Neg
	at_ResNeg = MpcAttributeMetaData()
	at_ResNeg.type = MpcAttributeType.QuantityScalar
	at_ResNeg.name = 'Res_Neg'
	at_ResNeg.group = 'Non-linear'
	at_ResNeg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Res_Neg')+'<br/>') + 
		html_par('Residual strength ratio for negative loading direction (positive value)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	at_ResNeg.dimension = u.F/u.L**2
	
	# theta_u_Plus
	at_thetauPlus = MpcAttributeMetaData()
	at_thetauPlus.type = MpcAttributeType.Real
	at_thetauPlus.name = 'theta_u_Plus'
	at_thetauPlus.group = 'Non-linear'
	at_thetauPlus.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theta_u_Plus')+'<br/>') + 
		html_par('Ultimate rotation capacity for positive loading direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	# theta_u_Neg
	at_thetauNeg = MpcAttributeMetaData()
	at_thetauNeg.type = MpcAttributeType.Real
	at_thetauNeg.name = 'theta_u_Neg'
	at_thetauNeg.group = 'Non-linear'
	at_thetauNeg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theta_u_Neg')+'<br/>') + 
		html_par('Ultimate rotation capacity for negative loading direction (positive value)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	# D_Plus
	at_DPlus = MpcAttributeMetaData()
	at_DPlus.type = MpcAttributeType.Real
	at_DPlus.name = 'D_Plus'
	at_DPlus.group = 'Non-linear'
	at_DPlus.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D_Plus')+'<br/>') + 
		html_par('Rate of cyclic deterioration in the positive loading direction (this parameter is used to create assymetric hysteretic behavior for the case of a composite beam). For symmetric hysteretic response use 1.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	# D_Neg
	at_DNeg = MpcAttributeMetaData()
	at_DNeg.type = MpcAttributeType.Real
	at_DNeg.name = 'D_Neg'
	at_DNeg.group = 'Non-linear'
	at_DNeg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D_Neg')+'<br/>') + 
		html_par('Rate of cyclic deterioration in the negative loading direction (this parameter is used to create assymetric hysteretic behavior for the case of a composite beam). For symmetric hysteretic response use 1.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Peak-Oriented_Hysteretic_Response_(ModIMKPeakOriented_Material)','ModIMKPeakOriented Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ModIMKPeakOriented'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_K0)
	xom.addAttribute(at_asPlus)
	xom.addAttribute(at_asNeg)
	xom.addAttribute(at_MyPlus)
	xom.addAttribute(at_MyNeg)
	xom.addAttribute(at_LamdaS)
	xom.addAttribute(at_LamdaC)
	xom.addAttribute(at_LamdaA)
	xom.addAttribute(at_LamdaK)
	xom.addAttribute(at_cS)
	xom.addAttribute(at_cC)
	xom.addAttribute(at_cA)
	xom.addAttribute(at_cK)
	xom.addAttribute(at_thetapPlus)
	xom.addAttribute(at_thetapNeg)
	xom.addAttribute(at_thetapcPlus)
	xom.addAttribute(at_thetapcNeg)
	xom.addAttribute(at_ResPos)
	xom.addAttribute(at_ResNeg)
	xom.addAttribute(at_thetauPlus)
	xom.addAttribute(at_thetauNeg)
	xom.addAttribute(at_DPlus)
	xom.addAttribute(at_DNeg)

	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ModIMKPeakOriented $matTag $K0 $as_Plus $as_Neg $My_Plus $My_Neg
	#$Lamda_S $Lamda_C $Lamda_A $Lamda_K $c_S $c_C $c_A $c_K $theta_p_Plus $theta_p_Neg
	#$theta_pc_Plus $theta_pc_Neg $Res_Pos $Res_Neg $theta_u_Plus $theta_u_Neg $D_Plus $D_Neg
	
	xobj = pinfo.phys_prop.XObject	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	K0_at = xobj.getAttribute('K0')
	if(K0_at is None):
		raise Exception('Error: cannot find "K0" attribute')
	K0 = K0_at.quantityScalar
	
	as_Plus_at = xobj.getAttribute('as_Plus')
	if(as_Plus_at is None):
		raise Exception('Error: cannot find "as_Plus" attribute')
	as_Plus = as_Plus_at.real
	
	as_Neg_at = xobj.getAttribute('as_Neg')
	if(as_Neg_at is None):
		raise Exception('Error: cannot find "as_Neg" attribute')
	as_Neg = as_Neg_at.real
	
	My_Plus_at = xobj.getAttribute('My_Plus')
	if(My_Plus_at is None):
		raise Exception('Error: cannot find "My_Plus" attribute')
	My_Plus = My_Plus_at.quantityScalar
	
	My_Neg_at = xobj.getAttribute('My_Neg')
	if(My_Neg_at is None):
		raise Exception('Error: cannot find "My_Neg" attribute')
	My_Neg = My_Neg_at.quantityScalar
	
	Lamda_S_at = xobj.getAttribute('Lamda_S')
	if(Lamda_S_at is None):
		raise Exception('Error: cannot find "Lamda_S" attribute')
	Lamda_S = Lamda_S_at.real
	
	Lamda_C_at = xobj.getAttribute('Lamda_C')
	if(Lamda_C_at is None):
		raise Exception('Error: cannot find "Lamda_C" attribute')
	Lamda_C = Lamda_C_at.real
	
	Lamda_A_at = xobj.getAttribute('Lamda_A')
	if(Lamda_A_at is None):
		raise Exception('Error: cannot find "Lamda_A" attribute')
	Lamda_A = Lamda_A_at.real
	
	Lamda_K_at = xobj.getAttribute('Lamda_K')
	if(Lamda_K_at is None):
		raise Exception('Error: cannot find "Lamda_K" attribute')
	Lamda_K = Lamda_K_at.real
	
	c_S_at = xobj.getAttribute('c_S')
	if(c_S_at is None):
		raise Exception('Error: cannot find "c_S" attribute')
	c_S = c_S_at.real
	
	c_C_at = xobj.getAttribute('c_C')
	if(c_C_at is None):
		raise Exception('Error: cannot find "c_C" attribute')
	c_C = c_C_at.real
	
	c_A_at = xobj.getAttribute('c_A')
	if(c_A_at is None):
		raise Exception('Error: cannot find "c_A" attribute')
	c_A = c_A_at.real
	
	c_K_at = xobj.getAttribute('c_K')
	if(c_K_at is None):
		raise Exception('Error: cannot find "c_K" attribute')
	c_K = c_K_at.real
	
	theta_p_Plus_at = xobj.getAttribute('theta_p_Plus')
	if(theta_p_Plus_at is None):
		raise Exception('Error: cannot find "theta_p_Plus" attribute')
	theta_p_Plus = theta_p_Plus_at.real
	
	theta_p_Neg_at = xobj.getAttribute('theta_p_Neg')
	if(theta_p_Neg_at is None):
		raise Exception('Error: cannot find "theta_p_Neg" attribute')
	theta_p_Neg = theta_p_Neg_at.real
	
	theta_pc_Plus_at = xobj.getAttribute('theta_pc_Plus')
	if(theta_pc_Plus_at is None):
		raise Exception('Error: cannot find "theta_pc_Plus" attribute')
	theta_pc_Plus = theta_pc_Plus_at.real
	
	theta_pc_Neg_at = xobj.getAttribute('theta_pc_Neg')
	if(theta_pc_Neg_at is None):
		raise Exception('Error: cannot find "theta_pc_Neg" attribute')
	theta_pc_Neg = theta_pc_Neg_at.real
	
	Res_Pos_at = xobj.getAttribute('Res_Pos')
	if(Res_Pos_at is None):
		raise Exception('Error: cannot find "Res_Pos" attribute')
	Res_Pos = Res_Pos_at.quantityScalar
	
	Res_Neg_at = xobj.getAttribute('Res_Neg')
	if(Res_Neg_at is None):
		raise Exception('Error: cannot find "Res_Neg" attribute')
	Res_Neg = Res_Neg_at.quantityScalar
	
	theta_u_Plus_at = xobj.getAttribute('theta_u_Plus')
	if(theta_u_Plus_at is None):
		raise Exception('Error: cannot find "theta_u_Plus" attribute')
	theta_u_Plus = theta_u_Plus_at.real
	
	theta_u_Neg_at = xobj.getAttribute('theta_u_Neg')
	if(theta_u_Neg_at is None):
		raise Exception('Error: cannot find "theta_u_Neg" attribute')
	theta_u_Neg = theta_u_Neg_at.real
	
	D_Plus_at = xobj.getAttribute('D_Plus')
	if(D_Plus_at is None):
		raise Exception('Error: cannot find "D_Plus" attribute')
	D_Plus = D_Plus_at.real
	
	D_Neg_at = xobj.getAttribute('D_Neg')
	if(D_Neg_at is None):
		raise Exception('Error: cannot find "D_Neg" attribute')
	D_Neg = D_Neg_at.real
	
	
	str_tcl = '{}uniaxialMaterial ModIMKPeakOriented {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, K0.value, as_Plus, as_Neg, My_Plus.value, My_Neg.value, Lamda_S, Lamda_C, Lamda_A, Lamda_K, c_S, c_C, c_A,
			c_K, theta_p_Plus, theta_p_Neg,theta_pc_Plus, theta_pc_Neg, Res_Pos.value, Res_Neg.value, theta_u_Plus, theta_u_Neg, D_Plus, D_Neg)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)