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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Brick_u-p_Element','Brick u-p Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Brick_u-p_Element','Brick u-p Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Brick_u-p_Element','Brick u-p Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Brick_u-p_Element','Brick u-p Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Brick_u-p_Element','Brick u-p Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Brick_u-p_Element','Brick u-p Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Brick_u-p_Element','Brick u-p Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Brick_u-p_Element','Brick u-p Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Brick_u-p_Element','Brick u-p Element')+'<br/>') +
		html_end()
		)
	at_bZ.setDefault(0.0)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'bbarBrickUP'
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

def getNodalSpatialDim(xobj):
	return [(3,4),(3,4),(3,4),(3,4),(3,4),(3,4),(3,4),(3,4)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	#element bbarBrickUP $eleTag $Node1 $Node2 $Node3 $Node4 $Node5 $Node6 $Node7 $Node8
	#$matTag $bulk $fmass $PermX $PermY $PermZ <$bX=0 $bY=0 $bZ=0>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	pinfo.updateModelBuilder(3,4)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh=phys_prop.XObject.Xnamespace
	if (namePh!='materials.nD'):
		raise Exception('Error: physical property must be "materials.nD" and not: "{}"'.format(namePh))
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Hexahedron or len(node_vect)!=8:
		raise Exception('Error: invalid type of element or number of nodes')
	
	# mandatory parameters
	bulk_at = xobj.getAttribute('bulk')
	if(bulk_at is None):
		raise Exception('Error: cannot find "bulk" attribute')
	bulk = bulk_at.quantityScalar
	
	fmass_at = xobj.getAttribute('fmass')
	if(fmass_at is None):
		raise Exception('Error: cannot find "fmass" attribute')
	fmass = fmass_at.quantityScalar
	
	PermX_at = xobj.getAttribute('PermX')
	if(PermX_at is None):
		raise Exception('Error: cannot find "PermX" attribute')
	PermX = PermX_at.real
	
	PermY_at = xobj.getAttribute('PermY')
	if(PermY_at is None):
		raise Exception('Error: cannot find "PermY" attribute')
	PermY = PermY_at.real
	
	PermZ_at = xobj.getAttribute('PermZ')
	if(PermZ_at is None):
		raise Exception('Error: cannot find "PermZ" attribute')
	PermZ = PermZ_at.real
	
	# optional paramters
	sopt = ''
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		bX_at = xobj.getAttribute('bX')
		if(bX_at is None):
			raise Exception('Error: cannot find "bX" attribute')
		bX = bX_at.real
		
		bY_at = xobj.getAttribute('bY')
		if(bY_at is None):
			raise Exception('Error: cannot find "bY" attribute')
		bY = bY_at.real
		
		bZ_at = xobj.getAttribute('bZ')
		if(bZ_at is None):
			raise Exception('Error: cannot find "bZ" attribute')
		bZ = bZ_at.real
		
		sopt += ' {} {} {}'.format(bX, bY, bZ)
	
	str_tcl = '{}element bbarBrickUP {}{} {} {} {} {} {} {}{}\n'.format(
				pinfo.indent, tag, nstr, matTag, bulk.value, fmass.value, PermX, PermY, PermZ, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)