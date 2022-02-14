import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# gTol
	at_gTol = MpcAttributeMetaData()
	at_gTol.type = MpcAttributeType.Real
	at_gTol.name = 'gTol'
	at_gTol.group = 'Group'
	at_gTol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gTol')+'<br/>') +
		html_par('gap tolerance') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SimpleContact2D','SimpleContact2D')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SimpleContact2D','SimpleContact2D')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'SimpleContact2D'
	xom.addAttribute(at_gTol)
	xom.addAttribute(at_fTol)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,2),(2,2),(2,2)]

def writeTcl(pinfo):
	# element SimpleContact2D $eleTag $iNode $jNode $sNode $lNode $matTag $gTol $fTol
	
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
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	# Lagrange multiplier node
	nstr+=' {}'.format(pinfo.next_node_id)
	
	gTol_at = xobj.getAttribute('gTol')
	if(gTol_at is None):
		raise Exception('Error: cannot find "gTol" attribute')
	gTol = gTol_at.real
	
	fTol_at = xobj.getAttribute('fTol')
	if(fTol_at is None):
		raise Exception('Error: cannot find "fTol" attribute')
	fTol = fTol_at.real
	
	# stuff to write
	strNode='{}{} {} {} {} {}\n'.format(pinfo.indent,'\n#Lagrange multiplier node\n# node', 'tag', 'x', 'y', 'z')
	# Lagrange multiplier node needs 2 ndm , 2 ndf
	pinfo.updateModelBuilder(2, 2)
	strNode+='{}node {} {} {} {}\n'.format(pinfo.indent, pinfo.next_node_id, pinfo.lagrangian_node_xyz[0], pinfo.lagrangian_node_xyz[1], pinfo.lagrangian_node_xyz[2])
	pinfo.next_node_id += 1
	
	# now write the extra node into the file
	pinfo.out_file.write(strNode)
	
	str_tcl = '{}element SimpleContact2D {}{} {} {} {}\n'.format(pinfo.indent, tag, nstr, matTag, gTol, fTol)
	# now write the string into the file
	pinfo.out_file.write(str_tcl)