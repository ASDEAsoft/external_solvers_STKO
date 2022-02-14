import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Group'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') +
		html_par('to activate eleHeightFac and eleWidthFac') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	
	# eleHeightFac
	at_eleHeightFac = MpcAttributeMetaData()
	at_eleHeightFac.type = MpcAttributeType.Real
	at_eleHeightFac.name = 'eleHeightFac'
	at_eleHeightFac.group = 'Optional parameters'
	at_eleHeightFac.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eleHeightFac')+'<br/>') +
		html_par('floating point value (as a ratio to the total height of the element) to be considered for determination of the distance in between the tension-compression couples (optional, default: 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_eleHeightFac.setDefault(1.0)
	
	# eleWidthFac
	at_eleWidthFac = MpcAttributeMetaData()
	at_eleWidthFac.type = MpcAttributeType.Real
	at_eleWidthFac.name = 'eleWidthFac'
	at_eleWidthFac.group = 'Optional parameters'
	at_eleWidthFac.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eleWidthFac')+'<br/>') +
		html_par('floating point value (as a ratio to the total width of the element) to be considered for determination of the distance in between the tension-compression couples (optional, default: 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BeamColumnJoint_Element','BeamColumnJoint Element')+'<br/>') +
		html_end()
		)
	at_eleWidthFac.setDefault(1.0)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'beamColumnJoint'
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_eleHeightFac)
	xom.addAttribute(at_eleWidthFac)
	
	
	# visibility dependencies
	
	# eleHeightFac, eleWidthFac-dep
	xom.setVisibilityDependency(at_Optional, at_eleHeightFac)
	xom.setVisibilityDependency(at_Optional, at_eleWidthFac)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3),(2,3),(2,3)]

def writeTcl(pinfo):
	
	# element beamColumnJoint $eleTag $Nd1 $Nd2 $Nd3 $Nd4 $Mat1 $Mat2 $Mat3 $Mat4 $Mat5 $Mat6 $Mat7 $Mat8 $Mat9 $Mat10 $Mat11 $Mat12 $Mat13 <$eleHeightFac $eleWidthFac>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	pinfo.updateModelBuilder(2,3)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	nstr = ''
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=4):
		raise Exception('Error: invalid number of nodes')
	
	# special_purpose
	if phys_prop.XObject.name != 'beamColumnJointMaterial':
		raise Exception('Wrong material type for ZeroLength element. Expected: beamColumnJointMaterial, given: {}'.format(phys_prop.XObject.name))
	
	mat_string = ''
	mat_counter = 0
	for i in range (1,14):
		mat_tag_att_name = 'Mat{}'.format(i)
		matTag_at = phys_prop.XObject.getAttribute(mat_tag_att_name)
		if(matTag_at is None):
			raise Exception('Error: cannot find "{}" attribute'.format(mat_tag_att_name))
		mat_tag = matTag_at.index
		if mat_tag > 0:
			mat_counter += 1
			mat_string += ' {}'.format(mat_tag)
			
	if mat_counter != 13:
		raise Exception ('Error: invalid number of materials')
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		eleHeightFac_at = xobj.getAttribute('eleHeightFac')
		if(eleHeightFac_at is None):
			raise Exception('Error: cannot find "eleHeightFac" attribute')
		eleHeightFac = eleHeightFac_at.real
	
		eleWidthFac_at = xobj.getAttribute('eleWidthFac')
		if(eleWidthFac_at is None):
			raise Exception('Error: cannot find "eleWidthFac" attribute')
		eleWidthFac = eleWidthFac_at.real
	
		sopt += ' {} {}'.format(eleHeightFac, eleWidthFac)
	
	# element beamColumnJoint $eleTag $Nd1 $Nd2 $Nd3 $Nd4 $Mat1 $Mat2 $Mat3 $Mat4 $Mat5 $Mat6 $Mat7 $Mat8 $Mat9 $Mat10 $Mat11 $Mat12 $Mat13 <$eleHeightFac $eleWidthFac>
	
	str_tcl = '{}element beamColumnJoint {}{}{}{}\n'.format(pinfo.indent, tag, nstr, mat_string, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
