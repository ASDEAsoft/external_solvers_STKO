from PyMpc import *
from mpc_utils_html import *

def analyzeCommand(xom):
	
	'''
	analyze $numIncr <$dt> <$dtMin $dtMax $Jd>
	'''
	
	# use_adapt
	at_time_step_type = MpcAttributeMetaData()
	at_time_step_type.type = MpcAttributeType.String
	at_time_step_type.name = 'Time Step Type'
	at_time_step_type.group = 'analyze'
	at_time_step_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Time Step Type')+'<br/>')+ 
		html_par('Choose how to increment the time step. It can be either Fixed or Adaptive. The Adaptive Time Step will try to adapt the time step size based on the convergence properties of the problem.') +
		html_end()
		)
	at_time_step_type.sourceType = MpcAttributeSourceType.List
	at_time_step_type.setSourceList(['Adaptive Time Step','Fixed Time Step'])
	at_time_step_type.setDefault('Fixed Time Step')
	
	# booleanAdaptive
	at_adaptive = MpcAttributeMetaData()
	at_adaptive.type = MpcAttributeType.Boolean
	at_adaptive.name = 'Adaptive Time Step'
	at_adaptive.group = 'integrator'
	at_adaptive.editable = False
	
	# booleanAdaptive
	at_fixed = MpcAttributeMetaData()
	at_fixed.type = MpcAttributeType.Boolean
	at_fixed.name = 'Fixed Time Step'
	at_fixed.group = 'integrator'
	at_fixed.editable = False
		
	# numIncr
	at_numIncr = MpcAttributeMetaData()
	at_numIncr.type = MpcAttributeType.Integer
	at_numIncr.name = 'numIncr'
	at_numIncr.group = 'analyze'
	at_numIncr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIncr')+'<br/>') +
		html_par('number of analysis steps to perform') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Analyze_Command','Analyze Command')+'<br/>') +
		html_end()
		)
	at_numIncr.setDefault(10)
	
	# duration
	at_duration_tr = MpcAttributeMetaData()
	at_duration_tr.type = MpcAttributeType.Real
	at_duration_tr.name = 'duration/transient'
	at_duration_tr.group = 'analyze'
	at_duration_tr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('duration')+'<br/>')+ 
		html_par('The total duration of the transient analysis.') +
		html_end()
		)
	
	# dt Transient
	at_dt_Transient = MpcAttributeMetaData()
	at_dt_Transient.type = MpcAttributeType.Real
	at_dt_Transient.name = 'dt Transient'
	at_dt_Transient.group = 'analyze'
	at_dt_Transient.editable = False # for upgrading
	
	at_max_factor = MpcAttributeMetaData()
	at_max_factor.type = MpcAttributeType.Real
	at_max_factor.name = 'max factor'
	at_max_factor.group = 'AdaptiveControl'
	at_max_factor.setDefault(1.0)
	at_max_factor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('max factor')+'<br/>')+ 
		html_par('Given that:<br/>- dT(adaptive) = factor * dT(initial)<br/>then:<br/>- factor &lt;= max_factor') +
		html_end()
		)
	
	at_min_factor = MpcAttributeMetaData()
	at_min_factor.type = MpcAttributeType.Real
	at_min_factor.name = 'min factor'
	at_min_factor.group = 'AdaptiveControl'
	at_min_factor.setDefault(1.0E-6)
	at_min_factor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('min factor')+'<br/>')+ 
		html_par('Given that:<br/>- dT(adaptive) = factor * dT(initial)<br/>then:<br/>- factor &gt;= min_factor') +
		html_end()
		)
	
	at_max_factor_incr = MpcAttributeMetaData()
	at_max_factor_incr.type = MpcAttributeType.Real
	at_max_factor_incr.name = 'max factor incr'
	at_max_factor_incr.group = 'AdaptiveControl'
	at_max_factor_incr.setDefault(1.5)
	at_max_factor_incr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('max factor incr')+'<br/>')+ 
		html_par('Given that:- dT(adaptive) = factor * dT(initial)<br/>- factor = factor(old)*factor_increment<br/>- factor_increment = desired_iter/num_iter<br/>then:<br/>- factor_increment &lt;= max_factor_incr') +
		html_end()
		)
	
	at_min_factor_incr = MpcAttributeMetaData()
	at_min_factor_incr.type = MpcAttributeType.Real
	at_min_factor_incr.name = 'min factor incr'
	at_min_factor_incr.group = 'AdaptiveControl'
	at_min_factor_incr.setDefault(0.0)
	at_min_factor_incr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('max factor incr')+'<br/>')+ 
		html_par('Given that:- dT(adaptive) = factor * dT(initial)<br/>- factor = factor(old)*factor_increment<br/>- factor_increment = desired_iter/num_iter<br/>then:<br/>- factor_increment &gt;= min_factor_incr') +
		html_end()
		)
	
	xom.addAttribute(at_time_step_type)
	xom.addAttribute(at_adaptive)
	xom.addAttribute(at_fixed)
	xom.addAttribute(at_numIncr)
	xom.addAttribute(at_dt_Transient)
	xom.addAttribute(at_duration_tr)
	xom.addAttribute(at_max_factor)
	xom.addAttribute(at_min_factor)
	xom.addAttribute(at_max_factor_incr)
	xom.addAttribute(at_min_factor_incr)
	
	xom.setBooleanAutoExclusiveDependency(at_time_step_type, at_adaptive)
	xom.setVisibilityDependency(at_adaptive, at_max_factor)
	xom.setVisibilityDependency(at_adaptive, at_min_factor)
	xom.setVisibilityDependency(at_adaptive, at_max_factor_incr)
	xom.setVisibilityDependency(at_adaptive, at_min_factor_incr)


def writeTcl_analyze(pinfo, xobj):
	
	# analyze $numIncr <$dt> <$dtMin $dtMax $Jd>
	
	sopt = ''
	
	numIncr_at = xobj.getAttribute('numIncr')
	if(numIncr_at is None):
		raise Exception('Error: cannot find "numIncr" attribute')
	numIncr = numIncr_at.integer
	
	use_duration_at = xobj.getAttribute('Transient')
	if(use_duration_at is None):
		raise Exception('Error: cannot find "Transient" attribute')
	if use_duration_at.boolean:
		duration_at = xobj.getAttribute('duration/transient')
		if(duration_at is None):
			raise Exception('Error: cannot find "dt Transient" attribute')
		duration = duration_at.real
		sopt += ' {}'.format(duration)
	
	str_tcl = '{}analyze {}{}\n'.format(pinfo.indent, numIncr, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)