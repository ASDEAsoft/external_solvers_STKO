import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# numIntgrPts
	at_numIntgrPts = MpcAttributeMetaData()
	at_numIntgrPts.type = MpcAttributeType.Integer
	at_numIntgrPts.name = 'numIntgrPts'
	at_numIntgrPts.group = 'Group'
	at_numIntgrPts.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIntgrPts')+'<br/>') +
		html_par('number of integration points along the element.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Flexure-Shear_Interaction_Displacement-Based_Beam-Column_Element','Flexure-Shear Interaction Displacement-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# cRot
	at_cRot = MpcAttributeMetaData()
	at_cRot.type = MpcAttributeType.Real
	at_cRot.name = 'cRot'
	at_cRot.group = 'Group'
	at_cRot.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cRot')+'<br/>') +
		html_par('identifier for element center of rotation (or center of curvature distribution). Fraction of the height distance from bottom to the center of rotation (0 to 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Flexure-Shear_Interaction_Displacement-Based_Beam-Column_Element','Flexure-Shear Interaction Displacement-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# -mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.Boolean
	at_mass.name = '-mass'
	at_mass.group = 'Group'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mass')+'<br/>') +
		html_par('element mass density (per unit length), from which a lumped-mass matrix is formed (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Flexure-Shear_Interaction_Displacement-Based_Beam-Column_Element','Flexure-Shear Interaction Displacement-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# massDens
	at_massDens = MpcAttributeMetaData()
	at_massDens.type = MpcAttributeType.QuantityScalar
	at_massDens.name = 'massDens'
	at_massDens.group = '-mass'
	at_massDens.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('massDens')+'<br/>') +
		html_par('element mass density (per unit length), from which a lumped-mass matrix is formed (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Flexure-Shear_Interaction_Displacement-Based_Beam-Column_Element','Flexure-Shear Interaction Displacement-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_massDens.setDefault(0.0)
	# at_massDens.dimension = u.M/u.L**3
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'dispBeamColumnInt'
	xom.addAttribute(at_numIntgrPts)
	xom.addAttribute(at_cRot)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_massDens)
	
	
	# visibility dependencies
	
	# massDens-dep
	xom.setVisibilityDependency(at_mass, at_massDens)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3)]	#(ndm,ndf)

def writeTcl(pinfo):
	
	#element dispBeamColumnInt $eleTag $iNode $jNode $numIntgrPts $secTag $transfTag $cRot <-mass $massDens>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	pinfo.updateModelBuilder(2,3)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh = phys_prop.XObject.Xnamespace
	if (namePh!='sections'):
		raise Exception('Error: physical property must be "sections" and not: "{}"'.format(namePh))
	
	secTag = phys_prop.id
	
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Line or len(node_vect)!=2:
		raise Exception('Error: invalid type of element or number of nodes')
	
	
	# mandatory parameters
	numIntgrPts_at = xobj.getAttribute('numIntgrPts')
	if(numIntgrPts_at is None):
		raise Exception('Error: cannot find "numIntgrPts" attribute')
	numIntgrPts = numIntgrPts_at.integer
	
	cRot_at = xobj.getAttribute('cRot')
	if(cRot_at is None):
		raise Exception('Error: cannot find "cRot" attribute')
	cRot = cRot_at.real
	
	
	# optional paramters
	sopt = ''
	
	mass_at = xobj.getAttribute('-mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "-mass" attribute')
	mass = mass_at.boolean
	if mass:
		massDens_at = xobj.getAttribute('massDens')
		if(massDens_at is None):
			raise Exception('Error: cannot find "massDens" attribute')
		massDens = massDens_at.quantityScalar
		
		sopt += '-mass {}'.format(massDens.value)
	
	
	# Geometric Transformation Command
	geomTransf = '\n# Geometric transformation command\n'
	geomTransf += 'geomTransf LinearInt {}'.format(tag)
	
	vect_z = elem.orientation.computeOrientation().col(2)
	geomTransf += ' {} {} {}'.format(vect_z.x, vect_z.y, vect_z.z)
	geomTransf += '\n'
	
	# now write the geomTransf into the file
	pinfo.out_file.write(geomTransf)
	
	
	str_tcl = '{}element dispBeamColumnInt {}{} {} {} {} {} {}\n'.format(pinfo.indent, tag, nstr, numIntgrPts, secTag, tag, cRot, sopt)
	
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)