import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Group'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') +
		html_par('Young\'s Modulus of element material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/VS3D4','VS3D4')+'<br/>') +
		html_end()
		)
	
	# G
	at_G = MpcAttributeMetaData()
	at_G.type = MpcAttributeType.QuantityScalar
	at_G.name = 'G'
	at_G.group = 'Group'
	at_G.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('G')+'<br/>') +
		html_par('Shear Modulus of element material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/VS3D4','VS3D4')+'<br/>') +
		html_end()
		)
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Group'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') +
		html_par('element mass density (per unit volume) from which a lumped element mass matrix is computed (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/VS3D4','VS3D4')+'<br/>') +
		html_end()
		)
	at_rho.setDefault(0.0)
	
	# R
	at_R = MpcAttributeMetaData()
	at_R.type = MpcAttributeType.QuantityScalar
	at_R.name = 'R'
	at_R.group = 'Group'
	at_R.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R')+'<br/>') +
		html_par('distance from the scattered wave source to the boundary') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/VS3D4','VS3D4')+'<br/>') +
		html_end()
		)
	at_R.dimension = u.L
	
	# alphaN
	at_alphaN = MpcAttributeMetaData()
	at_alphaN.type = MpcAttributeType.Real
	at_alphaN.name = 'alphaN'
	at_alphaN.group = 'Group'
	at_alphaN.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaN')+'<br/>') +
		html_par('correction parameter in the normal direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/VS3D4','VS3D4')+'<br/>') +
		html_end()
		)
	
	# alphaT
	at_alphaT = MpcAttributeMetaData()
	at_alphaT.type = MpcAttributeType.Real
	at_alphaT.name = 'alphaT'
	at_alphaT.group = 'Group'
	at_alphaT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaT')+'<br/>') +
		html_par('correction parameter in the tangential direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/VS3D4','VS3D4')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'VS3D4'
	xom.addAttribute(at_E)
	xom.addAttribute(at_G)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_R)
	xom.addAttribute(at_alphaN)
	xom.addAttribute(at_alphaT)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,3),(3,3),(3,3),(3,3)] #(ndm, ndf)

def writeTcl(pinfo):
	
	#element VS3D4 $eleTag $node1 $node2 $node3 $node4 $E $G $rho $R $alphaN $alphaT
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=4):
		raise Exception('Error: invalid number of nodes')
	
	
	# mandatory parameters
	at_E = xobj.getAttribute('E')
	if(at_E is None):
		raise Exception('Error: cannot find "E" attribute')
	E = at_E.quantityScalar.value
	
	at_G = xobj.getAttribute('G')
	if(at_G is None):
		raise Exception('Error: cannot find "G" attribute')
	G = at_G.quantityScalar.value
	
	rho_at = xobj.getAttribute('rho')
	if(rho_at is None):
		raise Exception('Error: cannot find "rho" attribute')
	rho = rho_at.quantityScalar.value
	
	R_at = xobj.getAttribute('R')
	if(R_at is None):
		raise Exception('Error: cannot find "R" attribute')
	R = R_at.quantityScalar.value
	
	alphaN_at = xobj.getAttribute('alphaN')
	if(alphaN_at is None):
		raise Exception('Error: cannot find "alphaN" attribute')
	alphaN = alphaN_at.real
	
	alphaT_at = xobj.getAttribute('alphaT')
	if(alphaT_at is None):
		raise Exception('Error: cannot find "alphaT" attribute')
	alphaT = alphaT_at.real
	
	
	str_tcl = '{}element VS3D4 {}{} {} {} {} {} {} {}\n'.format(pinfo.indent, tag, nstr, E, G, rho, R, alphaN, alphaT)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)