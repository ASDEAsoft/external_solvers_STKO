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
	
	# fpcc
	at_fpcc = MpcAttributeMetaData()
	at_fpcc.type = MpcAttributeType.QuantityScalar
	at_fpcc.name = 'fpcc'
	at_fpcc.group = 'Non-linear'
	at_fpcc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fpcc')+'<br/>') + 
		html_par('Compressive strength (f\'c)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
		html_end()
		)
	at_fpcc.dimension = u.F/u.L**2
	
	# epcc
	at_epcc = MpcAttributeMetaData()
	at_epcc.type = MpcAttributeType.Real
	at_epcc.name = 'epcc'
	at_epcc.group = 'Non-linear'
	at_epcc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epcc')+'<br/>') + 
		html_par('Strain at compressive strength (ε\'c)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
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
		html_par('Initial tangent modulus (Ec)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
		html_end()
		)
	at_Ec.dimension = u.F/u.L**2
	
	# rc
	at_rc = MpcAttributeMetaData()
	at_rc.type = MpcAttributeType.Real
	at_rc.name = 'rc'
	at_rc.group = 'Non-linear'
	at_rc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rc')+'<br/>') + 
		html_par('Shape parameter in Tsai’s equation defined for compression (rc)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
		html_end()
		)
	
	# xcrn
	at_xcrn = MpcAttributeMetaData()
	at_xcrn.type = MpcAttributeType.Real
	at_xcrn.name = 'xcrn'
	at_xcrn.group = 'Non-linear'
	at_xcrn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('xcrn')+'<br/>') + 
		html_par('Non-dimensional critical strain on compression envelope (ε-cr, where the envelope curve starts following a straight line)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
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
		html_par('Tensile strength(ft)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
		html_end()
		)
	at_ft.dimension = u.F/u.L**2
	
	# et
	at_et = MpcAttributeMetaData()
	at_et.type = MpcAttributeType.Real
	at_et.name = 'et'
	at_et.group = 'Non-linear'
	at_et.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('et')+'<br/>') + 
		html_par('Strain at tensile strength (εt)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
		html_end()
		)
	
	# rt
	at_rt = MpcAttributeMetaData()
	at_rt.type = MpcAttributeType.Real
	at_rt.name = 'rt'
	at_rt.group = 'Non-linear'
	at_rt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rt')+'<br/>') + 
		html_par('Shape parameter in Tsai’s equation defined for tension (rt)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
		html_end()
		)
	
	# xcrp
	at_xcrp = MpcAttributeMetaData()
	at_xcrp.type = MpcAttributeType.Real
	at_xcrp.name = 'xcrp'
	at_xcrp.group = 'Non-linear'
	at_xcrp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('xcrp')+'<br/>') + 
		html_par('Non-dimensional critical strain on tension envelope (ε+cr, where the envelope curve starts following a straight line – large value [e.g., 10000] recommended when tension stiffening is considered)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
		html_end()
		)
	
	# -GapClose
	at_GapClose = MpcAttributeMetaData()
	at_GapClose.type = MpcAttributeType.Boolean
	at_GapClose.name = '-GapClose'
	at_GapClose.group = 'Non-linear'
	at_GapClose.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-GapClose')+'<br/>') + 
		html_par('gap = 0, less gradual gap closure (default); gap = 1, more gradual gap closure') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
		html_end()
		)
	
	# gap
	at_gap = MpcAttributeMetaData()
	at_gap.type = MpcAttributeType.Integer
	at_gap.name = 'gap'
	at_gap.group = '-GapClose'
	at_gap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gap')+'<br/>') + 
		html_par('gap = 0, less gradual gap closure (default); gap = 1, more gradual gap closure') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM Material')+'<br/>') +
		html_end()
		)
	at_gap.setDefault(0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ConcreteCM'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_fpcc)
	xom.addAttribute(at_epcc)
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_rc)
	xom.addAttribute(at_xcrn)
	xom.addAttribute(at_ft)
	xom.addAttribute(at_et)
	xom.addAttribute(at_rt)
	xom.addAttribute(at_xcrp)
	xom.addAttribute(at_GapClose)
	xom.addAttribute(at_gap)
	
	# GapClose-dep
	xom.setVisibilityDependency(at_GapClose, at_gap)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ConcreteCM $mattag $fpcc $epcc $Ec $rc $xcrn $ft $et $rt $xcrp <-GapClose $gap>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fpcc_at = xobj.getAttribute('fpcc')
	if(fpcc_at is None):
		raise Exception('Error: cannot find "fpcc" attribute')
	fpcc = fpcc_at.quantityScalar
	
	epcc_at = xobj.getAttribute('epcc')
	if(epcc_at is None):
		raise Exception('Error: cannot find "epcc" attribute')
	epcc = epcc_at.real
	
	Ec_at = xobj.getAttribute('Ec')
	if(Ec_at is None):
		raise Exception('Error: cannot find "Ec" attribute')
	Ec = Ec_at.quantityScalar
	
	rc_at = xobj.getAttribute('rc')
	if(rc_at is None):
		raise Exception('Error: cannot find "rc" attribute')
	rc = rc_at.real
	
	xcrn_at = xobj.getAttribute('xcrn')
	if(xcrn_at is None):
		raise Exception('Error: cannot find "xcrn" attribute')
	xcrn = xcrn_at.real
	
	ft_at = xobj.getAttribute('ft')
	if(ft_at is None):
		raise Exception('Error: cannot find "ft" attribute')
	ft = ft_at.quantityScalar
	
	et_at = xobj.getAttribute('et')
	if(et_at is None):
		raise Exception('Error: cannot find "et" attribute')
	et = et_at.real
	
	rt_at = xobj.getAttribute('rt')
	if(rt_at is None):
		raise Exception('Error: cannot find "rt" attribute')
	rt = rt_at.real
	
	xcrp_at = xobj.getAttribute('xcrp')
	if(xcrp_at is None):
		raise Exception('Error: cannot find "xcrp" attribute')
	xcrp = xcrp_at.real
	
	
	# optional paramters
	sopt = ''
	
	GapClose_at = xobj.getAttribute('-GapClose')
	if(GapClose_at is None):
		raise Exception('Error: cannot find "-GapClose" attribute')
	GapClose = GapClose_at.boolean
	if GapClose:
		gap_at = xobj.getAttribute('gap')
		if(gap_at is None):
			raise Exception('Error: cannot find "gap" attribute')
		gap = gap_at.integer
		
		sopt += '-GapClose {}'.format(gap)
	
	str_tcl = '{}uniaxialMaterial ConcreteCM {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fpcc.value, epcc, Ec.value, rc, xcrn, ft.value, et, rt, xcrp, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
	
def getMaterialProperties(xobj):
	# This function return the Material Properties necessary 
	#	for the computation of confinement:
	#		fc = Peak strength of concrete
	#		epsc0 = strain at peak strength
	#		epscu = ultimate strain
	#		Ec = Elastic modulus
	
	fc = __get_xobj_attribute(xobj, 'fpcc').quantityScalar.value
	epsc0 = __get_xobj_attribute(xobj, 'epcc').real
	epscu = __get_xobj_attribute(xobj, 'xcrn').real * epsc0
	Ec = __get_xobj_attribute(xobj, 'Ec').quantityScalar.value
	
	return (fc, epsc0, epscu, Ec)
	
def getParamsConfinedVersion(xobj,fcc,epscc0,epsccu,fccu):
	# This function returns the paramters of the materials
	#	in confined version, given the main parameters
	
	# get Parameters of unconfined version
	fc = __get_xobj_attribute(xobj, 'fpcc').quantityScalar.value
	e0 = __get_xobj_attribute(xobj, 'epcc').real
	Ec = __get_xobj_attribute(xobj, 'Ec').quantityScalar.value
	rc = __get_xobj_attribute(xobj, 'rc').real
	xcrn = __get_xobj_attribute(xobj, 'xcrn').real
	ft = __get_xobj_attribute(xobj, 'ft').quantityScalar.value
	et = __get_xobj_attribute(xobj, 'et').real
	rt = __get_xobj_attribute(xobj, 'rt').real
	xcrp = __get_xobj_attribute(xobj, 'xcrp').real
	
	params = (fcc, epscc0, Ec, rc, xcrn, ft, et, rt, xcrp)
	GapClose = __get_xobj_attribute(xobj, '-GapClose').boolean
	if GapClose:
		gap = __get_xobj_attribute(xobj, 'gap').integer
		params += ("-GapClose", gap)
	
	return params