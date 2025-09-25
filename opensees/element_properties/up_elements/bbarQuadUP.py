import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# thick
	at_thick = MpcAttributeMetaData()
	at_thick.type = MpcAttributeType.QuantityScalar
	at_thick.name = 'thick'
	at_thick.group = 'Group'
	at_thick.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('thick')+'<br/>') +
		html_par('Element thickness') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/BbarQuad_u-p_Element','BbarQuad u-p Element')+'<br/>') +
		html_end()
		)
	at_thick.dimension = u.L
	
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
		html_par('where Bf is the bulk modulus of fluid phase (2.2x106 kPa (or 3.191x105 psi) for water), and n the initial porosity.') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/BbarQuad_u-p_Element','BbarQuad u-p Element')+'<br/>') +
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
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/BbarQuad_u-p_Element','BbarQuad u-p Element')+'<br/>') +
		html_end()
		)
	# at_fmass.dimension = u.M
	
	# hPerm
	at_hPerm = MpcAttributeMetaData()
	at_hPerm.type = MpcAttributeType.Real
	at_hPerm.name = 'hPerm'
	at_hPerm.group = 'Group'
	at_hPerm.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('hPerm')+'<br/>') +
		html_par('Permeability coefficient in horizontal direction.') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/BbarQuad_u-p_Element','BbarQuad u-p Element')+'<br/>') +
		html_end()
		)
	
	# vPerm
	at_vPerm = MpcAttributeMetaData()
	at_vPerm.type = MpcAttributeType.Real
	at_vPerm.name = 'vPerm'
	at_vPerm.group = 'Group'
	at_vPerm.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vPerm')+'<br/>') +
		html_par('Permeability coefficient in vertical direction.') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/BbarQuad_u-p_Element','BbarQuad u-p Element')+'<br/>') +
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
		html_par('to activate b1, b2 and t') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/BbarQuad_u-p_Element','BbarQuad u-p Element')+'<br/>') +
		html_end()
		)
	
	# b1
	at_b1 = MpcAttributeMetaData()
	at_b1.type = MpcAttributeType.Real
	at_b1.name = 'b1'
	at_b1.group = 'Optional parameters'
	at_b1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b1')+'<br/>') +
		html_par('Optional gravity acceleration components in horizontal direction (defaults are 0.0)') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/BbarQuad_u-p_Element','BbarQuad u-p Element')+'<br/>') +
		html_end()
		)
	at_b1.setDefault(0.0)
	
	# b2
	at_b2 = MpcAttributeMetaData()
	at_b2.type = MpcAttributeType.Real
	at_b2.name = 'b2'
	at_b2.group = 'Optional parameters'
	at_b2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b2')+'<br/>') +
		html_par('Optional gravity acceleration components in vertical direction (defaults are 0.0)') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/BbarQuad_u-p_Element','BbarQuad u-p Element')+'<br/>') +
		html_end()
		)
	at_b2.setDefault(0.0)
	
	# t
	at_t = MpcAttributeMetaData()
	at_t.type = MpcAttributeType.QuantityScalar
	at_t.name = 't'
	at_t.group = 'Optional parameters'
	at_t.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('t')+'<br/>') +
		html_par('Optional uniform element normal traction, positive in tension (default is 0.0)') +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/BbarQuad_u-p_Element','BbarQuad u-p Element')+'<br/>') +
		html_end()
		)
	at_t.setDefault(0.0)
	at_t.dimension = u.F
	
	xom = MpcXObjectMetaData()
	xom.name = 'bbarQuadUP'
	xom.addAttribute(at_thick)
	xom.addAttribute(at_bulk)
	xom.addAttribute(at_fmass)
	xom.addAttribute(at_hPerm)
	xom.addAttribute(at_vPerm)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_b1)
	xom.addAttribute(at_b2)
	xom.addAttribute(at_t)
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_b1)
	xom.setVisibilityDependency(at_Optional, at_b2)
	xom.setVisibilityDependency(at_Optional, at_t)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3),(2,3),(2,3)]	# ndm, ndf

def writeTcl(pinfo):
	
	# element bbarQuadUP $eleTag $iNode $jNode $kNode $lNode $thick $matTag $bulk $fmass $hPerm $vPerm <$b1=0 $b2=0 $t=0>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	# checks
	if phys_prop is None:
		raise Exception('Missing physical property for element {} ("{}")'.format(elem.id, xobj.name))
	if phys_prop.XObject.Xnamespace != 'materials.nD':
		raise Exception('Physical property must be "materials.nD" and not: "{}"'.format(phys_prop.XObject.Xnamespace))
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral) or (len(elem.nodes) != 4):
		raise Exception('Invalid element type for "{}", expected Quadrilateral with 4 nodes, given {} with {} nodes'.format(elem_prop.name, elem.geometryFamilyType(), len(elem.nodes)))
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# update model
	pinfo.updateModelBuilder(2, 3)
	
	# write description
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# util to get attribute
	def get_attr(pname):
		at = xobj.getAttribute(pname)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(pname))
		return at
	
	# mandatory parameters
	thick = get_attr('thick').quantityScalar.value
	bulk = get_attr('bulk').quantityScalar.value
	fmass = get_attr('fmass').quantityScalar.value
	hPerm = get_attr('hPerm').real
	vPerm = get_attr('vPerm').real
	
	# optional paramters
	sopt = ''
	if get_attr('Optional').boolean:
		b1 = get_attr('b1').real
		b2 = get_attr('b2').real
		t = get_attr('t').quantityScalar.value
		sopt = '{} {} {}'.format(b1, b2, t)
		
	# node string
	nstr = ' '.join([str(elem.nodes[i].id) for i in range(len(elem.nodes))])
	
	# now write the string into the file
	pinfo.out_file.write(
		'{}element bbarQuadUP {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, nstr, thick, matTag, bulk, fmass, hPerm, vPerm, sopt)
		)
