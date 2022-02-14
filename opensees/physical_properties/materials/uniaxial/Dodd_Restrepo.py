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
		html_par('Yield strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DoddRestrepo','Dodd_Restrepo Material')+'<br/>') +
		html_end()
		)
	at_Fy.dimension = u.F/u.L**2
	
	# Fsu
	at_Fsu = MpcAttributeMetaData()
	at_Fsu.type = MpcAttributeType.QuantityScalar
	at_Fsu.name = 'Fsu'
	at_Fsu.group = 'Non-linear'
	at_Fsu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fsu')+'<br/>') + 
		html_par('Ultimate tensile strength (UTS)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DoddRestrepo','Dodd_Restrepo Material')+'<br/>') +
		html_end()
		)
	at_Fsu.dimension = u.F/u.L**2
	
	# ESH
	at_ESH = MpcAttributeMetaData()
	at_ESH.type = MpcAttributeType.Real
	at_ESH.name = 'ESH'
	at_ESH.group = 'Non-linear'
	at_ESH.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ESH')+'<br/>') + 
		html_par('Tensile strain at initiation of strain hardening') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DoddRestrepo','Dodd_Restrepo Material')+'<br/>') +
		html_end()
		)

	# ESU
	at_ESU = MpcAttributeMetaData()
	at_ESU.type = MpcAttributeType.Real
	at_ESU.name = 'ESU'
	at_ESU.group = 'Non-linear'
	at_ESU.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ESU')+'<br/>') + 
		html_par('Tensile strain at the UTS') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DoddRestrepo','Dodd_Restrepo Material')+'<br/>') +
		html_end()
		)
	
	# Youngs
	at_Youngs = MpcAttributeMetaData()
	at_Youngs.type = MpcAttributeType.QuantityScalar
	at_Youngs.name = 'Youngs'
	at_Youngs.group = 'Non-linear'
	at_Youngs.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Youngs')+'<br/>') + 
		html_par('Modulus of elasticity') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DoddRestrepo','Dodd_Restrepo Material')+'<br/>') +
		html_end()
		)
	at_Youngs.dimension = u.F/u.L**2

	# ESHI
	at_ESHI = MpcAttributeMetaData()
	at_ESHI.type = MpcAttributeType.Real
	at_ESHI.name = 'ESHI'
	at_ESHI.group = 'Non-linear'
	at_ESHI.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ESHI')+'<br/>') + 
		html_par('Tensile strain for a point on strain hardening curve, recommended range of values for ESHI: [ (ESU + 5*ESH)/6, (ESU + 3*ESH)/4]') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DoddRestrepo','Dodd_Restrepo Material')+'<br/>') +
		html_end()
		)
		
	# FSHI
	at_FSHI = MpcAttributeMetaData()
	at_FSHI.type = MpcAttributeType.QuantityScalar
	at_FSHI.name = 'FSHI'
	at_FSHI.group = 'Non-linear'
	at_FSHI.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('FSHI')+'<br/>') + 
		html_par('ensile stress at point on strain hardening curve corresponding to ESHI') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DoddRestrepo','Dodd_Restrepo Material')+'<br/>') +
		html_end()
		)
	at_FSHI.dimension = u.F/u.L**2
	
	# use_OmegaFac
	at_use_OmegaFac = MpcAttributeMetaData()
	at_use_OmegaFac.type = MpcAttributeType.Boolean
	at_use_OmegaFac.name = 'use_OmegaFac'
	at_use_OmegaFac.group = 'Non-linear'
	at_use_OmegaFac.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_OmegaFac')+'<br/>') + 
		html_par('Roundedness factor for Bauschinger curve in cycle reversals from the strain hardening curve. Range: [0.75, 1.15]. Largest value tends to near a bilinear Bauschinger curve. Default = 1.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DoddRestrepo','Dodd_Restrepo Material')+'<br/>') +
		html_end()
		)
	
	# OmegaFac
	at_OmegaFac = MpcAttributeMetaData()
	at_OmegaFac.type = MpcAttributeType.Real
	at_OmegaFac.name = 'OmegaFac'
	at_OmegaFac.group = 'Optional parameters'
	at_OmegaFac.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OmegaFac')+'<br/>') + 
		html_par('Roundedness factor for Bauschinger curve in cycle reversals from the strain hardening curve. Range: [0.75, 1.15]. Largest value tends to near a bilinear Bauschinger curve. Default = 1.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DoddRestrepo','Dodd_Restrepo Material')+'<br/>') +
		html_end()
		)
	at_OmegaFac.setDefault(1.0)

	xom = MpcXObjectMetaData()
	xom.name = 'Dodd_Restrepo'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_Fsu)
	xom.addAttribute(at_ESH)
	xom.addAttribute(at_ESU)
	xom.addAttribute(at_Youngs)
	xom.addAttribute(at_ESHI)
	xom.addAttribute(at_FSHI)
	xom.addAttribute(at_use_OmegaFac)
	xom.addAttribute(at_OmegaFac)
	
	# OmegaFac-dep
	xom.setVisibilityDependency(at_use_OmegaFac, at_OmegaFac)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Dodd_Restrepo $tag $Fy $Fsu $ESH $ESU $Youngs $ESHI $FSHI <$OmegaFac>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	Fy_at = xobj.getAttribute('Fy')
	if(Fy_at is None):
		raise Exception('Error: cannot find "Fy" attribute')
	Fy = Fy_at.quantityScalar
	
	Fsu_at = xobj.getAttribute('Fsu')
	if(Fsu_at is None):
		raise Exception('Error: cannot find "Fsu" attribute')
	Fsu = Fsu_at.quantityScalar
	
	ESH_at = xobj.getAttribute('ESH')
	if(ESH_at is None):
		raise Exception('Error: cannot find "ESH" attribute')
	ESH = ESH_at.real
	
	ESU_at = xobj.getAttribute('ESU')
	if(ESU_at is None):
		raise Exception('Error: cannot find "ESU" attribute')
	ESU = ESU_at.real
	
	Youngs_at = xobj.getAttribute('Youngs')
	if(Youngs_at is None):
		raise Exception('Error: cannot find "Youngs" attribute')
	Youngs = Youngs_at.quantityScalar
	
	ESHI_at = xobj.getAttribute('ESHI')
	if(ESHI_at is None):
		raise Exception('Error: cannot find "ESHI" attribute')
	ESHI = ESHI_at.real
	
	FSHI_at = xobj.getAttribute('FSHI')
	if(FSHI_at is None):
		raise Exception('Error: cannot find "FSHI" attribute')
	FSHI = FSHI_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	use_OmegaFac_at = xobj.getAttribute('use_OmegaFac')
	if(use_OmegaFac_at is None):
		raise Exception('Error: cannot find "use_OmegaFac" attribute')
	use_OmegaFac = use_OmegaFac_at.boolean
	if use_OmegaFac:
		OmegaFac_at = xobj.getAttribute('OmegaFac')
		if(OmegaFac_at is None):
			raise Exception('Error: cannot find "OmegaFac" attribute')
		OmegaFac = OmegaFac_at.real
		
		sopt += '{}'.format(OmegaFac)
	
	
	str_tcl = '{}uniaxialMaterial Dodd_Restrepo {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, Fy.value, Fsu.value, ESH, ESU, Youngs.value, ESHI, FSHI.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)