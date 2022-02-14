import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Group'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# nu
	at_nu = MpcAttributeMetaData()
	at_nu.type = MpcAttributeType.Real
	at_nu.name = 'nu'
	at_nu.group = 'Group'
	at_nu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nu')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# ft
	at_ft = MpcAttributeMetaData()
	at_ft.type = MpcAttributeType.QuantityScalar
	at_ft.name = 'ft'
	at_ft.group = 'Group'
	at_ft.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ft')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_ft.dimension = u.F/u.L**2
	
	# fc
	at_fc = MpcAttributeMetaData()
	at_fc.type = MpcAttributeType.QuantityScalar
	at_fc.name = 'fc'
	at_fc.group = 'Group'
	at_fc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fc')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_fc.dimension = u.F/u.L**2
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Group'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'Optional parameters'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# Ap
	at_Ap = MpcAttributeMetaData()
	at_Ap.type = MpcAttributeType.Real
	at_Ap.name = 'Ap'
	at_Ap.group = 'Optional parameters'
	at_Ap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ap')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# An
	at_An = MpcAttributeMetaData()
	at_An.type = MpcAttributeType.Real
	at_An.name = 'An'
	at_An.group = 'Optional parameters'
	at_An.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('An')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# Bn
	at_Bn = MpcAttributeMetaData()
	at_Bn.type = MpcAttributeType.Real
	at_Bn.name = 'Bn'
	at_Bn.group = 'Optional parameters'
	at_Bn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Bn')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'PlasticDamageConcretePlaneStress'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_E)
	xom.addAttribute(at_nu)
	xom.addAttribute(at_ft)
	xom.addAttribute(at_fc)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_Ap)
	xom.addAttribute(at_An)
	xom.addAttribute(at_Bn)
	
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_beta)
	xom.setVisibilityDependency(at_Optional, at_Ap)
	xom.setVisibilityDependency(at_Optional, at_An)
	xom.setVisibilityDependency(at_Optional, at_Bn)
	
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial PlasticDamageConcretePlaneStress $tag $E $nu $ft $fc <$beta $Ap $An $Bn>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar
	
	nu_at = xobj.getAttribute('nu')
	if(nu_at is None):
		raise Exception('Error: cannot find "nu" attribute')
	nu = nu_at.real
	
	ft_at = xobj.getAttribute('ft')
	if(ft_at is None):
		raise Exception('Error: cannot find "ft" attribute')
	ft = ft_at.quantityScalar
	
	fc_at = xobj.getAttribute('fc')
	if(fc_at is None):
		raise Exception('Error: cannot find "fc" attribute')
	fc = fc_at.quantityScalar
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		beta_at = xobj.getAttribute('beta')
		if(beta_at is None):
			raise Exception('Error: cannot find "beta" attribute')
		beta = beta_at.real
		
		Ap_at = xobj.getAttribute('Ap')
		if(Ap_at is None):
			raise Exception('Error: cannot find "Ap" attribute')
		Ap = Ap_at.real
		
		An_at = xobj.getAttribute('An')
		if(An_at is None):
			raise Exception('Error: cannot find "An" attribute')
		An = An_at.real
		
		Bn_at = xobj.getAttribute('Bn')
		if(Bn_at is None):
			raise Exception('Error: cannot find "Bn" attribute')
		Bn = Bn_at.real
		
		sopt += '{} {} {} {}'.format(beta, Ap, An, Bn)
	
	str_tcl = '{}nDMaterial PlasticDamageConcretePlaneStress {} {} {} {} {} {}\n'.format(pinfo.indent, tag, E.value, nu, ft.value, fc.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)