import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def _err(msg):
	return 'Error in "SetInitialTemperature" :\n{}'.format(msg)

def makeXObjectMetaData():
	t0 = MpcAttributeMetaData()
	t0.type = MpcAttributeType.QuantityScalar
	t0.name = 't0'
	t0.group = 'Data'
	t0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('t0')+'<br/>') + 
		html_par('The initial temperature') +
		html_end()
		)
	t0.setDefault(0.0)
	xom = MpcXObjectMetaData()
	xom.name = 'SetInitialTemperature'
	xom.Xgroup = 'Thermal'
	xom.addAttribute(t0)
	return xom

def writeTcl(pinfo):
	
	# a global value
	t0 = pinfo.analysis_step.XObject.getAttribute('t0').quantityScalar.value
	pinfo.out_file.write('\n{}# Define initial temperature on all DOFs\n'.format(pinfo.indent))
	pinfo.out_file.write('{}foreach node [getNodeTags] {{\n'.format(pinfo.indent))
	pinfo.out_file.write('{}{}setNodeDisp $node 1 {} -commit\n'.format(pinfo.indent, pinfo.tabIndent, t0))
	pinfo.out_file.write('{}}}\n'.format(pinfo.indent))