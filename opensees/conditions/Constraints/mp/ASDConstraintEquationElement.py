import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import math
import os

def _err(id, msg):
	return 'Error in "ASDConstraintEquationElement" at "Condition {}":\n{}'.format(id, msg)
def _geta(xobj, name):
	a = xobj.getAttribute(name)
	if a is None:
		raise Exception(_err(xobj.parent.componentId, 'cannot find "{}" attribute'.format(name)))
	return a

def makeXObjectMetaData():
	
	# TODO: change the URL when the documentation for ASDConstraintEquationElement is ready
	dp = 'https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/ASDEmbeddedNodeElement.html'
	
	def mka(name, type, group='Default', description='', defval=None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(description) +
			html_par(html_href(dp,'ASDConstraintEquationElement')+'<br/>') +
			html_end()
			)
		if defval:
			a.setDefault(defval)
		return a
	
	# create all attributes
	dimension = mka('Dimension', MpcAttributeType.String, defval='3D', description="no description")
	dimension.sourceType = MpcAttributeSourceType.List
	dimension.setSourceList(['2D', '3D'])
	
	modeltype = mka('ModelType', MpcAttributeType.String, defval='U (Displacement)')
	modeltype.sourceType = MpcAttributeSourceType.List
	modeltype.setSourceList(['U (Displacement)', 'U-P (Displacement+Pressure)', 'U-R (Displacement+Rotation)'])
	
	K = mka('K (Penalty)', MpcAttributeType.QuantityScalar, description='A penalty stiffness value used to enforce the constraint', defval=1.0e12)
	K.dimension = u.F/u.L
	Cdof = mka('Constrained DOF', MpcAttributeType.Integer, description='The 1-based DOF of the constrained node')
	Rdofs = mka('Retained DOFs', MpcAttributeType.QuantityVector, description='The 1-based list of DOFs for each retained node')
	Rfact = mka('Retained Factors', MpcAttributeType.QuantityVector, description='The factors for each one of the retained DOFs')
	
	# add attributes to the XObject
	xom = MpcXObjectMetaData()
	xom.name = 'ASDConstraintEquationElement'
	xom.addAttribute(dimension)
	xom.addAttribute(modeltype)
	xom.addAttribute(K)
	xom.addAttribute(Cdof)
	xom.addAttribute(Rdofs)
	xom.addAttribute(Rfact)
	
	return xom

def makeConditionRepresentationData(xobj):
	'''
	Create the condition representation data for STKO.
	Here we want a simple point-representation in global
	coordinate system, that can be applied only on interactions.
	'''
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Points
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array()
	d.on_vertices = False
	d.on_edges = False
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = True
	
	return d

def getRequestedNodalSpatialDim(xobj):
	'''
	similar to the def getNodalSpatialDim(xobj, xobj_phys_prop) method in element properties,
	but with a conceptual difference. getNodalSpatialDim returns a list of (ndm,ndf) pair
	whose length is equal to the number of nodes for that element, following the local
	numbering of each element.
	Here instead we return a map, where the key is the ID of the (only) nodes where
	the condition requires a specific dimension (here for example the master node)
	'''
	
	# find proper NDM and NDF
	_2D = _geta(xobj, 'Dimension').string == '2D'
	_UP = _geta(xobj, 'ModelType').string == 'U-P (Displacement+Pressure)'
	_UR = _geta(xobj, 'ModelType').string == 'U-R (Displacement+Rotation)'
	if _2D:
		ndm = 2
		if _UP or _UR:
			ndf = [3, 2] # user-defined goes first
		else:
			ndf = [2, 3] # standard
		
	else:
		ndm = 3
		if _UP:
			ndf = [4, 3, 6] # user-defined goes first
		elif _UR:
			ndf = [6, 3, 4] # user-defined goes first
		else:
			ndf = [3, 4, 6] # standard
	
	requested_node_dim_map = {}
	condition = xobj.parent
	all_inter = condition.assignment.interactions
	doc = App.caeDocument()
	for inter in all_inter:
		moi = doc.mesh.getMeshedInteraction(inter.id)
		for elem in moi.elements:
			for node in elem.nodes:
				requested_node_dim_map[node.id] = (ndm, ndf)
	return requested_node_dim_map

def writeTcl_mpConstraints(pinfo):
	# element ASDConstraintEquationElement $tag $K $cNode $cDof <$rNode1 $rDof1 $rFact1 ... $rNodeN $rDofN $rFactN>
	
	# the XObject
	xobj = pinfo.condition.XObject
	
	# the document
	doc = App.caeDocument()
	if(doc is None):
		raise Exception(_err(pinfo.condition.id, 'null cae document'))
	
	# get all interactions with this condition
	all_inter = pinfo.condition.assignment.interactions
	if len(all_inter) == 0:
		return
	
	# check partition
	is_partitioned = (pinfo.process_count > 1)
	
	# get XObject's arguments
	K = _geta(xobj, 'K (Penalty)').quantityScalar.value
	Cdof = _geta(xobj, 'Constrained DOF').integer
	Rdofs = _geta(xobj, 'Retained DOFs').quantityVector.value
	Rfact = _geta(xobj, 'Retained Factors').quantityVector.value
	
	# do checks
	if len(Rdofs) != len(Rfact):
		raise Exception(_err(pinfo.condition.id,
			'The length of "Retained DOFs" ({}) should match the length of "Retained Factors" ({})'.format(len(Rdofs), len(Rfact))
			))
	
	def internal(process_id, process_block_count):
		# first-done flag for partitioned process
		first_done = False
		# process each interaction
		for inter in all_inter:
			# do some checks about the interaction type
			if inter.type != MpcInteractionType.GeneralLink:
				raise Exception(_err(pinfo.condition.id, 
					'Interaction "{}" [{}] should be a GeneralLink interaction, not {}.'.format(
						inter.name, inter.id, inter.type)
						))
			# process all link elements
			moi = doc.mesh.getMeshedInteraction(inter.id)
			# there should be only one element per interaction for a GeneralLink... but a loop
			# is more generic for future implementations
			for elem in moi.elements:
				# skip elements not on this partition
				if is_partitioned:
					if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
						continue
				# number of retained nodes and constrained nodes
				NN = len(elem.nodes)
				NM = elem.numberOfMasterNodes()
				NS = NN - NM
				if NS != 1:
					raise Exception(_err(pinfo.condition.id, 'Link element should have only 1 constrained node'))
				# get the constrained node
				Cnode = elem.nodes[-1].id
				# get the retained nodes
				Rnodes = [elem.nodes[i].id for i in range(NM)]
				# check consistency
				if len(Rnodes) != len(Rdofs):
					raise Exception(_err(
						'The length of "Retained DOFs" ({}) and "Retained Factors" ({}) should match the number of Master nodes ({})'.format(len(Rdofs), len(Rfact), NM)
						))
				# open process if-statement block
				block_indent = ''
				if is_partitioned:
					block_indent = pinfo.tabIndent
					if not first_done:
						if process_block_count == 0:
							pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
						else:
							pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
						first_done = True
				# we cannot use the elem.id as the id of this new element, as it is used as a condition
				# in STKO, so the user can apply multiple conditions to the same link!
				new_elem_id = pinfo.next_elem_id
				pinfo.next_elem_id += 1
				# map it (not mandatory)
				if elem.id in pinfo.auto_generated_element_data_map:
					auto_gen_data = pinfo.auto_generated_element_data_map[elem.id]
				else:
					auto_gen_data = tclin.auto_generated_element_data()
					pinfo.auto_generated_element_data_map[elem.id] = auto_gen_data
				auto_gen_data.elements.append(new_elem_id)
				auto_gen_data.elements_connectivity.append(
					[(elem.nodes[i].id, elem.nodes[i].x, elem.nodes[i].y, elem.nodes[i].z) for i in range(len(elem.nodes))]
					)
				# write this element
				pinfo.out_file.write(
					'{}{}element ASDConstraintEquationElement {}   {}   {} {}   {}\n'.format(
						pinfo.indent, block_indent, new_elem_id, K, Cnode, Cdof, 
						'   '.join( '{} {} {}'.format(Rnodes[i], int(Rdofs[i]), Rfact[i]) for i in range(NM) )
						)
					)
		
	# write description
	description = '\n{}# element ASDConstraintEquationElement $tag $K $cNode $cDof <$rNode1 $rDof1 $rFact1 ... $rNodeN $rDofN $rFactN>\n'.format(pinfo.indent)
	pinfo.out_file.write(description)
	
	# call the internal function based on partitions
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			pinfo.setProcessId(process_id)
			process_block_count = internal(process_id, process_block_count)
	else:
		internal(0, 0)