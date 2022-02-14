import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# K
	at_K = MpcAttributeMetaData()
	at_K.type = MpcAttributeType.QuantityScalar
	at_K.name = 'K'
	at_K.group = 'Non linear'
	at_K.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('K')+'<br/>') + 
		html_par('bulk module of the acoustic medium') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AcousticMedium','AcousticMedium')+'<br/>') +
		html_end()
		)
	at_K.dimension = u.F/u.L**2
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Non linear'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('mass density of the acoustic medium') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AcousticMedium','AcousticMedium')+'<br/>') +
		html_end()
		)
	#at_rho.dimension = u.M/u.L**3
	
	xom = MpcXObjectMetaData()
	xom.name = 'AcousticMedium'
	xom.Xgroup = 'Misc'
	xom.addAttribute(at_K)
	xom.addAttribute(at_rho)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial AcousticMedium $matTag $K $rho
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	K_at = xobj.getAttribute('K')
	if(K_at is None):
		raise Exception('Error: cannot find "K" attribute')
	K = K_at.quantityScalar
	
	rho_at = xobj.getAttribute('rho')
	if(rho_at is None):
		raise Exception('Error: cannot find "rho" attribute')
	rho = rho_at.quantityScalar
	
	str_tcl = '{}nDMaterial AcousticMedium {} {} {}\n'.format(pinfo.indent, tag, K.value, rho.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)