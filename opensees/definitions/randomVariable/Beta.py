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

	# a
	at_a = MpcAttributeMetaData()
	at_a.type = MpcAttributeType.Real
	at_a.name = 'a'
	at_a.group = 'Group'
	at_a.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a')+'<br/>') +
		html_par('the a parameter (min) of the 4-parameter Beta') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Beta Random Variable')+'<br/>') +
		html_end()
		)
		
	# b
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.Real
	at_b.name = 'b'
	at_b.group = 'Group'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b')+'<br/>') +
		html_par('the b parameter (max) of the 4-parameter Beta') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Beta Random Variable')+'<br/>') +
		html_end()
		)
		
	# q
	at_q = MpcAttributeMetaData()
	at_q.type = MpcAttributeType.Real
	at_q.name = 'q'
	at_q.group = 'Group'
	at_q.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('q')+'<br/>') +
		html_par('the q shape parameter of the 4-parameter Beta') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Beta Random Variable')+'<br/>') +
		html_end()
		)
		
	# r
	at_r = MpcAttributeMetaData()
	at_r.type = MpcAttributeType.Real
	at_r.name = 'r'
	at_r.group = 'Group'
	at_r.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('r')+'<br/>') +
		html_par('the r shape parameter of the 4-parameter Beta') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Beta Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Beta Random Variable')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Sensitivity_Command_Manual','Beta Random Variable')+'<br/>') +
		html_end()
		)

	xom = MpcXObjectMetaData()
	xom.name = 'Beta'
	xom.addAttribute(at_a)
	xom.addAttribute(at_b)
	xom.addAttribute(at_q)
	xom.addAttribute(at_r)
	xom.addAttribute(at_useStartPoint)
	xom.addAttribute(at_startPoint)

	# startPoint-dep
	xom.setVisibilityDependency(at_useStartPoint, at_startPoint)

	return xom

def writeTcl(pinfo):

	#randomVariable $tag beta -parameters $a $b $q $r <-startPoint $startPoint>
	xobj = pinfo.definition.XObject

	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName

	tag = xobj.parent.componentId

	a = _get_xobj_attribute(xobj, 'a').real
	b = _get_xobj_attribute(xobj, 'b').real
	q = _get_xobj_attribute(xobj, 'q').real
	r = _get_xobj_attribute(xobj, 'r').real
	
	# optional paramters
	sopt = ''

	useStartPoint = _get_xobj_attribute(xobj, '-startPoint').boolean
	if useStartPoint:
		startPoint = _get_xobj_attribute(xobj, 'startPoint').real
		sopt += ' -startPoint {}'.format(startPoint)

	str_tcl = '{}randomVariable {} beta -parameters {} {} {} {}{}\n'.format(pinfo.indent, tag, a, b, q, r, sopt)

	# now write the string into the file
	pinfo.out_file.write(str_tcl)
