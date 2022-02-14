# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# F0
	at_F0 = MpcAttributeMetaData()
	at_F0.type = MpcAttributeType.QuantityScalar
	at_F0.name = 'F0'
	at_F0.group = 'Non-linear'
	at_F0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('F0')+'<br/>') + 
		html_par('Intercept strength of the shear wall spring element for the asymtotic line to the envelope curve F0 > FI > 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	at_F0.dimension = u.F
	
	# FI
	at_FI = MpcAttributeMetaData()
	at_FI.type = MpcAttributeType.QuantityScalar
	at_FI.name = 'FI'
	at_FI.group = 'Non-linear'
	at_FI.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('FI')+'<br/>') + 
		html_par('Intercept strength of the spring element for the pinching branch of the hysteretic curve. (FI > 0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	at_FI.dimension = u.F
	
	# DU
	at_DU = MpcAttributeMetaData()
	at_DU.type = MpcAttributeType.QuantityScalar
	at_DU.name = 'DU'
	at_DU.group = 'Non-linear'
	at_DU.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('DU')+'<br/>') + 
		html_par('Spring element displacement at ultimate load. (DU > 0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	at_DU.dimension = u.L
	
	# S0
	at_S0 = MpcAttributeMetaData()
	at_S0.type = MpcAttributeType.QuantityScalar
	at_S0.name = 'S0'
	at_S0.group = 'Non-linear'
	at_S0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('S0')+'<br/>') + 
		html_par('Initial stiffness of the shear wall spring element (S0 > 0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	at_S0.dimension = u.F/u.L**2
	
	# R1
	at_R1 = MpcAttributeMetaData()
	at_R1.type = MpcAttributeType.Real
	at_R1.name = 'R1'
	at_R1.group = 'Non-linear'
	at_R1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R1')+'<br/>') + 
		html_par('Stiffness ratio of the asymptotic line to the spring element envelope curve. The slope of this line is R1 S0. (0 < R1 < 1.0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	
	# R2
	at_R2 = MpcAttributeMetaData()
	at_R2.type = MpcAttributeType.Real
	at_R2.name = 'R2'
	at_R2.group = 'Non-linear'
	at_R2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R2')+'<br/>') + 
		html_par('Stiffness ratio of the descending branch of the spring element envelope curve. The slope of this line is R2 S0. ( R2 < 0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	
	# R3
	at_R3 = MpcAttributeMetaData()
	at_R3.type = MpcAttributeType.Real
	at_R3.name = 'R3'
	at_R3.group = 'Non-linear'
	at_R3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R3')+'<br/>') + 
		html_par('Stiffness ratio of the unloading branch off the spring element envelope curve. The slope of this line is R3 S0. ( R3 1).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	
	# R4
	at_R4 = MpcAttributeMetaData()
	at_R4.type = MpcAttributeType.Real
	at_R4.name = 'R4'
	at_R4.group = 'Non-linear'
	at_R4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R4')+'<br/>') + 
		html_par('Stiffness ratio of the pinching branch for the spring element. The slope of this line is R4 S0. ( R4 > 0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Non-linear'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('Stiffness degradation parameter for the shear wall spring element. (ALPHA > 0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'Non-linear'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') + 
		html_par('Stiffness degradation parameter for the spring element. (BETA > 0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SAWS_Material','SAWS Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'SAWS'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_F0)
	xom.addAttribute(at_FI)
	xom.addAttribute(at_DU)
	xom.addAttribute(at_S0)
	xom.addAttribute(at_R1)
	xom.addAttribute(at_R2)
	xom.addAttribute(at_R3)
	xom.addAttribute(at_R4)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_beta)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial SAWS $tag $F0 $FI $DU $S0 $R1 $R2 $R3 $R4 $alph $beta
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	F0_at = xobj.getAttribute('F0')
	if(F0_at is None):
		raise Exception('Error: cannot find "F0" attribute')
	F0 = F0_at.quantityScalar
	
	FI_at = xobj.getAttribute('FI')
	if(FI_at is None):
		raise Exception('Error: cannot find "FI" attribute')
	FI = FI_at.quantityScalar
	
	DU_at = xobj.getAttribute('DU')
	if(DU_at is None):
		raise Exception('Error: cannot find "DU" attribute')
	DU = DU_at.quantityScalar
	
	S0_at = xobj.getAttribute('S0')
	if(S0_at is None):
		raise Exception('Error: cannot find "S0" attribute')
	S0 = S0_at.quantityScalar
	
	R1_at = xobj.getAttribute('R1')
	if(R1_at is None):
		raise Exception('Error: cannot find "R1" attribute')
	R1 = R1_at.real
	
	R2_at = xobj.getAttribute('R2')
	if(R2_at is None):
		raise Exception('Error: cannot find "R2" attribute')
	R2 = R2_at.real
	
	R3_at = xobj.getAttribute('R3')
	if(R3_at is None):
		raise Exception('Error: cannot find "R3" attribute')
	R3 = R3_at.real
	
	R4_at = xobj.getAttribute('R4')
	if(R4_at is None):
		raise Exception('Error: cannot find "R4" attribute')
	R4 = R4_at.real
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	beta_at = xobj.getAttribute('beta')
	if(beta_at is None):
		raise Exception('Error: cannot find "beta" attribute')
	beta = beta_at.real
	
	
	str_tcl = '{}uniaxialMaterial SAWS {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, F0.value, FI.value, DU.value, S0.value, R1, R2, R3, R4, alpha, beta)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)