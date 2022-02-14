import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# weight
	at_weight = MpcAttributeMetaData()
	at_weight.type = MpcAttributeType.Real
	at_weight.name = 'weight'
	at_weight.group = 'Group'
	at_weight.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('weight')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CatenaryCableElement','CatenaryCableElement')+'<br/>') +
		html_end()
		)
	
	# L0
	at_L0 = MpcAttributeMetaData()
	at_L0.type = MpcAttributeType.QuantityScalar
	at_L0.name = 'L0'
	at_L0.group = 'Group'
	at_L0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('L0')+'<br/>') +
		html_par('unstretched length of the cable') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CatenaryCableElement','CatenaryCableElement')+'<br/>') +
		html_end()
		)
	at_L0.dimension = u.L
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Group'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') +
		html_par('coefficient of thermal expansion') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CatenaryCableElement','CatenaryCableElement')+'<br/>') +
		html_end()
		)
	
	# temperature_change
	at_temperature_change = MpcAttributeMetaData()
	at_temperature_change.type = MpcAttributeType.QuantityScalar
	at_temperature_change.name = 'temperature_change'
	at_temperature_change.group = 'Group'
	at_temperature_change.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('temperature_change')+'<br/>') +
		html_par('temperature change for the element') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CatenaryCableElement','CatenaryCableElement')+'<br/>') +
		html_end()
		)
	at_temperature_change.dimension = u.T
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Group'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') +
		html_par('mass per unit length') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CatenaryCableElement','CatenaryCableElement')+'<br/>') +
		html_end()
		)
	# at_rho.dimension = u.M/u.L
	
	# errorTol
	at_errorTol = MpcAttributeMetaData()
	at_errorTol.type = MpcAttributeType.Real
	at_errorTol.name = 'errorTol'
	at_errorTol.group = 'Group'
	at_errorTol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('errorTol')+'<br/>') +
		html_par('allowed tolerance for within-element equilbrium (Newton-Rhapson iterations)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CatenaryCableElement','CatenaryCableElement')+'<br/>') +
		html_end()
		)
	
	# Nsubsteps
	at_Nsubsteps = MpcAttributeMetaData()
	at_Nsubsteps.type = MpcAttributeType.Integer
	at_Nsubsteps.name = 'Nsubsteps'
	at_Nsubsteps.group = 'Group'
	at_Nsubsteps.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Nsubsteps')+'<br/>') +
		html_par('number of within-element substeps into which equilibrium iterations are subdivided (not number of steps to convergence)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CatenaryCableElement','CatenaryCableElement')+'<br/>') +
		html_end()
		)
	
	# massType
	at_massType = MpcAttributeMetaData()
	at_massType.type = MpcAttributeType.Integer
	at_massType.name = 'massType'
	at_massType.group = 'Group'
	at_massType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('massType')+'<br/>') +
		html_par('Mass matrix model to use (massType = 0 lumped mass matrix, massType = 1 rigid-body mass matrix (in development))') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CatenaryCableElement','CatenaryCableElement')+'<br/>') +
		html_end()
		)
	at_massType.sourceType = MpcAttributeSourceType.List
	at_massType.setSourceList([0, 1])
	at_massType.setDefault(0)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'CatenaryCable'
	xom.addAttribute(at_weight)
	xom.addAttribute(at_L0)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_temperature_change)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_errorTol)
	xom.addAttribute(at_Nsubsteps)
	xom.addAttribute(at_massType)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,3),(3,3)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	# element CatenaryCable $tag $iNode $jNode $weight $E $A $L0 $alpha $temperature_change $rho $errorTol $Nsubsteps $massType
	
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
	weight_at = xobj.getAttribute('weight')
	if(weight_at is None):
		raise Exception('Error: cannot find "weight" attribute')
	weight = weight_at.real
	
	L0_at = xobj.getAttribute('L0')
	if(L0_at is None):
		raise Exception('Error: cannot find "L0" attribute')
	L0 = L0_at.quantityScalar.value
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real

	temperature_change_at = xobj.getAttribute('temperature_change')
	if(temperature_change_at is None):
		raise Exception('Error: cannot find "temperature_change" attribute')
	temperature_change = temperature_change_at.quantityScalar.value
	
	rho_at = xobj.getAttribute('rho')
	if(rho_at is None):
		raise Exception('Error: cannot find "rho" attribute')
	rho = rho_at.quantityScalar.value
	
	errorTol_at = xobj.getAttribute('errorTol')
	if(errorTol_at is None):
		raise Exception('Error: cannot find "errorTol" attribute')
	errorTol = errorTol_at.real
	
	Nsubsteps_at = xobj.getAttribute('Nsubsteps')
	if(Nsubsteps_at is None):
		raise Exception('Error: cannot find "Nsubsteps" attribute')
	Nsubsteps = Nsubsteps_at.integer
	
	at_Section = phys_prop.XObject.getAttribute('Section')
	if(at_Section is None):
		raise Exception('Error: cannot find "Section" attribute')
	Section = at_Section.customObject
	
	at_E = phys_prop.XObject.getAttribute('E')
	if(at_E is None):
		raise Exception('Error: cannot find "E" attribute')
	E = at_E.quantityScalar.value
	
	A = Section.properties.area
	
	
	at_massType = xobj.getAttribute('massType')
	if(at_massType is None):
		raise Exception('Error: cannot find "massType " attribute')
	massType = at_massType.integer
	
	
	# element CatenaryCable $tag $iNode $jNode $weight $E $A $L0 $alpha $temperature_change $rho $errorTol $Nsubsteps $massType
	str_tcl = '{}element CatenaryCable {}{} {} {} {} {} {} {} {} {} {} {}\n'.format(
				pinfo.indent, tag, nstr, weight, E, A, L0, alpha, temperature_change, rho, errorTol, Nsubsteps, massType)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)