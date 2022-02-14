import PyMpc.Units as u
from PyMpc import *
import PyMpc
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import math 

def makeXObjectMetaData():
	
	# radius
	at_radius = MpcAttributeMetaData()
	at_radius.type = MpcAttributeType.QuantityScalar
	at_radius.name = 'radius'
	at_radius.group = 'Group'
	at_radius.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('radius')+'<br/>') +
		html_par('radius of circular beam associated with beam element') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamEndContact3D','BeamEndContact3D')+'<br/>') +
		html_end()
		)
	at_radius.dimension = u.L
	
	# gTol
	at_gTol = MpcAttributeMetaData()
	at_gTol.type = MpcAttributeType.Real
	at_gTol.name = 'gTol'
	at_gTol.group = 'Group'
	at_gTol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gTol')+'<br/>') +
		html_par('gap tolerance') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamEndContact3D','BeamEndContact3D')+'<br/>') +
		html_end()
		)
	
	# fTol
	at_fTol = MpcAttributeMetaData()
	at_fTol.type = MpcAttributeType.Real
	at_fTol.name = 'fTol'
	at_fTol.group = 'Group'
	at_fTol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fTol')+'<br/>') +
		html_par('force tolerance') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamEndContact3D','BeamEndContact3D')+'<br/>') +
		html_end()
		)
	
	# cFlag
	at_cFlag = MpcAttributeMetaData()
	at_cFlag.type = MpcAttributeType.Boolean
	at_cFlag.name = 'cFlag'
	at_cFlag.group = 'Optional parameter'
	at_cFlag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cFlag')+'<br/>') +
		html_par('optional initial contact flag') +
		html_par('cFlag = 0 >> contact between bodies is initially assumed (DEFAULT)') +
		html_par('cFlag = 1 >> no contact between bodies is initially assumed') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamEndContact3D','BeamEndContact3D')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'BeamEndContact3D'
	xom.addAttribute(at_radius)
	xom.addAttribute(at_gTol)
	xom.addAttribute(at_fTol)
	xom.addAttribute(at_cFlag)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6),(3,[3, 4])]

def writeTcl(pinfo):
	
	# element and properties
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	# description
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# checks
	if (elem.numberOfMasterNodes() != 2):
		raise Exception('Error: numbers of master node must be 2')
	if (elem.numberOfSlaveNodes() != 1):
		raise Exception('Error: numbers of master node must be 1')
	
	# parameters
	def geta(name):
		a = xobj.getAttribute(name)
		if a is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return a
	radius = geta('radius').quantityScalar.value
	gTol = geta('gTol').real
	fTol = geta('fTol').real
	cFlag = 1 if geta('cFlag').boolean else ''
	
	# formatter for new nodes
	FMT = pinfo.get_double_formatter()
	
	# nodes
	node_vect = [node.id for node in elem.nodes]
	
	# if the second master node is closer to the slave than the first master,
	# swap them
	D1 = (elem.nodes[1].position - elem.nodes[2].position).norm()
	D0 = (elem.nodes[0].position - elem.nodes[2].position).norm()
	if D1 < D0:
		node_vect[0], node_vect[1] = node_vect[1], node_vect[0]
	
	# auxiliary node and lagrangian node need 3 dofs
	pinfo.updateModelBuilder(3, 3)
	
	# if the 3rd node has 4 dofs, we need to create an extra node
	if pinfo.node_to_model_map[node_vect[2]][1] == 4:
		new_node_id = pinfo.next_node_id
		pinfo.next_node_id += 1
		old_node = elem.nodes[2]
		node_vect[2] = new_node_id
		pinfo.out_file.write('{}# auxiliary 3D-U node\n'.format(pinfo.indent))
		pinfo.out_file.write('{}node {} {} {} {}\n'.format(pinfo.indent, new_node_id, FMT(old_node.x), FMT(old_node.y), FMT(old_node.z))) #write the extra node (coinciding with the old node)
		pinfo.out_file.write('{}equalDOF {} {} 1 2 3\n'.format(pinfo.indent, old_node.id, new_node_id)) # link them with edof in common dofs
	
	# lagrange multiplier node
	lag_node = pinfo.next_node_id
	pinfo.next_node_id += 1
	pinfo.out_file.write('{}# Lagrangian 3D-3U node\n'.format(pinfo.indent))
	pinfo.out_file.write('{}node {} {} {} {}\n'.format(pinfo.indent, lag_node, FMT(pinfo.lagrangian_node_xyz[0]), FMT(pinfo.lagrangian_node_xyz[1]), FMT(pinfo.lagrangian_node_xyz[2])))
	
	# now write the string into the file
	pinfo.updateModelBuilder(3, 6)
	pinfo.out_file.write('{}element BeamEndContact3D {}   {} {} {} {}   {} {} {} {}\n'.format(pinfo.indent, tag, *node_vect, lag_node, radius, gTol, fTol, cFlag))