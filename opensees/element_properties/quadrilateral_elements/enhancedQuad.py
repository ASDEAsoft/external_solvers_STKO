import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import PyMpc
import PyMpc.App

def makeXObjectMetaData():
	
	# type
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.String
	at_type.name = 'type'
	at_type.group = 'Group'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') +
		html_par('string representing material behavior. Valid options depend on the NDMaterial object and its available material formulations. The type parameter can be either "PlaneStrain" or "PlaneStress."') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Enhanced_Strain_Quadrilateral_Element','Enhanced Quad')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList(['PlaneStrain', 'PlaneStress'])
	at_type.setDefault('PlaneStrain')
	
	# thick
	at_thick = MpcAttributeMetaData()
	at_thick.type = MpcAttributeType.QuantityScalar
	at_thick.name = 'thickness'
	at_thick.group = 'Group'
	at_thick.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('thickness')+'<br/>') +
		html_par('element thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Enhanced_Strain_Quadrilateral_Element','Enhanced Quad')+'<br/>') +
		html_end()
		)
	at_thick.dimension = u.L
	
	xom = MpcXObjectMetaData()
	xom.name = 'enhancedQuad'
	xom.addAttribute(at_type)
	xom.addAttribute(at_thick)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,2),(2,2),(2,2),(2,2)]	#[(ndm, ndf)...]

def writeTcl(pinfo):
	
	elem = pinfo.elem
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral) or (len(elem.nodes) !=4):
		raise Exception(
			'Error: invalid type of element or number of nodes for element type "enhancedQuad".\n'
			'It must be a quadrilateral with 4 nodes, not a {} with {} nodes'.format(elem.geometryFamilyType(), len(elem.nodes)))
	
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	xobj = elem_prop.XObject
	
	if phys_prop is None:
		raise Exception('Error: missing physical property for element type "enhancedQuad"')
	
	# get parameters
	type_at = xobj.getAttribute('type')
	if(type_at is None):
		raise Exception('Error: cannot find "type" attribute')
	type = '"{}"'.format(type_at.string)
	
	thick_at = xobj.getAttribute('thickness')
	if(thick_at is None):
		raise Exception('Error: cannot find "thickness" attribute')
	thickness = thick_at.quantityScalar.value
	
	# update model builder
	pinfo.updateModelBuilder(2, 2)
	
	# write comment
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# element enhancedQuad $eleTag $iNode $jNode $kNode $lNode $thick $type $matTag
	pinfo.out_file.write('{}element enhancedQuad {} {} {} {} {} {} {} {}\n'.format(
		pinfo.indent, elem.id, elem.nodes[0].id, elem.nodes[1].id, elem.nodes[2].id, elem.nodes[3].id, 
		thickness, type, phys_prop.id))