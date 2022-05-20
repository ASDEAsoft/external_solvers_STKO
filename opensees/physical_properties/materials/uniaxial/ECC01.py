# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# sigt0
	at_sigt0 = MpcAttributeMetaData()
	at_sigt0.type = MpcAttributeType.QuantityScalar
	at_sigt0.name = 'sigt0'
	at_sigt0.group = 'Non-linear'
	at_sigt0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sigt0')+'<br/>') + 
		html_par('tensile cracking stress') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	at_sigt0.dimension = u.F/u.L**2
	
	# epst0
	at_epst0 = MpcAttributeMetaData()
	at_epst0.type = MpcAttributeType.Real
	at_epst0.name = 'epst0'
	at_epst0.group = 'Non-linear'
	at_epst0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epst0')+'<br/>') + 
		html_par('strain at tensile cracking stress') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	# sigt1
	at_sigt1 = MpcAttributeMetaData()
	at_sigt1.type = MpcAttributeType.QuantityScalar
	at_sigt1.name = 'sigt1'
	at_sigt1.group = 'Non-linear'
	at_sigt1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sigt1')+'<br/>') + 
		html_par('peak tensile stress') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	at_sigt1.dimension = u.F/u.L**2
	
	# epst1
	at_epst1 = MpcAttributeMetaData()
	at_epst1.type = MpcAttributeType.Real
	at_epst1.name = 'epst1'
	at_epst1.group = 'Non-linear'
	at_epst1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epst1')+'<br/>') + 
		html_par('strain at peak tensile stress') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
		
	# epst1
	at_epst2 = MpcAttributeMetaData()
	at_epst2.type = MpcAttributeType.Real
	at_epst2.name = 'epst2'
	at_epst2.group = 'Non-linear'
	at_epst2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epst2')+'<br/>') + 
		html_par('strain at peak tensile stress') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	# sigc0
	at_sigc0 = MpcAttributeMetaData()
	at_sigc0.type = MpcAttributeType.QuantityScalar
	at_sigc0.name = 'sigc0'
	at_sigc0.group = 'Non-linear'
	at_sigc0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sigc0')+'<br/>') + 
		html_par('compressive strength (see NOTES)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	at_sigc0.dimension = u.F/u.L**2
	
	# epsc0
	at_epsc0 = MpcAttributeMetaData()
	at_epsc0.type = MpcAttributeType.Real
	at_epsc0.name = 'epsc0'
	at_epsc0.group = 'Non-linear'
	at_epsc0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsc0')+'<br/>') + 
		html_par('strain at compressive strength (see NOTES)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	# epsc1
	at_epsc1 = MpcAttributeMetaData()
	at_epsc1.type = MpcAttributeType.Real
	at_epsc1.name = 'epsc1'
	at_epsc1.group = 'Non-linear'
	at_epsc1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsc1')+'<br/>') + 
		html_par('ultimate compressive strain (see NOTES)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	# alphaT1
	at_alphaT1 = MpcAttributeMetaData()
	at_alphaT1.type = MpcAttributeType.Real
	at_alphaT1.name = 'alphaT1'
	at_alphaT1.group = 'Non-linear'
	at_alphaT1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaT1')+'<br/>') + 
		html_par('exponent of the unloading curve in tensile strain hardening region') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	# alphaT2
	at_alphaT2 = MpcAttributeMetaData()
	at_alphaT2.type = MpcAttributeType.Real
	at_alphaT2.name = 'alphaT2'
	at_alphaT2.group = 'Non-linear'
	at_alphaT2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaT2')+'<br/>') + 
		html_par('exponent of the unloading curve in tensile softening region') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	# alphaC
	at_alphaC = MpcAttributeMetaData()
	at_alphaC.type = MpcAttributeType.Real
	at_alphaC.name = 'alphaC'
	at_alphaC.group = 'Non-linear'
	at_alphaC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaC')+'<br/>') + 
		html_par('exponent of the unloading curve in the compressive softening') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	# alphaCU
	at_alphaCU = MpcAttributeMetaData()
	at_alphaCU.type = MpcAttributeType.Real
	at_alphaCU.name = 'alphaCU'
	at_alphaCU.group = 'Non-linear'
	at_alphaCU.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alphaCU')+'<br/>') + 
		html_par('exponent of the compressive softening curve (use 1 for linear softening)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	# betaT
	at_betaT = MpcAttributeMetaData()
	at_betaT.type = MpcAttributeType.Real
	at_betaT.name = 'betaT'
	at_betaT.group = 'Non-linear'
	at_betaT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('betaT')+'<br/>') + 
		html_par('parameter to determine permanent strain in tension') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	# betaC
	at_betaC = MpcAttributeMetaData()
	at_betaC.type = MpcAttributeType.Real
	at_betaC.name = 'betaC'
	at_betaC.group = 'Non-linear'
	at_betaC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('betaC')+'<br/>') + 
		html_par('parameter to determine permanent strain in compression') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Engineered_Cementitious_Composites_Material','Engineered Cementitious Composites Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ECC01'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_sigt0)
	xom.addAttribute(at_epst0)
	xom.addAttribute(at_sigt1)
	xom.addAttribute(at_epst1)
	xom.addAttribute(at_epst2)
	xom.addAttribute(at_sigc0)
	xom.addAttribute(at_epsc0)
	xom.addAttribute(at_epsc1)
	xom.addAttribute(at_alphaT1)
	xom.addAttribute(at_alphaT2)
	xom.addAttribute(at_alphaC)
	xom.addAttribute(at_alphaCU)
	xom.addAttribute(at_betaT)
	xom.addAttribute(at_betaC)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ECC01 $matTag $sigt0 $epst0 $sigt1 $epst1 $epst2 $sigc0
	#$epsc0 $epsc1 $alphaT1 $alphaT2 $alphaC $alphaCU $betaT $betaC
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	sigt0_at = xobj.getAttribute('sigt0')
	if(sigt0_at is None):
		raise Exception('Error: cannot find "sigt0" attribute')
	sigt0 = sigt0_at.quantityScalar.value
	
	epst0_at = xobj.getAttribute('epst0')
	if(epst0_at is None):
		raise Exception('Error: cannot find "epst0" attribute')
	epst0 = epst0_at.real
	
	sigt1_at = xobj.getAttribute('sigt1')
	if(sigt1_at is None):
		raise Exception('Error: cannot find "sigt1" attribute')
	sigt1 = sigt1_at.quantityScalar.value
	
	epst1_at = xobj.getAttribute('epst1')
	if(epst1_at is None):
		raise Exception('Error: cannot find "epst1" attribute')
	epst1 = epst1_at.real
	
	epst2_at = xobj.getAttribute('epst2')
	if(epst2_at is None):
		raise Exception('Error: cannot find "epst2" attribute')
	epst2 = epst2_at.real
	
	sigc0_at = xobj.getAttribute('sigc0')
	if(sigc0_at is None):
		raise Exception('Error: cannot find "sigc0" attribute')
	sigc0 = sigc0_at.quantityScalar.value
	
	epsc0_at = xobj.getAttribute('epsc0')
	if(epsc0_at is None):
		raise Exception('Error: cannot find "epsc0" attribute')
	epsc0 = epsc0_at.real
	
	epsc1_at = xobj.getAttribute('epsc1')
	if(epsc1_at is None):
		raise Exception('Error: cannot find "epsc1" attribute')
	epsc1 = epsc1_at.real
	
	alphaT1_at = xobj.getAttribute('alphaT1')
	if(alphaT1_at is None):
		raise Exception('Error: cannot find "alphaT1" attribute')
	alphaT1 = alphaT1_at.real
	
	alphaT2_at = xobj.getAttribute('alphaT2')
	if(alphaT2_at is None):
		raise Exception('Error: cannot find "alphaT2" attribute')
	alphaT2 = alphaT2_at.real
	
	alphaC_at = xobj.getAttribute('alphaC')
	if(alphaC_at is None):
		raise Exception('Error: cannot find "alphaC" attribute')
	alphaC = alphaC_at.real
	
	alphaCU_at = xobj.getAttribute('alphaCU')
	if(alphaCU_at is None):
		raise Exception('Error: cannot find "alphaCU" attribute')
	alphaCU = alphaCU_at.real
	
	betaT_at = xobj.getAttribute('betaT')
	if(betaT_at is None):
		raise Exception('Error: cannot find "betaT" attribute')
	betaT = betaT_at.real
	
	betaC_at = xobj.getAttribute('betaC')
	if(betaC_at is None):
		raise Exception('Error: cannot find "betaC" attribute')
	betaC = betaC_at.real
	
	
	str_tcl = '{}uniaxialMaterial ECC01 {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, sigt0, epst0, sigt1, epst1, epst2, sigc0, epsc0, epsc1, alphaT1, alphaT2, alphaC, alphaCU, betaT, betaC)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)