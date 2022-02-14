import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

class my_data:
	def __init__(self):
		# attributes will be set in the __control method
		pass

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
		html_end()
		)
	at_3D.editable = False
	
	# kr
	at_kr = MpcAttributeMetaData()
	at_kr.type = MpcAttributeType.Real
	at_kr.name = 'kr'
	at_kr.group = 'Group'
	at_kr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kr')+'<br/>') +
		html_end()
		)
	
	# radius
	at_radius = MpcAttributeMetaData()
	at_radius.type = MpcAttributeType.Real
	at_radius.name = 'radius'
	at_radius.group = 'Group'
	at_radius.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('radius')+'<br/>') +
		html_end()
		)

	# theta0
	at_theta0 = MpcAttributeMetaData()
	at_theta0.type = MpcAttributeType.Real
	at_theta0.name = 'theta0'
	at_theta0.group = 'Group'
	at_theta0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('theta0')+'<br/>') +
		html_end()
		)

	# kappa
	at_kappa = MpcAttributeMetaData()
	at_kappa.type = MpcAttributeType.Real
	at_kappa.name = 'kappa'
	at_kappa.group = 'Group'
	at_kappa.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kappa')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLengthRocking'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_kr)
	xom.addAttribute(at_radius)
	xom.addAttribute(at_theta0)
	xom.addAttribute(at_kappa)
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	return xom

def __control(xobj):
	d = my_data()
	Dimension_at = xobj.getAttribute('Dimension')
	if(Dimension_at is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	d.Dimension = Dimension_at.string
	if d.Dimension == '2D':
		d.ndm = 2
		d.ndf = [2, 3] # we allow 2D-U 2D-R and 2D-P
	else:
		d.ndm = 3
		d.ndf = [3, 4, 6] # we allow 3D-U 3D-R and 3D-P
	return d

def getNodalSpatialDim(xobj):
	d = __control(xobj)
	return [(d.ndm,d.ndf),(d.ndm,d.ndf)]

def writeTcl(pinfo):

	# element zeroLengthRocking eleTag? iNode? jNode? kr? radius? theta0? kappa? <-orient x1? x2? x3? y1? y2? y3?>
	# get element and properties
	elem = pinfo.elem
	elem_prop = pinfo.elem_prop
	tag = elem.id
	xobj = elem_prop.XObject

	# check number of nodes
	if (len(elem.nodes)!=2):
		raise Exception('Error: invalid number of nodes')

	# write a comment
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# here we get the nodal NDF and NDM
	d = __control(xobj)

	# get ndm and edof_agrs based on 2D or 3D problems
	if d.Dimension == '2D':
		# 2D case
		ndm = 2
		edof_agrs = '1 2'
	else:
		# 3D case
		ndm = 3
		edof_agrs = '1 2 3'

	# in this list we put the nodal ids for the zero length element.
	# they will be the actual nodes of the element if they are compatible with the nmd/ndm of
	# the element (as defined by the user),
	# otherwise the ids of extra nodes (generated here) 
	node_ids_for_zero_length = [0, 0]
	# the dofs of the zero length element (can be 2 or 3 for 2D problems, or 3, 4 or 6 for 3D problems)
	ndf = None 
	# loop over the nodes of the elements and fill the node_ids_for_zero_length list
	# if necessary, build extra nodes
	FMT = pinfo.get_double_formatter()
	for i in range(2):
		inode = elem.nodes[i]
		inode_id = inode.id
		if not inode_id in pinfo.node_to_model_map:
			raise Exception('node {} of zero length element is not in the model map'.format(i))
		value = pinfo.node_to_model_map[inode_id]
		if ndm != value[0]: # ndm must be consistent
			raise Exception('node {} of {}D zero length element has incorrent ndm = {}'.format(i, ndm, value[0]))
		# ndf of the zero length may vary
		node_ndf = value[1]
		# take the ndf of the zero length element from the first node
		if ndf is None: 
			ndf = node_ndf
			if ndf == 4:
				ndf = 3 # if 3D-U-P -> make it 3D-U
			if ndf == 3:
				if ndm == 2:
					if node_ndf == 2:
						ndf = 2
		# compare the ndf of the ith node with the ndf of the element
		if node_ndf != ndf:
			# if the element and ith-node ndf's do not match
			# build and extra node and link it with the ith-node via edof constraint
			pinfo.updateModelBuilder(ndm, ndf)
			extra_node_id = pinfo.next_node_id # get the next node id
			pinfo.next_node_id += 1 # increment the next node id
			node_ids_for_zero_length[i] = extra_node_id
			pinfo.out_file.write('{}node {} {} {} {}\n'.format(pinfo.indent, extra_node_id, FMT(inode.x), FMT(inode.y), FMT(inode.z))) #write the extra node (coinciding with the ith-node)
			pinfo.out_file.write('{}equalDOF {} {} {}\n'.format(pinfo.indent, extra_node_id, inode_id, edof_agrs)) # link them with edof in common dofs
		else:
			# just use the ith-node id
			node_ids_for_zero_length[i] = inode_id
	
	# update model builder, the constructor of the zeroLength element looks for it
	pinfo.updateModelBuilder(ndm, ndf)
	
	# build the string of nodes
	nstr = ' '.join([str(node_id) for node_id in node_ids_for_zero_length])

	# mandatory parameters
	kr_at = xobj.getAttribute('kr')
	if(kr_at is None):
		raise Exception('Error: cannot find "kr" attribute')
	kr = kr_at.real

	radius_at = xobj.getAttribute('radius')
	if(radius_at is None):
		raise Exception('Error: cannot find "radius" attribute')
	radius = radius_at.real

	theta0_at = xobj.getAttribute('theta0')
	if(theta0_at is None):
		raise Exception('Error: cannot find "theta0" attribute')
	theta0 = theta0_at.real

	kappa_at = xobj.getAttribute('kappa')
	if(kappa_at is None):
		raise Exception('Error: cannot find "kappa" attribute')
	kappa = kappa_at.real

	# orientation vectors
	vect_x=elem.orientation.computeOrientation().col(0)
	vect_y=elem.orientation.computeOrientation().col(1)

	# element zeroLengthRocking eleTag? iNode? jNode? kr? radius? theta0? kappa? <-orient x1? x2? x3? y1? y2? y3?>
	str_tcl = '{}element zeroLengthRocking {} {} {} {} {} {} -orient {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, nstr, kr, radius, theta0, kappa, vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	# now write the string into the file
	pinfo.out_file.write(str_tcl)