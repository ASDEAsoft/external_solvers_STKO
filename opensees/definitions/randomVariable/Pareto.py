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

	# k
	at_kParam = MpcAttributeMetaData()
	at_kParam.type = MpcAttributeType.Real
	at_kParam.name = 'k'
	at_kParam.group = 'Group'
	at_kParam.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k')+'<br/>') +
		html_par('the k parameter of the distribution. k is defined as the shape parameter') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Pareto Random Variable')+'<br/>') +
		html_end()
		)

	# u
	at_uParam = MpcAttributeMetaData()
	at_uParam.type = MpcAttributeType.Real
	at_uParam.name = 'u'
	at_uParam.group = 'Group'
	at_uParam.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('u')+'<br/>') +
		html_par('the u parameter of the distribution. u is defined as the scale parameter') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Pareto Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Pareto Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Pareto Random Variable')+'<br/>') +
		html_end()
		)

	xom = MpcXObjectMetaData()
	xom.name = 'Pareto'
	xom.addAttribute(at_kParam)
	xom.addAttribute(at_uParam)
	xom.addAttribute(at_useStartPoint)
	xom.addAttribute(at_startPoint)

	# startPoint-dep
	xom.setVisibilityDependency(at_useStartPoint, at_startPoint)

	return xom

def writeTcl(pinfo):

	#randomVariable $tag pareto -parameters $u <-startPoint $startPoint>
	xobj = pinfo.definition.XObject

	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName

	tag = xobj.parent.componentId

	k = _get_xobj_attribute(xobj, 'k'). real
	u = _get_xobj_attribute(xobj, 'u'). real

	# optional paramters
	sopt = ''

	useStartPoint = _get_xobj_attribute(xobj, '-startPoint').boolean
	if useStartPoint:
		startPoint = _get_xobj_attribute(xobj, 'startPoint').real
		sopt += ' -startPoint {}'.format(startPoint)

	str_tcl = '{}randomVariable {} pareto -parameters {} {}{}\n'.format(pinfo.indent, tag, k, u, sopt)

	# now write the string into the file
	pinfo.out_file.write(str_tcl)
