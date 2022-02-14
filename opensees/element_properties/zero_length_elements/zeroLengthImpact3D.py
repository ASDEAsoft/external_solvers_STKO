import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# direction
	at_direction = MpcAttributeMetaData()
	at_direction.type = MpcAttributeType.Integer
	at_direction.name = 'direction'
	at_direction.group = 'Group'
	at_direction.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('direction')+'<br/>') +
		html_par('1 if out-normal vector of master plane points to +X direction') +
		html_par('2 if out-normal vector of master plane points to +Y direction') +
		html_par('3 if out-normal vector of master plane points to +Z direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthImpact3D','ZeroLengthImpact3D')+'<br/>') +
		html_end()
		)
	at_direction.sourceType = MpcAttributeSourceType.List
	at_direction.setSourceList([1, 2, 3])
	at_direction.setDefault(1)
	
	# initGap
	at_initGap = MpcAttributeMetaData()
	at_initGap.type = MpcAttributeType.QuantityScalar
	at_initGap.name = 'initGap'
	at_initGap.group = 'Group'
	at_initGap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('initGap')+'<br/>') +
		html_par('Initial gap between master plane and slave plane') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthImpact3D','ZeroLengthImpact3D')+'<br/>') +
		html_end()
		)
	at_initGap.dimension = u.L
	
	# frictionRatio
	at_frictionRatio = MpcAttributeMetaData()
	at_frictionRatio.type = MpcAttributeType.Real
	at_frictionRatio.name = 'frictionRatio'
	at_frictionRatio.group = 'Group'
	at_frictionRatio.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('frictionRatio')+'<br/>') +
		html_par('Friction ratio in two tangential directions (parallel to master and slave planes)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthImpact3D','ZeroLengthImpact3D')+'<br/>') +
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
		html_par('Penalty in two tangential directions') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthImpact3D','ZeroLengthImpact3D')+'<br/>') +
		html_end()
		)
	
	# Kn
	at_Kn = MpcAttributeMetaData()
	at_Kn.type = MpcAttributeType.Real
	at_Kn.name = 'Kn'
	at_Kn.group = 'Group'
	at_Kn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kn')+'<br/>') +
		html_par('Penalty in normal direction (normal to master and slave planes)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthImpact3D','ZeroLengthImpact3D')+'<br/>') +
		html_end()
		)
	
	# Kn2
	at_Kn2 = MpcAttributeMetaData()
	at_Kn2.type = MpcAttributeType.Real
	at_Kn2.name = 'Kn2'
	at_Kn2.group = 'Group'
	at_Kn2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kn2')+'<br/>') +
		html_par('Penalty in normal direction after yielding based on Hertz impact model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthImpact3D','ZeroLengthImpact3D')+'<br/>') +
		html_end()
		)
	
	# Delta_y
	at_Delta_y = MpcAttributeMetaData()
	at_Delta_y.type = MpcAttributeType.Real
	at_Delta_y.name = 'Delta_y'
	at_Delta_y.group = 'Group'
	at_Delta_y.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Delta_y')+'<br/>') +
		html_par('Yield deformation based on Hertz impact model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthImpact3D','ZeroLengthImpact3D')+'<br/>') +
		html_end()
		)
	
	# cohesion
	at_cohesion = MpcAttributeMetaData()
	at_cohesion.type = MpcAttributeType.QuantityScalar
	at_cohesion.name = 'cohesion'
	at_cohesion.group = 'Group'
	at_cohesion.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cohesion')+'<br/>') +
		html_par('Cohesion, if no cohesion, it is zero') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthImpact3D','ZeroLengthImpact3D')+'<br/>') +
		html_end()
		)
	at_cohesion.dimension = u.F/u.L**2
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLengthImpact3D'
	xom.addAttribute(at_direction)
	xom.addAttribute(at_initGap)
	xom.addAttribute(at_frictionRatio)
	xom.addAttribute(at_Kt)
	xom.addAttribute(at_Kn)
	xom.addAttribute(at_Kn2)
	xom.addAttribute(at_Delta_y)
	xom.addAttribute(at_cohesion)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return[(3,3),(3,3)]

def writeTcl(pinfo):
	
	#element zeroLengthImpact3D $tag $slaveNode $masterNode $direction $initGap $frictionRatio $Kt $Kn $Kn2 $Delta_y $cohesion
	
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
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
	
	if (len(node_vect)!=2):
		raise Exception('Error: invalid number of nodes')
	
	# use reverse iterator because in stko the first is the master node
	# while this command wants the slave node first
	nstr = ' '.join([str(node_id) for node_id in reversed(node_vect)])
	
	# mandatory parameters
	direction_at = xobj.getAttribute('direction')
	if(direction_at is None):
		raise Exception('Error: cannot find "direction" attribute')
	direction = direction_at.integer
	
	initGap_at = xobj.getAttribute('initGap')
	if(initGap_at is None):
		raise Exception('Error: cannot find "initGap" attribute')
	initGap = initGap_at.quantityScalar
	
	frictionRatio_at = xobj.getAttribute('frictionRatio')
	if(frictionRatio_at is None):
		raise Exception('Error: cannot find "frictionRatio" attribute')
	frictionRatio = frictionRatio_at.real
	
	Kt_at = xobj.getAttribute('Kt')
	if(Kt_at is None):
		raise Exception('Error: cannot find "Kt" attribute')
	Kt = Kt_at.real
	
	Kn_at = xobj.getAttribute('Kn')
	if(Kn_at is None):
		raise Exception('Error: cannot find "Kn" attribute')
	Kn = Kn_at.real
	
	Kn2_at = xobj.getAttribute('Kn2')
	if(Kn2_at is None):
		raise Exception('Error: cannot find "Kn2" attribute')
	Kn2 = Kn2_at.real
	
	Delta_y_at = xobj.getAttribute('Delta_y')
	if(Delta_y_at is None):
		raise Exception('Error: cannot find "Delta_y" attribute')
	Delta_y = Delta_y_at.real
	
	cohesion_at = xobj.getAttribute('cohesion')
	if(cohesion_at is None):
		raise Exception('Error: cannot find "cohesion" attribute')
	cohesion = cohesion_at.quantityScalar
	
	str_tcl = '{}element zeroLengthImpact3D {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, nstr, direction, initGap.value, frictionRatio, Kt, Kn, Kn2, Delta_y, cohesion.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)