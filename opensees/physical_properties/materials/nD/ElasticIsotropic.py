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
		html_par('elastic Modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Isotropic_Material','Elastic Isotropic Material')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# v
	at_v = MpcAttributeMetaData()
	at_v.type = MpcAttributeType.Real
	at_v.name = 'v'
	at_v.group = 'Elasticity'
	at_v.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('v')+'<br/>') + 
		html_par('Poisson\'s ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Isotropic_Material','Elastic Isotropic Material')+'<br/>') +
		html_end()
		)
	
	# use_rho
	at_use_rho = MpcAttributeMetaData()
	at_use_rho.type = MpcAttributeType.Boolean
	at_use_rho.name = 'use_rho'
	at_use_rho.group = 'Optional parameters'
	at_use_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_rho')+'<br/>') + 
		html_par('mass density, optional default = 0.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Isotropic_Material','Elastic Isotropic Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Isotropic_Material','Elastic Isotropic Material')+'<br/>') +
		html_end()
		)
	at_rho.setDefault(0.0)
	#at_rho.dimension = u.M/u.L**3
	
	xom = MpcXObjectMetaData()
	xom.name = 'ElasticIsotropic'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_E)
	xom.addAttribute(at_v)
	xom.addAttribute(at_use_rho)
	xom.addAttribute(at_rho)
	
	# rho-dep
	xom.setVisibilityDependency(at_use_rho, at_rho)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial ElasticIsotropic $matTag $E $v <$rho>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar
	
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
	
	str_tcl = '{}nDMaterial ElasticIsotropic {} {} {}{}\n'.format(pinfo.indent, tag, E.value, v, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)