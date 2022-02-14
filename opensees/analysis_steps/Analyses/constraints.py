from PyMpc import *
from mpc_utils_html import *

def constraintsCommand(xom):

	# constraintsCommand
	at_constraintsCommand = MpcAttributeMetaData()
	at_constraintsCommand.type = MpcAttributeType.String
	at_constraintsCommand.name = 'constraints'
	at_constraintsCommand.group = 'constraints'
	at_constraintsCommand.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('constraintsCommand')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Constraints_Command','Constraints Command')+'<br/>') +
		html_end()
		)
	at_constraintsCommand.sourceType = MpcAttributeSourceType.List
	at_constraintsCommand.setSourceList(['Plain Constraints', 'Lagrange Multipliers', 'Penalty Method', 'Transformation Method'])
	at_constraintsCommand.setDefault('Plain Constraints')
	
	# lagrangeMultipliers
	at_LagrangeMultipliers = MpcAttributeMetaData()
	at_LagrangeMultipliers.type = MpcAttributeType.Boolean
	at_LagrangeMultipliers.name = 'Lagrange Multipliers'
	at_LagrangeMultipliers.group = 'constraints'
	at_LagrangeMultipliers.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('LagrangeMultipliers')+'<br/>') + 
		html_par('Lagrange Multipliers') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Lagrange_Multipliers','Lagrange Multipliers')+'<br/>') +
		html_end()
		)
	at_LagrangeMultipliers.editable = False
	
	# optional
	at_Optional_lagrangeMultipliers = MpcAttributeMetaData()
	at_Optional_lagrangeMultipliers.type = MpcAttributeType.Boolean
	at_Optional_lagrangeMultipliers.name = 'Optional lagrangeMultipliers'
	at_Optional_lagrangeMultipliers.group = 'constraints'
	at_Optional_lagrangeMultipliers.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional lagrangeMultipliers')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Lagrange_Multipliers','Lagrange Multipliers')+'<br/>') +
		html_end()
		)
	
	# alphaS/lagrangeMultipliers
	at_alphaS = MpcAttributeMetaData()
	at_alphaS.type = MpcAttributeType.Real
	at_alphaS.name = 'alphaS/LagrangeMultipliers'
	at_alphaS.group = 'constraints'
	at_alphaS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaS')+'<br/>') +
		html_par('&alpha;S factor on singe points. optional, default = 1.0')+
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Lagrange_Multipliers','Lagrange Multipliers')+'<br/>') +
		html_end()
		)
	at_alphaS.setDefault(1.0)
	
	# alphaM/lagrangeMultipliers
	at_alphaM = MpcAttributeMetaData()
	at_alphaM.type = MpcAttributeType.Real
	at_alphaM.name = 'alphaM/LagrangeMultipliers'
	at_alphaM.group = 'constraints'
	at_alphaM.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaM')+'<br/>') +
		html_par('&alpha;M factor on multi-points, optional default = 1.0')+
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Lagrange_Multipliers','Lagrange Multipliers')+'<br/>') +
		html_end()
		)
	at_alphaM.setDefault(1.0)
	
	# penaltyMethod
	at_penaltyMethod = MpcAttributeMetaData()
	at_penaltyMethod.type = MpcAttributeType.Boolean
	at_penaltyMethod.name = 'Penalty Method'
	at_penaltyMethod.group = 'constraints'
	at_penaltyMethod.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('penaltyMethod')+'<br/>') + 
		html_par('Penalty Method') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Penalty_Method','Penalty Method')+'<br/>') +
		html_end()
		)
	at_penaltyMethod.editable = False
	
	# alphaS/penaltyMethod
	at_alphaS_1 = MpcAttributeMetaData()
	at_alphaS_1.type = MpcAttributeType.Real
	at_alphaS_1.name = 'alphaS/penaltyMethod'
	at_alphaS_1.group = 'constraints'
	at_alphaS_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaS')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Penalty_Method','Penalty Method')+'<br/>') +
		html_end()
		)
	at_alphaS_1.setDefault(1.e18)
	
	# alphaM/penaltyMethod
	at_alphaM_1 = MpcAttributeMetaData()
	at_alphaM_1.type = MpcAttributeType.Real
	at_alphaM_1.name = 'alphaM/penaltyMethod'
	at_alphaM_1.group = 'constraints'
	at_alphaM_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaM')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Penalty_Method','Penalty Method')+'<br/>') +
		html_end()
		)
	at_alphaM_1.setDefault(1.e18)
	
	xom.addAttribute(at_constraintsCommand)
	xom.addAttribute(at_LagrangeMultipliers)
	xom.addAttribute(at_Optional_lagrangeMultipliers)
	xom.addAttribute(at_alphaS)
	xom.addAttribute(at_alphaM)
	xom.addAttribute(at_penaltyMethod)
	xom.addAttribute(at_alphaS_1)
	xom.addAttribute(at_alphaM_1)
	
	
	# LagrangeMultipliers-alphaS LagrangeMultipliers-alphaM
	xom.setVisibilityDependency(at_LagrangeMultipliers, at_Optional_lagrangeMultipliers)
	
	xom.setVisibilityDependency(at_Optional_lagrangeMultipliers, at_alphaS)
	xom.setVisibilityDependency(at_LagrangeMultipliers, at_alphaS)
	
	xom.setVisibilityDependency(at_Optional_lagrangeMultipliers, at_alphaM)
	xom.setVisibilityDependency(at_LagrangeMultipliers, at_alphaM)
	
	# penalty Methods-alphaS penalty Methods-alphaM
	xom.setVisibilityDependency(at_penaltyMethod, at_alphaS_1)
	xom.setVisibilityDependency(at_penaltyMethod, at_alphaM_1)
	
	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(at_constraintsCommand, at_LagrangeMultipliers)
	xom.setBooleanAutoExclusiveDependency(at_constraintsCommand, at_penaltyMethod)

def writeTcl_constraints(pinfo, xobj):
	
	sopt = ''
	constraintsCommand_at = xobj.getAttribute('constraints')
	if(constraintsCommand_at is None):
		raise Exception('Error: cannot find "constraints" attribute')
	constraints = constraintsCommand_at.string
	
	if constraints == 'Plain Constraints':
		str_tcl = '{}constraints Plain\n'.format(pinfo.indent)
		
	elif constraints == 'Lagrange Multipliers':
		at_optional = xobj.getAttribute('Optional lagrangeMultipliers')
		if(at_optional is None):
			raise Exception('Error: cannot find "optional" attribute')
		optional = at_optional.boolean
		
		if optional:
			alphaS_at = xobj.getAttribute('alphaS/LagrangeMultipliers')
			if(alphaS_at is None):
				raise Exception('Error: cannot find "alphaS" attribute')
			sopt += ' {}'.format(alphaS_at.real)
			
			alphaM_at = xobj.getAttribute('alphaM/LagrangeMultipliers')
			if(alphaM_at is None):
				raise Exception('Error: cannot find "alphaM" attribute')
			sopt += ' {}'.format(alphaM_at.real)
			
		str_tcl = '{}constraints Lagrange{}\n'.format (pinfo.indent, sopt)
	
	elif constraints == 'Penalty Method':
		
		alphaS_at = xobj.getAttribute('alphaS/penaltyMethod')
		if(alphaS_at is None):
			raise Exception('Error: cannot find "alphaS" attribute')
		alphaS = alphaS_at.real
		
		alphaM_at = xobj.getAttribute('alphaM/penaltyMethod')
		if(alphaM_at is None):
			raise Exception('Error: cannot find "alphaM" attribute')
		alphaM = alphaM_at.real
	
		str_tcl = '{}constraints Penalty {} {}\n'.format (pinfo.indent, alphaS, alphaM)
		
	elif constraints == 'Transformation Method':
		str_tcl = '{}constraints Transformation\n'.format(pinfo.indent)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)