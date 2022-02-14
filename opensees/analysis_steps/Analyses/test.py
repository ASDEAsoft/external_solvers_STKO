from PyMpc import *
from mpc_utils_html import *

def getOpenSeesCommandName(testCommand):
	if testCommand == 'Norm Unbalance Test':
		return 'NormUnbalance'
	elif testCommand == 'Norm Displacement Increment Test':
		return 'NormDispIncr'
	elif testCommand == 'Energy Increment Test':
		return 'EnergyIncr'
	elif testCommand == 'Relative Norm Unbalance Test':
		return 'RelativeNormUnbalance'
	elif testCommand == 'Relative Norm Displacement Increment Test':
		return 'RelativeNormDispIncr'
	elif testCommand == 'Total Relative Norm Displacement Increment Test':
		return 'RelativeTotalNormDispIncr'
	elif testCommand == 'Relative Energy Increment Test':
		return 'RelativeEnergyIncr'
	elif testCommand == 'Fixed Number of Iterations':
		return 'FixedNumIter'
	raise Exception('Unknown attribute name for test command: {}'.format(testCommand))

def testCommand(xom, group_suffix=''):
	
	group = 'test' + str(group_suffix)
	# test testType? arg1? ...
	
	# testCommand
	at_testCommand = MpcAttributeMetaData()
	at_testCommand.type = MpcAttributeType.String
	at_testCommand.name = 'testCommand'
	at_testCommand.group = group
	at_testCommand.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('testCommand')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Test_Command','Test Command')+'<br/>') +
		html_end()
		)
	at_testCommand.sourceType = MpcAttributeSourceType.List
	at_testCommand.setSourceList(['Norm Unbalance Test', 'Norm Displacement Increment Test', 'Energy Increment Test',
	'Relative Norm Unbalance Test', 'Relative Norm Displacement Increment Test', 'Total Relative Norm Displacement Increment Test', 
	'Relative Energy Increment Test', 'Fixed Number of Iterations'])
	at_testCommand.setDefault('Norm Unbalance Test')
	
	#------------------------------------------- Norm Unbalance Test -------------------------------------------
	
	# test NormUnbalance $tol $iter <$pFlag> <$nType>
	
	# NormUnbalance 
	at_NormUnbalance = MpcAttributeMetaData()
	at_NormUnbalance.type = MpcAttributeType.Boolean
	at_NormUnbalance.name = 'Norm Unbalance Test'
	at_NormUnbalance.group = group
	at_NormUnbalance.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('NormUnbalance')+'<br/>') + 
		html_par('Norm Unbalance Test') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Unbalance_Test','Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_NormUnbalance.editable = False
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol/NormUnbalance'
	at_tol.group = group
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('t	the tolerance criteria used to check for convergence') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Unbalance_Test','Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_tol.setDefault(0.0001)
	
	# iter
	at_iter = MpcAttributeMetaData()
	at_iter.type = MpcAttributeType.Integer
	at_iter.name = 'iter/NormUnbalance'
	at_iter.group = group
	at_iter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('iter')+'<br/>') +
		html_par('the max number of iterations to check before returning failure condition') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Unbalance_Test','Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_iter.setDefault(10)
	
	# use_pFlag
	at_use_pFlag = MpcAttributeMetaData()
	at_use_pFlag.type = MpcAttributeType.Boolean
	at_use_pFlag.name = 'use_pFlag/NormUnbalance'
	at_use_pFlag.group = group
	at_use_pFlag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_pFlag')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Displacement_Increment_Test','Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_use_pFlag.setDefault(False)
	at_use_pFlag.editable= False
	
	# pFlag
	at_pFlag = MpcAttributeMetaData()
	at_pFlag.type = MpcAttributeType.String
	at_pFlag.name = 'pFlag/NormUnbalance'
	at_pFlag.group = group
	at_pFlag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pFlag')+'<br/>') +
		html_par('optional print flag, default is 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Unbalance_Test','Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_pFlag.sourceType = MpcAttributeSourceType.List
	at_pFlag.setSourceList(['0', '1', '2', '3', '4', '5'])
	at_pFlag.setDefault('0')
	
	# use_nType
	at_use_nType = MpcAttributeMetaData()
	at_use_nType.type = MpcAttributeType.Boolean
	at_use_nType.name = 'use_nType/NormUnbalance'
	at_use_nType.group = group
	at_use_nType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_nType')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Displacement_Increment_Test','Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	
	# nType
	at_nType = MpcAttributeMetaData()
	at_nType.type = MpcAttributeType.Integer
	at_nType.name = 'nType/NormUnbalance'
	at_nType.group = group
	at_nType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nType')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Unbalance_Test','Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------- Norm Displacement Increment Test ------------------------------
	
	# test NormDispIncr $tol $iter <$pFlag> <$nType>
	
	# NormDispIncr 
	at_NormDispIncr = MpcAttributeMetaData()
	at_NormDispIncr.type = MpcAttributeType.Boolean
	at_NormDispIncr.name = 'Norm Displacement Increment Test'
	at_NormDispIncr.group = group
	at_NormDispIncr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('NormDispIncr')+'<br/>') + 
		html_par('Norm Displacement Increment Test') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Displacement_Increment_Test','Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_NormDispIncr.editable = False
	
	# tol/NormDispIncr
	at_tol_1 = MpcAttributeMetaData()
	at_tol_1.type = MpcAttributeType.Real
	at_tol_1.name = 'tol/NormDispIncr'
	at_tol_1.group = group
	at_tol_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('t	the tolerance criteria used to check for convergence') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Displacement_Increment_Test','Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_tol_1.setDefault(0.0001)
	
	# iter/NormDispIncr
	at_iter_1 = MpcAttributeMetaData()
	at_iter_1.type = MpcAttributeType.Integer
	at_iter_1.name = 'iter/NormDispIncr'
	at_iter_1.group = group
	at_iter_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('iter')+'<br/>') +
		html_par('the max number of iterations to check before returning failure condition') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Displacement_Increment_Test','Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_iter_1.setDefault(10)
	# use_pFlag/NormDispIncr
	at_use_pFlag_1 = MpcAttributeMetaData()
	at_use_pFlag_1.type = MpcAttributeType.Boolean
	at_use_pFlag_1.name = 'use_pFlag/NormDispIncr'
	at_use_pFlag_1.group = group
	at_use_pFlag_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_pFlag')+'<br/>') +
		html_par('optional print flag, default is 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Displacement_Increment_Test','Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_use_pFlag_1.setDefault(False)
	at_use_pFlag_1.editable= False
	
	# pFlag/NormDispIncr
	at_pFlag_1 = MpcAttributeMetaData()
	at_pFlag_1.type = MpcAttributeType.String
	at_pFlag_1.name = 'pFlag/NormDispIncr'
	at_pFlag_1.group = group
	at_pFlag_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pFlag')+'<br/>') +
		html_par('optional print flag, default is 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Displacement_Increment_Test','Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_pFlag_1.sourceType = MpcAttributeSourceType.List
	at_pFlag_1.setSourceList(['0', '1', '2', '3', '4', '5'])
	at_pFlag_1.setDefault('0')
	
	# use_nType/NormDispIncr
	at_use_nType_1 = MpcAttributeMetaData()
	at_use_nType_1.type = MpcAttributeType.Boolean
	at_use_nType_1.name = 'use_nType/NormDispIncr'
	at_use_nType_1.group = group
	at_use_nType_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_nType')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Displacement_Increment_Test','Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	
	# nType/NormDispIncr
	at_nType_1 = MpcAttributeMetaData()
	at_nType_1.type = MpcAttributeType.Integer
	at_nType_1.name = 'nType/NormDispIncr'
	at_nType_1.group = group
	at_nType_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nType')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Norm_Displacement_Increment_Test','Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------- Energy Increment Test -----------------------------------------
	
	# test EnergyIncr $tol $iter <$pFlag> <$nType>
	
	# EnergyIncr 
	at_EnergyIncr = MpcAttributeMetaData()
	at_EnergyIncr.type = MpcAttributeType.Boolean
	at_EnergyIncr.name = 'Energy Increment Test'
	at_EnergyIncr.group = group
	at_EnergyIncr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('EnergyIncr')+'<br/>') + 
		html_par('Norm Unbalance Test') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Energy_Increment_Test','Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_EnergyIncr.editable = False
	
	# tol/EnergyIncr
	at_tol_2 = MpcAttributeMetaData()
	at_tol_2.type = MpcAttributeType.Real
	at_tol_2.name = 'tol/EnergyIncr'
	at_tol_2.group = group
	at_tol_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('t	the tolerance criteria used to check for convergence') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Energy_Increment_Test','Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_tol_2.setDefault(0.0001)

	# iter/EnergyIncr
	at_iter_2 = MpcAttributeMetaData()
	at_iter_2.type = MpcAttributeType.Integer
	at_iter_2.name = 'iter/EnergyIncr'
	at_iter_2.group = group
	at_iter_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('iter')+'<br/>') +
		html_par('the max number of iterations to check before returning failure condition') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Energy_Increment_Test','Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_iter_2.setDefault(10)

	# use_pFlag/EnergyIncr
	at_use_pFlag_2 = MpcAttributeMetaData()
	at_use_pFlag_2.type = MpcAttributeType.Boolean
	at_use_pFlag_2.name = 'use_pFlag/EnergyIncr'
	at_use_pFlag_2.group = group
	at_use_pFlag_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_pFlag')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Energy_Increment_Test','Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_use_pFlag_2.setDefault(False)
	at_use_pFlag_2.editable= False
	
	# pFlag/EnergyIncr
	at_pFlag_2 = MpcAttributeMetaData()
	at_pFlag_2.type = MpcAttributeType.String
	at_pFlag_2.name = 'pFlag/EnergyIncr'
	at_pFlag_2.group = group
	at_pFlag_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pFlag')+'<br/>') +
		html_par('optional print flag, default is 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Energy_Increment_Test','Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_pFlag_2.sourceType = MpcAttributeSourceType.List
	at_pFlag_2.setSourceList(['0', '1', '2', '3', '4', '5'])
	at_pFlag_2.setDefault('0')
	
	# use_nType/EnergyIncr
	at_use_nType_2 = MpcAttributeMetaData()
	at_use_nType_2.type = MpcAttributeType.Boolean
	at_use_nType_2.name = 'use_nType/EnergyIncr'
	at_use_nType_2.group = group
	at_use_nType_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_nType')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Energy_Increment_Test','Energy Increment Test')+'<br/>') +
		html_end()
		)
		
		
	# nType/EnergyIncr
	at_nType_2 = MpcAttributeMetaData()
	at_nType_2.type = MpcAttributeType.Integer
	at_nType_2.name = 'nType/EnergyIncr'
	at_nType_2.group = group
	at_nType_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nType')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Energy_Increment_Test','Energy Increment Test')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------- Relative Norm Unbalance Test ----------------------------------
	
	# test RelativeNormUnbalance $tol $iter <$pFlag> <$nType>
	
	# RelativeNormUnbalance
	at_RelativeNormUnbalance = MpcAttributeMetaData()
	at_RelativeNormUnbalance.type = MpcAttributeType.Boolean
	at_RelativeNormUnbalance.name = 'Relative Norm Unbalance Test'
	at_RelativeNormUnbalance.group = group
	at_RelativeNormUnbalance.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('RelativeNormUnbalance')+'<br/>') + 
		html_par('Norm Unbalance Test') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Unbalance_Test','Relative Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_RelativeNormUnbalance.editable = False
	
	# tol/RelativeNormUnbalance
	at_tol_3 = MpcAttributeMetaData()
	at_tol_3.type = MpcAttributeType.Real
	at_tol_3.name = 'tol/RelativeNormUnbalance'
	at_tol_3.group = group
	at_tol_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('t	the tolerance criteria used to check for convergence') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Unbalance_Test','Relative Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_tol_3.setDefault(0.0001)
	
	# iter/RelativeNormUnbalance
	at_iter_3 = MpcAttributeMetaData()
	at_iter_3.type = MpcAttributeType.Integer
	at_iter_3.name = 'iter/RelativeNormUnbalance'
	at_iter_3.group = group
	at_iter_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('iter')+'<br/>') +
		html_par('the max number of iterations to check before returning failure condition') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Unbalance_Test','Relative Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_iter_3.setDefault(10)
	
	# use_pFlag/RelativeNormUnbalance
	at_use_pFlag_3 = MpcAttributeMetaData()
	at_use_pFlag_3.type = MpcAttributeType.Boolean
	at_use_pFlag_3.name = 'use_pFlag/RelativeNormUnbalance'
	at_use_pFlag_3.group = group
	at_use_pFlag_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_pFlag')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Unbalance_Test','Relative Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_use_pFlag_3.setDefault(False)
	at_use_pFlag_3.editable= False
	
	# pFlag/RelativeNormUnbalance
	at_pFlag_3 = MpcAttributeMetaData()
	at_pFlag_3.type = MpcAttributeType.String
	at_pFlag_3.name = 'pFlag/RelativeNormUnbalance'
	at_pFlag_3.group = group
	at_pFlag_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pFlag')+'<br/>') +
		html_par('optional print flag, default is 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Unbalance_Test','Relative Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	at_pFlag_3.sourceType = MpcAttributeSourceType.List
	at_pFlag_3.setSourceList(['0', '1', '2', '3', '4', '5'])
	at_pFlag_3.setDefault('0')
	
	# use_nType/RelativeNormUnbalance
	at_use_nType_3 = MpcAttributeMetaData()
	at_use_nType_3.type = MpcAttributeType.Boolean
	at_use_nType_3.name = 'use_nType/RelativeNormUnbalance'
	at_use_nType_3.group = group
	at_use_nType_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_nType')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Unbalance_Test','Relative Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	
	# nType/RelativeNormUnbalance
	at_nType_3 = MpcAttributeMetaData()
	at_nType_3.type = MpcAttributeType.Integer
	at_nType_3.name = 'nType/RelativeNormUnbalance'
	at_nType_3.group = group
	at_nType_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nType')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Unbalance_Test','Relative Norm Unbalance Test')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------- Relative Norm Displacement Increment Test -------------------------------------------
	
	# test RelativeNormDispIncr $tol $iter <$pFlag> <$nType>
	
	# RelativeNormDispIncr
	at_RelativeNormDispIncr = MpcAttributeMetaData()
	at_RelativeNormDispIncr.type = MpcAttributeType.Boolean
	at_RelativeNormDispIncr.name = 'Relative Norm Displacement Increment Test'
	at_RelativeNormDispIncr.group = group
	at_RelativeNormDispIncr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('RelativeNormDispIncr')+'<br/>') + 
		html_par('Norm Unbalance Test') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Displacement_Increment_Test','Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_RelativeNormDispIncr.editable = False
	
	# tol/RelativeNormDispIncr
	at_tol_4 = MpcAttributeMetaData()
	at_tol_4.type = MpcAttributeType.Real
	at_tol_4.name = 'tol/RelativeNormDispIncr'
	at_tol_4.group = group
	at_tol_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('t	the tolerance criteria used to check for convergence') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Displacement_Increment_Test','Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_tol_4.setDefault(0.0001)

	# iter/RelativeNormDispIncr
	at_iter_4 = MpcAttributeMetaData()
	at_iter_4.type = MpcAttributeType.Integer
	at_iter_4.name = 'iter/RelativeNormDispIncr'
	at_iter_4.group = group
	at_iter_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('iter')+'<br/>') +
		html_par('the max number of iterations to check before returning failure condition') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Displacement_Increment_Test','Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_iter_4.setDefault(10)

	# use_pFlag/RelativeNormDispIncr
	at_use_pFlag_4 = MpcAttributeMetaData()
	at_use_pFlag_4.type = MpcAttributeType.Boolean
	at_use_pFlag_4.name = 'use_pFlag/RelativeNormDispIncr'
	at_use_pFlag_4.group = group
	at_use_pFlag_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_pFlag')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Displacement_Increment_Test','Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_use_pFlag_4.setDefault(False)
	at_use_pFlag_4.editable= False
	
	# pFlag/RelativeNormDispIncr
	at_pFlag_4 = MpcAttributeMetaData()
	at_pFlag_4.type = MpcAttributeType.String
	at_pFlag_4.name = 'pFlag/RelativeNormDispIncr'
	at_pFlag_4.group = group
	at_pFlag_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pFlag')+'<br/>') +
		html_par('optional print flag, default is 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Displacement_Increment_Test','Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_pFlag_4.sourceType = MpcAttributeSourceType.List
	at_pFlag_4.setSourceList(['0', '1', '2', '3', '4', '5'])
	at_pFlag_4.setDefault('0')
	
	# use_nType/RelativeNormDispIncr
	at_use_nType_4 = MpcAttributeMetaData()
	at_use_nType_4.type = MpcAttributeType.Boolean
	at_use_nType_4.name = 'use_nType/RelativeNormDispIncr'
	at_use_nType_4.group = group
	at_use_nType_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_nType')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Displacement_Increment_Test','Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	
	# nType/RelativeNormDispIncr
	at_nType_4 = MpcAttributeMetaData()
	at_nType_4.type = MpcAttributeType.Integer
	at_nType_4.name = 'nType/RelativeNormDispIncr'
	at_nType_4.group = group
	at_nType_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nType')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Norm_Displacement_Increment_Test','Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------- Total Relative Norm Displacement Increment Test -------------------------------------------
	
	# test RelativeTotalNormDispIncr $tol $iter <$pFlag> <$nType>
	
	# RelativeTotalNormDispIncr
	at_RelativeTotalNormDispIncr = MpcAttributeMetaData()
	at_RelativeTotalNormDispIncr.type = MpcAttributeType.Boolean
	at_RelativeTotalNormDispIncr.name = 'Total Relative Norm Displacement Increment Test'
	at_RelativeTotalNormDispIncr.group = group
	at_RelativeTotalNormDispIncr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('RelativeNormDispIncr')+'<br/>') + 
		html_par('Norm Unbalance Test') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Total_Relative_Norm_Displacement_Increment_Test','Total Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_RelativeTotalNormDispIncr.editable = False
	
	# tol/RelativeTotalNormDispIncr
	at_tol_5 = MpcAttributeMetaData()
	at_tol_5.type = MpcAttributeType.Real
	at_tol_5.name = 'tol/RelativeTotalNormDispIncr'
	at_tol_5.group = group
	at_tol_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('t	the tolerance criteria used to check for convergence') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Total_Relative_Norm_Displacement_Increment_Test','Total Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_tol_5.setDefault(0.0001)

	# iter/RelativeTotalNormDispIncr
	at_iter_5 = MpcAttributeMetaData()
	at_iter_5.type = MpcAttributeType.Integer
	at_iter_5.name = 'iter/RelativeTotalNormDispIncr'
	at_iter_5.group = group
	at_iter_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('iter')+'<br/>') +
		html_par('the max number of iterations to check before returning failure condition') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Total_Relative_Norm_Displacement_Increment_Test','Total Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_iter_5.setDefault(10)

	# use_pFlag/RelativeTotalNormDispIncr
	at_use_pFlag_5 = MpcAttributeMetaData()
	at_use_pFlag_5.type = MpcAttributeType.Boolean
	at_use_pFlag_5.name = 'use_pFlag/RelativeTotalNormDispIncr'
	at_use_pFlag_5.group = group
	at_use_pFlag_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_pFlag')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Total_Relative_Norm_Displacement_Increment_Test','Total Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_use_pFlag_5.setDefault(False)
	at_use_pFlag_5.editable= False
	
	# pFlag/RelativeTotalNormDispIncr
	at_pFlag_5 = MpcAttributeMetaData()
	at_pFlag_5.type = MpcAttributeType.String
	at_pFlag_5.name = 'pFlag/RelativeTotalNormDispIncr'
	at_pFlag_5.group = group
	at_pFlag_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pFlag')+'<br/>') +
		html_par('optional print flag, default is 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Total_Relative_Norm_Displacement_Increment_Test','Total Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	at_pFlag_5.sourceType = MpcAttributeSourceType.List
	at_pFlag_5.setSourceList(['0', '1', '2', '3', '4', '5'])
	at_pFlag_5.setDefault('0')
	
	# use_nType/RelativeTotalNormDispIncr
	at_use_nType_5 = MpcAttributeMetaData()
	at_use_nType_5.type = MpcAttributeType.Boolean
	at_use_nType_5.name = 'use_nType/RelativeTotalNormDispIncr'
	at_use_nType_5.group = group
	at_use_nType_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_nType')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Total_Relative_Norm_Displacement_Increment_Test','Total Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
		
		
	# nType/RelativeTotalNormDispIncr
	at_nType_5 = MpcAttributeMetaData()
	at_nType_5.type = MpcAttributeType.Integer
	at_nType_5.name = 'nType/RelativeTotalNormDispIncr'
	at_nType_5.group = group
	at_nType_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nType')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Total_Relative_Norm_Displacement_Increment_Test','Total Relative Norm Displacement Increment Test')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------- Relative Energy Increment Test --------------------------------
	
	# test RelativeEnergyIncr $tol $iter <$pFlag> <$nType>
	
	# RelativeEnergyIncr
	at_RelativeEnergyIncr = MpcAttributeMetaData()
	at_RelativeEnergyIncr.type = MpcAttributeType.Boolean
	at_RelativeEnergyIncr.name = 'Relative Energy Increment Test'
	at_RelativeEnergyIncr.group = group
	at_RelativeEnergyIncr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('RelativeNormDispIncr')+'<br/>') + 
		html_par('Norm Unbalance Test') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Energy_Increment_Test','Relative Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_RelativeEnergyIncr.editable = False
	
	# tol/RelativeEnergyIncr
	at_tol_6 = MpcAttributeMetaData()
	at_tol_6.type = MpcAttributeType.Real
	at_tol_6.name = 'tol/RelativeEnergyIncr'
	at_tol_6.group = group
	at_tol_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('t	the tolerance criteria used to check for convergence') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Energy_Increment_Test','Relative Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_tol_6.setDefault(0.0001)

	# iter/RelativeEnergyIncr
	at_iter_6 = MpcAttributeMetaData()
	at_iter_6.type = MpcAttributeType.Integer
	at_iter_6.name = 'iter/RelativeEnergyIncr'
	at_iter_6.group = group
	at_iter_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('iter')+'<br/>') +
		html_par('the max number of iterations to check before returning failure condition') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Energy_Increment_Test','Relative Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_iter_6.setDefault(10)

	# use_pFlag/RelativeEnergyIncr
	at_use_pFlag_6 = MpcAttributeMetaData()
	at_use_pFlag_6.type = MpcAttributeType.Boolean
	at_use_pFlag_6.name = 'use_pFlag/RelativeEnergyIncr'
	at_use_pFlag_6.group = group
	at_use_pFlag_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_pFlag')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Energy_Increment_Test','Relative Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_use_pFlag_6.setDefault(False)
	at_use_pFlag_6.editable= False
	
	# pFlag/RelativeEnergyIncr
	at_pFlag_6 = MpcAttributeMetaData()
	at_pFlag_6.type = MpcAttributeType.String
	at_pFlag_6.name = 'pFlag/RelativeEnergyIncr'
	at_pFlag_6.group = group
	at_pFlag_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pFlag')+'<br/>') +
		html_par('optional print flag, default is 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Energy_Increment_Test','Relative Energy Increment Test')+'<br/>') +
		html_end()
		)
	at_pFlag_6.sourceType = MpcAttributeSourceType.List
	at_pFlag_6.setSourceList(['0', '1', '2', '3', '4', '5'])
	at_pFlag_6.setDefault('0')
	
	# use_nType/RelativeEnergyIncr
	at_use_nType_6 = MpcAttributeMetaData()
	at_use_nType_6.type = MpcAttributeType.Boolean
	at_use_nType_6.name = 'use_nType/RelativeEnergyIncr'
	at_use_nType_6.group = group
	at_use_nType_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_nType')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Energy_Increment_Test','Relative Energy Increment Test')+'<br/>') +
		html_end()
		)
	
	# nType/RelativeEnergyIncr
	at_nType_6 = MpcAttributeMetaData()
	at_nType_6.type = MpcAttributeType.Integer
	at_nType_6.name = 'nType/RelativeEnergyIncr'
	at_nType_6.group = group
	at_nType_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nType')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Relative_Energy_Increment_Test','Relative Energy Increment Test')+'<br/>') +
		html_end()
		)
	
	#-----------------------------------------------------------------------------------------------------------
	#------------------------------------------- Fixed Number of Iterations ------------------------------------
	
	# test FixedNumIter $iter <$pFlag> <$nType>
	
	# FixedNumIter
	at_FixedNumIter = MpcAttributeMetaData()
	at_FixedNumIter.type = MpcAttributeType.Boolean
	at_FixedNumIter.name = 'Fixed Number of Iterations'
	at_FixedNumIter.group = group
	at_FixedNumIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('FixedNumIter')+'<br/>') + 
		html_par('Norm Unbalance Test') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fixed_Number_of_Iterations','Fixed Number of Iterations')+'<br/>') +
		html_end()
		)
	at_FixedNumIter.editable = False

	# iter/FixedNumIter
	at_iter_7 = MpcAttributeMetaData()
	at_iter_7.type = MpcAttributeType.Integer
	at_iter_7.name = 'iter/FixedNumIter'
	at_iter_7.group = group
	at_iter_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('iter')+'<br/>') +
		html_par('the max number of iterations to check before returning failure condition') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fixed_Number_of_Iterations','Fixed Number of Iterations')+'<br/>') +
		html_end()
		)
	at_iter_7.setDefault(10)

	# use_pFlag/FixedNumIter
	at_use_pFlag_7 = MpcAttributeMetaData()
	at_use_pFlag_7.type = MpcAttributeType.Boolean
	at_use_pFlag_7.name = 'use_pFlag/FixedNumIter'
	at_use_pFlag_7.group = group
	at_use_pFlag_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_pFlag')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fixed_Number_of_Iterations','Fixed Number of Iterations')+'<br/>') +
		html_end()
		)
	at_use_pFlag_7.setDefault(False)
	at_use_pFlag_7.editable= False
		
	# pFlag/FixedNumIter
	at_pFlag_7 = MpcAttributeMetaData()
	at_pFlag_7.type = MpcAttributeType.String
	at_pFlag_7.name = 'pFlag/FixedNumIter'
	at_pFlag_7.group = group
	at_pFlag_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pFlag')+'<br/>') +
		html_par('optional print flag, default is 0') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fixed_Number_of_Iterations','Fixed Number of Iterations')+'<br/>') +
		html_end()
		)
	at_pFlag_7.sourceType = MpcAttributeSourceType.List
	at_pFlag_7.setSourceList(['0', '1', '2', '3', '4', '5'])
	at_pFlag_7.setDefault('0')
		
		
	# use_nType/FixedNumIter
	at_use_nType_7 = MpcAttributeMetaData()
	at_use_nType_7.type = MpcAttributeType.Boolean
	at_use_nType_7.name = 'use_nType/FixedNumIter'
	at_use_nType_7.group = group
	at_use_nType_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_nType')+'<br/>') +
		html_par('time-step increment. Required if transient or variable transient analysis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fixed_Number_of_Iterations','Fixed Number of Iterations')+'<br/>') +
		html_end()
		)
		
		
	# nType/FixedNumIter
	at_nType_7 = MpcAttributeMetaData()
	at_nType_7.type = MpcAttributeType.Integer
	at_nType_7.name = 'nType/FixedNumIter'
	at_nType_7.group = group
	at_nType_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nType')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Fixed_Number_of_Iterations','Fixed Number of Iterations')+'<br/>') +
		html_end()
		)
	
	xom.addAttribute(at_testCommand)
	xom.addAttribute(at_NormUnbalance)
	xom.addAttribute(at_tol)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_use_pFlag)
	xom.addAttribute(at_pFlag)
	xom.addAttribute(at_use_nType)
	xom.addAttribute(at_nType)
	
	
	xom.addAttribute(at_NormDispIncr)
	xom.addAttribute(at_tol_1)
	xom.addAttribute(at_iter_1)
	xom.addAttribute(at_use_pFlag_1)
	xom.addAttribute(at_pFlag_1)
	xom.addAttribute(at_use_nType_1)
	xom.addAttribute(at_nType_1)
	
	
	xom.addAttribute(at_EnergyIncr)
	xom.addAttribute(at_tol_2)
	xom.addAttribute(at_iter_2)
	xom.addAttribute(at_use_pFlag_2)
	xom.addAttribute(at_pFlag_2)
	xom.addAttribute(at_use_nType_2)
	xom.addAttribute(at_nType_2)
	
	
	xom.addAttribute(at_RelativeNormUnbalance)
	xom.addAttribute(at_tol_3)
	xom.addAttribute(at_iter_3)
	xom.addAttribute(at_use_pFlag_3)
	xom.addAttribute(at_pFlag_3)
	xom.addAttribute(at_use_nType_3)
	xom.addAttribute(at_nType_3)
	
	
	xom.addAttribute(at_RelativeNormDispIncr)
	xom.addAttribute(at_tol_4)
	xom.addAttribute(at_iter_4)
	xom.addAttribute(at_use_pFlag_4)
	xom.addAttribute(at_pFlag_4)
	xom.addAttribute(at_use_nType_4)
	xom.addAttribute(at_nType_4)
	
	
	xom.addAttribute(at_RelativeTotalNormDispIncr)
	xom.addAttribute(at_tol_5)
	xom.addAttribute(at_iter_5)
	xom.addAttribute(at_use_pFlag_5)
	xom.addAttribute(at_pFlag_5)
	xom.addAttribute(at_use_nType_5)
	xom.addAttribute(at_nType_5)
	
	
	xom.addAttribute(at_RelativeEnergyIncr)
	xom.addAttribute(at_tol_6)
	xom.addAttribute(at_iter_6)
	xom.addAttribute(at_use_pFlag_6)
	xom.addAttribute(at_pFlag_6)
	xom.addAttribute(at_use_nType_6)
	xom.addAttribute(at_nType_6)
	
	
	xom.addAttribute(at_FixedNumIter)
	xom.addAttribute(at_iter_7)
	xom.addAttribute(at_use_pFlag_7)
	xom.addAttribute(at_pFlag_7)
	xom.addAttribute(at_use_nType_7)
	xom.addAttribute(at_nType_7)
	
	
	# NormUnbalance
	xom.setVisibilityDependency(at_NormUnbalance, at_tol)
	xom.setVisibilityDependency(at_NormUnbalance, at_iter)
	
	xom.setVisibilityDependency(at_NormUnbalance, at_use_pFlag)
	xom.setVisibilityDependency(at_NormUnbalance, at_pFlag)
	xom.setVisibilityDependency(at_use_pFlag, at_pFlag)
	
	xom.setVisibilityDependency(at_NormUnbalance, at_use_nType)
	xom.setVisibilityDependency(at_use_nType, at_nType)
	xom.setVisibilityDependency(at_NormUnbalance, at_nType)
	
	# NormDispIncr
	xom.setVisibilityDependency(at_NormDispIncr, at_tol_1)
	xom.setVisibilityDependency(at_NormDispIncr, at_iter_1)
	
	xom.setVisibilityDependency(at_NormDispIncr, at_use_pFlag_1)
	xom.setVisibilityDependency(at_NormDispIncr, at_pFlag_1)
	xom.setVisibilityDependency(at_use_pFlag_1, at_pFlag_1)
	
	xom.setVisibilityDependency(at_NormDispIncr, at_use_nType_1)
	xom.setVisibilityDependency(at_use_nType_1, at_nType_1)
	xom.setVisibilityDependency(at_NormDispIncr, at_nType_1)
	
	# EnergyIncr
	xom.setVisibilityDependency(at_EnergyIncr, at_tol_2)
	xom.setVisibilityDependency(at_EnergyIncr, at_iter_2)
	
	xom.setVisibilityDependency(at_EnergyIncr, at_use_pFlag_2)
	xom.setVisibilityDependency(at_EnergyIncr, at_pFlag_2)
	xom.setVisibilityDependency(at_use_pFlag_2, at_pFlag_2)
	
	xom.setVisibilityDependency(at_EnergyIncr, at_use_nType_2)
	xom.setVisibilityDependency(at_use_nType_2, at_nType_2)
	xom.setVisibilityDependency(at_EnergyIncr, at_nType_2)
	
	# RelativeNormUnbalance
	xom.setVisibilityDependency(at_RelativeNormUnbalance, at_tol_3)
	xom.setVisibilityDependency(at_RelativeNormUnbalance, at_iter_3)
	
	xom.setVisibilityDependency(at_RelativeNormUnbalance, at_use_pFlag_3)
	xom.setVisibilityDependency(at_RelativeNormUnbalance, at_pFlag_3)
	xom.setVisibilityDependency(at_use_pFlag_3, at_pFlag_3)
	
	xom.setVisibilityDependency(at_RelativeNormUnbalance, at_use_nType_3)
	xom.setVisibilityDependency(at_use_nType_3, at_nType_3)
	xom.setVisibilityDependency(at_RelativeNormUnbalance, at_nType_3)
	
	
	# RelativeNormUnbalance
	xom.setVisibilityDependency(at_RelativeNormDispIncr, at_tol_4)
	xom.setVisibilityDependency(at_RelativeNormDispIncr, at_iter_4)
	
	xom.setVisibilityDependency(at_RelativeNormDispIncr, at_use_pFlag_4)
	xom.setVisibilityDependency(at_RelativeNormDispIncr, at_pFlag_4)
	xom.setVisibilityDependency(at_use_pFlag_4, at_pFlag_4)
	
	xom.setVisibilityDependency(at_RelativeNormDispIncr, at_use_nType_4)
	xom.setVisibilityDependency(at_use_nType_4, at_nType_4)
	xom.setVisibilityDependency(at_RelativeNormDispIncr, at_nType_4)
	
	
	# RelativeTotalNormDispIncr
	xom.setVisibilityDependency(at_RelativeTotalNormDispIncr, at_tol_5)
	xom.setVisibilityDependency(at_RelativeTotalNormDispIncr, at_iter_5)
	
	xom.setVisibilityDependency(at_RelativeTotalNormDispIncr, at_use_pFlag_5)
	xom.setVisibilityDependency(at_RelativeTotalNormDispIncr, at_pFlag_5)
	xom.setVisibilityDependency(at_use_pFlag_5, at_pFlag_5)
	
	xom.setVisibilityDependency(at_RelativeTotalNormDispIncr, at_use_nType_5)
	xom.setVisibilityDependency(at_use_nType_5, at_nType_5)
	xom.setVisibilityDependency(at_RelativeTotalNormDispIncr, at_nType_5)
	
	
	# RelativeEnergyIncr
	xom.setVisibilityDependency(at_RelativeEnergyIncr, at_tol_6)
	xom.setVisibilityDependency(at_RelativeEnergyIncr, at_iter_6)
	
	xom.setVisibilityDependency(at_RelativeEnergyIncr, at_use_pFlag_6)
	xom.setVisibilityDependency(at_RelativeEnergyIncr, at_pFlag_6)
	xom.setVisibilityDependency(at_use_pFlag_6, at_pFlag_6)
	
	xom.setVisibilityDependency(at_RelativeEnergyIncr, at_use_nType_6)
	xom.setVisibilityDependency(at_use_nType_6, at_nType_6)
	xom.setVisibilityDependency(at_RelativeEnergyIncr, at_nType_6)
	
	# FixedNumIter
	xom.setVisibilityDependency(at_FixedNumIter, at_iter_7)
	
	xom.setVisibilityDependency(at_FixedNumIter, at_use_pFlag_7)
	xom.setVisibilityDependency(at_FixedNumIter, at_pFlag_7)
	xom.setVisibilityDependency(at_use_pFlag_7, at_pFlag_7)
	
	xom.setVisibilityDependency(at_FixedNumIter, at_use_nType_7)
	xom.setVisibilityDependency(at_use_nType_7, at_nType_7)
	xom.setVisibilityDependency(at_FixedNumIter, at_nType_7)
	
	# auto-exclusive dependencies
	
	xom.setBooleanAutoExclusiveDependency(at_testCommand, at_NormUnbalance)
	
	xom.setBooleanAutoExclusiveDependency(at_testCommand, at_NormDispIncr)
	
	xom.setBooleanAutoExclusiveDependency(at_testCommand, at_EnergyIncr)
	
	xom.setBooleanAutoExclusiveDependency(at_testCommand, at_RelativeNormUnbalance)
	
	xom.setBooleanAutoExclusiveDependency(at_testCommand, at_RelativeNormDispIncr)
	
	xom.setBooleanAutoExclusiveDependency(at_testCommand, at_RelativeTotalNormDispIncr)
	
	xom.setBooleanAutoExclusiveDependency(at_testCommand, at_RelativeEnergyIncr)
	
	xom.setBooleanAutoExclusiveDependency(at_testCommand, at_FixedNumIter)

def writeTcl_test(pinfo, xobj, group_suffix='', iter_override = None):
	
	# utility to get attribute from xobject
	def get_attr(at_name):
		at = xobj.getAttribute(at_name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(at_name))
		return at
	
	# get the test command
	testCommand = get_attr('testCommand').string
	
	# process based on test command type
	# common procedure
	cmd_name = getOpenSeesCommandName(testCommand)
	# default parameters
	tol = '' # init tolerance as empty strin (not double) because one of the test does not want it
	iter = 0
	pFlag = None # default to None, so that if the user does not set it, but sets the nType, we make it 0
	nType = None
	# get tolerance - not mandatory
	try:
		tol = get_attr('tol/{}'.format(cmd_name)).real
	except:
		pass
	# get num iter
	iter = get_attr('iter/{}'.format(cmd_name)).integer
	if iter_override:
		iter = iter_override
	# get pFlag
	if get_attr('use_pFlag/{}'.format(cmd_name)).boolean:
		pFlag = get_attr('pFlag/{}'.format(cmd_name)).string
	# get nType
	if get_attr('use_nType/{}'.format(cmd_name)).boolean:
		nType = get_attr('nType/{}'.format(cmd_name)).integer
	# if nType is set, force pFlag to 0 if unset
	if (nType is not None) and (pFlag is None):
		pFlag = '0'
	# convert None to empty string
	if pFlag is None:
		pFlag = ''
	if nType is None:
		nType = ''
	# write
	pinfo.out_file.write('{}test {} {} {} {} {}\n'.format(pinfo.indent, cmd_name, tol, iter, pFlag, nType))