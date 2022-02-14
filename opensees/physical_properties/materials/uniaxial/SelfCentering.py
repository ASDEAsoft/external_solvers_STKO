# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# k1
	at_k1 = MpcAttributeMetaData()
	at_k1.type = MpcAttributeType.QuantityScalar
	at_k1.name = 'k1'
	at_k1.group = 'Non-linear'
	at_k1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k1')+'<br/>') + 
		
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	at_k1.dimension = u.F/u.L
	
	# k2
	at_k2 = MpcAttributeMetaData()
	at_k2.type = MpcAttributeType.QuantityScalar
	at_k2.name = 'k2'
	at_k2.group = 'Non-linear'
	at_k2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k2')+'<br/>') + 
		html_par('Post-Activation Stiffness (0<k2<k1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	at_k2.dimension = u.F/u.L
	
	# sigAct
	at_sigAct = MpcAttributeMetaData()
	at_sigAct.type = MpcAttributeType.QuantityScalar
	at_sigAct.name = 'sigAct'
	at_sigAct.group = 'Non-linear'
	at_sigAct.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sigAct')+'<br/>') + 
		html_par('Forward Activation Stress/Force') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	at_sigAct.dimension = u.F/u.L**2
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'Non-linear'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') + 
		html_par('Ratio of Forward to Reverse Activation Stress/Force') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	
	# use_epsSlip
	at_use_epsSlip = MpcAttributeMetaData()
	at_use_epsSlip.type = MpcAttributeType.Boolean
	at_use_epsSlip.name = 'use_epsSlip'
	at_use_epsSlip.group = 'Non-linear'
	at_use_epsSlip.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_epsSlip')+'<br/>') + 
		html_par('slip Strain/Deformation (if epsSlip = 0, there will be no slippage)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	
	# epsSlip
	at_epsSlip = MpcAttributeMetaData()
	at_epsSlip.type = MpcAttributeType.Real
	at_epsSlip.name = 'epsSlip'
	at_epsSlip.group = 'Optional parameters'
	at_epsSlip.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsSlip')+'<br/>') + 
		html_par('slip Strain/Deformation (if epsSlip = 0, there will be no slippage)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	
	# use_epsBear
	at_use_epsBear = MpcAttributeMetaData()
	at_use_epsBear.type = MpcAttributeType.Boolean
	at_use_epsBear.name = 'use_epsBear'
	at_use_epsBear.group = 'Non-linear'
	at_use_epsBear.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_epsBear')+'<br/>') + 
		html_par('Bearing Strain/Deformation (if epsBear = 0, there will be no bearing)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	
	# epsBear
	at_epsBear = MpcAttributeMetaData()
	at_epsBear.type = MpcAttributeType.Real
	at_epsBear.name = 'epsBear'
	at_epsBear.group = 'Optional parameters'
	at_epsBear.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsBear')+'<br/>') + 
		html_par('Bearing Strain/Deformation (if epsBear = 0, there will be no bearing)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	
	# use_rBear
	at_use_rBear = MpcAttributeMetaData()
	at_use_rBear.type = MpcAttributeType.Boolean
	at_use_rBear.name = 'use_rBear'
	at_use_rBear.group = 'Non-linear'
	at_use_rBear.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_rBear')+'<br/>') + 
		html_par('Ratio of Bearing Stiffness to Initial Stiffness k1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	
	# rBear
	at_rBear = MpcAttributeMetaData()
	at_rBear.type = MpcAttributeType.Real
	at_rBear.name = 'rBear'
	at_rBear.group = 'Optional parameters'
	at_rBear.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rBear')+'<br/>') + 
		html_par('Ratio of Bearing Stiffness to Initial Stiffness k1') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/SelfCentering_Material','SelfCentering Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'SelfCentering'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_k1)
	xom.addAttribute(at_k2)
	xom.addAttribute(at_sigAct)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_use_epsSlip)
	xom.addAttribute(at_epsSlip)
	xom.addAttribute(at_use_epsBear)
	xom.addAttribute(at_epsBear)
	xom.addAttribute(at_use_rBear)
	xom.addAttribute(at_rBear)
	
	# epsSlip-dep
	xom.setVisibilityDependency(at_use_epsSlip, at_epsSlip)
	
	# epsBear-dep
	xom.setVisibilityDependency(at_use_epsBear, at_epsBear)
	
	# rBear-dep
	xom.setVisibilityDependency(at_use_rBear, at_rBear)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial SelfCentering $matTag $k1 $k2 $sigAct $beta <$epsSlip> <$epsBear> <rBear>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	k1_at = xobj.getAttribute('k1')
	if(k1_at is None):
		raise Exception('Error: cannot find "k1" attribute')
	k1 = k1_at.quantityScalar
	
	k2_at = xobj.getAttribute('k2')
	if(k2_at is None):
		raise Exception('Error: cannot find "k2" attribute')
	k2 = k2_at.quantityScalar
	
	sigAct_at = xobj.getAttribute('sigAct')
	if(sigAct_at is None):
		raise Exception('Error: cannot find "sigAct" attribute')
	sigAct = sigAct_at.quantityScalar
	
	beta_at = xobj.getAttribute('beta')
	if(beta_at is None):
		raise Exception('Error: cannot find "beta" attribute')
	beta = beta_at.real
	
	
	# optional paramters
	sopt = ''
	
	use_epsSlip_at = xobj.getAttribute('use_epsSlip')
	if(use_epsSlip_at is None):
		raise Exception('Error: cannot find "use_epsSlip" attribute')
	use_epsSlip = use_epsSlip_at.boolean
	if use_epsSlip:
		epsSlip_at = xobj.getAttribute('epsSlip')
		if(epsSlip_at is None):
			raise Exception('Error: cannot find "epsSlip" attribute')
		epsSlip = epsSlip_at.real
		
		sopt += '{}'.format(epsSlip)
	
	use_epsBear_at = xobj.getAttribute('use_epsBear')
	if(use_epsBear_at is None):
		raise Exception('Error: cannot find "use_epsBear" attribute')
	use_epsBear = use_epsBear_at.boolean
	if use_epsBear:
		epsBear_at = xobj.getAttribute('epsBear')
		if(epsBear_at is None):
			raise Exception('Error: cannot find "epsBear" attribute')
		epsBear = epsBear_at.real
		
		sopt += ' {}'.format(epsBear)
	
	use_rBear_at = xobj.getAttribute('use_rBear')
	if(use_rBear_at is None):
		raise Exception('Error: cannot find "use_rBear" attribute')
	use_rBear = use_rBear_at.boolean
	if use_rBear:
		rBear_at = xobj.getAttribute('rBear')
		if(rBear_at is None):
			raise Exception('Error: cannot find "rBear" attribute')
		rBear = rBear_at.real
		
		sopt += ' {}'.format(rBear)
	
	
	str_tcl = '{}uniaxialMaterial SelfCentering {} {} {} {} {} {}\n'.format(pinfo.indent, tag, k1.value, k2.value, sigAct.value, beta, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)