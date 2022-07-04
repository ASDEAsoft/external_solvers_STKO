import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.utils.tcl_input as tclin

####################################################################################
# Utilities
####################################################################################

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

####################################################################################
# Main methods
####################################################################################

def makeXObjectMetaData():
	
	# Beam
	at_Beam = MpcAttributeMetaData()
	at_Beam.type = MpcAttributeType.Index
	at_Beam.name = 'Beam'
	at_Beam.group = 'Beam'
	at_Beam.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Element properties Beam')+'<br/>') +
		html_par('assign "element property" for beam') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_Beam.indexSource.type = MpcAttributeIndexSourceType.ElementProperty
	at_Beam.indexSource.addAllowedNamespace("beam_column_elements")
	'''at_Beam.indexSource.addAllowedNamespaceList(["Namespace_1", "Namespace_2"])'''
	
	# zeroLength_i
	at_zeroLength_i = MpcAttributeMetaData()
	at_zeroLength_i.type = MpcAttributeType.Index
	at_zeroLength_i.name = 'zeroLength_i'
	at_zeroLength_i.group = 'ZeroLength'
	at_zeroLength_i.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('zeroLength')+'<br/>') +
		html_par('zeroLength at the node i') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLength_Element','ZeroLength Element')+'<br/>') +
		html_end()
		)
	at_zeroLength_i.indexSource.type = MpcAttributeIndexSourceType.ElementProperty
	at_zeroLength_i.indexSource.addAllowedNamespace("zero_length_elements")
	
	# zeroLength_j
	at_zeroLength_j = MpcAttributeMetaData()
	at_zeroLength_j.type = MpcAttributeType.Index
	at_zeroLength_j.name = 'zeroLength_j'
	at_zeroLength_j.group = 'ZeroLength'
	at_zeroLength_j.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('zeroLength')+'<br/>') +
		html_par('zeroLength at the node j') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLength_Element','ZeroLength Element')+'<br/>') +
		html_end()
		)
	at_zeroLength_j.indexSource.type = MpcAttributeIndexSourceType.ElementProperty
	at_zeroLength_j.indexSource.addAllowedNamespace("zero_length_elements")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'HingedBeam'
	xom.addAttribute(at_Beam)
	xom.addAttribute(at_zeroLength_i)
	xom.addAttribute(at_zeroLength_j)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	
	# checks
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	if xobj_phys_prop.name != 'HingedBeamPP':
		raise Exception('Wrong material type for "HingedBeam" element. Expected: "HingedBeamPP", given: "{}"'.format(xobj_phys_prop.name))
	
	# read element properties
	xobj_ep_beam_index = _get_xobj_attribute(xobj, 'Beam').index
	xobj_ep_hinge_i_index = _get_xobj_attribute(xobj, 'zeroLength_i').index
	xobj_ep_hinge_j_index = _get_xobj_attribute(xobj, 'zeroLength_j').index
	
	do_hinge_i = (xobj_ep_hinge_i_index != 0)
	do_hinge_j = (xobj_ep_hinge_j_index != 0)
	
	ep_Beam = doc.elementProperties[xobj_ep_beam_index]
	ep_Beam_xobj = ep_Beam.XObject
	if do_hinge_i:
		ep_zeroLength_i = doc.elementProperties[xobj_ep_hinge_i_index]
		ep_zeroLength_i_xobj = ep_zeroLength_i.XObject
	
	if do_hinge_j:
		ep_zeroLength_j = doc.elementProperties[xobj_ep_hinge_j_index]
		ep_zeroLength_j_xobj = ep_zeroLength_j.XObject
	
	# read physical properties
	xobj_pp_beam_index = _get_xobj_attribute(xobj_phys_prop, 'PP_Beam').index
	pp_Beam = doc.physicalProperties[xobj_pp_beam_index]
	pp_Beam_xobj = pp_Beam.XObject
	
	if do_hinge_i:
		xobj_pp_hinge_i_index = _get_xobj_attribute(xobj_phys_prop, 'zeroLength_i').index
		if xobj_pp_hinge_i_index == 0:
			raise Exception("You provided a hinge element in I-end, but no hinge material!")
		pp_zeroLength_i = doc.physicalProperties[xobj_pp_hinge_i_index]
		pp_zeroLength_i_xobj = pp_zeroLength_i.XObject
	
	if do_hinge_j:
		xobj_pp_hinge_j_index = _get_xobj_attribute(xobj_phys_prop, 'zeroLength_j').index
		if xobj_pp_hinge_j_index == 0:
			raise Exception("You provided a hinge element in J-end, but no hinge material!")
		pp_zeroLength_j = doc.physicalProperties[xobj_pp_hinge_j_index]
		pp_zeroLength_j_xobj = pp_zeroLength_j.XObject
	
	# read module and getNodalSpatialDim
	tp_vector_coll = []
	
	if do_hinge_i:
		ep_zeroLength_i_module_name = 'opensees.element_properties.{}.{}'.format(ep_zeroLength_i_xobj.Xnamespace, ep_zeroLength_i_xobj.name)
		ep_zeroLength_i_module = importlib.import_module(ep_zeroLength_i_module_name)
		ep_zeroLength_i_dim = ep_zeroLength_i_module.getNodalSpatialDim(ep_zeroLength_i_xobj, pp_zeroLength_i_xobj)
		tp_vector_coll.append(ep_zeroLength_i_dim)
	
	ep_Beam_module_name = 'opensees.element_properties.{}.{}'.format(ep_Beam_xobj.Xnamespace, ep_Beam_xobj.name)
	ep_Beam_module = importlib.import_module(ep_Beam_module_name)
	ep_Beam_dim = ep_Beam_module.getNodalSpatialDim(ep_Beam_xobj, pp_Beam_xobj)
	tp_vector_coll.append(ep_Beam_dim)
	
	if do_hinge_j:
		ep_zeroLength_j_module_name = 'opensees.element_properties.{}.{}'.format(ep_zeroLength_j_xobj.Xnamespace, ep_zeroLength_j_xobj.name)
		ep_zeroLength_j_module = importlib.import_module(ep_zeroLength_j_module_name)
		ep_zeroLength_j_dim = ep_zeroLength_j_module.getNodalSpatialDim(ep_zeroLength_j_xobj, pp_zeroLength_j_xobj)
		tp_vector_coll.append(ep_zeroLength_j_dim)
	
	
	# here we want to check that both the 2-end zero length and the inner beam elements
	# have the same dimension (i.e. 2d or 3d).
	# don't do any check on the dofs, their compatibility is checked while
	# constructing the node map.
	ndm = None
	for tp_vector in tp_vector_coll:
		# item is a vector of tuples
		for tp in tp_vector:
			# tp is a tuple, where the first item is the NDM
			# while the second item is 1 or multiples (vector) of NDF
			if ndm is None:
				ndm = tp[0]
			else:
				if ndm != tp[0]:
					raise Exception('Error: different spatial dimension between the elements')
	# ndf is taken from the beam because the beam requirement in terms of dofs is more strict:
	# beam = (2, 3) or (3, 6)
	# z lenght = (2, [2,3]), (3, [3,4,6])
	ndf = ep_Beam_dim[0][1]
	
	return [(ndm,ndf),(ndm,ndf)]	# 2 nodes for Beam and 2 nodes for zeroLength

def writeTcl(pinfo):
	# element_properties_Beam, zeroLength_i, zeroLength_j, physical_properties_Beam, zeroLengthMaterial_i, zeroLengthMaterial_j
	
	# get document
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	# get element and check it
	elem = pinfo.elem
	if elem.topologyType() != MpcElementTopologyType.Edge:
		raise Exception('Error: element must be "Edge" and not "{}"'.format(elem.topologyType().name))
	if len(elem.nodes) != 2 and len(elem.nodes) != 3:
		raise Exception('Error: internal element for hinged beam must have 2 or 3 nodes')
	tag = elem.id
	
	# get physical and element properties
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	if(phys_prop is None):
		raise Exception('Error: HingedBeam has a null physical property. Please assign a physical property of type "HingedBeamPP"')
	if(elem_prop is None):
		raise Exception('Error: HingedBeam has a null element property. Please assign a physical property of type "HingedBeam"')
	
	# get element properties
	xobj_ep_beam_index = _get_xobj_attribute(elem_prop.XObject, 'Beam').index
	xobj_ep_hinge_i_index = _get_xobj_attribute(elem_prop.XObject, 'zeroLength_i').index
	xobj_ep_hinge_j_index = _get_xobj_attribute(elem_prop.XObject, 'zeroLength_j').index
	
	# get physical properties
	if phys_prop.XObject.name != 'HingedBeamPP':
		raise Exception('Wrong material type for "HingedBeam" element. Expected: "HingedBeamPP", given: "{}"'.format(phys_prop.XObject.name))
	xobj_pp_beam_index = _get_xobj_attribute(phys_prop.XObject, 'PP_Beam').index
	xobj_pp_hinge_i_index = _get_xobj_attribute(phys_prop.XObject, 'zeroLength_i').index
	xobj_pp_hinge_j_index = _get_xobj_attribute(phys_prop.XObject, 'zeroLength_j').index
	
	# check
	if xobj_ep_hinge_i_index != 0:
		if xobj_pp_hinge_i_index == 0:
			raise Exception("You provided a hinge element in I-end, but no hinge material!")
	# if xobj_pp_hinge_i_index != 0:
		# if xobj_ep_hinge_i_index == 0:
			# raise Exception("You provided a hinge material in I-end, but no hinge element!")
	if xobj_ep_hinge_j_index != 0:
		if xobj_pp_hinge_j_index == 0:
			raise Exception("You provided a hinge element in J-end, but no hinge material!")
	# if xobj_pp_hinge_j_index != 0:
		# if xobj_ep_hinge_j_index == 0:
			# raise Exception("You provided a hinge material in J-end, but no hinge element!")
	
	# let's see if we have to build hinges, and at what sides
	do_hinge_i = (elem.nodes[0].flags & MpcNodeFlags.OnVertex) and (xobj_ep_hinge_i_index != 0)
	do_hinge_j = (elem.nodes[1].flags & MpcNodeFlags.OnVertex) and (xobj_ep_hinge_j_index != 0)
	
	# exterior elements are zero length, created here but not in STKO
	auto_gen_data = tclin.auto_generated_element_data()
	if do_hinge_i:
		exterior_elem_i = pinfo.next_elem_id
		pinfo.next_elem_id += 1
		auto_gen_data.elements.append(exterior_elem_i)
	if do_hinge_j:
		exterior_elem_j = pinfo.next_elem_id
		pinfo.next_elem_id += 1
		auto_gen_data.elements.append(exterior_elem_j)
	if len(auto_gen_data.elements):
		pinfo.auto_generated_element_data_map[elem.id] = auto_gen_data
	
	# save original nodes' ids, they are going to be changed for processing inner elements
	# and then set back to the original ones
	# why? because the nodes generated by STKO are put into the model map
	# moreover, since they are created here, they are not in the node_to_model_map
	# just add their ndm/ndf pair to the node_to_model_map copying from the exterior ones
	exterior_node_i = pinfo.elem.nodes[0].id
	exterior_node_j = pinfo.elem.nodes[1].id
	# since we are going to change them (probably) with the joint model ...
	# save a copy to be used in the finally statement
	exterior_node_i_copy = exterior_node_i
	exterior_node_j_copy = exterior_node_j
	
	# nodes
	node_vect = [exterior_node_i, exterior_node_j]
	# apply correction for joints (2D)??
	if 'RCJointModel3D' in pinfo.custom_data:
		joint_manager = pinfo.custom_data['RCJointModel3D']
		node_pos = joint_manager.adjustBeamConnectivity(pinfo, elem, node_vect)
	else:
		node_pos = [elem.nodes[0].position, elem.nodes[1].position]
	exterior_node_i = node_vect[0]
	exterior_node_j = node_vect[1]
	
	if do_hinge_i:
		interior_node_i = pinfo.next_node_id
		pinfo.next_node_id += 1
		pinfo.node_to_model_map[interior_node_i] = pinfo.node_to_model_map[exterior_node_i]
	else:
		interior_node_i = exterior_node_i
	if do_hinge_j:
		interior_node_j = pinfo.next_node_id
		pinfo.next_node_id += 1
		pinfo.node_to_model_map[interior_node_j] = pinfo.node_to_model_map[exterior_node_j]
	else:
		interior_node_j = exterior_node_j
	
	'''
	in the following code block we need to do a hack:
	we change the indices of element/nodes for processing zero-length and interior
	beam element. but actually there is only 1 element in STKO.
	to make sure that the hacking is reverted to the original state we use 
	the following try-catch-finally block
	'''
	ndm_ndf = pinfo.node_to_model_map[exterior_node_i]
	pinfo.updateModelBuilder(ndm_ndf[0], ndm_ndf[1])
	FMT = pinfo.get_double_formatter()
	try:
		
		#------------------------------------------------- Interior nodes ---------------------------------------------------
		
		if do_hinge_i or do_hinge_j:
			strNode = '{}{} {} {} {} {}\n'.format(pinfo.indent,'\n# Extra nodes for zeroLength\n# node', 'tag', 'x', 'y', 'z')
			if do_hinge_i:
				strNode += '{}node {} {} {} {}\n'.format(pinfo.indent, interior_node_i, FMT(node_pos[0].x), FMT(node_pos[0].y), FMT(node_pos[0].z))
			if do_hinge_j:
				strNode += '{}node {} {} {} {}\n'.format(pinfo.indent, interior_node_j, FMT(node_pos[1].x), FMT(node_pos[1].y), FMT(node_pos[1].z))
			pinfo.out_file.write(strNode)
		
		#------------------------------------------------------- Beam -------------------------------------------------------
		
		# hack elem nodal id!!!!
		pinfo.elem.nodes[0].id = interior_node_i
		pinfo.elem.nodes[1].id = interior_node_j
		
		# hack properties !!
		pinfo.phys_prop = doc.physicalProperties[xobj_pp_beam_index]
		pinfo.elem_prop = doc.elementProperties[xobj_ep_beam_index]

		ep_Beam = doc.elementProperties[xobj_ep_beam_index]
		ep_Beam_xobj = ep_Beam.XObject
		
		#read module
		ep_Beam_module_name = 'opensees.element_properties.{}.{}'.format(ep_Beam_xobj.Xnamespace, ep_Beam_xobj.name)
		ep_Beam_module = importlib.import_module(ep_Beam_module_name)
		ep_Beam_module.writeTcl(pinfo)
		
		
		#---------------------------------------------------- zeroLength i ----------------------------------------------------
		
		if do_hinge_i:
			# hack elem nodal id!!!!
			pinfo.elem.nodes[0].id = exterior_node_i # master
			pinfo.elem.nodes[1].id = interior_node_i # slave
			
			# hack elements id
			pinfo.elem.id = exterior_elem_i
			
			# hack properties
			pinfo.phys_prop = doc.physicalProperties[xobj_pp_hinge_i_index]
			pinfo.elem_prop = doc.elementProperties[xobj_ep_hinge_i_index]
			
			ep_zeroLength_i = doc.elementProperties[xobj_ep_hinge_i_index]
			ep_zeroLength_i_xobj = ep_zeroLength_i.XObject
			
			#read module
			ep_zeroLength_i_module_name = 'opensees.element_properties.{}.{}'.format(ep_zeroLength_i_xobj.Xnamespace, ep_zeroLength_i_xobj.name)
			ep_zeroLength_i_module = importlib.import_module(ep_zeroLength_i_module_name)
			ep_zeroLength_i_module.writeTcl(pinfo)
		
		#---------------------------------------------------- zeroLength j ----------------------------------------------------
		
		if do_hinge_j:
			# hack elem nodal id!!!!
			pinfo.elem.nodes[0].id = interior_node_j # master
			pinfo.elem.nodes[1].id = exterior_node_j # slave
			
			# hack elements id
			pinfo.elem.id = exterior_elem_j
			
			pinfo.phys_prop = doc.physicalProperties[xobj_pp_hinge_j_index]
			pinfo.elem_prop = doc.elementProperties[xobj_ep_hinge_j_index]
			
			ep_zeroLength_j = doc.elementProperties[xobj_ep_hinge_j_index]
			ep_zeroLength_j_xobj = ep_zeroLength_j.XObject
			
			#read module
			ep_zeroLength_j_module_name = 'opensees.element_properties.{}.{}'.format(ep_zeroLength_j_xobj.Xnamespace, ep_zeroLength_j_xobj.name)
			ep_zeroLength_j_module = importlib.import_module(ep_zeroLength_j_module_name)
			ep_zeroLength_j_module.writeTcl(pinfo)
	
	except Exception as the_exception:
		
		# re-raise the exception here
		raise the_exception
		
	finally:
		
		# get rid of the hack
		# this code MUST be called even in case of exceptions!
		# thus the finally!
		
		pinfo.elem.nodes[0].id = exterior_node_i_copy
		pinfo.elem.nodes[1].id = exterior_node_j_copy
		
		pinfo.elem.id = tag
		
		pinfo.phys_prop = phys_prop
		pinfo.elem_prop = elem_prop