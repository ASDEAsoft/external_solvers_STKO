# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# qzType
	at_qzType = MpcAttributeMetaData()
	at_qzType.type = MpcAttributeType.Integer
	at_qzType.name = 'qzType'
	at_qzType.group = 'Non-linear'
	at_qzType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('qzType')+'<br/>') + 
		html_par('qzType = 1 Backbone of q-z curve approximates Reese and O\'Neill\'s (1987) relation for drilled shafts in clay.') +
		html_par('qzType = 2 Backbone of q-z curve approximates Vijayvergiya\'s (1977) relation for piles in sand.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/QzSimple1_Material','QzSimple1 Material')+'<br/>') +
		html_end()
		)
	at_qzType.sourceType = MpcAttributeSourceType.List
	at_qzType.setSourceList([1, 2])
	at_qzType.setDefault(1)
	
	# qult
	at_qult = MpcAttributeMetaData()
	at_qult.type = MpcAttributeType.QuantityScalar
	at_qult.name = 'qult'
	at_qult.group = 'Non-linear'
	at_qult.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('qult')+'<br/>') + 
		html_par('Ultimate capacity of the q-z material. SEE NOTE 1.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/QzSimple1_Material','QzSimple1 Material')+'<br/>') +
		html_end()
		)
	at_qult.dimension = u.F/u.L
	
	# Z50
	at_Z50 = MpcAttributeMetaData()
	at_Z50.type = MpcAttributeType.QuantityScalar
	at_Z50.name = 'Z50'
	at_Z50.group = 'Non-linear'
	at_Z50.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Z50')+'<br/>') + 
		html_par('Displacement at which 50% of qult is mobilized in monotonic loading. SEE NOTE 2.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/QzSimple1_Material','QzSimple1 Material')+'<br/>') +
		html_end()
		)
	at_Z50.dimension = u.L
	
	# use_suction_c
	at_use_suction_c = MpcAttributeMetaData()
	at_use_suction_c.type = MpcAttributeType.Boolean
	at_use_suction_c.name = 'use_suction_c'
	at_use_suction_c.group = 'Non-linear'
	at_use_suction_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_suction_c')+'<br/>') + 
		html_par('Uplift resistance is equal to suction*qult. Default = 0.0. The value of suction must be 0.0 to 0.1. SEE NOTE 3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/QzSimple1_Material','QzSimple1 Material')+'<br/>') +
		html_end()
		)
	
	# suction
	at_suction = MpcAttributeMetaData()
	at_suction.type = MpcAttributeType.Real
	at_suction.name = 'suction'
	at_suction.group = 'Optional parameters'
	at_suction.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('suction')+'<br/>') + 
		html_par('Uplift resistance is equal to suction*qult. Default = 0.0. The value of suction must be 0.0 to 0.1. SEE NOTE 3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/QzSimple1_Material','QzSimple1 Material')+'<br/>') +
		html_end()
		)
	at_suction.setDefault(0.0)
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.Real
	at_c.name = 'c'
	at_c.group = 'Optional parameters'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') + 
		html_par('The viscous damping term (dashpot) on the far-field (elastic) component of the displacement rate (velocity). Default = 0.0. Nonzero c values are used to represent radiation damping effects. SEE NOTE 3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/QzSimple1_Material','QzSimple1 Material')+'<br/>') +
		html_end()
		)
	at_c.setDefault(0.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'QzSimple1'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_qzType)
	xom.addAttribute(at_qult)
	xom.addAttribute(at_Z50)
	xom.addAttribute(at_use_suction_c)
	xom.addAttribute(at_suction)
	xom.addAttribute(at_c)
	
	# suction_c-dep
	xom.setVisibilityDependency(at_use_suction_c, at_suction)
	xom.setVisibilityDependency(at_use_suction_c, at_c)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial QzSimple1 $matTag $qzType $qult $Z50 <$suction $c>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	qzType_at = xobj.getAttribute('qzType')
	if(qzType_at is None):
		raise Exception('Error: cannot find "qzType" attribute')
	qzType = qzType_at.integer
	
	qult_at = xobj.getAttribute('qult')
	if(qult_at is None):
		raise Exception('Error: cannot find "qult" attribute')
	qult = qult_at.quantityScalar
	
	Z50_at = xobj.getAttribute('Z50')
	if(Z50_at is None):
		raise Exception('Error: cannot find "Z50" attribute')
	Z50 = Z50_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	use_suction_c_at = xobj.getAttribute('use_suction_c')
	if(use_suction_c_at is None):
		raise Exception('Error: cannot find "use_suction_c" attribute')
	use_suction_c = use_suction_c_at.boolean
	if use_suction_c:
		suction_at = xobj.getAttribute('suction')
		if(suction_at is None):
			raise Exception('Error: cannot find "suction" attribute')
		suction = suction_at.real
		
		c_at = xobj.getAttribute('c')
		if(c_at is None):
			raise Exception('Error: cannot find "c" attribute')
		c = c_at.real
		
		sopt += '{} {}'.format(suction, c)
	
	
	str_tcl = '{}uniaxialMaterial QzSimple1 {} {} {} {} {}\n'.format(pinfo.indent, tag, qzType, qult.value, Z50.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)