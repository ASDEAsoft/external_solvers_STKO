import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.utils.tcl_input as tclin
import math
from opensees.conditions.Constraints.mp.ASDEmbeddedNodeElementUtils import ASDEmbeddedNodeElementUtils as ebu
import os

def _err(id, msg):
	return 'Error in "ASDEmbeddedNodeElement" at "Condition {}":\n{}'.format(id, msg)
def _geta(xobj, name):
	a = xobj.getAttribute(name)
	if a is None:
		raise Exception(_err(xobj.parent.componentId, 'cannot find "{}" attribute'.format(name)))
	return a

def makeXObjectMetaData():
	
	dp = 'https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/ASDEmbeddedNodeElement.html'
	
	# stiffness
	K = MpcAttributeMetaData()
	K.type = MpcAttributeType.QuantityScalar
	K.name = 'K (Penalty)'
	K.group = 'Default'
	K.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K (Penalty)')+'<br/>') + 
		html_par(
			"A penalty stiffness value used to enforce the constraint.<br/>"
			"This value should be large enough to enforce the constraint, but not too large, otherwise the system may become ill-conditioned.<br/>"
			"It is possible to estimate this value to be approximately 3 or 4 orders of magnitude greater than the Young's modulus of the embedding material.<br/>"
			"Also note that this value will be automatically scaled by the volume of the embedding element, so it should be independent from the element size."
			) +
		html_par(html_href(dp,'ASDEmbeddedNodeElement')+'<br/>') +
		html_end()
		)
	K.dimension = u.F/u.L/u.L
	K.setDefault(1.0e12)
	
	# rotation flag
	rot = MpcAttributeMetaData()
	rot.type = MpcAttributeType.Boolean
	rot.name = 'Constrain Rotations'
	rot.group = 'Default'
	rot.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Constrain Rotations')+'<br/>') + 
		html_par(
			"If True, the constrained-node's rotational DOFs will be constrained "
			"to be equal to the skew symmetric part of the retained-nodes' displacement gradient.<br/>"
			"Note that this flag will be discarded if the constrained node has no rotational DOFs."
			) +
		html_par(html_href(dp,'ASDEmbeddedNodeElement')+'<br/>') +
		html_end()
		)
	rot.setDefault(True)
	
	# rotation flag
	pressure = MpcAttributeMetaData()
	pressure.type = MpcAttributeType.Boolean
	pressure.name = 'Constrain Pressure'
	pressure.group = 'Default'
	pressure.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Constrain Pressure')+'<br/>') + 
		html_par(
			"If True, the constrained-node's pressure DOF will be constrained "
			"to be equal to the weighted average of the retained-nodes's pressure DOF.<br/>"
			"Note that this flag will be discarded if at least 1 node (either retained or constrained) is not U-P."
			) +
		html_par(html_href(dp,'ASDEmbeddedNodeElement')+'<br/>') +
		html_end()
		)
	pressure.setDefault(False)
	
	# -KP
	use_KP = MpcAttributeMetaData()
	use_KP.type = MpcAttributeType.Boolean
	use_KP.name = '-KP'
	use_KP.group = 'Default'
	use_KP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-KP')+'<br/>') + 
		html_par(
			"If True, the user can define a custom value for the KP stiffness parameter for pressure DOF. Otherwise it will be equal to K"
			) +
		html_par(html_href(dp,'ASDEmbeddedNodeElement')+'<br/>') +
		html_end()
		)
	use_KP.setDefault(False)
	
	# stiffness
	KP = MpcAttributeMetaData()
	KP.type = MpcAttributeType.QuantityScalar
	KP.name = 'KP (Penalty)'
	KP.group = 'Default'
	KP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('KP (Penalty)')+'<br/>') + 
		html_par(
			"A penalty stiffness value used to enforce the constraint for Pressure DOF.<br/>"
			) +
		html_par(html_href(dp,'ASDEmbeddedNodeElement')+'<br/>') +
		html_end()
		)
	KP.dimension = u.F/u.L/u.L
	KP.setDefault(1.0e12)
	
	# ignore outside
	son = MpcAttributeMetaData()
	son.type = MpcAttributeType.Boolean
	son.name = 'Ignore Nodes Outside'
	son.group = 'Default'
	son.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-rot')+'<br/>') + 
		html_par(
			"If True, all the nodes that are outside of the embedding domain will be skipped without generating any error.<br/>"
			"If, instead, you want to make sure that all nodes are properly constrained, you can turn this flag Off.<br/>"
			"In this case, when a node is outside the embedding domain of more than 1 % of the embedding domain size, and error will be generated."
			) +
		html_par(html_href(dp,'ASDEmbeddedNodeElement')+'<br/>') +
		html_end()
		)
	son.setDefault(True)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDEmbeddedNodeElement'
	xom.addAttribute(K)
	xom.addAttribute(rot)
	xom.addAttribute(pressure)
	xom.addAttribute(use_KP)
	xom.addAttribute(KP)
	xom.addAttribute(son)
	
	return xom

def makeConditionRepresentationData(xobj):
	'''
	Create the condition representation data for STKO.
	Here we want an simple points (vector) representation in global
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

def onEditBegin(editor, xobj):
	if _geta(xobj, 'Constrain Rotations').boolean:
		_geta(xobj, 'Constrain Pressure').boolean = False
		_geta(xobj, '-KP').visible = False
		_geta(xobj, 'KP (Penalty)').visible = False
	if _geta(xobj, 'Constrain Pressure').boolean:
		_geta(xobj, 'Constrain Rotations').boolean = False
		_geta(xobj, '-KP').visible = True
		_geta(xobj, 'KP (Penalty)').visible = _geta(xobj, '-KP').boolean
	else:
		_geta(xobj, '-KP').visible = False
		_geta(xobj, 'KP (Penalty)').visible = False

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name == 'Constrain Rotations':
		if _geta(xobj, 'Constrain Rotations').boolean:
			_geta(xobj, 'Constrain Pressure').boolean = False
			_geta(xobj, '-KP').visible = False
			_geta(xobj, 'KP (Penalty)').visible = False
	elif attribute_name == 'Constrain Pressure':
		if _geta(xobj, 'Constrain Pressure').boolean:
			_geta(xobj, 'Constrain Rotations').boolean = False
			_geta(xobj, '-KP').visible = True
			_geta(xobj, 'KP (Penalty)').visible = _geta(xobj, '-KP').boolean
		else:
			_geta(xobj, '-KP').visible = False
			_geta(xobj, 'KP (Penalty)').visible = False
	elif attribute_name == '-KP':
		_geta(xobj, 'KP (Penalty)').visible = _geta(xobj, '-KP').boolean

def writeTcl_mpConstraints(pinfo):
	
	# element ASDEmbeddedNodeElement $Tag  $Cnode   $Rnode1 $Rnode2 $Rnode3 <$Rnode4>   <-K $K> <-rot> <-p> <-KP $KP>
	
	# Utility functions ====================================================================================
	
	import numpy as np
	
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
	rot = '-rot' if _geta(xobj, 'Constrain Rotations').boolean else ''
	pressure = '-p' if _geta(xobj, 'Constrain Pressure').boolean else ''
	ignore_outside = _geta(xobj, 'Ignore Nodes Outside').boolean
	KP_value = _geta(xobj, 'KP (Penalty)').quantityScalar.value
	KP = '-KP {}'.format(KP_value) if (_geta(xobj, 'Constrain Pressure').boolean and _geta(xobj, '-KP').boolean) else ''
	
	# some stats
	stats = [0, 0]
	
	# internal function to process all interactions
	def internal(process_id, process_block_count):
		# first-done flag for partitioned process
		first_done = False
		# process each interaction
		for inter in all_inter:
			# get info about master geometry and do some checks
			if inter.type != MpcInteractionType.NodeToElement:
				raise Exception(_err(pinfo.condition.id, 
					'Interaction "{}" [{}] should be a Node-to-Element interaction, not {}.'.format(
						inter.name, inter.id, inter.type)
						))
			# process all link elements
			moi = doc.mesh.getMeshedInteraction(inter.id)
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
				# the constrained node
				Cnode = elem.nodes[-1]
				Cpos = np.asarray([[Cnode.x],[Cnode.y], [Cnode.z]])
				# get source element
				source_elem = elem.sourceElement
				if source_elem is None:
					raise Exception(_err(pinfo.condition.id, 'Link element should have a valid source element'))
				# check source element and extract embedding sub-simplex (3-node triangle or 4-node tetrahedron)
				retained_nodes = []
				distance = 1.0e10
				family = source_elem.geometryFamilyType()
				if family == MpcElementGeometryFamilyType.Triangle:
					# for any triangle, the first 3 nodes are the corner ones
					retained_nodes = [source_elem.nodes[i] for i in range(3)]
					_, distance = ebu.lct3(retained_nodes, Cpos)
				elif family == MpcElementGeometryFamilyType.Tetrahedron:
					# for any tetrahedron, the first 4 nodes are the corner ones
					retained_nodes = [source_elem.nodes[i] for i in range(4)]
					_, distance = ebu.lct4(retained_nodes, Cpos)
				elif family == MpcElementGeometryFamilyType.Quadrilateral:
					# for any quadrilateral, the first 4 nodes are the corner ones.
					# we need to find the closest sub-simplex
					aux = []
					for sub in ebu.QSubs:
						trial_nodes = [source_elem.nodes[i] for i in sub]
						_, trial_distance = ebu.lct3(trial_nodes, Cpos)
						aux.append((trial_nodes, trial_distance))
					aux = sorted(aux, key = lambda variable: variable[1])
					retained_nodes = aux[0][0]
					distance = aux[0][1]
				elif family == MpcElementGeometryFamilyType.Hexahedron:
					# for any hexahedron, the first 8 nodes are the corner ones.
					# we need to find the closest sub-simplex
					aux = []
					for sub in ebu.HSubs:
						trial_nodes = [source_elem.nodes[i] for i in sub]
						_, trial_distance = ebu.lct4(trial_nodes, Cpos)
						aux.append((trial_nodes, trial_distance))
					aux = sorted(aux, key = lambda variable: variable[1])
					retained_nodes = aux[0][0]
					distance = aux[0][1]
				else:
					# unsupported element type
					raise Exception(_err(pinfo.condition.id, 
						'The source element (master geometry) of the Link element {} '
						'has a wrong family type ({})'.format(elem.id, family)
						))
				# check distance
				if distance > 1.0e-2:
					if ignore_outside:
						stats[1] += 1
						continue
					else:
						raise Exception(_err(pinfo.condition.id, 
							'The constrained node of the Link element {} '
							'is outside the embedding domain (error = {} %; Max allowed error = 1.0 %)'.format(elem.id, distance*100.0)
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
				# write this element
				pinfo.out_file.write(
					'{}{}element ASDEmbeddedNodeElement {}  {}   {}   -K {} {} {} {}\n'.format(
						pinfo.indent, block_indent, elem.id, Cnode.id, 
						' '.join(str(Rnode.id) for Rnode in retained_nodes),
						K, rot, pressure, KP
						)
					)
				stats[0] += 1
		# end-for-each-interaction
		# update process block count
		if is_partitioned:
			if first_done:
				process_block_count += 1
			if process_block_count > 0 and first_done:
				pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count
	
	# write description
	description = '\n{}# element ASDEmbeddedNodeElement $Tag  $Cnode   $Rnode1 $Rnode2 $Rnode3 <$Rnode4>   <-K $K> <-rot> <-p> <-KP $KP>\n'.format(pinfo.indent)
	pinfo.out_file.write(description)
	
	# call the internal function based on partitions
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			pinfo.setProcessId(process_id)
			process_block_count = internal(process_id, process_block_count)
	else:
		internal(0, 0)
	
	# print stats
	print('Processed "ASDEmbeddedNodeElement" at "Condition {}":'.format(pinfo.condition.id))
	print('   {} nodes correctly embedded\n   {} nodes ignored because outside the embedding domain'.format(*stats))
	