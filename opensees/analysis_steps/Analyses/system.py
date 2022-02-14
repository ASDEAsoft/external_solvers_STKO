from PyMpc import *
from mpc_utils_html import *

def systemCommand(xom, group_suffix=''):
	
	'''
	system BandGeneral
	system BandSPD
	system ProfileSPD
	system SparseGEN
	system UmfPack <-lvalueFact $LVALUE>
	system FullGeneral
	system SparseSYM
	system Mumps
	system CuSP -rTol $RTOL -mInt $MINT -pre $PRE -solver $SOLVER
	'''
	group = str(group_suffix) + 'system' 
	
	# system
	at_system = MpcAttributeMetaData()
	at_system.type = MpcAttributeType.String
	at_system.name = 'system'
	at_system.group = group
	at_system.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('system')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/System_Command','System Command')+'<br/>') +
		html_end()
		)
	at_system.sourceType = MpcAttributeSourceType.List
	at_system.setSourceList(['BandGeneral SOE', 'BandSPD SOE', 'ProfileSPD SOE', 'SuperLU SOE', 'UmfPack SOE', 'FullGeneral', 'SparseSYM SOE', 'Mumps', 'Cusp', 'ParallelProfileSPD', 'Diagonal', 'MPIDiagonal'])
	at_system.setDefault('UmfPack SOE')
	
	'''
	UmfPack SOE
	'''
	# UmfPack
	at_UmfPack = MpcAttributeMetaData()
	at_UmfPack.type = MpcAttributeType.Boolean
	at_UmfPack.name = 'UmfPack SOE'
	at_UmfPack.group = group
	at_UmfPack.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('UmfPack')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/UmfPack_SOE','UmfPack SOE')+'<br/>') +
		html_end()
		)
	at_UmfPack.editable = False
	
	# -lvalueFact
	at_lvalueFact = MpcAttributeMetaData()
	at_lvalueFact.type = MpcAttributeType.Boolean
	at_lvalueFact.name = '-lvalueFact'
	at_lvalueFact.group = group
	at_lvalueFact.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-lvalueFact')+'<br/>') + 
		html_par('(LVALUE*the number of nonzero entries) is the amount of additional memory set aside for fill in during the matrix solution, \
				by default the LVALUE factor is 10. You only need to experiment with this if you get error messages back about LVALUE being too small.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/UmfPack_SOE','UmfPack SOE')+'<br/>') +
		html_end()
		)
	
	# LVALUE
	at_LVALUE = MpcAttributeMetaData()
	at_LVALUE.type = MpcAttributeType.Integer
	at_LVALUE.name = 'LVALUE'
	at_LVALUE.group = group
	at_LVALUE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('LVALUE')+'<br/>') + 
		html_par('(LVALUE*the number of nonzero entries) is the amount of additional memory set aside for fill in during the matrix solution, \
				by default the LVALUE factor is 10. You only need to experiment with this if you get error messages back about LVALUE being too small.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/UmfPack_SOE','UmfPack SOE')+'<br/>') +
		html_end()
		)
	at_LVALUE.setDefault(10)
	
	'''
	Mumps
	'''
	# Mumps
	at_Mumps = MpcAttributeMetaData()
	at_Mumps.type = MpcAttributeType.Boolean
	at_Mumps.name = 'Mumps'
	at_Mumps.group = group
	at_Mumps.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mumps')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Mumps','Mumps')+'<br/>') +
		html_end()
		)
	at_Mumps.editable = False
	
	# -ICNTL
	at_ICNTL = MpcAttributeMetaData()
	at_ICNTL.type = MpcAttributeType.Boolean
	at_ICNTL.name = '-ICNTL14'
	at_ICNTL.group = group
	at_ICNTL.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-ICNTL14')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Mumps','Mumps')+'<br/>') +
		html_end()
		)
	at_ICNTL.setDefault(True)
	
	# at_ICNTL14_VALUE
	at_ICNTL14_VALUE = MpcAttributeMetaData()
	at_ICNTL14_VALUE.type = MpcAttributeType.Integer
	at_ICNTL14_VALUE.name = 'ICNTL14 Value'
	at_ICNTL14_VALUE.group = group
	at_ICNTL14_VALUE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ICNTL14 Value')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Mumps','Mumps')+'<br/>') +
		html_end()
		)
	at_ICNTL14_VALUE.setDefault(200)
	
	# -matrixType
	at_matrixType = MpcAttributeMetaData()
	at_matrixType.type = MpcAttributeType.Boolean
	at_matrixType.name = '-matrixType'
	at_matrixType.group = group
	at_matrixType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('specify matrix type')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Mumps','Mumps')+'<br/>') +
		html_end()
		)
	at_matrixType.setDefault(False)
	
	# at_matrixType_value
	at_matrixType_value = MpcAttributeMetaData()
	at_matrixType_value.type = MpcAttributeType.String
	at_matrixType_value.name = 'matrixType'
	at_matrixType_value.group = group
	at_matrixType_value.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matrix type')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Mumps','Mumps')+'<br/>') +
		html_end()
		)
	at_matrixType_value.setDefault('Unsymmetric')
	at_matrixType_value.sourceType = MpcAttributeSourceType.List
	at_matrixType_value.setSourceList(['Unsymmetric', 'Symmetric Positive Definite', 'Symmetric General'])
	
	'''
	Cusp
	'''
	# Cusp
	at_Cusp = MpcAttributeMetaData()
	at_Cusp.type = MpcAttributeType.Boolean
	at_Cusp.name = 'Cusp'
	at_Cusp.group = group
	at_Cusp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Cusp')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Cusp','Cusp')+'<br/>') +
		html_end()
		)
	at_Cusp.editable = False
	
	# RTOL
	at_RTOL = MpcAttributeMetaData()
	at_RTOL.type = MpcAttributeType.Real
	at_RTOL.name = 'RTOL'
	at_RTOL.group = group
	at_RTOL.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('RTOL')+'<br/>') + 
		html_par('Set the relative tolerance') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Cusp','Cusp')+'<br/>') +
		html_end()
		)
	
	# MINT
	at_MINT = MpcAttributeMetaData()
	at_MINT.type = MpcAttributeType.Integer
	at_MINT.name = 'MINT'
	at_MINT.group = group
	at_MINT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('MINT')+'<br/>') + 
		html_par('Set the maximum number of iterations') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Cusp','Cusp')+'<br/>') +
		html_end()
		)
	
	# PRE
	at_PRE = MpcAttributeMetaData()
	at_PRE.type = MpcAttributeType.String
	at_PRE.name = 'PRE'
	at_PRE.group = group
	at_PRE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('PRE')+'<br/>') + 
		html_par('Set the preconditioner. can be none, diagonal, and ainv') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Cusp','Cusp')+'<br/>') +
		html_end()
		)
	at_PRE.sourceType = MpcAttributeSourceType.List
	at_PRE.setSourceList(['none', 'diagonal', 'ainv'])
	at_PRE.setDefault('none')
	
	# SOLVER
	at_SOLVER = MpcAttributeMetaData()
	at_SOLVER.type = MpcAttributeType.String
	at_SOLVER.name = 'SOLVER'
	at_SOLVER.group = group
	at_SOLVER.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('SOLVER')+'<br/>') + 
		html_par('Set the iterative solver. can be bicg, bicgstab, cg, and gmres') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Cusp','Cusp')+'<br/>') +
		html_end()
		)
	at_SOLVER.sourceType = MpcAttributeSourceType.List
	at_SOLVER.setSourceList(['bicg', 'bicgstab', 'cg', 'gmres'])
	at_SOLVER.setDefault('bicg')
	
	xom.addAttribute(at_system)
	xom.addAttribute(at_UmfPack)
	xom.addAttribute(at_lvalueFact)
	xom.addAttribute(at_LVALUE)
	xom.addAttribute(at_Mumps)
	xom.addAttribute(at_ICNTL)
	xom.addAttribute(at_ICNTL14_VALUE)
	xom.addAttribute(at_matrixType)
	xom.addAttribute(at_matrixType_value)
	xom.addAttribute(at_Cusp)
	xom.addAttribute(at_RTOL)
	xom.addAttribute(at_MINT)
	xom.addAttribute(at_PRE)
	xom.addAttribute(at_SOLVER)
	
	
	# visibility dependencies
	
	# LVALUE-dep
	xom.setVisibilityDependency(at_UmfPack, at_lvalueFact)
	
	xom.setVisibilityDependency(at_UmfPack, at_LVALUE)
	xom.setVisibilityDependency(at_lvalueFact, at_LVALUE)
	
	# LVALUE-Mumps
	xom.setVisibilityDependency(at_Mumps, at_ICNTL)
	xom.setVisibilityDependency(at_Mumps, at_ICNTL14_VALUE)
	xom.setVisibilityDependency(at_ICNTL, at_ICNTL14_VALUE)
	
	xom.setVisibilityDependency(at_Mumps, at_matrixType)
	xom.setVisibilityDependency(at_Mumps, at_matrixType_value)
	xom.setVisibilityDependency(at_matrixType, at_matrixType_value)
	
	# LVALUE-dep
	xom.setVisibilityDependency(at_Cusp, at_RTOL)
	xom.setVisibilityDependency(at_Cusp, at_MINT)
	xom.setVisibilityDependency(at_Cusp, at_PRE)
	xom.setVisibilityDependency(at_Cusp, at_SOLVER)
	
	
	# auto-exclusive dependencies
	# system
	xom.setBooleanAutoExclusiveDependency(at_system, at_UmfPack)
	xom.setBooleanAutoExclusiveDependency(at_system, at_Mumps)
	xom.setBooleanAutoExclusiveDependency(at_system, at_Cusp)
	
	return xom
	
def writeTcl_system(pinfo, xobj):
	
	'''
	system BandGeneral
	system BandSPD
	system ProfileSPD
	system SparseGEN
	system UmfPack <-lvalueFact $LVALUE>
	system FullGeneral
	system SparseSYM
	system Mumps
	system CuSP -rTol $RTOL -mInt $MINT -pre $PRE -solver $SOLVER
	'''
	
	sopt = ''
	sopt_1 = ''
	
	system_at = xobj.getAttribute('system')
	if(system_at is None):
		raise Exception('Error: cannot find "system" attribute')
	system = system_at.string
	
	if system == 'BandGeneral SOE':
		str_tcl = '{}system BandGeneral\n'.format(pinfo.indent)
	
	elif system == 'BandSPD SOE':
		str_tcl = '{}system BandSPD\n'.format(pinfo.indent)
	
	elif system == 'ProfileSPD SOE':
		str_tcl = '{}system ProfileSPD\n'.format(pinfo.indent)
	
	elif system == 'SuperLU SOE':
		str_tcl = '{}system SparseGEN\n'.format(pinfo.indent)
	
	elif system == 'UmfPack SOE':
		lvalueFact_at = xobj.getAttribute('-lvalueFact')
		if(lvalueFact_at is None):
			raise Exception('Error: cannot find "-lvalueFact" attribute')
		if lvalueFact_at.boolean:
			
			LVALUE_at = xobj.getAttribute('LVALUE')
			if(LVALUE_at is None):
				raise Exception('Error: cannot find "LVALUE" attribute')
			LVALUE = LVALUE_at.integer
			
			sopt += ' -lvalueFact {}'.format(LVALUE)
		
		str_tcl = '{}system UmfPack{}\n'.format(pinfo.indent, sopt)
	
	elif system == 'FullGeneral':
		str_tcl = '{}system FullGeneral\n'.format(pinfo.indent)
	
	elif system == 'SparseSYM SOE':
		str_tcl = '{}system SparseSYM\n'.format(pinfo.indent)
	
	elif system == 'Diagonal':
		str_tcl = '{}system Diagonal\n'.format(pinfo.indent)
	
	elif system == 'MPIDiagonal':
		str_tcl = '{}system MPIDiagonal\n'.format(pinfo.indent)
	
	elif system == 'Mumps':
		ICNTL14_at = xobj.getAttribute('-ICNTL14')
		if(ICNTL14_at is None):
			raise Exception('Error: cannot find "-ICNTL14" attribute')
		if ICNTL14_at.boolean:
			ICNTL14_LVALUE_at = xobj.getAttribute('ICNTL14 Value')
			if(ICNTL14_LVALUE_at is None):
				raise Exception('Error: cannot find "ICNTL14 Value" attribute')
			ICNTL14_VALUE = ICNTL14_LVALUE_at.integer
			sopt_1 += ' -ICNTL14 {}'.format(ICNTL14_VALUE)
		
		matrixType_at = xobj.getAttribute('-matrixType')
		if(matrixType_at is None):
			raise Exception('Error: cannot find "-matrixType" attribute')
		if matrixType_at.boolean:
			matrixType_value_at = xobj.getAttribute('matrixType')
			if(matrixType_value_at is None):
				raise Exception('Error: cannot find "matrixType" attribute')
			matrixType_value = 0
			if matrixType_value_at.string == 'Symmetric Positive Definite':
				matrixType_value = 1
			elif matrixType_value_at.string == 'Symmetric General':
				matrixType_value = 2
			sopt_1 += ' -matrixType {}'.format(matrixType_value)
		
		str_tcl = '{}system Mumps{}\n'.format(pinfo.indent, sopt_1)
		
	elif system == 'Cusp':
		RTOL_at = xobj.getAttribute('RTOL')
		if(RTOL_at is None):
			raise Exception('Error: cannot find "RTOL" attribute')
		RTOL = RTOL_at.real
		
		MINT_at = xobj.getAttribute('MINT')
		if(MINT_at is None):
			raise Exception('Error: cannot find "MINT" attribute')
		MINT = MINT_at.integer
		
		PRE_at = xobj.getAttribute('PRE')
		if(PRE_at is None):
			raise Exception('Error: cannot find "PRE" attribute')
		PRE = PRE_at.string
		
		SOLVER_at = xobj.getAttribute('SOLVER')
		if(SOLVER_at is None):
			raise Exception('Error: cannot find "SOLVER" attribute')
		SOLVER = SOLVER_at.string
		
		str_tcl = '{}system CuSP -rTol {} -mInt {} -pre {} -solver {}\n'.format(
					pinfo.indent, RTOL, MINT, PRE, SOLVER)
		
	elif system == 'ParallelProfileSPD':
		str_tcl = '{}system ParallelProfileSPD\n'.format(pinfo.indent)
	
	if pinfo.process_count > 1 and (system != 'Mumps' and system != 'ParallelProfileSPD') :
		IO.write_cerr('Warning : partitioned model, "system" (in AnalysesCommand) different from "Mumps" or "ParallelProfileSPD" attribute, there may be some problems\n')
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)