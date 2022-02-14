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

	# epsilon
	at_epsilon = MpcAttributeMetaData()
	at_epsilon.type = MpcAttributeType.Real
	at_epsilon.name = 'epsilon'
	at_epsilon.group = 'Group'
	at_epsilon.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('u')+'<br/>') +
		html_par('the epsilon parameter of the distribution. epsilon is defined as') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Type3SmallestValue Random Variable')+'<br/>') +
		html_end()
		)
		
	# u
	at_u = MpcAttributeMetaData()
	at_u.type = MpcAttributeType.Real
	at_u.name = 'u'
	at_u.group = 'Group'
	at_u.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('u')+'<br/>') +
		html_par('the u parameter of the distribution. u is defined as ') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Type3SmallestValue Random Variable')+'<br/>') +
		html_end()
		)
		
	# k
	at_k = MpcAttributeMetaData()
	at_k.type = MpcAttributeType.Real
	at_k.name = 'k'
	at_k.group = 'Group'
	at_k.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k')+'<br/>') +
		html_par('the k parameter of the distribution. k is defined as ') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Type3SmallestValue Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Type3SmallestValue Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Type3SmallestValue Random Variable')+'<br/>') +
		html_end()
		)

	xom = MpcXObjectMetaData()
	xom.name = 'Type3SmallestValue'
	xom.addAttribute(at_epsilon)
	xom.addAttribute(at_u)
	xom.addAttribute(at_k)
	xom.addAttribute(at_useStartPoint)
	xom.addAttribute(at_startPoint)

	# startPoint-dep
	xom.setVisibilityDependency(at_useStartPoint, at_startPoint)

	return xom

def writeTcl(pinfo):

	#randomVariable $tag type3SmallestValue -parameters $u <-startPoint $startPoint>
	xobj = pinfo.definition.XObject

	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName

	tag = xobj.parent.componentId
	
	epsilon = _get_xobj_attribute(xobj, 'epsilon'). real
	u = _get_xobj_attribute(xobj, 'u'). real
	k = _get_xobj_attribute(xobj, 'k'). real

	# optional paramters
	sopt = ''

	useStartPoint = _get_xobj_attribute(xobj, '-startPoint').boolean
	if useStartPoint:
		startPoint = _get_xobj_attribute(xobj, 'startPoint').real
		sopt += ' -startPoint {}'.format(startPoint)

	str_tcl = '{}randomVariable {} type3SmallestValue -parameters {} {} {}{}\n'.format(pinfo.indent, tag, epsilon, u, k, sopt)

	# now write the string into the file
	pinfo.out_file.write(str_tcl)
