import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# nDivide
	at_nDivide = MpcAttributeMetaData()
	at_nDivide.type = MpcAttributeType.Integer
	at_nDivide.name = 'nDivide'
	at_nDivide.group = 'Group'
	at_nDivide.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nDivide')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# shape
	at_shape = MpcAttributeMetaData()
	at_shape.type = MpcAttributeType.Integer
	at_shape.name = 'shape'
	at_shape.group = '-shape'
	at_shape.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('shape')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# size
	at_size = MpcAttributeMetaData()
	at_size.type = MpcAttributeType.Real
	at_size.name = 'size'
	at_size.group = '-size'
	at_size.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('size')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# -lambda
	at_use_lambda = MpcAttributeMetaData()
	at_use_lambda.type = MpcAttributeType.Boolean
	at_use_lambda.name = '-lambda'
	at_use_lambda.group = 'Optional parameters'
	at_use_lambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-lambda')+'<br/>') +
		html_par('optional, default = -1.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# lambda
	at_lambda = MpcAttributeMetaData()
	at_lambda.type = MpcAttributeType.Real
	at_lambda.name = 'lambda'
	at_lambda.group = '-lambda'
	at_lambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lambda')+'<br/>') +
		html_par('optional, default = -1.0') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_lambda.setDefault(-1.0)
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Group'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# -mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.Boolean
	at_mass.name = '-mass'
	at_mass.group = 'Optional parameters'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mass')+'<br/>') +
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.QuantityScalar
	at_m.name = 'm'
	at_m.group = '-mass'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') +
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_m.setDefault(0.0)
	#at_m.dimension = u.M
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'multipleNormalSpring'
	xom.addAttribute(at_nDivide)
	xom.addAttribute(at_shape)
	xom.addAttribute(at_size)
	xom.addAttribute(at_use_lambda)
	xom.addAttribute(at_lambda)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	
	
	# visibility dependencies
	
	# lambda-dep
	xom.setVisibilityDependency(at_use_lambda, at_lambda)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]	#[(ndm, ndf)...]

def writeTcl(pinfo):
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	pinfo.updateModelBuilder(3,6)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=2): 													#CONTROLLARE: elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral or 
		raise Exception('Error: invalid type of element or number of nodes')	#CONTROLLARE IL FamilyType
	
	
	nDivide_at = xobj.getAttribute('nDivide')
	if(nDivide_at is None):
		raise Exception('Error: cannot find "nDivide" attribute')
	nDivide = nDivide_at.integer
	
	shape_at = xobj.getAttribute('shape')
	if(shape_at is None):
		raise Exception('Error: cannot find "shape" attribute')
	shape = shape_at.integer
	
	size_at = xobj.getAttribute('size')
	if(size_at is None):
		raise Exception('Error: cannot find "size" attribute')
	size = size_at.real
	
	# optional parameters
	sopt = ''
	
	use_lambda_at = xobj.getAttribute('-lambda')
	if(use_lambda_at is None):
		raise Exception('Error: cannot find "-lambda" attribute')
	if use_lambda_at.boolean:
		lambda_at = xobj.getAttribute('lambda')
		if(lambda_at is None):
			raise Exception('Error: cannot find "lambda" attribute')
		lambda_ = lambda_at.real
		
		sopt += ' -lambda {}'.format(lambda_)
	
	'''
	-orient SARA' INSERITO ATTRAVERSO UNA FUNZIONE
	'''
	orient_at = xobj.getAttribute('-orient')
	if(orient_at is None):
		raise Exception('Error: cannot find "-orient" attribute')
	if orient_at.boolean:
		sopt += ' -orient 1.0 0.0 0.0 0.0 1.0 0.0'		#vectorX = [1.0, 0.0, 0.0]; vectorY = [0.0, 1.0, 0.0]
	
	m_at = xobj.getAttribute('m')
	if(m_at is None):
		raise Exception('Error: cannot find "m" attribute')
	m = m_at.boolean
	if m:
		sopt += ' -mass {}'.format(m)
	
	# element multipleNormalSpring eleTag? iNode? jNode? nDivide? -mat matTag? -shape shape? -size size? <-lambda lambda?> <-orient <x1? x2? x3?> yp1? yp2? yp3?> <-mass m?>\n
	
	str_tcl = '{}element multipleNormalSpring {}{} {} -mat {} -shape {} -size {}{}\n'.format(pinfo.indent, tag, nstr, nDivide, matTag, shape, size, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)