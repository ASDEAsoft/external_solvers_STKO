import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import PyMpc
import PyMpc.App

def makeXObjectMetaData():
	xom = MpcXObjectMetaData()
	xom.name = 'nineNodeQuad'
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2)]	#[(ndm, ndf)...]

def writeTcl(pinfo):
	
	elem = pinfo.elem
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral) or (len(elem.nodes) !=9):
		raise Exception(
			'Error: invalid type of element or number of nodes for element type "nineNodeQuad".\n'
			'It must be a quadrilateral with 9 nodes, not a {} with {} nodes'.format(elem.geometryFamilyType(), len(elem.nodes)))
	
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	xobj = elem_prop.XObject
	
	if phys_prop is None:
		raise Exception('Error: missing physical property for element type "nineNodeQuad"')
	
	# update model builder
	pinfo.updateModelBuilder(2, 2)
	
	# write comment
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# element nineNodeQuad $eleTag $iNode $jNode $kNode $lNode $thick $type $matTag
	pinfo.out_file.write('{}element nineNodeQuad {} {} {} {} {} {} {} {} {} {} {}\n'.format(
		pinfo.indent, elem.id, 
		elem.nodes[0].id, elem.nodes[1].id, elem.nodes[2].id, elem.nodes[3].id, 
		elem.nodes[4].id, elem.nodes[5].id, elem.nodes[6].id, elem.nodes[7].id, elem.nodes[8].id, 
		phys_prop.id))