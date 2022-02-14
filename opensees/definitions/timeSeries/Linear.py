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
	
	# factor
	at_factor = MpcAttributeMetaData()
	at_factor.type = MpcAttributeType.Boolean
	at_factor.name = '-factor'
	at_factor.group = 'Group'
	at_factor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-factor')+'<br/>') + 
		html_par('the linear factor (optional, default=1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Linear_TimeSeries','Constant TimeSeries')+'<br/>') +
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
		html_par('the linear factor (optional, default=1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Linear_TimeSeries','Constant TimeSeries')+'<br/>') +
		html_end()
		)
	at_cFactor.setDefault(1.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Linear'
	xom.addAttribute(at_Function)
	xom.addAttribute(at_factor)
	xom.addAttribute(at_cFactor)
	
	
	# cFactor-dep
	xom.setVisibilityDependency(at_factor, at_cFactor)
	
	return xom

def evaluateFunctionAttribute(xobj):
	if(xobj is None):
		print('Error: xobj is null\n')
		return PyMpc.Math.mat()
	
	if(xobj.name != 'Linear'):
		print('Error: invalid xobj type, expected "Linear", given "{}"'.format(xobj.name))
		return PyMpc.Math.mat()
	
	func_at = xobj.getAttribute('__mpc_function__')
	if(func_at is None):
		print('Error: cannot find "__mpc_function__" attribute\n')
		return PyMpc.Math.mat()
	
	fact_at = xobj.getAttribute('-factor')
	if(fact_at is None):
		print('Error: cannot find "factor" attribute\n')
		return PyMpc.Math.mat()
	
	cFactor_at = xobj.getAttribute('cFactor')
	if(cFactor_at is None):
		print('Error: cannot find "cFactor" attribute\n')
		return PyMpc.Math.mat()
	
	cFactor = cFactor_at.real
	xy = PyMpc.Math.mat(2, 2)
	xy[0, 0] = 0.0
	xy[0, 1] = 0.0
	xy[1, 0] = 1.0
	xy[1, 1] = cFactor
	
	return xy

def writeTcl(pinfo):
	
	#timeSeries Linear $tag <-factor $cFactor>
	xobj = pinfo.definition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	# optional paramters
	sopt = ''
	
	fact_at = xobj.getAttribute('-factor')
	if(fact_at is None):
		raise Exception('Error: cannot find "-factor" attribute\n')
	fact = fact_at.boolean
	if fact:
		cFactor_at = xobj.getAttribute('cFactor')
		if(cFactor_at is None):
			raise Exception('Error: cannot find "cFactor" attribute')
		cFactor = cFactor_at.real
		sopt += ' -factor {}'.format(cFactor)
	
	str_tcl = '{}timeSeries Linear {}{}\n'.format(pinfo.indent, tag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)