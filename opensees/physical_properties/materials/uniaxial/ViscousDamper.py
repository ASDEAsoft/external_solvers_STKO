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
		html_par('Elastic stiffness of linear spring to model the axial flexibility of a viscous damper (e.g. combined stiffness of the supporting brace and internal damper portion)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
		html_end()
		)
	at_K.dimension = u.F/u.L
	
	# Cd
	at_Cd = MpcAttributeMetaData()
	at_Cd.type = MpcAttributeType.Real
	at_Cd.name = 'Cd'
	at_Cd.group = 'Non-linear'
	at_Cd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Cd')+'<br/>') + 
		html_par('Damping coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
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
		html_par('Velocity exponent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
		html_end()
		)
	
	# use_LGap
	at_use_LGap = MpcAttributeMetaData()
	at_use_LGap.type = MpcAttributeType.Boolean
	at_use_LGap.name = 'use_LGap'
	at_use_LGap.group = 'Non-linear'
	at_use_LGap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_LGap')+'<br/>') + 
		html_par('Gap length to simulate the gap length due to the pin tolerance') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
		html_end()
		)
	
	# LGap
	at_LGap = MpcAttributeMetaData()
	at_LGap.type = MpcAttributeType.Real
	at_LGap.name = 'LGap'
	at_LGap.group = 'Optional parameters'
	at_LGap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('LGap')+'<br/>') + 
		html_par('Gap length to simulate the gap length due to the pin tolerance') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
		html_end()
		)
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('Employed adaptive numerical algorithm (default value NM = 1; 1 = Dormand-Prince54, 2=6th order Adams-Bashforth-Moulton, 3=modified Rosenbrock Triple)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
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
		html_par('Employed adaptive numerical algorithm (default value NM = 1)') +
		html_par('1 = Dormand-Prince54,') +
		html_par('2=6th order Adams-Bashforth-Moulton,') +
		html_par('3=modified Rosenbrock Triple') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
		html_end()
		)
	at_NM.sourceType = MpcAttributeSourceType.List
	at_NM.setSourceList([1, 2, 3])
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
		html_end()
		)
	at_AbsTol.setDefault(10e-10)
	
	# MaxHalf
	at_MaxHalf = MpcAttributeMetaData()
	at_MaxHalf.type = MpcAttributeType.Integer
	at_MaxHalf.name = 'MaxHalf'
	at_MaxHalf.group = 'Optional parameters'
	at_MaxHalf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('MaxHalf')+'<br/>') + 
		html_par('Maximum number of sub-step iterations within an integration step (default value 15)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ViscousDamper_Material','ViscousDamper Material')+'<br/>') +
		html_end()
		)
	at_MaxHalf.setDefault(15)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ViscousDamper'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_K)
	xom.addAttribute(at_Cd)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_use_LGap)
	xom.addAttribute(at_LGap)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_NM)
	xom.addAttribute(at_RelTol)
	xom.addAttribute(at_AbsTol)
	xom.addAttribute(at_MaxHalf)
	
	
	# it is possible to have 3 or 4 or 8 input variables
	
	# use_LGap-dep
	xom.setVisibilityDependency(at_use_LGap, at_LGap)
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_NM)
	xom.setVisibilityDependency(at_Optional, at_RelTol)
	xom.setVisibilityDependency(at_Optional, at_AbsTol)
	xom.setVisibilityDependency(at_Optional, at_MaxHalf)
	
	xom.setVisibilityDependency(at_use_LGap, at_NM)
	xom.setVisibilityDependency(at_use_LGap, at_RelTol)
	xom.setVisibilityDependency(at_use_LGap, at_AbsTol)
	xom.setVisibilityDependency(at_use_LGap, at_MaxHalf)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ViscousDamper $matTag $K $Cd $alpha <$LGap> <$NM $RelTol $AbsTol $MaxHalf>
	
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
	Cd = Cd_at.real
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	
	# optional paramters
	sopt = ''
	
	use_LGap_at = xobj.getAttribute('use_LGap')
	if(use_LGap_at is None):
		raise Exception('Error: cannot find "use_LGap" attribute')
	use_LGap = use_LGap_at.boolean
	if use_LGap:
		LGap_at = xobj.getAttribute('LGap')
		if(LGap_at is None):
			raise Exception('Error: cannot find "LGap" attribute')
		LGap = LGap_at.real
		
		sopt += '{}'.format(LGap)
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if (Optional and use_LGap):
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
		MaxHalf = MaxHalf_at.integer
		
		sopt += ' {} {} {} {}'.format(NM, RelTol, AbsTol, MaxHalf)
	
	
	str_tcl = '{}uniaxialMaterial ViscousDamper {} {} {} {} {}\n'.format(pinfo.indent, tag, K.value, Cd, alpha, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)