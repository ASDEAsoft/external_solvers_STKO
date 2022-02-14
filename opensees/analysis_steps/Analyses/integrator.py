from PyMpc import *
from mpc_utils_html import *

def integratorCommand(xom):
	
	visibleOptional = False
	notVisibleForNewAnalysis = False

	# booleanStaticIntegrators
	at_booleanStaticIntegrators = MpcAttributeMetaData()
	at_booleanStaticIntegrators.type = MpcAttributeType.Boolean
	at_booleanStaticIntegrators.name = 'Static'
	at_booleanStaticIntegrators.group = 'integrator'
	at_booleanStaticIntegrators.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Static')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Integrator_Command','Integrator Command')+'<br/>') +
		html_end()
		)
	at_booleanStaticIntegrators.editable = False
	
	# staticIntegrators
	at_staticIntegrators = MpcAttributeMetaData()
	at_staticIntegrators.type = MpcAttributeType.String
	at_staticIntegrators.name = 'staticIntegrators'
	at_staticIntegrators.group = 'integrator'
	at_staticIntegrators.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('staticIntegrators')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Integrator_Command','Integrator Command')+'<br/>') +
		html_end()
		)
	at_staticIntegrators.sourceType = MpcAttributeSourceType.List
	at_staticIntegrators.setSourceList(['Load Control', 'Displacement Control', 'Parallel Displacement Control', 'Minimum Unbalanced Displacement Norm','Arc-Length Control', 'EQPath', 'HSConstraint'])
	at_staticIntegrators.setDefault('Load Control')
	
	# booleanTransientIntegrators
	at_booleanTransientIntegrators = MpcAttributeMetaData()
	at_booleanTransientIntegrators.type = MpcAttributeType.Boolean
	at_booleanTransientIntegrators.name = 'Transient'
	at_booleanTransientIntegrators.group = 'integrator'
	at_booleanTransientIntegrators.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Transient')+'<br/>') + 
		html_par('transientIntegrators') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Integrator_Command','Integrator Command')+'<br/>') +
		html_end()
		)
	at_booleanTransientIntegrators.editable = False
	
	# transientIntegrators
	at_transientIntegrators = MpcAttributeMetaData()
	at_transientIntegrators.type = MpcAttributeType.String
	at_transientIntegrators.name = 'transientIntegrators'
	at_transientIntegrators.group = 'integrator'
	at_transientIntegrators.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('transientIntegrators')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Integrator_Command','Integrator Command')+'<br/>') +
		html_end()
		)
	at_transientIntegrators.sourceType = MpcAttributeSourceType.List
	at_transientIntegrators.setSourceList(['Central Difference', 'Newmark Method', 'Hilber-Hughes-Taylor Method', 'Generalized Alpha Method', 'TRBDF2',
									   'Explicit Difference', 'AlphaOS_TP', 'AlphaOSGeneralized_TP', 'HHT_TP', 'HHTExplicit_TP', 'HHTGeneralizedExplicit_TP', 'KRAlphaExplicit_TP',
									   'Newmark Explicit'])
	at_transientIntegrators.setDefault('Central Difference')
	
	#-------------------------------------------------Static Integrators-------------------------------------------------
	
	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------Load Control------------------------------------------
	
	# integrator LoadControl $lambda <$numIter $minLambda $maxLambda>
	
	# loadControl
	at_loadControl = MpcAttributeMetaData()
	at_loadControl.type = MpcAttributeType.Boolean
	at_loadControl.name = 'Load Control'
	at_loadControl.group = 'integrator'
	at_loadControl.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('loadControl')+'<br/>') + 
		html_par('Load Control') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Load_Control','Load Control')+'<br/>') +
		html_end()
		)
	at_loadControl.editable = False
	
	# lambda
	at_lambda = MpcAttributeMetaData()
	at_lambda.type = MpcAttributeType.Real
	at_lambda.name = 'lambda'
	at_lambda.group = 'integrator'
	at_lambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('the load factor increment &lambda;') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Load_Control','Load Control')+'<br/>') +
		html_end()
		)
	at_lambda.setDefault(0.1)
	at_lambda.editable = notVisibleForNewAnalysis
	
	# lambdatot
	at_lambda_tot = MpcAttributeMetaData()
	at_lambda_tot.type = MpcAttributeType.Real
	at_lambda_tot.name = 'duration'
	at_lambda_tot.group = 'integrator'
	at_lambda_tot.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('The total duration of the analysis. For Load Control it is the total final load factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Load_Control','Load Control')+'<br/>') +
		html_end()
		)
	at_lambda_tot.setDefault(1.0)
	
	# optional
	at_Optional_LoadControl = MpcAttributeMetaData()
	at_Optional_LoadControl.type = MpcAttributeType.Boolean
	at_Optional_LoadControl.name = 'Optional LoadControl'
	at_Optional_LoadControl.group = 'integrator'
	at_Optional_LoadControl.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional LoadControl')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Load_Control','Load Control')+'<br/>') +
		html_end()
		)
	at_Optional_LoadControl.setDefault(False)
	at_Optional_LoadControl.editable = visibleOptional
	
	# numIter
	at_numIter = MpcAttributeMetaData()
	at_numIter.type = MpcAttributeType.Integer
	at_numIter.name = 'numIter'
	at_numIter.group = 'integrator'
	at_numIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIter')+'<br/>') +
		html_par('the number of iterations the user would like to occur in the solution algorithm. Optional, default = 1.0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Load_Control','Load Control')+'<br/>') +
		html_end()
		)
	
	# minLambda
	at_minLambda = MpcAttributeMetaData()
	at_minLambda.type = MpcAttributeType.Real
	at_minLambda.name = 'minLambda'
	at_minLambda.group = 'integrator'
	at_minLambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('minLambda')+'<br/>') +
		html_par('the min stepsize the user will allow. optional, defualt = &lambda;min = &lambda;') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Load_Control','Load Control')+'<br/>') +
		html_end()
		)
	
	# maxLambda
	at_maxLambda = MpcAttributeMetaData()
	at_maxLambda.type = MpcAttributeType.Real
	at_maxLambda.name = 'maxLambda'
	at_maxLambda.group = 'integrator'
	at_maxLambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxLambda')+'<br/>') +
		html_par('the man stepsize the user will allow. optional, defualt = &lambda;max = &lambda;') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Load_Control','Load Control')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#--------------------------------------------Parallel Displacement Control----------------------------------
	
	# integrator parallelDisplacementControl $node $dof $incr <$numIter $&Delta;Umin $&Delta;Umax>
	# parallelDisplacementControl
	at_parallelDisplacementControl = MpcAttributeMetaData()
	at_parallelDisplacementControl.type = MpcAttributeType.Boolean
	at_parallelDisplacementControl.name = 'Parallel Displacement Control'
	at_parallelDisplacementControl.group = 'integrator'
	at_parallelDisplacementControl.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('parallelDisplacementControl')+'<br/>') + 
		html_par('Displacement Control') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	at_parallelDisplacementControl.editable = False
	
	# node
	at_parallelNode = MpcAttributeMetaData()
	at_parallelNode.type = MpcAttributeType.Index
	at_parallelNode.name = 'SelectionSet/parallelDisplacementControl'
	at_parallelNode.group = 'integrator'
	at_parallelNode.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('node')+'<br/>') +
		html_par((
			'Node whose response controls solution.<br/>'
			'Choose a selection set that contains just 1 vertex. '
			'The node generated for that vertex will be used.'
			)) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	at_parallelNode.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	# dof
	at_parallelDof = MpcAttributeMetaData()
	at_parallelDof.type = MpcAttributeType.Integer
	at_parallelDof.name = 'dof/parallelDisplacementControl'
	at_parallelDof.group = 'integrator'
	at_parallelDof.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dof')+'<br/>') +
		html_par('degree of freedom at the node, valid options: 1 through ndf at node') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	
	# incr
	at_parallelIncr = MpcAttributeMetaData()
	at_parallelIncr.type = MpcAttributeType.Real
	at_parallelIncr.name = 'incr/parallelDisplacementControl'
	at_parallelIncr.group = 'integrator'
	at_parallelIncr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('incr')+'<br/>') +
		html_par('first displacement increment &Delta;Udof') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	at_parallelIncr.editable = notVisibleForNewAnalysis
	
	# cyclic
	at_parallelCyclic = MpcAttributeMetaData()
	at_parallelCyclic.type = MpcAttributeType.Boolean
	at_parallelCyclic.name = 'Cyclic/parallelDisplacementControl'
	at_parallelCyclic.group = 'integrator'
	at_parallelCyclic.setDefault(False)
	at_parallelCyclic.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Cyclic')+'<br/>') +
		html_par('If checked, you can specify a time series of type "Path" containing multiple values of target displacement. Those values will be used as the cyclic target displacement history') +
		html_end()
		)
	
	#target displacement
	at_parallelTargetDisp = MpcAttributeMetaData()
	at_parallelTargetDisp.type = MpcAttributeType.Real
	at_parallelTargetDisp.name = 'Target Displacement/parallelDisplacementControl'
	at_parallelTargetDisp.group = 'integrator'
	at_parallelTargetDisp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Target Displacement')+'<br/>') +
		html_par('The target (final) displacement value for the selected node DOF') +
		html_end()
		)
	
	# # tsTagAccel
	at_parallel_tsTag = MpcAttributeMetaData()
	at_parallel_tsTag.type = MpcAttributeType.Index
	at_parallel_tsTag.name = 'Target Displacement History/parallelDisplacementControl'
	at_parallel_tsTag.group = 'integrator'
	at_parallel_tsTag.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_parallel_tsTag.indexSource.addAllowedNamespace("timeSeries")
	at_parallel_tsTag.indexSource.addAllowedClass("Path")
	at_parallel_tsTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Target Displacement History')+'<br/>') +
		html_par('A Path TimeSeries that defines the cyclic target displacement history') +
		html_end()
		)
	
	# optional
	at_Optional_parallelDisplacementControl = MpcAttributeMetaData()
	at_Optional_parallelDisplacementControl.type = MpcAttributeType.Boolean
	at_Optional_parallelDisplacementControl.name = 'Optional parallelDisplacementControl/parallelDisplacementControl'
	at_Optional_parallelDisplacementControl.group = 'integrator'
	at_Optional_parallelDisplacementControl.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional LoadControl')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	at_Optional_parallelDisplacementControl.setDefault(False)
	at_Optional_parallelDisplacementControl.editable = visibleOptional
	
	# numIter
	at_parallelNumIter_1 = MpcAttributeMetaData()
	at_parallelNumIter_1.type = MpcAttributeType.Integer
	at_parallelNumIter_1.name = 'numIter/parallelDisplacementControl'
	at_parallelNumIter_1.group = 'integrator'
	at_parallelNumIter_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIter')+'<br/>') +
		html_par('the number of iterations the user would like to occur in the solution algorithm. Optional, default = 1.0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	
	# deltaUmin
	at_parallelDeltaUmin = MpcAttributeMetaData()
	at_parallelDeltaUmin.type = MpcAttributeType.Real
	at_parallelDeltaUmin.name = 'delta U min/parallelDisplacementControl'
	at_parallelDeltaUmin.group = 'integrator'
	at_parallelDeltaUmin.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('deltaUmin')+'<br/>') +
		html_par('the min stepsize the user will allow. optional, default = &Delta;Umin = &Delta;U0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	
	# deltaUmax
	at_parallelDeltaUmax = MpcAttributeMetaData()
	at_parallelDeltaUmax.type = MpcAttributeType.Real
	at_parallelDeltaUmax.name = 'delta U max/parallelDisplacementControl'
	at_parallelDeltaUmax.group = 'integrator'
	at_parallelDeltaUmax.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('deltaUmax')+'<br/>') +
		html_par('the max stepsize the user will allow. optional, default = &Delta;Umax = &Delta;U0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------Displacement Control----------------------------------
	
	#integrator DisplacementControl $node $dof $incr <$numIter $&Delta;Umin $&Delta;Umax>
	
	# displacementControl
	at_displacementControl = MpcAttributeMetaData()
	at_displacementControl.type = MpcAttributeType.Boolean
	at_displacementControl.name = 'Displacement Control'
	at_displacementControl.group = 'integrator'
	at_displacementControl.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('DisplacementControl')+'<br/>') + 
		html_par('Displacement Control') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	at_displacementControl.editable = False
	
	# node
	at_node = MpcAttributeMetaData()
	at_node.type = MpcAttributeType.Index
	at_node.name = 'SelectionSet'
	at_node.group = 'integrator'
	at_node.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('node')+'<br/>') +
		html_par((
			'Node whose response controls solution.<br/>'
			'Choose a selection set that contains just 1 vertex. '
			'The node generated for that vertex will be used.'
			)) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	at_node.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	# dof
	at_dof = MpcAttributeMetaData()
	at_dof.type = MpcAttributeType.Integer
	at_dof.name = 'dof'
	at_dof.group = 'integrator'
	at_dof.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dof')+'<br/>') +
		html_par('degree of freedom at the node, valid options: 1 through ndf at node') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	
	# incr
	at_incr = MpcAttributeMetaData()
	at_incr.type = MpcAttributeType.Real
	at_incr.name = 'incr'
	at_incr.group = 'integrator'
	at_incr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('incr')+'<br/>') +
		html_par('first displacement increment &Delta;Udof') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	at_incr.editable = notVisibleForNewAnalysis
	
	# cyclic
	at_Cyclic = MpcAttributeMetaData()
	at_Cyclic.type = MpcAttributeType.Boolean
	at_Cyclic.name = 'Cyclic'
	at_Cyclic.group = 'integrator'
	at_Cyclic.setDefault(False)
	at_Cyclic.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Cyclic')+'<br/>') +
		html_par('If checked, you can specify a time series of type "Path" containing multiple values of target displacement. Those values will be used as the cyclic target displacement history') +
		html_end()
		)
	
	# target displacement
	at_TargetDisp = MpcAttributeMetaData()
	at_TargetDisp.type = MpcAttributeType.Real
	at_TargetDisp.name = 'Target Displacement'
	at_TargetDisp.group = 'integrator'
	at_TargetDisp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Target Displacement')+'<br/>') +
		html_par('The target (final) displacement value for the selected node DOF') +
		html_end()
		)
	
	# # tsTagAccel
	at_tsTag = MpcAttributeMetaData()
	at_tsTag.type = MpcAttributeType.Index
	at_tsTag.name = 'Target Displacement History'
	at_tsTag.group = 'integrator'
	at_tsTag.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_tsTag.indexSource.addAllowedNamespace("timeSeries")
	at_tsTag.indexSource.addAllowedClass("Path")
	at_tsTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Target Displacement History')+'<br/>') +
		html_par('A Path TimeSeries that defines the cyclic target displacement history') +
		html_end()
		)
	
	# optional
	at_Optional_DisplacementControl = MpcAttributeMetaData()
	at_Optional_DisplacementControl.type = MpcAttributeType.Boolean
	at_Optional_DisplacementControl.name = 'Optional DisplacementControl'
	at_Optional_DisplacementControl.group = 'integrator'
	at_Optional_DisplacementControl.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional LoadControl')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	at_Optional_DisplacementControl.setDefault(False)
	at_Optional_DisplacementControl.editable = visibleOptional
	
	# numIter
	at_numIter_1 = MpcAttributeMetaData()
	at_numIter_1.type = MpcAttributeType.Integer
	at_numIter_1.name = 'numIter/DisplacementControl'
	at_numIter_1.group = 'integrator'
	at_numIter_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIter')+'<br/>') +
		html_par('the number of iterations the user would like to occur in the solution algorithm. Optional, default = 1.0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	
	# deltaUmin
	at_deltaUmin = MpcAttributeMetaData()
	at_deltaUmin.type = MpcAttributeType.Real
	at_deltaUmin.name = 'delta U min'
	at_deltaUmin.group = 'integrator'
	at_deltaUmin.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('deltaUmin')+'<br/>') +
		html_par('the min stepsize the user will allow. optional, defualt = delta Umin = deltaU0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	
	# deltaUmax
	at_deltaUmax = MpcAttributeMetaData()
	at_deltaUmax.type = MpcAttributeType.Real
	at_deltaUmax.name = 'delta U max'
	at_deltaUmax.group = 'integrator'
	at_deltaUmax.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('deltaUmax')+'<br/>') +
		html_par('the max stepsize the user will allow. optional, default = delta Umax = delta U0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------Minimum Unbalanced Displacement Norm-----------------------------------
	
	# integrator MinUnbalDispNorm $dlambda1 <$Jd $minLambda $maxLambda>
	
	# MinUnbalDispNorm
	at_MinUnbalDispNorm = MpcAttributeMetaData()
	at_MinUnbalDispNorm.type = MpcAttributeType.Boolean
	at_MinUnbalDispNorm.name = 'Minimum Unbalanced Displacement Norm'
	at_MinUnbalDispNorm.group = 'integrator'
	at_MinUnbalDispNorm.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('MinUnbalDispNorm')+'<br/>') + 
		html_par('Minimum Unbalanced Displacement Norm') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Minimum_Unbalanced_Displacement_Norm','Minimum Unbalanced Displacement Norm')+'<br/>') +
		html_end()
		)
	at_MinUnbalDispNorm.editable = False
	
	# dlambda1
	at_dlambda1 = MpcAttributeMetaData()
	at_dlambda1.type = MpcAttributeType.Real
	at_dlambda1.name = 'dlambda1'
	at_dlambda1.group = 'integrator'
	at_dlambda1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dlambda1')+'<br/>') +
		html_par('first load increment (pseudo-time step) at the first iteration in the next invocation of the analysis command') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Minimum_Unbalanced_Displacement_Norm','Minimum Unbalanced Displacement Norm')+'<br/>') +
		html_end()
		)
	at_dlambda1.setDefault(0.1)
	
	# optional
	at_Optional_MinUnbalDispNorm = MpcAttributeMetaData()
	at_Optional_MinUnbalDispNorm.type = MpcAttributeType.Boolean
	at_Optional_MinUnbalDispNorm.name = 'Optional MinUnbalDispNorm'
	at_Optional_MinUnbalDispNorm.group = 'integrator'
	at_Optional_MinUnbalDispNorm.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional LoadControl')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Minimum_Unbalanced_Displacement_Norm','Minimum Unbalanced Displacement Norm')+'<br/>') +
		html_end()
		)
	at_Optional_MinUnbalDispNorm.setDefault(False)
	at_Optional_MinUnbalDispNorm.editable = visibleOptional
	
	# Jd
	at_Jd_integrator = MpcAttributeMetaData()
	at_Jd_integrator.type = MpcAttributeType.Real
	at_Jd_integrator.name = 'Jd/integrator'
	at_Jd_integrator.group = 'integrator'
	at_Jd_integrator.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Jd')+'<br/>') +
		html_par('factor relating first load increment at subsequent time steps') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Minimum_Unbalanced_Displacement_Norm','Minimum Unbalanced Displacement Norm')+'<br/>') +
		html_end()
		)
	at_Jd_integrator.setDefault(1.0)
	
	# minLambda
	at_minLambda_1 = MpcAttributeMetaData()
	at_minLambda_1.type = MpcAttributeType.Real
	at_minLambda_1.name = 'minLambda/MinUnbalDispNorm'
	at_minLambda_1.group = 'integrator'
	at_minLambda_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('minLambda')+'<br/>') +
		html_par('the min stepsize the user will allow. optional, defualt = &lambda;min = &lambda;') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Load_Control','Load Control')+'<br/>') +
		html_end()
		)
	
	# maxLambda
	at_maxLambda_1 = MpcAttributeMetaData()
	at_maxLambda_1.type = MpcAttributeType.Real
	at_maxLambda_1.name = 'maxLambda/MinUnbalDispNorm'
	at_maxLambda_1.group = 'integrator'
	at_maxLambda_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxLambda ')+'<br/>') +
		html_par('the man stepsize the user will allow. optional, defualt = &lambda;max = &lambda;') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Load_Control','Load Control')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------------Arc-Length Control-----------------------------------------
	
	# integrator ArcLength $s $alpha
	
	# Arc-Length Control
	at_ArcLength = MpcAttributeMetaData()
	at_ArcLength.type = MpcAttributeType.Boolean
	at_ArcLength.name = 'Arc-Length Control'
	at_ArcLength.group = 'integrator'
	at_ArcLength.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('MinUnbalDispNorm')+'<br/>') + 
		html_par('Arc-Length Control') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Arc-Length_Control','Arc-Length Control')+'<br/>') +
		html_end()
		)
	at_ArcLength.editable = False
	
	#s
	at_s = MpcAttributeMetaData()
	at_s.type = MpcAttributeType.Real
	at_s.name = 's'
	at_s.group = 'integrator'
	at_s.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('arcLength')+'<br/>') +
		html_par('s the arcLength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Arc-Length_Control','Arc-Length Control')+'<br/>') +
		html_end()
		)
	at_s.setDefault(1.0)
	at_s.editable = notVisibleForNewAnalysis

	# target Arc-Length
	at_target_arclength = MpcAttributeMetaData()
	at_target_arclength.type = MpcAttributeType.Real
	at_target_arclength.name = 'Target Arc-Length'
	at_target_arclength.group = 'integrator'
	at_target_arclength.setDefault(1.0)
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'integrator'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('arcLength')+'<br/>') +
		html_par('alpha a scaling factor on the reference loads') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Arc-Length_Control','Arc-Length Control')+'<br/>') +
		html_end()
		)
	at_alpha.setDefault(0.1)
	
	#-----------------------------------------------------------------------------------------------------------
	#--------------------------------------------------------EQPath---------------------------------------------
	#$type = 1 Minimum Residual Disp ;
	#$type = 2 Normal Plain ;
	#$type = 3 Update Normal Plain ;
	#$type = 4 Cylindrical Arc-Length ;
	# integrator EQPath $arc_length $type
	
	# EQPath 
	at_EQPath = MpcAttributeMetaData()
	at_EQPath.type = MpcAttributeType.Boolean
	at_EQPath.name = 'EQPath'
	at_EQPath.group = 'integrator'
	at_EQPath.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('EQPath')+'<br/>') + 
		html_par('EQPath') +
		html_par(html_href('','EQPath')+'<br/>') +
		html_end()
		)
	at_EQPath.editable = False
	
	# arc_length
	at_target_arc_EQPath = MpcAttributeMetaData()
	at_target_arc_EQPath.type = MpcAttributeType.Real
	at_target_arc_EQPath.name = 'Target Arc-Length/EQPath'
	at_target_arc_EQPath.group = 'integrator'
	at_target_arc_EQPath.setDefault(1.0)
	
	# staticIntegrators
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.String
	at_type.name = 'type/EQPath'
	at_type.group = 'integrator'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') + 
		html_par('EQPath') +
		html_par(html_href('','EQPath')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList(['Minimum Residual Disp', 'Normal Plain', 'Update Normal Plain', 'Cylindrical Arc-Length'])
	at_type.setDefault('Minimum Residual Disp')

	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------------------HSConstraint-----------------------------------------
	# integrator HSConstraint $arcLength <$psi_u $psi_f $u_ref>

	# HSConstraint 
	at_HSConstraint = MpcAttributeMetaData()
	at_HSConstraint.type = MpcAttributeType.Boolean
	at_HSConstraint.name = 'HSConstraint'
	at_HSConstraint.group = 'integrator'
	at_HSConstraint.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('HSConstraint')+'<br/>') + 
		html_par('HSConstraint') +
		html_end()
		)
	at_HSConstraint.editable = False
	
	# arc_length
	at_arcLength = MpcAttributeMetaData()
	at_arcLength.type = MpcAttributeType.Real
	at_arcLength.name = 'Target Arc-Length/HSConstraint'
	at_arcLength.group = 'integrator'
	at_arcLength.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('arcLength')+'<br/>') +
		html_par('HSConstraint') +
		html_end()
		)

	# optional
	at_Optional_HSConstraint = MpcAttributeMetaData()
	at_Optional_HSConstraint.type = MpcAttributeType.Boolean
	at_Optional_HSConstraint.name = 'Optional/HSConstraint'
	at_Optional_HSConstraint.group = 'integrator'
	at_Optional_HSConstraint.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional HSConstraint')+'<br/>') +
		html_end()
		)
	at_Optional_HSConstraint.setDefault(False)
	at_Optional_HSConstraint.editable = visibleOptional

	# psi_u
	at_psi_u = MpcAttributeMetaData()
	at_psi_u.type = MpcAttributeType.Real
	at_psi_u.name = 'psi_u/HSConstraint'
	at_psi_u.group = 'integrator'
	at_psi_u.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('psi_u')+'<br/>') +
		html_par('HSConstraint') +
		html_end()
		)
	at_psi_u.setDefault(1.0)

	# psi_f
	at_psi_f = MpcAttributeMetaData()
	at_psi_f.type = MpcAttributeType.Real
	at_psi_f.name = 'psi_f/HSConstraint'
	at_psi_f.group = 'integrator'
	at_psi_f.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('psi_f')+'<br/>') +
		html_par('HSConstraint') +
		html_end()
		)
	at_psi_f.setDefault(1.0)

	# u_ref
	at_u_ref = MpcAttributeMetaData()
	at_u_ref.type = MpcAttributeType.Real
	at_u_ref.name = 'u_ref/HSConstraint'
	at_u_ref.group = 'integrator'
	at_u_ref.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('u_ref')+'<br/>') +
		html_par('HSConstraint') +
		html_end()
		)
	at_u_ref.setDefault(1.0)

	#------------------------------------------Transient Integrators------------------------------------------
	
	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------Central Difference------------------------------------
	# integrator CentralDifference
	
	
	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------Newmark Method------------------------------------
	# integrator Newmark $gamma $beta
	
	# Newmark
	at_Newmark = MpcAttributeMetaData()
	at_Newmark.type = MpcAttributeType.Boolean
	at_Newmark.name = 'Newmark Method'
	at_Newmark.group = 'integrator'
	at_Newmark.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Newmark Method')+'<br/>') + 
		html_par('Newmark Method') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newmark_Method','Newmark Method')+'<br/>') +
		html_end()
		)
	at_Newmark.editable = False
	
	# gamma
	at_gamma = MpcAttributeMetaData()
	at_gamma.type = MpcAttributeType.Real
	at_gamma.name = 'gamma'
	at_gamma.group = 'integrator'
	at_gamma.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') +
		html_par('gamma factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newmark_Method','Newmark Method')+'<br/>') +
		html_end()
		)
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'integrator'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') +
		html_par('beta factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Newmark_Method','Newmark Method')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------Newmark Explicit------------------------------------
	# integrator Newmark $gamma
	
	# Newmark Explicit
	at_NewmarkExplicit = MpcAttributeMetaData()
	at_NewmarkExplicit.type = MpcAttributeType.Boolean
	at_NewmarkExplicit.name = 'Newmark Explicit'
	at_NewmarkExplicit.group = 'integrator'
	at_NewmarkExplicit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Newmark Explicit')+'<br/>') + 
		html_end()
		)
	at_NewmarkExplicit.editable = False
	
	# gamma
	at_gamma_n_e = MpcAttributeMetaData()
	at_gamma_n_e.type = MpcAttributeType.Real
	at_gamma_n_e.name = 'gamma/NewmarkExplicit'
	at_gamma_n_e.group = 'integrator'
	at_gamma_n_e.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') +
		html_end()
		)
	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------Hilber-Hughes-Taylor Method---------------------------------
	
	# integrator HHT $alpha <$gamma $beta>
	at_HHT = MpcAttributeMetaData()
	at_HHT.type = MpcAttributeType.Boolean
	at_HHT.name = 'Hilber-Hughes-Taylor Method'
	at_HHT.group = 'integrator'
	at_HHT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Hilber-Hughes-Taylor Method')+'<br/>') + 
		html_par('Hilber-Hughes-Taylor Method') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hilber-Hughes-Taylor_Method','Newmark Method')+'<br/>') +
		html_end()
		)
	at_HHT.editable = False
	
	# alpha
	at_alpha_1 = MpcAttributeMetaData()
	at_alpha_1.type = MpcAttributeType.Real
	at_alpha_1.name = 'alpha/HHT'
	at_alpha_1.group = 'integrator'
	at_alpha_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') +
		html_par('alpha factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hilber-Hughes-Taylor_Method','Newmark Method')+'<br/>') +
		html_end()
		)
	
	# optional
	at_Optional_Hilber_Hughes_Taylor = MpcAttributeMetaData()
	at_Optional_Hilber_Hughes_Taylor.type = MpcAttributeType.Boolean
	at_Optional_Hilber_Hughes_Taylor.name = 'Optional Hilber-Hughes-Taylor Method'
	at_Optional_Hilber_Hughes_Taylor.group = 'integrator'
	at_Optional_Hilber_Hughes_Taylor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional Hilber-Hughes-Taylor Method')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hilber-Hughes-Taylor_Method','Newmark Method')+'<br/>') +
		html_end()
		)
	at_Optional_Hilber_Hughes_Taylor.setDefault(False)
	at_Optional_Hilber_Hughes_Taylor.editable = visibleOptional
	
	# gamma
	at_gamma_1 = MpcAttributeMetaData()
	at_gamma_1.type = MpcAttributeType.Real
	at_gamma_1.name = 'gamma/HHT'
	at_gamma_1.group = 'integrator'
	at_gamma_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') +
		html_par('gamma factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hilber-Hughes-Taylor_Method','Newmark Method')+'<br/>') +
		html_end()
		)
	
	# beta
	at_beta_1 = MpcAttributeMetaData()
	at_beta_1.type = MpcAttributeType.Real
	at_beta_1.name = 'beta/HHT'
	at_beta_1.group = 'integrator'
	at_beta_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') +
		html_par('beta factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hilber-Hughes-Taylor_Method','Newmark Method')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------Generalized Alpha Method------------------------------------
	
	# integrator GeneralizedAlpha $alphaM $alphaF <$gamma $beta>
	# GeneralizedAlpha
	at_GeneralizedAlpha = MpcAttributeMetaData()
	at_GeneralizedAlpha.type = MpcAttributeType.Boolean
	at_GeneralizedAlpha.name = 'Generalized Alpha Method'
	at_GeneralizedAlpha.group = 'integrator'
	at_GeneralizedAlpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Generalized Alpha Method')+'<br/>') + 
		html_par('Generalized Alpha Method') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Generalized_Alpha_Method','Generalized Alpha Method')+'<br/>') +
		html_end()
		)
	at_GeneralizedAlpha.editable = False
	
	# alpha
	at_alphaM = MpcAttributeMetaData()
	at_alphaM.type = MpcAttributeType.Real
	at_alphaM.name = 'alphaM'
	at_alphaM.group = 'integrator'
	at_alphaM.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaM')+'<br/>') +
		html_par('alphaM factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Generalized_Alpha_Method','Generalized Alpha Method')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alphaF = MpcAttributeMetaData()
	at_alphaF.type = MpcAttributeType.Real
	at_alphaF.name = 'alphaF'
	at_alphaF.group = 'integrator'
	at_alphaF.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaF')+'<br/>') +
		html_par('alphaF factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Generalized_Alpha_Method','Generalized Alpha Method')+'<br/>') +
		html_end()
		)
	
	# optional
	at_Optional_GeneralizedAlpha  = MpcAttributeMetaData()
	at_Optional_GeneralizedAlpha.type = MpcAttributeType.Boolean
	at_Optional_GeneralizedAlpha.name = 'Optional GeneralizedAlpha'
	at_Optional_GeneralizedAlpha.group = 'integrator'
	at_Optional_GeneralizedAlpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional Generalized Alpha Method')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Generalized_Alpha_Method','Generalized Alpha Method')+'<br/>') +
		html_end()
		)
	at_Optional_GeneralizedAlpha.setDefault(False)
	at_Optional_GeneralizedAlpha.editable = visibleOptional
	
	# gamma
	at_gamma_2 = MpcAttributeMetaData()
	at_gamma_2.type = MpcAttributeType.Real
	at_gamma_2.name = 'gamma/GeneralizedAlpha'
	at_gamma_2.group = 'integrator'
	at_gamma_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') +
		html_par('gamma factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Generalized_Alpha_Method','Generalized Alpha Method')+'<br/>') +
		html_end()
		)
	
	# beta
	at_beta_2 = MpcAttributeMetaData()
	at_beta_2.type = MpcAttributeType.Real
	at_beta_2.name = 'beta/GeneralizedAlpha'
	at_beta_2.group = 'integrator'
	at_beta_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') +
		html_par('beta factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Generalized_Alpha_Method','Generalized Alpha Method')+'<br/>') +
		html_end()
		)

	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------AlphaOS_TP------------------------------------

	# AlphaOS_TP $alpha <-updateElemDisp>
	# AlphaOS_TP
	at_AlphaOS_TP = MpcAttributeMetaData()
	at_AlphaOS_TP.type = MpcAttributeType.Boolean
	at_AlphaOS_TP.name = 'AlphaOS_TP'
	at_AlphaOS_TP.group = 'integrator'
	at_AlphaOS_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('AlphaOS_TP')+'<br/>') + 
		html_end()
		)
	at_AlphaOS_TP.editable = False
	
	# alpha
	at_alphaAlphaOS_TP = MpcAttributeMetaData()
	at_alphaAlphaOS_TP.type = MpcAttributeType.Real
	at_alphaAlphaOS_TP.name = 'alpha/AlphaOS_TP'
	at_alphaAlphaOS_TP.group = 'integrator'
	at_alphaAlphaOS_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') +
		html_end()
		)

	# optional
	at_Optional_AlphaOS_TP = MpcAttributeMetaData()
	at_Optional_AlphaOS_TP.type = MpcAttributeType.Boolean
	at_Optional_AlphaOS_TP.name = '-updateElemDisp'
	at_Optional_AlphaOS_TP.group = 'integrator'
	at_Optional_AlphaOS_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional -updateElemDisp')+'<br/>') +
		html_end()
		)
	at_Optional_AlphaOS_TP.setDefault(False)
	at_Optional_AlphaOS_TP.editable = visibleOptional
	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------AlphaOSGeneralized_TP------------------------------------

	# AlphaOSGeneralized_TP $rhoInf <-updateElemDisp>
	# AlphaOSGeneralized_TP
	at_AlphaOSGeneralized_TP = MpcAttributeMetaData()
	at_AlphaOSGeneralized_TP.type = MpcAttributeType.Boolean
	at_AlphaOSGeneralized_TP.name = 'AlphaOSGeneralized_TP'
	at_AlphaOSGeneralized_TP.group = 'integrator'
	at_AlphaOSGeneralized_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('AlphaOSGeneralized_TP')+'<br/>') + 
		html_end()
		)
	at_AlphaOSGeneralized_TP.editable = False
	
	# rhoInf
	at_rhoInfAOSF_TP = MpcAttributeMetaData()
	at_rhoInfAOSF_TP.type = MpcAttributeType.Real
	at_rhoInfAOSF_TP.name = 'rhoInf/AlphaOSGeneralized_TP'
	at_rhoInfAOSF_TP.group = 'integrator'
	at_rhoInfAOSF_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rhoInf')+'<br/>') +
		html_end()
		)

	# optional
	at_Optional_AOSF_TP = MpcAttributeMetaData()
	at_Optional_AOSF_TP.type = MpcAttributeType.Boolean
	at_Optional_AOSF_TP.name = '-updateElemDisp/AlphaOSGeneralized_TP'
	at_Optional_AOSF_TP.group = 'integrator'
	at_Optional_AOSF_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional -updateElemDisp')+'<br/>') +
		html_end()
		)
	at_Optional_AOSF_TP.setDefault(False)
	at_Optional_AOSF_TP.editable = visibleOptional

	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------HHT_TP------------------------------------

	# HHT_TP $alpha <$gamma $beta>
	# HHT_TP
	at_HHT_TP = MpcAttributeMetaData()
	at_HHT_TP.type = MpcAttributeType.Boolean
	at_HHT_TP.name = 'HHT_TP'
	at_HHT_TP.group = 'integrator'
	at_HHT_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('HHT_TP')+'<br/>') + 
		html_end()
		)
	at_HHT_TP.editable = False
	
	# alpha
	at_alpha_HHT_TP = MpcAttributeMetaData()
	at_alpha_HHT_TP.type = MpcAttributeType.Real
	at_alpha_HHT_TP.name = 'alpha/HHT_TP'
	at_alpha_HHT_TP.group = 'integrator'
	at_alpha_HHT_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') +
		html_end()
		)

	# optional
	at_Optional_HHT_TP = MpcAttributeMetaData()
	at_Optional_HHT_TP.type = MpcAttributeType.Boolean
	at_Optional_HHT_TP.name = 'Optional/HHT_TP'
	at_Optional_HHT_TP.group = 'integrator'
	at_Optional_HHT_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional <$gamma $beta>')+'<br/>') +
		html_end()
		)
	at_Optional_HHT_TP.setDefault(False)
	at_Optional_HHT_TP.editable = visibleOptional

	# gamma
	at_gamma_HHT_TP = MpcAttributeMetaData()
	at_gamma_HHT_TP.type = MpcAttributeType.Real
	at_gamma_HHT_TP.name = 'gamma/HHT_TP'
	at_gamma_HHT_TP.group = 'integrator'
	at_gamma_HHT_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') +
		html_end()
		)

	# beta
	at_beta_HHT_TP = MpcAttributeMetaData()
	at_beta_HHT_TP.type = MpcAttributeType.Real
	at_beta_HHT_TP.name = 'beta/HHT_TP'
	at_beta_HHT_TP.group = 'integrator'
	at_beta_HHT_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') +
		html_end()
		)

	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------HHTExplicit_TP------------------------------------

	# HHTExplicit_TP $alpha <$gamma>
	# HHTExplicit_TP
	at_HHTExplicit_TP = MpcAttributeMetaData()
	at_HHTExplicit_TP.type = MpcAttributeType.Boolean
	at_HHTExplicit_TP.name = 'HHTExplicit_TP'
	at_HHTExplicit_TP.group = 'integrator'
	at_HHTExplicit_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('HHTExplicit_TP')+'<br/>') + 
		html_end()
		)
	at_HHTExplicit_TP.editable = False
	
	# alpha
	at_alpha_HHTExplicit_TP = MpcAttributeMetaData()
	at_alpha_HHTExplicit_TP.type = MpcAttributeType.Real
	at_alpha_HHTExplicit_TP.name = 'alpha/HHTExplicit_TP'
	at_alpha_HHTExplicit_TP.group = 'integrator'
	at_alpha_HHTExplicit_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') +
		html_end()
		)

	# optional
	at_Optional_HHTExplicit_TP = MpcAttributeMetaData()
	at_Optional_HHTExplicit_TP.type = MpcAttributeType.Boolean
	at_Optional_HHTExplicit_TP.name = 'Optional/HHTExplicit_TP'
	at_Optional_HHTExplicit_TP.group = 'integrator'
	at_Optional_HHTExplicit_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional <$gamma $beta>')+'<br/>') +
		html_end()
		)
	at_Optional_HHTExplicit_TP.setDefault(False)
	at_Optional_HHTExplicit_TP.editable = visibleOptional


	# gamma
	at_gamma_HHTExplicit_TP = MpcAttributeMetaData()
	at_gamma_HHTExplicit_TP.type = MpcAttributeType.Real
	at_gamma_HHTExplicit_TP.name = 'gamma/HHTExplicit_TP'
	at_gamma_HHTExplicit_TP.group = 'integrator'
	at_gamma_HHTExplicit_TP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') +
		html_end()
		)

	#-----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------HHTGeneralizedExplicit_TP------------------------------------

	# HHTGeneralizedExplicit_TP $rhoB $alphaF
	# HHTGeneralizedExplicit_TP $alphaI $alphaF $beta $gamma
	
	# HHTGeneralizedExplicit_TP
	at_HHTGE = MpcAttributeMetaData()
	at_HHTGE.type = MpcAttributeType.Boolean
	at_HHTGE.name = 'HHTGeneralizedExplicit_TP'
	at_HHTGE.group = 'integrator'
	at_HHTGE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('HHTGeneralizedExplicit_TP')+'<br/>') + 
		html_end()
		)
	at_HHTGE.editable = False
	
	# transientIntegrators
	at_mode = MpcAttributeMetaData()
	at_mode.type = MpcAttributeType.String
	at_mode.name = 'mode'
	at_mode.group = 'integrator'
	at_mode.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('HHTGeneralizedExplicit_TP')+'<br/>') + 
		html_end()
		)
	at_mode.sourceType = MpcAttributeSourceType.List
	at_mode.setSourceList(['rhoB alphaF', 'alphaI alphaF beta gamma'])
	at_mode.setDefault('rhoB alphaF')
	
	# rhoB alphaF
	at_mode_1 = MpcAttributeMetaData()
	at_mode_1.type = MpcAttributeType.Boolean
	at_mode_1.name = 'rhoB alphaF'
	at_mode_1.group = 'integrator'
	at_mode_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('HHTGeneralizedExplicit_TP')+'<br/>') + 
		html_end()
		)
	at_mode_1.editable = False
	
	# rhoB
	at_rhoB_HHTGE = MpcAttributeMetaData()
	at_rhoB_HHTGE.type = MpcAttributeType.Real
	at_rhoB_HHTGE.name = 'rhoB/HHTGeneralizedExplicit_TP'
	at_rhoB_HHTGE.group = 'integrator'
	at_rhoB_HHTGE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rhoB')+'<br/>') +
		html_end()
		)

	# alphaI
	at_alphaI_HHTGE = MpcAttributeMetaData()
	at_alphaI_HHTGE.type = MpcAttributeType.Real
	at_alphaI_HHTGE.name = 'alphaI/HHTGeneralizedExplicit_TP'
	at_alphaI_HHTGE.group = 'integrator'
	at_alphaI_HHTGE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaI')+'<br/>') +
		html_end()
		)
		
	# alphaF
	at_alphaF_HHTGE = MpcAttributeMetaData()
	at_alphaF_HHTGE.type = MpcAttributeType.Real
	at_alphaF_HHTGE.name = 'alphaF/HHTGeneralizedExplicit_TP'
	at_alphaF_HHTGE.group = 'integrator'
	at_alphaF_HHTGE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaF')+'<br/>') +
		html_end()
		)
		
	# beta
	at_beta_HHTGE = MpcAttributeMetaData()
	at_beta_HHTGE.type = MpcAttributeType.Real
	at_beta_HHTGE.name = 'beta/HHTGeneralizedExplicit_TP'
	at_beta_HHTGE.group = 'integrator'
	at_beta_HHTGE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') +
		html_end()
		)
	
	# gamma
	at_gamma_HHTGE = MpcAttributeMetaData()
	at_gamma_HHTGE.type = MpcAttributeType.Real
	at_gamma_HHTGE.name = 'gamma/HHTGeneralizedExplicit_TP'
	at_gamma_HHTGE.group = 'integrator'
	at_gamma_HHTGE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') +
		html_end()
		)

	# alphaI alphaF beta gamma
	at_mode_2 = MpcAttributeMetaData()
	at_mode_2.type = MpcAttributeType.Boolean
	at_mode_2.name = 'alphaI alphaF beta gamma'
	at_mode_2.group = 'integrator'
	at_mode_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('HHTGeneralizedExplicit_TP')+'<br/>') + 
		html_end()
		)
	at_mode_2.editable = False

	#-----------------------------------------------------------------------------------------------------------
	#--------------------------------------------------KRAlphaExplicit_TP---------------------------------------
	
	# KRAlphaExplicit_TP $rhoInf
	
	# KRAlphaExplicit_TP
	at_KRA = MpcAttributeMetaData()
	at_KRA.type = MpcAttributeType.Boolean
	at_KRA.name = 'KRAlphaExplicit_TP'
	at_KRA.group = 'integrator'
	at_KRA.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('KRAlphaExplicit_TP')+'<br/>') + 
		html_end()
		)
	at_KRA.editable = False
	
	
	# rhoB
	at_rhoInf_KRA = MpcAttributeMetaData()
	at_rhoInf_KRA.type = MpcAttributeType.Real
	at_rhoInf_KRA.name = 'rhoInf/KRAlphaExplicit_TP'
	at_rhoInf_KRA.group = 'integrator'
	at_rhoInf_KRA.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rhoInf')+'<br/>') +
		html_end()
		)

	#-----------------------------------------------------------------------------------------------------------
	#---------------------------------------------------------TRBDF2--------------------------------------------
	
	# integrator TRBDF2
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------------Explicit Difference----------------------------------------
	
	# integrator Explicitdifference
	
	#-----------------------------------------------------------------------------------------------------------
	#
	#
	#-----------------------------------------------------------------------------------------------------------
	
	
	xom.addAttribute(at_booleanStaticIntegrators)
	xom.addAttribute(at_staticIntegrators)
	xom.addAttribute(at_booleanTransientIntegrators)
	xom.addAttribute(at_transientIntegrators)
	
	# Static Integrators
	
	# loadControl
	xom.addAttribute(at_loadControl)
	xom.addAttribute(at_lambda)
	xom.addAttribute(at_lambda_tot)
	xom.addAttribute(at_Optional_LoadControl)
	xom.addAttribute(at_numIter)
	xom.addAttribute(at_minLambda)
	xom.addAttribute(at_maxLambda)
	
	# parallelDisplacementControl
	xom.addAttribute(at_parallelDisplacementControl)
	xom.addAttribute(at_parallelNode)
	xom.addAttribute(at_parallelDof)
	xom.addAttribute(at_parallelIncr)
	xom.addAttribute(at_parallelCyclic)
	xom.addAttribute(at_parallelTargetDisp)
	xom.addAttribute(at_parallel_tsTag)
	xom.addAttribute(at_Optional_parallelDisplacementControl)
	xom.addAttribute(at_parallelNumIter_1)
	xom.addAttribute(at_parallelDeltaUmin)
	xom.addAttribute(at_parallelDeltaUmax)
	
	# displacementControl
	xom.addAttribute(at_displacementControl)
	xom.addAttribute(at_node)
	xom.addAttribute(at_dof)
	xom.addAttribute(at_incr)
	xom.addAttribute(at_Cyclic)
	xom.addAttribute(at_TargetDisp)
	xom.addAttribute(at_tsTag)
	xom.addAttribute(at_Optional_DisplacementControl)
	xom.addAttribute(at_numIter_1)
	xom.addAttribute(at_deltaUmin)
	xom.addAttribute(at_deltaUmax)
	
	# MinUnbalDispNorm
	xom.addAttribute(at_MinUnbalDispNorm)
	xom.addAttribute(at_dlambda1)
	xom.addAttribute(at_Optional_MinUnbalDispNorm)
	xom.addAttribute(at_Jd_integrator)
	xom.addAttribute(at_minLambda_1)
	xom.addAttribute(at_maxLambda_1)
	
	# ArcLength
	xom.addAttribute(at_ArcLength)
	xom.addAttribute(at_target_arclength)
	xom.addAttribute(at_s)
	xom.addAttribute(at_alpha)

	# EQPath
	xom.addAttribute(at_EQPath)
	xom.addAttribute(at_target_arc_EQPath)
	xom.addAttribute(at_type)

	# HSConstraint
	xom.addAttribute(at_HSConstraint)
	xom.addAttribute(at_arcLength)
	xom.addAttribute(at_Optional_HSConstraint)
	xom.addAttribute(at_psi_u)
	xom.addAttribute(at_psi_f)
	xom.addAttribute(at_u_ref)

	# Transient Integrators
	# Newmark Method
	
	xom.addAttribute(at_Newmark)
	xom.addAttribute(at_gamma)
	xom.addAttribute(at_beta)

	# Transient Integrators
	# Newmark Explicit
	
	xom.addAttribute(at_NewmarkExplicit)
	xom.addAttribute(at_gamma_n_e)
	
	# Hilber-Hughes-Taylor Method
	xom.addAttribute(at_HHT)
	xom.addAttribute(at_alpha_1)
	xom.addAttribute(at_Optional_Hilber_Hughes_Taylor)
	xom.addAttribute(at_gamma_1)
	xom.addAttribute(at_beta_1)
	
	# Generalized Alpha Method
	xom.addAttribute(at_GeneralizedAlpha)
	xom.addAttribute(at_alphaF)
	xom.addAttribute(at_alphaM)
	xom.addAttribute(at_Optional_GeneralizedAlpha)
	xom.addAttribute(at_gamma_2)
	xom.addAttribute(at_beta_2)
	
	
		# AlphaOS_TP
	xom.addAttribute(at_AlphaOS_TP)
	xom.addAttribute(at_alphaAlphaOS_TP)
	xom.addAttribute(at_Optional_AlphaOS_TP)

	# AlphaOSGeneralized_TP
	xom.addAttribute(at_AlphaOSGeneralized_TP)
	xom.addAttribute(at_rhoInfAOSF_TP)
	xom.addAttribute(at_Optional_AOSF_TP)

	# HHT_TP
	xom.addAttribute(at_HHT_TP)
	xom.addAttribute(at_alpha_HHT_TP)
	xom.addAttribute(at_Optional_HHT_TP)
	xom.addAttribute(at_gamma_HHT_TP)
	xom.addAttribute(at_beta_HHT_TP)

	# HHTExplicit_TP
	xom.addAttribute(at_HHTExplicit_TP)
	xom.addAttribute(at_alpha_HHTExplicit_TP)
	xom.addAttribute(at_Optional_HHTExplicit_TP)
	xom.addAttribute(at_gamma_HHTExplicit_TP)

	# HHTGeneralizedExplicit_TP
	xom.addAttribute(at_HHTGE)
	xom.addAttribute(at_mode)
	xom.addAttribute(at_mode_1)
	xom.addAttribute(at_rhoB_HHTGE)
	xom.addAttribute(at_alphaI_HHTGE)
	xom.addAttribute(at_alphaF_HHTGE)
	xom.addAttribute(at_beta_HHTGE)
	xom.addAttribute(at_gamma_HHTGE)
	xom.addAttribute(at_mode_2)

	# KRAlphaExplicit_TP
	xom.addAttribute(at_KRA)
	xom.addAttribute(at_rhoInf_KRA)

	# Static Integrators
	# Integrator Command Dependency
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_staticIntegrators)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_transientIntegrators)
	
	xom.setVisibilityDependency(at_loadControl, at_lambda_tot)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_lambda_tot)
	
	# loadControl
	xom.setVisibilityDependency(at_loadControl, at_Optional_LoadControl)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_Optional_LoadControl)
	
	xom.setVisibilityDependency(at_Optional_LoadControl, at_numIter)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_numIter)
	xom.setVisibilityDependency(at_loadControl, at_numIter)
	
	xom.setVisibilityDependency(at_Optional_LoadControl, at_minLambda)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_minLambda)
	xom.setVisibilityDependency(at_loadControl, at_minLambda)
	
	xom.setVisibilityDependency(at_Optional_LoadControl, at_maxLambda)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_maxLambda)
	xom.setVisibilityDependency(at_loadControl, at_maxLambda)
	
	# parallelDisplacementControl
	xom.setVisibilityDependency(at_parallelDisplacementControl, at_Optional_parallelDisplacementControl)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_Optional_parallelDisplacementControl)
	
	xom.setVisibilityDependency(at_parallelDisplacementControl, at_parallelCyclic)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_parallelCyclic)
	
	xom.setVisibilityDependency(at_parallelDisplacementControl, at_parallelNode)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_parallelNode)
	
	xom.setVisibilityDependency(at_parallelDisplacementControl, at_parallelDof)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_parallelDof)
	
	xom.setVisibilityDependency(at_parallelDisplacementControl, at_parallelTargetDisp)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_parallelTargetDisp)
	
	xom.setVisibilityDependency(at_Optional_parallelDisplacementControl, at_parallelNumIter_1)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_parallelNumIter_1)
	xom.setVisibilityDependency(at_parallelDisplacementControl, at_parallelNumIter_1)
	
	xom.setVisibilityDependency(at_parallelCyclic, at_parallel_tsTag)
	xom.setVisibilityDependency(at_parallelDisplacementControl, at_parallel_tsTag)
	xom.setVisibilityDependency(at_booleanStaticIntegrators,at_parallel_tsTag)
	
	
	xom.setVisibilityDependency(at_Optional_parallelDisplacementControl, at_parallelDeltaUmin)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_parallelDeltaUmin)
	xom.setVisibilityDependency(at_parallelDisplacementControl, at_parallelDeltaUmin)
	
	xom.setVisibilityDependency(at_Optional_parallelDisplacementControl, at_parallelDeltaUmax)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_parallelDeltaUmax)
	xom.setVisibilityDependency(at_parallelDisplacementControl, at_parallelDeltaUmax)
	
	# displacementControl
	xom.setVisibilityDependency(at_displacementControl, at_Optional_DisplacementControl)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_Optional_DisplacementControl)
	
	
	xom.setVisibilityDependency(at_displacementControl, at_node)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_node)
	
	xom.setVisibilityDependency(at_displacementControl, at_dof)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_dof)
	
	xom.setVisibilityDependency(at_displacementControl, at_TargetDisp)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_TargetDisp)
	
	xom.setVisibilityDependency(at_displacementControl, at_Cyclic)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_Cyclic)
	
	xom.setVisibilityDependency(at_Cyclic, at_tsTag)
	xom.setVisibilityDependency(at_displacementControl, at_tsTag)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_tsTag)
	
	xom.setVisibilityDependency(at_Optional_DisplacementControl, at_numIter_1)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_numIter_1)
	xom.setVisibilityDependency(at_displacementControl, at_numIter_1)
	
	xom.setVisibilityDependency(at_Optional_DisplacementControl, at_deltaUmin)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_deltaUmin)
	xom.setVisibilityDependency(at_displacementControl, at_deltaUmin)
	
	xom.setVisibilityDependency(at_Optional_DisplacementControl, at_deltaUmax)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_deltaUmax)
	xom.setVisibilityDependency(at_displacementControl, at_deltaUmax)
	
	# MinUnbalDispNorm
	xom.setVisibilityDependency(at_MinUnbalDispNorm, at_Optional_MinUnbalDispNorm)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_Optional_MinUnbalDispNorm)
	
	xom.setVisibilityDependency(at_MinUnbalDispNorm, at_dlambda1)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_dlambda1)
	
	xom.setVisibilityDependency(at_Optional_MinUnbalDispNorm, at_Jd_integrator)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_Jd_integrator)
	xom.setVisibilityDependency(at_MinUnbalDispNorm, at_Jd_integrator)
	
	xom.setVisibilityDependency(at_Optional_MinUnbalDispNorm, at_minLambda_1)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_minLambda_1)
	xom.setVisibilityDependency(at_MinUnbalDispNorm, at_minLambda_1)
	
	xom.setVisibilityDependency(at_Optional_MinUnbalDispNorm, at_maxLambda_1)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_maxLambda_1)
	xom.setVisibilityDependency(at_MinUnbalDispNorm, at_maxLambda_1)
	
	# arcLength
	xom.setVisibilityDependency(at_ArcLength, at_target_arclength)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_target_arclength)
	
	xom.setVisibilityDependency(at_ArcLength, at_alpha)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_alpha)	

	# at_EQPath
	xom.setVisibilityDependency(at_EQPath, at_target_arc_EQPath)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_target_arc_EQPath)
	
	xom.setVisibilityDependency(at_EQPath, at_type)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_type)

	# HSConstraint
	xom.setVisibilityDependency(at_HSConstraint, at_arcLength)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_arcLength)

	xom.setVisibilityDependency(at_HSConstraint, at_Optional_HSConstraint)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_Optional_HSConstraint)
	
	xom.setVisibilityDependency(at_Optional_HSConstraint, at_psi_u)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_psi_u)
	xom.setVisibilityDependency(at_HSConstraint, at_psi_u)
	
	xom.setVisibilityDependency(at_Optional_HSConstraint, at_psi_f)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_psi_f)
	xom.setVisibilityDependency(at_HSConstraint, at_psi_f)
	
	xom.setVisibilityDependency(at_Optional_HSConstraint, at_u_ref)
	xom.setVisibilityDependency(at_booleanStaticIntegrators, at_u_ref)
	xom.setVisibilityDependency(at_HSConstraint, at_u_ref)

	
	# auto-exclusive dependencies
	
	xom.setBooleanAutoExclusiveDependency(at_staticIntegrators, at_loadControl)
	
	xom.setBooleanAutoExclusiveDependency(at_staticIntegrators, at_parallelDisplacementControl)
	
	xom.setBooleanAutoExclusiveDependency(at_staticIntegrators, at_displacementControl)
	
	xom.setBooleanAutoExclusiveDependency(at_staticIntegrators, at_MinUnbalDispNorm)
	
	xom.setBooleanAutoExclusiveDependency(at_staticIntegrators, at_ArcLength)

	xom.setBooleanAutoExclusiveDependency(at_staticIntegrators, at_EQPath)

	xom.setBooleanAutoExclusiveDependency(at_staticIntegrators, at_HSConstraint)
	
	# Transient Integrators
	# Integrator Command Dependency
	
	# Newmark Method
	xom.setVisibilityDependency(at_Newmark, at_gamma)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_gamma)
	
	xom.setVisibilityDependency(at_Newmark, at_beta)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_beta)

	# Newmark Explicit
	xom.setVisibilityDependency(at_NewmarkExplicit, at_gamma_n_e)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_gamma_n_e)
	
	# Hilber-Hughes-Taylor Method
	xom.setVisibilityDependency(at_HHT, at_Optional_Hilber_Hughes_Taylor)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_Optional_Hilber_Hughes_Taylor)
	
	xom.setVisibilityDependency(at_HHT, at_alpha_1)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_alpha_1)
	
	xom.setVisibilityDependency(at_Optional_Hilber_Hughes_Taylor, at_gamma_1)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_gamma_1)
	xom.setVisibilityDependency(at_HHT, at_gamma_1)
	
	xom.setVisibilityDependency(at_Optional_Hilber_Hughes_Taylor, at_beta_1)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_beta_1)
	xom.setVisibilityDependency(at_HHT, at_beta_1)
	
	# Generalized Alpha Method
	xom.setVisibilityDependency(at_GeneralizedAlpha, at_Optional_GeneralizedAlpha)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_Optional_GeneralizedAlpha)
	
	xom.setVisibilityDependency(at_GeneralizedAlpha, at_alphaM)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_alphaM)
	
	xom.setVisibilityDependency(at_GeneralizedAlpha, at_alphaF)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_alphaF)
	
	xom.setVisibilityDependency(at_Optional_GeneralizedAlpha, at_gamma_2)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_gamma_2)
	xom.setVisibilityDependency(at_GeneralizedAlpha, at_gamma_2)
	
	xom.setVisibilityDependency(at_Optional_GeneralizedAlpha, at_beta_2)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_beta_2)
	xom.setVisibilityDependency(at_GeneralizedAlpha, at_beta_2)

	# AlphaOS_TP
	xom.setVisibilityDependency(at_AlphaOS_TP, at_alphaAlphaOS_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_alphaAlphaOS_TP)
	
	xom.setVisibilityDependency(at_AlphaOS_TP, at_Optional_AlphaOS_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_Optional_AlphaOS_TP)
	
	# AlphaOSGeneralized_TP
	xom.setVisibilityDependency(at_AlphaOSGeneralized_TP, at_rhoInfAOSF_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_rhoInfAOSF_TP)
	
	xom.setVisibilityDependency(at_AlphaOSGeneralized_TP, at_Optional_AOSF_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_Optional_AOSF_TP)

	# aHHT_TP
	xom.setVisibilityDependency(at_HHT_TP, at_alpha_HHT_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_alpha_HHT_TP)
	
	xom.setVisibilityDependency(at_HHT_TP, at_Optional_HHT_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_Optional_HHT_TP)
	
	xom.setVisibilityDependency(at_Optional_HHT_TP, at_gamma_HHT_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_gamma_HHT_TP)
	xom.setVisibilityDependency(at_HHT_TP, at_gamma_HHT_TP)

	xom.setVisibilityDependency(at_Optional_HHT_TP, at_beta_HHT_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_beta_HHT_TP)
	xom.setVisibilityDependency(at_HHT_TP, at_beta_HHT_TP)

	# aHHTExplicit_TP
	xom.setVisibilityDependency(at_HHTExplicit_TP, at_alpha_HHTExplicit_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_alpha_HHTExplicit_TP)
	
	xom.setVisibilityDependency(at_HHTExplicit_TP, at_Optional_HHTExplicit_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_Optional_HHTExplicit_TP)
	
	xom.setVisibilityDependency(at_Optional_HHTExplicit_TP, at_gamma_HHTExplicit_TP)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_gamma_HHTExplicit_TP)
	xom.setVisibilityDependency(at_HHTExplicit_TP, at_gamma_HHTExplicit_TP)

	# HHTGeneralizedExplicit_TP
	xom.setVisibilityDependency(at_HHTGE, at_mode)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_mode)

	xom.setVisibilityDependency(at_mode_1, at_rhoB_HHTGE)
	xom.setVisibilityDependency(at_HHTGE, at_rhoB_HHTGE)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_rhoB_HHTGE)
	
	xom.setVisibilityDependency(at_mode_2, at_alphaI_HHTGE)
	xom.setVisibilityDependency(at_HHTGE, at_alphaI_HHTGE)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_alphaI_HHTGE)
	
	xom.setVisibilityDependency(at_HHTGE, at_alphaF_HHTGE)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_alphaF_HHTGE)
	
	xom.setVisibilityDependency(at_mode_2, at_beta_HHTGE)
	xom.setVisibilityDependency(at_HHTGE, at_beta_HHTGE)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_beta_HHTGE)

	xom.setVisibilityDependency(at_mode_2, at_gamma_HHTGE)
	xom.setVisibilityDependency(at_HHTGE, at_gamma_HHTGE)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_gamma_HHTGE)
	
	xom.setBooleanAutoExclusiveDependency(at_mode, at_mode_1)
	xom.setBooleanAutoExclusiveDependency(at_mode, at_mode_2)

	# KRAlphaExplicit_TP
	xom.setVisibilityDependency(at_KRA, at_rhoInf_KRA)
	xom.setVisibilityDependency(at_booleanTransientIntegrators, at_rhoInf_KRA)

	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_Newmark)
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_NewmarkExplicit)
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_HHT)
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_GeneralizedAlpha)
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_AlphaOS_TP)
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_AlphaOSGeneralized_TP)
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_HHT_TP)
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_HHTExplicit_TP)
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_HHTGE)
	xom.setBooleanAutoExclusiveDependency(at_transientIntegrators, at_KRA)

def writeTcl_integrator(pinfo, xobj):
	
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	sopt = ''
	
	booleanStaticIntegrators = geta('Static').boolean
	booleanTransientIntegrators = geta('Transient').boolean
	
	if booleanStaticIntegrators:
	# ----------------- staticIntegrators -----------------
		staticIntegrators = geta('staticIntegrators').string
		# ----------------- Load Control -----------------
		if staticIntegrators == 'Load Control':
			# lambda
			duration = geta('duration').real
			#optional
			optional = geta('Optional LoadControl').boolean
			if optional:
				numIter = geta('numIter').integer
				minLambda = geta('minLambda').real
				maxLambda = geta('maxLambda').real
				
				sopt += ' {} {} {}'.format(numIter, minLambda, maxLambda)
			
			str_tcl = '{}integrator LoadControl {}{}\n'.format(pinfo.indent, 0.0, sopt) #solo per la prima dichiarazione
	
		# ----------------- Parallel Displacement Control -----------------
		elif staticIntegrators == 'Parallel Displacement Control':
			doc = App.caeDocument()
			# node	
			SelectionSetParallel_at = xobj.getAttribute('SelectionSet/parallelDisplacementControl')
			if(SelectionSetParallel_at is None):
				raise Exception('Error: cannot find "SelectionSet" attribute')
			selection_set = doc.getSelectionSet(SelectionSetParallel_at.index)
			if selection_set is None:
				raise Exception('Error: No selection set specified for the control node of the ParallelDisplacementControl integrator')
			if len(selection_set.geometries) != 1:
				raise Exception('Error: the selection set for ParallelDisplacementControl must contain 1 vertex (found {} geometries)'.format(len(selection_set.geometries)))
			for geometry_id, geometry_subset in selection_set.geometries.items():
				mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
				if len(geometry_subset.vertices) != 1: 
					raise Exception('Error: the selection set for ParallelDisplacementControl must contain 1 vertex (found {} vertices)'.format(len(geometry_subset.vertices)));
				for domain_id in geometry_subset.vertices:
					node = mesh_of_geom.vertices[domain_id].id
		
			#dof
			dof = geta('dof/parallelDisplacementControl').integer
			#incr
			incrParallel_at = xobj.getAttribute('incr/parallelDisplacementControl')
			if(incrParallel_at is None):
				raise Exception('Error: cannot find "incr" attribute')
			incr = incrParallel_at.real
			
			# Optional DisplacementControl
			optional = geta('Optional parallelDisplacementControl/parallelDisplacementControl').boolean
			
			if optional:
				numIter = geta('numIter/parallelDisplacementControl').integer
				deltaUmin = geta('delta U min/parallelDisplacementControl').real
				deltaUmax = geta('delta U max/parallelDisplacementControl').real
				
				sopt += ' {} {} {}'.format(numIter, deltaUmin, deltaUmax)
			
			str_tcl = '{}integrator ParallelDisplacementControl {} {} {}{}\n'.format(pinfo.indent, node, dof, 0.0, sopt)#solo per la prima dichiarazione
	
		# ----------------- Displacement Control -----------------
		elif staticIntegrators == 'Displacement Control':
			doc = App.caeDocument()
			# node	
			SelectionSet_at = xobj.getAttribute('SelectionSet')
			if(SelectionSet_at is None):
				raise Exception('Error: cannot find "SelectionSet" attribute')
			selection_set = doc.getSelectionSet(SelectionSet_at.index)
			if selection_set is None:
				raise Exception('Error: No selection set specified for the control node of the DisplacementControl integrator')
			if len(selection_set.geometries) != 1:
				raise Exception('Error: the selection set for DisplacementControl must contain 1 vertex (found {} geometries)'.format(len(selection_set.geometries)))
			for geometry_id, geometry_subset in selection_set.geometries.items():
				mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
				if len(geometry_subset.vertices) != 1: 
					raise Exception('Error: the selection set for DisplacementControl must contain 1 vertex (found {} vertices)'.format(len(geometry_subset.vertices)));
				for domain_id in geometry_subset.vertices:
					node = mesh_of_geom.vertices[domain_id].id
		
			#dof
			dof = geta('dof').integer
			#incr
			incr = geta('incr').real
			# Optional DisplacementControl
			optional = geta('Optional DisplacementControl').boolean
			
			if optional:
				numIter = geta('numIter/DisplacementControl').integer
				deltaUmin = geta('delta U min').real
				deltaUmax = geta('delta U max').real
				
				sopt += ' {} {} {}'.format(numIter, deltaUmin, deltaUmax)
			
			str_tcl = '{}integrator DisplacementControl {} {} {}{}\n'.format(pinfo.indent, node, dof, 0.1, sopt)#solo per la prima dichiarazione
			
		# ----------------- Minimum Unbalanced Displacement Norm -----------------
		elif staticIntegrators == 'Minimum Unbalanced Displacement Norm':
			# dlambda1
			dlambda1 = geta('dlambda1').real
			# Optional MinUnbalDispNorm
			optional = geta('Optional MinUnbalDispNorm').boolean
			
			if optional:
				Jd_integrator = geta('Jd/integrator').real
				minLambda = geta('minLambda/MinUnbalDispNorm').real
				maxLambda = geta('maxLambda/MinUnbalDispNorm').real
				
				sopt += ' {} {} {}'.format(Jd_integrator, minLambda, maxLambda)
		
			str_tcl = '{}integrator MinUnbalDispNorm {}{}\n'.format(pinfo.indent, dlambda1, sopt)
		
		# ----------------- Arc-Length Control -----------------
		elif staticIntegrators == 'Arc-Length Control':
			# s
			#s = geta('s').real
			# alpha
			alpha = geta('alpha').real
			
			str_tcl = '{}integrator ArcLength {} {}\n'.format(pinfo.indent, 0.0, alpha)#solo per la prima dichiarazione

		# ----------------- EQPath -----------------
		elif staticIntegrators == 'EQPath':
			# s
			arc_length = geta('Target Arc-Length/EQPath').real
			eq_type = geta('type/EQPath').string
			int_type = 0
			if eq_type == 'Minimum Residual Disp':
				int_type = 1
			if eq_type == 'Normal Plain':
				int_type = 2
			if eq_type == 'Update Normal Plain':
				int_type = 3
			if eq_type == 'Cylindrical Arc-Length':
				int_type = 4
			str_tcl = '{}integrator EQPath {} {}\n'.format(pinfo.indent, 0.0, int_type)#solo per la prima dichiarazione

		# ----------------- HSConstraint -----------------
		elif staticIntegrators == 'HSConstraint':
			# arcLength
			HSConst_arc_length = geta('Target Arc-Length/HSConstraint').real

			# Optional HSConstraint
			optional_HSConstraint = geta('Optional/HSConstraint').boolean
			
			sopt_HSConstraint = ''
			if optional_HSConstraint:
				sopt_HSConstraint += ' {}'.format(geta('psi_u/HSConstraint').real)
				sopt_HSConstraint += ' {}'.format(geta('psi_f/HSConstraint').real)
				sopt_HSConstraint += ' {}'.format(geta('u_ref/HSConstraint').real)

			str_tcl = '{}integrator HSConstraint {}{}\n'.format(pinfo.indent, 0.0, sopt_HSConstraint)#solo per la prima dichiarazione
	
	elif booleanTransientIntegrators:
	# ----------------- transientIntegrators -----------------
		transientIntegrators = geta('transientIntegrators').string
		
		# ----------------- Central Difference -----------------
		if transientIntegrators == 'Central Difference':
			str_tcl = '{}integrator CentralDifference\n'.format(pinfo.indent)
			
		# ----------------- Newmark Method -----------------
		elif transientIntegrators == 'Newmark Method':
			# gamma
			gamma = geta('gamma').real
			# beta
			beta = geta('beta').real
		
			str_tcl = '{}integrator Newmark {} {}\n'.format(pinfo.indent, gamma, beta)
			
		# ----------------- Newmark Explicit -----------------
		elif transientIntegrators == 'Newmark Explicit':
			# gamma/NewmarkExplicit
			gamma = geta('gamma/NewmarkExplicit').real
		
			str_tcl = '{}integrator NewmarkExplicit {}\n'.format(pinfo.indent, gamma)

		# ----------------- Hilber-Hughes-Taylor Method -----------------
		elif transientIntegrators == 'Hilber-Hughes-Taylor Method':
		# alpha/HHT
			alpha = geta('alpha/HHT').real
			
			# Optional Hilber-Hughes-Taylor Method
			optional = geta('Optional Hilber-Hughes-Taylor Method').boolean
			
			if optional:
				#gamma/HHT
				gamma = geta('gamma/HHT').real
				#beta/HHT
				beta = geta('beta/HHT').real

				sopt += ' {} {}'.format(gamma, beta)
			
			str_tcl = '{}integrator HHT {}{}\n'.format(pinfo.indent, alpha, sopt)
			
		# ----------------- Generalized Alpha Method -----------------
		elif transientIntegrators == 'Generalized Alpha Method':
			# alphaM
			alphaM = geta('alphaM').real
			# alphaM
			alphaF = geta('alphaF').real
			# Optional GeneralizedAlpha
			optional = geta('Optional GeneralizedAlpha').boolean
			
			if optional:
				# gamma/GeneralizedAlpha
				gamma = geta('gamma/GeneralizedAlpha').real
				#beta/GeneralizedAlpha
				beta = geta('beta/GeneralizedAlpha').real
				
				sopt += ' {} {}'.format(gamma, beta)
			
			str_tcl = '{}integrator GeneralizedAlpha {} {}{}\n'.format(pinfo.indent, alphaM, alphaF, sopt)
			
		# ----------------- AlphaOS_TP -----------------
		elif transientIntegrators == 'AlphaOS_TP':
			# alpha/AlphaOS_TP
			alphaAlphaOS_TP = geta('alpha/AlphaOS_TP').real
			updateElemDisp = ''
			# Optional -updateElemDisp
			if geta('-updateElemDisp').boolean:
				updateElemDisp += ' -updateElemDisp'

			str_tcl = '{}integrator AlphaOS_TP {}{}\n'.format(pinfo.indent, alphaAlphaOS_TP, updateElemDisp)

		# ----------------- AlphaOSGeneralized_TP -----------------
		elif transientIntegrators == 'AlphaOSGeneralized_TP':
			# rhoInf/AlphaOSGeneralized_TP'
			rhoInfAOSF_TP = geta('rhoInf/AlphaOSGeneralized_TP').real
			updateElemDisp_AOSF_TP = ''
			# Optional -updateElemDisp
			if geta('-updateElemDisp/AlphaOSGeneralized_TP').boolean:
				updateElemDisp_AOSF_TP += ' -updateElemDisp'

			str_tcl = '{}integrator AlphaOSGeneralized_TP {}{}\n'.format(pinfo.indent, rhoInfAOSF_TP, updateElemDisp_AOSF_TP)

		# ----------------- OptionalHHTExplicit_TP -----------------
		elif transientIntegrators == 'HHTExplicit_TP':
			# rhoInf/HHTExplicit_TP'
			alpha_HHTExplicit_TP = geta('alpha/HHTExplicit_TP').real
			
			optional_HHTExplicit_TP = ''
			# Optional <$gamma $beta>
			if geta('Optional/HHTExplicit_TP').boolean:
				optional_HHTExplicit_TP += ' {}'.format(geta('gamma/HHTExplicit_TP').real)
				
			str_tcl = '{}integrator HHTExplicit_TP {}{}\n'.format(pinfo.indent, alpha_HHTExplicit_TP, optional_HHTExplicit_TP)

		# ----------------- HHT_TP -----------------
		elif transientIntegrators == 'HHT_TP':
			# rhoInf/HHT_TP'
			alpha_HHT_TP = geta('alpha/HHT_TP').real
			
			optional_HHT_TP = ''
			# Optional <$gamma $beta>
			if geta('Optional/HHT_TP').boolean:
				optional_HHT_TP += ' {}'.format(geta('gamma/HHT_TP').real)
				optional_HHT_TP += ' {}'.format(geta('beta/HHT_TP').real)
			
			str_tcl = '{}integrator HHT_TP {}{}\n'.format(pinfo.indent, alpha_HHT_TP, optional_HHT_TP)

		# ----------------- HHTGeneralizedExplicit_TP -----------------
		elif transientIntegrators == 'HHTGeneralizedExplicit_TP':
			# rhoB/HHTGeneralizedExplicit_TP
			sopt_HHTGE = ''
			if geta('rhoB alphaF').boolean:
				sopt_HHTGE += ' {}'.format(geta('rhoB/HHTGeneralizedExplicit_TP').real)
				sopt_HHTGE += ' {}'.format(geta('alphaF/HHTGeneralizedExplicit_TP').real)
			
			if geta('alphaI alphaF beta gamma').boolean:
				sopt_HHTGE += ' {}'.format(geta('alphaI/HHTGeneralizedExplicit_TP').real)
				sopt_HHTGE += ' {}'.format(geta('alphaF/HHTGeneralizedExplicit_TP').real)
				sopt_HHTGE += ' {}'.format(geta('beta/HHTGeneralizedExplicit_TP').real)
				sopt_HHTGE += ' {}'.format(geta('gamma/HHTGeneralizedExplicit_TP').real)

			str_tcl = '{}integrator HHTGeneralizedExplicit_TP{}\n'.format(pinfo.indent, sopt_HHTGE)

		# ----------------- KRAlphaExplicit_TP -----------------
		elif transientIntegrators == 'KRAlphaExplicit_TP':
			str_tcl = '{}integrator KRAlphaExplicit_TP {}\n'.format(pinfo.indent, geta('rhoInf/KRAlphaExplicit_TP').real)

		# ----------------- TRBDF2 -----------------
		elif transientIntegrators == 'TRBDF2':
			str_tcl = '{}integrator TRBDF2\n'.format(pinfo.indent)
			
		# ----------------- Explicit Difference -----------------
		elif transientIntegrators == 'Explicit Difference':
			str_tcl = '{}integrator ExplicitDifference\n'.format(pinfo.indent)
		
	# now write the string into the file
	pinfo.out_file.write(str_tcl)