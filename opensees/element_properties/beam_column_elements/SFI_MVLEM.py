import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.Integer
	at_m.name = 'm'
	at_m.group = 'Group'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') +
		html_par('Number of element macro-fibers') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SFI_MVLEM_-_Cyclic_Shear-Flexure_Interaction_Model_for_RC_Walls','SFI MVLEM - Cyclic Shear-Flexure Interaction Model for RC Walls')+'<br/>') +
		html_end()
		)
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.Real
	at_c.name = 'c'
	at_c.group = 'Group'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') +
		html_par('Location of center of rotation with from the iNode, c = 0.4 (recommended)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SFI_MVLEM_-_Cyclic_Shear-Flexure_Interaction_Model_for_RC_Walls','SFI MVLEM - Cyclic Shear-Flexure Interaction Model for RC Walls')+'<br/>') +
		html_end()
		)
	
	# Thicknesses
	at_Thicknesses = MpcAttributeMetaData()
	at_Thicknesses.type = MpcAttributeType.QuantityVector
	at_Thicknesses.name = 'Thicknesses'
	at_Thicknesses.group = '-thick'
	at_Thicknesses.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Thicknesses')+'<br/>') +
		html_par('Array of m macro-fiber thicknesses') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SFI_MVLEM_-_Cyclic_Shear-Flexure_Interaction_Model_for_RC_Walls','SFI MVLEM - Cyclic Shear-Flexure Interaction Model for RC Walls')+'<br/>') +
		html_end()
		)
	
	# Widths
	at_Widths = MpcAttributeMetaData()
	at_Widths.type = MpcAttributeType.QuantityVector
	at_Widths.name = 'Widths'
	at_Widths.group = '-width'
	at_Widths.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Widths')+'<br/>') +
		html_par('Array of m macro-fiber widths') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SFI_MVLEM_-_Cyclic_Shear-Flexure_Interaction_Model_for_RC_Walls','SFI MVLEM - Cyclic Shear-Flexure Interaction Model for RC Walls')+'<br/>') +
		html_end()
		)
	
	# Material_tags
	at_Material_tags = MpcAttributeMetaData()
	at_Material_tags.type = MpcAttributeType.IndexVector
	at_Material_tags.name = 'Material_tags'
	at_Material_tags.group = '-mat'
	at_Material_tags.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Material_tags')+'<br/>') +
		html_par('Array of m macro-fiber nDMaterial* tags') +
		html_par('*SFI_MVLEM element shall be used with nDMaterial '+ html_href('http://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM') +', which is a 2-D plane-stress constitutive relationship representing reinforced concrete panel behavior.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SFI_MVLEM_-_Cyclic_Shear-Flexure_Interaction_Model_for_RC_Walls','SFI MVLEM - Cyclic Shear-Flexure Interaction Model for RC Walls')+'<br/>') +
		html_end()
		)
	at_Material_tags.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Material_tags.indexSource.addAllowedNamespace("materials.nD")
	at_Material_tags.indexSource.addAllowedClass("FSAM")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'SFI_MVLEM'
	xom.addAttribute(at_m)
	xom.addAttribute(at_c)
	xom.addAttribute(at_Thicknesses)
	xom.addAttribute(at_Widths)
	xom.addAttribute(at_Material_tags)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	#Element SFI_MVLEM $eleTag $iNode $jNode $m $c -thick {Thicknesses} -width {Widths} -mat {Material_tags}
	
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
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Line or len(node_vect)!=2:
		raise Exception('Error: invalid type of element or number of nodes')
	
	
	# mandatory parameters
	m_at = xobj.getAttribute('m')
	if(m_at is None):
		raise Exception('Error: cannot find "m" attribute')
	m = m_at.integer
	
	c_at = xobj.getAttribute('c')
	if(c_at is None):
		raise Exception('Error: cannot find "c" attribute')
	c = c_at.real
	
	Thicknesses_at = xobj.getAttribute('Thicknesses')
	if(Thicknesses_at is None):
		raise Exception('Error: cannot find "Thicknesses" attribute')
	Thicknesses = Thicknesses_at.quantityVector
	
	
	if(m != len(Thicknesses)):
		raise Exception('Error: different length between Thicknesses vector and Number of element macro-fibers')
	
	
	Widths_at = xobj.getAttribute('Widths')
	if(Widths_at is None):
		raise Exception('Error: cannot find "Widths" attribute')
	Widths = Widths_at.quantityVector
	
	if(m!=len(Widths)):
		raise Exception('Error: different length between Widths vector and Number of element macro-fibers')
	
	
	Material_tags_at = xobj.getAttribute('Material_tags')
	if(Material_tags_at is None):
		raise Exception('Error: cannot find "Material_tags" attribute')
	Material_tags = Material_tags_at.indexVector
	
	if(m!=len(Material_tags)):
		raise Exception('Error: different length between Material_tags vector and Number of element macro-fibers')
	
	
	Thicknesses_str = ''
	Widths_str = ''
	Material_tags_str = ''
	for i in range(m):
		Thicknesses_str += ' {}'.format(Thicknesses.valueAt(i))
		Widths_str += ' {}'.format(Widths.valueAt(i))
		Material_tags_str += ' {}'.format(Material_tags[i])
	
	
	str_tcl = '{}element SFI_MVLEM {}{} {} {} -thick{} -width{} -mat{}\n'.format(pinfo.indent, tag, nstr, m, c, Thicknesses_str, Widths_str, Material_tags_str)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)