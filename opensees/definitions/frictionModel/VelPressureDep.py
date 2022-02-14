import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# muSlow
	at_muSlow = MpcAttributeMetaData()
	at_muSlow.type = MpcAttributeType.Real
	at_muSlow.name = 'muSlow'
	at_muSlow.group = 'Group'
	at_muSlow.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('muSlow')+'<br/>') + 
		html_par('coefficient of friction at low velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Pressure_Dependent_Friction','Velocity and Pressure Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# muFast0
	at_muFast0 = MpcAttributeMetaData()
	at_muFast0.type = MpcAttributeType.Real
	at_muFast0.name = 'muFast0'
	at_muFast0.group = 'Group'
	at_muFast0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('muFast0')+'<br/>') + 
		html_par('initial coefficient of friction at high velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Pressure_Dependent_Friction','Velocity and Pressure Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# A
	at_A = MpcAttributeMetaData()
	at_A.type = MpcAttributeType.QuantityScalar
	at_A.name = 'A'
	at_A.group = 'Group'
	at_A.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('A')+'<br/>') + 
		html_par('nominal contact area') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Pressure_Dependent_Friction','Velocity and Pressure Dependent Friction')+'<br/>') +
		html_end()
		)
	at_A.dimension = u.L**2
	
	# deltaMu
	at_deltaMu = MpcAttributeMetaData()
	at_deltaMu.type = MpcAttributeType.Real
	at_deltaMu.name = 'deltaMu'
	at_deltaMu.group = 'Group'
	at_deltaMu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('deltaMu')+'<br/>') + 
		html_par('pressure parameter calibrated from experimental data') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Pressure_Dependent_Friction','Velocity and Pressure Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Group'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('pressure parameter calibrated from experimental data') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Pressure_Dependent_Friction','Velocity and Pressure Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# transRate
	at_transRate = MpcAttributeMetaData()
	at_transRate.type = MpcAttributeType.Real
	at_transRate.name = 'transRate'
	at_transRate.group = 'Group'
	at_transRate.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('transRate')+'<br/>') + 
		html_par('transition rate from low to high velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Pressure_Dependent_Friction','Velocity and Pressure Dependent Friction')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'VelPressureDep'
	xom.addAttribute(at_muSlow)
	xom.addAttribute(at_muFast0)
	xom.addAttribute(at_A)
	xom.addAttribute(at_deltaMu)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_transRate)
	
	
	return xom

def writeTcl(pinfo):
	
	#frictionModel VelPressureDep $frnTag $muSlow $muFast0 $A $deltaMu $alpha $transRate
	xobj = pinfo.definition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	frnTag = xobj.parent.componentId
	
	# mandatory parameters
	muSlow_at = xobj.getAttribute('muSlow')
	if(muSlow_at is None):
		raise Exception('Error: cannot find "muSlow" attribute')
	muSlow = muSlow_at.real
	
	muFast0_at = xobj.getAttribute('muFast0')
	if(muFast0_at is None):
		raise Exception('Error: cannot find "muFast0" attribute')
	muFast0 = muFast0_at.real
	
	A_at = xobj.getAttribute('A')
	if(A_at is None):
		raise Exception('Error: cannot find "A" attribute')
	A = A_at.quantityScalar
	
	deltaMu_at = xobj.getAttribute('deltaMu')
	if(deltaMu_at is None):
		raise Exception('Error: cannot find "deltaMu" attribute')
	deltaMu = deltaMu_at.real
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	transRate_at = xobj.getAttribute('transRate')
	if(transRate_at is None):
		raise Exception('Error: cannot find "transRate" attribute')
	transRate = transRate_at.real
	
	
	str_tcl = '{}frictionModel VelPressureDep {} {} {} {} {} {} {}\n'.format(pinfo.indent, frnTag, muSlow, muFast0, A.value, deltaMu, alpha, transRate)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)