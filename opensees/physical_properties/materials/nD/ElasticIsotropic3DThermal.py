import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# E0
	at_E0 = MpcAttributeMetaData()
	at_E0.type = MpcAttributeType.QuantityScalar
	at_E0.name = 'E0'
	at_E0.group = 'Elasticity'
	at_E0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E0')+'<br/>') + 
		html_par('elastic Modulus') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','Elastic Isotropic 3D Thermal')+'<br/>') +
		html_end()
		)
	at_E0.dimension = u.F/u.L**2
	
	# v
	at_v = MpcAttributeMetaData()
	at_v.type = MpcAttributeType.Real
	at_v.name = 'v'
	at_v.group = 'Elasticity'
	at_v.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('v')+'<br/>') + 
		html_par('Poisson\'s ratio') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','Elastic Isotropic 3D Thermal')+'<br/>') +
		html_end()
		)
	
	# use_rho
	at_use_rho = MpcAttributeMetaData()
	at_use_rho.type = MpcAttributeType.Boolean
	at_use_rho.name = 'use_rho'
	at_use_rho.group = 'Non-linear'
	at_use_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_rho')+'<br/>') + 
		html_par('mass density, optional default = 0.0.') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','Elastic Isotropic 3D Thermal')+'<br/>') +
		html_end()
		)
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Optional parameters'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('mass density, optional default = 0.0.') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','Elastic Isotropic 3D Thermal')+'<br/>') +
		html_end()
		)
	at_rho.setDefault(0.0)
	#at_rho.dimension = u.M/u.L**3
	
	#use_alpha
	at_use_alpha = MpcAttributeMetaData()
	at_use_alpha.type = MpcAttributeType.Boolean
	at_use_alpha.name = 'use_alpha'
	at_use_alpha.group = 'Group'
	at_use_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_steelType')+'<br/>') + 
		html_par('to activate "alpha"') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','Elastic Isotropic 3D Thermal')+'<br/>') +
		html_end()
		)
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Optional parameters'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','Elastic Isotropic 3D Thermal')+'<br/>') +
		html_end()
		)
	
	#use_steelType
	at_use_steelType = MpcAttributeMetaData()
	at_use_steelType.type = MpcAttributeType.Boolean
	at_use_steelType.name = 'use_steelType'
	at_use_steelType.group = 'Group'
	at_use_steelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_steelType')+'<br/>') + 
		html_par('to activate "-SteelSoft" or "-ConcreteSoft"') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','Elastic Isotropic 3D Thermal')+'<br/>') +
		html_end()
		)
	
	# steelType
	at_softindex = MpcAttributeMetaData()
	at_softindex.type = MpcAttributeType.String
	at_softindex.name = 'steelType'
	at_softindex.group = 'Optional parameters'
	at_softindex.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('steelType')+'<br/>') + 
		html_par('choose between "-SteelSoft" and "-ConcreteSoft"') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','Elastic Isotropic 3D Thermal')+'<br/>') +
		html_end()
		)
	at_softindex.sourceType = MpcAttributeSourceType.List
	at_softindex.setSourceList(['-SteelSoft', '-ConcreteSoft'])
	at_softindex.setDefault('-SteelSoft')
	
	xom = MpcXObjectMetaData()
	xom.name = 'ElasticIsotropic3DThermal'
	xom.Xgroup = 'Thermal'
	xom.addAttribute(at_E0)
	xom.addAttribute(at_v)
	xom.addAttribute(at_use_rho)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_use_alpha)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_use_steelType)
	xom.addAttribute(at_softindex)
	
	# at_use_alpha-at_alpha
	xom.setVisibilityDependency(at_use_alpha, at_alpha)
	
	# at_use_steelType-at_softindex
	xom.setVisibilityDependency(at_use_steelType, at_softindex)
	
	# rho-dep
	xom.setVisibilityDependency(at_use_rho, at_rho)
	
	return xom

def writeTcl(pinfo):
	
	# nDMaterial ElasticIsotropic $tag $E0 $V <$rho> <$alpha> <-cSoft/-sSoft>
	xobj = pinfo.phys_prop.XObject
	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	E0_at = xobj.getAttribute('E0')
	if(E0_at is None):
		raise Exception('Error: cannot find "E0" attribute')
	E0 = E0_at.quantityScalar
	
	v_at = xobj.getAttribute('v')
	if(v_at is None):
		raise Exception('Error: cannot find "v" attribute')
	v = v_at.real
	
	# optional paramters
	sopt = ''
	
	use_rho_at = xobj.getAttribute('use_rho')
	if(use_rho_at is None):
		raise Exception('Error: cannot find "use_rho" attribute')
	use_rho = use_rho_at.boolean
	if use_rho:
		rho_at = xobj.getAttribute('rho')
		if(rho_at is None):
			raise Exception('Error: cannot find "rho" attribute')
		rho = rho_at.quantityScalar
		
		sopt += ' {}'.format(rho.value)
	
	use_alpha_at = xobj.getAttribute('use_alpha')
	if(use_alpha_at is None):
		raise Exception('Error: cannot find "use_alpha" attribute')
	use_alpha = use_alpha_at.boolean
	if use_alpha:
		alpha_at = xobj.getAttribute('alpha')
		if(alpha_at is None):
			raise Exception('Error: cannot find "alpha" attribute')
		alpha = alpha_at.real
		
		sopt += ' {}'.format(alpha)
	
	use_steelType_at = xobj.getAttribute('use_steelType')
	if(use_steelType_at is None):
		raise Exception('Error: cannot find "use_steelType" attribute')
	use_steelType = use_steelType_at.boolean
	if use_steelType:
		steelType_at = xobj.getAttribute('steelType')
		if(steelType_at is None):
			raise Exception('Error: cannot find "steelType" attribute')
		steelType = steelType_at.string
		
		sopt += ' {}'.format(steelType)
	
	str_tcl = '{}nDMaterial ElasticIsotropic3DThermal {} {} {}{}\n'.format(pinfo.indent, tag, E0.value, v, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)