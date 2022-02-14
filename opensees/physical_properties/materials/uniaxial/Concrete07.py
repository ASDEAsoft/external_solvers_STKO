# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

####################################################################################
# Utilities
####################################################################################

def __get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

####################################################################################
# Main methods
####################################################################################

def makeXObjectMetaData():
	
	# fc
	at_fc = MpcAttributeMetaData()
	at_fc.type = MpcAttributeType.QuantityScalar
	at_fc.name = 'fc'
	at_fc.group = 'Non-linear'
	at_fc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fc')+'<br/>') + 
		html_par('concrete compressive strength (compression is negative)*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete07_%E2%80%93_Chang_%26_Mander%E2%80%99s_1994_Concrete_Model','Concrete07 – Chang & Mander’s 1994 Concrete Model')+'<br/>') +
		html_end()
		)
	at_fc.dimension = u.F/u.L**2
	
	# ec
	at_ec = MpcAttributeMetaData()
	at_ec.type = MpcAttributeType.Real
	at_ec.name = 'ec'
	at_ec.group = 'Non-linear'
	at_ec.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ec')+'<br/>') + 
		html_par('concrete strain at maximum compressive strength*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete07_%E2%80%93_Chang_%26_Mander%E2%80%99s_1994_Concrete_Model','Concrete07 – Chang & Mander’s 1994 Concrete Model')+'<br/>') +
		html_end()
		)
	
	# Ec
	at_Ec = MpcAttributeMetaData()
	at_Ec.type = MpcAttributeType.QuantityScalar
	at_Ec.name = 'Ec'
	at_Ec.group = 'Elasticity'
	at_Ec.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ec')+'<br/>') + 
		html_par('Initial Elastic modulus of the concrete') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete07_%E2%80%93_Chang_%26_Mander%E2%80%99s_1994_Concrete_Model','Concrete07 – Chang & Mander’s 1994 Concrete Model')+'<br/>') +
		html_end()
		)
	at_Ec.dimension = u.F/u.L**2
	
	# ft
	at_ft = MpcAttributeMetaData()
	at_ft.type = MpcAttributeType.QuantityScalar
	at_ft.name = 'ft'
	at_ft.group = 'Non-linear'
	at_ft.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ft')+'<br/>') + 
		html_par('tensile strength of concrete (tension is positive)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete07_%E2%80%93_Chang_%26_Mander%E2%80%99s_1994_Concrete_Model','Concrete07 – Chang & Mander’s 1994 Concrete Model')+'<br/>') +
		html_end()
		)
	at_ft.dimension = u.F/u.L**2
	
	# et
	at_et = MpcAttributeMetaData()
	at_et.type = MpcAttributeType.QuantityScalar
	at_et.name = 'et'
	at_et.group = 'Non-linear'
	at_et.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('et')+'<br/>') + 
		html_par('tensile strain at max tensile strength of concrete') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete07_%E2%80%93_Chang_%26_Mander%E2%80%99s_1994_Concrete_Model','Concrete07 – Chang & Mander’s 1994 Concrete Model')+'<br/>') +
		html_end()
		)
	at_et.dimension = u.F/u.L**2
	
	# xp
	at_xp = MpcAttributeMetaData()
	at_xp.type = MpcAttributeType.Real
	at_xp.name = 'xp'
	at_xp.group = 'Non-linear'
	at_xp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('xp')+'<br/>') + 
		html_par('Non-dimensional term that defines the strain at which the straight line descent begins in tension') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete07_%E2%80%93_Chang_%26_Mander%E2%80%99s_1994_Concrete_Model','Concrete07 – Chang & Mander’s 1994 Concrete Model')+'<br/>') +
		html_end()
		)
	
	# xn
	at_xn = MpcAttributeMetaData()
	at_xn.type = MpcAttributeType.Real
	at_xn.name = 'xn'
	at_xn.group = 'Non-linear'
	at_xn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('xn')+'<br/>') + 
		html_par('Non-dimensional term that defines the strain at which the straight line descent begins in compression') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete07_%E2%80%93_Chang_%26_Mander%E2%80%99s_1994_Concrete_Model','Concrete07 – Chang & Mander’s 1994 Concrete Model')+'<br/>') +
		html_end()
		)
	
	# r
	at_r = MpcAttributeMetaData()
	at_r.type = MpcAttributeType.Real
	at_r.name = 'r'
	at_r.group = 'Non-linear'
	at_r.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('r')+'<br/>') + 
		html_par('Parameter that controls the nonlinear descending branch') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete07_%E2%80%93_Chang_%26_Mander%E2%80%99s_1994_Concrete_Model','Concrete07 – Chang & Mander’s 1994 Concrete Model')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Concrete07'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_fc)
	xom.addAttribute(at_ec)
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_ft)
	xom.addAttribute(at_et)
	xom.addAttribute(at_xp)
	xom.addAttribute(at_xn)
	xom.addAttribute(at_r)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Concrete07 $matTag $fc $ec $Ec $ft $et $xp $xn $r
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fc_at = xobj.getAttribute('fc')
	if(fc_at is None):
		raise Exception('Error: cannot find "fc" attribute')
	fc = fc_at.quantityScalar
	
	ec_at = xobj.getAttribute('ec')
	if(ec_at is None):
		raise Exception('Error: cannot find "ec" attribute')
	ec = ec_at.real
	
	Ec_at = xobj.getAttribute('Ec')
	if(Ec_at is None):
		raise Exception('Error: cannot find "Ec" attribute')
	Ec = Ec_at.quantityScalar
	
	ft_at = xobj.getAttribute('ft')
	if(ft_at is None):
		raise Exception('Error: cannot find "ft" attribute')
	ft = ft_at.quantityScalar
	
	et_at = xobj.getAttribute('et')
	if(et_at is None):
		raise Exception('Error: cannot find "et" attribute')
	et = et_at.quantityScalar
	
	xp_at = xobj.getAttribute('xp')
	if(xp_at is None):
		raise Exception('Error: cannot find "xp" attribute')
	xp = xp_at.real
	
	xn_at = xobj.getAttribute('xn')
	if(xn_at is None):
		raise Exception('Error: cannot find "xn" attribute')
	xn = xn_at.real
	
	r_at = xobj.getAttribute('r')
	if(r_at is None):
		raise Exception('Error: cannot find "r" attribute')
	r = r_at.real
	
	
	
	str_tcl = '{}uniaxialMaterial Concrete07 {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fc.value, ec, Ec.value, ft.value, et.value, xp, xn, r)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
	