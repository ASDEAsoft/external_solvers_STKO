import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	''' --------------------------------------------- ↓ Extra Data for ImposedMotion ↓ ----------------------------------------------- '''
	
	# constraintsCommand
	at_direction = MpcAttributeMetaData()
	at_direction.type = MpcAttributeType.String
	at_direction.name = 'direction'
	at_direction.group = 'direction'
	at_direction.description = (
		html_par(html_begin()) +
		html_par('direction in which ground motion acts:') +
		html_par('corresponds to translation/rotation along the global axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	at_direction.sourceType = MpcAttributeSourceType.List
	at_direction.setSourceList(['dx', 'dy', 'dz', 'Rx', 'Ry', 'Rz'])
	at_direction.setDefault('dx')
	
	''' --------------------------------------------- ↑ Extra Data for ImposedMotion ↑ ----------------------------------------------- '''
	
	# -vel0
	at_use_vel0 = MpcAttributeMetaData()
	at_use_vel0.type = MpcAttributeType.Boolean
	at_use_vel0.name = '-vel0'
	at_use_vel0.group = 'Group'
	at_use_vel0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-vel0')+'<br/>') +
		html_par('the initial velocity (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	
	# vel0
	at_vel0 = MpcAttributeMetaData()
	at_vel0.type = MpcAttributeType.QuantityScalar
	at_vel0.name = 'vel0'
	at_vel0.group = '-vel0'
	at_vel0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vel0')+'<br/>') +
		html_par('the initial velocity (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	at_vel0.setDefault(0.0)
	at_vel0.dimension = u.L/u.t
	
	# -fact
	at_fact = MpcAttributeMetaData()
	at_fact.type = MpcAttributeType.Boolean
	at_fact.name = '-fact'
	at_fact.group = 'Group'
	at_fact.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fact')+'<br/>') +
		html_par('constant factor (optional, default=1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	
	# cFactor
	at_cFactor = MpcAttributeMetaData()
	at_cFactor.type = MpcAttributeType.Real
	at_cFactor.name = 'cFactor'
	at_cFactor.group = '-fact'
	at_cFactor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cFactor')+'<br/>') +
		html_par('constant factor (optional, default=1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	at_cFactor.setDefault(1.0)
	
	# -accel
	# at_accel = MpcAttributeMetaData()
	# at_accel.type = MpcAttributeType.Boolean
	# at_accel.name = '-accel'
	# at_accel.group = 'Group'
	# at_accel.description = (
		# html_par(html_begin()) +
		# html_par(html_boldtext('-accel')+'<br/>') +
		# html_par('acceleration') +
		# html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		# html_end()
		# )
	
	# tsTag
	at_tsTag = MpcAttributeMetaData()
	at_tsTag.type = MpcAttributeType.Index
	at_tsTag.name = 'tsTag'
	at_tsTag.group = '-accel'
	at_tsTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tsTag')+'<br/>') +
		html_par('tag of the TimeSeries series defining the acceleration history.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	at_tsTag.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_tsTag.indexSource.addAllowedNamespace("timeSeries")
	
	# -vel
	at_use_vel = MpcAttributeMetaData()
	at_use_vel.type = MpcAttributeType.Boolean
	at_use_vel.name = '-vel'
	at_use_vel.group = 'Group'
	at_use_vel.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-vel')+'<br/>') +
		html_par('velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	
	# vel
	at_vel = MpcAttributeMetaData()
	at_vel.type = MpcAttributeType.QuantityScalar
	at_vel.name = 'vel'
	at_vel.group = '-vel'
	at_vel.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vel')+'<br/>') +
		html_par('velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	at_vel.dimension = u.L/u.t
	
	# -disp
	at_use_disp = MpcAttributeMetaData()
	at_use_disp.type = MpcAttributeType.Boolean
	at_use_disp.name = '-disp'
	at_use_disp.group = 'Group'
	at_use_disp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-disp')+'<br/>') +
		html_par('displacement') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	
	# disp
	at_disp = MpcAttributeMetaData()
	at_disp.type = MpcAttributeType.QuantityScalar
	at_disp.name = 'disp'
	at_disp.group = '-disp'
	at_disp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('disp')+'<br/>') +
		html_par('displacement') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	at_disp.dimension = u.L
	
	# -int
	at_use_int = MpcAttributeMetaData()
	at_use_int.type = MpcAttributeType.Boolean
	at_use_int.name = '-int'
	at_use_int.group = 'Group'
	at_use_int.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-int')+'<br/>') +
		html_par('integrator') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	
	# int
	at_int = MpcAttributeMetaData()
	at_int.type = MpcAttributeType.String
	at_int.name = 'int'
	at_int.group = '-int'
	at_int.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('int')+'<br/>') +
		html_par('integrator') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	at_int.sourceType = MpcAttributeSourceType.List
	at_int.setSourceList(['Trapezoidal', 'Simpson'])
	at_int.setDefault('Trapezoidal')
	
	# ctype
	at_ctype = MpcAttributeMetaData()
	at_ctype.type = MpcAttributeType.Integer
	at_ctype.editable = False;
	at_ctype.name = 'ctype_constraint'
	at_ctype.group = 'Group'
	at_ctype.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ctype')+'<br/>') + 
		html_par('ctype') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniform_Excitation_Pattern','Uniform Excitation Pattern')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'UniformExcitation'
	xom.addAttribute(at_direction)
	xom.addAttribute(at_use_vel0)
	xom.addAttribute(at_vel0)
	xom.addAttribute(at_fact)
	xom.addAttribute(at_cFactor)
	# xom.addAttribute(at_accel)
	xom.addAttribute(at_tsTag)
	xom.addAttribute(at_use_vel)
	xom.addAttribute(at_vel)
	xom.addAttribute(at_use_disp)
	xom.addAttribute(at_disp)
	xom.addAttribute(at_use_int)
	xom.addAttribute(at_int)
	xom.addAttribute(at_ctype)
	
	
	# vel0-dep
	xom.setVisibilityDependency(at_use_vel0, at_vel0)
	
	# cFactor-dep
	xom.setVisibilityDependency(at_fact, at_cFactor)
	
	# accel-dep
	# xom.setVisibilityDependency(at_accel, at_tsTag)
	
	# vel-dep
	xom.setVisibilityDependency(at_use_vel, at_vel)
	
	# disp-dep
	xom.setVisibilityDependency(at_use_disp, at_disp)
	
	# int-dep
	xom.setVisibilityDependency(at_use_int, at_int)
	
	
	return xom

def writeTcl(pinfo):
	
	#pattern UniformExcitation $patternTag $dir -accel $tsTag <-vel0 $vel0> <-fact $cFactor>
	xobj = pinfo.analysis_step.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	
	tsTag_at = xobj.getAttribute('tsTag')
	if(tsTag_at is None):
		raise Exception('Error: cannot find "tsTag" attribute')
	tsTag = tsTag_at.index
	
	# optional paramters
	sopt = ''
	
	use_vel0_at = xobj.getAttribute('-vel0')
	if(use_vel0_at is None):
		raise Exception('Error: cannot find "-vel0" attribute')
	use_vel0 = use_vel0_at.boolean
	if use_vel0:
		vel0_at = xobj.getAttribute('vel0')
		if(vel0_at is None):
			raise Exception('Error: cannot find "vel0" attribute')
		vel0 = vel0_at.quantityScalar.value
		
		sopt += ' -vel0 {}'.format(vel0)
	
	
	fact_at = xobj.getAttribute('-fact')
	if(fact_at is None):
		raise Exception('Error: cannot find "-fact" attribute')
	fact = fact_at.boolean
	if fact:
		cFactor_at = xobj.getAttribute('cFactor')
		if(cFactor_at is None):
			raise Exception('Error: cannot find "cFactor" attribute')
		cFactor = cFactor_at.real
		
		sopt += ' -fact {}'.format(cFactor)
	
	
	use_vel_at = xobj.getAttribute('-vel')
	if(use_vel_at is None):
		raise Exception('Error: cannot find "-vel" attribute')
	use_vel = use_vel_at.boolean
	if use_vel:
		vel_at = xobj.getAttribute('vel')
		if(vel_at is None):
			raise Exception('Error: cannot find "vel" attribute')
		vel = vel_at.quantityScalar.value
		
		sopt += ' -vel {}'.format(vel)
	
	
	use_disp_at = xobj.getAttribute('-disp')
	if(use_disp_at is None):
		raise Exception('Error: cannot find "-disp" attribute')
	use_disp = use_disp_at.boolean
	if use_disp:
		disp_at = xobj.getAttribute('disp')
		if(disp_at is None):
			raise Exception('Error: cannot find "disp" attribute')
		disp = disp_at.quantityScalar.value
		
		sopt += ' -disp {}'.format(disp)
	
	
	use_int_at = xobj.getAttribute('-int')
	if(use_int_at is None):
		raise Exception('Error: cannot find "-int" attribute')
	use_int = use_int_at.boolean
	if use_int:
		int_at = xobj.getAttribute('int')
		if(int_at is None):
			raise Exception('Error: cannot find "int" attribute')
		int = int_at.string
		
		sopt += ' -int {}'.format(int)
	
	direction_at = xobj.getAttribute('direction')
	if(direction_at is None):
		raise Exception('Error: cannot find "direction" attribute')
	direction = direction_at.string
	
	dir = ''
	if direction == 'dx':
		dir = '1'
	
	if direction == 'dy':
		dir = '2'
	
	if direction == 'dz':
		dir = '3'
	
	if direction == 'Rx':
		dir = '4'
		
	if direction == 'Ry':
		dir = '5'
		
	if direction == 'Rz':
		dir = '6'
	
	pinfo.out_file.write('{}pattern UniformExcitation {} {} -accel {}{}\n'.format(pinfo.indent, tag, dir, tsTag, sopt))
