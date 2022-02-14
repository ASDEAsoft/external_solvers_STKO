# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fc
	at_fc = MpcAttributeMetaData()
	at_fc.type = MpcAttributeType.QuantityScalar
	at_fc.name = 'fc'
	at_fc.group = 'Non-linear'
	at_fc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fc')+'<br/>') + 
		html_par('concrete compressive strength *') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	at_fc.dimension = u.F/u.L**2
	
	# epsc
	at_epsc = MpcAttributeMetaData()
	at_epsc.type = MpcAttributeType.Real
	at_epsc.name = 'epsc'
	at_epsc.group = 'Non-linear'
	at_epsc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsc')+'<br/>') + 
		html_par('concrete strain at corresponding to compressive strength*') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
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
		html_par('concrete tensile strength *') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	at_ft.dimension = u.F/u.L**2
	
	# epst
	at_epst = MpcAttributeMetaData()
	at_epst.type = MpcAttributeType.Real
	at_epst.name = 'epst'
	at_epst.group = 'Non-linear'
	at_epst.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epst')+'<br/>') + 
		html_par('concrete strain at corresponding to tensile strength*') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	
	# Ec
	at_Ec = MpcAttributeMetaData()
	at_Ec.type = MpcAttributeType.QuantityScalar
	at_Ec.name = 'Ec'
	at_Ec.group = 'Non-linear'
	at_Ec.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ec')+'<br/>') + 
		html_par('concrete initial Elastic modulus*') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	at_Ec.dimension = u.F/u.L**2
	
	# alphac
	at_alphac = MpcAttributeMetaData()
	at_alphac.type = MpcAttributeType.Real
	at_alphac.name = 'alphac'
	at_alphac.group = 'Non-linear'
	at_alphac.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphac')+'<br/>') + 
		html_par('compressive descending parameter*') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	
	# alphat
	at_alphat = MpcAttributeMetaData()
	at_alphat.type = MpcAttributeType.Real
	at_alphat.name = 'alphat'
	at_alphat.group = 'Non-linear'
	at_alphat.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphat')+'<br/>') + 
		html_par('tensile descending parameter*') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	
	# use_cesp
	at_use_cesp = MpcAttributeMetaData()
	at_use_cesp.type = MpcAttributeType.Boolean
	at_use_cesp.name = 'use_cesp'
	at_use_cesp.group = 'Non-linear'
	at_use_cesp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_cesp')+'<br/>') + 
		html_par('plastic parameter, recommended values: 0.2~0.3') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	
	# cesp
	at_cesp = MpcAttributeMetaData()
	at_cesp.type = MpcAttributeType.Real
	at_cesp.name = 'cesp'
	at_cesp.group = 'Optional parameters'
	at_cesp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cesp')+'<br/>') + 
		html_par('plastic parameter, recommended values: 0.2~0.3') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	at_cesp.setDefault(0.25)
	
	# use_etap
	at_use_etap = MpcAttributeMetaData()
	at_use_etap.type = MpcAttributeType.Boolean
	at_use_etap.name = 'use_etap'
	at_use_etap.group = 'Non-linear'
	at_use_etap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_etap')+'<br/>') + 
		html_par('plastic parameter, recommended values: 1.0~1.3') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	
	# etap
	at_etap = MpcAttributeMetaData()
	at_etap.type = MpcAttributeType.Real
	at_etap.name = 'etap'
	at_etap.group = 'Optional parameters'
	at_etap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('etap')+'<br/>') + 
		html_par('plastic parameter, recommended values: 1.0~1.3') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value fc/epsc and ft/epst should be smaller than Ec.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteD','ConcreteD Material')+'<br/>') +
		html_end()
		)
	at_etap.setDefault(1.15)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ConcreteD'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_fc)
	xom.addAttribute(at_epsc)
	xom.addAttribute(at_ft)
	xom.addAttribute(at_epst)
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_alphac)
	xom.addAttribute(at_alphat)
	xom.addAttribute(at_use_cesp)
	xom.addAttribute(at_cesp)
	xom.addAttribute(at_use_etap)
	xom.addAttribute(at_etap)
	
	# cesp-dep
	xom.setVisibilityDependency(at_use_cesp, at_cesp)
	
	# etap-dep
	xom.setVisibilityDependency(at_use_etap, at_etap)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ConcreteD $matTag $fc $epsc $ft $epst $Ec $alphac $alphat <$cesp> <$etap>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fc_at = xobj.getAttribute('fc')
	if(fc_at is None):
		raise Exception('Error: cannot find "fc" attribute')
	fc = fc_at.quantityScalar
	
	epsc_at = xobj.getAttribute('epsc')
	if(epsc_at is None):
		raise Exception('Error: cannot find "epsc" attribute')
	epsc = epsc_at.real
	
	ft_at = xobj.getAttribute('ft')
	if(ft_at is None):
		raise Exception('Error: cannot find "ft" attribute')
	ft = ft_at.quantityScalar
	
	epst_at = xobj.getAttribute('epst')
	if(epst_at is None):
		raise Exception('Error: cannot find "epst" attribute')
	epst = epst_at.real
	
	Ec_at = xobj.getAttribute('Ec')
	if(Ec_at is None):
		raise Exception('Error: cannot find "Ec" attribute')
	Ec = Ec_at.quantityScalar
	
	alphac_at = xobj.getAttribute('alphac')
	if(alphac_at is None):
		raise Exception('Error: cannot find "alphac" attribute')
	alphac = alphac_at.real
	
	alphat_at = xobj.getAttribute('alphat')
	if(alphat_at is None):
		raise Exception('Error: cannot find "alphat" attribute')
	alphat = alphat_at.real
	
	
	# optional paramters
	sopt = ''
	
	use_cesp_at = xobj.getAttribute('use_cesp')
	if(use_cesp_at is None):
		raise Exception('Error: cannot find "use_cesp" attribute')
	use_cesp = use_cesp_at.boolean
	if use_cesp:
		cesp_at = xobj.getAttribute('cesp')
		if(cesp_at is None):
			raise Exception('Error: cannot find "cesp" attribute')
		cesp = cesp_at.real
		
		sopt += '{}'.format(cesp)
	
	use_etap_at = xobj.getAttribute('use_etap')
	if(use_etap_at is None):
		raise Exception('Error: cannot find "use_etap" attribute')
	use_etap = use_etap_at.boolean
	if use_etap:
		etap_at = xobj.getAttribute('etap')
		if(etap_at is None):
			raise Exception('Error: cannot find "etap" attribute')
		etap = etap_at.real
		
		sopt += ' {}'.format(etap)
	
	
	str_tcl = '{}uniaxialMaterial ConcreteD {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fc.value, epsc, ft.value, epst, Ec.value, alphac, alphat, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)