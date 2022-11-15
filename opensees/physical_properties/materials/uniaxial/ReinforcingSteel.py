# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fy
	at_fy = MpcAttributeMetaData()
	at_fy.type = MpcAttributeType.QuantityScalar
	at_fy.name = 'fy'
	at_fy.group = 'Non-linear'
	at_fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fy')+'<br/>') + 
		html_par('Yield stress in tension') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_fy.dimension = u.F/u.L**2
	
	# fu
	at_fu = MpcAttributeMetaData()
	at_fu.type = MpcAttributeType.QuantityScalar
	at_fu.name = 'fu'
	at_fu.group = 'Non-linear'
	at_fu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fu')+'<br/>') + 
		html_par('Ultimate stress in tension') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_fu.dimension = u.F/u.L**2
	
	# Es
	at_Es = MpcAttributeMetaData()
	at_Es.type = MpcAttributeType.QuantityScalar
	at_Es.name = 'Es'
	at_Es.group = 'Elasticity'
	at_Es.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Es')+'<br/>') + 
		html_par('Initial elastic tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_Es.dimension = u.F/u.L**2
	
	# Esh
	at_Esh = MpcAttributeMetaData()
	at_Esh.type = MpcAttributeType.QuantityScalar
	at_Esh.name = 'Esh'
	at_Esh.group = 'Non-linear'
	at_Esh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Esh')+'<br/>') + 
		html_par('Tangent at initial strain hardening') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_Esh.dimension = u.F/u.L**2
	
	# esh
	at_esh = MpcAttributeMetaData()
	at_esh.type = MpcAttributeType.Real
	at_esh.name = 'esh'
	at_esh.group = 'Non-linear'
	at_esh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('esh')+'<br/>') + 
		html_par('Strain corresponding to initial strain hardening') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	# eult
	at_eult = MpcAttributeMetaData()
	at_eult.type = MpcAttributeType.Real
	at_eult.name = 'eult'
	at_eult.group = 'Non-linear'
	at_eult.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eult')+'<br/>') + 
		html_par('Strain at peak stress') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	#aex_option
	# at_aex_option = MpcAttributeMetaData()
	# at_aex_option.type = MpcAttributeType.String
	# at_aex_option.name = 'Option'
	# at_aex_option.group = 'Non-linear'
	# at_aex_option.description = (
		# html_par(html_begin()) +
		# html_par(html_boldtext('Option')+'<br/>') + 
		# html_par('Choose between -GABuck, -DMBuck, -CMFatigue, -MPCurveParams and -IsoHard') +
		# html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		# html_end()
		# )
	# at_aex_option.sourceType = MpcAttributeSourceType.List
	# at_aex_option.setSourceList(['-GABuck', '-DMBuck', '-CMFatigue', '-MPCurveParams', '-IsoHard'])
	# at_aex_option.setDefault('-GABuck')
	
	# -GABuck
	at_GABuck = MpcAttributeMetaData()
	at_GABuck.type = MpcAttributeType.Boolean
	at_GABuck.name = '-GABuck'
	at_GABuck.group = 'Optional parameters'
	at_GABuck.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-GABuck')+'<br/>') + 
		html_par('Buckling Model Based on Gomes and Appleton (1997)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	#at_GABuck.editable = False
	
	# -DMBuck
	at_DMBuck = MpcAttributeMetaData()
	at_DMBuck.type = MpcAttributeType.Boolean
	at_DMBuck.name = '-DMBuck'
	at_DMBuck.group = 'Optional parameters'
	at_DMBuck.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-DMBuck')+'<br/>') + 
		html_par('Buckling model based on Dhakal and Maekawa (2002)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	#at_DMBuck.editable = False
	
	# -CMFatigue
	at_CMFatigue = MpcAttributeMetaData()
	at_CMFatigue.type = MpcAttributeType.Boolean
	at_CMFatigue.name = '-CMFatigue'
	at_CMFatigue.group = 'Optional parameters'
	at_CMFatigue.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-CMFatigue')+'<br/>') + 
		html_par('Coffin-Manson Fatigue and Strength Reduction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	#at_CMFatigue.editable = False
	
	# -MPCurveParams
	at_MPCurveParams = MpcAttributeMetaData()
	at_MPCurveParams.type = MpcAttributeType.Boolean
	at_MPCurveParams.name = '-MPCurveParams'
	at_MPCurveParams.group = 'Optional parameters'
	at_MPCurveParams.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-MPCurveParams')+'<br/>') + 
		html_par('Menegotto and Pinto Curve Parameters') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	#at_MPCurveParams.editable = False
	
	# -IsoHard
	at_IsoHard = MpcAttributeMetaData()
	at_IsoHard.type = MpcAttributeType.Boolean
	at_IsoHard.name = '-IsoHard'
	at_IsoHard.group = 'Optional parameters'
	at_IsoHard.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-IsoHard')+'<br/>') + 
		html_par('Isotropic Hardening / Diminishing Yield Plateau') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	#at_IsoHard.editable = False
	
	#Parameters for the optional parameters -GABuck
	# lsr1
	at_lsr1 = MpcAttributeMetaData()
	at_lsr1.type = MpcAttributeType.Real
	at_lsr1.name = 'lsr/1'
	at_lsr1.group = '-GABuck'
	at_lsr1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lsr')+'<br/>') + 
		html_par('Slenderness Ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = '-GABuck'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') + 
		html_par('Amplification factor for the buckled stress strain curve') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	# r
	at_r = MpcAttributeMetaData()
	at_r.type = MpcAttributeType.Real
	at_r.name = 'r'
	at_r.group = '-GABuck'
	at_r.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('r')+'<br/>') + 
		html_par('Buckling reduction factor. r can be a real number between [0.0 and 1.0]. r=1.0 full reduction (no buckling). r=0.0 no reduction 0.0<r<1.0 linear interpolation between buckled and unbuckled curves') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	# gamma
	at_gamma = MpcAttributeMetaData()
	at_gamma.type = MpcAttributeType.Real
	at_gamma.name = 'gamma'
	at_gamma.group = '-GABuck'
	at_gamma.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') + 
		html_par('Buckling constant') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	#Parameters for the optional parameters -DMBuck
	# lsr2
	at_lsr2 = MpcAttributeMetaData()
	at_lsr2.type = MpcAttributeType.Real
	at_lsr2.name = 'lsr/2'
	at_lsr2.group = '-DMBuck'
	at_lsr2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lsr')+'<br/>') + 
		html_par('Slenderness Ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	# alpha1
	at_alpha1 = MpcAttributeMetaData()
	at_alpha1.type = MpcAttributeType.Real
	at_alpha1.name = 'alpha/1'
	at_alpha1.group = '-DMBuck'
	at_alpha1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('Adjustment Constant usually between 0.75 and 1.0. Default: alpha=1.0, this parameter is optional.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_alpha1.setDefault(1.0)
	
	#Parameters for the optional parameters -CMFatigue
	# Cf
	at_Cf = MpcAttributeMetaData()
	at_Cf.type = MpcAttributeType.Real
	at_Cf.name = 'Cf'
	at_Cf.group = '-CMFatigue'
	at_Cf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Cf')+'<br/>') + 
		html_par('Coffin-Manson constant C') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	# alpha2
	at_alpha2 = MpcAttributeMetaData()
	at_alpha2.type = MpcAttributeType.Real
	at_alpha2.name = 'alpha/2'
	at_alpha2.group = '-CMFatigue'
	at_alpha2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('Coffin-Manson constant a') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	# Cd
	at_Cd = MpcAttributeMetaData()
	at_Cd.type = MpcAttributeType.Real
	at_Cd.name = 'Cd'
	at_Cd.group = '-CMFatigue'
	at_Cd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Cd')+'<br/>') + 
		html_par('CCyclic strength reduction constant') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	
	#Parameters for the optional parameters -MPCurveParams
	# R1
	at_R1 = MpcAttributeMetaData()
	at_R1.type = MpcAttributeType.Real
	at_R1.name = 'R1'
	at_R1.group = '-MPCurveParams'
	at_R1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R1')+'<br/>') + 
		html_par('(default = 0.333)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_R1.setDefault(0.333)
	
	# R2
	at_R2 = MpcAttributeMetaData()
	at_R2.type = MpcAttributeType.Real
	at_R2.name = 'R2'
	at_R2.group = '-MPCurveParams'
	at_R2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R2')+'<br/>') + 
		html_par('(default = 18)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_R2.setDefault(18)
	
	# R3
	at_R3 = MpcAttributeMetaData()
	at_R3.type = MpcAttributeType.Real
	at_R3.name = 'R3'
	at_R3.group = '-MPCurveParams'
	at_R3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('R3')+'<br/>') + 
		html_par('(default = 4)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_R3.setDefault(4)
	
	#Parameters for the optional parameters -IsoHard
	# a1
	at_a1 = MpcAttributeMetaData()
	at_a1.type = MpcAttributeType.Real
	at_a1.name = 'a1'
	at_a1.group = '-IsoHard'
	at_a1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a1')+'<br/>') + 
		html_par('Hardening constant (default = 4.3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_a1.setDefault(4.3)
	
	# limit
	at_limit = MpcAttributeMetaData()
	at_limit.type = MpcAttributeType.Real
	at_limit.name = 'limit'
	at_limit.group = '-IsoHard'
	at_limit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('limit')+'<br/>') + 
		html_par('Limit for the reduction of the yield plateau. % of original plateau length to remain (0.01 < limit < 1.0 ).Limit =1.0, then no reduction takes place (default =0.01)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Reinforcing_Steel_Material','ReinforcingSteel Material')+'<br/>') +
		html_end()
		)
	at_limit.setDefault(0.01)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'ReinforcingSteel'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(at_fy)
	xom.addAttribute(at_fu)
	xom.addAttribute(at_Es)
	xom.addAttribute(at_Esh)
	xom.addAttribute(at_esh)
	xom.addAttribute(at_eult)
	#xom.addAttribute(at_aex_option)
	xom.addAttribute(at_GABuck)
	xom.addAttribute(at_lsr1)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_r)
	xom.addAttribute(at_gamma)
	xom.addAttribute(at_DMBuck)
	xom.addAttribute(at_lsr2)
	xom.addAttribute(at_alpha1)
	xom.addAttribute(at_CMFatigue)
	xom.addAttribute(at_Cf)
	xom.addAttribute(at_alpha2)
	xom.addAttribute(at_Cd)
	xom.addAttribute(at_MPCurveParams)
	xom.addAttribute(at_R1)
	xom.addAttribute(at_R2)
	xom.addAttribute(at_R3)
	xom.addAttribute(at_IsoHard)
	xom.addAttribute(at_a1)
	xom.addAttribute(at_limit)
	
	# GABuck-dep
	xom.setVisibilityDependency(at_GABuck, at_lsr1)
	xom.setVisibilityDependency(at_GABuck, at_beta)
	xom.setVisibilityDependency(at_GABuck, at_r)
	xom.setVisibilityDependency(at_GABuck, at_gamma)
	
	# DMBuck-dep
	xom.setVisibilityDependency(at_DMBuck, at_lsr2)
	xom.setVisibilityDependency(at_DMBuck, at_alpha1)
	
	
	# CMFatigue-dep
	xom.setVisibilityDependency(at_CMFatigue, at_Cf)
	xom.setVisibilityDependency(at_CMFatigue, at_alpha2)
	xom.setVisibilityDependency(at_CMFatigue, at_Cd)
	
	# MPCurveParams-dep
	xom.setVisibilityDependency(at_MPCurveParams, at_R1)
	xom.setVisibilityDependency(at_MPCurveParams, at_R2)
	xom.setVisibilityDependency(at_MPCurveParams, at_R3)
	
	# IsoHard-dep
	xom.setVisibilityDependency(at_IsoHard, at_a1)
	xom.setVisibilityDependency(at_IsoHard, at_limit)
	
	
	# auto-exclusive dependencies
	# -GABuck, -DMBuck, -CMFatigue, -MPCurveParams, -IsoHard
	#xom.setBooleanAutoExclusiveDependency(at_aex_option, at_GABuck)
	#xom.setBooleanAutoExclusiveDependency(at_aex_option, at_DMBuck)
	#xom.setBooleanAutoExclusiveDependency(at_aex_option, at_CMFatigue)
	#xom.setBooleanAutoExclusiveDependency(at_aex_option, at_MPCurveParams)
	#xom.setBooleanAutoExclusiveDependency(at_aex_option, at_IsoHard)
	
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ReinforcingSteel $matTag $fy $fu $Es $Esh $esh $eult
	# <-GABuck $lsr $beta $r $gamma> <-DMBuck $lsr $alpha> <-CMFatigue $Cf $alpha $Cd>
	# <-MPCurveParams $R1 $R2 $R3> <-IsoHard $a1 $limit>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fy_at = xobj.getAttribute('fy')
	if(fy_at is None):
		raise Exception('Error: cannot find "fy" attribute')
	fy = fy_at.quantityScalar
	
	fu_at = xobj.getAttribute('fu')
	if(fu_at is None):
		raise Exception('Error: cannot find "fu" attribute')
	fu = fu_at.quantityScalar
	
	Es_at = xobj.getAttribute('Es')
	if(Es_at is None):
		raise Exception('Error: cannot find "Es" attribute')
	Es = Es_at.quantityScalar
	
	Esh_at = xobj.getAttribute('Esh')
	if(Esh_at is None):
		raise Exception('Error: cannot find "Esh" attribute')
	Esh = Esh_at.quantityScalar
	
	esh_at = xobj.getAttribute('esh')
	if(esh_at is None):
		raise Exception('Error: cannot find "esh" attribute')
	esh = esh_at.real
	
	eult_at = xobj.getAttribute('eult')
	if(eult_at is None):
		raise Exception('Error: cannot find "eult" attribute')
	eult = eult_at.real
	
	
	# optional paramters
	sopt = ''
	
	# <-GABuck $lsr $beta $r $gamma>
	GABuck_at = xobj.getAttribute('-GABuck')
	if(GABuck_at is None):
		raise Exception('Error: cannot find "-GABuck" attribute')
	GABuck = GABuck_at.boolean
	if GABuck:
		lsr1_at = xobj.getAttribute('lsr/1')
		if(lsr1_at is None):
			raise Exception('Error: cannot find "lsr" attribute')
		lsr1 = lsr1_at.real
		
		beta_at = xobj.getAttribute('beta')
		if(beta_at is None):
			raise Exception('Error: cannot find "beta" attribute')
		beta = beta_at.real
		
		r_at = xobj.getAttribute('r')
		if(r_at is None):
			raise Exception('Error: cannot find "r" attribute')
		r = r_at.real
		
		gamma_at = xobj.getAttribute('gamma')
		if(gamma_at is None):
			raise Exception('Error: cannot find "gamma" attribute')
		gamma = gamma_at.real
		
		sopt += '-GABuck {} {} {} {}'.format(lsr1, beta, r, gamma)
	else:
		# <-DMBuck $lsr $alpha>
		DMBuck_at = xobj.getAttribute('-DMBuck')
		if(DMBuck_at is None):
			raise Exception('Error: cannot find "-DMBuck" attribute')
		DMBuck = DMBuck_at.boolean
		if DMBuck:
			lsr2_at = xobj.getAttribute('lsr/2')
			if(lsr2_at is None):
				raise Exception('Error: cannot find "lsr" attribute')
			lsr2 = lsr2_at.real
			
			alpha1_at = xobj.getAttribute('alpha/1')
			if(alpha1_at is None):
				raise Exception('Error: cannot find "alpha" attribute')
			alpha1 = alpha1_at.real
			
			sopt += '-DMBuck {} {}'.format(lsr2, alpha1)
		else:
			# <-CMFatigue $Cf $alpha $Cd>
			CMFatigue_at = xobj.getAttribute('-CMFatigue')
			if(CMFatigue_at is None):
				raise Exception('Error: cannot find "-CMFatigue" attribute')
			CMFatigue = CMFatigue_at.boolean
			if CMFatigue:
				Cf_at = xobj.getAttribute('Cf')
				if(Cf_at is None):
					raise Exception('Error: cannot find "Cf" attribute')
				Cf = Cf_at.real
				
				alpha2_at = xobj.getAttribute('alpha/2')
				if(alpha2_at is None):
					raise Exception('Error: cannot find "alpha" attribute')
				alpha2 = alpha2_at.real
				
				Cd_at = xobj.getAttribute('Cd')
				if(Cd_at is None):
					raise Exception('Error: cannot find "Cd" attribute')
				Cd = Cd_at.real
				
				sopt += '-CMFatigue {} {} {}'.format(Cf, alpha2, Cd)
			else:
				# <-MPCurveParams $R1 $R2 $R3>
				MPCurveParams_at = xobj.getAttribute('-MPCurveParams')
				if(MPCurveParams_at is None):
					raise Exception('Error: cannot find "-MPCurveParams" attribute')
				MPCurveParams = MPCurveParams_at.boolean
				if MPCurveParams:
					R1_at = xobj.getAttribute('R1')
					if(R1_at is None):
						raise Exception('Error: cannot find "R1" attribute')
					R1 = R1_at.real
					
					R2_at = xobj.getAttribute('R2')
					if(R2_at is None):
						raise Exception('Error: cannot find "R2" attribute')
					R2 = R2_at.real
					
					R3_at = xobj.getAttribute('R3')
					if(R3_at is None):
						raise Exception('Error: cannot find "R3" attribute')
					R3 = R3_at.real
					
					sopt += '-MPCurveParams {} {} {}'.format(R1, R2, R3)
				else:
					# <-IsoHard $a1 $limit>
					IsoHard_at = xobj.getAttribute('-IsoHard')
					if(IsoHard_at is None):
						raise Exception('Error: cannot find "-IsoHard" attribute')
					IsoHard = IsoHard_at.boolean
					if IsoHard:
						a1_at = xobj.getAttribute('a1')
						if(a1_at is None):
							raise Exception('Error: cannot find "a1" attribute')
						a1 = a1_at.real
						
						limit_at = xobj.getAttribute('limit')
						if(limit_at is None):
							raise Exception('Error: cannot find "limit" attribute')
						limit = limit_at.real
						
						sopt += '-IsoHard {} {}'.format(a1, limit)
	
	
	str_tcl = '{}uniaxialMaterial ReinforcingSteel {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fy.value, fu.value, Es.value, Esh.value, esh, eult, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)