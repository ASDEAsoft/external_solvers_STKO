# enable default distribution tester for this module
from opensees.definitions.utils.tester.EnableTesterDistribution import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import PyMpc
import PyMpc.Math
from math import exp, pi
import opensees.utils.tcl_input as tclin

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def makeXObjectMetaData():

	# # Function ??? Fa fare il disegno?
	# at_Function = MpcAttributeMetaData()
	# at_Function.type = MpcAttributeType.String
	# at_Function.name = '__mpc_function__'
	# at_Function.group = 'Group'
	# at_Function.description = (
	# 	html_par(html_begin()) +
	# 	html_par(html_boldtext('Function')+'<br/>') +
	# 	html_par('') +
	# 	html_par(html_href('','')+'<br/>') +
	# 	html_end()
	# 	)
	# at_Function.editable = False

	# mean
	at_mean = MpcAttributeMetaData()
	at_mean.type = MpcAttributeType.Real
	at_mean.name = 'mean'
	at_mean.group = 'Group'
	at_mean.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mean')+'<br/>') +
		html_par('the mean of the distribution') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Normal Random Variable')+'<br/>') +
		html_end()
		)
	at_mean.setDefault(0.0)

	# dispersion
	at_dispersion = MpcAttributeMetaData()
	at_dispersion.type = MpcAttributeType.String
	at_dispersion.name = 'dispersion'
	at_dispersion.group = 'Group'
	at_dispersion.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-stdv')+'<br/>') +
		html_par('the dispersion of the distribution (Standard deviation or Coefficient of Variation)') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Normal Random Variable')+'<br/>') +
		html_end()
		)
	at_dispersion.sourceType = MpcAttributeSourceType.List
	at_dispersion.setSourceList(['-stdv',
								'-COV'])
	at_dispersion.setDefault('-stdv')

	# useStdv
	at_useStdv = MpcAttributeMetaData()
	at_useStdv.type = MpcAttributeType.Boolean
	at_useStdv.name = '-stdv'
	at_useStdv.group = 'Group'
	at_useStdv.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-COV')+'<br/>') +
		html_par('the standard deviation of the distribution') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Normal Random Variable')+'<br/>') +
		html_end()
		)
	at_useStdv.editable = False

	# stdv
	at_stdv = MpcAttributeMetaData()
	at_stdv.type = MpcAttributeType.Real
	at_stdv.name = 'stdv'
	at_stdv.group = 'Group'
	at_stdv.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('stdv')+'<br/>') +
		html_par('the standard deviation of the distribution') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Normal Random Variable')+'<br/>') +
		html_end()
		)
	at_stdv.setDefault(1.0)

	# useCOV
	at_useCOV = MpcAttributeMetaData()
	at_useCOV.type = MpcAttributeType.Boolean
	at_useCOV.name = '-COV'
	at_useCOV.group = 'Group'
	at_useCOV.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-COV')+'<br/>') +
		html_par('the coefficient of variation (COV) of the distribution') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Normal Random Variable')+'<br/>') +
		html_end()
		)
	at_useCOV.editable = False

	# COV
	at_COV = MpcAttributeMetaData()
	at_COV.type = MpcAttributeType.Real
	at_COV.name = 'COV'
	at_COV.group = 'Group'
	at_COV.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('COV')+'<br/>') +
		html_par('the coefficient of variation of the distribution') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Normal Random Variable')+'<br/>') +
		html_end()
		)
	at_COV.setDefault(0.1)

	#Optional parameters

	# -startPoint
	at_useStartPoint = MpcAttributeMetaData()
	at_useStartPoint.type = MpcAttributeType.Boolean
	at_useStartPoint.name = '-startPoint'
	at_useStartPoint.group = 'Optional'
	at_useStartPoint.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-startPoint')+'<br/>') +
		html_par('Specify the starting point') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Normal Random Variable')+'<br/>') +
		html_end()
		)

	# startPoint
	at_startPoint = MpcAttributeMetaData()
	at_startPoint.type = MpcAttributeType.Real
	at_startPoint.name = 'startPoint'
	at_startPoint.group = '-startPoint'
	at_startPoint.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-startPoint')+'<br/>') +
		html_par('Specify the starting point') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Normal Random Variable')+'<br/>') +
		html_end()
		)

	xom = MpcXObjectMetaData()
	xom.name = 'Normal'
	# xom.addAttribute(at_Function)
	xom.addAttribute(at_mean)
	xom.addAttribute(at_dispersion)
	xom.addAttribute(at_useStdv)
	xom.addAttribute(at_stdv)
	xom.addAttribute(at_useCOV)
	xom.addAttribute(at_COV)
	xom.addAttribute(at_useStartPoint)
	xom.addAttribute(at_startPoint)

	# stdv-dep
	xom.setVisibilityDependency(at_useStdv, at_stdv)

	# COV-dep
	xom.setVisibilityDependency(at_useCOV, at_COV)

	# startPoint-dep
	xom.setVisibilityDependency(at_useStartPoint, at_startPoint)

	# auto-exclusive dependencies
	# dispersion
	xom.setBooleanAutoExclusiveDependency(at_dispersion, at_useStdv)
	xom.setBooleanAutoExclusiveDependency(at_dispersion, at_useCOV)

	return xom

# def evaluateFunctionAttribute(xobj):
# 	if(xobj is None):
# 		print('Error: xobj is null\n')
# 		return PyMpc.Math.mat()
#
# 	if(xobj.name != 'Normal'):
# 		print('Error: invalid xobj type, expected "Normal", given "{}"'.format(xobj.name))
# 		return PyMpc.Math.mat()
#
# 	func_at = xobj.getAttribute('__mpc_function__')
# 	if(func_at is None):
# 		print('Error: cannot find "__mpc_function__" attribute\n')
# 		return PyMpc.Math.mat()
#
# 	mean_at = xobj.getAttribute('mean')
# 	if(mean_at is None):
# 		print('Error: cannot find "mean" attribute\n')
# 		return PyMpc.Math.mat()
# 	mu = mean_at.real
#
# 	useStdv_at = xobj.getAttribute('-stdv')
# 	if(useStdv_at is None):
# 		print('Error: cannot find "-stdv" attribute\n')
# 		return PyMpc.Math.mat()
# 	useStdv = useStdv_at.boolean
#
# 	if useStdv:
# 		stdv_at = xobj.getAttribute('stdv')
# 		if(stdv_at is None):
# 			print('Error: cannot find "stdv" attribute\n')
# 			return PyMpc.Math.mat()
# 		sigma = stdv_at.real
# 	else:
# 		useCOV_at = xobj.getAttribute('-COV')
# 		if(useCOV_at is None):
# 			print('Error: cannot find "-COV" attribute\n')
# 			return PyMpc.Math.mat()
# 		useCOV = useCOV_at.boolean
# 		if useCOV:
# 			COV_at = xobj.getAttribute('COV')
# 			if(COV_at is None):
# 				print('Error: cannot find "COV" attribute\n')
# 				return PyMpc.Math.mat()
# 			COV = COV_at.real
# 		else:
# 			print('Error: did not assigned stdv or COV\n')
# 			return PyMpc.Math.mat()
# 		if mu <= 0:
# 			# print('Error: COV can be used only with mean > 0.0\n')
# 			PyMpc.IO.write_cerr('Error: COV can be used only with mean > 0.0\n')
# 			return PyMpc.Math.mat()
# 		else:
# 			sigma = COV * mu
#
# 	# cFactor = cFactor_at.real
# 	xy = PyMpc.Math.mat(100, 2)
# 	x_begin = mu - 5*sigma
# 	x_end = mu + 5*sigma
#
# 	for i in range(100):
# 		xy[i, 0] = (x_end-x_begin)/100*i+x_begin
# 		xy[i, 1] = 1.0 / (sigma*(pi*2.0)**0.5) * exp( - 0.5 * ( ( xy[i,0] - mu ) / sigma )**2.0 )
#
# 	return xy

def writeTcl(pinfo):

	#randomVariable $tag normal -mean $mean -stdv $stdv
	xobj = pinfo.definition.XObject

	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName

	tag = xobj.parent.componentId

	#get mean
	mu = _get_xobj_attribute(xobj, 'mean').real

	# get Standard deviation
	useStdv = _get_xobj_attribute(xobj, '-stdv').boolean
	if useStdv:
		sigma = _get_xobj_attribute(xobj, 'stdv').real
	else:
		useCOV = _get_xobj_attribute(xobj, '-COV').boolean
		if useCOV:
			COV = _get_xobj_attribute(xobj, 'COV').real
		else:
			raise Exception('Error: did not assigned stdv or COV\n')
		if mu <= 0:
			raise Exception('Error: COV can be used only with mean > 0.0\n')
		else:
			sigma = COV * mu

	# optional paramters
	sopt = ''

	useStartPoint = _get_xobj_attribute(xobj, '-startPoint').boolean
	if useStartPoint:
		startPoint = _get_xobj_attribute(xobj, 'startPoint').real
		sopt += ' -startPoint {}'.format(startPoint)

	str_tcl = '{}randomVariable {} normal -mean {} -stdv {}{}\n'.format(pinfo.indent, tag, mu, sigma, sopt)

	# now write the string into the file
	pinfo.out_file.write(str_tcl)
