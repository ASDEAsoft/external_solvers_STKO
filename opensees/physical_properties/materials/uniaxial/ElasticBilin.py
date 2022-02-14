# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# EP1
	at_EP1 = MpcAttributeMetaData()
	at_EP1.type = MpcAttributeType.QuantityScalar
	at_EP1.name = 'EP1'
	at_EP1.group = 'Non-linear'
	at_EP1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('EP1')+'<br/>') + 
		html_par('tangent in tension for stains: 0 <= strains <= epsP2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticBilin_Material','ElasticBilin Material')+'<br/>') +
		html_end()
		)
	at_EP1.dimension = u.F/u.L**2
	
	# EP2
	at_EP2 = MpcAttributeMetaData()
	at_EP2.type = MpcAttributeType.QuantityScalar
	at_EP2.name = 'EP2'
	at_EP2.group = 'Non-linear'
	at_EP2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('EP2')+'<br/>') + 
		html_par('tangent when material in tension with strains > epsP2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticBilin_Material','ElasticBilin Material')+'<br/>') +
		html_end()
		)
	at_EP2.dimension = u.F/u.L**2
	
	# epsP2
	at_epsP2 = MpcAttributeMetaData()
	at_epsP2.type = MpcAttributeType.Real
	at_epsP2.name = 'epsP2'
	at_epsP2.group = 'Non-linear'
	at_epsP2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsP2')+'<br/>') + 
		html_par('strain at which material changes tangent in tension.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticBilin_Material','ElasticBilin Material')+'<br/>') +
		html_end()
		)
	
	#Optional parameters
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticBilin_Material','ElasticBilin Material')+'<br/>') +
		html_end()
		)
	
	# EN1
	at_EN1 = MpcAttributeMetaData()
	at_EN1.type = MpcAttributeType.QuantityScalar
	at_EN1.name = 'EN1'
	at_EN1.group = 'Optional parameters'
	at_EN1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('EN1')+'<br/>') + 
		html_par('optional, default = EP1. tangent in compression for stains: 0 < strains <= epsN2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticBilin_Material','ElasticBilin Material')+'<br/>') +
		html_end()
		)
	at_EN1.dimension = u.F/u.L**2
	
	# EN2
	at_EN2 = MpcAttributeMetaData()
	at_EN2.type = MpcAttributeType.QuantityScalar
	at_EN2.name = 'EN2'
	at_EN2.group = 'Optional parameters'
	at_EN2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('EN2')+'<br/>') + 
		html_par('optional, default = EP2. tangent in compression with strains < epsN2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticBilin_Material','ElasticBilin Material')+'<br/>') +
		html_end()
		)
	at_EN2.dimension = u.F/u.L**2
	
	# epsN2
	at_epsN2 = MpcAttributeMetaData()
	at_epsN2.type = MpcAttributeType.Real
	at_epsN2.name = 'epsN2'
	at_epsN2.group = 'Optional parameters'
	at_epsN2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsN2')+'<br/>') + 
		html_par('optional, default = -epsP2. strain at which material changes tangent in compression.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticBilin_Material','ElasticBilin Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ElasticBilin'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_EP1)
	xom.addAttribute(at_EP2)
	xom.addAttribute(at_epsP2)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_EN1)
	xom.addAttribute(at_EN2)
	xom.addAttribute(at_epsN2)
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_EN1)
	xom.setVisibilityDependency(at_Optional, at_EN2)
	xom.setVisibilityDependency(at_Optional, at_epsN2)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ElasticBilin $matTag $EP1 $EP2 $epsP2 <$EN1 $EN2 $epsN2>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	EP1_at = xobj.getAttribute('EP1')
	if(EP1_at is None):
		raise Exception('Error: cannot find "EP1" attribute')
	EP1 = EP1_at.quantityScalar
	
	EP2_at = xobj.getAttribute('EP2')
	if(EP2_at is None):
		raise Exception('Error: cannot find "EP2" attribute')
	EP2 = EP2_at.quantityScalar
	
	epsP2_at = xobj.getAttribute('epsP2')
	if(epsP2_at is None):
		raise Exception('Error: cannot find "epsP2" attribute')
	epsP2 = epsP2_at.real
	
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		EN1_at = xobj.getAttribute('EN1')
		if(EN1_at is None):
			raise Exception('Error: cannot find "EN1" attribute')
		EN1 = EN1_at.quantityScalar
		
		EN2_at = xobj.getAttribute('EN2')
		if(EN2_at is None):
			raise Exception('Error: cannot find "EN2" attribute')
		EN2 = EN2_at.quantityScalar
		
		epsN2_at = xobj.getAttribute('epsN2')
		if(epsN2_at is None):
			raise Exception('Error: cannot find "epsN2" attribute')
		epsN2 = epsN2_at.real
		
		sopt += '{} {} {}'.format(EN1.value, EN2.value, epsN2)
	
	str_tcl = '{}uniaxialMaterial ElasticBilin {} {} {} {} {}\n'.format(pinfo.indent, tag, EP1.value, EP2.value, epsP2, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)