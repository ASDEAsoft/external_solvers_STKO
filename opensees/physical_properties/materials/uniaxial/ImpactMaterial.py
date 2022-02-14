# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# K1
	at_K1 = MpcAttributeMetaData()
	at_K1.type = MpcAttributeType.QuantityScalar
	at_K1.name = 'K1'
	at_K1.group = 'Non-linear'
	at_K1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K1')+'<br/>') + 
		html_par('initial stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Impact_Material','Impact Material')+'<br/>') +
		html_end()
		)
	at_K1.dimension = u.F/u.L
	
	# K2
	at_K2 = MpcAttributeMetaData()
	at_K2.type = MpcAttributeType.QuantityScalar
	at_K2.name = 'K2'
	at_K2.group = 'Non-linear'
	at_K2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K2')+'<br/>') + 
		html_par('secondary stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Impact_Material','Impact Material')+'<br/>') +
		html_end()
		)
	at_K2.dimension = u.F/u.L
	
	# delta_y
	at_delta_y = MpcAttributeMetaData()
	at_delta_y.type = MpcAttributeType.QuantityScalar
	at_delta_y.name = 'delta_y'
	at_delta_y.group = 'Non-linear'
	at_delta_y.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('delta_y')+'<br/>') + 
		html_par('yield displacement') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Impact_Material','Impact Material')+'<br/>') +
		html_end()
		)
	at_delta_y.dimension = u.L
	
	# gap
	at_gap = MpcAttributeMetaData()
	at_gap.type = MpcAttributeType.QuantityScalar
	at_gap.name = 'gap'
	at_gap.group = 'Non-linear'
	at_gap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gap')+'<br/>') + 
		html_par('initial gap*') +
		html_par('This material is implemented as a compression-only gap material. Delta_y and gap should be input as negative values.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Impact_Material','Impact Material')+'<br/>') +
		html_end()
		)
	at_gap.dimension = u.L
	
	xom = MpcXObjectMetaData()
	xom.name = 'ImpactMaterial'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_K1)
	xom.addAttribute(at_K2)
	xom.addAttribute(at_delta_y)
	xom.addAttribute(at_gap)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ImpactMaterial $matTag $K1 $K2 $δy $gap
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	K1_at = xobj.getAttribute('K1')
	if(K1_at is None):
		raise Exception('Error: cannot find "K1" attribute')
	K1 = K1_at.quantityScalar
	
	K2_at = xobj.getAttribute('K2')
	if(K2_at is None):
		raise Exception('Error: cannot find "K2" attribute')
	K2 = K2_at.quantityScalar
	
	delta_y_at = xobj.getAttribute('delta_y')
	if(delta_y_at is None):
		raise Exception('Error: cannot find "delta_y" attribute')
	delta_y = delta_y_at.quantityScalar
	
	gap_at = xobj.getAttribute('gap')
	if(gap_at is None):
		raise Exception('Error: cannot find "gap" attribute')
	gap = gap_at.quantityScalar
	
	
	str_tcl = '{}uniaxialMaterial ImpactMaterial {} {} {} {} {}\n'.format(
			pinfo.indent, tag, K1.value, K2.value, delta_y.value, gap.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)