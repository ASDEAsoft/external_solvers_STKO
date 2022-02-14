import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# aSlow
	at_aSlow = MpcAttributeMetaData()
	at_aSlow.type = MpcAttributeType.Real
	at_aSlow.name = 'aSlow'
	at_aSlow.group = 'Group'
	at_aSlow.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('aSlow')+'<br/>') + 
		html_par('constant for coefficient of friction at low velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Normal_Force_Dependent_Friction','Velocity and Normal Force Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# nSlow
	at_nSlow = MpcAttributeMetaData()
	at_nSlow.type = MpcAttributeType.Real
	at_nSlow.name = 'nSlow'
	at_nSlow.group = 'Group'
	at_nSlow.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nSlow')+'<br/>') + 
		html_par('exponent for coefficient of friction at low velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Normal_Force_Dependent_Friction','Velocity and Normal Force Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# aFast
	at_aFast = MpcAttributeMetaData()
	at_aFast.type = MpcAttributeType.Real
	at_aFast.name = 'aFast'
	at_aFast.group = 'Group'
	at_aFast.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('aFast')+'<br/>') + 
		html_par('constant for coefficient of friction at high velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Normal_Force_Dependent_Friction','Velocity and Normal Force Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# nFast
	at_nFast = MpcAttributeMetaData()
	at_nFast.type = MpcAttributeType.Real
	at_nFast.name = 'nFast'
	at_nFast.group = 'Group'
	at_nFast.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nFast')+'<br/>') + 
		html_par('exponent for coefficient of friction at high velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Normal_Force_Dependent_Friction','Velocity and Normal Force Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# alpha0
	at_alpha0 = MpcAttributeMetaData()
	at_alpha0.type = MpcAttributeType.Real
	at_alpha0.name = 'alpha0'
	at_alpha0.group = 'Group'
	at_alpha0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha0')+'<br/>') + 
		html_par('constant rate parameter coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Normal_Force_Dependent_Friction','Velocity and Normal Force Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# alpha1
	at_alpha1 = MpcAttributeMetaData()
	at_alpha1.type = MpcAttributeType.Real
	at_alpha1.name = 'alpha1'
	at_alpha1.group = 'Group'
	at_alpha1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha1')+'<br/>') + 
		html_par('linear rate parameter coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Normal_Force_Dependent_Friction','Velocity and Normal Force Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# alpha2
	at_alpha2 = MpcAttributeMetaData()
	at_alpha2.type = MpcAttributeType.Real
	at_alpha2.name = 'alpha2'
	at_alpha2.group = 'Group'
	at_alpha2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha2')+'<br/>') + 
		html_par('quadratic rate parameter coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Normal_Force_Dependent_Friction','Velocity and Normal Force Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# maxMuFact
	at_maxMuFact = MpcAttributeMetaData()
	at_maxMuFact.type = MpcAttributeType.Real
	at_maxMuFact.name = 'maxMuFact'
	at_maxMuFact.group = 'Group'
	at_maxMuFact.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxMuFact')+'<br/>') + 
		html_par('factor for determining the maximum coefficient of friction. This value prevents the friction coefficient from exceeding an unrealistic maximum value when the normal force becomes very small. The maximum friction coefficient is determined from μFast, for example μ ≤ maxMuFac*μFast.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_and_Normal_Force_Dependent_Friction','Velocity and Normal Force Dependent Friction')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'VelNormalFrcDep'
	xom.addAttribute(at_aSlow)
	xom.addAttribute(at_nSlow)
	xom.addAttribute(at_aFast)
	xom.addAttribute(at_nFast)
	xom.addAttribute(at_alpha0)
	xom.addAttribute(at_alpha1)
	xom.addAttribute(at_alpha2)
	xom.addAttribute(at_maxMuFact)
	
	
	return xom

def writeTcl(pinfo):
	
	#frictionModel VelNormalFrcDep $frnTag $aSlow $nSlow $aFast $nFast $alpha0 $alpha1 $alpha2 $maxMuFact
	xobj = pinfo.definition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	frnTag = xobj.parent.componentId
	
	# mandatory parameters
	aSlow_at = xobj.getAttribute('aSlow')
	if(aSlow_at is None):
		raise Exception('Error: cannot find "aSlow" attribute')
	aSlow = aSlow_at.real
	
	nSlow_at = xobj.getAttribute('nSlow')
	if(nSlow_at is None):
		raise Exception('Error: cannot find "nSlow" attribute')
	nSlow = nSlow_at.real
	
	aFast_at = xobj.getAttribute('aFast')
	if(aFast_at is None):
		raise Exception('Error: cannot find "aFast" attribute')
	aFast = aFast_at.real
	
	nFast_at = xobj.getAttribute('nFast')
	if(nFast_at is None):
		raise Exception('Error: cannot find "nFast" attribute')
	nFast = nFast_at.real
	
	alpha0_at = xobj.getAttribute('alpha0')
	if(alpha0_at is None):
		raise Exception('Error: cannot find "alpha0" attribute')
	alpha0 = alpha0_at.real
	
	alpha1_at = xobj.getAttribute('alpha1')
	if(alpha1_at is None):
		raise Exception('Error: cannot find "alpha1" attribute')
	alpha1 = alpha1_at.real
	
	alpha2_at = xobj.getAttribute('alpha2')
	if(alpha2_at is None):
		raise Exception('Error: cannot find "alpha2" attribute')
	alpha2 = alpha2_at.real
	
	maxMuFact_at = xobj.getAttribute('maxMuFact')
	if(maxMuFact_at is None):
		raise Exception('Error: cannot find "maxMuFact" attribute')
	maxMuFact = maxMuFact_at.real
	
	
	str_tcl = '{}frictionModel VelNormalFrcDep {} {} {} {} {} {} {} {} {}\n'.format(pinfo.indent, frnTag, aSlow, nSlow, aFast, nFast, alpha0, alpha1, alpha2, maxMuFact)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)