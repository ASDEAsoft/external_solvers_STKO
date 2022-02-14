# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# ePf1
	at_ePf1 = MpcAttributeMetaData()
	at_ePf1.type = MpcAttributeType.Real
	at_ePf1.name = 'ePf1'
	at_ePf1.group = 'Non-linear'
	at_ePf1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ePf1')+'<br/>') + 
		html_par('floating point value defining force points on the positive response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# ePf2
	at_ePf2 = MpcAttributeMetaData()
	at_ePf2.type = MpcAttributeType.Real
	at_ePf2.name = 'ePf2'
	at_ePf2.group = 'Non-linear'
	at_ePf2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ePf2')+'<br/>') + 
		html_par('floating point value defining force points on the positive response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# ePf3
	at_ePf3 = MpcAttributeMetaData()
	at_ePf3.type = MpcAttributeType.Real
	at_ePf3.name = 'ePf3'
	at_ePf3.group = 'Non-linear'
	at_ePf3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ePf3')+'<br/>') + 
		html_par('floating point value defining force points on the positive response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# ePf4
	at_ePf4 = MpcAttributeMetaData()
	at_ePf4.type = MpcAttributeType.Real
	at_ePf4.name = 'ePf4'
	at_ePf4.group = 'Non-linear'
	at_ePf4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ePf4')+'<br/>') + 
		html_par('floating point value defining force points on the positive response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# ePd1
	at_ePd1 = MpcAttributeMetaData()
	at_ePd1.type= MpcAttributeType.Real
	at_ePd1.name= 'ePd1'
	at_ePd1.group= 'Non-linear'
	at_ePd1.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('ePd1')+'<br/>') + 
		html_par('floating point value defining deformation points on the positive response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# ePd2
	at_ePd2 = MpcAttributeMetaData()
	at_ePd2.type= MpcAttributeType.Real
	at_ePd2.name= 'ePd2'
	at_ePd2.group= 'Non-linear'
	at_ePd2.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('ePd2')+'<br/>') + 
		html_par('floating point value defining deformation points on the positive response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# ePd3
	at_ePd3 = MpcAttributeMetaData()
	at_ePd3.type= MpcAttributeType.Real
	at_ePd3.name= 'ePd3'
	at_ePd3.group= 'Non-linear'
	at_ePd3.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('ePd3')+'<br/>') + 
		html_par('floating point value defining deformation points on the positive response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# ePd4
	at_ePd4 = MpcAttributeMetaData()
	at_ePd4.type= MpcAttributeType.Real
	at_ePd4.name= 'ePd4'
	at_ePd4.group= 'Non-linear'
	at_ePd4.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('ePd4')+'<br/>') + 
		html_par('floating point value defining deformation points on the positive response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type= MpcAttributeType.Boolean
	at_Optional.name= 'Optional'
	at_Optional.group= 'Non-linear'
	at_Optional.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# eNf1
	at_eNf1 = MpcAttributeMetaData()
	at_eNf1.type= MpcAttributeType.Real
	at_eNf1.name= 'eNf1'
	at_eNf1.group= 'Optional parameters'
	at_eNf1.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('eNf1')+'<br/>') + 
		html_par('floating point value defining force points on the negative response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# eNf2
	at_eNf2 = MpcAttributeMetaData()
	at_eNf2.type= MpcAttributeType.Real
	at_eNf2.name= 'eNf2'
	at_eNf2.group= 'Optional parameters'
	at_eNf2.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('eNf2')+'<br/>') + 
		html_par('floating point value defining force points on the negative response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# eNf3
	at_eNf3 = MpcAttributeMetaData()
	at_eNf3.type= MpcAttributeType.Real
	at_eNf3.name= 'eNf3'
	at_eNf3.group= 'Optional parameters'
	at_eNf3.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('eNf3')+'<br/>') + 
		html_par('floating point value defining force points on the negative response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
		
	# eNf4
	at_eNf4 = MpcAttributeMetaData()
	at_eNf4.type= MpcAttributeType.Real
	at_eNf4.name= 'eNf4'
	at_eNf4.group= 'Optional parameters'
	at_eNf4.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('eNf4')+'<br/>') + 
		html_par('floating point value defining force points on the negative response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# eNd1
	at_eNd1 = MpcAttributeMetaData()
	at_eNd1.type= MpcAttributeType.Real
	at_eNd1.name= 'eNd1'
	at_eNd1.group= 'Optional parameters'
	at_eNd1.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('eNd1')+'<br/>') + 
		html_par('floating point value defining deformation points on the negative response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# eNd2
	at_eNd2 = MpcAttributeMetaData()
	at_eNd2.type= MpcAttributeType.Real
	at_eNd2.name= 'eNd2'
	at_eNd2.group= 'Optional parameters'
	at_eNd2.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('eNd2')+'<br/>') + 
		html_par('floating point value defining deformation points on the negative response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
		
	# eNd3
	at_eNd3 = MpcAttributeMetaData()
	at_eNd3.type= MpcAttributeType.Real
	at_eNd3.name= 'eNd3'
	at_eNd3.group= 'Optional parameters'
	at_eNd3.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('eNd3')+'<br/>') + 
		html_par('floating point value defining deformation points on the negative response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# eNd4
	at_eNd4 = MpcAttributeMetaData()
	at_eNd4.type= MpcAttributeType.Real
	at_eNd4.name= 'eNd4'
	at_eNd4.group= 'Optional parameters'
	at_eNd4.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('eNd4')+'<br/>') + 
		html_par('floating point value defining deformation points on the negative response envelope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# rDispP
	at_rDispP = MpcAttributeMetaData()
	at_rDispP.type= MpcAttributeType.Real
	at_rDispP.name= 'rDispP'
	at_rDispP.group= 'Non-linear'
	at_rDispP.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('rDispP')+'<br/>') + 
		html_par('floating point value defining the ratio of the deformation at which reloading occurs to the maximum historic deformation demand') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)

	# rForceP
	at_rForceP = MpcAttributeMetaData()
	at_rForceP.type= MpcAttributeType.Real
	at_rForceP.name= 'rForceP'
	at_rForceP.group= 'Non-linear'
	at_rForceP.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('rForceP')+'<br/>') + 
		html_par('floating point value defining the ratio of the force at which reloading begins to force corresponding to the maximum historic deformation demand') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# uForceP
	at_uForceP = MpcAttributeMetaData()
	at_uForceP.type= MpcAttributeType.Real
	at_uForceP.name= 'uForceP'
	at_uForceP.group= 'Non-linear'
	at_uForceP.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('uForceP')+'<br/>') + 
		html_par('floating point value defining the ratio of strength developed upon unloading from negative load to the maximum strength developed under monotonic loading') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)	
	
	# rDispN
	at_rDispN = MpcAttributeMetaData()
	at_rDispN.type= MpcAttributeType.Real
	at_rDispN.name= 'rDispN'
	at_rDispN.group= 'Optional parameters'
	at_rDispN.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('rDispN')+'<br/>') + 
		html_par('floating point value defining the ratio of the deformation at which reloading occurs to the minimum historic deformation demand') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# fForceN
	at_fForceN = MpcAttributeMetaData()
	at_fForceN.type= MpcAttributeType.Real
	at_fForceN.name= 'rForceN'
	at_fForceN.group= 'Optional parameters'
	at_fForceN.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('fForceN')+'<br/>') + 
		html_par('floating point value defining the ratio of the force at which reloading begins to force corresponding to the minimum historic deformation demand') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)

	# uForceN
	at_uForceN = MpcAttributeMetaData()
	at_uForceN.type= MpcAttributeType.Real
	at_uForceN.name= 'uForceN'
	at_uForceN.group= 'Optional parameters'
	at_uForceN.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('uForceN')+'<br/>') + 
		html_par('floating point value defining the ratio of strength developed upon unloading from negative load to the minimum strength developed under monotonic loading') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gK1
	at_gK1 = MpcAttributeMetaData()
	at_gK1.type= MpcAttributeType.Real
	at_gK1.name= 'gK1'
	at_gK1.group= 'Non-linear'
	at_gK1.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gK1')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for unloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gK2
	at_gK2 = MpcAttributeMetaData()
	at_gK2.type= MpcAttributeType.Real
	at_gK2.name= 'gK2'
	at_gK2.group= 'Non-linear'
	at_gK2.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gK2')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for unloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gK3
	at_gK3 = MpcAttributeMetaData()
	at_gK3.type= MpcAttributeType.Real
	at_gK3.name= 'gK3'
	at_gK3.group= 'Non-linear'
	at_gK3.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gK3')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for unloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gK4
	at_gK4 = MpcAttributeMetaData()
	at_gK4.type= MpcAttributeType.Real
	at_gK4.name= 'gK4'
	at_gK4.group= 'Non-linear'
	at_gK4.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gK4')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for unloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gKLim
	at_gKLim = MpcAttributeMetaData()
	at_gKLim.type= MpcAttributeType.Real
	at_gKLim.name= 'gKLim'
	at_gKLim.group= 'Non-linear'
	at_gKLim.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gKLim')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for unloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
		
	# gD1 
	at_gD1= MpcAttributeMetaData()
	at_gD1.type= MpcAttributeType.Real
	at_gD1.name= 'gD1'
	at_gD1.group= 'Non-linear'
	at_gD1.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gD1')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for reloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gD2 
	at_gD2= MpcAttributeMetaData()
	at_gD2.type= MpcAttributeType.Real
	at_gD2.name= 'gD2'
	at_gD2.group= 'Non-linear'
	at_gD2.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gD2')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for reloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gD3
	at_gD3= MpcAttributeMetaData()
	at_gD3.type= MpcAttributeType.Real
	at_gD3.name= 'gD3'
	at_gD3.group= 'Non-linear'
	at_gD3.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gD3')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for reloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gD4
	at_gD4= MpcAttributeMetaData()
	at_gD4.type= MpcAttributeType.Real
	at_gD4.name= 'gD4'
	at_gD4.group= 'Non-linear'
	at_gD4.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gD4')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for reloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gDLim
	at_gDLim= MpcAttributeMetaData()
	at_gDLim.type= MpcAttributeType.Real
	at_gDLim.name= 'gDLim'
	at_gDLim.group= 'Non-linear'
	at_gDLim.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gDLim')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for reloading stiffness degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gF1
	at_gF1= MpcAttributeMetaData()
	at_gF1.type= MpcAttributeType.Real
	at_gF1.name= 'gF1'
	at_gF1.group= 'Non-linear'
	at_gF1.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gF1')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for strength degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gF2
	at_gF2= MpcAttributeMetaData()
	at_gF2.type= MpcAttributeType.Real
	at_gF2.name= 'gF2'
	at_gF2.group= 'Non-linear'
	at_gF2.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gF2')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for strength degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gF3
	at_gF3= MpcAttributeMetaData()
	at_gF3.type= MpcAttributeType.Real
	at_gF3.name= 'gF3'
	at_gF3.group= 'Non-linear'
	at_gF3.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gF3')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for strength degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gF4
	at_gF4= MpcAttributeMetaData()
	at_gF4.type= MpcAttributeType.Real
	at_gF4.name= 'gF4'
	at_gF4.group= 'Non-linear'
	at_gF4.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gF4')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for strength degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gFLim
	at_gFLim= MpcAttributeMetaData()
	at_gFLim.type= MpcAttributeType.Real
	at_gFLim.name= 'gFLim'
	at_gFLim.group= 'Non-linear'
	at_gFLim.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gFLim')+'<br/>') + 
		html_par('floating point value controlling cyclic degradation model for strength degradation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	
	# gE
	at_gE= MpcAttributeMetaData()
	at_gE.type= MpcAttributeType.Real
	at_gE.name= 'gE'
	at_gE.group= 'Non-linear'
	at_gE.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('gE')+'<br/>') + 
		html_par('floating point value used to define maximum energy dissipation under cyclic loading. Total energy dissipation capacity is defined as this factor multiplied by the energy dissipated under monotonic loading.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
		
	# dmgType
	at_dmgType= MpcAttributeMetaData()
	at_dmgType.type= MpcAttributeType.String
	at_dmgType.name= 'dmgType'
	at_dmgType.group= 'Misc'
	at_dmgType.description= (
		html_par(html_begin()) +
		html_par(html_boldtext('dmgType')+'<br/>') + 
		html_par('string to indicate type of damage (option: "cycle", "energy")') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Pinching4_Material','Pinching4 Material')+'<br/>') +
		html_end()
		)
	at_dmgType.sourceType = MpcAttributeSourceType.List
	at_dmgType.setSourceList(['cycle', 'energy'])
	at_dmgType.setDefault('cycle')
	
	xom= MpcXObjectMetaData()
	xom.name= 'Pinching4'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_ePf1)
	xom.addAttribute(at_ePf2)
	xom.addAttribute(at_ePf3)
	xom.addAttribute(at_ePf4)
	xom.addAttribute(at_ePd1)
	xom.addAttribute(at_ePd2)
	xom.addAttribute(at_ePd3)
	xom.addAttribute(at_ePd4)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_eNf1)
	xom.addAttribute(at_eNf2)
	xom.addAttribute(at_eNf3)
	xom.addAttribute(at_eNf4)
	xom.addAttribute(at_eNd1)
	xom.addAttribute(at_eNd2)
	xom.addAttribute(at_eNd3)
	xom.addAttribute(at_eNd4)
	xom.addAttribute(at_rDispP)
	xom.addAttribute(at_rForceP)
	xom.addAttribute(at_uForceP)
	xom.addAttribute(at_rDispN)
	xom.addAttribute(at_fForceN)
	xom.addAttribute(at_uForceN)
	xom.addAttribute(at_gK1)
	xom.addAttribute(at_gK2)
	xom.addAttribute(at_gK3)
	xom.addAttribute(at_gK4)
	xom.addAttribute(at_gKLim)
	xom.addAttribute(at_gD1)
	xom.addAttribute(at_gD2)
	xom.addAttribute(at_gD3)
	xom.addAttribute(at_gD4)
	xom.addAttribute(at_gDLim)
	xom.addAttribute(at_gF1)
	xom.addAttribute(at_gF2)
	xom.addAttribute(at_gF3)
	xom.addAttribute(at_gF4)
	xom.addAttribute(at_gFLim)
	xom.addAttribute(at_gE)
	xom.addAttribute(at_dmgType)
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_eNf1)
	xom.setVisibilityDependency(at_Optional, at_eNd1)
	xom.setVisibilityDependency(at_Optional, at_eNf2)
	xom.setVisibilityDependency(at_Optional, at_eNd2)
	xom.setVisibilityDependency(at_Optional, at_eNf3)
	xom.setVisibilityDependency(at_Optional, at_eNd3)
	xom.setVisibilityDependency(at_Optional, at_eNf4)
	xom.setVisibilityDependency(at_Optional, at_eNd4)
	xom.setVisibilityDependency(at_Optional, at_rDispN)
	xom.setVisibilityDependency(at_Optional, at_fForceN)
	xom.setVisibilityDependency(at_Optional, at_uForceN)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Pinching4 $matTag $ePf1 $ePd1 $ePf2 $ePd2 $ePf3 $ePd3 $ePf4 $ePd4
	#<$eNf1 $eNd1 $eNf2 $eNd2 $eNf3 $eNd3 $eNf4 $eNd4> $rDispP $rForceP $uForceP
	#<$rDispN $rForceN $uForceN > $gK1 $gK2 $gK3 $gK4 $gKLim $gD1 $gD2 $gD3 $gD4 $gDLim
	#$gF1 $gF2 $gF3 $gF4 $gFLim $gE $dmgType
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	ePf1_at = xobj.getAttribute('ePf1')
	if(ePf1_at is None):
		raise Exception('Error: cannot find "ePf1" attribute')
	ePf1 = ePf1_at.real
	
	ePd1_at = xobj.getAttribute('ePd1')
	if(ePd1_at is None):
		raise Exception('Error: cannot find "ePd1" attribute')
	ePd1 = ePd1_at.real
	
	ePf2_at = xobj.getAttribute('ePf2')
	if(ePf2_at is None):
		raise Exception('Error: cannot find "ePf2" attribute')
	ePf2 = ePf2_at.real
	
	ePd2_at = xobj.getAttribute('ePd2')
	if(ePd2_at is None):
		raise Exception('Error: cannot find "ePd2" attribute')
	ePd2 = ePd2_at.real
	
	ePf3_at = xobj.getAttribute('ePf3')
	if(ePf3_at is None):
		raise Exception('Error: cannot find "ePf3" attribute')
	ePf3 = ePf3_at.real
	
	ePd3_at = xobj.getAttribute('ePd3')
	if(ePd3_at is None):
		raise Exception('Error: cannot find "ePd3" attribute')
	ePd3 = ePd3_at.real
	
	ePf4_at = xobj.getAttribute('ePf4')
	if(ePf4_at is None):
		raise Exception('Error: cannot find "ePf4" attribute')
	ePf4 = ePf4_at.real
	
	ePd4_at = xobj.getAttribute('ePd4')
	if(ePd4_at is None):
		raise Exception('Error: cannot find "ePd4" attribute')
	ePd4 = ePd4_at.real
	
	rDispP_at = xobj.getAttribute('rDispP')
	if(rDispP_at is None):
		raise Exception('Error: cannot find "rDispP" attribute')
	rDispP = rDispP_at.real
	
	rForceP_at = xobj.getAttribute('rForceP')
	if(rForceP_at is None):
		raise Exception('Error: cannot find "rForceP" attribute')
	rForceP = rForceP_at.real
	
	uForceP_at = xobj.getAttribute('uForceP')
	if(uForceP_at is None):
		raise Exception('Error: cannot find "uForceP" attribute')
	uForceP = uForceP_at.real
	
	gK1_at = xobj.getAttribute('gK1')
	if(gK1_at is None):
		raise Exception('Error: cannot find "gK1" attribute')
	gK1 = gK1_at.real
	
	gK2_at = xobj.getAttribute('gK2')
	if(gK2_at is None):
		raise Exception('Error: cannot find "gK2" attribute')
	gK2 = gK2_at.real
	
	gK3_at = xobj.getAttribute('gK3')
	if(gK3_at is None):
		raise Exception('Error: cannot find "gK3" attribute')
	gK3 = gK3_at.real
	
	gK4_at = xobj.getAttribute('gK4')
	if(gK4_at is None):
		raise Exception('Error: cannot find "gK4" attribute')
	gK4 = gK4_at.real
	
	gKLim_at = xobj.getAttribute('gKLim')
	if(gKLim_at is None):
		raise Exception('Error: cannot find "gKLim" attribute')
	gKLim = gKLim_at.real
	
	gD1_at = xobj.getAttribute('gD1')
	if(gD1_at is None):
		raise Exception('Error: cannot find "gD1" attribute')
	gD1 = gD1_at.real
	
	gD2_at = xobj.getAttribute('gD2')
	if(gD2_at is None):
		raise Exception('Error: cannot find "gD2" attribute')
	gD2 = gD2_at.real
	
	gD3_at = xobj.getAttribute('gD3')
	if(gD3_at is None):
		raise Exception('Error: cannot find "gD3" attribute')
	gD3 = gD3_at.real
	
	gD4_at = xobj.getAttribute('gD4')
	if(gD4_at is None):
		raise Exception('Error: cannot find "gD4" attribute')
	gD4 = gD4_at.real
	
	gDLim_at = xobj.getAttribute('gDLim')
	if(gDLim_at is None):
		raise Exception('Error: cannot find "gDLim" attribute')
	gDLim = gDLim_at.real
	
	gF1_at = xobj.getAttribute('gF1')
	if(gF1_at is None):
		raise Exception('Error: cannot find "gF1" attribute')
	gF1 = gF1_at.real
	
	gF2_at = xobj.getAttribute('gF2')
	if(gF2_at is None):
		raise Exception('Error: cannot find "gF2" attribute')
	gF2 = gF2_at.real
	
	gF3_at = xobj.getAttribute('gF3')
	if(gF3_at is None):
		raise Exception('Error: cannot find "gF3" attribute')
	gF3 = gF3_at.real
	
	gF4_at = xobj.getAttribute('gF4')
	if(gF4_at is None):
		raise Exception('Error: cannot find "gF4" attribute')
	gF4 = gF4_at.real
	
	gFLim_at = xobj.getAttribute('gFLim')
	if(gFLim_at is None):
		raise Exception('Error: cannot find "gFLim" attribute')
	gFLim = gFLim_at.real
	
	gE_at = xobj.getAttribute('gE')
	if(gE_at is None):
		raise Exception('Error: cannot find "gE" attribute')
	gE = gE_at.real
	
	dmgType_at = xobj.getAttribute('dmgType')
	if(dmgType_at is None):
		raise Exception('Error: cannot find "dmgType" attribute')
	dmgType = dmgType_at.string
	
	
	# optional paramters
	sopt_1 = ''
	sopt_2 = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		eNf1_at = xobj.getAttribute('eNf1')
		if(eNf1_at is None):
			raise Exception('Error: cannot find "eNf1" attribute')
		eNf1 = eNf1_at.real
		
		eNd1_at = xobj.getAttribute('eNd1')
		if(eNd1_at is None):
			raise Exception('Error: cannot find "eNd1" attribute')
		eNd1 = eNd1_at.real
		
		eNf2_at = xobj.getAttribute('eNf2')
		if(eNf2_at is None):
			raise Exception('Error: cannot find "eNf2" attribute')
		eNf2 = eNf2_at.real
		
		eNd2_at = xobj.getAttribute('eNd2')
		if(eNd2_at is None):
			raise Exception('Error: cannot find "eNd2" attribute')
		eNd2 = eNd2_at.real
		
		eNf3_at = xobj.getAttribute('eNf3')
		if(eNf3_at is None):
			raise Exception('Error: cannot find "eNf3" attribute')
		eNf3 = eNf3_at.real
		
		eNd3_at = xobj.getAttribute('eNd3')
		if(eNd3_at is None):
			raise Exception('Error: cannot find "eNd3" attribute')
		eNd3 = eNd3_at.real
		
		eNf4_at = xobj.getAttribute('eNf4')
		if(eNf4_at is None):
			raise Exception('Error: cannot find "eNf4" attribute')
		eNf4 = eNf4_at.real
		
		eNd4_at = xobj.getAttribute('eNd4')
		if(eNd4_at is None):
			raise Exception('Error: cannot find "eNd4" attribute')
		eNd4 = eNd4_at.real
		
		sopt_1 += '{} {} {} {} {} {} {} {}'.format(eNf1, eNd1, eNf2, eNd2, eNf3, eNd3, eNf4, eNd4)
		
		rDispN_at = xobj.getAttribute('rDispN')
		if(rDispN_at is None):
			raise Exception('Error: cannot find "rDispN" attribute')
		rDispN = rDispN_at.real
		
		rForceN_at = xobj.getAttribute('rForceN')
		if(rForceN_at is None):
			raise Exception('Error: cannot find "rForceN" attribute')
		rForceN = rForceN_at.real
		
		uForceN_at = xobj.getAttribute('uForceN')
		if(uForceN_at is None):
			raise Exception('Error: cannot find "uForceN" attribute')
		uForceN = uForceN_at.real
		
		sopt_2 += '{} {} {}'.format(rDispN, rForceN, uForceN)
	
	
	str_tcl = '{}uniaxialMaterial Pinching4 {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, ePf1, ePd1, ePf2, ePd2, ePf3, ePd3, ePf4, ePd4, sopt_1, rDispP, rForceP, uForceP, sopt_2, gK1, gK2, gK3, gK4,
			gKLim, gD1, gD2, gD3, gD4, gDLim, gF1, gF2, gF3, gF4, gFLim, gE, dmgType)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)