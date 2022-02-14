import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# frnTag1
	at_frnTag1 = MpcAttributeMetaData()
	at_frnTag1.type = MpcAttributeType.Index
	at_frnTag1.name = 'frnTag1'
	at_frnTag1.group = 'Group'
	at_frnTag1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('frnTag1')+'<br/>') +
		html_par('tag associated with previously-defined '+html_href('http://opensees.berkeley.edu/wiki/index.php/FrictionModel_Command','FrictionModel')+' at the three sliding interfaces') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_frnTag1.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_frnTag1.indexSource.addAllowedNamespace("frictionModel")
	
	# frnTag2
	at_frnTag2 = MpcAttributeMetaData()
	at_frnTag2.type = MpcAttributeType.Index
	at_frnTag2.name = 'frnTag2'
	at_frnTag2.group = 'Group'
	at_frnTag2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('frnTag2')+'<br/>') +
		html_par('tag associated with previously-defined '+html_href('http://opensees.berkeley.edu/wiki/index.php/FrictionModel_Command','FrictionModel')+' at the three sliding interfaces') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_frnTag2.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_frnTag2.indexSource.addAllowedNamespace("frictionModel")
	
	# frnTag3
	at_frnTag3 = MpcAttributeMetaData()
	at_frnTag3.type = MpcAttributeType.Index
	at_frnTag3.name = 'frnTag3'
	at_frnTag3.group = 'Group'
	at_frnTag3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('frnTag3')+'<br/>') +
		html_par('tag associated with previously-defined '+html_href('http://opensees.berkeley.edu/wiki/index.php/FrictionModel_Command','FrictionModel')+' at the three sliding interfaces') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_frnTag3.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_frnTag3.indexSource.addAllowedNamespace("frictionModel")
	
	# L1
	at_L1 = MpcAttributeMetaData()
	at_L1.type = MpcAttributeType.QuantityScalar
	at_L1.name = 'L1'
	at_L1.group = 'Group'
	at_L1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('L1')+'<br/>') +
		html_par('effective radii. Li = R_i - h_i (see Figure 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_L1.dimension = u.L
	
	# L2
	at_L2 = MpcAttributeMetaData()
	at_L2.type = MpcAttributeType.QuantityScalar
	at_L2.name = 'L2'
	at_L2.group = 'Group'
	at_L2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('L2')+'<br/>') +
		html_par('effective radii. Li = R_i - h_i (see Figure 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_L2.dimension = u.L
	
	# L3
	at_L3 = MpcAttributeMetaData()
	at_L3.type = MpcAttributeType.QuantityScalar
	at_L3.name = 'L3'
	at_L3.group = 'Group'
	at_L3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('L3')+'<br/>') +
		html_par('effective radii. Li = R_i - h_i (see Figure 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_L3.dimension = u.L
	
	# d1
	at_d1 = MpcAttributeMetaData()
	at_d1.type = MpcAttributeType.QuantityScalar
	at_d1.name = 'd1'
	at_d1.group = 'Group'
	at_d1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('d1')+'<br/>') +
		html_par('displacement limits of pendulums (Figure 1). Displacement limit of the bearing is 2d1+d2+d3+L1*d3/L3-L1*d2/L2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_d1.dimension = u.L
	
	# d2
	at_d2 = MpcAttributeMetaData()
	at_d2.type = MpcAttributeType.QuantityScalar
	at_d2.name = 'd2'
	at_d2.group = 'Group'
	at_d2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('d2')+'<br/>') +
		html_par('displacement limits of pendulums (Figure 1). Displacement limit of the bearing is 2d1+d2+d3+L1*d3/L3-L1*d2/L2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_d2.dimension = u.L
	
	# d3
	at_d3 = MpcAttributeMetaData()
	at_d3.type = MpcAttributeType.QuantityScalar
	at_d3.name = 'd3'
	at_d3.group = 'Group'
	at_d3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('d3')+'<br/>') +
		html_par('displacement limits of pendulums (Figure 1). Displacement limit of the bearing is 2d1+d2+d3+L1*d3/L3-L1*d2/L2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_d3.dimension = u.L
	
	# W
	at_W = MpcAttributeMetaData()
	at_W.type = MpcAttributeType.QuantityScalar
	at_W.name = 'W'
	at_W.group = 'Group'
	at_W.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('W')+'<br/>') +
		html_par('axial force used for the first trial of the first analysis step.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_W.dimension = u.F
	
	# uy
	at_uy = MpcAttributeMetaData()
	at_uy.type = MpcAttributeType.QuantityScalar
	at_uy.name = 'uy'
	at_uy.group = 'Group'
	at_uy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('uy')+'<br/>') +
		html_par('lateral displacement where sliding of the bearing starts. Recommended value = 0.25 to 1 mm. A smaller value may cause convergence problem.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_uy.dimension = u.L
	
	# kvt
	at_kvt = MpcAttributeMetaData()
	at_kvt.type = MpcAttributeType.QuantityScalar
	at_kvt.name = 'kvt'
	at_kvt.group = 'Group'
	at_kvt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kvt')+'<br/>') +
		html_par('Tension stiffness k_vt of the bearing.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_kvt.dimension = u.F/u.L**2
	
	# minFv
	at_minFv = MpcAttributeMetaData()
	at_minFv.type = MpcAttributeType.QuantityScalar
	at_minFv.name = 'minFv'
	at_minFv.group = 'Group'
	at_minFv.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('minFv')+'<br/>') +
		html_par('(>=0)') +
		html_par('minimum vertical compression force in the bearing used for computing the horizontal tangent stiffness matrix from the normalized tangent stiffness matrix of the element. minFv is substituted for the actual compressive force when it is less than minFv, and prevents the element from using a negative stiffness matrix in the horizontal direction when uplift occurs. The vertical nodal force returned to nodes is always computed from kvc (or kvt) and vertical deformation, and thus is not affected by minFv.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	at_minFv.dimension = u.F
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.QuantityScalar
	at_tol.name = 'tol'
	at_tol.group = 'Group'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('relative tolerance for checking the convergence of the element. Recommended value = 1e-10 to 1e-3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Triple_Friction_Pendulum_Element','Triple Friction Pendulum Element')+'<br/>') +
		html_end()
		)
	
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'TripleFrictionPendulum'
	xom.addAttribute(at_frnTag1)
	xom.addAttribute(at_frnTag2)
	xom.addAttribute(at_frnTag3)
	xom.addAttribute(at_L1)
	xom.addAttribute(at_L2)
	xom.addAttribute(at_L3)
	xom.addAttribute(at_d1)
	xom.addAttribute(at_d2)
	xom.addAttribute(at_d3)
	xom.addAttribute(at_W)
	xom.addAttribute(at_uy)
	xom.addAttribute(at_kvt)
	xom.addAttribute(at_minFv)
	xom.addAttribute(at_tol)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)] #(ndm, ndf)

def writeTcl(pinfo):
	
	# element TripleFrictionPendulum $eleTag $iNode $jNode $frnTag1 $frnTag2 $frnTag3 $vertMatTag $rotZMatTag $rotXMatTag $rotYMatTag $L1 $L2 $L3 $d1 $d2 $d3 $W $uy $kvt $minFv $tol
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect) != 2):
		raise Exception('Error: invalid number of nodes')
	
	# mandatory parameters
	frnTag1_at = xobj.getAttribute('frnTag1')
	if(frnTag1_at is None):
		raise Exception('Error: cannot find "frnTag1" attribute')
	frnTag1 = frnTag1_at.index
	
	frnTag2_at = xobj.getAttribute('frnTag2')
	if(frnTag2_at is None):
		raise Exception('Error: cannot find "frnTag2" attribute')
	frnTag2 = frnTag2_at.index
	
	frnTag3_at = xobj.getAttribute('frnTag3')
	if(frnTag3_at is None):
		raise Exception('Error: cannot find "frnTag3" attribute')
	frnTag3 = frnTag3_at.index
	
	# special_purpose
	if phys_prop.XObject.name != 'TripleFrictionPendulumMaterial':
		raise Exception('Wrong material type for "TripleFrictionPendulum" element. Expected: "TripleFrictionPendulumMaterial", given: "{}"'.format(phys_prop.XObject.name))
	
	vertMatTag_at = phys_prop.XObject.getAttribute('vertMatTag')
	if(vertMatTag_at is None):
		raise Exception('Error: cannot find "vertMatTag" attribute')
	vertMatTag=vertMatTag_at.index
	
	rotZMatTag_at = phys_prop.XObject.getAttribute('rotZMatTag')
	if(rotZMatTag_at is None):
		raise Exception('Error: cannot find "rotZMatTag" attribute')
	rotZMatTag=rotZMatTag_at.index
	
	rotXMatTag_at = phys_prop.XObject.getAttribute('rotXMatTag')
	if(rotXMatTag_at is None):
		raise Exception('Error: cannot find "rotXMatTag" attribute')
	rotXMatTag=rotXMatTag_at.index
	
	rotYMatTag_at = phys_prop.XObject.getAttribute('rotYMatTag')
	if(rotYMatTag_at is None):
		raise Exception('Error: cannot find "rotYMatTag" attribute')
	rotYMatTag=rotYMatTag_at.index
	
	# mandatory parameters
	L1_at = xobj.getAttribute('L1')
	if(L1_at is None):
		raise Exception('Error: cannot find "L1" attribute')
	L1 = L1_at.quantityScalar.value
	
	L2_at = xobj.getAttribute('L2')
	if(L2_at is None):
		raise Exception('Error: cannot find "L2" attribute')
	L2 = L2_at.quantityScalar.value
	
	L3_at = xobj.getAttribute('L3')
	if(L3_at is None):
		raise Exception('Error: cannot find "L3" attribute')
	L3 = L3_at.quantityScalar.value
	
	d1_at = xobj.getAttribute('d1')
	if(d1_at is None):
		raise Exception('Error: cannot find "d1" attribute')
	d1 = d1_at.quantityScalar.value
	
	d2_at = xobj.getAttribute('d2')
	if(d2_at is None):
		raise Exception('Error: cannot find "d2" attribute')
	d2 = d2_at.quantityScalar.value
	
	d3_at = xobj.getAttribute('d3')
	if(d3_at is None):
		raise Exception('Error: cannot find "d3" attribute')
	d3 = d3_at.quantityScalar.value
	
	W_at = xobj.getAttribute('W')
	if(W_at is None):
		raise Exception('Error: cannot find "W" attribute')
	W = W_at.quantityScalar.value
	
	uy_at = xobj.getAttribute('uy')
	if(uy_at is None):
		raise Exception('Error: cannot find "uy" attribute')
	uy = uy_at.quantityScalar.value
	
	kvt_at = xobj.getAttribute('kvt')
	if(kvt_at is None):
		raise Exception('Error: cannot find "kvt" attribute')
	kvt = kvt_at.quantityScalar.value
	
	minFv_at = xobj.getAttribute('minFv')
	if(minFv_at is None):
		raise Exception('Error: cannot find "minFv" attribute')
	minFv = minFv_at.quantityScalar.value
	
	tol_at = xobj.getAttribute('tol')
	if(tol_at is None):
		raise Exception('Error: cannot find "tol" attribute')
	tol = tol_at.quantityScalar.value
	
	
	str_tcl = '{}element TripleFrictionPendulum {}{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, nstr, frnTag1, frnTag2, frnTag3, vertMatTag, rotXMatTag, rotXMatTag, rotYMatTag, L1,
			L2, L3, d1, d2, d3, W, uy, kvt, minFv, tol)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)