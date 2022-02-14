# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	#MODE 1: Direct Input
	
	# nodeT
	at_nodeT = MpcAttributeMetaData()
	at_nodeT.type = MpcAttributeType.Index
	at_nodeT.name = 'nodeT'
	at_nodeT.group = 'Mode_1'
	at_nodeT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nodeT')+'<br/>') + 
		html_par('integer node tag to define the first node at the extreme end of the associated flexural frame member (L3 or D5 in Figure)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# nodeB
	at_nodeB = MpcAttributeMetaData()
	at_nodeB.type = MpcAttributeType.Index
	at_nodeB.name = 'nodeB'
	at_nodeB.group = 'Mode_1'
	at_nodeB.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nodeB')+'<br/>') + 
		html_par('integer node tag to define the last node at the extreme end of the associated flexural frame member (L2 or D2 in Figure)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# driftAxis
	at_driftAxis = MpcAttributeMetaData()
	at_driftAxis.type = MpcAttributeType.Integer
	at_driftAxis.name = 'driftAxis'
	at_driftAxis.group = 'Mode_1'
	at_driftAxis.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('driftAxis')+'<br/>') + 
		html_par('integer to indicate the drift axis in which lateral-strength degradation will occur. This axis should be orthogonal to the axis of measured rotation (see rotAxis in Rotation Shear Curve definition)') +
		html_par('driftAxis = 1 – Drift along the x-axis') +
		html_par('driftAxis = 2 – Drift along the y-axis') +
		html_par('driftAxis = 3 – Drift along the z-axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	at_driftAxis.sourceType = MpcAttributeSourceType.List
	at_driftAxis.setSourceList([1, 2, 3])
	at_driftAxis.setDefault(1)
	
	# Kelas
	at_Kelas = MpcAttributeMetaData()
	at_Kelas.type = MpcAttributeType.QuantityScalar
	at_Kelas.name = 'Kelas'
	at_Kelas.group = 'Mode_1'
	at_Kelas.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kelas')+'<br/>') + 
		html_par('floating point value to define the initial material elastic stiffness (Kelastic); Kelas > 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	at_Kelas.dimension = u.F/u.L
	
	# crvTyp
	at_crvTyp = MpcAttributeMetaData()
	at_crvTyp.type = MpcAttributeType.Integer
	at_crvTyp.name = 'crvTyp'
	at_crvTyp.group = 'Mode_1'
	at_crvTyp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('crvTyp')+'<br/>') + 
		html_par('integer flag to indicate the type of limit curve associated with this material.') +
		html_par('crvTyp = 0 – No limit curve') +
		html_par('crvTyp = 1 – axial limit curve') +
		html_par('crvTyp = 2 – ' + html_href('http://opensees.berkeley.edu/wiki/index.php/RotationShearCurve','RotationShearCurve')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	at_crvTyp.sourceType = MpcAttributeSourceType.List
	at_crvTyp.setSourceList([0, 1, 2])
	at_crvTyp.setDefault(0)
	
	# crvTag
	at_crvTag = MpcAttributeMetaData()
	at_crvTag.type = MpcAttributeType.Index
	at_crvTag.name = 'crvTag'
	at_crvTag.group = 'Mode_1'
	at_crvTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('crvTag')+'<br/>') + 
		html_par('integer tag for the unique limit curve object associated with this material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# YpinchUPN
	at_YpinchUPN = MpcAttributeMetaData()
	at_YpinchUPN.type = MpcAttributeType.Real
	at_YpinchUPN.name = 'YpinchUPN'
	at_YpinchUPN.group = 'Mode_1'
	at_YpinchUPN.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('YpinchUPN')+'<br/>') + 
		html_par('floating point unloading force pinching factor for loading in the negative direction. Note: This value must be between zero and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# YpinchRPN
	at_YpinchRPN = MpcAttributeMetaData()
	at_YpinchRPN.type = MpcAttributeType.Real
	at_YpinchRPN.name = 'YpinchRPN'
	at_YpinchRPN.group = 'Mode_1'
	at_YpinchRPN.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('YpinchRPN')+'<br/>') + 
		html_par('floating point reloading force pinching factor for loading in the negative direction. Note: This value must be between negative one and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# XpinchRPN
	at_XpinchRPN = MpcAttributeMetaData()
	at_XpinchRPN.type = MpcAttributeType.Real
	at_XpinchRPN.name = 'XpinchRPN'
	at_XpinchRPN.group = 'Mode_1'
	at_XpinchRPN.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('XpinchRPN')+'<br/>') + 
		html_par('floating point reloading displacement pinching factor for loading in the negative direction. Note: This value must be between negative one and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# YpinchUNP
	at_YpinchUNP = MpcAttributeMetaData()
	at_YpinchUNP.type = MpcAttributeType.Real
	at_YpinchUNP.name = 'YpinchUNP'
	at_YpinchUNP.group = 'Mode_1'
	at_YpinchUNP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('YpinchUNP')+'<br/>') + 
		html_par('floating point unloading force pinching factor for loading in the positive direction. Note: This value must be between zero and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# YpinchRNP
	at_YpinchRNP = MpcAttributeMetaData()
	at_YpinchRNP.type = MpcAttributeType.Real
	at_YpinchRNP.name = 'YpinchRNP'
	at_YpinchRNP.group = 'Mode_1'
	at_YpinchRNP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('YpinchRNP')+'<br/>') + 
		html_par('floating point reloading force pinching factor for loading in the positive direction. Note: This value must be between negative one and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# XpinchRNP
	at_XpinchRNP = MpcAttributeMetaData()
	at_XpinchRNP.type = MpcAttributeType.Real
	at_XpinchRNP.name = 'XpinchRNP'
	at_XpinchRNP.group = 'Mode_1'
	at_XpinchRNP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('XpinchRNP')+'<br/>') + 
		html_par('floating point reloading displacement pinching factor for loading in the positive direction. Note: This value must be between negative one and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgStrsLimE
	at_dmgStrsLimE = MpcAttributeMetaData()
	at_dmgStrsLimE.type = MpcAttributeType.Real
	at_dmgStrsLimE.name = 'dmgStrsLimE'
	at_dmgStrsLimE.group = 'Mode_1'
	at_dmgStrsLimE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgStrsLimE')+'<br/>') + 
		html_par('floating point force limit for elastic stiffness damage (typically defined as the lowest of shear strength or shear at flexrual yielding).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgDispMax
	at_dmgDispMax = MpcAttributeMetaData()
	at_dmgDispMax.type = MpcAttributeType.Real
	at_dmgDispMax.name = 'dmgDispMax'
	at_dmgDispMax.group = 'Mode_1'
	at_dmgDispMax.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgDispMax')+'<br/>') + 
		html_par('This value is used to compute the maximum deformation at flexural yield (δmax Eq. 1) and using the initial elastic stiffness (Kelastic) the monotonic energy (Emono Eq. 1) to yield. Input 1 if this type of damage is not required and set dmgE1, dmgE2, dmgE3, dmgE4, and dmgELim to zero floating point for ultimate drift at failure (δmax Eq. 1) and is used for strength and stiffness damage.') +
		html_par('This value is used to compute the monotonic energy at axial failure (Emono Eq. 2) by computing the area under the backbone in the positive loading direction up to δmax. Input 1 if this type of damage is not required and set dmgR1, dmgR2, dmgR3, dmgR4, and dmgRLim to zero for reloading stiffness damage. Similarly set dmgS1, dmgS2, dmgS3, dmgS4, and dmgSLim to zero if reloading strength damage is not required') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgE1
	at_dmgE1 = MpcAttributeMetaData()
	at_dmgE1.type = MpcAttributeType.Real
	at_dmgE1.name = 'dmgE1'
	at_dmgE1.group = 'Mode_1'
	at_dmgE1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgE1')+'<br/>') + 
		html_par('floating point elastic stiffness damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgE2
	at_dmgE2 = MpcAttributeMetaData()
	at_dmgE2.type = MpcAttributeType.Real
	at_dmgE2.name = 'dmgE2'
	at_dmgE2.group = 'Mode_1'
	at_dmgE2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgE2')+'<br/>') + 
		html_par('floating point elastic stiffness damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgE3
	at_dmgE3 = MpcAttributeMetaData()
	at_dmgE3.type = MpcAttributeType.Real
	at_dmgE3.name = 'dmgE3'
	at_dmgE3.group = 'Mode_1'
	at_dmgE3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgE3')+'<br/>') + 
		html_par('floating point elastic stiffness damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgE4
	at_dmgE4 = MpcAttributeMetaData()
	at_dmgE4.type = MpcAttributeType.Real
	at_dmgE4.name = 'dmgE4'
	at_dmgE4.group = 'Mode_1'
	at_dmgE4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgE4')+'<br/>') + 
		html_par('floating point elastic stiffness damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgELim
	at_dmgELim = MpcAttributeMetaData()
	at_dmgELim.type = MpcAttributeType.Real
	at_dmgELim.name = 'dmgELim'
	at_dmgELim.group = 'Mode_1'
	at_dmgELim.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgELim')+'<br/>') + 
		html_par('floating point elastic stiffness damage limit Dlim shown in Eq. 1; Note: This value must be between zero and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgR1
	at_dmgR1 = MpcAttributeMetaData()
	at_dmgR1.type = MpcAttributeType.Real
	at_dmgR1.name = 'dmgR1'
	at_dmgR1.group = 'Mode_1'
	at_dmgR1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgR1')+'<br/>') + 
		html_par('floating point reloading stiffness damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgR2
	at_dmgR2 = MpcAttributeMetaData()
	at_dmgR2.type = MpcAttributeType.Real
	at_dmgR2.name = 'dmgR2'
	at_dmgR2.group = 'Mode_1'
	at_dmgR2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgR2')+'<br/>') + 
		html_par('floating point reloading stiffness damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgR3
	at_dmgR3 = MpcAttributeMetaData()
	at_dmgR3.type = MpcAttributeType.Real
	at_dmgR3.name = 'dmgR3'
	at_dmgR3.group = 'Mode_1'
	at_dmgR3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgR3')+'<br/>') + 
		html_par('floating point reloading stiffness damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgR4
	at_dmgR4 = MpcAttributeMetaData()
	at_dmgR4.type = MpcAttributeType.Real
	at_dmgR4.name = 'dmgR4'
	at_dmgR4.group = 'Mode_1'
	at_dmgR4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgR4')+'<br/>') + 
		html_par('floating point reloading stiffness damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgRLim
	at_dmgRLim = MpcAttributeMetaData()
	at_dmgRLim.type = MpcAttributeType.Real
	at_dmgRLim.name = 'dmgRLim'
	at_dmgRLim.group = 'Mode_1'
	at_dmgRLim.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgRLim')+'<br/>') + 
		html_par('floating point elastic stiffness damage limit Dlim shown in Eq. 1; Note: This value must be between zero and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgRCyc
	at_dmgRCyc = MpcAttributeMetaData()
	at_dmgRCyc.type = MpcAttributeType.Real
	at_dmgRCyc.name = 'dmgRCyc'
	at_dmgRCyc.group = 'Mode_1'
	at_dmgRCyc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgRCyc')+'<br/>') + 
		html_par('floating point cyclic reloading stiffness damage index; Note: This value must be between zero and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgS1
	at_dmgS1 = MpcAttributeMetaData()
	at_dmgS1.type = MpcAttributeType.Real
	at_dmgS1.name = 'dmgS1'
	at_dmgS1.group = 'Mode_1'
	at_dmgS1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgS1')+'<br/>') + 
		html_par('floating point backbone strength damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgS2
	at_dmgS2 = MpcAttributeMetaData()
	at_dmgS2.type = MpcAttributeType.Real
	at_dmgS2.name = 'dmgS2'
	at_dmgS2.group = 'Mode_1'
	at_dmgS2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgS2')+'<br/>') + 
		html_par('floating point backbone strength damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgS3
	at_dmgS3 = MpcAttributeMetaData()
	at_dmgS3.type = MpcAttributeType.Real
	at_dmgS3.name = 'dmgS3'
	at_dmgS3.group = 'Mode_1'
	at_dmgS3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgS3')+'<br/>') + 
		html_par('floating point backbone strength damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgS4
	at_dmgS4 = MpcAttributeMetaData()
	at_dmgS4.type = MpcAttributeType.Real
	at_dmgS4.name = 'dmgS4'
	at_dmgS4.group = 'Mode_1'
	at_dmgS4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgS4')+'<br/>') + 
		html_par('floating point backbone strength damage factors α1,α2,α3,α4 shown in Eq. 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgSLim
	at_dmgSLim = MpcAttributeMetaData()
	at_dmgSLim.type = MpcAttributeType.Real
	at_dmgSLim.name = 'dmgSLim'
	at_dmgSLim.group = 'Mode_1'
	at_dmgSLim.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgSLim')+'<br/>') + 
		html_par('floating point backbone strength damage limit Dlim shown in Eq. 1; Note: This value must be between zero and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	# dmgSCyc
	at_dmgSCyc = MpcAttributeMetaData()
	at_dmgSCyc.type = MpcAttributeType.Real
	at_dmgSCyc.name = 'dmgSCyc'
	at_dmgSCyc.group = 'Mode_1'
	at_dmgSCyc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgSCyc')+'<br/>') + 
		html_par('floating point cyclic backbone strength damage index; Note: This value must be between zero and unity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching_Limit_State_Material','Pinching Limit State Material')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'PinchingLimitStateMaterial'
	xom.Xgroup = 'Other Uniaxial Materials'
	#Mode_1
	xom.addAttribute(at_nodeT)
	xom.addAttribute(at_nodeB)
	xom.addAttribute(at_driftAxis)
	xom.addAttribute(at_Kelas)
	xom.addAttribute(at_crvTyp)
	xom.addAttribute(at_crvTag)
	xom.addAttribute(at_YpinchUPN)
	xom.addAttribute(at_YpinchRPN)
	xom.addAttribute(at_XpinchRPN)
	xom.addAttribute(at_YpinchUNP)
	xom.addAttribute(at_YpinchRNP)
	xom.addAttribute(at_XpinchRNP)
	xom.addAttribute(at_dmgStrsLimE)
	xom.addAttribute(at_dmgDispMax)
	xom.addAttribute(at_dmgE1)
	xom.addAttribute(at_dmgE2)
	xom.addAttribute(at_dmgE3)
	xom.addAttribute(at_dmgE4)
	xom.addAttribute(at_dmgELim)
	xom.addAttribute(at_dmgR1)
	xom.addAttribute(at_dmgR2)
	xom.addAttribute(at_dmgR3)
	xom.addAttribute(at_dmgR4)
	xom.addAttribute(at_dmgRLim)
	xom.addAttribute(at_dmgRCyc)
	xom.addAttribute(at_dmgS1)
	xom.addAttribute(at_dmgS2)
	xom.addAttribute(at_dmgS3)
	xom.addAttribute(at_dmgS4)
	xom.addAttribute(at_dmgSLim)
	xom.addAttribute(at_dmgSCyc)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial PinchingLimitStateMaterial $matTag $nodeT $nodeB $driftAxis $Kelas $crvTyp $crvTag $YpinchUPN
	#$YpinchRPN $XpinchRPN $YpinchUNP $YpinchRNP $XpinchRNP $dmgStrsLimE $dmgDispMax $dmgE1 $dmgE2 $dmgE3 $dmgE4
	#$dmgELim $dmgR1 $dmgR2 $dmgR3 $dmgR4 $dmgRLim $dmgRCyc $dmgS1 $dmgS2 $dmgS3 $dmgS4 $dmgSLim $dmgSCyc
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	nodeT_at = xobj.getAttribute('nodeT')
	if(nodeT_at is None):
		raise Exception('Error: cannot find "nodeT" attribute')
	nodeT = nodeT_at.index
	
	nodeB_at = xobj.getAttribute('nodeB')
	if(nodeB_at is None):
		raise Exception('Error: cannot find "nodeB" attribute')
	nodeB = nodeB_at.index
	
	driftAxis_at = xobj.getAttribute('driftAxis')
	if(driftAxis_at is None):
		raise Exception('Error: cannot find "driftAxis" attribute')
	driftAxis = driftAxis_at.integer
	
	Kelas_at = xobj.getAttribute('Kelas')
	if(Kelas_at is None):
		raise Exception('Error: cannot find "Kelas" attribute')
	Kelas = Kelas_at.quantityScalar
	
	crvTyp_at = xobj.getAttribute('crvTyp')
	if(crvTyp_at is None):
		raise Exception('Error: cannot find "crvTyp" attribute')
	crvTyp = crvTyp_at.integer
	
	crvTag_at = xobj.getAttribute('crvTag')
	if(crvTag_at is None):
		raise Exception('Error: cannot find "crvTag" attribute')
	crvTag = crvTag_at.index
	
	YpinchUPN_at = xobj.getAttribute('YpinchUPN')
	if(YpinchUPN_at is None):
		raise Exception('Error: cannot find "YpinchUPN" attribute')
	YpinchUPN = YpinchUPN_at.real
	
	YpinchRPN_at = xobj.getAttribute('YpinchRPN')
	if(YpinchRPN_at is None):
		raise Exception('Error: cannot find "YpinchRPN" attribute')
	YpinchRPN = YpinchRPN_at.real
	
	XpinchRPN_at = xobj.getAttribute('XpinchRPN')
	if(XpinchRPN_at is None):
		raise Exception('Error: cannot find "XpinchRPN" attribute')
	XpinchRPN = XpinchRPN_at.real
	
	YpinchUNP_at = xobj.getAttribute('YpinchUNP')
	if(YpinchUNP_at is None):
		raise Exception('Error: cannot find "YpinchUNP" attribute')
	YpinchUNP = YpinchUNP_at.real
	
	YpinchRNP_at = xobj.getAttribute('YpinchRNP')
	if(YpinchRNP_at is None):
		raise Exception('Error: cannot find "YpinchRNP" attribute')
	YpinchRNP = YpinchRNP_at.real
	
	XpinchRNP_at = xobj.getAttribute('XpinchRNP')
	if(XpinchRNP_at is None):
		raise Exception('Error: cannot find "XpinchRNP" attribute')
	XpinchRNP = XpinchRNP_at.real
	
	dmgStrsLimE_at = xobj.getAttribute('dmgStrsLimE')
	if(dmgStrsLimE_at is None):
		raise Exception('Error: cannot find "dmgStrsLimE" attribute')
	dmgStrsLimE = dmgStrsLimE_at.real
	
	dmgDispMax_at = xobj.getAttribute('dmgDispMax')
	if(dmgDispMax_at is None):
		raise Exception('Error: cannot find "dmgDispMax" attribute')
	dmgDispMax = dmgDispMax_at.real
	
	dmgE1_at = xobj.getAttribute('dmgE1')
	if(dmgE1_at is None):
		raise Exception('Error: cannot find "dmgE1" attribute')
	dmgE1 = dmgE1_at.real
	
	dmgE2_at = xobj.getAttribute('dmgE2')
	if(dmgE2_at is None):
		raise Exception('Error: cannot find "dmgE2" attribute')
	dmgE2 = dmgE2_at.real
	
	dmgE3_at = xobj.getAttribute('dmgE3')
	if(dmgE3_at is None):
		raise Exception('Error: cannot find "dmgE3" attribute')
	dmgE3 = dmgE3_at.real
	
	dmgE4_at = xobj.getAttribute('dmgE4')
	if(dmgE4_at is None):
		raise Exception('Error: cannot find "dmgE4" attribute')
	dmgE4 = dmgE4_at.real
	
	dmgELim_at = xobj.getAttribute('dmgELim')
	if(dmgELim_at is None):
		raise Exception('Error: cannot find "dmgELim" attribute')
	dmgELim = dmgELim_at.real
	
	dmgR1_at = xobj.getAttribute('dmgR1')
	if(dmgR1_at is None):
		raise Exception('Error: cannot find "dmgR1" attribute')
	dmgR1 = dmgR1_at.real
	
	dmgR2_at = xobj.getAttribute('dmgR2')
	if(dmgR2_at is None):
		raise Exception('Error: cannot find "dmgR2" attribute')
	dmgR2 = dmgR2_at.real
	
	dmgR3_at = xobj.getAttribute('dmgR3')
	if(dmgR3_at is None):
		raise Exception('Error: cannot find "dmgR3" attribute')
	dmgR3 = dmgR3_at.real
	
	dmgR4_at = xobj.getAttribute('dmgR4')
	if(dmgR4_at is None):
		raise Exception('Error: cannot find "dmgR4" attribute')
	dmgR4 = dmgR4_at.real
	
	dmgRLim_at = xobj.getAttribute('dmgRLim')
	if(dmgRLim_at is None):
		raise Exception('Error: cannot find "dmgRLim" attribute')
	dmgRLim = dmgRLim_at.real
	
	dmgRCyc_at = xobj.getAttribute('dmgRCyc')
	if(dmgRCyc_at is None):
		raise Exception('Error: cannot find "dmgRCyc" attribute')
	dmgRCyc = dmgRCyc_at.real
	
	dmgS1_at = xobj.getAttribute('dmgS1')
	if(dmgS1_at is None):
		raise Exception('Error: cannot find "dmgS1" attribute')
	dmgS1 = dmgS1_at.real
	
	dmgS2_at = xobj.getAttribute('dmgS2')
	if(dmgS2_at is None):
		raise Exception('Error: cannot find "dmgS2" attribute')
	dmgS2 = dmgS2_at.real
	
	dmgS3_at = xobj.getAttribute('dmgS3')
	if(dmgS3_at is None):
		raise Exception('Error: cannot find "dmgS3" attribute')
	dmgS3 = dmgS3_at.real
	
	dmgS4_at = xobj.getAttribute('dmgS4')
	if(dmgS4_at is None):
		raise Exception('Error: cannot find "dmgS4" attribute')
	dmgS4 = dmgS4_at.real
	
	dmgSLim_at = xobj.getAttribute('dmgSLim')
	if(dmgSLim_at is None):
		raise Exception('Error: cannot find "dmgSLim" attribute')
	dmgSLim = dmgSLim_at.real
	
	dmgSCyc_at = xobj.getAttribute('dmgSCyc')
	if(dmgSCyc_at is None):
		raise Exception('Error: cannot find "dmgSCyc" attribute')
	dmgSCyc = dmgSCyc_at.real
	
	
	str_tcl = '{}uniaxialMaterial PinchingLimitStateMaterial {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, nodeT, nodeB, driftAxis, Kelas.value, crvTyp, crvTag, YpinchUPN, YpinchRPN, XpinchRPN, YpinchUNP, YpinchRNP, XpinchRNP, dmgStrsLimE,
			dmgDispMax, dmgE1, dmgE2, dmgE3, dmgE4, dmgELim, dmgR1, dmgR2, dmgR3, dmgR4, dmgRLim, dmgRCyc, dmgS1, dmgS2, dmgS3, dmgS4, dmgSLim, dmgSCyc)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)