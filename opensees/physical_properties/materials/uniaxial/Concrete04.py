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
		html_par('floating point values defining concrete compressive strength at 28 days (compression is negative)*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete04_Material_--_Popovics_Concrete_Material','Concrete04 Material')+'<br/>') +
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
		html_par('floating point values defining concrete strain at maximum strength*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete04_Material_--_Popovics_Concrete_Material','Concrete04 Material')+'<br/>') +
		html_end()
		)
	
	# ecu
	at_ecu = MpcAttributeMetaData()
	at_ecu.type = MpcAttributeType.Real
	at_ecu.name = 'ecu'
	at_ecu.group = 'Non-linear'
	at_ecu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ecu')+'<br/>') + 
		html_par('floating point values defining concrete strain at crushing strength*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete04_Material_--_Popovics_Concrete_Material','Concrete04 Material')+'<br/>') +
		html_end()
		)
		
	# Ec
	at_Ec = MpcAttributeMetaData()
	at_Ec.type = MpcAttributeType.QuantityScalar
	at_Ec.name = 'Ec'
	at_Ec.group = 'Linear'
	at_Ec.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ec')+'<br/>') + 
		html_par('floating point values defining initial stiffness**') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete04_Material_--_Popovics_Concrete_Material','Concrete04 Material')+'<br/>') +
		html_end()
		)
	at_Ec.dimension = u.F/u.L**2
	
	# use_fct_et
	at_use_fct_et = MpcAttributeMetaData()
	at_use_fct_et.type = MpcAttributeType.Boolean
	at_use_fct_et.name = 'use_fct_et'
	at_use_fct_et.group = 'Non-linear'
	at_use_fct_et.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_fct_et')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete04_Material_--_Popovics_Concrete_Material','Concrete04 Material')+'<br/>') +
		html_end()
		)
	
	# fct
	at_fct = MpcAttributeMetaData()
	at_fct.type = MpcAttributeType.QuantityScalar
	at_fct.name = 'fct'
	at_fct.group = 'Optional parameters'
	at_fct.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fct')+'<br/>') + 
		html_par('floating point value defining the maximum tensile strength of concrete') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete04_Material_--_Popovics_Concrete_Material','Concrete04 Material')+'<br/>') +
		html_end()
		)
	at_fct.dimension = u.F/u.L**2
	
	# et
	at_et = MpcAttributeMetaData()
	at_et.type = MpcAttributeType.QuantityScalar
	at_et.name = 'et'
	at_et.group = 'Optional parameters'
	at_et.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('et')+'<br/>') + 
		html_par('floating point value defining ultimate tensile strain of concrete') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete04_Material_--_Popovics_Concrete_Material','Concrete04 Material')+'<br/>') +
		html_end()
		)
	at_Ec.dimension = u.F/u.L**2
	
	# use_beta
	at_use_beta = MpcAttributeMetaData()
	at_use_beta.type = MpcAttributeType.Boolean
	at_use_beta.name = 'use_beta'
	at_use_beta.group = 'Non-linear'
	at_use_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_beta')+'<br/>') + 
		html_par('loating point value defining the exponential curve parameter to define the residual stress (as a factor of $ft) at $etu') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete04_Material_--_Popovics_Concrete_Material','Concrete04 Material')+'<br/>') +
		html_end()
		)
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'Optional parameters'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') + 
		html_par('loating point value defining the exponential curve parameter to define the residual stress (as a factor of $ft) at $etu') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete04_Material_--_Popovics_Concrete_Material','Concrete04 Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Concrete04'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_fc)
	xom.addAttribute(at_ec)
	xom.addAttribute(at_ecu)
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_use_fct_et)
	xom.addAttribute(at_fct)
	xom.addAttribute(at_et)
	xom.addAttribute(at_use_beta)
	xom.addAttribute(at_beta)
	
	# fct_et-dep
	xom.setVisibilityDependency(at_use_fct_et, at_fct)
	xom.setVisibilityDependency(at_use_fct_et, at_et)
	
	# beta-dep
	xom.setVisibilityDependency(at_use_beta, at_beta)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Concrete04 $matTag $fc $ec $ecu $Ec <$fct $et> <$beta>
	
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
	
	ecu_at = xobj.getAttribute('ecu')
	if(ecu_at is None):
		raise Exception('Error: cannot find "ecu" attribute')
	ecu = ecu_at.real
	
	Ec_at = xobj.getAttribute('Ec')
	if(Ec_at is None):
		raise Exception('Error: cannot find "Ec" attribute')
	Ec = Ec_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	use_fct_et_at = xobj.getAttribute('use_fct_et')
	if(use_fct_et_at is None):
		raise Exception('Error: cannot find "use_fct_et" attribute')
	use_fct_et = use_fct_et_at.boolean
	if use_fct_et:
		fct_at = xobj.getAttribute('fct')
		if(fct_at is None):
			raise Exception('Error: cannot find "fct" attribute')
		fct = fct_at.quantityScalar
		
		et_at = xobj.getAttribute('et')
		if(et_at is None):
			raise Exception('Error: cannot find "et" attribute')
		et = et_at.quantityScalar
		
		sopt += '{} {}'.format(fct.value, et.value)
	
	use_beta_at = xobj.getAttribute('use_beta')
	if(use_beta_at is None):
		raise Exception('Error: cannot find "use_beta" attribute')
	use_beta = use_beta_at.boolean
	if use_beta:
		beta_at = xobj.getAttribute('beta')
		if(beta_at is None):
			raise Exception('Error: cannot find "beta" attribute')
		beta = beta_at.real
		
		sopt += ' {}'.format(beta)
	
	
	str_tcl = '{}uniaxialMaterial Concrete04 {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fc.value, ec, ecu, Ec.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
	
def getMaterialProperties(xobj):
	# This function return the Material Properties necessary 
	#	for the computation of confinement:
	#		fc = Peak strength of concrete
	#		epsc0 = strain at peak strength
	#		epscu = ultimate strain
	#		Ec = Elastic modulus
	
	fc = __get_xobj_attribute(xobj, 'fc').quantityScalar.value
	epsc0 = __get_xobj_attribute(xobj, 'ec').real
	epscu = __get_xobj_attribute(xobj, 'ecu').real
	Ec = __get_xobj_attribute(xobj, 'Ec').quantityScalar.value
	
	return (fc, epsc0, epscu, Ec)
	
def getParamsConfinedVersion(xobj,fcc,epscc0,epsccu,fccu):
	# This function returns the paramters of the materials
	#	in confined version, given the main parameters
	
	# get Parameters of unconfined version
	fc = __get_xobj_attribute(xobj, 'fc').quantityScalar.value
	epsc0 = __get_xobj_attribute(xobj, 'ec').real
	epscu = __get_xobj_attribute(xobj, 'ecu').real
	Ec = __get_xobj_attribute(xobj, 'Ec').quantityScalar.value
	
	params = (fcc, epscc0, epsccu, Ec)
	
	use_fct_et = __get_xobj_attribute(xobj, 'use_fct_et').boolean
	if use_fct_et:
		fct = __get_xobj_attribute(xobj, 'fct').quantityScalar.value
		et = __get_xobj_attribute(xobj, 'et').quantityScalar.value
		params += (fct, et)

	use_beta = __get_xobj_attribute(xobj, 'use_beta').boolean
	if use_beta:
		beta = __get_xobj_attribute(xobj, 'beta').real
		params += (beta,)
	
	return params