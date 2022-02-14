import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# type
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.String
	at_type.name = 'type'
	at_type.group = 'Group'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') +
		html_par('string to relay material behavior to the element, can be either "PlaneStrain" or "PlaneStress"') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquad_Element','SSPquad Element')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList(['PlaneStrain', 'PlaneStress'])
	at_type.setDefault('PlaneStrain')
	
	# thick
	at_thick = MpcAttributeMetaData()
	at_thick.type = MpcAttributeType.QuantityScalar
	at_thick.name = 'thick'
	at_thick.group = 'Group'
	at_thick.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('thick')+'<br/>') +
		html_par('thickness of the element in out-of-plane direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquad_Element','SSPquad Element')+'<br/>') +
		html_end()
		)
	at_thick.dimension = u.L
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Group'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') +
		html_par('to activate b1 and b2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquad_Element','SSPquad Element')+'<br/>') +
		html_end()
		)
	
	# b1
	at_b1 = MpcAttributeMetaData()
	at_b1.type = MpcAttributeType.QuantityScalar
	at_b1.name = 'b1'
	at_b1.group = 'Optional parameters'
	at_b1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b1')+'<br/>') +
		html_par('constant body force in global x-direction (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquad_Element','SSPquad Element')+'<br/>') +
		html_end()
		)
	at_b1.setDefault(0.0)
	at_b1.dimension = u.F
	
	# b2
	at_b2 = MpcAttributeMetaData()
	at_b2.type = MpcAttributeType.QuantityScalar
	at_b2.name = 'b2'
	at_b2.group = 'Optional parameters'
	at_b2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b2')+'<br/>') +
		html_par('constant body force in global y-direction (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquad_Element','SSPquad Element')+'<br/>') +
		html_end()
		)
	at_b2.setDefault(0.0)
	at_b2.dimension = u.F
	
	xom = MpcXObjectMetaData()
	xom.name = 'SSPquad'
	xom.addAttribute(at_type)
	xom.addAttribute(at_thick)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_b1)
	xom.addAttribute(at_b2)
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_b1)
	xom.setVisibilityDependency(at_Optional, at_b2)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,2),(2,2),(2,2),(2,2)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	# element SSPquad $eleTag $iNode $jNode $kNode $lNode $matTag $type $thick <$b1 $b2>
	
	elem=pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	namePh=phys_prop.XObject.Xnamespace
	if not namePh.startswith('materials.nD'):
		raise Exception('Error: physical property must be "materials.nD" and not: "{}"'.format(namePh))
	
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Quadrilateral or len(node_vect)!=4:
		raise Exception('Error: invalid type of element or number of nodes')
	
	
	# mandatory parameters
	type_at = xobj.getAttribute('type')
	if(type_at is None):
		raise Exception('Error: cannot find "type" attribute')
	type = '"{}"'.format(type_at.string)
	
	thick_at = xobj.getAttribute('thick')
	if(thick_at is None):
		raise Exception('Error: cannot find "thick" attribute')
	thick = thick_at.quantityScalar.value
	
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		b1_at = xobj.getAttribute('b1')
		if(b1_at is None):
			raise Exception('Error: cannot find "b1" attribute')
		b1 = b1_at.quantityScalar.value
		
		b2_at = xobj.getAttribute('b2')
		if(b2_at is None):
			raise Exception('Error: cannot find "b2" attribute')
		b2 = b2_at.quantityScalar.value
		
		sopt += ' {} {}'.format(b1, b2)
	
	
	str_tcl = '{}element SSPquad {}{} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, matTag, type, thick, sopt)
	
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)