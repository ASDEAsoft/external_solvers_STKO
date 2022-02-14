import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# LrgDspTag
	at_LrgDspTag = MpcAttributeMetaData()
	at_LrgDspTag.type = MpcAttributeType.Integer
	at_LrgDspTag.name = 'LrgDspTag'
	at_LrgDspTag.group = 'Group'
	at_LrgDspTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('LrgDspTag')+'<br/>') +
		html_par('an integer indicating the flag for considering large deformations:') +
		html_par('0 - for small deformations and constant geometry') +
		html_par('1 - for large deformations and time varying geometry') +
		html_par('2 - for large deformations ,time varying geometry and length correction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Joint2D_Element','Joint2D Element')+'<br/>') +
		html_end()
		)
	at_LrgDspTag.sourceType = MpcAttributeSourceType.List
	at_LrgDspTag.setSourceList([0, 1, 2])
	at_LrgDspTag.setDefault(0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Joint2D'
	xom.addAttribute(at_LrgDspTag)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3),(2,3),(2,3),(2,4)]

def writeTcl(pinfo):
	
	# element Joint2D $eleTag $Nd1 $Nd2 $Nd3 $Nd4 $NdC <$Mat1 $Mat2 $Mat3 $Mat4> $MatC $LrgDspTag
	
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
	nstr = ''
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=4):
		raise Exception('Error: invalid number of nodes')
	
	# integer tags indicating the central node of beam-column joint
	nstr+=' {}'.format(pinfo.next_node_id)
	pinfo.next_node_id+=1
	
	# special_purpose
	if phys_prop.XObject.name != 'Joint2DMaterial':
		raise Exception('Wrong material type for ZeroLength element. Expected: Joint2DMaterial, given: {}'.format(phys_prop.XObject.name))
	
	MatC_at = phys_prop.XObject.getAttribute('MatC')
	MatC=MatC_at.index
	
	
	use_Mat_at = phys_prop.XObject.getAttribute('use_Mat')
	if(use_Mat_at is None):
		raise Exception('Error: cannot find "use_Mat" attribute')
	use_Mat = use_Mat_at.boolean
		# optional paramters
	sopt = ''
	if use_Mat:
		Mat1_at = phys_prop.XObject.getAttribute('Mat1')
		Mat1=Mat1_at.index
		
		Mat2_at = phys_prop.XObject.getAttribute('Mat2')
		Mat2=Mat2_at.index
		
		Mat3_at = phys_prop.XObject.getAttribute('Mat3')
		Mat3=Mat3_at.index
		
		Mat4_at = phys_prop.XObject.getAttribute('Mat4')
		Mat4=Mat4_at.index
		
		sopt+='{} {} {} {}'.format(Mat1, Mat2, Mat3, Mat4)
	
	LrgDspTag_at = xobj.getAttribute('LrgDspTag')
	if(LrgDspTag_at is None):
		raise Exception('Error: cannot find "LrgDspTag" attribute')
	LrgDspTag = LrgDspTag_at.integer
	
	str_tcl = '{}element Joint2D {}{} {} {} {}\n'.format(pinfo.indent, tag, nstr, sopt, MatC, LrgDspTag)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)