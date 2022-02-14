# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# K
	at_K = MpcAttributeMetaData()
	at_K.type = MpcAttributeType.QuantityScalar
	at_K.name = 'K'
	at_K.group = 'Elasticity'
	at_K.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K')+'<br/>') + 
		html_par('Elastic stiffness of linear spring to model the axial flexibility of an oil damper (brace and damper portion)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	at_K.dimension = u.F/u.L
	
	# Cd
	at_Cd = MpcAttributeMetaData()
	at_Cd.type = MpcAttributeType.QuantityScalar
	at_Cd.name = 'Cd'
	at_Cd.group = 'Non-linear'
	at_Cd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Cd')+'<br/>') + 
		html_par('Damping coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	at_Cd.dimension = u.F/(u.L/u.t)
	
	# use_Fr_p
	at_use_Fr_p = MpcAttributeMetaData()
	at_use_Fr_p.type = MpcAttributeType.Boolean
	at_use_Fr_p.name = 'use_Fr_p'
	at_use_Fr_p.group = 'Optional parameters'
	at_use_Fr_p.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_Fr_p')+'<br/>') + 
		html_par('Damper relief load (default=1.0, Damper property)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	
	# Fr
	at_Fr = MpcAttributeMetaData()
	at_Fr.type = MpcAttributeType.QuantityScalar
	at_Fr.name = 'Fr'
	at_Fr.group = 'Non-linear'
	at_Fr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fr')+'<br/>') + 
		html_par('Damper relief load (default=1.0, Damper property)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	at_Fr.setDefault(1.0)
	at_Fr.dimension = u.F
	
	# p
	at_p = MpcAttributeMetaData()
	at_p.type = MpcAttributeType.Real
	at_p.name = 'p'
	at_p.group = 'Non-linear'
	at_p.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p')+'<br/>') + 
		html_par('Post-relief viscous damping coefficient ratio (default=1.0, linear oil damper)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	at_p.setDefault(1.0)
	
	# use_LGap
	at_use_LGap = MpcAttributeMetaData()
	at_use_LGap.type = MpcAttributeType.Boolean
	at_use_LGap.name = 'use_LGap'
	at_use_LGap.group = 'Non-linear'
	at_use_LGap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_LGap')+'<br/>') + 
		html_par('gap length to simulate the gap length due to the pin tolerance (default=0.0: zero tolerance)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	
	# LGap
	at_LGap = MpcAttributeMetaData()
	at_LGap.type = MpcAttributeType.QuantityScalar
	at_LGap.name = 'LGap'
	at_LGap.group = 'Optional parameters'
	at_LGap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('LGap')+'<br/>') + 
		html_par('gap length to simulate the gap length due to the pin tolerance (default=0.0: zero tolerance)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	at_LGap.setDefault(0.0)
	at_LGap.dimension = u.L
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	
	# NM
	at_NM = MpcAttributeMetaData()
	at_NM.type = MpcAttributeType.Integer
	at_NM.name = 'NM'
	at_NM.group = 'Optional parameters'
	at_NM.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('NM')+'<br/>') + 
		html_par('Employed adaptive numerical algorithm (default value NM = 1; 1 = Dormand-Prince54, 2=6th order Adams-Bashforth-Moulton, 3=modified Rosenbrock Triple)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	at_NM.sourceType = MpcAttributeSourceType.List
	at_NM.setSourceList([1, 2])
	at_NM.setDefault(1)
	
	# RelTol
	at_RelTol = MpcAttributeMetaData()
	at_RelTol.type = MpcAttributeType.Real
	at_RelTol.name = 'RelTol'
	at_RelTol.group = 'Optional parameters'
	at_RelTol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('RelTol')+'<br/>') + 
		html_par('Tolerance for absolute relative error control of the adaptive iterative algorithm (default value 10^-6)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	at_RelTol.setDefault(10e-6)
	
	# AbsTol
	at_AbsTol = MpcAttributeMetaData()
	at_AbsTol.type = MpcAttributeType.Real
	at_AbsTol.name = 'AbsTol'
	at_AbsTol.group = 'Optional parameters'
	at_AbsTol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('AbsTol')+'<br/>') + 
		html_par('Tolerance for absolute error control of adaptive iterative algorithm (default value 10^-10)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	at_AbsTol.setDefault(10e-10)
	
	# MaxHalf
	at_MaxHalf = MpcAttributeMetaData()
	at_MaxHalf.type = MpcAttributeType.Real
	at_MaxHalf.name = 'MaxHalf'
	at_MaxHalf.group = 'Optional parameters'
	at_MaxHalf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('MaxHalf')+'<br/>') + 
		html_par('Maximum number of sub-step iterations within an integration step (default value 15)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BilinearOilDamper_Material','BilinearOilDamper Material')+'<br/>') +
		html_end()
		)
	at_MaxHalf.setDefault(15)
	
	xom = MpcXObjectMetaData()
	xom.name = 'BilinearOilDamper'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_K)
	xom.addAttribute(at_Cd)
	xom.addAttribute(at_use_Fr_p)
	xom.addAttribute(at_Fr)
	xom.addAttribute(at_p)
	xom.addAttribute(at_use_LGap)
	xom.addAttribute(at_LGap)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_NM)
	xom.addAttribute(at_RelTol)
	xom.addAttribute(at_AbsTol)
	xom.addAttribute(at_MaxHalf)
	
	# Fr_p-dep
	xom.setVisibilityDependency(at_use_Fr_p, at_Fr)
	xom.setVisibilityDependency(at_use_Fr_p, at_p)
	
	# LGap-dep
	xom.setVisibilityDependency(at_use_LGap, at_LGap)
	
	# use_Optional-dep
	xom.setVisibilityDependency(at_Optional, at_NM)
	xom.setVisibilityDependency(at_Optional, at_RelTol)
	xom.setVisibilityDependency(at_Optional, at_AbsTol)
	xom.setVisibilityDependency(at_Optional, at_MaxHalf)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial BilinearOilDamper $matTag $K $Cd <$Fr $p> <$LGap> <$NM $RelTol $AbsTol $MaxHalf>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	K_at = xobj.getAttribute('K')
	if(K_at is None):
		raise Exception('Error: cannot find "K" attribute')
	K = K_at.quantityScalar
	
	Cd_at = xobj.getAttribute('Cd')
	if(Cd_at is None):
		raise Exception('Error: cannot find "Cd" attribute')
	Cd = Cd_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	use_Fr_p_at = xobj.getAttribute('use_Fr_p')
	if(use_Fr_p_at is None):
		raise Exception('Error: cannot find "use_Fr_p" attribute')
	use_Fr_p = use_Fr_p_at.boolean
	if use_Fr_p:
		Fr_at = xobj.getAttribute('Fr')
		if(Fr_at is None):
			raise Exception('Error: cannot find "Fr" attribute')
		Fr = Fr_at.quantityScalar
		
		p_at = xobj.getAttribute('p')
		if(p_at is None):
			raise Exception('Error: cannot find "p" attribute')
		p = p_at.real
		
		sopt += '{} {} '.format(Fr.value, p)
	
	use_LGap_at = xobj.getAttribute('use_LGap')
	if(use_LGap_at is None):
		raise Exception('Error: cannot find "use_LGap" attribute')
	use_LGap = use_LGap_at.boolean
	if use_LGap:
		LGap_at = xobj.getAttribute('LGap')
		if(LGap_at is None):
			raise Exception('Error: cannot find "LGap" attribute')
		LGap = LGap_at.quantityScalar
		
		sopt += ' {}'.format(LGap.value)
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		NM_at = xobj.getAttribute('NM')
		if(NM_at is None):
			raise Exception('Error: cannot find "NM" attribute')
		NM = NM_at.integer
		
		RelTol_at = xobj.getAttribute('RelTol')
		if(RelTol_at is None):
			raise Exception('Error: cannot find "RelTol" attribute')
		RelTol = RelTol_at.real
		
		AbsTol_at = xobj.getAttribute('AbsTol')
		if(AbsTol_at is None):
			raise Exception('Error: cannot find "AbsTol" attribute')
		AbsTol = AbsTol_at.real
		
		MaxHalf_at = xobj.getAttribute('MaxHalf')
		if(MaxHalf_at is None):
			raise Exception('Error: cannot find "MaxHalf" attribute')
		MaxHalf = MaxHalf_at.real
		
		sopt += ' {} {} {} {}'.format(NM, RelTol, AbsTol, MaxHalf)
	
	
	str_tcl = '{}uniaxialMaterial BilinearOilDamper {} {} {} {}\n'.format(pinfo.indent, tag, K.value, Cd.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)