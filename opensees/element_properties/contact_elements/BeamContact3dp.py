import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# radius
	at_radius = MpcAttributeMetaData()
	at_radius.type = MpcAttributeType.QuantityScalar
	at_radius.name = 'radius'
	at_radius.group = 'Group'
	at_radius.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('radius')+'<br/>') +
		html_par('constant radius of circular beam associated with beam element') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_radius.dimension = u.L
	
	# transType
	at_transfType = MpcAttributeMetaData()
	at_transfType.type = MpcAttributeType.String
	at_transfType.name = 'transfType'
	at_transfType.group = 'Group'
	at_transfType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('transfType')+'<br/>') +
		html_par(' The geometric-transformation command is used to construct a coordinate-transformation (CrdTransf) object, which transforms beam element stiffness and resisting force from the basic system to the global-coordinate system.The command has at least one argument, the transformation type.') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_transfType.sourceType = MpcAttributeSourceType.List
	at_transfType.setSourceList(['Linear', 'PDelta', 'Corotational'])
	at_transfType.setDefault('Linear')
	
	# penalty
	at_penalty = MpcAttributeMetaData()
	at_penalty.type = MpcAttributeType.Real
	at_penalty.name = 'penalty'
	at_penalty.group = 'Group'
	at_penalty.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('penalty')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# cSwitch
	at_cSwitch = MpcAttributeMetaData()
	at_cSwitch.type = MpcAttributeType.Boolean
	at_cSwitch.name = 'cSwitch'
	at_cSwitch.group = 'Group'
	at_cSwitch.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cSwitch')+'<br/>') +
		html_par('optional initial contact flag') +
		html_par('cFlag = 0 >> contact between bodies is initially assumed (DEFAULT)') +
		html_par('cFlag = 1 >> no contact between bodies is initially assumed') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'BeamContact3dp'
	xom.addAttribute(at_radius)
	xom.addAttribute(at_transfType)
	xom.addAttribute(at_penalty)
	xom.addAttribute(at_cSwitch)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6),(3,[3, 4])]

def writeTcl(pinfo):
	
	# element and properties
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# description
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# checks
	if not phys_prop.XObject.Xnamespace.startswith('materials.nD'):
		raise Exception ('Error: materials must be nDMaterial')
	if(phys_prop.XObject.name != 'ContactMaterial3D'):
		raise Exception('Error: material must be "ContactMaterial3D" and not "{}"'.format(phys_prop.XObject.name))
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
	transType = geta('transfType').string
	penalty = geta('penalty').real
	cSwitch = 1 if geta('cSwitch').boolean else ''
	
	# formatter for new nodes
	FMT = pinfo.get_double_formatter()
	
	# nodes
	node_vect = [node.id for node in elem.nodes]
	
	# if the 3rd node has 4 dofs, we need to create an extra node
	if pinfo.node_to_model_map[node_vect[2]][1] == 4:
		new_node_id = pinfo.next_node_id
		pinfo.next_node_id += 1
		old_node = elem.nodes[2]
		node_vect[2] = new_node_id
		pinfo.updateModelBuilder(3, 3)
		pinfo.out_file.write('{}# auxiliary 3D-U node\n'.format(pinfo.indent))
		pinfo.out_file.write('{}node {} {} {} {}\n'.format(pinfo.indent, new_node_id, FMT(old_node.x), FMT(old_node.y), FMT(old_node.z))) #write the extra node (coinciding with the old node)
		pinfo.out_file.write('{}equalDOF {} {} 1 2 3\n'.format(pinfo.indent, old_node.id, new_node_id)) # link them with edof in common dofs
	
	# now write the geomTransf into the file
	vect_z = elem.orientation.computeOrientation().col(2)
	pinfo.updateModelBuilder(3, 6)
	pinfo.out_file.write('{}# Geometric transformation command\n'.format(pinfo.indent))
	pinfo.out_file.write('{}geomTransf {} {} {} {} {}\n'.format(pinfo.indent, transType, tag, vect_z.x, vect_z.y, vect_z.z))
	
	# now write the string into the file
	pinfo.out_file.write('{}element BeamContact3Dp {}   {} {} {}   {} {} {} {} {}\n'.format(pinfo.indent, tag, *node_vect, radius, tag, matTag, penalty, cSwitch))