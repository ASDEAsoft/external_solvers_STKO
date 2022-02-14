import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import PyMpc
import PyMpc.Math
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Function
	at_Function = MpcAttributeMetaData()
	at_Function.type = MpcAttributeType.String
	at_Function.name = '__mpc_function__'
	at_Function.group = 'Group'
	at_Function.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Function')+'<br/>') + 
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_Function.editable = False
	
	# choice
	at_choice = MpcAttributeMetaData()
	at_choice.type = MpcAttributeType.String
	at_choice.name = 'choice'
	at_choice.group = 'Group'
	at_choice.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('choice')+'<br/>') + 
		html_par('time interval between specified points.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	at_choice.sourceType = MpcAttributeSourceType.List
	at_choice.setSourceList(['constant', 'non_constant'])
	at_choice.setDefault('constant')
	
	# constant
	at_constant = MpcAttributeMetaData()
	at_constant.type = MpcAttributeType.Boolean
	at_constant.name = 'constant'
	at_constant.group = 'Group'
	at_constant.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('constant')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	at_constant.editable = False
	
	# non_constant
	at_non_constant = MpcAttributeMetaData()
	at_non_constant.type = MpcAttributeType.Boolean
	at_non_constant.name = 'non_constant'
	at_non_constant.group = 'Group'
	at_non_constant.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('non_constant')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	at_non_constant.editable = False
	
	# list_of_values
	at_list_of_values = MpcAttributeMetaData()
	at_list_of_values.type = MpcAttributeType.QuantityVector
	at_list_of_values.name = 'list_of_values'
	at_list_of_values.group = '-values'
	at_list_of_values.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('list_of_values')+'<br/>') + 
		html_par('file containing the load factors values') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	#at_list_of_values.setDefault([0, 1])
	
	# list_of_times
	at_list_of_times = MpcAttributeMetaData()
	at_list_of_times.type = MpcAttributeType.QuantityVector
	at_list_of_times.name = 'list_of_times'
	at_list_of_times.group = '-time'
	at_list_of_times.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('list_of_times')+'<br/>') + 
		html_par('file containing the time values for corresponding load factors') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	#at_list_of_times.setDefault([0, 1])
	
	# dt
	at_dt = MpcAttributeMetaData()
	at_dt.type = MpcAttributeType.Real
	at_dt.name = 'dt'
	at_dt.group = '-dt'
	at_dt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dt')+'<br/>') + 
		html_par('time interval between specified points.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	
	# factor
	at_factor = MpcAttributeMetaData()
	at_factor.type = MpcAttributeType.Boolean
	at_factor.name = '-factor'
	at_factor.group = 'Group'
	at_factor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-factor')+'<br/>') + 
		html_par('optional, a factor to multiply load factors by (default = 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	
	# cFactor
	at_cFactor = MpcAttributeMetaData()
	at_cFactor.type = MpcAttributeType.Real
	at_cFactor.name = 'cFactor'
	at_cFactor.group = '-factor'
	at_cFactor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cFactor')+'<br/>') + 
		html_par('optional, a factor to multiply load factors by (default = 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	at_cFactor.setDefault(1.0)
	
	# -startTime
	at_startTime = MpcAttributeMetaData()
	at_startTime.type = MpcAttributeType.Boolean
	at_startTime.name = '-startTime'
	at_startTime.group = 'Group'
	at_startTime.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-startTime')+'<br/>') + 
		html_par('optional, to provide a start time for provided load factors (default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	
	# tStart
	at_tStart = MpcAttributeMetaData()
	at_tStart.type = MpcAttributeType.Real
	at_tStart.name = 'tStart'
	at_tStart.group = '-startTime'
	at_tStart.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tStart')+'<br/>') + 
		html_par('optional, to provide a start time for provided load factors (default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Path_TimeSeries','Path TimeSeries')+'<br/>') +
		html_end()
		)
	at_tStart.setDefault(0.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Path'
	xom.addAttribute(at_Function)
	xom.addAttribute(at_choice)
	xom.addAttribute(at_constant)
	xom.addAttribute(at_non_constant)
	xom.addAttribute(at_list_of_values)
	xom.addAttribute(at_list_of_times)
	xom.addAttribute(at_dt)
	xom.addAttribute(at_factor)
	xom.addAttribute(at_cFactor)
	xom.addAttribute(at_startTime)
	xom.addAttribute(at_tStart)
	
	
	# list_of_times-dep
	xom.setVisibilityDependency(at_non_constant, at_list_of_times)
	
	# dt-dep
	xom.setVisibilityDependency(at_constant, at_dt)
	
	# cFactor-dep
	xom.setVisibilityDependency(at_factor, at_cFactor)
	
	# startTime-dep
	xom.setVisibilityDependency(at_constant, at_startTime)
	
	# tStart-dep
	xom.setVisibilityDependency(at_startTime, at_tStart)
	xom.setVisibilityDependency(at_constant, at_tStart)
	
	
	# auto-exclusive dependencies
	# constant or non_constant
	xom.setBooleanAutoExclusiveDependency(at_choice, at_constant)
	xom.setBooleanAutoExclusiveDependency(at_choice, at_non_constant)
	
	return xom

def evaluateFunctionAttribute(xobj):
	if(xobj is None):
		print('Error: xobj is null\n')
		return PyMpc.Math.mat()
	
	if(xobj.name != 'Path'):
		print('Error: invalid xobj type, expected "Path", given "{}"'.format(xobj.name))
		return PyMpc.Math.mat()
	
	func_at = xobj.getAttribute('__mpc_function__')
	if(func_at is None):
		print('Error: cannot find "__mpc_function__" attribute\n')
		return PyMpc.Math.mat()
	
	choice_at = xobj.getAttribute('choice')
	if(choice_at is None):
		print('Error: cannot find "choice" attribute\n')
		return PyMpc.Math.mat()
	
	constant_at = xobj.getAttribute('constant')
	if(constant_at is None):
		print('Error: cannot find "constant" attribute\n')
		return PyMpc.Math.mat()
	
	non_constant_at = xobj.getAttribute('non_constant')
	if(non_constant_at is None):
		print('Error: cannot find "non_constant" attribute\n')
		return PyMpc.Math.mat()
	
	list_of_values_at = xobj.getAttribute('list_of_values')
	if(list_of_values_at is None):
		print('Error: cannot find "list_of_values" attribute\n')
		return PyMpc.Math.mat()
	
	list_of_times_at = xobj.getAttribute('list_of_times')
	if(list_of_times_at is None):
		print('Error: cannot find "list_of_times" attribute\n')
		return PyMpc.Math.mat()
	
	dt_at = xobj.getAttribute('dt')
	if(dt_at is None):
		print('Error: cannot find "dt" attribute\n')
		return PyMpc.Math.mat()
	
	fact_at = xobj.getAttribute('-factor')
	if(fact_at is None):
		print('Error: cannot find "-factor" attribute\n')
		return PyMpc.Math.mat()
	
	cFactor_at = xobj.getAttribute('cFactor')
	if(cFactor_at is None):
		print('Error: cannot find "cFactor" attribute\n')
		return PyMpc.Math.mat()
	
	startTime_at = xobj.getAttribute('-startTime')
	if(startTime_at is None):
		print('Error: cannot find "-startTime" attribute\n')
		return PyMpc.Math.mat()
	
	tStart_at = xobj.getAttribute('tStart')
	if(tStart_at is None):
		print('Error: cannot find "tStart" attribute\n')
		return PyMpc.Math.mat()
	
	constant = constant_at.boolean
	non_constant = non_constant_at.boolean
	listValue = list_of_values_at.quantityVector
	listTime = list_of_times_at.quantityVector
	cFactor = cFactor_at.real
	
	xy = PyMpc.Math.mat(len(listValue), 2)
	
	if(non_constant == True):
		if(len(listValue)!=len(listTime)):
			raise Exception('Different length of vectors')
		for i in range(len(listValue)):
			xy[i, 0] = listTime.valueAt(i)
			xy[i, 1] = listValue.valueAt(i)
	else:
		ix = 0.0
		if startTime_at.boolean:
			ix = tStart_at.real
		dt = dt_at.real
		for i in range(len(listValue)):
			xy[i, 0] = ix
			xy[i, 1] = listValue.valueAt(i)
			ix += dt
	
	return xy

def writeTcl(pinfo):
	
	xobj = pinfo.definition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	sopt = ''	#optional string
	
	#with both 'constant' and 'non_constant'
	fact_at = xobj.getAttribute('-factor')
	if(fact_at is None):
		print('Error: cannot find "-factor" attribute\n')
		return PyMpc.Math.mat()
	fact = fact_at.boolean
	if fact:
		cFactor_at = xobj.getAttribute('cFactor')
		if(cFactor_at is None):
			raise Exception('Error: cannot find "cFactor" attribute')
		cFactor = cFactor_at.real
		sopt += ' -factor {}'.format(cFactor)
	
	
	constant_at = xobj.getAttribute('constant')
	if(constant_at is None):
		raise Exception('Error: cannot find "constant" attribute')
	constant = constant_at.boolean
	if constant:
		# with 'constant'
		#timeSeries Path $tag -dt $dt -values {list_of_values} <-factor $cFactor> <-useLast> <-prependZero> <-startTime $tStart>
		
		dt_at = xobj.getAttribute('dt')
		if(dt_at is None):
			raise Exception('Error: cannot find "dt" attribute')
		dt = dt_at.real
		
		list_of_values_at = xobj.getAttribute('list_of_values')
		if(list_of_values_at is None):
			raise Exception('Error: cannot find "list_of_values" attribute')
		listValues = list_of_values_at.quantityVector
		
		#set list TCL
		values_str = 'set timeSeries_list_of_values_{}'.format(tag)+' {'
		
		nLetters=len(values_str)
		nTab=nLetters//4
		
		n = 1
		for i in range(len(listValues)):
			if (i == (10*n)):
				values_str += '\\\n{}{}'.format(pinfo.indent, tclin.utils.nIndent(nTab))
				n += 1
			if (i!=len(listValues)-1):
				values_str += '{} '.format(listValues.valueAt(i))
			else:
				values_str += '{}'.format(listValues.valueAt(i))
		
		values_str += '}\n'
		pinfo.out_file.write(values_str)
		#end list TCL
		
		#optional paramters with 'constant'
		startTime_at = xobj.getAttribute('-startTime')
		if(startTime_at is None):
			raise Exception('Error: cannot find "-startTime" attribute')
		startTime = startTime_at.boolean
		if startTime:
			tStart_at = xobj.getAttribute('tStart')
			if(tStart_at is None):
				raise Exception('Error: cannot find "tStart" attribute')
			tStart = tStart_at.real
			sopt += ' -startTime {}'.format(tStart)
		
		#now write the 'constant' string into the file
		str_tcl = '{0}timeSeries Path {1} -dt {2} -values $timeSeries_list_of_values_{1} {3}\n'.format(pinfo.indent, tag, dt, sopt)
	
	else:
		#with 'non_constant'
		#timeSeries Path $tag -time {list_of_times} -values {list_of_values} <-factor $cFactor> <-useLast>
		
		list_of_times_at = xobj.getAttribute('list_of_times')
		if(list_of_times_at is None):
			raise Exception('Error: cannot find "list_of_times" attribute')
		listTimes = list_of_times_at.quantityVector
		
		list_of_values_at = xobj.getAttribute('list_of_values')
		if(list_of_values_at is None):
			raise Exception('Error: cannot find "list_of_values" attribute')
		listValues = list_of_values_at.quantityVector
		
		
		#set list TCL
		times_str = 'set timeSeries_list_of_times_{}'.format(tag)+' {'
		values_str = 'set timeSeries_list_of_values_{}'.format(tag)+' {'
		
		nLettersT = len(times_str)
		nLettersV = len(values_str)
		nTabT = nLettersT // 4
		nTabV = nLettersV // 4
		
		n = 1
		for i in range(len(listTimes)):
			if (i == (10*n)):
				times_str += '\\\n{}{}'.format(pinfo.indent, tclin.utils.nIndent(nTabT))
				values_str += '\\\n{}{}'.format(pinfo.indent, tclin.utils.nIndent(nTabV))
				n += 1
			if (i!=len(listTimes)-1):
				times_str += '{} '.format(listTimes.valueAt(i))
				values_str += '{} '.format(listValues.valueAt(i))
			else:
				times_str += '{}'.format(listTimes.valueAt(i))
				values_str += '{}'.format(listValues.valueAt(i))
		
		times_str += '}\n'
		values_str += '}\n'
		pinfo.out_file.write(times_str)
		pinfo.out_file.write(values_str)
		
		#end list TCL
		#now write the 'non_constant' string into the file
		str_tcl = '{0}timeSeries Path {1} -time $timeSeries_list_of_times_{1} -values $timeSeries_list_of_values_{1}{2}\n'.format(pinfo.indent, tag, sopt)
	
	pinfo.out_file.write(str_tcl)