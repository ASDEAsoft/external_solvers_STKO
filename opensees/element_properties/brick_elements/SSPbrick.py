import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Group'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') +
		html_par('to activate b1, b2 and b3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrick_Element','SSPbrick Element')+'<br/>') +
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
		html_par('constant body force in global x-directions (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrick_Element','SSPbrick Element')+'<br/>') +
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
		html_par('constant body force in global y-directions (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrick_Element','SSPbrick Element')+'<br/>') +
		html_end()
		)
	at_b2.setDefault(0.0)
	at_b2.dimension = u.F
	
	# b3
	at_b3 = MpcAttributeMetaData()
	at_b3.type = MpcAttributeType.QuantityScalar
	at_b3.name = 'b3'
	at_b3.group = 'Optional parameters'
	at_b3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b3')+'<br/>') +
		html_par('constant body force in global z-directions (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrick_Element','SSPbrick Element')+'<br/>') +
		html_end()
		)
	at_b3.setDefault(0.0)
	at_b3.dimension = u.F
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'SSPbrick'
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_b1)
	xom.addAttribute(at_b2)
	xom.addAttribute(at_b3)
	
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_b1)
	xom.setVisibilityDependency(at_Optional, at_b2)
	xom.setVisibilityDependency(at_Optional, at_b3)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3),(3,3)]

def writeTcl(pinfo):
	# element SSPbrick $eleTag $iNode $jNode $kNode $lNode $mNode $nNode $pNode $qNode $matTag <$b1 $b2 $b3>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh=phys_prop.XObject.Xnamespace
	if not namePh.startswith('materials.nD'):
		raise Exception ('Error: materials must be nDMaterial')
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += '{} '.format(node.id)
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Hexahedron or len(node_vect)!=8:
		raise Exception('Error: invalid type of element or number of nodes')
	
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
		
		b3_at = xobj.getAttribute('b3')
		if(b3_at is None):
			raise Exception('Error: cannot find "b3" attribute')
		b3 = b3_at.quantityScalar.value
		
		sopt += ' {} {} {}'.format(b1, b2, b3)
	# element SSPbrick $eleTag $iNode $jNode $kNode $lNode $mNode $nNode $pNode $qNode $matTag <$b1 $b2 $b3>
	str_tcl = '{}element SSPbrick {} {}{}{}\n'.format(pinfo.indent, tag, nstr, matTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
