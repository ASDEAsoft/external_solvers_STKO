from PyMpc import *
from mpc_utils_html import *

def algorithmCommand(xom, group_suffix=''):
	
	'''
	algorithm Linear <-secant> <-initial> <-factorOnce>
	algorithm Newton <-secant> <-initial> <-initialThenCurrent>
	algorithm NewtonLineSearch <-type $typeSearch> <-tol $tol> <-maxIter $maxIter> <-minEta $minEta> <-maxEta $maxEta>
	algorithm ModifiedNewton <-secant> <-initial>
	algorithm KrylovNewton <-iterate $tangIter> <-increment $tangIncr> <-maxDim $maxDim>
	algorithm SecantNewton <-iterate $tangIter> <-increment $tangIncr> <-maxDim $maxDim>
	algorithm BFGS <-secant> <-initial> <-count>
	algorithm Broyden <$count>
	'''
	group = str(group_suffix)+'algorithm' 
	
	# algorithm
	at_algorithm = MpcAttributeMetaData()
	at_algorithm.type = MpcAttributeType.String
	at_algorithm.name = 'algorithm'
	at_algorithm.group = group
	at_algorithm.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('algorithm')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Algorithm_Command','Algorithm Command')+'<br/>') +
		html_end()
		)
	at_algorithm.sourceType = MpcAttributeSourceType.List
	at_algorithm.setSourceList(['Linear',
								'Newton',
								'Newton with Line Search',
								'Modified Newton',
								'Krylov-Newton',
								'Secant Newton',
								'BFGS',
								'Broyden'])
	at_algorithm.setDefault('Newton')
	
	'''
	Linear
	'''
	# Linear
	at_Linear = MpcAttributeMetaData()
	at_Linear.type = MpcAttributeType.Boolean
	at_Linear.name = 'Linear'
	at_Linear.group = group
	at_Linear.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Linear')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Linear_Algorithm','Linear Algorithm')+'<br/>') +
		html_end()
		)
	at_Linear.editable = False
	
	# use_formTangent
	at_use_formTangent_Linear = MpcAttributeMetaData()
	at_use_formTangent_Linear.type = MpcAttributeType.Boolean
	at_use_formTangent_Linear.name = 'use_formTangent/Linear'
	at_use_formTangent_Linear.group = group
	at_use_formTangent_Linear.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness or initial stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Linear_Algorithm','Linear Algorithm')+'<br/>') +
		html_end()
		)
	
	# formTangent
	at_formTangent_Linear = MpcAttributeMetaData()
	at_formTangent_Linear.type = MpcAttributeType.String
	at_formTangent_Linear.name = 'formTangent/Linear'
	at_formTangent_Linear.group = group
	at_formTangent_Linear.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness or initial stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Linear_Algorithm','Linear Algorithm')+'<br/>') +
		html_end()
		)
	at_formTangent_Linear.sourceType = MpcAttributeSourceType.List
	at_formTangent_Linear.setSourceList(['-secant', '-initial'])
	at_formTangent_Linear.setDefault('-secant')
	
	# -factorOnce
	at_factorOnce = MpcAttributeMetaData()
	at_factorOnce.type = MpcAttributeType.Boolean
	at_factorOnce.name = '-factorOnce'
	at_factorOnce.group = group
	at_factorOnce.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-factorOnce')+'<br/>') + 
		html_par('optional flag to indicate to only set up and factor matrix once') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Linear_Algorithm','Linear Algorithm')+'<br/>') +
		html_end()
		)
	
	'''
	Newton
	'''
	# Newton
	at_Newton = MpcAttributeMetaData()
	at_Newton.type = MpcAttributeType.Boolean
	at_Newton.name = 'Newton'
	at_Newton.group = group
	at_Newton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Newton')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_Algorithm','Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_Newton.editable = False
	
	# use_formTangent
	at_use_formTangent_Newton = MpcAttributeMetaData()
	at_use_formTangent_Newton.type = MpcAttributeType.Boolean
	at_use_formTangent_Newton.name = 'use_formTangent/Newton'
	at_use_formTangent_Newton.group = group
	at_use_formTangent_Newton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness, initial stiffness or to use initial stiffness on first step, then use current stiffness for subsequent steps') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_Algorithm','Newton Algorithm')+'<br/>') +
		html_end()
		)
	
	# formTangent
	at_formTangent_Newton = MpcAttributeMetaData()
	at_formTangent_Newton.type = MpcAttributeType.String
	at_formTangent_Newton.name = 'formTangent/Newton'
	at_formTangent_Newton.group = group
	at_formTangent_Newton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness, initial stiffness or to use initial stiffness on first step, then use current stiffness for subsequent steps') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_Algorithm','Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_formTangent_Newton.sourceType = MpcAttributeSourceType.List
	at_formTangent_Newton.setSourceList(['-secant', '-initial', '-initialThenCurrent'])
	at_formTangent_Newton.setDefault('-secant')
	
	'''
	NewtonLineSearch
	'''
	# NewtonLineSearch
	at_NewtonLineSearch = MpcAttributeMetaData()
	at_NewtonLineSearch.type = MpcAttributeType.Boolean
	at_NewtonLineSearch.name = 'Newton with Line Search'
	at_NewtonLineSearch.group = group
	at_NewtonLineSearch.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('NewtonLineSearch')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	at_NewtonLineSearch.editable = False
	
	# -type
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.Boolean
	at_type.name = '-type'
	at_type.group = group
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-type')+'<br/>') + 
		html_par('line search algorithm. optional default is InitialInterpoled. valid types are: Bisection, Secant, RegulaFalsi, InitialInterpolated') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	
	# typeSearch
	at_typeSearch = MpcAttributeMetaData()
	at_typeSearch.type = MpcAttributeType.String
	at_typeSearch.name = 'typeSearch'
	at_typeSearch.group = group
	at_typeSearch.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('typeSearch')+'<br/>') + 
		html_par('line search algorithm. optional default is InitialInterpoled. valid types are: Bisection, Secant, RegulaFalsi, InitialInterpolated') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	at_typeSearch.sourceType = MpcAttributeSourceType.List
	at_typeSearch.setSourceList(['Bisection', 'Secant', 'RegulaFalsi', 'LinearInterpolated', 'InitialInterpolated'])
	at_typeSearch.setDefault('Bisection')
	
	# -tol
	at_use_tol = MpcAttributeMetaData()
	at_use_tol.type = MpcAttributeType.Boolean
	at_use_tol.name = '-tol'
	at_use_tol.group = group
	at_use_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-tol')+'<br/>') + 
		html_par('tolerance for search. optional, defeulat = 0.8') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = group
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') + 
		html_par('tolerance for search. optional, defeulat = 0.8') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	at_tol.setDefault(0.8)
	
	# -maxIter
	at_use_maxIter = MpcAttributeMetaData()
	at_use_maxIter.type = MpcAttributeType.Boolean
	at_use_maxIter.name = '-maxIter'
	at_use_maxIter.group = group
	at_use_maxIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-maxIter')+'<br/>') + 
		html_par('max num of iterations to try. optional, default = 10') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	
	# maxIter
	at_maxIter = MpcAttributeMetaData()
	at_maxIter.type = MpcAttributeType.Integer
	at_maxIter.name = 'maxIter'
	at_maxIter.group = group
	at_maxIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxIter')+'<br/>') + 
		html_par('max num of iterations to try. optional, default = 10') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	at_maxIter.setDefault(10)
	
	# -minEta
	at_use_minEta = MpcAttributeMetaData()
	at_use_minEta.type = MpcAttributeType.Boolean
	at_use_minEta.name = '-minEta'
	at_use_minEta.group = group
	at_use_minEta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-minEta')+'<br/>') + 
		html_par('a min eta value. optional, default = 0.1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	
	# minEta
	at_minEta = MpcAttributeMetaData()
	at_minEta.type = MpcAttributeType.Real
	at_minEta.name = 'minEta'
	at_minEta.group = group
	at_minEta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('minEta')+'<br/>') + 
		html_par('a min eta value. optional, default = 0.1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	at_minEta.setDefault(0.1)
	
	# -maxEta
	at_use_maxEta = MpcAttributeMetaData()
	at_use_maxEta.type = MpcAttributeType.Boolean
	at_use_maxEta.name = '-maxEta'
	at_use_maxEta.group = group
	at_use_maxEta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-maxEta')+'<br/>') + 
		html_par('a max eta value. optional, default = 10.0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	
	# maxEta
	at_maxEta = MpcAttributeMetaData()
	at_maxEta.type = MpcAttributeType.Real
	at_maxEta.name = 'maxEta'
	at_maxEta.group = group
	at_maxEta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxEta')+'<br/>') + 
		html_par('a max eta value. optional, default = 10.0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newton_with_Line_Search_Algorithm','Newton with Line Search Algorithm')+'<br/>') +
		html_end()
		)
	at_maxEta.setDefault(10.0)
	
	'''
	ModifiedNewton
	'''
	# ModifiedNewton
	at_ModifiedNewton = MpcAttributeMetaData()
	at_ModifiedNewton.type = MpcAttributeType.Boolean
	at_ModifiedNewton.name = 'Modified Newton'
	at_ModifiedNewton.group = group
	at_ModifiedNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ModifiedNewton')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Newton_Algorithm','Modified Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_ModifiedNewton.editable = False
	
	# use_formTangent
	at_use_formTangent_ModifiedNewton = MpcAttributeMetaData()
	at_use_formTangent_ModifiedNewton.type = MpcAttributeType.Boolean
	at_use_formTangent_ModifiedNewton.name = 'use_formTangent/ModifiedNewton'
	at_use_formTangent_ModifiedNewton.group = group
	at_use_formTangent_ModifiedNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness, initial stiffness or to use initial stiffness on first step, then use current stiffness for subsequent steps') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Newton_Algorithm','Modified Newton Algorithm')+'<br/>') +
		html_end()
		)
	
	# formTangent
	at_formTangent_ModifiedNewton = MpcAttributeMetaData()
	at_formTangent_ModifiedNewton.type = MpcAttributeType.String
	at_formTangent_ModifiedNewton.name = 'formTangent/ModifiedNewton'
	at_formTangent_ModifiedNewton.group = group
	at_formTangent_ModifiedNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness, initial stiffness or to use initial stiffness on first step, then use current stiffness for subsequent steps') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Modified_Newton_Algorithm','Modified Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_formTangent_ModifiedNewton.sourceType = MpcAttributeSourceType.List
	at_formTangent_ModifiedNewton.setSourceList(['-secant', '-initial'])
	at_formTangent_ModifiedNewton.setDefault('-secant')
	
	'''
	KrylovNewton
	'''
	# KrylovNewton
	at_KrylovNewton = MpcAttributeMetaData()
	at_KrylovNewton.type = MpcAttributeType.Boolean
	at_KrylovNewton.name = 'Krylov-Newton'
	at_KrylovNewton.group = group
	at_KrylovNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('KrylovNewton')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Krylov-Newton_Algorithm','Krylov-Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_KrylovNewton.editable = False
	
	# -iterate
	at_iterate_KrylovNewton = MpcAttributeMetaData()
	at_iterate_KrylovNewton.type = MpcAttributeType.Boolean
	at_iterate_KrylovNewton.name = '-iterate/KrylovNewton'
	at_iterate_KrylovNewton.group = group
	at_iterate_KrylovNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-iterate')+'<br/>') + 
		html_par('tangent to iterate on, options are current, initial, noTangent. default is current') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Krylov-Newton_Algorithm','Krylov-Newton Algorithm')+'<br/>') +
		html_end()
		)
	
	# tangIter
	at_tangIter_KrylovNewton = MpcAttributeMetaData()
	at_tangIter_KrylovNewton.type = MpcAttributeType.String
	at_tangIter_KrylovNewton.name = 'tangIter/KrylovNewton'
	at_tangIter_KrylovNewton.group = group
	at_tangIter_KrylovNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tangIter')+'<br/>') + 
		html_par('tangent to iterate on, options are current, initial, noTangent. default is current') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Krylov-Newton_Algorithm','Krylov-Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_tangIter_KrylovNewton.sourceType = MpcAttributeSourceType.List
	at_tangIter_KrylovNewton.setSourceList(['current', 'initial', 'noTangent'])
	at_tangIter_KrylovNewton.setDefault('current')
	
	# -increment
	at_increment_KrylovNewton = MpcAttributeMetaData()
	at_increment_KrylovNewton.type = MpcAttributeType.Boolean
	at_increment_KrylovNewton.name = '-increment/KrylovNewton'
	at_increment_KrylovNewton.group = group
	at_increment_KrylovNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-increment')+'<br/>') + 
		html_par('tangent to increment on, options are current, initial, noTangent. default is current') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Krylov-Newton_Algorithm','Krylov-Newton Algorithm')+'<br/>') +
		html_end()
		)
	
	# tangIncr
	at_tangIncr_KrylovNewton = MpcAttributeMetaData()
	at_tangIncr_KrylovNewton.type = MpcAttributeType.String
	at_tangIncr_KrylovNewton.name = 'tangIncr/KrylovNewton'
	at_tangIncr_KrylovNewton.group = group
	at_tangIncr_KrylovNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tangIncr')+'<br/>') + 
		html_par('tangent to increment on, options are current, initial, noTangent. default is current') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Krylov-Newton_Algorithm','Krylov-Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_tangIncr_KrylovNewton.sourceType = MpcAttributeSourceType.List
	at_tangIncr_KrylovNewton.setSourceList(['current', 'initial', 'noTangent'])
	at_tangIncr_KrylovNewton.setDefault('current')
	
	# -maxDim
	at_use_maxDim_KrylovNewton = MpcAttributeMetaData()
	at_use_maxDim_KrylovNewton.type = MpcAttributeType.Boolean
	at_use_maxDim_KrylovNewton.name = '-maxDim/KrylovNewton'
	at_use_maxDim_KrylovNewton.group = group
	at_use_maxDim_KrylovNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-maxDim')+'<br/>') + 
		html_par('max number of iterations until the tangent is reformed and the acceleration restarts (default = 3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Krylov-Newton_Algorithm','Krylov-Newton Algorithm')+'<br/>') +
		html_end()
		)
	
	# maxDim
	at_maxDim_KrylovNewton = MpcAttributeMetaData()
	at_maxDim_KrylovNewton.type = MpcAttributeType.Integer
	at_maxDim_KrylovNewton.name = 'maxDim/KrylovNewton'
	at_maxDim_KrylovNewton.group = group
	at_maxDim_KrylovNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxDim')+'<br/>') + 
		html_par('max number of iterations until the tangent is reformed and the acceleration restarts (default = 3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Krylov-Newton_Algorithm','Krylov-Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_maxDim_KrylovNewton.setDefault(3)
	
	'''
	SecantNewton
	'''
	# SecantNewton
	at_SecantNewton = MpcAttributeMetaData()
	at_SecantNewton.type = MpcAttributeType.Boolean
	at_SecantNewton.name = 'Secant Newton'
	at_SecantNewton.group = group
	at_SecantNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('SecantNewton')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Secant_Newton_Algorithm','Secant Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_SecantNewton.editable = False
	
	# -iterate
	at_iterate_SecantNewton = MpcAttributeMetaData()
	at_iterate_SecantNewton.type = MpcAttributeType.Boolean
	at_iterate_SecantNewton.name = '-iterate/SecantNewton'
	at_iterate_SecantNewton.group = group
	at_iterate_SecantNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-iterate')+'<br/>') + 
		html_par('tangent to iterate on, options are current, initial, noTangent. default is current') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Secant_Newton_Algorithm','Secant Newton Algorithm')+'<br/>') +
		html_end()
		)
	
	# tangIter
	at_tangIter_SecantNewton = MpcAttributeMetaData()
	at_tangIter_SecantNewton.type = MpcAttributeType.String
	at_tangIter_SecantNewton.name = 'tangIter/SecantNewton'
	at_tangIter_SecantNewton.group = group
	at_tangIter_SecantNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tangIter')+'<br/>') + 
		html_par('tangent to iterate on, options are current, initial, noTangent. default is current') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Secant_Newton_Algorithm','Secant Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_tangIter_SecantNewton.sourceType = MpcAttributeSourceType.List
	at_tangIter_SecantNewton.setSourceList(['current', 'initial', 'noTangent'])
	at_tangIter_SecantNewton.setDefault('current')
	
	# -increment
	at_increment_SecantNewton = MpcAttributeMetaData()
	at_increment_SecantNewton.type = MpcAttributeType.Boolean
	at_increment_SecantNewton.name = '-increment/SecantNewton'
	at_increment_SecantNewton.group = group
	at_increment_SecantNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-increment')+'<br/>') + 
		html_par('tangent to increment on, options are current, initial, noTangent. default is current') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Secant_Newton_Algorithm','Secant Newton Algorithm')+'<br/>') +
		html_end()
		)
	
	# tangIncr
	at_tangIncr_SecantNewton = MpcAttributeMetaData()
	at_tangIncr_SecantNewton.type = MpcAttributeType.String
	at_tangIncr_SecantNewton.name = 'tangIncr/SecantNewton'
	at_tangIncr_SecantNewton.group = group
	at_tangIncr_SecantNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tangIncr')+'<br/>') + 
		html_par('tangent to increment on, options are current, initial, noTangent. default is current') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Secant_Newton_Algorithm','Secant Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_tangIncr_SecantNewton.sourceType = MpcAttributeSourceType.List
	at_tangIncr_SecantNewton.setSourceList(['current', 'initial', 'noTangent'])
	at_tangIncr_SecantNewton.setDefault('current')
	
	# -maxDim
	at_use_maxDim_SecantNewton = MpcAttributeMetaData()
	at_use_maxDim_SecantNewton.type = MpcAttributeType.Boolean
	at_use_maxDim_SecantNewton.name = '-maxDim/SecantNewton'
	at_use_maxDim_SecantNewton.group = group
	at_use_maxDim_SecantNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-maxDim')+'<br/>') + 
		html_par('max number of iterations until the tangent is reformed and acceleration restarts (default = 3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Secant_Newton_Algorithm','Secant Newton Algorithm')+'<br/>') +
		html_end()
		)
	
	# maxDim
	at_maxDim_SecantNewton = MpcAttributeMetaData()
	at_maxDim_SecantNewton.type = MpcAttributeType.Integer
	at_maxDim_SecantNewton.name = 'maxDim/SecantNewton'
	at_maxDim_SecantNewton.group = group
	at_maxDim_SecantNewton.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxDim')+'<br/>') + 
		html_par('max number of iterations until the tangent is reformed and acceleration restarts (default = 3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Secant_Newton_Algorithm','Secant Newton Algorithm')+'<br/>') +
		html_end()
		)
	at_maxDim_SecantNewton.setDefault(3)
	
	'''
	BFGS
	'''
	# BFGS
	at_BFGS = MpcAttributeMetaData()
	at_BFGS.type = MpcAttributeType.Boolean
	at_BFGS.name = 'BFGS'
	at_BFGS.group = group
	at_BFGS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('BFGS')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BFGS_Algorithm','BFGS Algorithm')+'<br/>') +
		html_end()
		)
	at_BFGS.editable = False
	
	# use_formTangent
	at_use_formTangent_BFGS = MpcAttributeMetaData()
	at_use_formTangent_BFGS.type = MpcAttributeType.Boolean
	at_use_formTangent_BFGS.name = 'use_formTangent/BFGS'
	at_use_formTangent_BFGS.group = group
	at_use_formTangent_BFGS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness or initial stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BFGS_Algorithm','BFGS Algorithm')+'<br/>') +
		html_end()
		)
	
	# formTangent
	at_formTangent_BFGS = MpcAttributeMetaData()
	at_formTangent_BFGS.type = MpcAttributeType.String
	at_formTangent_BFGS.name = 'formTangent/BFGS'
	at_formTangent_BFGS.group = group
	at_formTangent_BFGS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness or initial stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BFGS_Algorithm','BFGS Algorithm')+'<br/>') +
		html_end()
		)
	at_formTangent_BFGS.sourceType = MpcAttributeSourceType.List
	at_formTangent_BFGS.setSourceList(['-secant', '-initial'])
	at_formTangent_BFGS.setDefault('-secant')
	
	# -count
	at_use_count_BFGS = MpcAttributeMetaData()
	at_use_count_BFGS.type = MpcAttributeType.Boolean
	at_use_count_BFGS.name = '-count/BFGS'
	at_use_count_BFGS.group = group
	at_use_count_BFGS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-count')+'<br/>') + 
		html_par('number of iterations within a time step until a new tangent is formed') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BFGS_Algorithm','BFGS Algorithm')+'<br/>') +
		html_end()
		)
	
	# count
	at_count_BFGS = MpcAttributeMetaData()
	at_count_BFGS.type = MpcAttributeType.Integer
	at_count_BFGS.name = 'count/BFGS'
	at_count_BFGS.group = group
	at_count_BFGS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('count')+'<br/>') + 
		html_par('number of iterations within a time step until a new tangent is formed') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BFGS_Algorithm','BFGS Algorithm')+'<br/>') +
		html_end()
		)
	
	'''
	Broyden
	'''
	# Broyden
	at_Broyden = MpcAttributeMetaData()
	at_Broyden.type = MpcAttributeType.Boolean
	at_Broyden.name = 'Broyden'
	at_Broyden.group = group
	at_Broyden.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Broyden')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Broyden_Algorithm','Broyden Algorithm')+'<br/>') +
		html_end()
		)
	at_Broyden.editable = False
	
	# use_formTangent
	at_use_formTangent_Broyden = MpcAttributeMetaData()
	at_use_formTangent_Broyden.type = MpcAttributeType.Boolean
	at_use_formTangent_Broyden.name = 'use_formTangent/Broyden'
	at_use_formTangent_Broyden.group = group
	at_use_formTangent_Broyden.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness or initial stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Broyden_Algorithm','Broyden Algorithm')+'<br/>') +
		html_end()
		)
	
	# formTangent
	at_formTangent_Broyden = MpcAttributeMetaData()
	at_formTangent_Broyden.type = MpcAttributeType.String
	at_formTangent_Broyden.name = 'formTangent/Broyden'
	at_formTangent_Broyden.group = group
	at_formTangent_Broyden.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('formTangent')+'<br/>') + 
		html_par('optional flag to indicate to use secant stiffness or initial stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Broyden_Algorithm','Broyden Algorithm')+'<br/>') +
		html_end()
		)
	at_formTangent_Broyden.sourceType = MpcAttributeSourceType.List
	at_formTangent_Broyden.setSourceList(['-secant', '-initial'])
	at_formTangent_Broyden.setDefault('-secant')
	
	# -count
	at_use_count_Broyden = MpcAttributeMetaData()
	at_use_count_Broyden.type = MpcAttributeType.Boolean
	at_use_count_Broyden.name = '-count/Broyden'
	at_use_count_Broyden.group = group
	at_use_count_Broyden.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-count')+'<br/>') + 
		html_par('number of iterations within a time step until a new tangent is formed') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Broyden_Algorithm','Broyden Algorithm')+'<br/>') +
		html_end()
		)
	
	# count
	at_count_Broyden = MpcAttributeMetaData()
	at_count_Broyden.type = MpcAttributeType.Integer
	at_count_Broyden.name = 'count/Broyden'
	at_count_Broyden.group = group
	at_count_Broyden.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('count')+'<br/>') + 
		html_par('number of iterations within a time step until a new tangent is formed') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Broyden_Algorithm','Broyden Algorithm')+'<br/>') +
		html_end()
		)
	
	xom.addAttribute(at_algorithm)
	# Algorithm / Linear
	xom.addAttribute(at_Linear)
	xom.addAttribute(at_use_formTangent_Linear)
	xom.addAttribute(at_formTangent_Linear)
	xom.addAttribute(at_factorOnce)
	# Algorithm / Newton
	xom.addAttribute(at_Newton)
	xom.addAttribute(at_use_formTangent_Newton)
	xom.addAttribute(at_formTangent_Newton)
	# Algorithm / NewtonLineSearch
	xom.addAttribute(at_NewtonLineSearch)
	xom.addAttribute(at_type)
	xom.addAttribute(at_typeSearch)
	xom.addAttribute(at_use_tol)
	xom.addAttribute(at_tol)
	xom.addAttribute(at_use_maxIter)
	xom.addAttribute(at_maxIter)
	xom.addAttribute(at_use_minEta)
	xom.addAttribute(at_minEta)
	xom.addAttribute(at_use_maxEta)
	xom.addAttribute(at_maxEta)
	# Algorithm / ModifiedNewton
	xom.addAttribute(at_ModifiedNewton)
	xom.addAttribute(at_use_formTangent_ModifiedNewton)
	xom.addAttribute(at_formTangent_ModifiedNewton)
	# Algorithm / KrylovNewton
	xom.addAttribute(at_KrylovNewton)
	xom.addAttribute(at_iterate_KrylovNewton)
	xom.addAttribute(at_tangIter_KrylovNewton)
	xom.addAttribute(at_increment_KrylovNewton)
	xom.addAttribute(at_tangIncr_KrylovNewton)
	xom.addAttribute(at_use_maxDim_KrylovNewton)
	xom.addAttribute(at_maxDim_KrylovNewton)
	# Algorithm / SecantNewton
	xom.addAttribute(at_SecantNewton)
	xom.addAttribute(at_iterate_SecantNewton)
	xom.addAttribute(at_tangIter_SecantNewton)
	xom.addAttribute(at_increment_SecantNewton)
	xom.addAttribute(at_tangIncr_SecantNewton)
	xom.addAttribute(at_use_maxDim_SecantNewton)
	xom.addAttribute(at_maxDim_SecantNewton)
	# Algorithm / BFGS
	xom.addAttribute(at_BFGS)
	xom.addAttribute(at_use_formTangent_BFGS)
	xom.addAttribute(at_formTangent_BFGS)
	xom.addAttribute(at_use_count_BFGS)
	xom.addAttribute(at_count_BFGS)
	# Algorithm / Broyden
	xom.addAttribute(at_Broyden)
	xom.addAttribute(at_use_formTangent_Broyden)
	xom.addAttribute(at_formTangent_Broyden)
	xom.addAttribute(at_use_count_Broyden)
	xom.addAttribute(at_count_Broyden)
	
	
	# visibility dependencies / Linear
	xom.setVisibilityDependency(at_Linear, at_use_formTangent_Linear)
	xom.setVisibilityDependency(at_Linear, at_formTangent_Linear)
	xom.setVisibilityDependency(at_Linear, at_factorOnce)
	
	xom.setVisibilityDependency(at_use_formTangent_Linear, at_formTangent_Linear)
	
	# visibility dependencies / Newton
	xom.setVisibilityDependency(at_Newton, at_use_formTangent_Newton)
	xom.setVisibilityDependency(at_Newton, at_formTangent_Newton)
	
	xom.setVisibilityDependency(at_use_formTangent_Newton, at_formTangent_Newton)
	
	# visibility dependencies / NewtonLineSearch
	xom.setVisibilityDependency(at_NewtonLineSearch, at_type)
	xom.setVisibilityDependency(at_NewtonLineSearch, at_use_tol)
	xom.setVisibilityDependency(at_NewtonLineSearch, at_use_maxIter)
	xom.setVisibilityDependency(at_NewtonLineSearch, at_use_minEta)
	xom.setVisibilityDependency(at_NewtonLineSearch, at_use_maxEta)
	
	xom.setVisibilityDependency(at_NewtonLineSearch, at_typeSearch)
	xom.setVisibilityDependency(at_type, at_typeSearch)
	xom.setVisibilityDependency(at_NewtonLineSearch, at_tol)
	xom.setVisibilityDependency(at_use_tol, at_tol)
	xom.setVisibilityDependency(at_NewtonLineSearch, at_maxIter)
	xom.setVisibilityDependency(at_use_maxIter, at_maxIter)
	xom.setVisibilityDependency(at_NewtonLineSearch, at_minEta)
	xom.setVisibilityDependency(at_use_minEta, at_minEta)
	xom.setVisibilityDependency(at_NewtonLineSearch, at_maxEta)
	xom.setVisibilityDependency(at_use_maxEta, at_maxEta)
	
	# visibility dependencies / ModifiedNewton
	xom.setVisibilityDependency(at_ModifiedNewton, at_use_formTangent_ModifiedNewton)
	
	xom.setVisibilityDependency(at_ModifiedNewton, at_formTangent_ModifiedNewton)
	xom.setVisibilityDependency(at_use_formTangent_ModifiedNewton, at_formTangent_ModifiedNewton)
	
	# visibility dependencies / KrylovNewton
	xom.setVisibilityDependency(at_KrylovNewton, at_iterate_KrylovNewton)
	xom.setVisibilityDependency(at_KrylovNewton, at_increment_KrylovNewton)
	xom.setVisibilityDependency(at_KrylovNewton, at_use_maxDim_KrylovNewton)
	
	xom.setVisibilityDependency(at_KrylovNewton, at_tangIter_KrylovNewton)
	xom.setVisibilityDependency(at_iterate_KrylovNewton, at_tangIter_KrylovNewton)
	xom.setVisibilityDependency(at_KrylovNewton, at_tangIncr_KrylovNewton)
	xom.setVisibilityDependency(at_increment_KrylovNewton, at_tangIncr_KrylovNewton)
	xom.setVisibilityDependency(at_KrylovNewton, at_maxDim_KrylovNewton)
	xom.setVisibilityDependency(at_use_maxDim_KrylovNewton, at_maxDim_KrylovNewton)
	
	# visibility dependencies / SecantNewton
	xom.setVisibilityDependency(at_SecantNewton, at_iterate_SecantNewton)
	xom.setVisibilityDependency(at_SecantNewton, at_increment_SecantNewton)
	xom.setVisibilityDependency(at_SecantNewton, at_use_maxDim_SecantNewton)
	
	xom.setVisibilityDependency(at_SecantNewton, at_tangIter_SecantNewton)
	xom.setVisibilityDependency(at_iterate_SecantNewton, at_tangIter_SecantNewton)
	xom.setVisibilityDependency(at_SecantNewton, at_tangIncr_SecantNewton)
	xom.setVisibilityDependency(at_increment_SecantNewton, at_tangIncr_SecantNewton)
	xom.setVisibilityDependency(at_SecantNewton, at_maxDim_SecantNewton)
	xom.setVisibilityDependency(at_use_maxDim_SecantNewton, at_maxDim_SecantNewton)
	
	# visibility dependencies / BFGS
	xom.setVisibilityDependency(at_BFGS, at_use_formTangent_BFGS)
	xom.setVisibilityDependency(at_BFGS, at_use_count_BFGS)
	
	xom.setVisibilityDependency(at_BFGS, at_formTangent_BFGS)
	xom.setVisibilityDependency(at_use_formTangent_BFGS, at_formTangent_BFGS)
	xom.setVisibilityDependency(at_BFGS, at_count_BFGS)
	xom.setVisibilityDependency(at_use_count_BFGS, at_count_BFGS)
	
	# visibility dependencies / Broyden
	xom.setVisibilityDependency(at_Broyden, at_use_formTangent_Broyden)
	xom.setVisibilityDependency(at_Broyden, at_use_count_Broyden)
	
	xom.setVisibilityDependency(at_Broyden, at_formTangent_Broyden)
	xom.setVisibilityDependency(at_use_formTangent_Broyden, at_formTangent_Broyden)
	xom.setVisibilityDependency(at_Broyden, at_count_Broyden)
	xom.setVisibilityDependency(at_use_count_Broyden, at_count_Broyden)
	
	
	# auto-exclusive dependencies
	# algorithm
	xom.setBooleanAutoExclusiveDependency(at_algorithm, at_Linear)
	xom.setBooleanAutoExclusiveDependency(at_algorithm, at_Newton)
	xom.setBooleanAutoExclusiveDependency(at_algorithm, at_NewtonLineSearch)
	xom.setBooleanAutoExclusiveDependency(at_algorithm, at_ModifiedNewton)
	xom.setBooleanAutoExclusiveDependency(at_algorithm, at_KrylovNewton)
	xom.setBooleanAutoExclusiveDependency(at_algorithm, at_SecantNewton)
	xom.setBooleanAutoExclusiveDependency(at_algorithm, at_BFGS)
	xom.setBooleanAutoExclusiveDependency(at_algorithm, at_Broyden)

def writeTcl_algorithm(pinfo, xobj):
	
	'''
	algorithm Linear <-secant> <-initial> <-factorOnce>
	algorithm Newton <-secant> <-initial> <-initialThenCurrent>
	algorithm NewtonLineSearch <-type $typeSearch> <-tol $tol> <-maxIter $maxIter> <-minEta $minEta> <-maxEta $maxEta>
	algorithm ModifiedNewton <-secant> <-initial>
	algorithm KrylovNewton <-iterate $tangIter> <-increment $tangIncr> <-maxDim $maxDim>
	algorithm SecantNewton <-iterate $tangIter> <-increment $tangIncr> <-maxDim $maxDim>
	algorithm BFGS <-secant> <-initial> <-count>
	algorithm Broyden <$count>
	'''
	
	sopt = ''
	
	algorithm_at = xobj.getAttribute('algorithm')
	if(algorithm_at is None):
		raise Exception('Error: cannot find "algorithm" attribute')
	algorithm = algorithm_at.string
	
	if algorithm == 'Linear':
		use_formTangent_at = xobj.getAttribute('use_formTangent/Linear')
		if(use_formTangent_at is None):
			raise Exception('Error: cannot find "use_formTangent" attribute')
		if use_formTangent_at.boolean:
			formTangent_at = xobj.getAttribute('formTangent/Linear')
			if(formTangent_at is None):
				raise Exception('Error: cannot find "formTangent" attribute')
			formTangent = formTangent_at.string
			
			sopt += ' {}'.format(formTangent)
		
		factorOnce_at = xobj.getAttribute('-factorOnce')
		if(factorOnce_at is None):
			raise Exception('Error: cannot find "-factorOnce" attribute')
		if factorOnce_at.boolean:
			sopt += ' -factorOnce'
		
		str_tcl = '{}algorithm Linear{}\n'.format(pinfo.indent, sopt)
	
	elif algorithm == 'Newton':
		use_formTangent_at = xobj.getAttribute('use_formTangent/Newton')
		if(use_formTangent_at is None):
			raise Exception('Error: cannot find "use_formTangent" attribute')
		if use_formTangent_at.boolean:
			formTangent_at = xobj.getAttribute('formTangent/Newton')
			if(formTangent_at is None):
				raise Exception('Error: cannot find "formTangent" attribute')
			formTangent = formTangent_at.string
			
			sopt += ' {}'.format(formTangent)
		
		str_tcl = '{}algorithm Newton{}\n'.format(pinfo.indent, sopt)
	
	elif algorithm == 'Newton with Line Search':
		type_at = xobj.getAttribute('-type')
		if(type_at is None):
			raise Exception('Error: cannot find "-type" attribute')
		if type_at.boolean:
			typeSearch_at = xobj.getAttribute('typeSearch')
			if(typeSearch_at is None):
				raise Exception('Error: cannot find "typeSearch" attribute')
			typeSearch = typeSearch_at.string
			
			sopt += ' -type {}'.format(typeSearch)
		
		use_tol_at = xobj.getAttribute('-tol')
		if(use_tol_at is None):
			raise Exception('Error: cannot find "-tol" attribute')
		if use_tol_at.boolean:
			tol_at = xobj.getAttribute('tol')
			if(tol_at is None):
				raise Exception('Error: cannot find "tol" attribute')
			tol = tol_at.real
			
			sopt += ' -tol {}'.format(tol)
		
		use_maxIter_at = xobj.getAttribute('-maxIter')
		if(use_maxIter_at is None):
			raise Exception('Error: cannot find "-maxIter" attribute')
		if use_maxIter_at.boolean:
			maxIter_at = xobj.getAttribute('maxIter')
			if(maxIter_at is None):
				raise Exception('Error: cannot find "maxIter" attribute')
			maxIter = maxIter_at.integer
			
			sopt += ' -maxIter {}'.format(maxIter)
		
		use_minEta_at = xobj.getAttribute('-minEta')
		if(use_minEta_at is None):
			raise Exception('Error: cannot find "-minEta" attribute')
		if use_minEta_at.boolean:
			minEta_at = xobj.getAttribute('minEta')
			if(minEta_at is None):
				raise Exception('Error: cannot find "minEta" attribute')
			minEta = minEta_at.real
			
			sopt += ' -minEta {}'.format(minEta)
		
		use_maxEta_at = xobj.getAttribute('-maxEta')
		if(use_maxEta_at is None):
			raise Exception('Error: cannot find "-maxEta" attribute')
		if use_maxEta_at.boolean:
			maxEta_at = xobj.getAttribute('maxEta')
			if(maxEta_at is None):
				raise Exception('Error: cannot find "maxEta" attribute')
			maxEta = maxEta_at.real
			
			sopt += ' -maxEta {}'.format(maxEta)
		
		str_tcl = '{}algorithm NewtonLineSearch{}\n'.format(pinfo.indent, sopt)
	
	elif algorithm == 'Modified Newton':
		use_formTangent_at = xobj.getAttribute('use_formTangent/ModifiedNewton')
		if(use_formTangent_at is None):
			raise Exception('Error: cannot find "use_formTangent" attribute')
		if use_formTangent_at.boolean:
			formTangent_at = xobj.getAttribute('formTangent/ModifiedNewton')
			if(formTangent_at is None):
				raise Exception('Error: cannot find "formTangent" attribute')
			formTangent = formTangent_at.string
			
			sopt += ' {}'.format(formTangent)
		
		str_tcl = '{}algorithm ModifiedNewton{}\n'.format(pinfo.indent, sopt)
	
	elif algorithm == 'Krylov-Newton':
		iterate_at = xobj.getAttribute('-iterate/KrylovNewton')
		if(iterate_at is None):
			raise Exception('Error: cannot find "-iterate" attribute')
		if iterate_at.boolean:
			tangIter_at = xobj.getAttribute('tangIter/KrylovNewton')
			if(tangIter_at is None):
				raise Exception('Error: cannot find "tangIter" attribute')
			tangIter = tangIter_at.string
			
			sopt += ' -iterate {}'.format(tangIter)
		
		increment_at = xobj.getAttribute('-increment/KrylovNewton')
		if(increment_at is None):
			raise Exception('Error: cannot find "-increment" attribute')
		if increment_at.boolean:
			tangIncr_at = xobj.getAttribute('tangIncr/KrylovNewton')
			if(tangIncr_at is None):
				raise Exception('Error: cannot find "tangIncr" attribute')
			tangIncr = tangIncr_at.string
			
			sopt += ' -increment {}'.format(tangIncr)
		
		use_maxDim_at = xobj.getAttribute('-maxDim/KrylovNewton')
		if(use_maxDim_at is None):
			raise Exception('Error: cannot find "-maxDim" attribute')
		if use_maxDim_at.boolean:
			maxDim_at = xobj.getAttribute('maxDim/KrylovNewton')
			if(maxDim_at is None):
				raise Exception('Error: cannot find "maxDim" attribute')
			maxDim = maxDim_at.integer
			
			sopt += ' -maxDim {}'.format(maxDim)
		
		str_tcl = '{}algorithm KrylovNewton{}\n'.format(pinfo.indent, sopt)
	
	elif algorithm == 'Secant Newton':
		iterate_at = xobj.getAttribute('-iterate/SecantNewton')
		if(iterate_at is None):
			raise Exception('Error: cannot find "-iterate" attribute')
		if iterate_at.boolean:
			tangIter_at = xobj.getAttribute('tangIter/SecantNewton')
			if(tangIter_at is None):
				raise Exception('Error: cannot find "tangIter" attribute')
			tangIter = tangIter_at.string
			
			sopt += ' -iterate {}'.format(tangIter)
		
		increment_at = xobj.getAttribute('-increment/SecantNewton')
		if(increment_at is None):
			raise Exception('Error: cannot find "-increment" attribute')
		if increment_at.boolean:
			tangIncr_at = xobj.getAttribute('tangIncr/SecantNewton')
			if(tangIncr_at is None):
				raise Exception('Error: cannot find "tangIncr" attribute')
			tangIncr = tangIncr_at.string
			
			sopt += ' -increment {}'.format(tangIncr)
		
		use_maxDim_at = xobj.getAttribute('-maxDim/SecantNewton')
		if(use_maxDim_at is None):
			raise Exception('Error: cannot find "-maxDim" attribute')
		if use_maxDim_at.boolean:
			maxDim_at = xobj.getAttribute('maxDim/SecantNewton')
			if(maxDim_at is None):
				raise Exception('Error: cannot find "maxDim" attribute')
			maxDim = maxDim_at.integer
			
			sopt += ' -maxDim {}'.format(maxDim)
		
		str_tcl = '{}algorithm SecantNewton{}\n'.format(pinfo.indent, sopt)
	
	elif algorithm == 'BFGS':
		use_formTangent_at = xobj.getAttribute('use_formTangent/BFGS')
		if(use_formTangent_at is None):
			raise Exception('Error: cannot find "use_formTangent" attribute')
		if use_formTangent_at.boolean:
			formTangent_at = xobj.getAttribute('formTangent/BFGS')
			if(formTangent_at is None):
				raise Exception('Error: cannot find "formTangent" attribute')
			formTangent = formTangent_at.string
			
			sopt += ' {}'.format(formTangent)
		
		use_count_at = xobj.getAttribute('-count/BFGS')
		if(use_count_at is None):
			raise Exception('Error: cannot find "-count" attribute')
		if use_count_at.boolean:
			count_at = xobj.getAttribute('count/BFGS')
			if(count_at is None):
				raise Exception('Error: cannot find "count" attribute')
			count = count_at.integer
			
			sopt += ' -count {}'.format(count)
		
		str_tcl = '{}algorithm BFGS{}\n'.format(pinfo.indent, sopt)
	
	elif algorithm == 'Broyden':
		use_formTangent_at = xobj.getAttribute('use_formTangent/Broyden')
		if(use_formTangent_at is None):
			raise Exception('Error: cannot find "use_formTangent" attribute')
		if use_formTangent_at.boolean:
			formTangent_at = xobj.getAttribute('formTangent/Broyden')
			if(formTangent_at is None):
				raise Exception('Error: cannot find "formTangent" attribute')
			formTangent = formTangent_at.string
			
			sopt += ' {}'.format(formTangent)
		
		use_count_at = xobj.getAttribute('-count/Broyden')
		if(use_count_at is None):
			raise Exception('Error: cannot find "-count" attribute')
		if use_count_at.boolean:
			count_at = xobj.getAttribute('count/Broyden')
			if(count_at is None):
				raise Exception('Error: cannot find "count" attribute')
			count = count_at.integer
			
			sopt += ' -count {}'.format(count)
		
		str_tcl = '{}algorithm Broyden{}\n'.format(pinfo.indent, sopt)
	
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)