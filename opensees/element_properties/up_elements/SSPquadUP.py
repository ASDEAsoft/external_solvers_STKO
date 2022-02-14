import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# thick
	at_thick = MpcAttributeMetaData()
	at_thick.type = MpcAttributeType.QuantityScalar
	at_thick.name = 'thick'
	at_thick.group = 'Group'
	at_thick.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('thick')+'<br/>') +
		html_par('thickness of the element in out-of-plane direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	at_thick.dimension = u.L
	
	# bulk
	at_fbulk = MpcAttributeMetaData()
	at_fbulk.type = MpcAttributeType.QuantityScalar
	at_fbulk.name = 'fbulk'
	at_fbulk.group = 'Group'
	at_fbulk.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fbulk')+'<br/>') +
		html_par('bulk modulus of the pore fluid') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	at_fbulk.dimension = u.F/u.L**2
	
	# fDen
	at_fDen = MpcAttributeMetaData()
	at_fDen.type = MpcAttributeType.QuantityScalar
	at_fDen.name = 'fDen'
	at_fDen.group = 'Group'
	at_fDen.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fDen')+'<br/>') +
		html_par('mass density of the pore fluid') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	
	# Optional_1
	at_Optional_1 = MpcAttributeMetaData()
	at_Optional_1.type = MpcAttributeType.Boolean
	at_Optional_1.name = 'Optional_1'
	at_Optional_1.group = 'Group'
	at_Optional_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional_1')+'<br/>') +
		html_par('to activate b1, b2 and t') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	
	# b1
	at_b1 = MpcAttributeMetaData()
	at_b1.type = MpcAttributeType.Real
	at_b1.name = 'b1'
	at_b1.group = 'Optional parameters 1'
	at_b1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b1')+'<br/>') +
		html_par('constant body force in global x-direction (optional, default = 0.0) - See Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	at_b1.setDefault(0.0)
	
	# b2
	at_b2 = MpcAttributeMetaData()
	at_b2.type = MpcAttributeType.Real
	at_b2.name = 'b2'
	at_b2.group = 'Optional parameters 1'
	at_b2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b2')+'<br/>') +
		html_par('constant body force in global y-direction (optional, default = 0.0) - See Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	at_b2.setDefault(0.0)
	
	
	# Optional_2
	at_Optional_2 = MpcAttributeMetaData()
	at_Optional_2.type = MpcAttributeType.Boolean
	at_Optional_2.name = 'Optional_2'
	at_Optional_2.group = 'Group'
	at_Optional_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional_2')+'<br/>') +
		html_par('to activate Pup, Plow, Pleft, and Pright') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	
	# Pup
	at_Pup = MpcAttributeMetaData()
	at_Pup.type = MpcAttributeType.Real
	at_Pup.name = 'Pup'
	at_Pup.group = 'Optional parameters 2'
	at_Pup.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Pup')+'<br/>') +
		html_par('constant body force in global x-direction (optional, default = 0.0) - See Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	at_Pup.setDefault(0.0)
	
	# Plow
	at_Plow = MpcAttributeMetaData()
	at_Plow.type = MpcAttributeType.Real
	at_Plow.name = 'Plow'
	at_Plow.group = 'Optional parameters 2'
	at_Plow.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Plow')+'<br/>') +
		html_par('constant body force in global x-direction (optional, default = 0.0) - See Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	at_Plow.setDefault(0.0)
	
	# Pleft
	at_Pleft = MpcAttributeMetaData()
	at_Pleft.type = MpcAttributeType.Real
	at_Pleft.name = 'Pleft'
	at_Pleft.group = 'Optional parameters 2'
	at_Pleft.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Pleft')+'<br/>') +
		html_par('constant body force in global x-direction (optional, default = 0.0) - See Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	at_Pleft.setDefault(0.0)
	
	
	# Pright
	at_Pright = MpcAttributeMetaData()
	at_Pright.type = MpcAttributeType.Real
	at_Pright.name = 'Pright'
	at_Pright.group = 'Optional parameters 2'
	at_Pright.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Pright')+'<br/>') +
		html_par('constant body force in global x-direction (optional, default = 0.0) - See Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SSPquadUP_Element','SSPquadUP Element')+'<br/>') +
		html_end()
		)
	at_Pright.setDefault(0.0)
	
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'SSPquadUP'
	xom.addAttribute(at_thick)
	xom.addAttribute(at_fbulk)
	xom.addAttribute(at_fDen)
	xom.addAttribute(at_k1)
	xom.addAttribute(at_k2)
	xom.addAttribute(at_void)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_Optional_1)
	xom.addAttribute(at_Optional_2)
	xom.addAttribute(at_b1)
	xom.addAttribute(at_b2)
	xom.addAttribute(at_Pup)
	xom.addAttribute(at_Plow)
	xom.addAttribute(at_Pleft)
	xom.addAttribute(at_Pright)
	
	# visibility dependencies
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional_1, at_b1)
	xom.setVisibilityDependency(at_Optional_1, at_b2)
	
	xom.setVisibilityDependency(at_Optional_2, at_Pup)
	xom.setVisibilityDependency(at_Optional_2, at_Plow)
	xom.setVisibilityDependency(at_Optional_2, at_Pleft)
	xom.setVisibilityDependency(at_Optional_2, at_Pright)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3),(2,3),(2,3)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	#element SSPquadUP eleTag? iNode? jNode? kNode? lNode? matTag? t? fBulk? fDen? k1? k2? void? alpha? <b1? b2?> <Pup? Plow? Pleft? Pright?>?"
	
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
	thick_at = xobj.getAttribute('thick')
	if(thick_at is None):
		raise Exception('Error: cannot find "thick" attribute')
	thick = thick_at.quantityScalar
	
	fbulk_at = xobj.getAttribute('fbulk')
	if(fbulk_at is None):
		raise Exception('Error: cannot find "fbulk" attribute')
	fbulk = fbulk_at.quantityScalar
	
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
	
	void_at = xobj.getAttribute('void')
	if(void_at is None):
		raise Exception('Error: cannot find "void" attribute')
	void = void_at.real
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	
	# optional paramters
	sopt1 = ''
	sopt2 = ''
	
	Optional_1_at = xobj.getAttribute('Optional_1')
	if(Optional_1_at is None):
		raise Exception('Error: cannot find "Optional_1" attribute')
	Optional_1 = Optional_1_at.boolean
	if Optional_1:
		b1_at = xobj.getAttribute('b1')
		if(b1_at is None):
			raise Exception('Error: cannot find "b1" attribute')
		b1 = b1_at.real
	
		b2_at = xobj.getAttribute('b2')
		if(b2_at is None):
			raise Exception('Error: cannot find "b2" attribute')
		b2 = b2_at.real
		
		sopt1 += ' {} {}'.format(b1, b2)
	
	Optional_2_at = xobj.getAttribute('Optional_2')
	if(Optional_2_at is None):
		raise Exception('Error: cannot find "Optional_2" attribute')
	Optional_2 = Optional_2_at.boolean
	if Optional_2:
		Pup_at = xobj.getAttribute('Pup')
		if(Pup_at is None):
			raise Exception('Error: cannot find "Pup" attribute')
		Pup = Pup_at.real

		Plow_at = xobj.getAttribute('Plow')
		if(Plow_at is None):
			raise Exception('Error: cannot find "Plow" attribute')
		Plow = Plow_at.real

		Pleft_at = xobj.getAttribute('Pleft')
		if(Pleft_at is None):
			raise Exception('Error: cannot find "Pleft" attribute')
		Pleft = Pleft_at.real
		
		Pright_at = xobj.getAttribute('Pright')
		if(Pright_at is None):
			raise Exception('Error: cannot find "Pright" attribute')
		Pright = Pright_at.real
		
		sopt2 += ' {} {} {} {}'.format(Pup, Plow, Pleft, Pright)
	
	str_tcl = '{}element SSPquadUP {}{} {} {} {} {} {} {} {} {}{}{}\n'.format(
				pinfo.indent, tag, nstr, matTag, thick.value, fbulk.value, fDen.value, k1, k2, void, alpha, sopt1, sopt2)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)