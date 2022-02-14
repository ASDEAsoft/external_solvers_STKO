import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# width
	at_width = MpcAttributeMetaData()
	at_width.type = MpcAttributeType.QuantityScalar
	at_width.name = 'width'
	at_width.group = 'Group'
	at_width.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('width')+'<br/>') +
		html_par('the width of the wall represented by the beam element in plane strain') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_width.dimension = u.L
	
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
		html_par('cSwitch = 0 >> contact between bodies is initially assumed (DEFAULT)') +
		html_par('cSwitch = 1 >> no contact between bodies is initially assumed') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'BeamContact2dp'
	xom.addAttribute(at_width)
	xom.addAttribute(at_penalty)
	xom.addAttribute(at_cSwitch)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3),(2,2)]	# ndm, ndf

def writeTcl(pinfo):
	
	#element BeamContact2Dp eleTag? iNode? jNode? slaveNode? matTag? width? penalty? <cSwitch>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh=phys_prop.XObject.Xnamespace
	if not namePh.startswith('materials.nD'):
		raise Exception('Error: physical property must be "materials.nD" and not: "{}"'.format(namePh))
	
	nameMaterial = phys_prop.XObject.name
	if(nameMaterial!='ContactMaterial2D'):
		raise Exception('Error: material must be "ContactMaterial2D" and not "{}"'.format(nameMaterial))
	
	# NODE
	nstr = ''
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	
	width_at = xobj.getAttribute('width')
	if(width_at is None):
		raise Exception('Error: cannot find "width" attribute')
	width = width_at.real
	
	penalty_at = xobj.getAttribute('penalty')
	if(penalty_at is None):
		raise Exception('Error: cannot find "penalty" attribute')
	penalty = penalty_at.real
	
	
	# optional paramters
	sopt = ''
	
	cSwitch_at = xobj.getAttribute('cSwitch')
	if(cSwitch_at is None):
		raise Exception('Error: cannot find "cSwitch" attribute')
	cSwitch = cSwitch_at.boolean
	if cSwitch:
		
		sopt += ' 1'
	
	
	str_tcl = '{}element BeamContact2Dp {}{} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, matTag, width, penalty, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)