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

	# mean
	at_mean = MpcAttributeMetaData()
	at_mean.type = MpcAttributeType.Real
	at_mean.name = 'mean'
	at_mean.group = 'Group'
	at_mean.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mean')+'<br/>') +
		html_par('the mean of the distribution') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
		html_end()
		)
	at_COV.setDefault(0.1)

	# useParameters
	at_useParameters = MpcAttributeMetaData()
	at_useParameters.type = MpcAttributeType.Boolean
	at_useParameters.name = '-parameters'
	at_useParameters.group = 'Group'
	at_useParameters.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-parameters')+'<br/>') +
		html_par('the a and b of the uniform distribution') +
		html_par('<u>Please note</u> that if parameters are specified, mean and stdv are ignored') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
		html_end()
		)
	at_useParameters.setDefault(False)

	# a
	at_a = MpcAttributeMetaData()
	at_a.type = MpcAttributeType.Real
	at_a.name = 'a'
	at_a.group = '-parameters'
	at_a.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a')+'<br/>') +
		html_par('Uniform distribution from a to b') +
		html_par('<u>Please note</u> that if parameters are specified, mean and stdv are ignored') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
		html_end()
		)

	# b
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.Real
	at_b.name = 'b'
	at_b.group = '-parameters'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('zeta')+'<br/>') +
		html_par('Uniform distribution from a to b') +
		html_par('<u>Please note</u> that if parameters are specified, mean and stdv are ignored') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
		html_end()
		)

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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Uniform Random Variable')+'<br/>') +
		html_end()
		)

	xom = MpcXObjectMetaData()
	xom.name = 'Uniform'
	# xom.addAttribute(at_Function)
	xom.addAttribute(at_mean)
	xom.addAttribute(at_dispersion)
	xom.addAttribute(at_useStdv)
	xom.addAttribute(at_stdv)
	xom.addAttribute(at_useCOV)
	xom.addAttribute(at_COV)
	xom.addAttribute(at_useParameters)
	xom.addAttribute(at_a)
	xom.addAttribute(at_b)
	xom.addAttribute(at_useStartPoint)
	xom.addAttribute(at_startPoint)

	# stdv-dep
	xom.setVisibilityDependency(at_useStdv, at_stdv)

	# COV-dep
	xom.setVisibilityDependency(at_useCOV, at_COV)

	# a b - dep
	xom.setVisibilityDependency(at_useParameters, at_a)
	xom.setVisibilityDependency(at_useParameters, at_b)

	# startPoint-dep
	xom.setVisibilityDependency(at_useStartPoint, at_startPoint)

	# auto-exclusive dependencies
	# dispersion
	xom.setBooleanAutoExclusiveDependency(at_dispersion, at_useStdv)
	xom.setBooleanAutoExclusiveDependency(at_dispersion, at_useCOV)

	return xom

def writeTcl(pinfo):

	#randomVariable $tag uniform <-mean $mean -stdv $stdv> <-parameters $a $b>
	xobj = pinfo.definition.XObject

	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName

	tag = xobj.parent.componentId

	useParameters = _get_xobj_attribute(xobj, '-parameters').boolean
	if useParameters:
		a = _get_xobj_attribute(xobj, 'a').real
		b = _get_xobj_attribute(xobj, 'b'). real
	else:
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

	if useParameters:
		str_tcl = '{}randomVariable {} uniform -parameters {} {}{}\n'.format(pinfo.indent, tag, a, b, sopt)
	else:
		str_tcl = '{}randomVariable {} uniform -mean {} -stdv {}{}\n'.format(pinfo.indent, tag, mu, sigma, sopt)

	# now write the string into the file
	pinfo.out_file.write(str_tcl)
