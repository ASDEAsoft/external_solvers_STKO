import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Kn
	at_Kn = MpcAttributeMetaData()
	at_Kn.type = MpcAttributeType.Real
	at_Kn.name = 'Kn'
	at_Kn.group = 'Group'
	at_Kn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kn')+'<br/>') +
		html_par('Penalty in normal direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	# Kt
	at_Kt = MpcAttributeMetaData()
	at_Kt.type = MpcAttributeType.Real
	at_Kt.name = 'Kt'
	at_Kt.group = 'Group'
	at_Kt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kt')+'<br/>') +
		html_par('Penalty in tangential direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	# mu
	at_mu = MpcAttributeMetaData()
	at_mu.type = MpcAttributeType.Real
	at_mu.name = 'mu'
	at_mu.group = 'Group'
	at_mu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu')+'<br/>') +
		html_par('friction coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.Real
	at_c.name = 'c'
	at_c.group = 'Group'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') +
		html_par('cohesion') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	# dir
	at_dir = MpcAttributeMetaData()
	at_dir.type = MpcAttributeType.Integer
	at_dir.name = 'dir'
	at_dir.group = 'Group'
	at_dir.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir')+'<br/>') +
		html_par('Direction flag of the contact plane (3D), it can be:') +
		html_par('1 Out normal of the master plane pointing to +X direction') +
		html_par('2 Out normal of the master plane pointing to +Y direction') +
		html_par('3 Out normal of the master plane pointing to +Z direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	at_dir.sourceType = MpcAttributeSourceType.List
	at_dir.setSourceList([1, 2, 3])
	at_dir.setDefault(1)
	
	# distributed
	at_distributed = MpcAttributeMetaData()
	at_distributed.type = MpcAttributeType.Boolean
	at_distributed.name = 'distributed'
	at_distributed.group = 'Group'
	at_distributed.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('distributed')+'<br/>') +
		html_par('se this flag if you are using distributed springs on edges or surfaces.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLengthContact3D'
	xom.addAttribute(at_Kn)
	xom.addAttribute(at_Kt)
	xom.addAttribute(at_mu)
	xom.addAttribute(at_c)
	xom.addAttribute(at_dir)
	xom.addAttribute(at_distributed)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	# allow 3D with U UP or UR
	return [(3, [3,4,6]), (3, [3,4,6])]

def writeTcl(pinfo):
	
	# element zeroLengthContact3D $eleTag $sNode $mNode $Kn $Kt $mu $c $dir
	
	# get element and properties
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
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
	
	# the supported ndm = 3D
	ndm = 3
	# edof args to allow NDF > 3
	edof_agrs = '1 2 3'
	
	# in this list we put the nodal ids for the zero length element.
	# they will be the actual nodes of the element if they are compatible with the nmd/ndm of
	# the element (as defined by the user),
	# otherwise the ids of extra nodes (generated here) 
	node_ids_for_zero_length = [0, 0]
	# the dofs of the zero length element (can be 3, 4 or 6 for 3D problems)
	ndf = None 
	# loop over the nodes of the elements and fill the node_ids_for_zero_length list
	# if necessary, build extra nodes
	FMT = pinfo.get_double_formatter()
	for i in range(2):
		inode = elem.nodes[i]
		inode_id = inode.id
		if not inode_id in pinfo.node_to_model_map:
			raise Exception('node {} of zero length contact 3d is not in the model map'.format(i))
		value = pinfo.node_to_model_map[inode_id]
		if ndm != value[0]: # ndm must be consistent
			raise Exception('node {} of zero length contact 3d has incorrent ndm = {}'.format(i, value[0]))
		# ndf of the zero length may vary
		node_ndf = value[1]
		# take the ndf of the zero length element from the first node
		if ndf is None: 
			ndf = node_ndf
			if ndf == 4:
				ndf = 3 # if 3D-U-P -> make it 3D-U
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
	
	# use reverse iterator because in stko the first is the master node
	# while this command wants the slave node first
	nstr = ' '.join([str(node_id) for node_id in reversed(node_ids_for_zero_length)]) 
	
	# mandatory parameters
	Kn_at = xobj.getAttribute('Kn')
	if(Kn_at is None):
		raise Exception('Error: cannot find "Kn" attribute')
	Kn = Kn_at.real
	
	Kt_at = xobj.getAttribute('Kt')
	if(Kt_at is None):
		raise Exception('Error: cannot find "Kt" attribute')
	Kt = Kt_at.real
	
	mu_at = xobj.getAttribute('mu')
	if(mu_at is None):
		raise Exception('Error: cannot find "mu" attribute')
	mu = mu_at.real
	
	c_at = xobj.getAttribute('c')
	if(c_at is None):
		raise Exception('Error: cannot find "c" attribute')
	c = c_at.real
	
	dir_at = xobj.getAttribute('dir')
	if(dir_at is None):
		raise Exception('Error: cannot find "dir" attribute')
	dir = dir_at.integer
	
	distributed_at = xobj.getAttribute('distributed')
	if(distributed_at is None):
		raise Exception('Error: cannot find "distributed" attribute')
	distributed = distributed_at.boolean
	if distributed:
		Kn *= elem.lumpingFactor
		Kt *= elem.lumpingFactor
		c *= elem.lumpingFactor
	
	str_tcl = '{}element zeroLengthContact3D {} {} {} {} {} {} {}\n'.format(pinfo.indent, tag, nstr, Kn, Kt, mu, c, dir)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)