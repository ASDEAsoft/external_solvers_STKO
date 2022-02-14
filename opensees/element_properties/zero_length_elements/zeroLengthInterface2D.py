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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthInterface2D','ZeroLengthInterface2D')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthInterface2D','ZeroLengthInterface2D')+'<br/>') +
		html_end()
		)
	
	# phi
	at_phi = MpcAttributeMetaData()
	at_phi.type = MpcAttributeType.QuantityScalar
	at_phi.name = 'phi'
	at_phi.group = 'Group'
	at_phi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('phi')+'<br/>') +
		html_par('Friction angle in degrees') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthInterface2D','ZeroLengthInterface2D')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLengthInterface2D'
	xom.addAttribute(at_Kn)
	xom.addAttribute(at_Kt)
	xom.addAttribute(at_phi)
	
	return xom

def writeTcl(pinfo):
	
	# zeroLengthInterface2D $eleTag -sNdNum $sNdNum -mNdNum $mNdNum -dof $sdof $mdof -Nodes $Nodes $Kn $Kt $phi
	
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
	
	mdof = elem.numberOfMasterNodes()
	sdof = elem.numberOfSlaveNodes()
	mNdNum = len(mdof)
	sNdNum = len(sdof)
	
	if sNdNum != mNdNum:
		raise Exception('Error: difference number between mNdNum and sNdNum')
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += '{} '.format(node.id)
	
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral or len(node_vect)!=4):
		raise Exception('Error: invalid type of element or number of nodes')
	
	Kn_at = xobj.getAttribute('Kn')
	if(Kn_at is None):
		raise Exception('Error: cannot find "Kn" attribute')
	Kn = Kn_at.quantityScalar
	
	Kt_at = xobj.getAttribute('Kt')
	if(Kt_at is None):
		raise Exception('Error: cannot find "Kt" attribute')
	Kt = Kt_at.quantityScalar
	
	phi_at = xobj.getAttribute('phi')
	if(phi_at is None):
		raise Exception('Error: cannot find "phi" attribute')
	phi = phi_at.quantityScalar
	
	str_tcl = '{}element zeroLengthInterface2D {} -sNdNum {} -mNdNum {} -dof {} {} -Nodes {} {} {} {} {} {}\n'.format(pinfo.indent, tag, sNdNum, mNdNum, sdof, Kn, Kt, phi)		#**********nstr
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)