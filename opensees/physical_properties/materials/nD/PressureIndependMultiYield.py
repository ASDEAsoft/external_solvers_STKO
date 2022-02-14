import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# nd
	at_nd = MpcAttributeMetaData()
	at_nd.type = MpcAttributeType.Integer
	at_nd.name = 'nd'
	at_nd.group = 'Non-linear'
	at_nd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nd')+'<br/>') + 
		html_par('Number of dimensions, 2 for plane-strain, and 3 for 3D analysis.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_nd.sourceType = MpcAttributeSourceType.List
	at_nd.setSourceList([2, 3])
	at_nd.setDefault(2)
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Non-linear'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('Saturated soil mass density.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	#at_rho.dimension = u.M/u.L**3
	
	# refShearModul
	at_refShearModul = MpcAttributeMetaData()
	at_refShearModul.type = MpcAttributeType.QuantityScalar
	at_refShearModul.name = 'refShearModul'
	at_refShearModul.group = 'Non-linear'
	at_refShearModul.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('refShearModul')+'<br/>') + 
		html_par('Reference low-strain shear modulus, specified at a reference mean effective confining pressure refPress of p\'r (see below).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_refShearModul .dimension = u.F/u.L**2
	
	# refBulkModul
	at_refBulkModul = MpcAttributeMetaData()
	at_refBulkModul.type = MpcAttributeType.QuantityScalar
	at_refBulkModul.name = 'refBulkModul'
	at_refBulkModul.group = 'Non-linear'
	at_refBulkModul.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('refBulkModul')+'<br/>') + 
		html_par('Reference bulk modulus, specified at a reference mean effective confining pressure refPress of p\'r (see below).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_refBulkModul.dimension = u.F/u.L**2
	
	# cohesi
	at_cohesi = MpcAttributeMetaData()
	at_cohesi.type = MpcAttributeType.QuantityScalar
	at_cohesi.name = 'cohesi'
	at_cohesi.group = 'Non-linear'
	at_cohesi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cohesi')+'<br/>') + 
		html_par('Apparent cohesion at zero effective confinement.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_cohesi.dimension = u.F/u.L**2
	
	# peakShearStra
	at_peakShearStra = MpcAttributeMetaData()
	at_peakShearStra.type = MpcAttributeType.Real
	at_peakShearStra.name = 'peakShearStra'
	at_peakShearStra.group = 'Non-linear'
	at_peakShearStra.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('peakShearStra')+'<br/>') + 
		html_par('An octahedral shear strain at which the maximum shear strength is reached, specified at a reference mean effective confining pressure refPress of p\'r (see below).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	
	# frictionAng
	at_frictionAng = MpcAttributeMetaData()
	at_frictionAng.type = MpcAttributeType.Real
	at_frictionAng.name = 'frictionAng'
	at_frictionAng.group = 'Optional parameters'
	at_frictionAng.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('frictionAng')+'<br/>') + 
		html_par('Friction angle at peak shear strength in degrees, optional (default is 0.0).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_frictionAng.setDefault(0)
	
	# refPress
	at_refPress = MpcAttributeMetaData()
	at_refPress.type = MpcAttributeType.QuantityScalar
	at_refPress.name = 'refPress'
	at_refPress.group = 'Optional parameters'
	at_refPress.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('refPress')+'<br/>') + 
		html_par('Reference mean effective confining pressure at which Gr, Br, and γmax are defined, optional (default is 100. kPa).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_refPress.setDefault(100)
	at_refPress .dimension = u.F/u.L**2
	
	# pressDependCoe
	at_pressDependCoe = MpcAttributeMetaData()
	at_pressDependCoe.type = MpcAttributeType.Real
	at_pressDependCoe.name = 'pressDependCoe'
	at_pressDependCoe.group = 'Optional parameters'
	at_pressDependCoe.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pressDependCoe')+'<br/>') + 
		html_par('A positive constant defining variations of G and B as a function of instantaneous effective confinement p\'(default is 0.0):') +
		html_par('G = Gr(p\'/p\'r)^d; B = Br(p\'r/p\'r)^d') +
		html_par('If Φ=0, d is reset to 0.0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_pressDependCoe.setDefault(0)
	
	# surface
	# choose beetwen automatic surface or user defined surfaces
	at_surface = MpcAttributeMetaData()
	at_surface.type = MpcAttributeType.String
	at_surface.name = 'surface'
	at_surface.group = 'Optional parameters'
	at_surface.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('surface')+'<br/>') +
		html_par('(Automatic surface generation): At a constant confinement p’, the shear stress τ(octahedral) - shear strain γ (octahedral) nonlinearity is defined by a hyperbolic curve (backbone curve)') +
		html_par('noYieldSurf = 20'+'<br/>') +
		html_par('(User defined surfaces): The user specified friction angle Φ is ignored. Instead, Φ is defined based on the formula in Note 3') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_surface.sourceType = MpcAttributeSourceType.List
	at_surface.setSourceList(['Automatic surface generation', 'User defined surfaces'])
	at_surface.setDefault('Automatic surface generation')
	
	# user_surfaces
	at_user_surfaces = MpcAttributeMetaData()
	at_user_surfaces.type = MpcAttributeType.Boolean
	at_user_surfaces.name = 'User defined surfaces'
	at_user_surfaces.group = 'Non-linear'
	at_user_surfaces.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_user_surfaces.editable = False
	
	# automatic_surface
	at_automatic_surface = MpcAttributeMetaData()
	at_automatic_surface.type = MpcAttributeType.Boolean
	at_automatic_surface.name = 'Automatic surface generation'
	at_automatic_surface.group = 'Non-linear'
	at_automatic_surface.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_automatic_surface.editable = False
	
	# noYieldSurf
	at_noYieldSurf = MpcAttributeMetaData()
	at_noYieldSurf.type = MpcAttributeType.Integer
	at_noYieldSurf.name = 'noYieldSurf'
	at_noYieldSurf.group = 'Optional parameters'
	at_noYieldSurf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('noYieldSurf')+'<br/>') + 
		html_par('Number of yield surfaces, optional (must be less than 40, default is 20). The surfaces are generated based on the hyperbolic relation defined in Note 2 below.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	at_noYieldSurf.setDefault(20)
	
	# r_Gs
	at_r_Gs = MpcAttributeMetaData()
	at_r_Gs.type = MpcAttributeType.QuantityMatrix
	at_r_Gs.name = 'r_Gs'
	at_r_Gs.group = 'Optional parameters'
	at_r_Gs.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('r_Gs')+'<br/>') +
		html_par('you can define yield surfaces directly based on desired shear modulus reduction curve. To do so, provide noYieldSurf pairs of shear strain (γ) and modulus ratio (Gs) values.'+'<br/>') +
		html_par('The number of columns must be 2 and will be considered up to 39 rows') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureIndependMultiYield_Material','PressureIndependMultiYield Material')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'PressureIndependMultiYield'
	xom.Xgroup = 'UC San Diego soil models'
	xom.addAttribute(at_nd)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_refShearModul)
	xom.addAttribute(at_refBulkModul)
	xom.addAttribute(at_cohesi)
	xom.addAttribute(at_peakShearStra)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_frictionAng)
	xom.addAttribute(at_refPress)
	xom.addAttribute(at_pressDependCoe)
	xom.addAttribute(at_surface)
	xom.addAttribute(at_user_surfaces)
	xom.addAttribute(at_automatic_surface)
	xom.addAttribute(at_noYieldSurf)
	xom.addAttribute(at_r_Gs)
	
	
	# use_Optional-dep
	xom.setVisibilityDependency(at_Optional, at_frictionAng)
	xom.setVisibilityDependency(at_Optional, at_refPress)
	xom.setVisibilityDependency(at_Optional, at_pressDependCoe)
	xom.setVisibilityDependency(at_Optional, at_surface)
	xom.setVisibilityDependency(at_Optional, at_noYieldSurf)
	xom.setVisibilityDependency(at_Optional, at_r_Gs)
	
	# user_surfaces-dep
	xom.setVisibilityDependency(at_user_surfaces, at_r_Gs)
	
	# automatic_surface-dep
	xom.setVisibilityDependency(at_automatic_surface, at_noYieldSurf)
	
	
	# auto-exclusive dependencies
	# user_surfaces or automatic_surface
	xom.setBooleanAutoExclusiveDependency(at_surface, at_user_surfaces)
	xom.setBooleanAutoExclusiveDependency(at_surface, at_automatic_surface)
	
	
	return xom

def writeTcl(pinfo):
	
	#nDmaterial PressureIndependMultiYield $tag $nd $rho $refShearModul $refBulkModul $cohesi
	# $peakShearStra <$frictionAng=0. $refPress=100. $pressDependCoe=0. $noYieldSurf=20 <$r1 $Gs1>>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	nd_at = xobj.getAttribute('nd')
	if(nd_at is None):
		raise Exception('Error: cannot find "nd" attribute')
	ndm = nd_at.integer
	
	rho_at = xobj.getAttribute('rho')
	if(rho_at is None):
		raise Exception('Error: cannot find "rho" attribute')
	rho = rho_at.quantityScalar
	
	refShearModul_at = xobj.getAttribute('refShearModul')
	if(refShearModul_at is None):
		raise Exception('Error: cannot find "refShearModul" attribute')
	refShearModul = refShearModul_at.quantityScalar
	
	refBulkModul_at = xobj.getAttribute('refBulkModul')
	if(refBulkModul_at is None):
		raise Exception('Error: cannot find "refBulkModul" attribute')
	refBulkModul = refBulkModul_at.quantityScalar
	
	cohesi_at = xobj.getAttribute('cohesi')
	if(cohesi_at is None):
		raise Exception('Error: cannot find "cohesi" attribute')
	cohesi = cohesi_at.quantityScalar
	
	peakShearStra_at = xobj.getAttribute('peakShearStra')
	if(peakShearStra_at is None):
		raise Exception('Error: cannot find "peakShearStra" attribute')
	peakShearStra = peakShearStra_at.real
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		frictionAng_at = xobj.getAttribute('frictionAng')
		if(frictionAng_at is None):
			raise Exception('Error: cannot find "frictionAng" attribute')
		frictionAng = frictionAng_at.real
		
		refPress_at = xobj.getAttribute('refPress')
		if(refPress_at is None):
			raise Exception('Error: cannot find "refPress" attribute')
		refPress = refPress_at.quantityScalar
		
		pressDependCoe_at = xobj.getAttribute('pressDependCoe')
		if(pressDependCoe_at is None):
			raise Exception('Error: cannot find "pressDependCoe" attribute')
		pressDependCoe = pressDependCoe_at.real
		
		sopt +='{} {} {}'.format(frictionAng, refPress.value, pressDependCoe)
		
		automatic_surface_at = xobj.getAttribute('Automatic surface generation')
		if(automatic_surface_at is None):
			raise Exception('Error: cannot find "Automatic surface generation" attribute')
		automatic_surface = automatic_surface_at.boolean
		if automatic_surface:
			noYieldSurf_at = xobj.getAttribute('noYieldSurf')
			if(noYieldSurf_at is None):
				raise Exception('Error: cannot find "noYieldSurf" attribute')
			noYieldSurf = noYieldSurf_at.integer
			
			sopt += ' {}'.format(noYieldSurf)
		
		else:
			r_Gs_at = xobj.getAttribute('r_Gs')
			if(r_Gs_at is None):
				raise Exception('Error: cannot find "r_Gs" attribute')
			r_Gs = r_Gs_at.quantityMatrix
			
			if(r_Gs.cols < 2):
				raise Exceptions('The number of columns must be 2')
			
			sopt += ' -{}'.format(r_Gs.rows)
			
			i=0			#rows
			while(i<39 and i<r_Gs.rows):
				j=0		#columns
				while(j<2):
					if(j==0):
						sopt+='\\\n\t{}{}'.format(pinfo.indent, r_Gs.valueAt(i,j))
					else:
						sopt+=' {}{}'.format(pinfo.indent, r_Gs.valueAt(i,j))
					j+=1
				i+=1
	
	str_tcl = '{}nDMaterial PressureIndependMultiYield {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, ndm, rho.value, refShearModul.value, refBulkModul.value, cohesi.value, peakShearStra, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)