import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
from opensees.conditions.Constraints.mp.ASDEmbeddedNodeElementUtils import ASDEmbeddedNodeElementUtils as ebu
import numpy as np

def _geta(xobj, name):
	a = xobj.getAttribute(name)
	if a is None:
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return a

def makeXObjectMetaData():
	
	def mka(name, type, group='Default', descr=''):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthImplexContact Element')) +
			html_end()
			)
		return a
	
	dimension = mka('Dimension', MpcAttributeType.String, descr='choose between 2D and 3D')
	dimension.sourceType = MpcAttributeSourceType.List
	dimension.setSourceList(['2D', '3D'])
	dimension.setDefault('2D')
	
	d2 = mka('2D', MpcAttributeType.Boolean)
	d2.editable = False
	
	d3 = mka('3D', MpcAttributeType.Boolean)
	d3.editable = False
	
	kn = mka('Kn', MpcAttributeType.Real, descr='Penalty in normal direction')
	kt = mka('Kt', MpcAttributeType.Real, descr='Penalty in tangential direction')
	mu = mka('mu', MpcAttributeType.Real, descr='friction coefficient [mu = tan(phi) where phi is the internal friction angle]')
	
	implex = mka('Impl-ex', MpcAttributeType.Boolean, descr=(
		'Method of integration at the material level can be:<br>'
		'0: implicit, standard backward-euler integration scheme (default)<br>'
		'1: impl-ex, an implicit/explicit integration scheme')
		)
	distributed = mka('distributed', MpcAttributeType.Boolean, descr='Use this flag if you are using distributed springs on edges or surfaces.')
	
	orientation_type = mka('Orientation Type', MpcAttributeType.String, descr=(
		'By default, this element uses its local axes (local-Y for 2D problems or local-Z for 3D problems) as the contact direction.<br>'
		'When this element is assigned to a Node-to-Element interaction, you can choose whether the contact direction can be the standard one (From Local Axes), '
		'or automatically computed from the master element (From Element).<br>'
		'When the interaction is a Node-to-Node link, and the distance between the 2 nodes is not zero, you can choose to use the link direction as contact direction (From Link Direction)')
		)
	orientation_type.sourceType = MpcAttributeSourceType.List
	orientation_type.setSourceList(['From Local Axes', 'From Element', 'From Link Direction'])
	orientation_type.setDefault('From Local Axes')
	
	rigidgap = mka('Rigid Gap', MpcAttributeType.Boolean, descr=(
		'Use this flag when the distance between the 2 nodes is larger than Zero, and you want to consider this initial gap as rigid.<br>'
		'Note: the master node must have rotational DOFs')
		)
	
	# for cohesive zone modelling
	is_cohesive = mka('Is Cohesive', MpcAttributeType.Boolean, group='Cohesive Zone', 
		descr='Use this flag if the contact behavior has a tensile and cohesive strength')
	ft = mka('ft', MpcAttributeType.Real, group='Cohesive Zone', descr='Tensile strength')
	Gt = mka('Gt', MpcAttributeType.Real, group='Cohesive Zone', descr='Tensile fracture energy')
	c  = mka('c' , MpcAttributeType.Real, group='Cohesive Zone', descr='Cohesive strength')
	Gc = mka('Gc', MpcAttributeType.Real, group='Cohesive Zone', descr='Cohesive fracture energy')
	
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLengthContactASDimplex'
	xom.addAttribute(dimension)
	xom.addAttribute(d2)
	xom.addAttribute(d3)
	xom.addAttribute(kn)
	xom.addAttribute(kt)
	xom.addAttribute(mu)
	xom.addAttribute(implex)
	xom.addAttribute(distributed)
	xom.addAttribute(orientation_type)
	xom.addAttribute(rigidgap)
	xom.addAttribute(is_cohesive)
	xom.addAttribute(ft)
	xom.addAttribute(Gt)
	xom.addAttribute(c)
	xom.addAttribute(Gc)
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(dimension, d2)
	xom.setBooleanAutoExclusiveDependency(dimension, d3)
	
	# visibility
	xom.setVisibilityDependency(is_cohesive, ft)
	xom.setVisibilityDependency(is_cohesive, Gt)
	xom.setVisibilityDependency(is_cohesive, c)
	xom.setVisibilityDependency(is_cohesive, Gc)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	if _geta(xobj,'2D').boolean:
		ndm = 2
		ndf = [2, 3]
	else:
		ndm = 3
		ndf = [3, 4, 6]
	# this is from old version, available only for node-to-node link
	# return [(ndm,ndf),(ndm,ndf)]
	# This is for the new version, available also for node-to-element link
	# We also allowed for the output vector of this function
	# to be larger than the actual number of nodes, but not less!
	# at most the slave element can have 9 nodes (quadratic quad)!
	return [(ndm,ndf) for i in range(10)]

class _globals:
	Tedges = ((0,1), (1,2), (2,1))
	Vz = Math.vec3(0.0, 0.0, 1.0)
def _get_contact_vec_2d(Cnode, retained_nodes):
	dmin = 1.0e20
	j = -1
	dymin = None
	cpos = Cnode.position
	for i in range(3):
		iedge = _globals.Tedges[i]
		pa = retained_nodes[iedge[0]].position
		pb = retained_nodes[iedge[1]].position
		dx = (pb-pa).normalized()
		dz = _globals.Vz
		dy = dz.cross(dx).normalized()
		dd = abs(dy.dot(cpos-pa))
		if j < 0 or dd < dmin:
			dmin = dd
			j = i
			dymin = dy
	return -1.0*dymin
def _get_contact_vec_3d(retained_nodes):
	p1 = retained_nodes[0].position
	p2 = retained_nodes[1].position
	p3 = retained_nodes[2].position
	dx = (p2-p1).normalized()
	dy = (p3-p1).normalized()
	dz = dx.cross(dy).normalized()
	return dz

def writeTcl(pinfo):
	
	# element zeroLengthContactASDimplex $eleTag $sNode $mNode $Kn $Kt $mu <-orient $x1 $x2 $x3> <-intType $type>
	
	# standardized error
	def err(msg):
		return 'Error in "zeroLengthContactASDimplex":\n{}'.format(msg)
	
	# get element and properties
	elem = pinfo.elem
	elem_prop = pinfo.elem_prop
	tag = elem.id
	xobj = elem_prop.XObject
	
	# check element type
	# it can be a node-node link, a node-element link, or any 2-node elements.
	if len(elem.nodes) < 2:
		raise Exception(err('Invalid number of nodes: {}. It should be >= 2!'.format(len(elem.nodes))))
	if len(elem.nodes) > 2:
		# now it should be a node-element link
		if elem.geometryFamilyType() != MpcElementGeometryFamilyType.Link:
			raise Exception(err('Invalid element type: {}.'.format(elem.geometryFamilyType())))
		# at the moment we don't have an embedded node on edge...
		if len(elem.nodes) == 3:
			raise Exception(err('The master element should come from a surface'))
	
	# write a comment
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# formatter
	FMT = pinfo.get_double_formatter()
	
	# 2d/3d
	d2 = _geta(xobj, '2D').boolean
	
	# compute lumping factor
	# this is fine for 2-node links
	lumpingFactor = elem.lumpingFactor
	# but for node-elem we have to take it from the source element
	if len(elem.nodes) > 2:
		source_elem = elem.sourceElement
		lumpingFactor = source_elem.area()
	
	# parameters
	kn = _geta(xobj, 'Kn').real
	kt = _geta(xobj, 'Kt').real
	mu = _geta(xobj, 'mu').real
	is_distributed = _geta(xobj, 'distributed').boolean
	if is_distributed:
		kn *= lumpingFactor
		kt *= lumpingFactor
	
	# implex
	sopt = ''
	is_implex = _geta(xobj, 'Impl-ex').boolean
	if is_implex:
		sopt += '-intType 1'
	
	# compute nodes
	if len(elem.nodes) > 2:
		# the constrained node (actually the constrained node will be created later on on these same coords)
		Cnode = elem.nodes[-1]
		Cpos = np.asarray([[Cnode.x],[Cnode.y], [Cnode.z]])
		# find the embedding master element
		source_elem = elem.sourceElement
		if source_elem is None:
			raise Exception(err('Link element should have a valid source element'))
		family = source_elem.geometryFamilyType()
		# identify the closest triangle source_nodes
		if family == MpcElementGeometryFamilyType.Triangle:
			retained_nodes = [source_elem.nodes[i] for i in range(3)]
		elif family == MpcElementGeometryFamilyType.Quadrilateral:
			aux = []
			for sub in ebu.QSubs:
				trial_nodes = [source_elem.nodes[i] for i in sub]
				_, trial_distance = ebu.lct3(trial_nodes, Cpos)
				aux.append((trial_nodes, trial_distance))
			aux = sorted(aux, key = lambda variable: variable[1])
			retained_nodes = aux[0][0]
		else:
			# unsupported element type
			raise Exception(err(
				'The source element (master geometry) of the Link element {} '
				'has a wrong family type ({})'.format(elem.id, family)
				))
		# we need to create an auxiliary node for the embed constraint.
		if d2:
			pinfo.updateModelBuilder(2, 2)
			aux_coord = ' '.join([FMT(Cnode.x), FMT(Cnode.y)])
		else:
			pinfo.updateModelBuilder(3, 3)
			aux_coord = ' '.join([FMT(Cnode.x), FMT(Cnode.y), FMT(Cnode.z)])
		aux_node_id = pinfo.next_node_id
		pinfo.next_node_id += 1
		pinfo.out_file.write('{}node {} {}\n'.format(pinfo.indent, aux_node_id, aux_coord))
		# write the embed constraint element
		aux_elem_id = pinfo.next_elem_id
		pinfo.next_elem_id += 1
		pinfo.out_file.write(
					'{}element ASDEmbeddedNodeElement {}  {}   {}   -K {}\n'.format(
						pinfo.indent, aux_elem_id, aux_node_id, 
						' '.join(str(Rnode.id) for Rnode in retained_nodes),
						kn
						)
					)
		# nodes
		nodes = [aux_node_id, elem.nodes[-1].id]
	else:
		if _geta(xobj, 'Rigid Gap').boolean:
			# if it is a rigid gap we need an extra node at slave position
			# rigidly linked to the master node
			p1 = elem.nodes[0].position
			p2 = elem.nodes[1].position
			linkdir = p2-p1
			dist = linkdir.norm()
			if dist < 1.0e-16:
				# no need to create an extra node
				nodes = [node.id for node in elem.nodes]
			else:
				# make sure the master node has rotational dofs
				mid = elem.nodes[0].id
				mid_ndf = pinfo.node_to_model_map[mid][1]
				if d2:
					if mid_ndf != 3:
						raise Exception(err('With the "Rigid Gap" option the master node must have Rotational DOFs'))
				else:
					if mid_ndf != 6:
						raise Exception(err('With the "Rigid Gap" option the master node must have Rotational DOFs'))
				# create auxialiry node at same position as slave node p2
				# todo: allow user to input its distance <= p2-p1
				aux_node_id = pinfo.next_node_id
				pinfo.next_node_id += 1
				if d2:
					pinfo.updateModelBuilder(2, 3)
					pinfo.out_file.write('{}node {} {} {}\n'.format(pinfo.indent, aux_node_id, FMT(p2.x), FMT(p2.y)))
				else:
					pinfo.updateModelBuilder(3, 6)
					pinfo.out_file.write('{}node {} {} {} {}\n'.format(pinfo.indent, aux_node_id, FMT(p2.x), FMT(p2.y), FMT(p2.z)))
				# make the rigid link
				pinfo.out_file.write('{}rigidLink "beam" {} {}\n'.format(pinfo.indent, mid, aux_node_id))
				# nodes
				nodes = [aux_node_id, elem.nodes[1].id]
		else:
			# nodes
			nodes = [node.id for node in elem.nodes]
	
	# compute contact vector
	ori_type = _geta(xobj, 'Orientation Type').string
	if ori_type == 'From Element':
		if len(elem.nodes) <= 2:
			raise Exception(err('The "From Element" orientation type is allowed only with Node-to-Element interactions!.'))
		# get the contact vector from the master element
		# todo: get it from source geometry asap, it will be smooth
		if d2:
			cvec = _get_contact_vec_2d(Cnode, retained_nodes)
		else:
			cvec = _get_contact_vec_3d(retained_nodes)
	elif ori_type == 'From Link Direction':
		if len(elem.nodes) > 2:
			raise Exception(err('The "From Link Direction" orientation type is allowed only with Node-to-Node interactions!.'))
		p1 = elem.nodes[0].position
		p2 = elem.nodes[1].position
		cvec = p2-p1
		dist = cvec.norm()
		if dist < 1.0e-16:
			raise Exception(err('The "From Link Direction" orientation type is allowed only with a finite distance between the link nodes!.'))
		cvec.normalize()
	else:
		# get the contact vector from the default (or user-defined) local axes
		if d2:
			cvec = elem.orientation.computeOrientation().col(1)
		else:
			cvec = elem.orientation.computeOrientation().col(2)
	
	# write contact element
	pinfo.out_file.write('{}element zeroLengthContactASDimplex {} {} {} {} {} {} -orient {} {} {} {}\n'.format(
			pinfo.indent, tag, *nodes, kn, kt, mu, FMT(cvec.x), FMT(cvec.y), FMT(cvec.z), sopt))
	
	# cohesive
	is_cohesive = _geta(xobj, 'Is Cohesive').boolean
	if is_cohesive:
		ft = _geta(xobj, 'ft').real
		Gt = _geta(xobj, 'Gt').real
		c = _geta(xobj, 'c').real
		Gc = _geta(xobj, 'Gc').real
		fc_low = ft*1.0e-8
		fc_hi = ft*1.0e50
		if is_distributed:
			ft *= lumpingFactor
			Gt *= lumpingFactor
			c *= lumpingFactor
			Gc *= lumpingFactor
			fc_low *= lumpingFactor
			fc_hi *= lumpingFactor
		# write begin comment
		pinfo.out_file.write('{}# begin cohesive zone for zeroLengthContactASDimplex {}\n'.format(pinfo.indent, tag))
		# write materials
		def _expsoft(_k, _ft, _Gt, _fc, _p):
			# uniaxialMaterial plugin $tag pdm DamageTC1D -E $K -ft $ft -Gt $Gt -fc0 $fc -fcp $fc -fcr $fc -ep [expr $fc/$K*10.0] -Gc [expr $fc*1.0e50] -pdf_t $pf -implex 1 -autoRegularization 0
			_tag = pinfo.next_physicalProperties_id
			pinfo.out_file.write((
				'{}uniaxialMaterial plugin {} pdm DamageTC1D '
				'-E {} -ft {} -Gt {} -fc0 {} -fcp {} -fcr {} -ep {} -Gc {} -pdf_t {} -implex {} -autoRegularization 0\n'.format(
					pinfo.indent, _tag, FMT(_k), FMT(_ft), FMT(_Gt), FMT(_fc), FMT(_fc), FMT(_fc),
					FMT(_fc/_k*10.0), FMT(_fc*1.0e50), FMT(_p), int(is_implex))
				))
			pinfo.next_physicalProperties_id += 1
			return _tag
		# tensile and cohesive material
		_T = _expsoft(kn, ft, Gt, fc_hi, 0.0)
		_C = _expsoft(kt, c, Gc, fc_low, 0.0)
		# write elements
		def _celem(_n1, _n2, _mat, _dir, _x, _y):
			# positive tension-cohesion ZL
			_tag = pinfo.next_elem_id
			pinfo.out_file.write('{}element zeroLength {}  {} {}  -mat {} -dir {} -orient {} {} {}  {} {} {}\n'.format(
				pinfo.indent, _tag, _n1, _n2, _mat, _dir,
				FMT(_x.x), FMT(_x.y), FMT(_x.z),  FMT(_y.x), FMT(_y.y), FMT(_y.z)))
			pinfo.next_elem_id += 1
			return _tag
		if d2:
			# compute the tangential vectors
			vx = cvec.cross(Math.vec3(0.0, 0.0, 1.0)).normalized()
			# positive tension-cohesion ZL
			_C1 = _celem(nodes[0], nodes[1], '{} {}'.format(_C, _T), '1 2', vx, cvec)
			# negative tension-cohesion ZL
			_C2 = _celem(nodes[1], nodes[0], '{}'.format(_C), '1', vx, cvec)
		else:
			# compute the tangential vectors
			if abs(cvec.x) >= 0.99:
				vx = Math.vec3(0.0,1.0,0.0).cross(cvec).normalized()
				vy = cvec.cross(vx).normalized()
			else:
				vy = cvec.cross(Math.vec3(1.0, 0.0, 0.0)).normalized()
				vx = vy.cross(cvec).normalized()
			# positive tension-cohesion ZL
			_C1 = _celem(nodes[0], nodes[1], '{} {} {}'.format(_C, _C, _T), '1 2 3', vx, vy)
			# negative tension-cohesion ZL
			_C2 = _celem(nodes[1], nodes[0], '{} {}'.format(_C, _C), '1 2', vx, vy)
		# write end comment
		pinfo.out_file.write('{}# end cohesive zone for zeroLengthContactASDimplex {}\n'.format(pinfo.indent, tag))