import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# bulk
	at_bulk = MpcAttributeMetaData()
	at_bulk.type = MpcAttributeType.QuantityScalar
	at_bulk.name = 'bulk'
	at_bulk.group = 'Group'
	at_bulk.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bulk')+'<br/>') +
		html_par('Combined undrained bulk modulus Bc relating changes in pore pressure and volumetric strain, may be approximated by:') +
		html_par('Bc ≈ Bf/n') +
		html_par('where Bf is the bulk modulus of fluid phase (2.2x10^6 kPa (or 3.191x10^5 psi) for water), and n the initial porosity.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Twenty_Eight_Node_Brick_u-p_Element','20-8 Node Brick u-p Element')+'<br/>') +
		html_end()
		)
	at_bulk.dimension = u.F/u.L**2
	
	# fmass
	at_fmass = MpcAttributeMetaData()
	at_fmass.type = MpcAttributeType.QuantityScalar
	at_fmass.name = 'fmass'
	at_fmass.group = 'Group'
	at_fmass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fmass')+'<br/>') +
		html_par('Fluid mass density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Twenty_Eight_Node_Brick_u-p_Element','20-8 Node Brick u-p Element')+'<br/>') +
		html_end()
		)
	# at_fmass.dimension = u.M
	
	# PermX
	at_PermX = MpcAttributeMetaData()
	at_PermX.type = MpcAttributeType.Real
	at_PermX.name = 'PermX'
	at_PermX.group = 'Group'
	at_PermX.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('PermX')+'<br/>') +
		html_par('Permeability coefficient in x direction.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Twenty_Eight_Node_Brick_u-p_Element','20-8 Node Brick u-p Element')+'<br/>') +
		html_end()
		)
	
	# PermY
	at_PermY = MpcAttributeMetaData()
	at_PermY.type = MpcAttributeType.Real
	at_PermY.name = 'PermY'
	at_PermY.group = 'Group'
	at_PermY.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('PermY')+'<br/>') +
		html_par('Permeability coefficient in y direction.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Twenty_Eight_Node_Brick_u-p_Element','20-8 Node Brick u-p Element')+'<br/>') +
		html_end()
		)
	
	# PermZ
	at_PermZ = MpcAttributeMetaData()
	at_PermZ.type = MpcAttributeType.Real
	at_PermZ.name = 'PermZ'
	at_PermZ.group = 'Group'
	at_PermZ.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('PermZ')+'<br/>') +
		html_par('Permeability coefficient in z direction.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Twenty_Eight_Node_Brick_u-p_Element','20-8 Node Brick u-p Element')+'<br/>') +
		html_end()
		)
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Group'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') +
		html_par('to activate bX, bY and bZ') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Twenty_Eight_Node_Brick_u-p_Element','20-8 Node Brick u-p Element')+'<br/>') +
		html_end()
		)
	
	# bX
	at_bX = MpcAttributeMetaData()
	at_bX.type = MpcAttributeType.Real
	at_bX.name = 'bX'
	at_bX.group = 'Optional parameters'
	at_bX.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bX')+'<br/>') +
		html_par('Optional gravity acceleration component in x direction (default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Twenty_Eight_Node_Brick_u-p_Element','20-8 Node Brick u-p Element')+'<br/>') +
		html_end()
		)
	at_bX.setDefault(0.0)
	
	# bY
	at_bY = MpcAttributeMetaData()
	at_bY.type = MpcAttributeType.Real
	at_bY.name = 'bY'
	at_bY.group = 'Optional parameters'
	at_bY.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bY')+'<br/>') +
		html_par('Optional gravity acceleration component in y direction (default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Twenty_Eight_Node_Brick_u-p_Element','20-8 Node Brick u-p Element')+'<br/>') +
		html_end()
		)
	at_bY.setDefault(0.0)
	
	# bZ
	at_bZ = MpcAttributeMetaData()
	at_bZ.type = MpcAttributeType.Real
	at_bZ.name = 'bZ'
	at_bZ.group = 'Optional parameters'
	at_bZ.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bZ')+'<br/>') +
		html_par('Optional gravity acceleration component in z direction (default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Twenty_Eight_Node_Brick_u-p_Element','20-8 Node Brick u-p Element')+'<br/>') +
		html_end()
		)
	at_bZ.setDefault(0.0)
	
	
	xom = MpcXObjectMetaData()
	xom.name = '20_8_BrickUP'
	xom.addAttribute(at_bulk)
	xom.addAttribute(at_fmass)
	xom.addAttribute(at_PermX)
	xom.addAttribute(at_PermY)
	xom.addAttribute(at_PermZ)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_bX)
	xom.addAttribute(at_bY)
	xom.addAttribute(at_bZ)
	
	
	# visibility dependencies
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_bX)
	xom.setVisibilityDependency(at_Optional, at_bY)
	xom.setVisibilityDependency(at_Optional, at_bZ)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,4),(3,4),(3,4),(3,4),(3,4),(3,4),(3,4),(3,4),
			(3,3),(3,3),(3,3),(3,3),
			(3,3),(3,3),(3,3),(3,3),
			(3,3),(3,3),(3,3),(3,3)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	#element 20_8_BrickUP $eleTag $Node1 ... $Node20 $matTag $bulk $fmass $PermX $PermY $PermZ <$bX=0 $bY=0 $bZ=0>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	# checks
	if phys_prop is None:
		raise Exception('Missing physical property for element {} ("{}")'.format(elem.id, xobj.name))
	if not phys_prop.XObject.Xnamespace.startswith('materials.nD'):
		raise Exception('Physical property must be "materials.nD" and not: "{}"'.format(phys_prop.XObject.Xnamespace))
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Hexahedron) or (len(elem.nodes) != 20):
		raise Exception('Invalid element type for "{}", expected Hexahedron with 20 nodes, given {} with {} nodes'.format(elem.geometryFamilyType(), len(elem.nodes)))
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# set spatial dimension/dofs. actually the command to create this element only checks for ndm = 3
	# not the ndf... because anyway this element needs nodes with 4 dofs and nodes with 3 dofs.
	pinfo.updateModelBuilder(3,4)
	
	# write a comment
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# nodes
	# note that nodes in opensees for the 20-node hexa does not follow the convention used in STKO
	# that's why we use the following permutation
	nstr = ' '.join([str(elem.nodes[i].id) for i in [0,1,2,3,   4,5,6,7,   8,9,10,11,   16,17,18,19,   12,13,14,15]])
	
	# util to get attribute
	def get_attr(pname):
		at = xobj.getAttribute(pname)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(pname))
		return at
	
	# mandatory parameters
	bulk = get_attr('bulk').quantityScalar.value
	fmass = get_attr('fmass').quantityScalar.value
	PermX = get_attr('PermX').real
	PermY = get_attr('PermY').real
	PermZ = get_attr('PermZ').real
	
	# optional paramters
	sopt = ''
	if get_attr('Optional').boolean:
		bX = get_attr('bX').real
		bY = get_attr('bY').real
		bZ = get_attr('bZ').real
		sopt += ' {} {} {}'.format(bX, bY, bZ)

	# now write the string into the file
	pinfo.out_file.write(
		'{}element 20_8_BrickUP {} {} {} {} {} {} {} {}{}\n'.format(
		pinfo.indent, tag, nstr, matTag, bulk, fmass, PermX, PermY, PermZ, sopt)
		)