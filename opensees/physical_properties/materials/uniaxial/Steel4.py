# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# f_y
	at_f_y = MpcAttributeMetaData()
	at_f_y.type = MpcAttributeType.QuantityScalar
	at_f_y.name = 'f_y'
	at_f_y.group = 'Non-linear'
	at_f_y.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('f_y')+'<br/>') + 
		html_par('yield strength (assumed identical in tension and compression)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	at_f_y.dimension = u.F/u.L**2
	
	# E_0c
	at_E_0c = MpcAttributeMetaData()
	at_E_0c.type = MpcAttributeType.QuantityScalar
	at_E_0c.name = 'E_0c'
	at_E_0c.group = 'Elasticity'
	at_E_0c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E_0c')+'<br/>') + 
		html_par('initial stiffness (Young\'s modulus)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	at_E_0c.dimension = u.F/u.L**2
	
	#Optional parameters
	# -kin
	at_kin = MpcAttributeMetaData()
	at_kin.type = MpcAttributeType.Boolean
	at_kin.name = '-kin'
	at_kin.group = 'Optional parameters'
	at_kin.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-kin')+'<br/>') + 
		html_par('apply kinematic hardening)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# -iso
	at_iso = MpcAttributeMetaData()
	at_iso.type = MpcAttributeType.Boolean
	at_iso.name = '-iso'
	at_iso.group = 'Optional parameters'
	at_iso.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-iso')+'<br/>') + 
		html_par('apply isotropic hardening)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# -ult
	at_ult = MpcAttributeMetaData()
	at_ult.type = MpcAttributeType.Boolean
	at_ult.name = '-ult'
	at_ult.group = 'Optional parameters'
	at_ult.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-ult')+'<br/>') + 
		html_par('apply an ultimate strength limit)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# -asym
	at_asym = MpcAttributeMetaData()
	at_asym.type = MpcAttributeType.Boolean
	at_asym.name = '-asym'
	at_asym.group = 'Optional parameters'
	at_asym.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-asym')+'<br/>') + 
		html_par('assume non-symmetric behavior') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# -init
	at_init = MpcAttributeMetaData()
	at_init.type = MpcAttributeType.Boolean
	at_init.name = '-init'
	at_init.group = 'Optional parameters'
	at_init.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-init')+'<br/>') + 
		html_par('	apply initial stress)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# -mem
	at_mem = MpcAttributeMetaData()
	at_mem.type = MpcAttributeType.Boolean
	at_mem.name = '-mem'
	at_mem.group = 'Optional parameters'
	at_mem.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mem')+'<br/>') + 
		html_par('configure the load history memory') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	#Parameters for the optional parameters -kin
	# b_k
	at_bk = MpcAttributeMetaData()
	at_bk.type = MpcAttributeType.Real
	at_bk.name = 'b_k'
	at_bk.group = '-kin'
	at_bk.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b_k')+'<br/>') + 
		html_par('hardening ratio (E_k/E_0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# R_0
	at_R0 = MpcAttributeMetaData()
	at_R0.type = MpcAttributeType.Real
	at_R0.name = 'R_0'
	at_R0.group = '-kin'
	at_R0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R_0')+'<br/>') + 
		html_par('control the exponential transition from linear elastic to hardening asymptote. Recommended value: R_0=20') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# r_1
	at_r1 = MpcAttributeMetaData()
	at_r1.type = MpcAttributeType.Real
	at_r1.name = 'r_1'
	at_r1.group = '-kin'
	at_r1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('r_1')+'<br/>') + 
		html_par('control the exponential transition from linear elastic to hardening asymptote. Recommended value: r_=0.90') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# r_2
	at_r2 = MpcAttributeMetaData()
	at_r2.type = MpcAttributeType.Real
	at_r2.name = 'r_2'
	at_r2.group = '-kin'
	at_r2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('r_2c')+'<br/>') + 
		html_par('control the exponential transition from linear elastic to hardening asymptote. Recommended value: r_2=0.15') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	#Parameters for the optional parameters -iso
	# b_i
	at_bi = MpcAttributeMetaData()
	at_bi.type = MpcAttributeType.Real
	at_bi.name = 'b_i'
	at_bi.group = '-iso'
	at_bi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b_i')+'<br/>') + 
		html_par('initial hardening ratio (E_i/E_0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# b_l
	at_bl = MpcAttributeMetaData()
	at_bl.type = MpcAttributeType.Real
	at_bl.name = 'b_l'
	at_bl.group = '-iso'
	at_bl.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b_l')+'<br/>') + 
		html_par('saturated hardening ratio (E_is/E_0c)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# rho_i
	at_rhoi = MpcAttributeMetaData()
	at_rhoi.type = MpcAttributeType.Real
	at_rhoi.name = 'rho_i'
	at_rhoi.group = '-iso'
	at_rhoi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho_i')+'<br/>') + 
		html_par('specifies the position of the intersection point between initial and saturated hardening asymptotes') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# R_i
	at_Ri = MpcAttributeMetaData()
	at_Ri.type = MpcAttributeType.Real
	at_Ri.name = 'R_i'
	at_Ri.group = '-iso'
	at_Ri.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R_i')+'<br/>') + 
		html_par('control the exponential transition from initial to saturated asymptote') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# l_yp
	at_lyp = MpcAttributeMetaData()
	at_lyp.type = MpcAttributeType.Real
	at_lyp.name = 'l_yp'
	at_lyp.group = '-iso'
	at_lyp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('l_yp')+'<br/>') + 
		html_par('length of the yield plateau in eps_y0 = f_y / E_0 units') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	#Parameters for the optional parameters -ult
	# f_u
	at_fu = MpcAttributeMetaData()
	at_fu.type = MpcAttributeType.QuantityScalar
	at_fu.name = 'f_u'
	at_fu.group = '-ult'
	at_fu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('f_u')+'<br/>') + 
		html_par('ultimate strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	at_fu.dimension = u.F/u.L**2
	
	# R_u
	at_Ru = MpcAttributeMetaData()
	at_Ru.type = MpcAttributeType.Real
	at_Ru.name = 'R_u'
	at_Ru.group = '-ult'
	at_Ru.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R_u')+'<br/>') + 
		html_par('control the exponential transition from kinematic hardening to perfectly plastic asymptote') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	#Parameters for the optional parameters -asym-kin
	# b_kc
	at_bkc = MpcAttributeMetaData()
	at_bkc.type = MpcAttributeType.Real
	at_bkc.name = 'b_kc'
	at_bkc.group = '-asym-kin'
	at_bkc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b_kc')+'<br/>') + 
		html_par('hardening ratio (E_kc/E_0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# R_0c
	at_R0c = MpcAttributeMetaData()
	at_R0c.type = MpcAttributeType.Real
	at_R0c.name = 'R_0c'
	at_R0c.group = '-asym-kin'
	at_R0c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R_0c')+'<br/>') + 
		html_par('control the exponential transition from linear elastic to hardening asymptote. Recommended value: R_0c=20') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# r_1c
	at_r1c = MpcAttributeMetaData()
	at_r1c.type = MpcAttributeType.Real
	at_r1c.name = 'r_1c'
	at_r1c.group = '-asym-kin'
	at_r1c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('r_1c')+'<br/>') + 
		html_par('control the exponential transition from linear elastic to hardening asymptote. Recommended value: r_1c=0.90') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# r_2c
	at_r2c = MpcAttributeMetaData()
	at_r2c.type = MpcAttributeType.Real
	at_r2c.name = 'r_2c'
	at_r2c.group = '-asym-kin'
	at_r2c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('r_2c')+'<br/>') + 
		html_par('control the exponential transition from linear elastic to hardening asymptote. Recommended value: r_2c=0.15') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	#Parameters for the optional parameters -asym-iso
	# b_ic
	at_bic = MpcAttributeMetaData()
	at_bic.type = MpcAttributeType.Real
	at_bic.name = 'b_ic'
	at_bic.group = '-asym-iso'
	at_bic.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b_ic')+'<br/>') + 
		html_par('initial hardening ratio (E_ic/E_0c)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# rho_ic
	at_rhoic = MpcAttributeMetaData()
	at_rhoic.type = MpcAttributeType.Real
	at_rhoic.name = 'rho_ic'
	at_rhoic.group = '-asym-iso'
	at_rhoic.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho_ic')+'<br/>') + 
		html_par('specifies the position of the intersection point between initial and saturated hardening asymptotes') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# b_lc
	at_blc = MpcAttributeMetaData()
	at_blc.type = MpcAttributeType.Real
	at_blc.name = 'b_lc'
	at_blc.group = '-asym-iso'
	at_blc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b_lc')+'<br/>') + 
		html_par('saturated hardening ratio (E_is/E_0c)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	# R_ic
	at_Ric = MpcAttributeMetaData()
	at_Ric.type = MpcAttributeType.Real
	at_Ric.name = 'R_ic'
	at_Ric.group = '-asym-iso'
	at_Ric.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R_ic')+'<br/>') + 
		html_par('control the exponential transition from initial to saturated asymptote') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	#Parameters for the optional parameters -asym-ult
	# f_uc
	at_fuc = MpcAttributeMetaData()
	at_fuc.type = MpcAttributeType.QuantityScalar
	at_fuc.name = 'f_uc'
	at_fuc.group = '-asym-ult'
	at_fuc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('f_uc')+'<br/>') + 
		html_par('ultimate strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	at_fuc.dimension = u.F/u.L**2
	# R_uc
	at_Ruc = MpcAttributeMetaData()
	at_Ruc.type = MpcAttributeType.Real
	at_Ruc.name = 'R_uc'
	at_Ruc.group = '-asym-ult'
	at_Ruc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R_uc')+'<br/>') + 
		html_par('control the exponential transition from kinematic hardening to perfectly plastic asymptote') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	
	#Parameters for the optional parameters -mem
	# cycNum
	at_cycNum = MpcAttributeMetaData()
	at_cycNum.type = MpcAttributeType.Integer
	at_cycNum.name = 'cycNum'
	at_cycNum.group = '-mem'
	at_cycNum.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cycNum')+'<br/>') + 
		html_par('expected number of half-cycles during the loading process Efficiency of the material can be slightly increased by correctly setting this value. The default value is cycNum = 50 Load history memory can be turned off by setting $cycNum = 0.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	at_cycNum.setDefault(50)
	
	#Parameters for the optional parameters -init
	# sig_init
	at_siginit = MpcAttributeMetaData()
	at_siginit.type = MpcAttributeType.QuantityScalar
	at_siginit.name = 'sig_init'
	at_siginit.group = '-init'
	at_siginit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sig_init')+'<br/>') + 
		html_par('initial stress value') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Steel4_Material','Steel4 Material')+'<br/>') +
		html_end()
		)
	at_siginit.dimension = u.F/u.L**2
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'Steel4'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(at_f_y)
	xom.addAttribute(at_E_0c)
	xom.addAttribute(at_kin)
	xom.addAttribute(at_iso)
	xom.addAttribute(at_ult)
	xom.addAttribute(at_asym)
	xom.addAttribute(at_init)
	xom.addAttribute(at_mem)
	xom.addAttribute(at_bk)
	xom.addAttribute(at_R0)
	xom.addAttribute(at_r1)
	xom.addAttribute(at_r2)
	xom.addAttribute(at_bi)
	xom.addAttribute(at_bl)
	xom.addAttribute(at_rhoi)
	xom.addAttribute(at_Ri)
	xom.addAttribute(at_lyp)
	xom.addAttribute(at_fu)
	xom.addAttribute(at_Ru)
	xom.addAttribute(at_bkc)
	xom.addAttribute(at_R0c)
	xom.addAttribute(at_r1c)
	xom.addAttribute(at_r2c)
	xom.addAttribute(at_bic)
	xom.addAttribute(at_rhoic)
	xom.addAttribute(at_blc)
	xom.addAttribute(at_Ric)
	xom.addAttribute(at_fuc)
	xom.addAttribute(at_Ruc)
	xom.addAttribute(at_siginit)
	xom.addAttribute(at_cycNum)
	
	# kin-dep
	xom.setVisibilityDependency(at_kin, at_bk)
	xom.setVisibilityDependency(at_kin, at_R0)
	xom.setVisibilityDependency(at_kin, at_r1)
	xom.setVisibilityDependency(at_kin, at_r2)
	# kin-asym-dep
	xom.setVisibilityDependency(at_kin, at_bkc)
	xom.setVisibilityDependency(at_kin, at_R0c)
	xom.setVisibilityDependency(at_kin, at_r1c)
	xom.setVisibilityDependency(at_kin, at_r2c)
	
	xom.setVisibilityDependency(at_asym, at_bkc)
	xom.setVisibilityDependency(at_asym, at_R0c)
	xom.setVisibilityDependency(at_asym, at_r1c)
	xom.setVisibilityDependency(at_asym, at_r2c)
	# iso-dep
	xom.setVisibilityDependency(at_iso, at_bi)
	xom.setVisibilityDependency(at_iso, at_bl)
	xom.setVisibilityDependency(at_iso, at_rhoi)
	xom.setVisibilityDependency(at_iso, at_Ri)
	xom.setVisibilityDependency(at_iso, at_lyp)
	# iso-asym-dep
	xom.setVisibilityDependency(at_iso, at_bic)
	xom.setVisibilityDependency(at_iso, at_blc)
	xom.setVisibilityDependency(at_iso, at_rhoic)
	xom.setVisibilityDependency(at_iso, at_Ric)
	
	xom.setVisibilityDependency(at_asym, at_bic)
	xom.setVisibilityDependency(at_asym, at_blc)
	xom.setVisibilityDependency(at_asym, at_rhoic)
	xom.setVisibilityDependency(at_asym, at_Ric)
	# ult-dep
	xom.setVisibilityDependency(at_ult, at_fu)
	xom.setVisibilityDependency(at_ult, at_Ru)
	# ult-asym-dep
	xom.setVisibilityDependency(at_ult, at_fuc)
	xom.setVisibilityDependency(at_ult, at_Ruc)
	
	xom.setVisibilityDependency(at_asym, at_fuc)
	xom.setVisibilityDependency(at_asym, at_Ruc)
	# init
	xom.setVisibilityDependency(at_init, at_siginit)
	# mem
	xom.setVisibilityDependency(at_mem, at_cycNum)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Steel4 $matTag $f_y $E_0 <-asym> <-kin $b_k $R_0 $r_1 $r_2 <$b_kc $R_0c $r_1c $r_2c>>
	# <-iso $b_i $rho_i $b_l $R_i $l_yp <$b_ic $rho_ic $b_lc $R_ic>> <-ult $f_u $R_u <$f_uc $R_uc>>
	# <-mem $cycNum> <-init $sig_init>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	f_y_at = xobj.getAttribute('f_y')
	if(f_y_at is None):
		raise Exception('Error: cannot find "f_y" attribute')
	f_y = f_y_at.quantityScalar
	
	E_0_at = xobj.getAttribute('E_0c')
	if(E_0_at is None):
		raise Exception('Error: cannot find "E_0c" attribute')
	E_0 = E_0_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	# <-asym>
	asym_at = xobj.getAttribute('-asym')
	if(asym_at is None):
		raise Exception('Error: cannot find "-asym" attribute')
	asym = asym_at.boolean
	if asym:
		sopt += '-asym'
	
	# <-kin $b_k $R_0 $r_1 $r_2 <$b_kc $R_0c $r_1c $r_2c>>
	kin_at = xobj.getAttribute('-kin')
	if(kin_at is None):
		raise Exception('Error: cannot find "-kin" attribute')
	kin = kin_at.boolean
	if kin:
		b_k_at = xobj.getAttribute('b_k')
		if(b_k_at is None):
			raise Exception('Error: cannot find "b_k" attribute')
		b_k = b_k_at.real
		
		R_0_at = xobj.getAttribute('R_0')
		if(R_0_at is None):
			raise Exception('Error: cannot find "R_0" attribute')
		R_0 = R_0_at.real
		
		r_1_at = xobj.getAttribute('r_1')
		if(r_1_at is None):
			raise Exception('Error: cannot find "r_1" attribute')
		r_1 = r_1_at.real
		
		r_2_at = xobj.getAttribute('r_2')
		if(r_2_at is None):
			raise Exception('Error: cannot find "r_2" attribute')
		r_2 = r_2_at.real
		
		sopt += ' -kin {} {} {} {}'.format(b_k, R_0, r_1, r_2)
		
		# <-asym> and <-kin>
		if asym:
			b_kc_at = xobj.getAttribute('b_kc')
			if(b_kc_at is None):
				raise Exception('Error: cannot find "b_kc" attribute')
			b_kc = b_kc_at.real
			
			R_0c_at = xobj.getAttribute('R_0c')
			if(R_0c_at is None):
				raise Exception('Error: cannot find "R_0c" attribute')
			R_0c = R_0c_at.real
			
			r_1c_at = xobj.getAttribute('r_1c')
			if(r_1c_at is None):
				raise Exception('Error: cannot find "r_1c" attribute')
			r_1c = r_1c_at.real
			
			r_2c_at = xobj.getAttribute('r_2c')
			if(r_2c_at is None):
				raise Exception('Error: cannot find "r_2c" attribute')
			r_2c = r_2c_at.real
			
			sopt += ' {} {} {} {}'.format(b_kc, R_0c, r_1c, r_2c)
	
	# <-iso $b_i $rho_i $b_l $R_i $l_yp <$b_ic $rho_ic $b_lc $R_ic>>
	iso_at = xobj.getAttribute('-iso')
	if(iso_at is None):
		raise Exception('Error: cannot find "-iso" attribute')
	iso = iso_at.boolean
	if iso:
		b_i_at = xobj.getAttribute('b_i')
		if(b_i_at is None):
			raise Exception('Error: cannot find "b_i" attribute')
		b_i = b_i_at.real
		
		rho_i_at = xobj.getAttribute('rho_i')
		if(rho_i_at is None):
			raise Exception('Error: cannot find "rho_i" attribute')
		rho_i = rho_i_at.real
		
		b_l_at = xobj.getAttribute('b_l')
		if(b_l_at is None):
			raise Exception('Error: cannot find "b_l" attribute')
		b_l = b_l_at.real
		
		R_i_at = xobj.getAttribute('R_i')
		if(R_i_at is None):
			raise Exception('Error: cannot find "R_i" attribute')
		R_i = R_i_at.real
		
		l_yp_at = xobj.getAttribute('l_yp')
		if(l_yp_at is None):
			raise Exception('Error: cannot find "l_yp" attribute')
		l_yp = l_yp_at.real
		
		sopt += ' -iso {} {} {} {} {}'.format(b_i, rho_i, b_l, R_i, l_yp)
		
		# <-asym> and <-iso>
		if asym:
			b_ic_at = xobj.getAttribute('b_ic')
			if(b_ic_at is None):
				raise Exception('Error: cannot find "b_ic" attribute')
			b_ic = b_ic_at.real
			
			rho_ic_at = xobj.getAttribute('rho_ic')
			if(rho_ic_at is None):
				raise Exception('Error: cannot find "rho_ic" attribute')
			rho_ic = rho_ic_at.real
			
			b_lc_at = xobj.getAttribute('b_lc')
			if(b_lc_at is None):
				raise Exception('Error: cannot find "b_lc" attribute')
			b_lc = b_lc_at.real
			
			R_ic_at = xobj.getAttribute('R_ic')
			if(R_ic_at is None):
				raise Exception('Error: cannot find "R_ic" attribute')
			R_ic = R_ic_at.real
			
			sopt += ' {} {} {} {}'.format(b_ic, rho_ic, b_lc, R_ic)
	
	# <-ult $f_u $R_u <$f_uc $R_uc>>
	ult_at = xobj.getAttribute('-ult')
	if(ult_at is None):
		raise Exception('Error: cannot find "-ult" attribute')
	ult = ult_at.boolean
	if ult:
		f_u_at = xobj.getAttribute('f_u')
		if(f_u_at is None):
			raise Exception('Error: cannot find "f_u" attribute')
		f_u = f_u_at.quantityScalar
		
		R_u_at = xobj.getAttribute('R_u')
		if(R_u_at is None):
			raise Exception('Error: cannot find "R_u" attribute')
		R_u = R_u_at.real
		
		sopt += ' -ult {} {}'.format(f_u.value, R_u)
		
		# <-asym> and <-ult>
		if asym:
			f_uc_at = xobj.getAttribute('f_uc')
			if(f_uc_at is None):
				raise Exception('Error: cannot find "f_uc" attribute')
			f_uc = f_uc_at.quantityScalar
			
			R_uc_at = xobj.getAttribute('R_uc')
			if(R_uc_at is None):
				raise Exception('Error: cannot find "R_uc" attribute')
			R_uc = R_uc_at.real
			
			sopt += ' {} {}'.format(f_uc.value, R_uc)
	
	# <-mem $cycNum>
	mem_at = xobj.getAttribute('-mem')
	if(mem_at is None):
		raise Exception('Error: cannot find "-mem" attribute')
	mem = mem_at.boolean
	if mem:
		cycNum_at = xobj.getAttribute('cycNum')
		if(cycNum_at is None):
			raise Exception('Error: cannot find "cycNum" attribute')
		cycNum = cycNum_at.integer
		
		sopt += ' -mem {}'.format(cycNum)
	
	# <-init $sig_init>
	init_at = xobj.getAttribute('-init')
	if(init_at is None):
		raise Exception('Error: cannot find "-init" attribute')
	init = init_at.boolean
	if init:
		sig_init_at = xobj.getAttribute('sig_init')
		if(sig_init_at is None):
			raise Exception('Error: cannot find "sig_init" attribute')
		sig_init = sig_init_at.quantityScalar
		
		sopt += ' -init {}'.format(sig_init.value)
	
	
	str_tcl = '{}uniaxialMaterial Steel4 {} {} {} {}\n'.format(pinfo.indent, tag, f_y.value, E_0.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)