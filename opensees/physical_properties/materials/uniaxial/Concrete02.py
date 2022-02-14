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
		html_par('Concrete compressive strength at 28 days (compression is negative)*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete02_Material_--_Linear_Tension_Softening','Concrete02 Material')+'<br/>') +
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
		html_par('Concrete strain at maximum strength*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete02_Material_--_Linear_Tension_Softening','Concrete02 Material')+'<br/>') +
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
		html_par('Concrete crushing strength *') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete02_Material_--_Linear_Tension_Softening','Concrete02 Material')+'<br/>') +
		html_end()
		)
	at_fpcu.dimension = u.F/u.L**2
	
	# epsU
	at_epsU = MpcAttributeMetaData()
	at_epsU.type = MpcAttributeType.Real
	at_epsU.name = 'epsU'
	at_epsU.group = 'Non-linear'
	at_epsU.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsU')+'<br/>') + 
		html_par('Concrete strain at crushing strength*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete02_Material_--_Linear_Tension_Softening','Concrete02 Material')+'<br/>') +
		html_end()
		)

	
	# lambda
	at_lambda = MpcAttributeMetaData()
	at_lambda.type = MpcAttributeType.Real
	at_lambda.name = 'lambda'
	at_lambda.group = 'Non-linear'
	at_lambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lambda')+'<br/>') + 
		html_par('Ratio between unloading slope at $epscu and initial slope') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete02_Material_--_Linear_Tension_Softening','Concrete02 Material')+'<br/>') +
		html_end()
		)
	
	# ft
	at_ft = MpcAttributeMetaData()
	at_ft.type = MpcAttributeType.QuantityScalar
	at_ft.name = 'ft'
	at_ft.group = 'Non-linear'
	at_ft.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ft')+'<br/>') + 
		html_par('Tensile strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete02_Material_--_Linear_Tension_Softening','Concrete02 Material')+'<br/>') +
		html_end()
		)
	at_ft.dimension = u.F/u.L**2
	
	# Ets
	at_Ets = MpcAttributeMetaData()
	at_Ets.type = MpcAttributeType.QuantityScalar
	at_Ets.name = 'Ets'
	at_Ets.group = 'Non-linear'
	at_Ets.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ets')+'<br/>') + 
		html_par('Tension softening stiffness (absolute value) (slope of the linear tension softening branch)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete02_Material_--_Linear_Tension_Softening','Concrete02 Material')+'<br/>') +
		html_end()
		)
	at_Ets.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'Concrete02'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_fpc)
	xom.addAttribute(at_epsc0)
	xom.addAttribute(at_fpcu)
	xom.addAttribute(at_epsU)
	xom.addAttribute(at_lambda)
	xom.addAttribute(at_ft)
	xom.addAttribute(at_Ets)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Concrete02 $matTag $fpc $epsc0 $fpcu $epsU $lambda $ft $Ets
	
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
	
	epsU_at = xobj.getAttribute('epsU')
	if(epsU_at is None):
		raise Exception('Error: cannot find "epsU" attribute')
	epsU = epsU_at.real
	
	lambda_at = xobj.getAttribute('lambda')
	if(lambda_at is None):
		raise Exception('Error: cannot find "lambda" attribute')
	lambd = lambda_at.real
	
	ft_at = xobj.getAttribute('ft')
	if(ft_at is None):
		raise Exception('Error: cannot find "ft" attribute')
	ft = ft_at.quantityScalar
	
	Ets_at = xobj.getAttribute('Ets')
	if(Ets_at is None):
		raise Exception('Error: cannot find "Ets" attribute')
	Ets = Ets_at.quantityScalar
	
	
	str_tcl = '{}uniaxialMaterial Concrete02 {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fpc.value, epsc0, fpcu.value, epsU, lambd, ft.value, Ets.value)
	
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
	epscu = __get_xobj_attribute(xobj, 'epsU').real
	Ec = 2 * fc / epsc0
	
	return (fc, epsc0, epscu, Ec)
	
def getParamsConfinedVersion(xobj,fcc,epscc0,epsccu,fccu):
	# This function returns the paramters of the materials
	#	in confined version, given the main parameters
	
	# get Parameters of unconfined version
	fc = __get_xobj_attribute(xobj, 'fpc').quantityScalar.value
	epsc0 = __get_xobj_attribute(xobj, 'epsc0').real
	fcu = __get_xobj_attribute(xobj, 'fpcu').quantityScalar.value
	epscu = __get_xobj_attribute(xobj, 'epsU').real
	lambd = __get_xobj_attribute(xobj, 'lambda').real
	ft = __get_xobj_attribute(xobj, 'ft').quantityScalar.value
	Ets = __get_xobj_attribute(xobj, 'Ets').quantityScalar.value
	Ec = 2 * fc / epsc0
	
	# Mantain E and compute a different epsc0
	epscc0 = 2 * fcc / Ec
	# epscc0 = (epscc0 + (2 * fcc / Ec))/2
	
	return (fcc, epscc0, fccu, epsccu, lambd, ft, Ets)