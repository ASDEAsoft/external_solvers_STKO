import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.element_properties.utils.geomTransf as gtran
import itertools

def internalBeamFunction(xom):
	
	# transType
	at_transType = gtran.makeAttribute('Group')
	
	# -mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.Boolean
	at_mass.name = '-mass'
	at_mass.group = 'Group'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mass')+'<br/>') +
		html_par('element mass density (per unit length), from which a lumped-mass matrix is formed (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement-Based_Beam-Column_Element','Displacement-Based Beam-Column Element')+'<br/>') +
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
		html_par('element mass density (per unit length), from which a lumped-mass matrix is formed (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement-Based_Beam-Column_Element','Displacement-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_massDens.setDefault(0.0)
	
	xom.addAttribute(at_transType)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_massDens)
	
	# massDens-dep
	xom.setVisibilityDependency(at_mass, at_massDens)


def __option1(phys_prop):
	# StandardIntegrationTypes
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType/1')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	secTag_at = phys_prop.XObject.getAttribute('secTag/1')
	if(secTag_at is None):
		raise Exception('Error: cannot find "secTag" attribute')
	secTag = secTag_at.index
	
	numIntPts_at = phys_prop.XObject.getAttribute('numIntPts/1')
	if(numIntPts_at is None):
		raise Exception('Error: cannot find "numIntPts" attribute')
	numIntPts = numIntPts_at.integer
	
	return ('{} {} {}'.format(IntegrationType, secTag, numIntPts))

def __option2(phys_prop):
	# UserDefined
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType/2')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	numIntPts_at = phys_prop.XObject.getAttribute('numIntPts/2')
	if(numIntPts_at is None):
		raise Exception('Error: cannot find "numIntPts" attribute')
	numIntPts = numIntPts_at.integer
	
	secTag_at = phys_prop.XObject.getAttribute('secTag/2')
	if(secTag_at is None):
		raise Exception('Error: cannot find "secTag" attribute')
	secTag = secTag_at.indexVector
	
	positions_at = phys_prop.XObject.getAttribute('positions/2')
	if(positions_at is None):
		raise Exception('Error: cannot find "positions" attribute')
	positions = positions_at.quantityVector
	
	weights_at = phys_prop.XObject.getAttribute('weights/2')
	if(weights_at is None):
		raise Exception('Error: cannot find "weights" attribute')
	weights = weights_at.quantityVector
	
	if numIntPts < 1:
		raise Exception ('Error: insufficient "numIntPts" ')
	if numIntPts!= (len(secTag))!= (len(positions)):
		raise Exception('Error: incorrect length between vectors "secTag" and "positions" with "numIntPts"')
	
	secTag_ = ''
	positions_=''
	weights_=''
	for i in range(len(secTag)):
		secTag_ += ' {}'.format(secTag[i])
		positions_ += ' {}'.format(positions.valueAt(i))
		weights_ += ' {}'.format(weights.valueAt(i))
	
	return ('{} {}{}{}{}'.format(IntegrationType, numIntPts, secTag_, positions_, weights_))

def __option3(phys_prop):
	# Hinge
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType/3')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	secTagI_at = phys_prop.XObject.getAttribute('secTagI/3')
	if(secTagI_at is None):
		raise Exception('Error: cannot find "secTagI" attribute')
	secTagI = secTagI_at.index
	
	lpI_at = phys_prop.XObject.getAttribute('lpI/3')
	if(lpI_at is None):
		raise Exception('Error: cannot find "lpI" attribute')
	lpI = lpI_at.quantityScalar.value
	
	secTagJ_at = phys_prop.XObject.getAttribute('secTagJ/3')
	if(secTagJ_at is None):
		raise Exception('Error: cannot find "secTagJ" attribute')
	secTagJ = secTagJ_at.index
	
	lpJ_at = phys_prop.XObject.getAttribute('lpJ/3')
	if(lpJ_at is None):
		raise Exception('Error: cannot find "lpJ" attribute')
	lpJ = lpJ_at.quantityScalar.value
	
	secTagE_at = phys_prop.XObject.getAttribute('secTagE/3')
	if(secTagE_at is None):
		raise Exception('Error: cannot find "secTagE" attribute')
	secTagE = secTagE_at.index
	
	return ('{} {} {} {} {} {}'.format(IntegrationType, secTagI, lpI, secTagJ, lpJ, secTagE))

def __option4(phys_prop):
	# UserHinge
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType/4')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	secTagE_at = phys_prop.XObject.getAttribute('secTagE/4')
	if(secTagE_at is None):
		raise Exception('Error: cannot find "secTagE" attribute')
	secTagE = secTagE_at.index
	
	npI_at = phys_prop.XObject.getAttribute('npI')
	if(npI_at is None):
		raise Exception('Error: cannot find "npI" attribute')
	npI = npI_at.integer
	
	npJ_at = phys_prop.XObject.getAttribute('npJ')
	if(npJ_at is None):
		raise Exception('Error: cannot find "npJ" attribute')
	npJ = npJ_at.integer
	
	secTagI_at = phys_prop.XObject.getAttribute('secTagI/4')
	if(secTagI_at is None):
		raise Exception('Error: cannot find "secTagI" attribute')
	secTagI = secTagI_at.indexVector
	
	positionsI_at = phys_prop.XObject.getAttribute('positionsI')
	if(positionsI_at is None):
		raise Exception('Error: cannot find "positionsI" attribute')
	positionsI = positionsI_at.quantityVector
	
	weightsI_at = phys_prop.XObject.getAttribute('weightsI')
	if(weightsI_at is None):
		raise Exception('Error: cannot find "weightsI" attribute')
	weightsI = weightsI_at.quantityVector
	
	secTagJ_at = phys_prop.XObject.getAttribute('secTagJ/4')
	if(secTagJ_at is None):
		raise Exception('Error: cannot find "secTagJ" attribute')
	secTagJ = secTagJ_at.indexVector
	
	positionsJ_at = phys_prop.XObject.getAttribute('positionsJ')
	if(positionsJ_at is None):
		raise Exception('Error: cannot find "positionsJ" attribute')
	positionsJ = positionsJ_at.quantityVector
	
	weightsJ_at = phys_prop.XObject.getAttribute('weightsJ')
	if(weightsJ_at is None):
		raise Exception('Error: cannot find "weightsJ" attribute')
	weightsJ = weightsJ_at.quantityVector
	
	if (len(positionsI)) !=(len(positionsJ)) !=(len(weightsI)) !=(len(weightsJ)):
		raise Exception('Error: different length between vectors "secTag", "positionsI" and "weightsJ"')
	
	str_spw_I = ' '.join(itertools.chain([str(tag) for tag in secTagI], [str(ipw.valueAt(i)) for ipw in [positionsI, weightsI] for i in range(len(ipw))]))
	str_spw_J = ' '.join(itertools.chain([str(tag) for tag in secTagJ], [str(ipw.valueAt(i)) for ipw in [positionsJ, weightsJ] for i in range(len(ipw))]))
	
	return ('{} {} {} {} {} {}'.format(IntegrationType, secTagE, npI, str_spw_I, npJ, str_spw_J))

def __option5(phys_prop):
	# DistHinge
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType/5')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	HingeIntegrationType_at = phys_prop.XObject.getAttribute('HingeIntegrationType/5')
	if(HingeIntegrationType_at is None):
		raise Exception('Error: cannot find "HingeIntegrationType" attribute')
	HingeIntegrationType = HingeIntegrationType_at.string
	
	numIntPts_at = phys_prop.XObject.getAttribute('numIntPts/5')
	if(numIntPts_at is None):
		raise Exception('Error: cannot find "numIntPts" attribute')
	numIntPts = numIntPts_at.integer
	
	secTagI_at = phys_prop.XObject.getAttribute('secTagI/5')
	if(secTagI_at is None):
		raise Exception('Error: cannot find "secTagI" attribute')
	secTagI = secTagI_at.index
	
	lpI_at = phys_prop.XObject.getAttribute('lpI/5')
	if(lpI_at is None):
		raise Exception('Error: cannot find "lpI" attribute')
	lpI = lpI_at.quantityScalar.value
	
	secTagJ_at = phys_prop.XObject.getAttribute('secTagJ/5')
	if(secTagJ_at is None):
		raise Exception('Error: cannot find "secTagJ" attribute')
	secTagJ = secTagJ_at.index
	
	lpJ_at = phys_prop.XObject.getAttribute('lpJ/5')
	if(lpJ_at is None):
		raise Exception('Error: cannot find "lpJ" attribute')
	lpJ = lpJ_at.quantityScalar.value
	
	secTagE_at = phys_prop.XObject.getAttribute('secTagE/5')
	if(secTagE_at is None):
		raise Exception('Error: cannot find "secTagE" attribute')
	secTagE = secTagE_at.index
	
	return ('{} {} {} {} {} {} {} {}'.format(
			IntegrationType, HingeIntegrationType, numIntPts, secTagI, lpI, secTagJ, lpJ, secTagE))

def __option6(phys_prop):
	# RegularizedHinge
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType/6')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	HingeIntegrationType_at = phys_prop.XObject.getAttribute('HingeIntegrationType/6')
	if(HingeIntegrationType_at is None):
		raise Exception('Error: cannot find "HingeIntegrationType" attribute')
	HingeIntegrationType = HingeIntegrationType_at.string
	
	numIntPts_at = phys_prop.XObject.getAttribute('numIntPts/6')
	if(numIntPts_at is None):
		raise Exception('Error: cannot find "numIntPts" attribute')
	numIntPts = numIntPts_at.integer
	
	secTagI_at = phys_prop.XObject.getAttribute('secTagI/6')
	if(secTagI_at is None):
		raise Exception('Error: cannot find "secTagI" attribute')
	secTagI = secTagI_at.index
	
	lpI_at = phys_prop.XObject.getAttribute('lpI/6')
	if(lpI_at is None):
		raise Exception('Error: cannot find "lpI" attribute')
	lpI = lpI_at.quantityScalar.value
	
	zetaI_at = phys_prop.XObject.getAttribute('zetaI')
	if(zetaI_at is None):
		raise Exception('Error: cannot find "zetaI" attribute')
	zetaI = zetaI_at.quantityScalar.value
	
	secTagJ_at = phys_prop.XObject.getAttribute('secTagJ/6')
	if(secTagJ_at is None):
		raise Exception('Error: cannot find "secTagJ" attribute')
	secTagJ = secTagJ_at.index
	
	lpJ_at = phys_prop.XObject.getAttribute('lpJ/6')
	if(lpJ_at is None):
		raise Exception('Error: cannot find "lpJ" attribute')
	lpJ = lpJ_at.quantityScalar.value
	
	zetaJ_at = phys_prop.XObject.getAttribute('zetaJ')
	if(zetaJ_at is None):
		raise Exception('Error: cannot find "zetaJ" attribute')
	zetaJ = zetaJ_at.quantityScalar.value
	
	secTagE_at = phys_prop.XObject.getAttribute('secTagE/6')
	if(secTagE_at is None):
		raise Exception('Error: cannot find "secTagE" attribute')
	secTagE = secTagE_at.index
	
	return ('{} {} {} {} {} {} {} {} {} {}'.format(
			IntegrationType, HingeIntegrationType, numIntPts, secTagI, lpI, zetaI, secTagJ, lpJ, zetaJ, secTagE))

def __option7(phys_prop):
	# FixedLocation
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType/7')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	numIntPts_at = phys_prop.XObject.getAttribute('numIntPts/7')
	if(numIntPts_at is None):
		raise Exception('Error: cannot find "numIntPts" attribute')
	numIntPts = numIntPts_at.integer
	
	secTag_at = phys_prop.XObject.getAttribute('secTag/7')
	if(secTag_at is None):
		raise Exception('Error: cannot find "secTag" attribute')
	secTag = secTag_at.indexVector
	
	positions_at = phys_prop.XObject.getAttribute('positions/7')
	if(positions_at is None):
		raise Exception('Error: cannot find "positions" attribute')
	positions = positions_at.quantityVector
	
	
	if(numIntPts < 1):
		raise Exception('Error: insufficient "numIntPts"')
	if(numIntPts != len(secTag) != len(positions)):
		raise Exception('Error: incorrect length between vectors "secTag" and "positions" with "numIntPts"')	#FAR CONTROLLARE A MASSIMO
	
	secTag_ = ''
	positions_ = ''
	for i in range(len(secTag)):
		secTag_ += ' {}'.format(secTag[i])
		positions_ += ' {}'.format(positions.valueAt(i))
	
	return ('{} {}{}{}'.format(IntegrationType, numIntPts, secTag_, positions_))

def __option8(phys_prop):
	# LowOrder
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType/8')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	numIntPts_at = phys_prop.XObject.getAttribute('numIntPts/8')
	if(numIntPts_at is None):
		raise Exception('Error: cannot find "numIntPts" attribute')
	numIntPts = numIntPts_at.integer
	
	secTag_at = phys_prop.XObject.getAttribute('secTag/8')
	if(secTag_at is None):
		raise Exception('Error: cannot find "secTag" attribute')
	secTag = secTag_at.indexVector
	
	positions_at = phys_prop.XObject.getAttribute('positions/8')
	if(positions_at is None):
		raise Exception('Error: cannot find "positions" attribute')
	positions = positions_at.quantityVector
	
	weights_at = phys_prop.XObject.getAttribute('weights/8')
	if(weights_at is None):
		raise Exception('Error: cannot find "weights" attribute')
	weights = weights_at.quantityVector
	
	
	if(numIntPts < 1):
		raise Exception('Error: insufficient "numIntPts"')
	if(numIntPts != len(secTag) != len(positions)):
		raise Exception('Error: incorrect length between vectors "secTag" and "positions" with "numIntPts"')
	
	secTag_ = ''
	positions_ = ''
	for i in range(len(secTag)):
		secTag_ += ' {}'.format(secTag[i])
		positions_ += ' {}'.format(positions.valueAt(i))
	
	weights_ = ''
	for j in range(len(weights)):
		weights_ += ' {}'.format(weights.valueAt(j))
	
	return ('{} {}{}{}{}'.format(IntegrationType, numIntPts, secTag_, positions_, weights_))

def __option9(phys_prop):
	# MidDistance
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType/9')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	numIntPts_at = phys_prop.XObject.getAttribute('numIntPts/9')
	if(numIntPts_at is None):
		raise Exception('Error: cannot find "numIntPts" attribute')
	numIntPts = numIntPts_at.integer
	
	secTag_at = phys_prop.XObject.getAttribute('secTag/9')
	if(secTag_at is None):
		raise Exception('Error: cannot find "secTag" attribute')
	secTag = secTag_at.indexVector
	
	positions_at = phys_prop.XObject.getAttribute('positions/9')
	if(positions_at is None):
		raise Exception('Error: cannot find "positions" attribute')
	positions = positions_at.quantityVector
	
	
	if(numIntPts < 1):
		raise Exception('Error: insufficient "numIntPts"')
	if(numIntPts != len(secTag) != len(positions)):
		raise Exception('Error: incorrect length between vectors "secTag" and "positions" with "numIntPts"')	#FAR CONTROLLARE A MASSIMO
	
	secTag_ = ''
	positions_ = ''
	for i in range(len(secTag)):
		secTag_ += ' {}'.format(secTag[i])
		positions_ += ' {}'.format(positions.valueAt(i))
	
	return ('{} {}{}{}'.format(IntegrationType, numIntPts, secTag_, positions_))

def writeTcl_internalBeamFunction(pinfo, specific_options = ''):
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	Dimension2 = Dimension2_at.boolean
	
	# nodes
	node_vect = [node.id for node in elem.nodes]
	# apply correction for joints
	if not Dimension2:
		if 'RCJointModel3D' in pinfo.custom_data:
			joint_manager = pinfo.custom_data['RCJointModel3D']
			joint_manager.adjustBeamConnectivity(pinfo, elem, node_vect)
	nstr = ' '.join(str(i) for i in node_vect)
	
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line or len(node_vect)!=2):
		raise Exception('Error: invalid type of element or number of nodes')
	
	# opzioni
	sopt1 = ''
	Option_at = phys_prop.XObject.getAttribute('Option')
	if(Option_at is None):
		raise Exception('Error: cannot find "Option" attribute')
	Option = Option_at.string
	
	if Option=='StandardIntegrationTypes':
		sopt1 = __option1(phys_prop)
	elif Option=='UserDefined':
		sopt1 = __option2(phys_prop)
	elif Option=='Hinge':
		sopt1 = __option3(phys_prop)
	elif Option=='UserHinge':
		sopt1 = __option4(phys_prop)
	elif Option=='DistHinge':
		sopt1 = __option5(phys_prop)
	elif Option=='RegularizedHinge':
		sopt1 = __option6(phys_prop)
	elif Option=='FixedLocation':
		sopt1 = __option7(phys_prop)
	elif Option=='LowOrder':
		sopt1 = __option8(phys_prop)
	elif Option=='MidDistance':
		sopt1 = __option9(phys_prop)
	
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
		
		sopt += ' -mass {}'.format(massDens.value)
	
	# geometric transformation command
	pinfo.out_file.write(gtran.writeGeomTransf(pinfo, (not Dimension2)))
	
	str_tcl = '{}element {} {} {} {} {}{}{}\n'.format(pinfo.indent, ClassName, tag, nstr, tag, sopt1, sopt, specific_options)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)