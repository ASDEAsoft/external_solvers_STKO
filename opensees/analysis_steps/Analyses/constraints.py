from PyMpc import *
from mpc_utils_html import *

def constraintsCommand(xom):
	
	# utils
	def _mka(name, type, descr, link):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = 'constraints'
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr if descr else '') +
			html_par(link + '<br/>') +
			html_end()
			)
		return a
	def _mka_lm(name, type, descr):
		return _mka(name, type, descr,
			html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/constraint/lagrangeMultipliers.html','Lagrange Multipliers'))
	def _mka_pn(name, type, descr):
		return _mka(name, type, descr,
			html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/constraint/PenaltyMethod.html','Penalty Method'))
	def _mka_auto(name, type, descr):
		return _mka(name, type, descr,
			html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/constraint/Auto.html','Auto Method'))
	
	# types
	types = _mka('constraints', MpcAttributeType.String, 'The list of available constraint handlers', 
		html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/constraints.html','Constraints Command'))
	types.sourceType = MpcAttributeSourceType.List
	types.setSourceList(['Plain Constraints', 'Lagrange Multipliers', 'Penalty Method', 'Transformation Method', 'Auto'])
	types.setDefault('Transformation Method')
	
	# lm
	lm = _mka_lm('Lagrange Multipliers', MpcAttributeType.Boolean, '')
	lm.editable = False
	# lm_opt
	lm_opt = _mka_lm('Optional lagrangeMultipliers', MpcAttributeType.Boolean, '')
	# lm_alphaS
	lm_alphaS = _mka_lm('alphaS/LagrangeMultipliers', MpcAttributeType.Real, '')
	lm_alphaS.setDefault(1.0)
	# lm_alphaM
	lm_alphaM = _mka_lm('alphaM/LagrangeMultipliers', MpcAttributeType.Real, '')
	lm_alphaM.setDefault(1.0)
	
	# pn
	pn = _mka_pn('Penalty Method', MpcAttributeType.Boolean, '')
	pn.editable = False
	# pn_alphaS
	pn_alphaS = _mka_pn('alphaS/penaltyMethod', MpcAttributeType.Real, '')
	pn_alphaS.setDefault(1.e18)
	# pn_alphaM
	pn_alphaM = _mka_pn('alphaM/penaltyMethod', MpcAttributeType.Real, '')
	pn_alphaM.setDefault(1.e18)
	
	# auto
	auto = _mka_auto('Auto', MpcAttributeType.Boolean, '')
	auto.editable = False
	# auto_verbose
	auto_verbose = _mka_auto('-verbose/auto', MpcAttributeType.Boolean, '')
	auto_verbose.setDefault(False)
	# auto_type
	auto_type = _mka_auto('Type/auto', MpcAttributeType.String, '')
	auto_type.sourceType = MpcAttributeSourceType.List
	auto_type.setSourceList(['Automatic', 'User-Defined'])
	auto_type.setDefault('Automatic')
	# auto_oom
	auto_oom_switch = _mka_auto('Automatic', MpcAttributeType.Boolean, '')
	auto_oom_switch.editable = False
	auto_oom = _mka_auto('oom/auto', MpcAttributeType.Integer, 'The increase in order-of-magnitude of the penalty stiffness wrt the original stiffness')
	auto_oom.setDefault(3)
	# auto_user
	auto_user_switch = _mka_auto('User-Defined', MpcAttributeType.Boolean, '')
	auto_user_switch.editable = False
	auto_user = _mka_auto('userPenalty/auto', MpcAttributeType.Real, '')
	auto_user.setDefault(1.0e18)
	
	# add
	xom.addAttribute(types)
	xom.addAttribute(lm)
	xom.addAttribute(lm_opt)
	xom.addAttribute(lm_alphaS)
	xom.addAttribute(lm_alphaM)
	xom.addAttribute(pn)
	xom.addAttribute(pn_alphaS)
	xom.addAttribute(pn_alphaM)
	xom.addAttribute(auto)
	xom.addAttribute(auto_verbose)
	xom.addAttribute(auto_type)
	xom.addAttribute(auto_oom_switch)
	xom.addAttribute(auto_oom)
	xom.addAttribute(auto_user_switch)
	xom.addAttribute(auto_user)
	
	# connections
	# lm
	xom.setVisibilityDependency(lm, lm_opt)
	xom.setVisibilityDependency(lm_opt, lm_alphaS)
	xom.setVisibilityDependency(lm, lm_alphaS)
	xom.setVisibilityDependency(lm_opt, lm_alphaM)
	xom.setVisibilityDependency(lm, lm_alphaM)
	# pn
	xom.setVisibilityDependency(pn, pn_alphaS)
	xom.setVisibilityDependency(pn, pn_alphaM)
	# auto
	xom.setVisibilityDependency(auto, auto_verbose)
	xom.setVisibilityDependency(auto, auto_type)
	xom.setVisibilityDependency(auto, auto_oom)
	xom.setVisibilityDependency(auto_oom_switch, auto_oom)
	xom.setVisibilityDependency(auto, auto_user)
	xom.setVisibilityDependency(auto_user_switch, auto_user)
	xom.setBooleanAutoExclusiveDependency(auto_type, auto_oom_switch)
	xom.setBooleanAutoExclusiveDependency(auto_type, auto_user_switch)
	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(types, lm)
	xom.setBooleanAutoExclusiveDependency(types, pn)
	xom.setBooleanAutoExclusiveDependency(types, auto)

def writeTcl_constraints(pinfo, xobj):
	
	# utility
	def _geta(name):
		a = xobj.getAttribute(name)
		if(a is None):
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return a
	
	# the constraint type
	constraints = _geta('constraints').string
	
	# plain
	if constraints == 'Plain Constraints':
		str_tcl = '{}constraints Plain\n'.format(
			pinfo.indent)
	# lagrange multipliers
	elif constraints == 'Lagrange Multipliers':
		sopt = ''
		if _geta('Optional lagrangeMultipliers').boolean:
			sopt = ' {} {}'.format(
				_geta('alphaS/LagrangeMultipliers').real,
				_geta('alphaM/LagrangeMultipliers').real)
		str_tcl = '{}constraints Lagrange{}\n'.format (pinfo.indent, sopt)
	# penalty
	elif constraints == 'Penalty Method':
		str_tcl = '{}constraints Penalty {} {}\n'.format(
			pinfo.indent,
			_geta('alphaS/penaltyMethod').real,
			_geta('alphaM/penaltyMethod').real)
	# transformation
	elif constraints == 'Transformation Method':
		str_tcl = '{}constraints Transformation\n'.format(
			pinfo.indent)
	# auto
	elif constraints == 'Auto':
		str_tcl = '{}constraints Auto{}{}{}\n'.format(
			pinfo.indent,
			' -verbose' if _geta('-verbose/auto').boolean else '',
			' -autoPenalty {}'.format(_geta('oom/auto').integer) if _geta('Automatic').boolean else '',
			' -userPenalty {}'.format(_geta('userPenalty/auto').real) if _geta('User-Defined').boolean else ''
		)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)