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
	
	# fpc
	at_fpc = MpcAttributeMetaData()
	at_fpc.type = MpcAttributeType.QuantityScalar
	at_fpc.name = 'fpc'
	at_fpc.group = 'Non-linear'
	at_fpc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fpc')+'<br/>') + 
		html_par('concrete compressive strength at 28 days (compression is negative)*') +
		html_par('Compressive concrete parameters should be input as negative values.') +
		html_par('The initial slope for this model is (2*fpc/epsc0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete01_Material_With_Stuff_in_the_Cracks','Concrete01 Material With Stuff in the Cracks')+'<br/>') +
		html_end()
		)
	at_fpc.dimension = u.F/u.L**2
	
	# epsc0
	at_epsc0 = MpcAttributeMetaData()
	at_epsc0.type = MpcAttributeType.Real
	at_epsc0.name = 'epsc0'
	at_epsc0.group = 'Non-linear'
	at_epsc0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsc0')+'<br/>') + 
		html_par('concrete strain at maximum strength*') +
		html_par('Compressive concrete parameters should be input as negative values.') +
		html_par('The initial slope for this model is (2*fpc/epsc0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete01_Material_With_Stuff_in_the_Cracks','Concrete01 Material With Stuff in the Cracks')+'<br/>') +
		html_end()
		)
	
	# fpcu
	at_fpcu = MpcAttributeMetaData()
	at_fpcu.type = MpcAttributeType.QuantityScalar
	at_fpcu.name = 'fpcu'
	at_fpcu.group = 'Non-linear'
	at_fpcu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fpcu')+'<br/>') + 
		html_par('concrete crushing strength *') +
		html_par('Compressive concrete parameters should be input as negative values.') +
		html_par('The initial slope for this model is (2*fpc/epsc0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete01_Material_With_Stuff_in_the_Cracks','Concrete01 Material With Stuff in the Cracks')+'<br/>') +
		html_end()
		)
	at_fpcu.dimension = u.F/u.L**2
	
	# epscu
	at_epscu = MpcAttributeMetaData()
	at_epscu.type = MpcAttributeType.Real
	at_epscu.name = 'epscu'
	at_epscu.group = 'Non-linear'
	at_epscu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epscu')+'<br/>') + 
		html_par('concrete strain at crushing strength*') +
		html_par('Compressive concrete parameters should be input as negative values.') +
		html_par('The initial slope for this model is (2*fpc/epsc0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete01_Material_With_Stuff_in_the_Cracks','Concrete01 Material With Stuff in the Cracks')+'<br/>') +
		html_end()
		)
	
	# use_endStrainSITC
	at_use_endStrainSITC = MpcAttributeMetaData()
	at_use_endStrainSITC.type = MpcAttributeType.Boolean
	at_use_endStrainSITC.name = 'use_endStrainSITC'
	at_use_endStrainSITC.group = 'Non-linear'
	at_use_endStrainSITC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_endStrainSITC')+'<br/>') + 
		html_par('optional, default = 0.03') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete01_Material_With_Stuff_in_the_Cracks','Concrete01 Material With Stuff in the Cracks')+'<br/>') +
		html_end()
		)
	
	# endStrainSITC
	at_endStrainSITC = MpcAttributeMetaData()
	at_endStrainSITC.type = MpcAttributeType.Real
	at_endStrainSITC.name = 'endStrainSITC'
	at_endStrainSITC.group = 'Optional parameters'
	at_endStrainSITC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('endStrainSITC')+'<br/>') + 
		html_par('optional, default = 0.03') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete01_Material_With_Stuff_in_the_Cracks','Concrete01 Material With Stuff in the Cracks')+'<br/>') +
		html_end()
		)
	at_endStrainSITC.setDefault(0.03)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Concrete01WithSITC'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_fpc)
	xom.addAttribute(at_epsc0)
	xom.addAttribute(at_fpcu)
	xom.addAttribute(at_epscu)
	xom.addAttribute(at_use_endStrainSITC)
	xom.addAttribute(at_endStrainSITC)
	
	# endStrainSITC-dep
	xom.setVisibilityDependency(at_use_endStrainSITC, at_endStrainSITC)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Concrete01WithSITC $matTag $fpc $epsc0 $fpcu $epsU <$endStrainSITC>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fpc_at = xobj.getAttribute('fpc')
	if(fpc_at is None):
		raise Exception('Error: cannot find "fpc" attribute')
	fpc = fpc_at.quantityScalar
	
	epsc0_at = xobj.getAttribute('epsc0')
	if(epsc0_at is None):
		raise Exception('Error: cannot find "epsc0" attribute')
	epsc0 = epsc0_at.real
	
	fpcu_at = xobj.getAttribute('fpcu')
	if(fpcu_at is None):
		raise Exception('Error: cannot find "fpcu" attribute')
	fpcu = fpcu_at.quantityScalar
	
	epscu_at = xobj.getAttribute('epscu')
	if(epscu_at is None):
		raise Exception('Error: cannot find "epscu" attribute')
	epscu = epscu_at.real
	
	
	# optional paramters
	sopt = ''
	
	use_endStrainSITC_at = xobj.getAttribute('use_endStrainSITC')
	if(use_endStrainSITC_at is None):
		raise Exception('Error: cannot find "use_endStrainSITC" attribute')
	use_endStrainSITC = use_endStrainSITC_at.boolean
	if use_endStrainSITC:
		endStrainSITC_at = xobj.getAttribute('endStrainSITC')
		if(endStrainSITC_at is None):
			raise Exception('Error: cannot find "endStrainSITC" attribute')
		endStrainSITC = endStrainSITC_at.real
		
		sopt += ' {}'.format(endStrainSITC)
	
	str_tcl = '{}uniaxialMaterial Concrete01WithSITC {} {} {} {} {}{}\n'.format(pinfo.indent, tag, fpc.value, epsc0, fpcu.value, epscu, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
	
def getMaterialProperties(xobj):
	# This function return the Material Properties necessary 
	#	for the computation of confinement:
	#		fc = Peak strength of concrete
	#		epsc0 = strain at peak strength
	#		epscu = ultimate strain
	#		Ec = Elastic modulus
	
	fc = __get_xobj_attribute(xobj, 'fpc').quantityScalar.value
	epsc0 = __get_xobj_attribute(xobj, 'epsc0').real
	epscu = __get_xobj_attribute(xobj, 'epscu').real
	Ec = 2 * fc / epsc0
	
	return (fc, epsc0, epscu, Ec)
	
def getParamsConfinedVersion(xobj,fcc,epscc0,epsccu,fccu):
	# This function returns the paramters of the materials
	#	in confined version, given the main parameters

	# Estimate fracture energy
	gc = 0.5 * epscc0 * fcc + 0.5 * (fcc + fccu) * (epsccu - epscc0)
	
	# get Parameters of unconfined version
	fc = __get_xobj_attribute(xobj, 'fpc').quantityScalar.value
	epsc0 = __get_xobj_attribute(xobj, 'epsc0').real
	fcu = __get_xobj_attribute(xobj, 'fpcu').quantityScalar.value
	epscu = __get_xobj_attribute(xobj, 'epscu').real
	Ec = 2 * fc / epsc0
	
	# Mantain E and compute a different epsc0
	epscc0 = 2 * fcc / Ec
	# epscc0 = (epscc0 + (2 * fcc / Ec))/2
	
	# # Option 1: pass through point fccu, epsccu but tend to the same residual as unconfined
	# epsccu = epscc0 + (fcu - fcc) * (epsccu - epscc0) / (fccu - fcc)
	# fccu = fcu
	
	# Option 2: proposal energy equivalence
	# Increase residual stress by same ammount of peak stress TODO: check if something better can be done
	fccu = fcu * fcc / fc
	epsccu = (2 * gc - fcc * epscc0)/(fcc + fccu) + epscc0
	
	params = (fcc, epscc0, fccu, epsccu)
	
	use_endStrainSITC = __get_xobj_attribute(xobj, 'use_endStrainSITC').boolean
	if use_endStrainSITC:
		endStrainSITC = __get_xobj_attribute(xobj, 'endStrainSITC').real
		params += (endStrainSITC,)
	
	return params