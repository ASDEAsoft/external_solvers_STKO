# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester2DPlaneStress import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin


def makeXObjectMetaData():
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Non-linear'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('Material density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM - 2D RC Panel Constitutive Behavior')+'<br/>') +
		html_end()
		)
	#at_rho.dimension = u.M/u.L**3
	
	# sX
	at_sX = MpcAttributeMetaData()
	at_sX.type = MpcAttributeType.Index
	at_sX.name = 'sX'
	at_sX.group = 'Non-linear'
	at_sX.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sX')+'<br/>') + 
		html_par('Tag of uniaxialMaterial simulating horizontal (x) reinforcement') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM - 2D RC Panel Constitutive Behavior')+'<br/>') +
		html_end()
		)
	at_sX.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_sX.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# sY
	at_sY = MpcAttributeMetaData()
	at_sY.type = MpcAttributeType.Index
	at_sY.name = 'sY'
	at_sY.group = 'Non-linear'
	at_sY.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sY')+'<br/>') + 
		html_par('Tag of uniaxialMaterial simulating vertical (y) reinforcement') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM - 2D RC Panel Constitutive Behavior')+'<br/>') +
		html_end()
		)
	at_sY.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_sY.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# conc
	at_conc = MpcAttributeMetaData()
	at_conc.type = MpcAttributeType.Index
	at_conc.name = 'conc'
	at_conc.group = 'Non-linear'
	at_conc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('conc')+'<br/>') + 
		html_par('Tag of uniaxialMaterial(1) simulating concrete') +
		html_par('(1) nDMaterial FSAM shall be used with uniaxialMaterial ' + html_href('http://opensees.berkeley.edu/wiki/index.php/ConcreteCM_-_Complete_Concrete_Model_by_Chang_and_Mander_(1994)','ConcreteCM')) +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM - 2D RC Panel Constitutive Behavior')+'<br/>') +
		html_end()
		)
	at_conc.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_conc.indexSource.addAllowedNamespace('materials.uniaxial')
	at_conc.indexSource.addAllowedClass('ConcreteCM')
	
	# rouX
	at_rouX = MpcAttributeMetaData()
	at_rouX.type = MpcAttributeType.Real
	at_rouX.name = 'rouX'
	at_rouX.group = 'Non-linear'
	at_rouX.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rouX')+'<br/>') + 
		html_par('Reinforcing ratio in horizontal (x) direction (rouX = As,x/Agross,x)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM - 2D RC Panel Constitutive Behavior')+'<br/>') +
		html_end()
		)
	
	# rouY
	at_rouY = MpcAttributeMetaData()
	at_rouY.type = MpcAttributeType.Real
	at_rouY.name = 'rouY'
	at_rouY.group = 'Non-linear'
	at_rouY.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rouY')+'<br/>') + 
		html_par('Reinforcing ratio in vertical (y) direction (rouY = As,y/Agross,y)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM - 2D RC Panel Constitutive Behavior')+'<br/>') +
		html_end()
		)
	
	# nu
	at_nu = MpcAttributeMetaData()
	at_nu.type = MpcAttributeType.Real
	at_nu.name = 'nu'
	at_nu.group = 'Non-linear'
	at_nu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nu')+'<br/>') + 
		html_par('Concrete friction coefficient (0.0 &lt; nu &lt; 1.5)') +	#(&lt; <) (&gt; >)
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM - 2D RC Panel Constitutive Behavior')+'<br/>') +
		html_end()
		)
	
	# alfadow
	at_alfadow = MpcAttributeMetaData()
	at_alfadow.type = MpcAttributeType.Real
	at_alfadow.name = 'alfadow'
	at_alfadow.group = 'Non-linear'
	at_alfadow.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alfadow')+'<br/>') + 
		html_par('Stiffness coefficient of reinforcement dowel action (0.0 &lt; alfadow &lt; 0.05)') +	#(&lt; <) (&gt; >)
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM - 2D RC Panel Constitutive Behavior')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'FSAM'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_rho)
	xom.addAttribute(at_sX)
	xom.addAttribute(at_sY)
	xom.addAttribute(at_conc)
	xom.addAttribute(at_rouX)
	xom.addAttribute(at_rouY)
	xom.addAttribute(at_nu)
	xom.addAttribute(at_alfadow)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial FSAM $mattag $rho $sX $sY $conc $rouX $rouY $nu $alfadow
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	rho_at = xobj.getAttribute('rho')
	if(rho_at is None):
		raise Exception('Error: cannot find "rho" attribute')
	rho = rho_at.quantityScalar
	
	sX_at = xobj.getAttribute('sX')
	if(sX_at is None):
		raise Exception('Error: cannot find "sX" attribute')
	sX = sX_at.index
	
	sY_at = xobj.getAttribute('sY')
	if(sY_at is None):
		raise Exception('Error: cannot find "sY" attribute')
	sY = sY_at.index
	
	conc_at = xobj.getAttribute('conc')
	if(conc_at is None):
		raise Exception('Error: cannot find "conc" attribute')
	conc = conc_at.index
	
	rouX_at = xobj.getAttribute('rouX')
	if(rouX_at is None):
		raise Exception('Error: cannot find "rouX" attribute')
	rouX = rouX_at.real
	
	rouY_at = xobj.getAttribute('rouY')
	if(rouY_at is None):
		raise Exception('Error: cannot find "rouY" attribute')
	rouY = rouY_at.real
	
	nu_at = xobj.getAttribute('nu')
	if(nu_at is None):
		raise Exception('Error: cannot find "nu" attribute')
	nu = nu_at.real
	
	alfadow_at = xobj.getAttribute('alfadow')
	if(alfadow_at is None):
		raise Exception('Error: cannot find "alfadow" attribute')
	alfadow = alfadow_at.real
	
	str_tcl = '{}nDMaterial FSAM {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, rho.value, sX, sY, conc, rouX, rouY, nu, alfadow)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)