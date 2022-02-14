import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Group'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') +
		html_par('choose between 2D and 3D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Group'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_2D.editable = False
	
	# 3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Group'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# R1
	at_R1 = MpcAttributeMetaData()
	at_R1.type = MpcAttributeType.QuantityScalar
	at_R1.name = 'R1'
	at_R1.group = 'Group'
	at_R1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R1')+'<br/>') +
		html_par('Radius of inner bottom sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_R1.dimension = u.L
	
	# R2
	at_R2 = MpcAttributeMetaData()
	at_R2.type = MpcAttributeType.QuantityScalar
	at_R2.name = 'R2'
	at_R2.group = 'Group'
	at_R2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R2')+'<br/>') +
		html_par('Radius of inner top sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_R2.dimension = u.L
	
	# R3
	at_R3 = MpcAttributeMetaData()
	at_R3.type = MpcAttributeType.QuantityScalar
	at_R3.name = 'R3'
	at_R3.group = 'Group'
	at_R3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R3')+'<br/>') +
		html_par('Radius of outer bottom sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_R3.dimension = u.L
	
	# R4
	at_R4 = MpcAttributeMetaData()
	at_R4.type = MpcAttributeType.QuantityScalar
	at_R4.name = 'R4'
	at_R4.group = 'Group'
	at_R4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R4')+'<br/>') +
		html_par('Radius of outer top sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_R4.dimension = u.L
	
	# D1
	at_D1 = MpcAttributeMetaData()
	at_D1.type = MpcAttributeType.QuantityScalar
	at_D1.name = 'D1'
	at_D1.group = 'Group'
	at_D1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D1')+'<br/>') +
		html_par('Diameter of inner bottom sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_D1.dimension = u.L
	
	# D2
	at_D2 = MpcAttributeMetaData()
	at_D2.type = MpcAttributeType.QuantityScalar
	at_D2.name = 'D2'
	at_D2.group = 'Group'
	at_D2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D2')+'<br/>') +
		html_par('Diameter of inner top sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_D2.dimension = u.L
	
	# D3
	at_D3 = MpcAttributeMetaData()
	at_D3.type = MpcAttributeType.QuantityScalar
	at_D3.name = 'D3'
	at_D3.group = 'Group'
	at_D3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D3')+'<br/>') +
		html_par('Diameter of outer bottom sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_D3.dimension = u.L
	
	# D4
	at_D4 = MpcAttributeMetaData()
	at_D4.type = MpcAttributeType.QuantityScalar
	at_D4.name = 'D4'
	at_D4.group = 'Group'
	at_D4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D4')+'<br/>') +
		html_par('Diameter of outer top sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_D4.dimension = u.L
	
	# d1
	at_d1 = MpcAttributeMetaData()
	at_d1.type = MpcAttributeType.QuantityScalar
	at_d1.name = 'd1'
	at_d1.group = 'Group'
	at_d1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('d1')+'<br/>') +
		html_par('diameter of inner slider') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_d1.dimension = u.L
	
	# d2
	at_d2 = MpcAttributeMetaData()
	at_d2.type = MpcAttributeType.QuantityScalar
	at_d2.name = 'd2'
	at_d2.group = 'Group'
	at_d2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('d2')+'<br/>') +
		html_par('diameter of inner slider') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_d2.dimension = u.L
	
	# d3
	at_d3 = MpcAttributeMetaData()
	at_d3.type = MpcAttributeType.QuantityScalar
	at_d3.name = 'd3'
	at_d3.group = 'Group'
	at_d3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('d3')+'<br/>') +
		html_par('diameter of outer bottom slider') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_d3.dimension = u.L
	
	# d4
	at_d4 = MpcAttributeMetaData()
	at_d4.type = MpcAttributeType.QuantityScalar
	at_d4.name = 'd4'
	at_d4.group = 'Group'
	at_d4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('d4')+'<br/>') +
		html_par('diameter of outer top slider') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_d4.dimension = u.L
	
	# mu1
	at_mu1 = MpcAttributeMetaData()
	at_mu1.type = MpcAttributeType.Real
	at_mu1.name = 'mu1'
	at_mu1.group = 'Group'
	at_mu1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu1')+'<br/>') +
		html_par('friction coefficient of inner bottom sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	
	# mu2
	at_mu2 = MpcAttributeMetaData()
	at_mu2.type = MpcAttributeType.Real
	at_mu2.name = 'mu2'
	at_mu2.group = 'Group'
	at_mu2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu2')+'<br/>') +
		html_par('friction coefficient of inner top sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	
	# mu3
	at_mu3 = MpcAttributeMetaData()
	at_mu3.type = MpcAttributeType.Real
	at_mu3.name = 'mu3'
	at_mu3.group = 'Group'
	at_mu3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu3')+'<br/>') +
		html_par('friction coefficient of outer bottom sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	
	# mu4
	at_mu4 = MpcAttributeMetaData()
	at_mu4.type = MpcAttributeType.Real
	at_mu4.name = 'mu4'
	at_mu4.group = 'Group'
	at_mu4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu4')+'<br/>') +
		html_par('friction coefficient of outer top sliding surface') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	
	# h1
	at_h1 = MpcAttributeMetaData()
	at_h1.type = MpcAttributeType.QuantityScalar
	at_h1.name = 'h1'
	at_h1.group = 'Group'
	at_h1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h1')+'<br/>') +
		html_par('height from inner bottom sliding surface to center of bearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_h1.dimension = u.L
	
	# h2
	at_h2 = MpcAttributeMetaData()
	at_h2.type = MpcAttributeType.QuantityScalar
	at_h2.name = 'h2'
	at_h2.group = 'Group'
	at_h2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h2')+'<br/>') +
		html_par('height from inner top sliding surface to center of bearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_h2.dimension = u.L
	
	# h3
	at_h3 = MpcAttributeMetaData()
	at_h3.type = MpcAttributeType.QuantityScalar
	at_h3.name = 'h3'
	at_h3.group = 'Group'
	at_h3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h3')+'<br/>') +
		html_par('height from outer bottom sliding surface to center of bearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_h3.dimension = u.L
	
	# h4
	at_h4 = MpcAttributeMetaData()
	at_h4.type = MpcAttributeType.QuantityScalar
	at_h4.name = 'h4'
	at_h4.group = 'Group'
	at_h4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h4')+'<br/>') +
		html_par('height from inner top sliding surface to center of bearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_h4.dimension = u.L
	
	# H0
	at_H0 = MpcAttributeMetaData()
	at_H0.type = MpcAttributeType.QuantityScalar
	at_H0.name = 'H0'
	at_H0.group = 'Group'
	at_H0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('H0')+'<br/>') +
		html_par('total height of bearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_H0.dimension = u.L
	
	# use_colLoad
	at_use_colLoad = MpcAttributeMetaData()
	at_use_colLoad.type = MpcAttributeType.Boolean
	at_use_colLoad.name = 'use_colLoad'
	at_use_colLoad.group = 'Group'
	at_use_colLoad.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_colLoad')+'<br/>') +
		html_par('optional, stiffness of spring in vertical dirn (dof 2 if ndm= 2, dof 3 if ndm = 3) (default=1.0e15)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	
	# colLoad
	at_colLoad = MpcAttributeMetaData()
	at_colLoad.type = MpcAttributeType.QuantityScalar
	at_colLoad.name = 'colLoad'
	at_colLoad.group = 'Group'
	at_colLoad.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('colLoad')+'<br/>') +
		html_par('initial axial load on bearing (only used for first time step then load come from model)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_colLoad.dimension = u.L
	
	# use_K
	at_use_K = MpcAttributeMetaData()
	at_use_K.type = MpcAttributeType.Boolean
	at_use_K.name = 'use_K'
	at_use_K.group = 'Group'
	at_use_K.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_K')+'<br/>') +
		html_par('optional, stiffness of spring in vertical dirn (dof 2 if ndm= 2, dof 3 if ndm = 3) (default=1.0e15)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	
	# K
	at_K = MpcAttributeMetaData()
	at_K.type = MpcAttributeType.QuantityScalar
	at_K.name = 'K'
	at_K.group = 'Group'
	at_K.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K')+'<br/>') +
		html_par('optional, stiffness of spring in vertical dirn (dof 2 if ndm= 2, dof 3 if ndm = 3) (default=1.0e15)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Bearing_Element','Triple Friction Pendulum Bearing Element')+'<br/>') +
		html_end()
		)
	at_K.setDefault(1.0e15)
	at_K.dimension = u.F/u.L
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'TFPbearing'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_R1)
	xom.addAttribute(at_R2)
	xom.addAttribute(at_R3)
	xom.addAttribute(at_R4)
	xom.addAttribute(at_D1)
	xom.addAttribute(at_D2)
	xom.addAttribute(at_D3)
	xom.addAttribute(at_D4)
	xom.addAttribute(at_d1)
	xom.addAttribute(at_d2)
	xom.addAttribute(at_d3)
	xom.addAttribute(at_d4)
	xom.addAttribute(at_mu1)
	xom.addAttribute(at_mu2)
	xom.addAttribute(at_mu3)
	xom.addAttribute(at_mu4)
	xom.addAttribute(at_h1)
	xom.addAttribute(at_h2)
	xom.addAttribute(at_h3)
	xom.addAttribute(at_h4)
	xom.addAttribute(at_H0)
	xom.addAttribute(at_use_colLoad)
	xom.addAttribute(at_colLoad)
	xom.addAttribute(at_use_K)
	xom.addAttribute(at_K)
	
	
	# visibility dependencies
	
	# colLoad-dep
	xom.setVisibilityDependency(at_use_colLoad, at_colLoad)
	
	# K-dep
	xom.setVisibilityDependency(at_use_K, at_K)
	
	
	# auto-exclusive dependencies
	
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	Dimension2 = Dimension2_at.boolean
	
	if Dimension2:
		ndm = 2
		ndf = 3
	
	else:
		ndm = 3
		ndf = 6
	
	return [(ndm,ndf),(ndm,ndf)]

def writeTcl(pinfo):
	
	# TFPbearing tag? iNode? jNode? $R1 $R2 $R3 $R4 $do1 $do2 $do3 $do4 $din1 $din2 $din3 $din4 $mu1 $mu2 $mu3 $mu4 $h1 $h2 $h3 $h4 $H0 <$a> <$K>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	if Dimension2_at.boolean:
		ndm = 2
		ndf = 3
	else:
		ndm = 3
		ndf = 6
	
	pinfo.updateModelBuilder(ndm, ndf)
	
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
	
	if (len(node_vect)!=2):
		raise Exception('Error: invalid number of nodes')
	
	R1_at = xobj.getAttribute('R1')
	if(R1_at is None):
		raise Exception('Error: cannot find "R1" attribute')
	R1 = R1_at.quantityScalar.value
	
	R2_at = xobj.getAttribute('R2')
	if(R2_at is None):
		raise Exception('Error: cannot find "R2" attribute')
	R2 = R2_at.quantityScalar.value
	
	R3_at = xobj.getAttribute('R3')
	if(R3_at is None):
		raise Exception('Error: cannot find "R3" attribute')
	R3 = R3_at.quantityScalar.value
	
	R4_at = xobj.getAttribute('R4')
	if(R4_at is None):
		raise Exception('Error: cannot find "R4" attribute')
	R4 = R4_at.quantityScalar.value
	
	D1_at = xobj.getAttribute('D1')
	if(D1_at is None):
		raise Exception('Error: cannot find "D1" attribute')
	D1 = D1_at.quantityScalar.value

	D2_at = xobj.getAttribute('D2')
	if(D2_at is None):
		raise Exception('Error: cannot find "D2" attribute')
	D2 = D2_at.quantityScalar.value
	
	D3_at = xobj.getAttribute('D3')
	if(D3_at is None):
		raise Exception('Error: cannot find "D3" attribute')
	D3 = D3_at.quantityScalar.value
	
	D4_at = xobj.getAttribute('D4')
	if(D4_at is None):
		raise Exception('Error: cannot find "D4" attribute')
	D4 = D4_at.quantityScalar.value
	
	d1_at = xobj.getAttribute('d1')
	if(d1_at is None):
		raise Exception('Error: cannot find "d1" attribute')
	d1 = d1_at.quantityScalar.value

	d2_at = xobj.getAttribute('d2')
	if(d2_at is None):
		raise Exception('Error: cannot find "d2" attribute')
	d2 = d2_at.quantityScalar.value
	
	d3_at = xobj.getAttribute('d3')
	if(d3_at is None):
		raise Exception('Error: cannot find "d3" attribute')
	d3 = d3_at.quantityScalar.value
	
	d4_at = xobj.getAttribute('d4')
	if(d4_at is None):
		raise Exception('Error: cannot find "d4" attribute')
	d4 = d4_at.quantityScalar.value
	
	mu1_at = xobj.getAttribute('mu1')
	if(mu1_at is None):
		raise Exception('Error: cannot finmu "mu1" attribute')
	mu1 = mu1_at.real

	mu2_at = xobj.getAttribute('mu2')
	if(mu2_at is None):
		raise Exception('Error: cannot finmu "mu2" attribute')
	mu2 = mu2_at.real
	
	mu3_at = xobj.getAttribute('mu3')
	if(mu3_at is None):
		raise Exception('Error: cannot finmu "mu3" attribute')
	mu3 = mu3_at.real
	
	mu4_at = xobj.getAttribute('mu4')
	if(mu4_at is None):
		raise Exception('Error: cannot finmu "mu4" attribute')
	mu4 = mu4_at.real
	
	h1_at = xobj.getAttribute('h1')
	if(h1_at is None):
		raise Exception('Error: cannot finh "h1" attribute')
	h1 = h1_at.quantityScalar.value

	h2_at = xobj.getAttribute('h2')
	if(h2_at is None):
		raise Exception('Error: cannot finh "h2" attribute')
	h2 = h2_at.quantityScalar.value
	
	h3_at = xobj.getAttribute('h3')
	if(h3_at is None):
		raise Exception('Error: cannot finh "h3" attribute')
	h3 = h3_at.quantityScalar.value
	
	h4_at = xobj.getAttribute('h4')
	if(h4_at is None):
		raise Exception('Error: cannot finh "h4" attribute')
	h4 = h4_at.quantityScalar.value
	
	H0_at = xobj.getAttribute('H0')
	if(H0_at is None):
		raise Exception('Error: cannot finh "H0" attribute')
	H0 = H0_at.quantityScalar.value
	
	
	# optional paramters
	sopt = ''
	
	use_colLoad_at = xobj.getAttribute('use_colLoad')
	if(use_colLoad_at is None):
		raise Exception('Error: cannot find "use_colLoad" attribute')
	use_colLoad = use_colLoad_at.boolean
	if use_colLoad:
		colLoad_at = xobj.getAttribute('colLoad')
		if(colLoad_at is None):
			raise Exception('Error: cannot find "colLoad" attribute')
		colLoad = colLoad_at.quantityScalar
		
		sopt += ' {}'.format(colLoad.value)
	
	use_K_at = xobj.getAttribute('use_K')
	if(use_K_at is None):
		raise Exception('Error: cannot find "use_K" attribute')
	use_K = use_K_at.boolean
	if use_K:
		K_at = xobj.getAttribute('K')
		if(K_at is None):
			raise Exception('Error: cannot find "K" attribute')
		K = K_at.quantityScalar
		
		sopt += ' {}'.format(K.value)
	
	
	str_tcl = '{}element TFPbearing {}{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}{}\n'.format(
				pinfo.indent, tag, nstr, R1, R2, R3, R4, D1, D2, D3, D4,
				d1, d2, d3, d4, mu1, mu2, mu3, mu4, h1, h2, h3, h4, H0, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)