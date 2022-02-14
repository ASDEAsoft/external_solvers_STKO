# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# soilType
	at_soilType = MpcAttributeMetaData()
	at_soilType.type = MpcAttributeType.Integer
	at_soilType.name = 'soilType'
	at_soilType.group = 'Non-linear'
	at_soilType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('soilType')+'<br/>') + 
		html_par('soilType = 1 Backbone of t-z curve approximates Reese and O\'Neill (1987).') +
		html_par('soilType = 2 Backbone of t-z curve approximates Mosher (1984) relation.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzLiq1_Material','TzLiq1 Material')+'<br/>') +
		html_end()
		)
	at_soilType.sourceType = MpcAttributeSourceType.List
	at_soilType.setSourceList([1, 2])
	at_soilType.setDefault(1)
	
	# tult
	at_tult = MpcAttributeMetaData()
	at_tult.type = MpcAttributeType.QuantityScalar
	at_tult.name = 'tult'
	at_tult.group = 'Non-linear'
	at_tult.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tult')+'<br/>') + 
		html_par('Ultimate capacity of the t-z material. SEE NOTE 1.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzLiq1_Material','TzLiq1 Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzLiq1_Material','TzLiq1 Material')+'<br/>') +
		html_end()
		)
	at_Z50.dimension = u.L
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.Real
	at_c.name = 'c'
	at_c.group = 'Non-linear'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') + 
		html_par('The viscous damping term (dashpot) on the far-field (elastic) component of the displacement rate (velocity). (optional Default = 0.0). See NOTE 2.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzLiq1_Material','TzLiq1 Material')+'<br/>') +
		html_end()
		)
	
	# seriesTag
	at_seriesTag = MpcAttributeMetaData()
	at_seriesTag.type = MpcAttributeType.Index
	at_seriesTag.name = 'seriesTag'
	at_seriesTag.group = '-timeSeries'
	at_seriesTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('seriesTag')+'<br/>') + 
		html_par('effective stress can be supplied by a time series by specifying the text string -timeSeries and the tag of the seriesm seriesTag.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/TzLiq1_Material','TzLiq1 Material')+'<br/>') +
		html_end()
		)
	at_seriesTag.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_seriesTag.indexSource.addAllowedNamespace('timeSeries')
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'TzLiq1'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_soilType)
	xom.addAttribute(at_tult)
	xom.addAttribute(at_Z50)
	xom.addAttribute(at_c)
	xom.addAttribute(at_seriesTag)
	
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial TzLiq1 $matTag $tzType $tult $z50 $c -timeSeries $seriesTag
	
	xobj = pinfo.phys_prop.XObject
	
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	tzType_at = xobj.getAttribute('soilType')
	if(tzType_at is None):
		raise Exception('Error: cannot find "soilType" attribute')
	tzType = tzType_at.integer
	
	tult_at = xobj.getAttribute('tult')
	if(tult_at is None):
		raise Exception('Error: cannot find "tult" attribute')
	tult = tult_at.quantityScalar
	
	z50_at = xobj.getAttribute('Z50')
	if(z50_at is None):
		raise Exception('Error: cannot find "Z50" attribute')
	z50 = z50_at.quantityScalar
	
	c_at = xobj.getAttribute('c')
	if(c_at is None):
		raise Exception('Error: cannot find "c" attribute')
	c = c_at.real
	
	seriesTag_at = xobj.getAttribute('seriesTag')
	if(seriesTag_at is None):
		raise Exception('Error: cannot find "seriesTag" attribute')
	seriesTag = seriesTag_at.index
	
	
	str_tcl = '{}uniaxialMaterial TzLiq1 {} {} {} {} {} -timeSeries {}\n'.format(
			pinfo.indent, tag, tzType, tult.value, z50.value, c, seriesTag)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)