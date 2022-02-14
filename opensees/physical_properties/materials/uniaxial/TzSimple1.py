# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# tzType
	at_tzType = MpcAttributeMetaData()
	at_tzType.type = MpcAttributeType.Integer
	at_tzType.name = 'tzType'
	at_tzType.group = 'Non-linear'
	at_tzType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tzType')+'<br/>') + 
		html_par('soilType = 1 Backbone of t-z curve approximates Reese and O\'Neill (1987).') +
		html_par('soilType = 2 Backbone of t-z curve approximates Mosher (1984) relation.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzSimple1_Material','TzSimple1 Material')+'<br/>') +
		html_end()
		)
	at_tzType.sourceType = MpcAttributeSourceType.List
	at_tzType.setSourceList([1, 2])
	at_tzType.setDefault(1)
	
	# tult
	at_tult = MpcAttributeMetaData()
	at_tult.type = MpcAttributeType.QuantityScalar
	at_tult.name = 'tult'
	at_tult.group = 'Non-linear'
	at_tult.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tult')+'<br/>') + 
		html_par('Ultimate capacity of the t-z material. SEE NOTE 1.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzSimple1_Material','TzSimple1 Material')+'<br/>') +
		html_end()
		)
	at_tult.dimension = u.F/u.L**2
	
	# Z50
	at_Z50 = MpcAttributeMetaData()
	at_Z50.type = MpcAttributeType.QuantityScalar
	at_Z50.name = 'Z50'
	at_Z50.group = 'Non-linear'
	at_Z50.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Z50')+'<br/>') + 
		html_par('Displacement at which 50% of tult is mobilized in monotonic loading.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzSimple1_Material','TzSimple1 Material')+'<br/>') +
		html_end()
		)
	at_Z50.dimension = u.L
	
	# use_c
	at_use_c = MpcAttributeMetaData()
	at_use_c.type = MpcAttributeType.Boolean
	at_use_c.name = 'use_c'
	at_use_c.group = 'Non-linear'
	at_use_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_c')+'<br/>') + 
		html_par('The viscous damping term (dashpot) on the far-field (elastic) component of the displacement rate (velocity). (optional Default = 0.0). See NOTE 2.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzSimple1_Material','TzSimple1 Material')+'<br/>') +
		html_end()
		)
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.Real
	at_c.name = 'c'
	at_c.group = 'Optional parameters'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') + 
		html_par('The viscous damping term (dashpot) on the far-field (elastic) component of the displacement rate (velocity). (optional Default = 0.0). See NOTE 2.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzSimple1_Material','TzSimple1 Material')+'<br/>') +
		html_end()
		)
	at_c.setDefault(0.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'TzSimple1'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_tzType)
	xom.addAttribute(at_tult)
	xom.addAttribute(at_Z50)
	xom.addAttribute(at_use_c)
	xom.addAttribute(at_c)
	
	# c-dep
	xom.setVisibilityDependency(at_use_c, at_c)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial TzSimple1 $matTag $tzType $tult $z50 <$c>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	tzType_at = xobj.getAttribute('tzType')
	if(tzType_at is None):
		raise Exception('Error: cannot find "tzType" attribute')
	tzType = tzType_at.integer
	
	tult_at = xobj.getAttribute('tult')
	if(tult_at is None):
		raise Exception('Error: cannot find "tult" attribute')
	tult = tult_at.quantityScalar
	
	z50_at = xobj.getAttribute('Z50')
	if(z50_at is None):
		raise Exception('Error: cannot find "Z50" attribute')
	z50 = z50_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	use_c_at = xobj.getAttribute('use_c')
	if(use_c_at is None):
		raise Exception('Error: cannot find "use_c" attribute')
	use_c = use_c_at.boolean
	if use_c:
		c_at = xobj.getAttribute('c')
		if(c_at is None):
			raise Exception('Error: cannot find "c" attribute')
		c = c_at.real
		
		sopt += '{}'.format(c)
	
	
	str_tcl = '{}uniaxialMaterial TzSimple1 {} {} {} {} {}\n'.format(
			pinfo.indent, tag, tzType, tult.value, z50.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)