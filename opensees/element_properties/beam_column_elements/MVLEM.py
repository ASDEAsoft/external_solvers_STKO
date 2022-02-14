import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Dens
	at_Dens = MpcAttributeMetaData()
	at_Dens.type = MpcAttributeType.QuantityScalar
	at_Dens.name = 'Dens'
	at_Dens.group = 'Group'
	at_Dens.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dens')+'<br/>') +
		html_par('Wall density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls','MVLEM - Multiple-Vertical-Line-Element-Model for RC Walls')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.Integer
	at_m.name = 'm'
	at_m.group = 'Group'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') +
		html_par('Number of element macro-fibers') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls','MVLEM - Multiple-Vertical-Line-Element-Model for RC Walls')+'<br/>') +
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
		html_par('Location of center of rotation from the iNode, c = 0.4 (recommended)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls','MVLEM - Multiple-Vertical-Line-Element-Model for RC Walls')+'<br/>') +
		html_end()
		)
	
	# Thicknesses
	at_Thicknesses = MpcAttributeMetaData()
	at_Thicknesses.type = MpcAttributeType.QuantityVector
	at_Thicknesses.name = 'Thicknesses'
	at_Thicknesses.group = 'Group'
	at_Thicknesses.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Thicknesses')+'<br/>') +
		html_par('Array of m macro-fiber thicknesses') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls','MVLEM - Multiple-Vertical-Line-Element-Model for RC Walls')+'<br/>') +
		html_end()
		)
	
	# Widths
	at_Widths = MpcAttributeMetaData()
	at_Widths.type = MpcAttributeType.QuantityVector
	at_Widths.name = 'Widths'
	at_Widths.group = 'Group'
	at_Widths.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Widths')+'<br/>') +
		html_par('Array of m macro-fiber widths') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls','MVLEM - Multiple-Vertical-Line-Element-Model for RC Walls')+'<br/>') +
		html_end()
		)
	
	# Reinforcing_ratios
	at_Reinforcing_ratios = MpcAttributeMetaData()
	at_Reinforcing_ratios.type = MpcAttributeType.QuantityVector
	at_Reinforcing_ratios.name = 'Reinforcing_ratios'
	at_Reinforcing_ratios.group = 'Group'
	at_Reinforcing_ratios.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Reinforcing_ratios')+'<br/>') +
		html_par('Array of m reinforcing ratios corresponding to macro-fibers; for each fiber: rhoi = As,i/Agross,i (1 < i < m)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls','MVLEM - Multiple-Vertical-Line-Element-Model for RC Walls')+'<br/>') +
		html_end()
		)
	
	# Concrete_tags
	at_Concrete_tags = MpcAttributeMetaData()
	at_Concrete_tags.type = MpcAttributeType.IndexVector
	at_Concrete_tags.name = 'Concrete_tags'
	at_Concrete_tags.group = 'Group'
	at_Concrete_tags.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Concrete_tags')+'<br/>') +
		html_par('Array of m uniaxialMaterial tags for concrete') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls','MVLEM - Multiple-Vertical-Line-Element-Model for RC Walls')+'<br/>') +
		html_end()
		)
	at_Concrete_tags.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Concrete_tags.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Steel_tags
	at_Steel_tags = MpcAttributeMetaData()
	at_Steel_tags.type = MpcAttributeType.IndexVector
	at_Steel_tags.name = 'Steel_tags'
	at_Steel_tags.group = 'Group'
	at_Steel_tags.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Steel_tags')+'<br/>') +
		html_par('Array of m uniaxialMaterial tags for steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls','MVLEM - Multiple-Vertical-Line-Element-Model for RC Walls')+'<br/>') +
		html_end()
		)
	at_Steel_tags.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Steel_tags.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# Shear_tag
	at_Shear_tag = MpcAttributeMetaData()
	at_Shear_tag.type = MpcAttributeType.Index
	at_Shear_tag.name = 'Shear_tag'
	at_Shear_tag.group = 'Group'
	at_Shear_tag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Shear_tag')+'<br/>') +
		html_par('Tag of uniaxialMaterial for shear material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls','MVLEM - Multiple-Vertical-Line-Element-Model for RC Walls')+'<br/>') +
		html_end()
		)
	at_Shear_tag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Shear_tag.indexSource.addAllowedNamespace("materials.uniaxial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'MVLEM'
	xom.addAttribute(at_Dens)
	xom.addAttribute(at_m)
	xom.addAttribute(at_c)
	xom.addAttribute(at_Thicknesses)
	xom.addAttribute(at_Widths)
	xom.addAttribute(at_Reinforcing_ratios)
	xom.addAttribute(at_Concrete_tags)
	xom.addAttribute(at_Steel_tags)
	xom.addAttribute(at_Shear_tag)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3)] # ndm, ndf

def writeTcl(pinfo):
	# Element MVLEM $eleTag $Dens $iNode $jNode $m $c -thick {Thicknesses} -width {Widths} -rho {Reinforcing_ratios} -matConcrete {Concrete_tags} -matSteel {Steel_tags} -matShear {Shear_tag}
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# mandatory parameters
	Dens_at = xobj.getAttribute('Dens')
	if(Dens_at is None):
		raise Exception('Error: cannot find "Dens" attribute')
	Dens = Dens_at.quantityScalar.value
	
	namePh=phys_prop.XObject.Xnamespace
	if (namePh!='materials.uniaxial'):
		raise Exception('Error: material must be uniaxial')
		
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += '{} '.format(node.id)
	
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Line or len(node_vect)!=2:
		raise Exception('Error: invalid type of element or number of nodes')
	
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
	
	if len(Thicknesses)!= m:
		raise Exception('Error: different length between Thicknesses vector and Number of element macro-fibers')
	
	Widths_at = xobj.getAttribute('Widths')
	if(Widths_at is None):
		raise Exception('Error: cannot find "Widths" attribute')
	Widths = Widths_at.quantityVector
	
	if len(Widths)!= m:
		raise Exception('Error: different length between Widths vector and Number of element macro-fibers')
	
	Reinforcing_ratios_at = xobj.getAttribute('Reinforcing_ratios')
	if(Reinforcing_ratios_at is None):
		raise Exception('Error: cannot find "Reinforcing_ratios" attribute')
	Reinforcing_ratios = Reinforcing_ratios_at.quantityVector
	
	if len(Reinforcing_ratios)!= m:
		raise Exception('Error: different length between Reinforcing_ratios vector and Number of element macro-fibers')
	
	Concrete_tags_at = xobj.getAttribute('Concrete_tags')
	if(Concrete_tags_at is None):
		raise Exception('Error: cannot find "Concrete_tags" attribute')
	Concrete_tags = Concrete_tags_at.indexVector
	
	if len(Concrete_tags)!= m:
		raise Exception('Error: different length between Concrete_tags vector and Number of element macro-fibers')
		
	Steel_tags_at = xobj.getAttribute('Steel_tags')
	if(Steel_tags_at is None):
		raise Exception('Error: cannot find "Steel_tags" attribute')
	Steel_tags = Steel_tags_at.indexVector
	if len(Steel_tags)!= m:
		raise Exception('Error: different length between Steel_tags vector and Number of element macro-fibers')
	
	Thicknesses_str=''
	Widths_str=''
	Reinforcing_ratios_str=''
	Concrete_tags_str=''
	Steel_tags_str=''
	
	
	for i in range(m):
		Thicknesses_str += ' {}'.format(Thicknesses.valueAt(i))
		Widths_str += ' {}'.format(Widths.valueAt(i))
		Reinforcing_ratios_str += ' {}'.format(Reinforcing_ratios.valueAt(i))
		Concrete_tags_str += ' {}'.format(Concrete_tags[i])
		Steel_tags_str += ' {}'.format(Steel_tags[i])
	
	Shear_tag_at = xobj.getAttribute('Shear_tag')
	if(Shear_tag_at is None):
		raise Exception('Error: cannot find "Shear_tag" attribute')
	Shear_tag = Shear_tag_at.index
	
	# Element MVLEM $eleTag $Dens $iNode $jNode $m $c -thick {Thicknesses} -width {Widths} -rho {Reinforcing_ratios} -matConcrete {Concrete_tags} -matSteel {Steel_tags} -matShear {Shear_tag}

	str_tcl = '{}element MVLEM {} {}{} {} {} -thick{} -thick{} -rho{} -matConcrete{} -matSteel{} -matShear {}{}\n'.format(pinfo.indent, tag, Dens, nstr, m, c, Thicknesses_str, Widths_str, Reinforcing_ratios_str, Concrete_tags_str, Steel_tags_str, Shear_tag)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)