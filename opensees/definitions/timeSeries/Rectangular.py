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
	
	# tStart
	at_tStart = MpcAttributeMetaData()
	at_tStart.type = MpcAttributeType.Real
	at_tStart.name = 'tStart'
	at_tStart.group = 'Group'
	at_tStart.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tStart')+'<br/>') + 
		html_par('starting time of non-zero load factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Rectangular_TimeSeries','Rectangular TimeSeries')+'<br/>') +
		html_end()
		)
	at_tStart.setDefault(0.0)
	
	# tEnd
	at_tEnd = MpcAttributeMetaData()
	at_tEnd.type = MpcAttributeType.Real
	at_tEnd.name = 'tEnd'
	at_tEnd.group = 'Group'
	at_tEnd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tEnd')+'<br/>') + 
		html_par('ending time of non-zero load factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Rectangular_TimeSeries','Rectangular TimeSeries')+'<br/>') +
		html_end()
		)
	at_tEnd.setDefault(1.0)
	
	# factor
	at_factor = MpcAttributeMetaData()
	at_factor.type = MpcAttributeType.Boolean
	at_factor.name = '-factor'
	at_factor.group = 'Group'
	at_factor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-factor')+'<br/>') + 
		html_par('the load factor applied (optional, default=1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Rectangular_TimeSeries','Rectangular TimeSeries')+'<br/>') +
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
		html_par('the load factor applied (optional, default=1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Rectangular_TimeSeries','Rectangular TimeSeries')+'<br/>') +
		html_end()
		)
	at_cFactor.setDefault(1.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Rectangular'
	xom.addAttribute(at_Function)
	xom.addAttribute(at_tStart)
	xom.addAttribute(at_tEnd)
	xom.addAttribute(at_factor)
	xom.addAttribute(at_cFactor)
	
	
	# cFactor-dep
	xom.setVisibilityDependency(at_factor, at_cFactor)
	
	return xom

def evaluateFunctionAttribute(xobj):
	if(xobj is None):
		print('Error: xobj is null\n')
		return PyMpc.Math.mat()
	
	if(xobj.name != 'Rectangular'):
		print('Error: invalid xobj type, expected "Rectangular", given "{}"'.format(xobj.name))
		return PyMpc.Math.mat()
	
	func_at = xobj.getAttribute('__mpc_function__')
	if(func_at is None):
		print('Error: cannot find "__mpc_function__" attribute\n')
		return PyMpc.Math.mat()
	
	tStart_at = xobj.getAttribute('tStart')
	if(tStart_at is None):
		print('Error: cannot find "tStart" attribute\n')
		return PyMpc.Math.mat()
	
	tEnd_at = xobj.getAttribute('tEnd')
	if(tEnd_at is None):
		print('Error: cannot find "tEnd" attribute\n')
		return PyMpc.Math.mat()
	
	fact_at = xobj.getAttribute('-factor')
	if(fact_at is None):
		print('Error: cannot find "-factor" attribute\n')
		return PyMpc.Math.mat()
	
	cFactor_at = xobj.getAttribute('cFactor')
	if(cFactor_at is None):
		print('Error: cannot find "cFactor" attribute\n')
		return PyMpc.Math.mat()
	
	tStart = tStart_at.real
	tEnd = tEnd_at.real
	cFactor = cFactor_at.real
	Dt = tEnd-tStart
	
	if(tStart>=tEnd):
		raise Exception('Invalid domain (tStart >= tEnd)')
	
	xy = PyMpc.Math.mat(6, 2)
	xy[0, 0] = tStart-Dt/10
	xy[0, 1] = 0
	xy[1, 0] = tStart
	xy[1, 1] = 0
	xy[2, 0] = tStart
	xy[2, 1] = cFactor
	xy[3, 0] = tEnd
	xy[3, 1] = cFactor
	xy[4, 0] = tEnd
	xy[4, 1] = 0
	xy[5, 0] = tEnd+Dt/10
	xy[5, 1] = 0
	return xy

def writeTcl(pinfo):
	
	#timeSeries Rectangular $tag $tStart $tEnd <-factor $cFactor>
	xobj = pinfo.definition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	tStart_at = xobj.getAttribute('tStart')
	if(tStart_at is None):
		raise Exception('Error: cannot find "tStart" attribute')
	tStart = tStart_at.real
	
	tEnd_at = xobj.getAttribute('tEnd')
	if(tEnd_at is None):
		raise Exception('Error: cannot find "tEnd" attribute')
	tEnd = tEnd_at.real
	
	
	# optional paramters
	sopt = ''
	
	fact_at = xobj.getAttribute('-factor')
	if(fact_at is None):
		raise Exception('Error: cannot find "-factor" attribute')
	fact = fact_at.boolean
	if fact:
		cFactor_at = xobj.getAttribute('cFactor')
		if(cFactor_at is None):
			raise Exception('Error: cannot find "cFactor" attribute')
		cFactor = cFactor_at.real
		sopt += ' -factor {}'.format(cFactor)
	
	str_tcl = '{}timeSeries Rectangular {} {} {}{}\n'.format(pinfo.indent, tag, tStart, tEnd, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)