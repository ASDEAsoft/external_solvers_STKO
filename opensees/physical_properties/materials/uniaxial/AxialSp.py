# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# sce
	at_sce = MpcAttributeMetaData()
	at_sce.type = MpcAttributeType.QuantityScalar
	at_sce.name = 'sce'
	at_sce.group = 'Non-linear'
	at_sce.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sce')+'<br/>') + 
		html_par('compressive modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AxialSp_Material','AxialSp Material')+'<br/>') +
		html_end()
		)
	at_sce.dimension = u.F/u.L**2
	
	# fty
	at_fty = MpcAttributeMetaData()
	at_fty.type = MpcAttributeType.QuantityScalar
	at_fty.name = 'fty'
	at_fty.group = 'Non-linear'
	at_fty.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fty')+'<br/>') + 
		html_par('yield stress under tension (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AxialSp_Material','AxialSp Material')+'<br/>') +
		html_end()
		)
	at_fty.dimension = u.F/u.L**2
	
	# fcy
	at_fcy = MpcAttributeMetaData()
	at_fcy.type = MpcAttributeType.QuantityScalar
	at_fcy.name = 'fcy'
	at_fcy.group = 'Non-linear'
	at_fcy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fcy')+'<br/>') + 
		html_par('yield stress under compression (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AxialSp_Material','AxialSp Material')+'<br/>') +
		html_end()
		)
	at_fcy.dimension = u.F/u.L**2
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AxialSp_Material','AxialSp Material')+'<br/>') +
		html_end()
		)
	
	# bte
	at_bte = MpcAttributeMetaData()
	at_bte.type = MpcAttributeType.Real
	at_bte.name = 'bte'
	at_bte.group = 'Optional parameters'
	at_bte.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bte')+'<br/>') + 
		html_par('reduction rate for tensile elastic range (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AxialSp_Material','AxialSp Material')+'<br/>') +
		html_end()
		)
	
	# bty
	at_bty = MpcAttributeMetaData()
	at_bty.type = MpcAttributeType.Real
	at_bty.name = 'bty'
	at_bty.group = 'Optional parameters'
	at_bty.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bty')+'<br/>') + 
		html_par('reduction rate for tensile yielding (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AxialSp_Material','AxialSp Material')+'<br/>') +
		html_end()
		)
	
	# bcy
	at_bcy = MpcAttributeMetaData()
	at_bcy.type = MpcAttributeType.Real
	at_bcy.name = 'bcy'
	at_bcy.group = 'Optional parameters'
	at_bcy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bcy')+'<br/>') + 
		html_par('reduction rate for compressive yielding (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AxialSp_Material','AxialSp Material')+'<br/>') +
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
		html_par('target point stress (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/AxialSp_Material','AxialSp Material')+'<br/>') +
		html_end()
		)
	at_fcr.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'AxialSp'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_sce)
	xom.addAttribute(at_fty)
	xom.addAttribute(at_fcy)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_bte)
	xom.addAttribute(at_bty)
	xom.addAttribute(at_bcy)
	xom.addAttribute(at_fcr)
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_bte)
	xom.setVisibilityDependency(at_Optional, at_bty)
	xom.setVisibilityDependency(at_Optional, at_bcy)
	xom.setVisibilityDependency(at_Optional, at_fcr)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial AxialSp $matTag $sce $fty $fcy <$bte $bty $bcy $fcr>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	sce_at = xobj.getAttribute('sce')
	if(sce_at is None):
		raise Exception('Error: cannot find "sce" attribute')
	sce = sce_at.quantityScalar
	
	fty_at = xobj.getAttribute('fty')
	if(fty_at is None):
		raise Exception('Error: cannot find "fty" attribute')
	fty = fty_at.quantityScalar
	
	fcy_at = xobj.getAttribute('fcy')
	if(fcy_at is None):
		raise Exception('Error: cannot find "fcy" attribute')
	fcy = fcy_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		bte_at = xobj.getAttribute('bte')
		if(bte_at is None):
			raise Exception('Error: cannot find "bte" attribute')
		bte = bte_at.real
		
		bty_at = xobj.getAttribute('bty')
		if(bty_at is None):
			raise Exception('Error: cannot find "bty" attribute')
		bty = bty_at.real
		
		bcy_at = xobj.getAttribute('bcy')
		if(bcy_at is None):
			raise Exception('Error: cannot find "bcy" attribute')
		bcy = bcy_at.real
		
		fcr_at = xobj.getAttribute('fcr')
		if(fcr_at is None):
			raise Exception('Error: cannot find "fcr" attribute')
		fcr = fcr_at.quantityScalar
		
		sopt += '{} {} {} {}'.format(bte, bty, bcy, fcr.value)
	
	
	str_tcl = '{}uniaxialMaterial AxialSp {} {} {} {} {}\n'.format(pinfo.indent, tag, sce.value, fty.value, fcy.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)