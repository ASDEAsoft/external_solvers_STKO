import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# matTag
	at_matTag = MpcAttributeMetaData()
	at_matTag.type = MpcAttributeType.Index
	at_matTag.name = 'matTag'
	at_matTag.group = 'Group'
	at_matTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') + 
		html_par('tag of uniaxial material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniaxial_Section','Uniaxial Section')+'<br/>') +
		html_end()
		)
	at_matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# quantity
	at_quantity = MpcAttributeMetaData()
	at_quantity.type = MpcAttributeType.String
	at_quantity.name = 'quantity'
	at_quantity.group = 'Group'
	at_quantity.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('quantity')+'<br/>') + 
		html_par('the force-deformation quantity to be modeled by this section object. One of the following strings is used:') +
		html_par('P Axial force-deformation') +
		html_par('Mz Moment-curvature about section local z-axis') +
		html_par('Vy Shear force-deformation along section local y-axis') +
		html_par('My Moment-curvature about section local z-axis') +
		html_par('Vz Shear force-deformation along section local z-axis') +
		html_par('T Torsion Force-Deformation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Uniaxial_Section','Uniaxial Section')+'<br/>') +
		html_end()
		)
	at_quantity.sourceType = MpcAttributeSourceType.List
	at_quantity.setSourceList(['P', 'Mz', 'Vy', 'My', 'Vz', 'T'])
	at_quantity.setDefault('P')
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'Uniaxial'
	xom.addAttribute(at_matTag)
	xom.addAttribute(at_quantity)
	
	return xom

def writeTcl(pinfo, xobj):
	
	#section Uniaxial $secTag $matTag $quantity
	
	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	matTag_at = xobj.getAttribute('matTag')
	if(matTag_at is None):
		raise Exception('Error: cannot find "matTag" attribute')
	matTag = matTag_at.index
	
	quantity_at = xobj.getAttribute('quantity')
	if(quantity_at is None):
		raise Exception('Error: cannot find "quantity" attribute')
	quantity = quantity_at.string
	
	
	str_tcl = '{}section Uniaxial {} {} {}\n'.format(pinfo.indent, tag, matTag, quantity)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)