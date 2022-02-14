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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_Dependent_Friction','Velocity Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# muFast
	at_muFast = MpcAttributeMetaData()
	at_muFast.type = MpcAttributeType.Real
	at_muFast.name = 'muFast'
	at_muFast.group = 'Group'
	at_muFast.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('muFast')+'<br/>') + 
		html_par('coefficient of friction at high velocity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_Dependent_Friction','Velocity Dependent Friction')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Velocity_Dependent_Friction','Velocity Dependent Friction')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'VelDependent'
	xom.addAttribute(at_muSlow)
	xom.addAttribute(at_muFast)
	xom.addAttribute(at_transRate)
	
	
	return xom

def writeTcl(pinfo):
	
	#frictionModel VelDependent $frnTag $muSlow $muFast $transRate
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
	
	muFast_at = xobj.getAttribute('muFast')
	if(muFast_at is None):
		raise Exception('Error: cannot find "muFast" attribute')
	muFast = muFast_at.real
	
	transRate_at = xobj.getAttribute('transRate')
	if(transRate_at is None):
		raise Exception('Error: cannot find "transRate" attribute')
	transRate = transRate_at.real
	
	
	str_tcl = '{}frictionModel VelDependent {} {} {} {}\n'.format(pinfo.indent, frnTag, muSlow, muFast, transRate)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)