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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamContact2D','BeamContact2D')+'<br/>') +
		html_end()
		)
	at_width.dimension = u.L
	
	# gTol
	at_gTol = MpcAttributeMetaData()
	at_gTol.type = MpcAttributeType.Real
	at_gTol.name = 'gTol'
	at_gTol.group = 'Group'
	at_gTol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gTol')+'<br/>') +
		html_par('gap tolerance') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamContact2D','BeamContact2D')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamContact2D','BeamContact2D')+'<br/>') +
		html_end()
		)
	
	# cFlag
	at_cFlag = MpcAttributeMetaData()
	at_cFlag.type = MpcAttributeType.Boolean
	at_cFlag.name = 'cFlag'
	at_cFlag.group = 'Group'
	at_cFlag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cFlag')+'<br/>') +
		html_par('optional initial contact flag') +
		html_par('cFlag = 0 >> contact between bodies is initially assumed (DEFAULT)') +
		html_par('cFlag = 1 >> no contact between bodies is initially assumed') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamContact2D','BeamContact2D')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'BeamContact2D'
	xom.addAttribute(at_width)
	xom.addAttribute(at_gTol)
	xom.addAttribute(at_fTol)
	xom.addAttribute(at_cFlag)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3),(2,2)]	# ndm, ndf

def writeTcl(pinfo):
	
	#element BeamContact2D eleTag? iNode? jNode? slaveNode? lambdaNode? matTag? width? gTol? fTol? <cFlag>
	
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
	if (namePh!='materials.nD'):
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
	
	# Lagrange multiplier node
	nstr+=' {}'.format(pinfo.next_node_id)
	
	if (elem.numberOfMasterNodes()!=2):
		raise Exception('Error: numbers of master node must be 2')
		
	if (elem.numberOfSlaveNodes()!=1):
		raise Exception('Error: numbers of slave node must be 1')
	
	width_at = xobj.getAttribute('width')
	if(width_at is None):
		raise Exception('Error: cannot find "width" attribute')
	width = width_at.quantityScalar.value
	
	gTol_at = xobj.getAttribute('gTol')
	if(gTol_at is None):
		raise Exception('Error: cannot find "gTol" attribute')
	gTol = gTol_at.real
	
	fTol_at = xobj.getAttribute('fTol')
	if(fTol_at is None):
		raise Exception('Error: cannot find "fTol" attribute')
	fTol = fTol_at.real
	
	# optional parameters
	sopt = ''
	
	cFlag_at = xobj.getAttribute('cFlag')
	if(cFlag_at is None):
		raise Exception('Error: cannot find "cFlag" attribute')
	cFlag = cFlag_at.boolean
	if cFlag:
		sopt += ' 1'
	
	# stuff to write
	strNode = '{}{} {} {} {} {}\n'.format(pinfo.indent,'\n#Lagrange multiplier node\n# node', 'tag', 'x', 'y', 'z')
	
	# Lagrange multiplier node needs 2 ndm , 2 ndf
	strNode += '{}node {} {} {} {}\n'.format(pinfo.indent, pinfo.next_node_id, pinfo.lagrangian_node_xyz[0], pinfo.lagrangian_node_xyz[1], pinfo.lagrangian_node_xyz[2])
	pinfo.next_node_id += 1
	
	str_tcl = '{}element BeamContact2D {}{} {} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, matTag, width, gTol, fTol, sopt)
	
	# now write the extra node into the file
	pinfo.updateModelBuilder(2,2)
	pinfo.out_file.write(strNode)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)