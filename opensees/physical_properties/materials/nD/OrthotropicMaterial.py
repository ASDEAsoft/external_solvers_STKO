# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# IsotropicMaterialTag
	at_IsotropicMaterialTag = MpcAttributeMetaData()
	at_IsotropicMaterialTag.type = MpcAttributeType.Index
	at_IsotropicMaterialTag.name = 'IsotropicMaterialTag'
	at_IsotropicMaterialTag.group = 'Source'
	at_IsotropicMaterialTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IsotropicMaterialTag')+'<br/>') + 
		html_par('integer tag of previously defined 3d ndIsotropicMaterial material') +
		html_end()
		)
	at_IsotropicMaterialTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_IsotropicMaterialTag.indexSource.addAllowedNamespace('materials.nD')

############################################################# Elasticity ######################################################################################
	# Ex
	at_Ex = MpcAttributeMetaData()
	at_Ex.type = MpcAttributeType.QuantityScalar
	at_Ex.name = 'Ex'
	at_Ex.group = 'Elasticity'
	at_Ex.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ex')+'<br/>') + 
		html_par('elastic Modulus along the x direction') +
		html_end()
		)
		
	# Ey
	at_Ey = MpcAttributeMetaData()
	at_Ey.type = MpcAttributeType.QuantityScalar
	at_Ey.name = 'Ey'
	at_Ey.group = 'Elasticity'
	at_Ey.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ey')+'<br/>') + 
		html_par('elastic Modulus along the y direction') +
		html_end()
		)
		
	# Ez
	at_Ez = MpcAttributeMetaData()
	at_Ez.type = MpcAttributeType.QuantityScalar
	at_Ez.name = 'Ez'
	at_Ez.group = 'Elasticity'
	at_Ez.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ez')+'<br/>') + 
		html_par('elastic Modulus along the z direction') +
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
		html_par('shear Modulus') +
		html_end()
		)
		
	# Gyz
	at_Gyz = MpcAttributeMetaData()
	at_Gyz.type = MpcAttributeType.QuantityScalar
	at_Gyz.name = 'Gyz'
	at_Gyz.group = 'Elasticity'
	at_Gyz.description = (
	html_par(html_begin()) +
		html_par(html_boldtext('Gyz')+'<br/>') +
		html_par('shear Modulus') +
		html_end()
		)
		
	# Gzx
	at_Gzx = MpcAttributeMetaData()
	at_Gzx.type = MpcAttributeType.QuantityScalar
	at_Gzx.name = 'Gzx'
	at_Gzx.group = 'Elasticity'
	at_Gzx.description = (
	html_par(html_begin()) +
		html_par(html_boldtext('Gzx')+'<br/>') +
		html_par('shear Modulus') +
		html_end()
		)
		
	# vxy
	at_vxy = MpcAttributeMetaData()
	at_vxy.type = MpcAttributeType.QuantityScalar
	at_vxy.name = 'vxy'
	at_vxy.group = 'Elasticity'
	at_vxy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vxy')+'<br/>') + 
		html_par('Poisson\'s ratio') +
		html_end()
		)
		
	# vyz
	at_vyz = MpcAttributeMetaData()
	at_vyz.type = MpcAttributeType.QuantityScalar
	at_vyz.name = 'vyz'
	at_vyz.group = 'Elasticity'
	at_vyz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vyz')+'<br/>') + 
		html_par('Poisson\'s ratio') +
		html_end()
		)
		
	# vzx
	at_vzx = MpcAttributeMetaData()
	at_vzx.type = MpcAttributeType.QuantityScalar
	at_vzx.name = 'vzx'
	at_vzx.group = 'Elasticity'
	at_vzx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vzx')+'<br/>') + 
		html_par('Poisson\'s ratio') +
		html_end()
		)

############################################################# Mapping #########################################################################################

    # Asigmaxx
	at_Asigmaxx = MpcAttributeMetaData()
	at_Asigmaxx.type = MpcAttributeType.QuantityScalar
	at_Asigmaxx.name = 'Asigmaxx'
	at_Asigmaxx.group = 'Mapping'
	at_Asigmaxx.description = (
	html_par(html_begin()) +
		html_par(html_boldtext('Asigmaxx')+'<br/>') + 
		html_par('Ratio between the isotropic strength f*x and the orthotropic strength fx') +
		html_end()
		)
		
	# Asigmayy
	at_Asigmayy = MpcAttributeMetaData()
	at_Asigmayy.type = MpcAttributeType.QuantityScalar
	at_Asigmayy.name = 'Asigmayy'
	at_Asigmayy.group = 'Mapping'
	at_Asigmayy.description = (
	html_par(html_begin()) +
		html_par(html_boldtext('Asigmayy')+'<br/>') + 
		html_par('Ratio between the isotropic strength f*y and the orthotropic strength fy') +
		html_end()
		)
		
	# Asigmazz
	at_Asigmazz = MpcAttributeMetaData()
	at_Asigmazz.type = MpcAttributeType.QuantityScalar
	at_Asigmazz.name = 'Asigmazz'
	at_Asigmazz.group = 'Mapping'
	at_Asigmazz.description = (
	html_par(html_begin()) +
		html_par(html_boldtext('Asigmazz')+'<br/>') + 
		html_par('Ratio between the isotropic strength f*z and the orthotropic strength fz') +
		html_end()
		)
	
    # Asigmaxyxy
	at_Asigmaxyxy = MpcAttributeMetaData()
	at_Asigmaxyxy.type = MpcAttributeType.QuantityScalar
	at_Asigmaxyxy.name = 'Asigmaxyxy'
	at_Asigmaxyxy.group = 'Mapping'
	at_Asigmaxyxy.description = (
	html_par(html_begin()) +
		html_par(html_boldtext('Asigmaxyxy')+'<br/>') + 
		html_par('Ratio between the isotropic strength f*xy and the orthotropic strength fxy') +
		html_end()
		)
		
	# Asigmayzyz
	at_Asigmayzyz = MpcAttributeMetaData()
	at_Asigmayzyz.type = MpcAttributeType.QuantityScalar
	at_Asigmayzyz.name = 'Asigmayzyz'
	at_Asigmayzyz.group = 'Mapping'
	at_Asigmayzyz.description = (
	html_par(html_begin()) +
		html_par(html_boldtext('Asigmayzyz')+'<br/>') + 
		html_par('Ratio between the isotropic strength f*yz and the orthotropic strength fyz') +
		html_end()
		)
		
	# Asigmaxzxz
	at_Asigmaxzxz = MpcAttributeMetaData()
	at_Asigmaxzxz.type = MpcAttributeType.QuantityScalar
	at_Asigmaxzxz.name = 'Asigmaxzxz'
	at_Asigmaxzxz.group = 'Mapping'
	at_Asigmaxzxz.description = (
	html_par(html_begin()) +
		html_par(html_boldtext('Asigmaxzxz')+'<br/>') + 
		html_par('Ratio between the isotropic strength f*xz and the orthotropic strength fxz') +
		html_end()
		)
	
############################################################# Misc ############################################################################################
	# surf_t
	at_surf_t = MpcAttributeMetaData()
	at_surf_t.type = MpcAttributeType.String
	at_surf_t.name = 'surf_t'
	at_surf_t.group = 'Misc'
	at_surf_t.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('surf_t')+'<br/>') +
		html_par('Tensile surface: Rankine or Lubliner') +
		html_end()
		)
	at_surf_t.sourceType = MpcAttributeSourceType.List
	at_surf_t.setSourceList(['Lubliner', 'Rankine'])
	at_surf_t.setDefault('Rankine')
	
	# bm
	at_bm = MpcAttributeMetaData()
	at_bm.type = MpcAttributeType.Real
	at_bm.name = 'bm'
	at_bm.group = 'Misc'
	at_bm.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bm')+'<br/>') + 
		html_par('Compressive biaxial strength factor') +
		html_end()
		)
	at_bm.setDefault(1.16)
	
	# m1
	at_m1 = MpcAttributeMetaData()
	at_m1.type = MpcAttributeType.Real
	at_m1.name = 'm1'
	at_m1.group = 'Misc'
	at_m1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m1')+'<br/>') + 
		html_par('Shear-Compression reduction factor in range [0, 1]') +
		html_end()
		)
	at_m1.setDefault(0.16)
	
	# Kc
	at_Kc = MpcAttributeMetaData()
	at_Kc.type = MpcAttributeType.Real
	at_Kc.name = 'Kc'
	at_Kc.group = 'Misc'
	at_Kc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kc')+'<br/>') + 
		html_par('Triaxial-Compression shape factor') +
		html_end()
		)
	at_Kc.setDefault(2.0/3.0)
	
	# eta
	at_eta = MpcAttributeMetaData()
	at_eta.type = MpcAttributeType.Real
	at_eta.name = 'eta'
	at_eta.group = 'Misc'
	at_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eta')+'<br/>') + 
		html_par('Viscosity parameter') +
		html_end()
		)
	at_eta.setDefault(0.0)
	
	# pdf_t
	at_pdf_t = MpcAttributeMetaData()
	at_pdf_t.type = MpcAttributeType.Real
	at_pdf_t.name = 'pdf_t'
	at_pdf_t.group = 'Misc'
	at_pdf_t.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pdf_t')+'<br/>') + 
		html_par('Plastic-Damage factor for tensile response in range [0 (full damage) ... (mixed) ... 1 (full plasticity)]') +
		html_end()
		)
	at_pdf_t.setDefault(0.35)
	
	# pdf_c
	at_pdf_c = MpcAttributeMetaData()
	at_pdf_c.type = MpcAttributeType.Real
	at_pdf_c.name = 'pdf_c'
	at_pdf_c.group = 'Misc'
	at_pdf_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pdf_c')+'<br/>') + 
		html_par('Plastic-Damage factor for compressive response in range [0 (full damage) ... (mixed) ... 1 (full plasticity)]') +
		html_end()
		)
	at_pdf_c.setDefault(0.7)
	
	# implex
	at_implex = MpcAttributeMetaData()
	at_implex.type = MpcAttributeType.String
	at_implex.name = 'implex'
	at_implex.group = 'Misc'
	at_implex.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('implex')+'<br/>') +
		html_par('Integration type: Implicit or IMPL-EX') +
		html_end()
		)
	at_implex.sourceType = MpcAttributeSourceType.List
	at_implex.setSourceList(['Implicit', 'IMPL-EX'])
	at_implex.setDefault('Implicit')
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'OrthotropicMaterial'
	xom.Xgroup = 'ASDEASoftware'
	#source 
	xom.addAttribute(at_IsotropicMaterialTag)
	# Elasticity
	xom.addAttribute(at_Ex)
	xom.addAttribute(at_Ey)
	xom.addAttribute(at_Ez)
	xom.addAttribute(at_Gxy)
	xom.addAttribute(at_Gyz)
	xom.addAttribute(at_Gzx)
	xom.addAttribute(at_vxy)
	xom.addAttribute(at_vyz)
	xom.addAttribute(at_vzx)
	# Mapping
	xom.addAttribute(at_Asigmaxx)
	xom.addAttribute(at_Asigmayy)
	xom.addAttribute(at_Asigmazz)
	xom.addAttribute(at_Asigmaxyxy)
	xom.addAttribute(at_Asigmayzyz)
	xom.addAttribute(at_Asigmaxzxz)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial DamageTC3D $tag $Ex $Ey $Ez $Gxy $Gyz $Gzx $vxy $vyz $vzx $Asigmaxx $Asigmayy $Asigmazz $Asigmaxyxy $Asigmayzyz $Asigmaxzxz $surf_t $bm $m1 $Kc $eta $pdf_t $pdf_c $implex
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
		
	# mandatory parameters
	isotag = geta('IsotropicMaterialTag').index
	Ex = geta('Ex').quantityScalar.value
	Ey = geta('Ey').quantityScalar.value
	Ez = geta('Ez').quantityScalar.value
	Gxy = geta('Gxy').quantityScalar.value
	Gyz = geta('Gyz').quantityScalar.value
	Gzx = geta('Gzx').quantityScalar.value
	vxy = geta('vxy').quantityScalar.value
	vyz = geta('vyz').quantityScalar.value
	vzx = geta('vzx').quantityScalar.value
	Asigmaxx = geta('Asigmaxx').quantityScalar.value
	Asigmayy = geta('Asigmayy').quantityScalar.value
	Asigmazz = geta('Asigmazz').quantityScalar.value
	Asigmaxyxy = geta('Asigmaxyxy').quantityScalar.value
	Asigmayzyz = geta('Asigmayzyz').quantityScalar.value
	Asigmaxzxz = geta('Asigmaxzxz').quantityScalar.value
	
	
	
	
	
	# TODO: check parameters...	
	str_tcl = '{}nDMaterial Orthotropic {} {}   {} {} {} {} {} {} {} {} {}   {} {} {} {} {} {}\n'.format(
		pinfo.indent, tag, isotag,
		Ex, Ey, Ez, Gxy, Gyz, Gzx, vxy, vyz, vzx, Asigmaxx, Asigmayy, Asigmazz, Asigmaxyxy, Asigmayzyz, Asigmaxzxz
		)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
	