from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	'''
	eigen <$solver> $numEigenvalues
	'''
	
	# use_solver
	at_use_solver = MpcAttributeMetaData()
	at_use_solver.type = MpcAttributeType.Boolean
	at_use_solver.name = 'use_solver'
	at_use_solver.group = 'eigen'
	at_use_solver.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_solver')+'<br/>') +
		html_par('optional string detailing type of solver') +
		html_par(html_href("https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/eigen.html",'Eigen Command')+'<br/>') +
		html_end()
		)
	
	# solver
	at_solver = MpcAttributeMetaData()
	at_solver.type = MpcAttributeType.String
	at_solver.name = 'solver'
	at_solver.group = 'eigen'
	at_solver.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('solver')+'<br/>') +
		html_par('optional string detailing type of solver') +
		html_par(html_href("https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/eigen.html",'Eigen Command')+'<br/>') +
		html_end()
		)
	at_solver.sourceType = MpcAttributeSourceType.List
	at_solver.setSourceList(['-frequency', '-standard', '-findLargest', '-genBandArpack', '-symmBandLapack', '-fullGenLapack'])
	at_solver.setDefault('-genBandArpack')
	
	# numEigenvalues
	at_numEigenvalues = MpcAttributeMetaData()
	at_numEigenvalues.type = MpcAttributeType.Integer
	at_numEigenvalues.name = 'numEigenvalues'
	at_numEigenvalues.group = 'eigen'
	at_numEigenvalues.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numEigenvalues')+'<br/>') +
		html_par('number of eigenvalues required') +
		html_par(html_href("https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/eigen.html",'Eigen Command')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'eigen'
	xom.addAttribute(at_use_solver)
	xom.addAttribute(at_solver)
	xom.addAttribute(at_numEigenvalues)
	
	
	# visibility dependencies
	# solver-dep
	xom.setVisibilityDependency(at_use_solver, at_solver)
	
	return xom

def writeTcl(pinfo):
	
	# eigen <$solver> $numEigenvalues
	
	xobj = pinfo.analysis_step.XObject
	
	sopt = ''
	
	use_solver_at = xobj.getAttribute('use_solver')
	if(use_solver_at is None):
		raise Exception('Error: cannot find "use_solver" attribute')
	if use_solver_at.boolean:
		solver_at = xobj.getAttribute('solver')
		if(solver_at is None):
			raise Exception('Error: cannot find "solver" attribute')
		solver = solver_at.string
		
		sopt += ' {}'.format(solver)
	
	numEigenvalues_at = xobj.getAttribute('numEigenvalues')
	if(numEigenvalues_at is None):
		raise Exception('Error: cannot find "numEigenvalues" attribute')
	numEigenvalues = numEigenvalues_at.integer
	
	
	str_tcl = '{}eigen{} {}\n'.format(pinfo.indent, sopt, numEigenvalues)
	
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)