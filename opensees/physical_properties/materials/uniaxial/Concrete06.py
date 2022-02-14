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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete06_Material','Concrete06 Material')+'<br/>') +
		html_end()
		)
	at_fc.dimension = u.F/u.L**2
	
	# e0
	at_e0 = MpcAttributeMetaData()
	at_e0.type = MpcAttributeType.Real
	at_e0.name = 'e0'
	at_e0.group = 'Non-linear'
	at_e0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e0')+'<br/>') + 
		html_par('strain at compressive strength*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete06_Material','Concrete06 Material')+'<br/>') +
		html_end()
		)
	
	# n
	at_n = MpcAttributeMetaData()
	at_n.type = MpcAttributeType.Real
	at_n.name = 'n'
	at_n.group = 'Non-linear'
	at_n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('n')+'<br/>') + 
		html_par('compressive shape factor') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete06_Material','Concrete06 Material')+'<br/>') +
		html_end()
		)
		
	# k
	at_k = MpcAttributeMetaData()
	at_k.type = MpcAttributeType.Real
	at_k.name = 'k'
	at_k.group = 'Linear'
	at_k.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k')+'<br/>') + 
		html_par('post-peak compressive shape factor*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete06_Material','Concrete06 Material')+'<br/>') +
		html_end()
		)
	
	# alpha1
	at_alpha1 = MpcAttributeMetaData()
	at_alpha1.type = MpcAttributeType.Real
	at_alpha1.name = 'alpha1'
	at_alpha1.group = 'Non-linear'
	at_alpha1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha1')+'<br/>') + 
		html_par('floating point value defining the maximum tensile strength of concrete') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete06_Material','Concrete06 Material')+'<br/>') +
		html_end()
		)
	
	# fcr
	at_fcr = MpcAttributeMetaData()
	at_fcr.type = MpcAttributeType.QuantityScalar
	at_fcr.name = 'fcr'
	at_fcr.group = 'Non-linear'
	at_fcr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fcr')+'<br/>') + 
		html_par('tensile strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete06_Material','Concrete06 Material')+'<br/>') +
		html_end()
		)
	at_fcr.dimension = u.F/u.L**2
	
	# ecr
	at_ecr = MpcAttributeMetaData()
	at_ecr.type = MpcAttributeType.Real
	at_ecr.name = 'ecr'
	at_ecr.group = 'Non-linear'
	at_ecr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ecr')+'<br/>') + 
		html_par('tensile strain at peak stress ($fcr)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete06_Material','Concrete06 Material')+'<br/>') +
		html_end()
		)
	
	# b
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.Real
	at_b.name = 'b'
	at_b.group = 'Non-linear'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b')+'<br/>') + 
		html_par('exponent of the tension stiffening curve') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete06_Material','Concrete06 Material')+'<br/>') +
		html_end()
		)
	
	# alpha2
	at_alpha2 = MpcAttributeMetaData()
	at_alpha2.type = MpcAttributeType.Real
	at_alpha2.name = 'alpha2'
	at_alpha2.group = 'Non-linear'
	at_alpha2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha2')+'<br/>') + 
		html_par('α2 parameter for tensile plastic strain definition') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Concrete06_Material','Concrete06 Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Concrete06'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_fc)
	xom.addAttribute(at_e0)
	xom.addAttribute(at_n)
	xom.addAttribute(at_k)
	xom.addAttribute(at_alpha1)
	xom.addAttribute(at_fcr)
	xom.addAttribute(at_ecr)
	xom.addAttribute(at_b)
	xom.addAttribute(at_alpha2)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Concrete06 $matTag $fc $e0 $n $k $alpha1 $fcr $ecr $b $alpha2
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fc_at = xobj.getAttribute('fc')
	if(fc_at is None):
		raise Exception('Error: cannot find "fc" attribute')
	fc = fc_at.quantityScalar
	
	e0_at = xobj.getAttribute('e0')
	if(e0_at is None):
		raise Exception('Error: cannot find "e0" attribute')
	e0 = e0_at.real
	
	n_at = xobj.getAttribute('n')
	if(n_at is None):
		raise Exception('Error: cannot find "n" attribute')
	n = n_at.real
	
	k_at = xobj.getAttribute('k')
	if(k_at is None):
		raise Exception('Error: cannot find "k" attribute')
	k = k_at.real
	
	alpha1_at = xobj.getAttribute('alpha1')
	if(alpha1_at is None):
		raise Exception('Error: cannot find "alpha1" attribute')
	alpha1 = alpha1_at.real
	
	fcr_at = xobj.getAttribute('fcr')
	if(fcr_at is None):
		raise Exception('Error: cannot find "fcr" attribute')
	fcr = fcr_at.quantityScalar
	
	ecr_at = xobj.getAttribute('ecr')
	if(ecr_at is None):
		raise Exception('Error: cannot find "ecr" attribute')
	ecr = ecr_at.real
	
	b_at = xobj.getAttribute('b')
	if(b_at is None):
		raise Exception('Error: cannot find "b" attribute')
	b = b_at.real
	
	alpha2_at = xobj.getAttribute('alpha2')
	if(alpha2_at is None):
		raise Exception('Error: cannot find "alpha2" attribute')
	alpha2 = alpha2_at.real
	
	
	str_tcl = '{}uniaxialMaterial Concrete06 {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fc.value, e0, n, k, alpha1, fcr.value, ecr, b, alpha2)
	
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
	epsc0 = __get_xobj_attribute(xobj, 'e0').real
	epscu = 5*epsc0
	# Elastic modulus Thorendfelt
	n = __get_xobj_attribute(xobj, 'n').real
	Ec = fc * n / ((n - 1) * epsc0)
	
	return (fc, epsc0, epscu, Ec)
	
def getParamsConfinedVersion(xobj,fcc,epscc0,epsccu,fccu):
	# This function returns the paramters of the materials
	#	in confined version, given the main parameters
	
	# get Parameters of unconfined version
	fc = __get_xobj_attribute(xobj, 'fc').quantityScalar.value
	e0 = __get_xobj_attribute(xobj, 'e0').real
	n = __get_xobj_attribute(xobj, 'n').real
	k = __get_xobj_attribute(xobj, 'k').real
	alpha1 = __get_xobj_attribute(xobj, 'alpha1').real
	fcr = __get_xobj_attribute(xobj, 'fcr').quantityScalar.value
	ecr = __get_xobj_attribute(xobj, 'ecr').real
	b = __get_xobj_attribute(xobj, 'b').real
	alpha2 = __get_xobj_attribute(xobj, 'alpha2').real
	
	Ec = fc * n / ((n - 1) * e0)
	
	# Calculate confined version
	# Solve for n
	nA = 1
	nB = 3
	yA = fcc * (nA * (epsccu/epscc0)) / (nA - 1 + (epsccu/epscc0)**(nA*k)) - fccu
	yB = fcc * (nB * (epsccu/epscc0)) / (nB - 1 + (epsccu/epscc0)**(nB*k)) - fccu
	tol = 1e-2
	ITMAX = 20
	it = 0
	while (abs(nA-nB) > tol) and (it <= ITMAX):
		nC = (nA + nB) / 2.0
		yC = fcc * (nC * (epsccu/epscc0)) / (nC - 1 + (epsccu/epscc0)**(nC*k)) - fccu
		if (yC * yA) > 0:
			#solution is between C and B
			yA, nA = yC, nC
		else:
			#solution is between A and Calculate
			yB, nB = yC, nC
		it += 1
	# print('Computed n = ', nC)
	n = nC
	epscc0 = fc * n / ((n - 1) * Ec)
	
	return (fcc, epscc0, n, k, alpha1, fcr, ecr, b, alpha2)