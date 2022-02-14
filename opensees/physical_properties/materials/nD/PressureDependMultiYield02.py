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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
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
		html_par('(Gr)') +
		html_par('Reference low-strain shear modulus, specified at a reference mean effective confining pressure refPress of p\'r (see below).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_refShearModul.dimension = u.F/u.L**2
	
	# refBulkModul
	at_refBulkModul = MpcAttributeMetaData()
	at_refBulkModul.type = MpcAttributeType.QuantityScalar
	at_refBulkModul.name = 'refBulkModul'
	at_refBulkModul.group = 'Non-linear'
	at_refBulkModul.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('refBulkModul')+'<br/>') + 
		html_par('(Br)') +
		html_par('Reference bulk modulus, specified at a reference mean effective confining pressure refPress of p\'r (see below).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_refBulkModul.dimension = u.F/u.L**2
	
	# frictionAng
	at_frictionAng = MpcAttributeMetaData()
	at_frictionAng.type = MpcAttributeType.Real
	at_frictionAng.name = 'frictionAng'
	at_frictionAng.group = 'Non-linear'
	at_frictionAng.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('frictionAng')+'<br/>') + 
		html_par('(Φ)') +
		html_par('Friction angle at peak shear strength, in degrees.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# peakShearStra
	at_peakShearStra = MpcAttributeMetaData()
	at_peakShearStra.type = MpcAttributeType.Real
	at_peakShearStra.name = 'peakShearStra'
	at_peakShearStra.group = 'Non-linear'
	at_peakShearStra.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('peakShearStra')+'<br/>') + 
		html_par('(γmax)') +
		html_par('An octahedral shear strain at which the maximum shear strength is reached, specified at a reference mean effective confining pressure refPress of p\'r (see below).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# refPress
	at_refPress = MpcAttributeMetaData()
	at_refPress.type = MpcAttributeType.QuantityScalar
	at_refPress.name = 'refPress'
	at_refPress.group = 'Non-linear'
	at_refPress.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('refPress')+'<br/>') + 
		html_par('(p’r)') +
		html_par('Reference mean effective confining pressure at which Gr, Br, and ฮณmax are defined.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_refPress.dimension = u.F/u.L**2
	
	# pressDependCoe
	at_pressDependCoe = MpcAttributeMetaData()
	at_pressDependCoe.type = MpcAttributeType.Real
	at_pressDependCoe.name = 'pressDependCoe'
	at_pressDependCoe.group = 'Non-linear'
	at_pressDependCoe.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pressDependCoe')+'<br/>') + 
		html_par('(d)') +
		html_par('A positive constant defining variations of G and B as a function of instantaneous effective confinement p\'') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# PTAng
	at_PTAng = MpcAttributeMetaData()
	at_PTAng.type = MpcAttributeType.Real
	at_PTAng.name = 'PTAng'
	at_PTAng.group = 'Non-linear'
	at_PTAng.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('PTAng')+'<br/>') + 
		html_par('(ΦPT)') +
		html_par('Phase transformation angle, in degrees.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# contrac1
	at_contrac1 = MpcAttributeMetaData()
	at_contrac1.type = MpcAttributeType.Real
	at_contrac1.name = 'contrac1'
	at_contrac1.group = 'Non-linear'
	at_contrac1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('contrac1')+'<br/>') + 
		html_par('A non-negative constant defining the rate of shear-induced volume decrease (contraction) or pore pressure buildup. A larger value corresponds to faster contraction rate.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# contrac2
	at_contrac2 = MpcAttributeMetaData()
	at_contrac2.type = MpcAttributeType.Real
	at_contrac2.name = 'contrac2'
	at_contrac2.group = 'Optional parameters'
	at_contrac2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('contrac2')+'<br/>') + 
		html_par('A non-negative constant reflecting dilation history on contraction tendency.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_contrac2.setDefault(5)
	
	# contrac3
	at_contrac3 = MpcAttributeMetaData()
	at_contrac3.type = MpcAttributeType.Real
	at_contrac3.name = 'contrac3'
	at_contrac3.group = 'Non-linear'
	at_contrac3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('contrac3')+'<br/>') + 
		html_par('A non-negative constant reflecting Kσ effect.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# dilat1
	at_dilat1 = MpcAttributeMetaData()
	at_dilat1.type = MpcAttributeType.Real
	at_dilat1.name = 'dilat1'
	at_dilat1.group = 'Non-linear'
	at_dilat1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dilat1')+'<br/>') + 
		html_par('Non-negative constant defining the rate of shear-induced volume increase (dilation). Larger values correspond to stronger dilation rate.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# dilat2
	at_dilat2 = MpcAttributeMetaData()
	at_dilat2.type = MpcAttributeType.Real
	at_dilat2.name = 'dilat2'
	at_dilat2.group = 'Optional parameters'
	at_dilat2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dilat2')+'<br/>') + 
		html_par('Non-negative constant defining the rate of shear-induced volume increase (dilation). Larger values correspond to stronger dilation rate.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_dilat2.setDefault(3)
	
	# dilat3
	at_dilat3 = MpcAttributeMetaData()
	at_dilat3.type = MpcAttributeType.Real
	at_dilat3.name = 'dilat3'
	at_dilat3.group = 'Non-linear'
	at_dilat3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dilat3')+'<br/>') + 
		html_par('A non-negative constant reflecting Kσ effect.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# liquefac1
	at_liquefac1 = MpcAttributeMetaData()
	at_liquefac1.type = MpcAttributeType.Real
	at_liquefac1.name = 'liquefac1'
	at_liquefac1.group = 'Optional parameters'
	at_liquefac1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('liquefac1')+'<br/>') + 
		html_par('Damage parameter to define accumulated permanent shear strain as a function of dilation history. (Redefined and different from PressureDependMultiYield material).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_liquefac1.setDefault(1)
	
	# liquefac2
	at_liquefac2 = MpcAttributeMetaData()
	at_liquefac2.type = MpcAttributeType.Real
	at_liquefac2.name = 'liquefac2'
	at_liquefac2.group = 'Optional parameters'
	at_liquefac2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('liquefac2')+'<br/>') + 
		html_par('Damage parameter to define biased accumulation of permanent shear strain as a function of load reversal history. (Redefined and different from PressureDependMultiYield material).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_liquefac2.setDefault(0)
	
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_automatic_surface.editable = False
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# noYieldSurf
	at_noYieldSurf = MpcAttributeMetaData()
	at_noYieldSurf.type = MpcAttributeType.Integer
	at_noYieldSurf.name = 'noYieldSurf'
	at_noYieldSurf.group = 'Optional parameters'
	at_noYieldSurf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('noYieldSurf')+'<br/>') + 
		html_par('Number of yield surfaces, optional (must be less than 40, default is 20). The surfaces are generated based on the hyperbolic relation defined in Note 2 below.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	
	# e
	at_e = MpcAttributeMetaData()
	at_e.type = MpcAttributeType.Real
	at_e.name = 'e'
	at_e.group = 'Optional parameters'
	at_e.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('e')+'<br/>') + 
		html_par('Initial void ratio, optional (default is 0.6).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_e.setDefault(0.6)
	
	# cs1
	at_cs1 = MpcAttributeMetaData()
	at_cs1.type = MpcAttributeType.Real
	at_cs1.name = 'cs1'
	at_cs1.group = 'Optional parameters'
	at_cs1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cs1')+'<br/>') + 
		html_par('Parameters defining a straight critical-state line ec in e-p\' space. (default values: cs1=0.9)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_cs1.setDefault(0.9)
	
	# cs2
	at_cs2 = MpcAttributeMetaData()
	at_cs2.type = MpcAttributeType.Real
	at_cs2.name = 'cs2'
	at_cs2.group = 'Optional parameters'
	at_cs2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cs2')+'<br/>') + 
		html_par('Parameters defining a straight critical-state line ec in e-p\' space. (default values: cs2=0.02)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_cs2.setDefault(0.02)
	
	# cs3
	at_cs3 = MpcAttributeMetaData()
	at_cs3.type = MpcAttributeType.Real
	at_cs3.name = 'cs3'
	at_cs3.group = 'Optional parameters'
	at_cs3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cs3')+'<br/>') + 
		html_par('Parameters defining a straight critical-state line ec in e-p\' space. (default values: cs3=0.7)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_cs3.setDefault(0.7)
	
	# pa
	at_pa = MpcAttributeMetaData()
	at_pa.type = MpcAttributeType.QuantityScalar
	at_pa.name = 'pa'
	at_pa.group = 'Optional parameters'
	at_pa.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pa')+'<br/>') + 
		html_par('Parameters defining a straight critical-state line ec in e-p\' space. (default values: pa =101 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_pa.setDefault(101)#kPa
	at_pa.dimension = u.F/u.L**2
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.QuantityScalar
	at_c.name = 'c'
	at_c.group = 'Optional parameters'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') + 
		html_par('Numerical constant (default value = 0.1 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_c.setDefault(0.1)#kPa
	at_c.dimension = u.F/u.L**2
	
	# Hv
	at_Hv = MpcAttributeMetaData()
	at_Hv.type = MpcAttributeType.Real
	at_Hv.name = 'Hv'
	at_Hv.group = 'Optional parameters'
	at_Hv.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Hv')+'<br/>') + 
		html_par('default value: 0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_Hv.setDefault(0)
	
	# Pv
	at_Pv = MpcAttributeMetaData()
	at_Pv.type = MpcAttributeType.Real
	at_Pv.name = 'Pv'
	at_Pv.group = 'Optional parameters'
	at_Pv.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Pv')+'<br/>') + 
		html_par('default value: 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PressureDependMultiYield02_Material','PressureDependMultiYield02 Material')+'<br/>') +
		html_end()
		)
	at_Pv.setDefault(1.0)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'PressureDependMultiYield02'
	xom.Xgroup = 'UC San Diego soil models'
	xom.addAttribute(at_nd)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_refShearModul)
	xom.addAttribute(at_refBulkModul)
	xom.addAttribute(at_frictionAng)
	xom.addAttribute(at_peakShearStra)
	xom.addAttribute(at_refPress)
	xom.addAttribute(at_pressDependCoe)
	xom.addAttribute(at_PTAng)
	xom.addAttribute(at_contrac1)
	xom.addAttribute(at_contrac2)
	xom.addAttribute(at_contrac3)
	xom.addAttribute(at_dilat1)
	xom.addAttribute(at_dilat2)
	xom.addAttribute(at_dilat3)
	xom.addAttribute(at_liquefac1)
	xom.addAttribute(at_liquefac2)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_surface)
	xom.addAttribute(at_user_surfaces)
	xom.addAttribute(at_automatic_surface)
	xom.addAttribute(at_noYieldSurf)
	xom.addAttribute(at_r_Gs)
	xom.addAttribute(at_e)
	xom.addAttribute(at_cs1)
	xom.addAttribute(at_cs2)
	xom.addAttribute(at_cs3)
	xom.addAttribute(at_pa)
	xom.addAttribute(at_c)
	xom.addAttribute(at_Hv)
	xom.addAttribute(at_Pv)
	
	# use_Optional-dep
	xom.setVisibilityDependency(at_Optional, at_noYieldSurf)
	xom.setVisibilityDependency(at_Optional, at_surface)
	xom.setVisibilityDependency(at_Optional, at_r_Gs)
	xom.setVisibilityDependency(at_Optional, at_contrac2)
	xom.setVisibilityDependency(at_Optional, at_dilat2)
	xom.setVisibilityDependency(at_Optional, at_liquefac1)
	xom.setVisibilityDependency(at_Optional, at_liquefac2)
	xom.setVisibilityDependency(at_Optional, at_e)
	xom.setVisibilityDependency(at_Optional, at_cs1)
	xom.setVisibilityDependency(at_Optional, at_cs2)
	xom.setVisibilityDependency(at_Optional, at_cs3)
	xom.setVisibilityDependency(at_Optional, at_pa)
	xom.setVisibilityDependency(at_Optional, at_c)
	xom.setVisibilityDependency(at_Optional, at_Hv)
	xom.setVisibilityDependency(at_Optional, at_Pv)
	
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
	
	#nDMaterial PressureDependMultiYield02 $tag $nd $rho $refShearModul $refBulkModul
	# $frictionAng $peakShearStra $refPress $pressDependCoe $PTAng $contrac1 $contrac3
	# $dilat1 $dilat3 <$noYieldSurf=20 <$r1 $Gs1 …> $contrac2=5. $dilat2=3. $liquefac1=1.
	# $liquefac2=0. $e=0.6 $cs1=0.9 $cs2=0.02 $cs3=0.7 $pa=101 <$c=0.1>>
	'''
	"nd", "rho", "refShearModul", "refBulkModul", "frictionAng", "peakShearStra", "refPress", "pressDependCoe",
	"phaseTransformAngle", "contractionParam1", "contractionParam3","dilationParam1","dilationParam3",
	"numberOfYieldSurf (=20)", "contractionParam2=5.0", "dilationParam2=3.0", "liquefactionParam1=1.0",
	"liquefactionParam2=0.0", "e (=0.6)", "volLimit1 (=0.9)", "volLimit2 (=0.02)", "volLimit3 (=0.7)",
	"Atmospheric pressure (=101)", "cohesi (=.1)", "Hv (=0)", "Pv (=1.)"
	'''
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
	
	frictionAng_at = xobj.getAttribute('frictionAng')
	if(frictionAng_at is None):
		raise Exception('Error: cannot find "frictionAng" attribute')
	frictionAng = frictionAng_at.real
	
	peakShearStra_at = xobj.getAttribute('peakShearStra')
	if(peakShearStra_at is None):
		raise Exception('Error: cannot find "peakShearStra" attribute')
	peakShearStra = peakShearStra_at.real
	
	refPress_at = xobj.getAttribute('refPress')
	if(refPress_at is None):
		raise Exception('Error: cannot find "refPress" attribute')
	refPress = refPress_at.quantityScalar
	
	pressDependCoe_at = xobj.getAttribute('pressDependCoe')
	if(pressDependCoe_at is None):
		raise Exception('Error: cannot find "pressDependCoe" attribute')
	pressDependCoe = pressDependCoe_at.real
	
	PTAng_at = xobj.getAttribute('PTAng')
	if(PTAng_at is None):
		raise Exception('Error: cannot find "PTAng" attribute')
	PTAng = PTAng_at.real
	
	contrac1_at = xobj.getAttribute('contrac1')
	if(contrac1_at is None):
		raise Exception('Error: cannot find "contrac1" attribute')
	contrac1 = contrac1_at.real
	
	contrac3_at = xobj.getAttribute('contrac3')
	if(contrac3_at is None):
		raise Exception('Error: cannot find "contrac3" attribute')
	contrac3 = contrac3_at.real
	
	dilat1_at = xobj.getAttribute('dilat1')
	if(dilat1_at is None):
		raise Exception('Error: cannot find "dilat1" attribute')
	dilat1 = dilat1_at.real
	
	dilat3_at = xobj.getAttribute('dilat3')
	if(dilat3_at is None):
		raise Exception('Error: cannot find "dilat3" attribute')
	dilat3 = dilat3_at.real
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		automatic_surface_at = xobj.getAttribute('Automatic surface generation')
		if(automatic_surface_at is None):
			raise Exception('Error: cannot find "Automatic surface generation" attribute')
		automatic_surface = automatic_surface_at.boolean
		if automatic_surface:
			noYieldSurf_at = xobj.getAttribute('noYieldSurf')
			if(noYieldSurf_at is None):
				raise Exception('Error: cannot find "noYieldSurf" attribute')
			noYieldSurf = noYieldSurf_at.integer
			
			sopt += '{}'.format(noYieldSurf)
		
		else:
			r_Gs_at = xobj.getAttribute('r_Gs')
			if(r_Gs_at is None):
				raise Exception('Error: cannot find "r_Gs" attribute')
			r_Gs = r_Gs_at.quantityMatrix
			
			if(r_Gs.cols < 2):
				raise Exceptions('The number of columns must be 2')
			
			sopt += '-{}'.format(r_Gs.rows)
			
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
		
		contrac2_at = xobj.getAttribute('contrac2')
		if(contrac2_at is None):
			raise Exception('Error: cannot find "contrac2" attribute')
		contrac2 = contrac2_at.real
		
		dilat2_at = xobj.getAttribute('dilat2')
		if(dilat2_at is None):
			raise Exception('Error: cannot find "dilat2" attribute')
		dilat2 = dilat2_at.real
		
		liquefac1_at = xobj.getAttribute('liquefac1')
		if(liquefac1_at is None):
			raise Exception('Error: cannot find "liquefac1" attribute')
		liquefac1 = liquefac1_at.real
		
		liquefac2_at = xobj.getAttribute('liquefac2')
		if(liquefac2_at is None):
			raise Exception('Error: cannot find "liquefac2" attribute')
		liquefac2 = liquefac2_at.real
		
		e_at = xobj.getAttribute('e')
		if(e_at is None):
			raise Exception('Error: cannot find "e" attribute')
		e = e_at.real
		
		cs1_at = xobj.getAttribute('cs1')
		if(cs1_at is None):
			raise Exception('Error: cannot find "cs1" attribute')
		cs1 = cs1_at.real
		
		cs2_at = xobj.getAttribute('cs2')
		if(cs2_at is None):
			raise Exception('Error: cannot find "cs2" attribute')
		cs2 = cs2_at.real
		
		cs3_at = xobj.getAttribute('cs3')
		if(cs3_at is None):
			raise Exception('Error: cannot find "cs3" attribute')
		cs3 = cs3_at.real
		
		pa_at = xobj.getAttribute('pa')
		if(pa_at is None):
			raise Exception('Error: cannot find "pa" attribute')
		pa = pa_at.quantityScalar
		
		c_at = xobj.getAttribute('c')
		if(c_at is None):
			raise Exception('Error: cannot find "c" attribute')
		c = c_at.quantityScalar
		
		Hv_at = xobj.getAttribute('Hv')
		if(Hv_at is None):
			raise Exception('Error: cannot find "Hv" attribute')
		Hv = Hv_at.real
		
		Pv_at = xobj.getAttribute('Pv')
		if(Pv_at is None):
			raise Exception('Error: cannot find "Pv" attribute')
		Pv = Pv_at.real
		
		sopt += '\\\n{}{} {} {} {} {} {} {} {} {} {} {} {}'.format(pinfo.indent, contrac2, dilat2, liquefac1, liquefac2, e, cs1, cs2, cs3, pa.value, c.value, Hv, Pv)
	
	str_tcl = '{}nDMaterial PressureDependMultiYield02 {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, ndm, rho.value, refShearModul.value, refBulkModul.value, frictionAng, peakShearStra,
			refPress.value, pressDependCoe, PTAng, contrac1, contrac3, dilat1, dilat3, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)