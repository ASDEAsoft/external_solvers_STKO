# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Elasticity'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('Tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Gap_Material','ElasticPPGap Material')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# Fy
	at_Fy = MpcAttributeMetaData()
	at_Fy.type = MpcAttributeType.QuantityScalar
	at_Fy.name = 'Fy'
	at_Fy.group = 'Non linear'
	at_Fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fy')+'<br/>') + 
		html_par('stress or force at which material reaches plastic state') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Gap_Material','ElasticPPGap Material')+'<br/>') +
		html_end()
		)
	at_Fy.dimension = u.F/u.L**2
	
	# gap
	at_gap = MpcAttributeMetaData()
	at_gap.type = MpcAttributeType.Real
	at_gap.name = 'gap'
	at_gap.group = 'Non-linear'
	at_gap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gap')+'<br/>') + 
		html_par('initial gap (strain or deformation)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Gap_Material','ElasticPPGap Material')+'<br/>') +
		html_end()
		)
	
	# use_eta
	at_use_eta = MpcAttributeMetaData()
	at_use_eta.type = MpcAttributeType.Boolean
	at_use_eta.name = 'use_eta'
	at_use_eta.group = 'Non-linear'
	at_use_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_eta')+'<br/>') + 
		html_par('hardening ratio (=Eh/E), which can be negative') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Gap_Material','ElasticPPGap Material')+'<br/>') +
		html_end()
		)
	
	# eta
	at_eta = MpcAttributeMetaData()
	at_eta.type = MpcAttributeType.Real
	at_eta.name = 'eta'
	at_eta.group = 'Optional parameters'
	at_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eta')+'<br/>') + 
		html_par('hardening ratio (=Eh/E), which can be negative') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Gap_Material','ElasticPPGap Material')+'<br/>') +
		html_end()
		)
	
	# use_damage
	at_use_damage = MpcAttributeMetaData()
	at_use_damage.type = MpcAttributeType.Boolean
	at_use_damage.name = 'use_damage'
	at_use_damage.group = 'Non-linear'
	at_use_damage.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_damage')+'<br/>') + 
		html_par('an optional string to specify whether to accumulate damage or not in the material. With the default string, "noDamage" the gap material will re-center on load reversal. If the string "damage" is provided this recentering will not occur and gap will grow.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Gap_Material','ElasticPPGap Material')+'<br/>') +
		html_end()
		)
	
	# damage
	at_damage = MpcAttributeMetaData()
	at_damage.type = MpcAttributeType.String
	at_damage.name = 'damage'
	at_damage.group = 'Optional parameters'
	at_damage.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('damage')+'<br/>') + 
		html_par('an optional string to specify whether to accumulate damage or not in the material. With the default string, "noDamage" the gap material will re-center on load reversal. If the string "damage" is provided this recentering will not occur and gap will grow.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Gap_Material','ElasticPPGap Material')+'<br/>') +
		html_end()
		)
	at_damage.sourceType = MpcAttributeSourceType.List
	at_damage.setSourceList(['damage', 'noDamage'])
	at_damage.setDefault('damage')
	
	xom = MpcXObjectMetaData()
	xom.name = 'ElasticPPGap'
	xom.Xgroup = 'Some Standard Uniaxial Materials'
	xom.addAttribute(at_E)
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_gap)
	xom.addAttribute(at_use_eta)
	xom.addAttribute(at_eta)
	xom.addAttribute(at_use_damage)
	xom.addAttribute(at_damage)
	
	# eta-dep
	xom.setVisibilityDependency(at_use_eta, at_eta)
	
	# damage-dep
	xom.setVisibilityDependency(at_use_damage, at_damage)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ElasticPPGap $matTag $E $Fy $gap <$eta> <damage>
	#uniaxialMaterial ElasticPPGap $matTag $E $Fy $gap $eta
	#uniaxialMaterial ElasticPPGap $matTag $E $Fy $gap damage <---- only if == damage
	#uniaxialMaterial ElasticPPGap $matTag $E $Fy $gap $eta $damage <---- here it can be damage or noDamage (any other string works a noDamage)
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	def geta(name):
		at = xobj.getAttribute(name)
		if(at is None):
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	# mandatory parameters
	E = geta('E').quantityScalar
	Fy = geta('Fy').quantityScalar
	gap = geta('gap').real
	
	# optional paramters
	sopt = ''
	use_eta = geta('use_eta').boolean
	use_damage = geta('use_damage').boolean
	if use_eta:
		eta = geta('eta').real
		if use_damage:
			damage = geta('damage').string
			if damage == 'damage':
				sopt += ' {} {}'.format(eta, damage)
			else:
				sopt += '{}'.format(eta)
		else:
			sopt += '{}'.format(eta)
	else:
		if use_damage:
			damage = geta('damage').string
			if damage == 'damage':
				sopt += ' {}'.format(damage)
	
	str_tcl = '{}uniaxialMaterial ElasticPPGap {} {} {} {} {}\n'.format(pinfo.indent, tag, E.value, Fy.value, gap, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)