import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeExtrusionShellDataInfo(xobj):
	h_at = xobj.getAttribute('h')
	if(h_at is None):
		raise Exception('Error: cannot find "h" attribute')
	h = h_at.quantityScalar.value
	info = MpcSectionExtrusionShellDataInfo(h)
	return info

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Group'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('Young\'s Modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Membrane_Plate_Section','Elastic Membrane Plate Section')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# nu
	at_nu = MpcAttributeMetaData()
	at_nu.type = MpcAttributeType.Real
	at_nu.name = 'nu'
	at_nu.group = 'Group'
	at_nu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nu')+'<br/>') + 
		html_par('Poisson\'s Ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Membrane_Plate_Section','Elastic Membrane Plate Section')+'<br/>') +
		html_end()
		)
	
	# h
	at_h = MpcAttributeMetaData()
	at_h.type = MpcAttributeType.QuantityScalar
	at_h.name = 'h'
	at_h.group = 'Group'
	at_h.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h')+'<br/>') + 
		html_par('depth of section') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Membrane_Plate_Section','Elastic Membrane Plate Section')+'<br/>') +
		html_end()
		)
	at_h.dimension = u.L
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Group'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('mass density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Membrane_Plate_Section','Elastic Membrane Plate Section')+'<br/>') +
		html_end()
		)
	#at_rho.dimension = u.M/u.L**3
	
	# Ep_mod
	at_Ep_mod = MpcAttributeMetaData()
	at_Ep_mod.type = MpcAttributeType.Real
	at_Ep_mod.name = 'Ep_mod'
	at_Ep_mod.group = 'Group'
	at_Ep_mod.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ep_mod')+'<br/>') + 
		html_par('Ratio of Flexural to Membrane stiffness. Optional. Default = 1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Membrane_Plate_Section','Elastic Membrane Plate Section')+'<br/>') +
		html_end()
		)
	at_Ep_mod.setDefault(1.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ElasticMembranePlateSection'
	xom.addAttribute(at_E)
	xom.addAttribute(at_nu)
	xom.addAttribute(at_h)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_Ep_mod)
	
	return xom

def writeTcl(pinfo):
	
	#section ElasticMembranePlateSection $secTag $E $nu $h $rho
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar
	
	nu_at = xobj.getAttribute('nu')
	if(nu_at is None):
		raise Exception('Error: cannot find "nu" attribute')
	nu = nu_at.real
	
	h_at = xobj.getAttribute('h')
	if(h_at is None):
		raise Exception('Error: cannot find "h" attribute')
	h = h_at.quantityScalar
	
	rho_at = xobj.getAttribute('rho')
	if(rho_at is None):
		raise Exception('Error: cannot find "rho" attribute')
	rho = rho_at.quantityScalar
	
	Ep_mod_at = xobj.getAttribute('Ep_mod')
	if(Ep_mod_at is None):
		raise Exception('Error: cannot find "Ep_mod" attribute')
	Ep_mod = Ep_mod_at.real
	
	str_tcl = '{}section ElasticMembranePlateSection {} {} {} {} {} {}\n'.format(pinfo.indent, tag, E.value, nu, h.value, rho.value, Ep_mod)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)