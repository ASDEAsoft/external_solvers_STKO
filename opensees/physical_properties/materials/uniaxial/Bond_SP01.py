# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Fy
	at_Fy = MpcAttributeMetaData()
	at_Fy.type = MpcAttributeType.QuantityScalar
	at_Fy.name = 'Fy'
	at_Fy.group = 'Non-linear'
	at_Fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fy')+'<br/>') + 
		html_par('Yield strength of the reinforcement steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bond_SP01_-_-_Strain_Penetration_Model_for_Fully_Anchored_Steel_Reinforcing_Bars','Bond SP01')+'<br/>') +
		html_end()
		)
	at_Fy.dimension = u.F/u.L**2
	
	# Sy
	at_Sy = MpcAttributeMetaData()
	at_Sy.type = MpcAttributeType.QuantityScalar
	at_Sy.name = 'Sy'
	at_Sy.group = 'Non-linear'
	at_Sy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Sy')+'<br/>') + 
		html_par('Rebar slip at member interface under yield stress. (see NOTES below)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bond_SP01_-_-_Strain_Penetration_Model_for_Fully_Anchored_Steel_Reinforcing_Bars','Bond SP01')+'<br/>') +
		html_end()
		)
	at_Sy.dimension = u.L
	
	# Fu
	at_Fu = MpcAttributeMetaData()
	at_Fu.type = MpcAttributeType.QuantityScalar
	at_Fu.name = 'Fu'
	at_Fu.group = 'Non-linear'
	at_Fu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fu')+'<br/>') + 
		html_par('Ultimate strength of the reinforcement steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bond_SP01_-_-_Strain_Penetration_Model_for_Fully_Anchored_Steel_Reinforcing_Bars','Bond SP01')+'<br/>') +
		html_end()
		)
	at_Fu.dimension = u.F/u.L**2
	
	# Su
	at_Su = MpcAttributeMetaData()
	at_Su.type = MpcAttributeType.QuantityScalar
	at_Su.name = 'Su'
	at_Su.group = 'Non-linear'
	at_Su.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Su')+'<br/>') + 
		html_par('Rebar slip at the loaded end at the bar fracture strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bond_SP01_-_-_Strain_Penetration_Model_for_Fully_Anchored_Steel_Reinforcing_Bars','Bond SP01')+'<br/>') +
		html_end()
		)
	at_Su.dimension = u.L
	
	# b
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.Real
	at_b.name = 'b'
	at_b.group = 'Non-linear'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b')+'<br/>') + 
		html_par('Initial hardening ratio in the monotonic slip vs. bar stress response (0.3~0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bond_SP01_-_-_Strain_Penetration_Model_for_Fully_Anchored_Steel_Reinforcing_Bars','Bond SP01')+'<br/>') +
		html_end()
		)
	
	# R
	at_R = MpcAttributeMetaData()
	at_R.type = MpcAttributeType.Real
	at_R.name = 'R'
	at_R.group = 'Non-linear'
	at_R.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R')+'<br/>') + 
		html_par('Pinching factor for the cyclic slip vs. bar response (0.5~1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bond_SP01_-_-_Strain_Penetration_Model_for_Fully_Anchored_Steel_Reinforcing_Bars','Bond SP01')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Bond_SP01'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_Sy)
	xom.addAttribute(at_Fu)
	xom.addAttribute(at_Su)
	xom.addAttribute(at_b)
	xom.addAttribute(at_R)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Bond_SP01 $matTag $Fy $Sy $Fu $Su $b $R
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	Fy_at = xobj.getAttribute('Fy')
	if(Fy_at is None):
		raise Exception('Error: cannot find "Fy" attribute')
	Fy = Fy_at.quantityScalar
	
	Sy_at = xobj.getAttribute('Sy')
	if(Sy_at is None):
		raise Exception('Error: cannot find "Sy" attribute')
	Sy = Sy_at.quantityScalar
	
	Fu_at = xobj.getAttribute('Fu')
	if(Fu_at is None):
		raise Exception('Error: cannot find "Fu" attribute')
	Fu = Fu_at.quantityScalar
	
	Su_at = xobj.getAttribute('Su')
	if(Su_at is None):
		raise Exception('Error: cannot find "Su" attribute')
	Su = Su_at.quantityScalar
	
	b_at = xobj.getAttribute('b')
	if(b_at is None):
		raise Exception('Error: cannot find "b" attribute')
	b = b_at.real
	
	R_at = xobj.getAttribute('R')
	if(R_at is None):
		raise Exception('Error: cannot find "R" attribute')
	R = R_at.real
	
	
	str_tcl = '{}uniaxialMaterial Bond_SP01 {} {} {} {} {} {} {}\n'.format(pinfo.indent, tag, Fy.value, Sy.value, Fu.value, Su.value, b, R)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)