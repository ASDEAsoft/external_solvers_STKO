import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# bf1
	at_bf1 = MpcAttributeMetaData()
	at_bf1.type = MpcAttributeType.QuantityScalar
	at_bf1.name = 'bf1'
	at_bf1.group = 'Group'
	at_bf1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bf1')+'<br/>') +
		html_par('body force in global x direction') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/734.htm','Twenty Node Brick Element')+'<br/>') +
		html_end()
		)
	at_bf1.setDefault(0.0)
	at_bf1.dimension = u.F
	
	# bf2
	at_bf2 = MpcAttributeMetaData()
	at_bf2.type = MpcAttributeType.QuantityScalar
	at_bf2.name = 'bf2'
	at_bf2.group = 'Group'
	at_bf2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bf2')+'<br/>') +
		html_par('body force in global y direction') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/734.htm','Twenty Node Brick Element')+'<br/>') +
		html_end()
		)
	at_bf2.setDefault(0.0)
	at_bf2.dimension = u.F
	
	# bf3
	at_bf3 = MpcAttributeMetaData()
	at_bf3.type = MpcAttributeType.QuantityScalar
	at_bf3.name = 'bf3'
	at_bf3.group = 'Group'
	at_bf3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bf3')+'<br/>') +
		html_par('body force in global z direction') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/734.htm','Twenty Node Brick Element')+'<br/>') +
		html_end()
		)
	at_bf3.setDefault(0.0)
	at_bf3.dimension = u.F
	
	
	xom = MpcXObjectMetaData()
	xom.name = '20NodeBrick'
	xom.addAttribute(at_bf1)
	xom.addAttribute(at_bf2)
	xom.addAttribute(at_bf3)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3)]

def writeTcl(pinfo):
	
	#element 20NodeBrick $eletag $node1 $node2 $node3 $node4 $node5 $node6 $node7 $node8 $node9 $node10 $node11
	#$node12 $node13 $node14 $node15 $node16 $node17 $node18 $node19 $node20 $matTag $bf1 $bf2 $bf3
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	pinfo.updateModelBuilder(3,3)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh=phys_prop.XObject.Xnamespace
	if not namePh.startswith('materials.nD'):
		raise Exception('Error: material must be nDMaterial')
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Hexahedron or len(elem.nodes)!=20:
		raise Exception('Error: invalid type of element or number of nodes')
	
	# nodes
	# note that nodes in opensees for the 20-node hexa does not follow the convention used in STKO
	# that's why we use the following permutation
	nstr = ' '.join([str(elem.nodes[i].id) for i in [0,1,2,3,   4,5,6,7,   8,9,10,11,   16,17,18,19,   12,13,14,15]])

	# mandatory parameters
	bf1_at = xobj.getAttribute('bf1')
	if(bf1_at is None):
		raise Exception('Error: cannot find "bf1" attribute')
	bf1 = bf1_at.quantityScalar.value
	
	bf2_at = xobj.getAttribute('bf2')
	if(bf2_at is None):
		raise Exception('Error: cannot find "bf2" attribute')
	bf2 = bf2_at.quantityScalar.value
	
	bf3_at = xobj.getAttribute('bf3')
	if(bf3_at is None):
		raise Exception('Error: cannot find "bf3" attribute')
	bf3 = bf3_at.quantityScalar.value
	
	
	str_tcl = '{}element 20NodeBrick {} {} {} {} {} {}\n'.format(pinfo.indent, tag, nstr, matTag, bf1, bf2, bf3)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)