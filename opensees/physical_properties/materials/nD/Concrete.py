# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	#html_par('To obtain a free version of the DLL for this material, please contact us') +
	def make_attr(name, group, descr):
		at = MpcAttributeMetaData()
		at.name = name
		at.group = group
		at.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
			html_par('contact: diego.talledo@iuav.it') +
			html_par(html_href('website','Concrete')+'<br/>') +
			html_end()
			)
		return at

	# fc
	at_fc = make_attr('fc', 'Strength', 'concrete compressive strength*<br>Concrete compressive strength and the corresponding strain should be input as negative values.<br>The value of fc is used for computing default values for other parameters.')
	at_fc.type = MpcAttributeType.QuantityScalar
	at_fc.dimension = u.F/u.L**2
	at_fc.setDefault(-30.0)
	
	# Ec
	at_Ec = make_attr('Ec', 'Elasticity', 'concrete elastic modulus*<br>Concrete elastic  modulus should be input as positive value.<br>Default value = [TO BE IMPLEMENTED].')
	at_Ec.type = MpcAttributeType.QuantityScalar
	at_Ec.dimension = u.F/u.L**2
	at_Ec.setDefault(30000) #DT Da aggiornare con Model Code 2010 o altro computed -> da implementare, sentire Massimo
	
	# v
	at_v = make_attr('v', 'Elasticity', 'concrete Poisson\'s ratio*<br>Typical values are 0.15-0.2 for uncracked concrete and 0.0 for cracked concrete')
	at_v.type = MpcAttributeType.Real
	at_v.name = 'v'
	at_v.setDefault(0.2)
	
	# f0n
	at_f0n = make_attr('f0n', 'Non-linear', 'concrete compressive stress corresponding to elastic threeshold*<br>Concrete compressive strengths and the corresponding strains should be input as negative values.<br>Default value = 0.6*fc.')
	at_f0n.type = MpcAttributeType.QuantityScalar
	at_f0n.dimension = u.F/u.L**2
	at_f0n.setDefault(-19.5) #DT Da aggiornare con Model Code 2010 o altro computed -> da implementare, sentire Massimo
	
	# f02dn
	at_f02dn = make_attr('f02dn', 'Non-linear', 'concrete compressive stress corresponding to elastic threeshold under biaxial conditions*<br>Concrete compressive strengths and the corresponding strains should be input as negative values.<br>Default value = 1.2*f0n.')
	at_f02dn.type = MpcAttributeType.QuantityScalar
	at_f02dn.dimension = u.F/u.L**2
	at_f02dn.setDefault(-23.4) #DT Da aggiornare con Model Code 2010 o altro computed -> da implementare, sentire Massimo
	
	# ft
	at_ft = make_attr('ft', 'Non-linear', 'concrete tensile strength*<br>Concrete tensile strengths and the corresponding strains should be input as positive values.<br>Default value = [TO BE IMPLEMENTED].')
	at_ft.type = MpcAttributeType.QuantityScalar
	at_ft.dimension = u.F/u.L**2
	at_ft.setDefault(3.0) #DT Da aggiornare con Model Code 2010 o altro computed -> da implementare, sentire Massimo
	
	# beta
	at_beta = make_attr('beta', 'Non-linear', 'concrete plastic parameter*<br>Increment of plastic strain is equal to beta times increment of total strain.<br>The typical value for beta is between 0.2 and 0.5.')
	at_beta.type = MpcAttributeType.Real
	at_beta.setDefault(0.3)
	
	# An
	at_An = make_attr('An', 'Non-linear', 'negative damage parameter*<br>Parameter for evolution of negative damage.<br>The typical value for An is between 2 and 5.')
	at_An.type = MpcAttributeType.Real
	at_An.setDefault(2.5)
	
	# Bn
	at_Bn = make_attr('Bn', 'Non-linear', 'negative damage parameter*<br>Parameter for evolution of negative damage.<br>The typical value for Bn is between 0.7 and 0.9.')
	at_Bn.type = MpcAttributeType.Real
	at_Bn.setDefault(0.8)
	
	# Gf
	at_Gf = make_attr('Gf', 'Non-linear', 'fracture energy*<br>This is the fracture energy, used to compute the parameter A+. The units are force/m.<br>Default value: [TO BE IMPLEMENTED].')
	at_Gf.type = MpcAttributeType.QuantityScalar
	at_Gf.dimension = u.F/u.L
	at_Gf.setDefault(0.100) # Da cambiare con MC 2010
	
	# Valori opzionali
	
	# Ap
	at_Ap = make_attr('Ap', 'Optional Parameters', 'positive damage parameter*<br>Parameter for evolution of positive damage.<br>If Gf is specified this parameter is evaluated automatically to regularize fracture energy.')
	at_Ap.type = MpcAttributeType.Real
	at_Ap.setDefault(0.0) 
	
	# -lc
	at_use_lc = make_attr('-lc', 'Optional Parameters', 'Characteristic Length*<br>If specified, this value is used for the material, otherwise it is evaluated from the element<br>Default value: 0.0.')
	at_use_lc.type = MpcAttributeType.Boolean
	
	# lc
	at_lc = make_attr('lc', '-lc', 'Characteristic Length*<br>If specified, this value is used for the material, otherwise it is evaluated from the element')
	at_lc.type = MpcAttributeType.QuantityScalar
	at_lc.dimension = u.L
	at_lc.setDefault(0.0)
	
	# -dpMax
	at_use_dpMax = make_attr('-dpMax', 'Optional Parameters', 'Maximum positive damage parameter*<br>The value must be in the range 0.0 - 1.0.<br>Default value = 0.99999.')
	at_use_dpMax.type = MpcAttributeType.Boolean
	
	# dpMax
	at_dpMax = make_attr('dpMax', '-dpMax', 'Maximum positive damage parameter*<br>The value must be in the range 0.0 - 1.0.<br>Default value = 0.99999.')
	at_dpMax.type = MpcAttributeType.Real
	at_dpMax.setDefault(0.99999)
	
	# -dnMax
	at_use_dnMax = make_attr('-dnMax', 'Optional Parameters', 'Maximum negative damage parameter*<br>The value must be in the range 0.0 - 1.0.<br>Default value = 0.99999.')
	at_use_dnMax.type = MpcAttributeType.Boolean
	
	# dnMax
	at_dnMax = make_attr('dnMax', '-dnMax', 'Maximum negative damage parameter*<br>The value must be in the range 0.0 - 1.0.<br>Default value = 0.99999.')
	at_dnMax.type = MpcAttributeType.Real
	at_dnMax.setDefault(0.99999)
	
	# -dchem
	at_use_dchem = make_attr('-dchem', 'Environmental Damage', 'Environmental Negative&Positive Damage*<br>If not provided a different value for environmental positive damage, this value will affect both positive and negative stresses<br>The value must be in the range 0.0 - 1.0.<br>Default value = 0.0')
	at_use_dchem.type = MpcAttributeType.Boolean
	
	# dchem
	at_dchem = make_attr('dchem', '-dchem', 'Environmental Negative&Positive Damage*<br>If not provided a different value for environmental positive damage, this value will affect both positive and negative stresses<br>The value must be in the range 0.0 - 1.0.<br>Default value = 0.0')
	at_dchem.type = MpcAttributeType.Real
	at_dchem.setDefault(0.0)
	
	# -dchemp
	at_use_dchemp = make_attr('-dchemp', 'Environmental Damage', 'Environmental Positive Damage*<br>The value must be in the range 0.0 - 1.0.<br>Default value = 0.0')
	at_use_dchemp.type = MpcAttributeType.Boolean
	
	# dchemp
	at_dchemp = make_attr('dchemp', '-dchemp', 'Environmental Positive Damage*<br>The value must be in the range 0.0 - 1.0.<br>Default value = 0.0')
	at_dchemp.type = MpcAttributeType.Real
	at_dchemp.setDefault(0.0)
	
	# -dchemvar
	at_use_dchemvar = make_attr('-dchemvar', 'Environmental Damage', 'Variable Environmental Damage*<br>[TO BE IMPLEMENTED]')
	at_use_dchemvar.type = MpcAttributeType.Boolean
	
	# dchemvar eps_u
	at_eps_u = make_attr('eps_u', '-dchemvar', 'Environmental Positive Damage*<br>Strain at which maximum damage is reached?[TO BE IMPLEMENTED]<br>Default value = 0.0')
	at_eps_u.type = MpcAttributeType.Real
	at_eps_u.setDefault(0.0)
	
	# -srf
	at_use_srf = make_attr('-srf', 'Optional Parameters', 'Shear Retention Factor*<br>[To be completed]')
	at_use_srf.type = MpcAttributeType.Boolean
	
	# gammaC
	at_gammaC = make_attr('gammaC', '-srf', 'Shear Retention Factor*<br>[To be completed]<br>Default value: -0.001 (Negative value = no influence of SRF)')
	at_gammaC.type = MpcAttributeType.Real
	at_gammaC.setDefault(-0.001)
	
	# -srfCompr
	at_use_srfCompr = make_attr('-srfCompr', '-srf', 'Shear Retention Factor also in compression*<br>[To be completed]<br>By default it is aplied only in tension')
	at_use_srfCompr.type = MpcAttributeType.Boolean
	at_use_srfCompr.setDefault(False)
	
	# -eqTensDef
	at_use_eqTensDef = make_attr('-eqTensDef', 'Optional Parameters', 'Equivalente tension to be adopted*<br>[To be completed]<br>Default value = 2 (as Compdyn 2009)')
	at_use_eqTensDef.type = MpcAttributeType.Boolean
	
	# eqTensDef
	at_eqTensDef = make_attr('eqTensDef', '-srf', 'Shear Retention Factor*<br>[To be completed]<br>Default value: -0.001 (Negative value = no influence of SRF)')
	at_eqTensDef.type = MpcAttributeType.Integer
	at_eqTensDef.setDefault(2)
	
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
	xom.name = 'Concrete'
	xom.Xgroup = 'IUAV nD Materials Concrete Masonry'
	xom.addAttribute(at_fc)
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_v)
	xom.addAttribute(at_f0n)
	xom.addAttribute(at_f02dn)
	xom.addAttribute(at_ft)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_An)
	xom.addAttribute(at_Bn)
	xom.addAttribute(at_Gf)
	xom.addAttribute(at_use_lc)
	xom.addAttribute(at_lc)
	xom.addAttribute(at_implex)
	xom.addAttribute(at_Ap)
	xom.addAttribute(at_use_dpMax)
	xom.addAttribute(at_dpMax)
	xom.addAttribute(at_use_dnMax)
	xom.addAttribute(at_dnMax)
	xom.addAttribute(at_use_dchem)
	xom.addAttribute(at_dchem)
	xom.addAttribute(at_use_dchemp)
	xom.addAttribute(at_dchemp)
	xom.addAttribute(at_use_dchemvar)
	xom.addAttribute(at_eps_u)
	xom.addAttribute(at_use_srf)
	xom.addAttribute(at_gammaC)
	xom.addAttribute(at_use_srfCompr)
	xom.addAttribute(at_use_eqTensDef)
	xom.addAttribute(at_eqTensDef)
	
	# Dependencies
	xom.setVisibilityDependency(at_use_lc, at_lc)
	xom.setVisibilityDependency(at_use_dpMax, at_dpMax)
	xom.setVisibilityDependency(at_use_dnMax, at_dnMax)
	xom.setVisibilityDependency(at_use_dchem, at_dchem)
	xom.setVisibilityDependency(at_use_dchem, at_use_dchemp)
	xom.setVisibilityDependency(at_use_dchemp, at_dchemp)
	xom.setVisibilityDependency(at_use_dchem, at_use_dchemvar)
	xom.setVisibilityDependency(at_use_dchemvar, at_eps_u)
	xom.setVisibilityDependency(at_use_srf, at_gammaC)
	xom.setVisibilityDependency(at_use_srf, at_use_srfCompr)
	xom.setVisibilityDependency(at_use_eqTensDef, at_eqTensDef)
	
	return xom
	
def __get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def writeTcl(pinfo):
	
	#nDMaterial ElasticIsotropic $matTag $E $v <$rho>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	Ec = __get_xobj_attribute(xobj, 'Ec').quantityScalar.value
	v = __get_xobj_attribute(xobj, 'v').real
	f0n = __get_xobj_attribute(xobj, 'f0n').quantityScalar.value
	f02dn = __get_xobj_attribute(xobj, 'f02dn').quantityScalar.value
	ft = __get_xobj_attribute(xobj, 'ft').quantityScalar.value
	beta = __get_xobj_attribute(xobj, 'beta').real
	An = __get_xobj_attribute(xobj, 'An').real
	Bn = __get_xobj_attribute(xobj, 'Bn').real
	Gf = __get_xobj_attribute(xobj, 'Gf').quantityScalar.value
	Ap = __get_xobj_attribute(xobj, 'Ap').real
	implex = 0 if __get_xobj_attribute(xobj, 'implex').string == 'Implicit' else 1
	
	# optional parameters
	sopt = ''
	
	# manage Gf
	sopt += '-Gf {}'.format(Gf)
	
	# specfy lc
	use_lc = __get_xobj_attribute(xobj,'-lc').boolean
	lc = __get_xobj_attribute(xobj, 'lc').quantityScalar.value
	if use_lc:
		sopt += ' -lc {}'.format(lc)
		
	# specify srf
	use_srf = __get_xobj_attribute(xobj,'-srf').boolean
	gammaC = __get_xobj_attribute(xobj, 'gammaC').real
	if use_srf:
		sopt += ' -srf {}'.format(gammaC)
	use_srfCompr = __get_xobj_attribute(xobj, '-srfCompr').boolean
	if use_srfCompr:
		sopt += ' -srfCompr'
	
	# Other optional parameters
	
	str_tcl = '{}nDMaterial Concrete {} {} {} {} {} {} {} {} {} {} {}\n'.format(pinfo.indent, tag, Ec, v, f0n, f02dn, ft, beta, An, Bn, Ap, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)