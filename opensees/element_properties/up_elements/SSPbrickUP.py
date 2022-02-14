import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fBulk
	at_fBulk = MpcAttributeMetaData()
	at_fBulk.type = MpcAttributeType.QuantityScalar
	at_fBulk.name = 'fBulk'
	at_fBulk.group = 'Group'
	at_fBulk.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fBulk')+'<br/>') +
		html_par('bulk modulus of the pore fluid') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
		html_end()
		)
	at_fBulk.dimension = u.F/u.L**2
	
	# fDen
	at_fDen = MpcAttributeMetaData()
	at_fDen.type = MpcAttributeType.QuantityScalar
	at_fDen.name = 'fDen'
	at_fDen.group = 'Group'
	at_fDen.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fDen')+'<br/>') +
		html_par('mass density of the pore fluid') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
		html_end()
		)
	# at_fDen.dimension = u.M/u.L**3
	
	# k1
	at_k1 = MpcAttributeMetaData()
	at_k1.type = MpcAttributeType.Real
	at_k1.name = 'k1'
	at_k1.group = 'Group'
	at_k1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k1')+'<br/>') +
		html_par('permeability coefficient in global x-directions') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
		html_end()
		)
	
	# k2
	at_k2 = MpcAttributeMetaData()
	at_k2.type = MpcAttributeType.Real
	at_k2.name = 'k2'
	at_k2.group = 'Group'
	at_k2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k2')+'<br/>') +
		html_par('permeability coefficient in global y-directions') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
		html_end()
		)
	
	# k3
	at_k3 = MpcAttributeMetaData()
	at_k3.type = MpcAttributeType.Real
	at_k3.name = 'k3'
	at_k3.group = 'Group'
	at_k3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k3')+'<br/>') +
		html_par('permeability coefficient in global z-directions') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
		html_end()
		)
	
	# void
	at_void = MpcAttributeMetaData()
	at_void.type = MpcAttributeType.Real
	at_void.name = 'void'
	at_void.group = 'Group'
	at_void.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('void')+'<br/>') +
		html_par('voids ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Group'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') +
		html_par('spatial pressure field stabilization parameter (see discussion below for more information)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
		html_end()
		)
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Group'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') +
		html_par('to activate b1, b2 and t') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
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
		html_par('constant body force in global x-direction (optional, default = 0.0) - See Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
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
		html_par('constant body force in global y-direction (optional, default = 0.0) - See Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
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
		html_par('constant body force in global z-direction (optional, default = 0.0) - See Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPbrickUP_Element','SSPbrickUP Element')+'<br/>') +
		html_end()
		)
	at_b3.setDefault(0.0)
	at_b3.dimension = u.F
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'SSPbrickUP'
	xom.addAttribute(at_fBulk)
	xom.addAttribute(at_fDen)
	xom.addAttribute(at_k1)
	xom.addAttribute(at_k2)
	xom.addAttribute(at_k3)
	xom.addAttribute(at_void)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_b1)
	xom.addAttribute(at_b2)
	xom.addAttribute(at_b3)
	
	
	# visibility dependencies
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_b1)
	xom.setVisibilityDependency(at_Optional, at_b2)
	xom.setVisibilityDependency(at_Optional, at_b3)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):

	return [(3,4),(3,4),(3,4),(3,4),(3,4),(3,4),(3,4),(3,4)]

def writeTcl(pinfo):
	
	# element SSPbrickUP eleTag? iNode? jNode? kNode? lNode? mNode? nNode? pNode? qNode? matTag? fBulk? fDen? k1? k2? k3? e? alpha? <b1? b2? b3?>
	
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
		nstr += ' {}'.format(node.id)
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Hexahedron or len(node_vect)!=8:
		raise Exception('Error: invalid type of element or number of nodes')
	
	fBulk_at = xobj.getAttribute('fBulk')
	if(fBulk_at is None):
		raise Exception('Error: cannot find "fBulk" attribute')
	fBulk = fBulk_at.quantityScalar
	
	fDen_at = xobj.getAttribute('fDen')
	if(fDen_at is None):
		raise Exception('Error: cannot find "fDen" attribute')
	fDen = fDen_at.quantityScalar
	
	k1_at = xobj.getAttribute('k1')
	if(k1_at is None):
		raise Exception('Error: cannot find "k1" attribute')
	k1 = k1_at.real
	
	k2_at = xobj.getAttribute('k2')
	if(k2_at is None):
		raise Exception('Error: cannot find "k2" attribute')
	k2 = k2_at.real
	
	k3_at = xobj.getAttribute('k3')
	if(k3_at is None):
		raise Exception('Error: cannot find "k3" attribute')
	k3 = k3_at.real
	
	e = xobj.getAttribute('void')
	if(e is None):
		raise Exception('Error: cannot find "void" attribute')
	e = e.real
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
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
		b1 = b1_at.quantityScalar
	
		b2_at = xobj.getAttribute('b2')
		if(b2_at is None):
			raise Exception('Error: cannot find "b2" attribute')
		b2 = b2_at.quantityScalar
	
		b3_at = xobj.getAttribute('b3')
		if(b3_at is None):
			raise Exception('Error: cannot find "b3" attribute')
		b3 = b3_at.quantityScalar
		
		sopt += '{} {} {}'.format(b1.value, b2.value, b3.value)
	
	str_tcl = '{}element SSPbrickUP {}{} {} {} {} {} {} {} {} {} {}\n'.format(pinfo.indent, tag, nstr, matTag, fBulk.value, fDen.value, k1, k2, k3, e, alpha, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)