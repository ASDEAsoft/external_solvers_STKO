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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLength_Element','ZeroLength Element')+'<br/>') +
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
		html_par('Dx Constraint') +
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
		html_par('Dx Constraint') +
		html_end()
		)
	at_3D.editable = False
	
	#-doRayleigh
	at_doRayleigh = MpcAttributeMetaData()
	at_doRayleigh.type = MpcAttributeType.Boolean
	at_doRayleigh.name = '-doRayleigh'
	at_doRayleigh.group = 'Group'
	at_doRayleigh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-doRayleigh')+'<br/>') +
		html_par('optional, default = 0') +
		html_par('rFlag = 0 NO RAYLEIGH DAMPING (default)') +
		html_par('rFlag = 1 include rayleigh damping') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLength_Element','ZeroLength Element')+'<br/>') +
		html_end()
		)
	
	# distributed
	at_distributed = MpcAttributeMetaData()
	at_distributed.type = MpcAttributeType.Boolean
	at_distributed.name = 'distributed'
	at_distributed.group = 'Group'
	at_distributed.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('distributed')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLength_Element','ZeroLength Element')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLength'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_doRayleigh)
	xom.addAttribute(at_distributed)
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	return xom

def __control(xobj, xobj_phys_prop):
	d = my_data()
	
	# get dimension from element property
	Dimension_at = xobj.getAttribute('Dimension')
	if(Dimension_at is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	d.Dimension = Dimension_at.string
	
	# check dimension compatibility between element and material
	if xobj_phys_prop.name != 'zeroLengthMaterial':
		raise Exception('Error: wrong physical property ({}) assigned to "zeroLength" element. Use "zeroLengthMaterial"'.format(xobj_phys_prop.name))
	DimensionMat_at = xobj_phys_prop.getAttribute('Dimension')
	if(DimensionMat_at is None):
		raise Exception('Error: cannot find "Dimension" attribute from physical property')
	DimensionMat = DimensionMat_at.string
	if(d.Dimension != DimensionMat ):
		raise Exception('Error: different dimension between "zeroLength" element and "zeroLengthMaterial"')
		
	# check whether zeroLengthMaterial is U-R (useful for 2D problems to tell if 3 dofs are UP or UR)
	UR_at = xobj_phys_prop.getAttribute('U-R (Displacement+Rotation)')
	if UR_at is None:
		raise Exception('Error: cannot find "U-R (Displacement+Rotation)" attribute from physical property')
	UR = UR_at.boolean
	
	if d.Dimension == '2D':
		d.ndm = 2
		if UR:
			d.ndf = [3, 2] # we allow 2D-U 2D-R and 2D-P (prefere user-defined)
		else:
			d.ndf = [2, 3] # we allow 2D-U 2D-R and 2D-P
	else:
		d.ndm = 3
		if UR:
			d.ndf = [6, 3, 4] # we allow 3D-U 3D-R and 3D-P (prefere user-defined)
		else:
			d.ndf = [3, 4, 6] # we allow 3D-U 3D-R and 3D-P
	return d

def getNodalSpatialDim(xobj, xobj_phys_prop):
	d = __control(xobj, xobj_phys_prop)
	return [(d.ndm,d.ndf),(d.ndm,d.ndf)]

def writeTcl(pinfo):
	
	#element zeroLength $eleTag $iNode $jNode -mat $matTag1 $matTag2 ... -dir $dir1 $dir2 ...<-doRayleigh $rFlag> <-orient $x1 $x2 $x3 $yp1 $yp2 $yp3>
	
	# get element and properties
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	tag = elem.id
	xobj = elem_prop.XObject
	
	# check number of nodes
	if (len(elem.nodes)!=2):
		raise Exception('Error: invalid number of nodes')
	
	# here we get the nodal NDF and NDM
	d = __control(xobj, phys_prop.XObject)
	
	# check dimension compatibility between element and material
	if phys_prop.XObject.name != 'zeroLengthMaterial':
		raise Exception('Error: wrong physical property ({}) assigned to "zeroLength" element. Use "zeroLengthMaterial"'.format(phys_prop.XObject.name))
	DimensionMat_at = phys_prop.XObject.getAttribute('Dimension')
	if(DimensionMat_at is None):
		raise Exception('Error: cannot find "Dimension" attribute from physical property')
	DimensionMat = DimensionMat_at.string
	if(d.Dimension != DimensionMat ):
		raise Exception('Error: different dimension between "zeroLength" element and "zeroLengthMaterial"')
	# check whether zeroLengthMaterial is U-R (useful for 2D problems to tell if 3 dofs are UP or UR)
	UR_at = phys_prop.XObject.getAttribute('U-R (Displacement+Rotation)')
	if UR_at is None:
		raise Exception('Error: cannot find "U-R (Displacement+Rotation)" attribute from physical property')
	UR = UR_at.boolean
	
	# write a comment
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
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
	
	# a first loop to make sure that both nodes have same ndm, and to store their ndf
	trial_ndf = [0, 0]
	# loop over the nodes of the elements and fill the node_ids_for_zero_length list
	# if necessary, build extra nodes
	for i in range(2):
		inode = elem.nodes[i]
		inode_id = inode.id
		node_ids_for_zero_length[i] = inode_id # start with this. change it later if necessary
		if not inode_id in pinfo.node_to_model_map:
			raise Exception('node {} of zero length element is not in the model map'.format(i))
		value = pinfo.node_to_model_map[inode_id]
		if ndm != value[0]: # ndm must be consistent
			raise Exception('node {} of {}D zero length element has incorrent ndm = {}'.format(i, ndm, value[0]))
		# ndf of the zero length may vary
		node_ndf = value[1]
		trial_ndf[i] = node_ndf
		# do a first check on the ndf
		if node_ndf < ndm:
			raise Exception('one of the zeroLength node has NDF < NDM (node = {}). This is not supported.'.format(inode_id))
	
	# switch off UR if necessary
	max_trial_ndf = max(trial_ndf[0], trial_ndf[1])
	if UR:
		if ndm == 2:
			if max_trial_ndf == 2: #cannot be < 2 due to previous checks
				UR = False # switch off UR
		elif ndm == 3:
			if max_trial_ndf < 6:
				UR = False # switch off UR
	
	# the dofs of the zero length element (can be 2 or 3 for 2D problems, or 3 or 6 for 3D problems)
	# both node must have the same ndm/ndf pair.
	ndf = 2
	if ndm == 2:
		if UR:
			ndf = 3
	else:
		if UR:
			ndf = 6
		else:
			ndf = 3
	
	# create extra nodes if the trial != ndf
	FMT = pinfo.get_double_formatter()
	def make_extra_node(the_loc_id):
		inode = elem.nodes[the_loc_id]
		pinfo.updateModelBuilder(ndm, ndf)
		extra_node_id = pinfo.next_node_id # get the next node id
		pinfo.next_node_id += 1 # increment the next node id
		node_ids_for_zero_length[the_loc_id] = extra_node_id
		pinfo.out_file.write('{}node {} {} {} {}\n'.format(pinfo.indent, extra_node_id, FMT(inode.x), FMT(inode.y), FMT(inode.z))) #write the extra node (coinciding with the ith-node)
		pinfo.out_file.write('{}equalDOF {} {} {}\n'.format(pinfo.indent, inode.id, extra_node_id, edof_agrs)) # link them with edof in common dofs
	if trial_ndf[0] != ndf:
		make_extra_node(0)
	if trial_ndf[1] != ndf:
		make_extra_node(1)
	
	# update model builder, the constructor of the zeroLength element looks for it
	pinfo.updateModelBuilder(ndm, ndf)
	
	# build the string of nodes
	nstr = ' '.join([str(node_id) for node_id in node_ids_for_zero_length])
	
	# get distributed flag
	distributed_at = xobj.getAttribute('distributed')
	if(distributed_at is None):
		raise Exception('Error: cannot find "distributed" attribute')
	distributed = distributed_at.boolean
	
	# build material and direction vectors
	mat_string = ''
	dir_string = ''
	if ndm == 2:
		if UR:
			max_num_mat = 3
		else:
			max_num_mat = 2
	else:
		if UR:
			max_num_mat = 6
		else:
			max_num_mat = 3
	for i in range(1, max_num_mat+1):
		dir_att_name = 'dir{}'.format(i)
		mat_tag_att_name = 'matTag{}'.format(i)
		dir_at = phys_prop.XObject.getAttribute(dir_att_name)
		if(dir_at is None):
			dir_att_name += '/{}'.format(DimensionMat)
			dir_at = phys_prop.XObject.getAttribute(dir_att_name)
			if(dir_at is None):
				raise Exception('Error: cannot find "{}" attribute'.format(dir_att_name))
		if dir_at.boolean:
			matTag_at = phys_prop.XObject.getAttribute(mat_tag_att_name)
			if(matTag_at is None):
				mat_tag_att_name += '/{}'.format(DimensionMat)
				matTag_at = phys_prop.XObject.getAttribute(mat_tag_att_name)
				if(matTag_at is None):
					raise Exception('Error: cannot find "{}" attribute'.format(mat_tag_att_name))
			mat_tag = matTag_at.index
			if mat_tag > 0:
				dir_string += ' {}'.format(i)
				mat_string += ' {}'.format(mat_tag)
			else: # if the id is not valid raise an error
				raise Exception("zeroLength Element Error: no material provided in direction {}".format(i))
				
	if not dir_string:
		raise Exception('Error: no "dir" selected')
	
	if distributed:
		# now we need to create a parallel material for each uniaxial material
		# we need to do so, because for distributed zero length we need to scale the material response (stress)
		# by the lumping factor.
		# recover original material ids from mat_string
		pinfo.out_file.write('\n{}# {}\n'.format(pinfo.indent, 'material parallel generated by zeroLength distributed'))
		orig_mat_ids = [int(item) for item in mat_string.strip(' ').split(' ') if item]
		# zero mat_string, needs to be updated with parallel material ids
		mat_string = ''
		for mat_id in orig_mat_ids:
			mat_tag_parallel = pinfo.next_physicalProperties_id # auto-generated parallel material
			str_tcl_mat_parallel = '{}uniaxialMaterial Parallel {} {} -factors {}\n'.format(pinfo.indent, mat_tag_parallel, mat_id, elem.lumpingFactor)
			pinfo.out_file.write(str_tcl_mat_parallel)
			mat_string += ' {}'.format(mat_tag_parallel)
			pinfo.next_physicalProperties_id = mat_tag_parallel + 1
	
	# optional paramters
	sopt = ''
	doRayleigh_at = xobj.getAttribute('-doRayleigh')
	if(doRayleigh_at is None):
		raise Exception('Error: cannot find "-doRayleigh" attribute')
	if doRayleigh_at.boolean:
		sopt += ' -doRayleigh 1'
	
	# orientation vectors
	vect_x=elem.orientation.computeOrientation().col(0)
	vect_y=elem.orientation.computeOrientation().col(1)
	
	# command
	str_tcl = '{}element zeroLength {} {} -mat{} -dir{}{} -orient {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, nstr, mat_string, dir_string, sopt, vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)