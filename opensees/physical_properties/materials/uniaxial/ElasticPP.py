# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Elasticity'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('Tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Material','ElasticPP Material')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# epsyP
	at_epsyP = MpcAttributeMetaData()
	at_epsyP.type = MpcAttributeType.Real
	at_epsyP.name = 'epsyP'
	at_epsyP.group = 'Non-linear'
	at_epsyP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsyP')+'<br/>') + 
		html_par('Strain or deformation at which material reaches plastic state in tension') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Material','ElasticPP Material')+'<br/>') +
		html_end()
		)
	
	#Optional parameters
	#Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('Strain or deformation at which material reaches plastic state in compression.(optional, default is tension value)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Material','ElasticPP Material')+'<br/>') +
		html_end()
		)
	
	# epsyN
	at_epsyN = MpcAttributeMetaData()
	at_epsyN.type = MpcAttributeType.Real
	at_epsyN.name = 'epsyN'
	at_epsyN.group = 'Optional parameters'
	at_epsyN.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsyN')+'<br/>') + 
		html_par('Strain or deformation at which material reaches plastic state in compression.(optional, default is tension value)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Material','ElasticPP Material')+'<br/>') +
		html_end()
		)
	
	# eps0
	at_eps0 = MpcAttributeMetaData()
	at_eps0.type = MpcAttributeType.Real
	at_eps0.name = 'eps0'
	at_eps0.group = 'Optional parameters'
	at_eps0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eps0')+'<br/>') + 
		html_par('Initial strain (optional, default: zero)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic-Perfectly_Plastic_Material','ElasticPP Material')+'<br/>') +
		html_end()
		)
	at_eps0.setDefault(0.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ElasticPP'
	xom.Xgroup = 'Some Standard Uniaxial Materials'
	xom.addAttribute(at_E)
	xom.addAttribute(at_epsyP)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_epsyN)
	xom.addAttribute(at_eps0)
	
	# use_Optional-dep
	xom.setVisibilityDependency(at_Optional, at_epsyN)
	xom.setVisibilityDependency(at_Optional, at_eps0)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ElasticPP $matTag $E $epsyP <$epsyN $eps0>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar
	
	epsyP_at = xobj.getAttribute('epsyP')
	if(epsyP_at is None):
		raise Exception('Error: cannot find "epsyP" attribute')
	epsyP = epsyP_at.real
	
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		epsyN_at = xobj.getAttribute('epsyN')
		if(epsyN_at is None):
			raise Exception('Error: cannot find "epsyN" attribute')
		epsyN = epsyN_at.real
		
		eps0_at = xobj.getAttribute('eps0')
		if(eps0_at is None):
			raise Exception('Error: cannot find "eps0" attribute')
		eps0 = eps0_at.real
		
		sopt += '{} {}'.format(epsyN, eps0)
	
	
	str_tcl = '{}uniaxialMaterial ElasticPP {} {} {} {}\n'.format(pinfo.indent, tag, E.value, epsyP, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)