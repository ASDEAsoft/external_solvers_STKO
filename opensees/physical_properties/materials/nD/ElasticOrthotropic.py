import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Ex
	at_Ex = MpcAttributeMetaData()
	at_Ex.type = MpcAttributeType.QuantityScalar
	at_Ex.name = 'Ex'
	at_Ex.group = 'Elasticity'
	at_Ex.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ex')+'<br/>') + 
		html_par('elastic Modulus in x direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	at_Ex.dimension = u.F/u.L**2
	
	# Ey
	at_Ey = MpcAttributeMetaData()
	at_Ey.type = MpcAttributeType.QuantityScalar
	at_Ey.name = 'Ey'
	at_Ey.group = 'Elasticity'
	at_Ey.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ey')+'<br/>') + 
		html_par('elastic Modulus in y direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	at_Ey.dimension = u.F/u.L**2
	
	# Ez
	at_Ez = MpcAttributeMetaData()
	at_Ez.type = MpcAttributeType.QuantityScalar
	at_Ez.name = 'Ez'
	at_Ez.group = 'Elasticity'
	at_Ez.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ez')+'<br/>') + 
		html_par('elastic Modulus in z direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	at_Ez.dimension = u.F/u.L**2
	
	# vxy
	at_vxy = MpcAttributeMetaData()
	at_vxy.type = MpcAttributeType.Real
	at_vxy.name = 'vxy'
	at_vxy.group = 'Elasticity'
	at_vxy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vxy')+'<br/>') + 
		html_par('Poisson\'s ratio in x direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	
	# vyz
	at_vyz = MpcAttributeMetaData()
	at_vyz.type = MpcAttributeType.Real
	at_vyz.name = 'vyz'
	at_vyz.group = 'Elasticity'
	at_vyz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vyz')+'<br/>') + 
		html_par('Poisson\'s ratio in y direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	
	# vzx
	at_vzx = MpcAttributeMetaData()
	at_vzx.type = MpcAttributeType.Real
	at_vzx.name = 'vzx'
	at_vzx.group = 'Elasticity'
	at_vzx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vzx')+'<br/>') + 
		html_par('Poisson\'s ratio in z direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
		
	# Gxy
	at_Gxy = MpcAttributeMetaData()
	at_Gxy.type = MpcAttributeType.QuantityScalar
	at_Gxy.name = 'Gxy'
	at_Gxy.group = 'Elasticity'
	at_Gxy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Gxy')+'<br/>') + 
		html_par('shear modulus xy') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	at_Gxy.dimension = u.F/u.L**2
	
	# Gyz
	at_Gyz = MpcAttributeMetaData()
	at_Gyz.type = MpcAttributeType.QuantityScalar
	at_Gyz.name = 'Gyz'
	at_Gyz.group = 'Elasticity'
	at_Gyz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Gyz')+'<br/>') + 
		html_par('shear modulus yz ') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	at_Gyz.dimension = u.F/u.L**2
	
	# Gzx
	at_Gzx = MpcAttributeMetaData()
	at_Gzx.type = MpcAttributeType.QuantityScalar
	at_Gzx.name = 'Gzx'
	at_Gzx.group = 'Elasticity'
	at_Gzx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Gz')+'<br/>') + 
		html_par('shear modulus zx') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	at_Gzx.dimension = u.F/u.L**2
	
	# use_rho
	at_use_rho = MpcAttributeMetaData()
	at_use_rho.type = MpcAttributeType.Boolean
	at_use_rho.name = 'use_rho'
	at_use_rho.group = 'Non-linear'
	at_use_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_rho')+'<br/>') + 
		html_par('mass density, optional default = 0.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Option parameters'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('mass density, optional default = 0.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Orthotropic_Material','Elastic Orthotropic Material')+'<br/>') +
		html_end()
		)
	at_rho.setDefault(0.0)
	#at_rho.dimension = u.M/u.L**3
	
	xom = MpcXObjectMetaData()
	xom.name = 'ElasticOrthotropic'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_Ex)
	xom.addAttribute(at_Ey)
	xom.addAttribute(at_Ez)
	xom.addAttribute(at_vxy)
	xom.addAttribute(at_vyz)
	xom.addAttribute(at_vzx)
	xom.addAttribute(at_Gxy)
	xom.addAttribute(at_Gyz)
	xom.addAttribute(at_Gzx)
	xom.addAttribute(at_use_rho)
	xom.addAttribute(at_rho)
	
	# use_rho-dep
	xom.setVisibilityDependency(at_use_rho, at_rho)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial ElasticOrthotropic $matTag $Ex $Ey $Ez $vxy $vyz $vzx $Gxy $Gyz $Gzx <$rho>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	Ex_at = xobj.getAttribute('Ex')
	if(Ex_at is None):
		raise Exception('Error: cannot find "Ex" attribute')
	Ex = Ex_at.quantityScalar
	
	Ey_at = xobj.getAttribute('Ey')
	if(Ey_at is None):
		raise Exception('Error: cannot find "Ey" attribute')
	Ey = Ey_at.quantityScalar
	
	Ez_at = xobj.getAttribute('Ez')
	if(Ez_at is None):
		raise Exception('Error: cannot find "Ez" attribute')
	Ez = Ez_at.quantityScalar
	
	vxy_at = xobj.getAttribute('vxy')
	if(vxy_at is None):
		raise Exception('Error: cannot find "vxy" attribute')
	vxy = vxy_at.real
	
	vyz_at = xobj.getAttribute('vyz')
	if(vyz_at is None):
		raise Exception('Error: cannot find "vyz" attribute')
	vyz = vyz_at.real
	
	vzx_at = xobj.getAttribute('vzx')
	if(vzx_at is None):
		raise Exception('Error: cannot find "vzx" attribute')
	vzx = vzx_at.real
	
	Gxy_at = xobj.getAttribute('Gxy')
	if(Gxy_at is None):
		raise Exception('Error: cannot find "Gxy" attribute')
	Gxy = Gxy_at.quantityScalar
	
	Gyz_at = xobj.getAttribute('Gyz')
	if(Gyz_at is None):
		raise Exception('Error: cannot find "Gyz" attribute')
	Gyz = Gyz_at.quantityScalar
	
	Gzx_at = xobj.getAttribute('Gzx')
	if(Gzx_at is None):
		raise Exception('Error: cannot find "Gzx" attribute')
	Gzx = Gzx_at.quantityScalar
	
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
		
		sopt += '{}'.format(rho.value)
	
	str_tcl = '{}nDMaterial ElasticOrthotropic {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, Ex.value, Ey.value, Ez.value, vxy, vyz, vzx, Gxy.value, Gyz.value, Gzx.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)