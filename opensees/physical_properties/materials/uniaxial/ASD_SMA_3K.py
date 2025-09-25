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
		html_par('Initial stiffness (k1 &gt; 0)') +
		html_par(html_href(' ',' ')+'<br/>') +
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
		html_par('Post-Activation Stiffness (0 &le; k2 &lt; k1)') +
		html_par(html_href(' ',' ')+'<br/>') +
		html_end()
		)
	at_k2.dimension = u.F/u.L

	# k3
	at_k3 = MpcAttributeMetaData()
	at_k3.type = MpcAttributeType.QuantityScalar
	at_k3.name = 'k3'
	at_k3.group = 'Non-linear'
	at_k3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k3')+'<br/>') +
		html_par('Unloading Stiffness (k2 &lt; k3 &le k1)') +
		html_par(html_href(' ',' ')+'<br/>') +
		html_end()
		)
	at_k3.dimension = u.F/u.L
	
	# sigAct
	at_sigAct = MpcAttributeMetaData()
	at_sigAct.type = MpcAttributeType.QuantityScalar
	at_sigAct.name = 'sigAct'
	at_sigAct.group = 'Non-linear'
	at_sigAct.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sigAct')+'<br/>') + 
		html_par('Forward Activation Stress/Force (sigAct &gt; 0)') +
		html_par(html_href(' ',' ')+'<br/>') +
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
		html_par('Ratio of Forward to Reverse Activation Stress/Force (0 &le; beta &le; 1)') +
		html_par(html_href(' ',' ')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASD_SMA_3K'
	xom.Xgroup = 'ASDEASoftware'
	xom.addAttribute(at_k1)
	xom.addAttribute(at_k2)
	xom.addAttribute(at_k3)
	xom.addAttribute(at_sigAct)
	xom.addAttribute(at_beta)
	
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ASD_SMA_3K $matTag $k1 $k2 $k3 $sigAct $beta 
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	k1_at = xobj.getAttribute('k1')
	if(k1_at is None):
		raise Exception('Error: cannot find "k1" attribute')
	k1 = k1_at.quantityScalar.value
	
	k2_at = xobj.getAttribute('k2')
	if(k2_at is None):
		raise Exception('Error: cannot find "k2" attribute')
	k2 = k2_at.quantityScalar.value

	k3_at = xobj.getAttribute('k3')
	if(k3_at is None):
		raise Exception('Error: cannot find "k3" attribute')
	k3 = k3_at.quantityScalar.value
	
	sigAct_at = xobj.getAttribute('sigAct')
	if(sigAct_at is None):
		raise Exception('Error: cannot find "sigAct" attribute')
	sigAct = sigAct_at.quantityScalar.value
	
	beta_at = xobj.getAttribute('beta')
	if(beta_at is None):
		raise Exception('Error: cannot find "beta" attribute')
	beta = beta_at.real
	
	# checks
	if k1 <= 0:
		raise Exception('Error: "k1" ({}) should be strictly positive (k1 > 0)'.format(k1))
	if k2 < 0 or k2 >= k1:
		raise Exception('Error: "k2" ({}) should be larger than or equal to zero and less than "k1" (0 <= k2 < k1)'.format(k2))
	if k3 <= k2 or k3 > k1:
		raise Exception('Error: "k3" ({}) should be larger than or equal to "k2" and less than or equal to "k1" (k2 &le; k3 &le k1)'.format(k3))
	if sigAct <= 0:
		raise Exception('Error: "sigAct" ({}) should be strictly positive (sigAct > 0)'.format(sigAct))
	if beta < 0 or beta > 1:
		raise Exception('Error: "beta" ({}) should be in the range 0-1 (0 <= beta <= 1)'.format(beta))
	
	# done
	str_tcl = '{}uniaxialMaterial ASD_SMA_3K {} {} {} {} {} {}\n'.format(pinfo.indent, tag, k1, k2, k3, sigAct, beta)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)