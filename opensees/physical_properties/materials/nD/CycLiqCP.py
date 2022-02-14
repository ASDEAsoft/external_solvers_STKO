import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# G0
	at_G0 = MpcAttributeMetaData()
	at_G0.type = MpcAttributeType.QuantityScalar
	at_G0.name = 'G0'
	at_G0.group = 'Non-linear'
	at_G0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('G0')+'<br/>') + 
		html_par('A constant related to elastic shear modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	at_G0.dimension = u.F/u.L**2
	
	# kappa
	at_kappa = MpcAttributeMetaData()
	at_kappa.type = MpcAttributeType.QuantityScalar
	at_kappa.name = 'kappa'
	at_kappa.group = 'Non-linear'
	at_kappa.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kappa')+'<br/>') + 
		html_par('A constant related to elastic bulk modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	at_kappa.dimension = u.F/u.L**2
	
	# h
	at_h = MpcAttributeMetaData()
	at_h.type = MpcAttributeType.Real
	at_h.name = 'h'
	at_h.group = 'Non-linear'
	at_h.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h')+'<br/>') + 
		html_par('Model parameter for plastic modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	
	# Mfc
	at_Mfc = MpcAttributeMetaData()
	at_Mfc.type = MpcAttributeType.Real
	at_Mfc.name = 'Mfc'
	at_Mfc.group = 'Non-linear'
	at_Mfc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mfc')+'<br/>') + 
		html_par('Stress ratio at failure in triaxial compression') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	
	# dre1
	at_dre1 = MpcAttributeMetaData()
	at_dre1.type = MpcAttributeType.Real
	at_dre1.name = 'dre1'
	at_dre1.group = 'Non-linear'
	at_dre1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dre1')+'<br/>') + 
		html_par('Coefficient for reversible dilatancy generation') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	
	# Mdc
	at_Mdc = MpcAttributeMetaData()
	at_Mdc.type = MpcAttributeType.Real
	at_Mdc.name = 'Mdc'
	at_Mdc.group = 'Non-linear'
	at_Mdc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mdc')+'<br/>') + 
		html_par('Stress ratio at which the reversible dilatancy sign changes') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	
	# dre2
	at_dre2 = MpcAttributeMetaData()
	at_dre2.type = MpcAttributeType.Real
	at_dre2.name = 'dre2'
	at_dre2.group = 'Non-linear'
	at_dre2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dre2')+'<br/>') + 
		html_par('Coefficient for reversible dilatancy release') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	
	# rdr
	at_rdr = MpcAttributeMetaData()
	at_rdr.type = MpcAttributeType.QuantityScalar
	at_rdr.name = 'rdr'
	at_rdr.group = 'Non-linear'
	at_rdr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rdr')+'<br/>') + 
		html_par('Reference shear strain length') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	at_rdr.dimension = u.L
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Non-linear'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('Parameter controlling the decrease rate of irreversible dilatancy') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	
	# dir
	at_dir = MpcAttributeMetaData()
	at_dir.type = MpcAttributeType.Real
	at_dir.name = 'dir'
	at_dir.group = 'Non-linear'
	at_dir.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir')+'<br/>') + 
		html_par('Coefficient for irreversible dilatancy potential') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	
	# ein
	at_ein = MpcAttributeMetaData()
	at_ein.type = MpcAttributeType.Real
	at_ein.name = 'ein'
	at_ein.group = 'Non-linear'
	at_ein.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ein')+'<br/>') + 
		html_par('Initial void ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
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
		html_par('Saturated mass density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
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
		html_par('Saturated mass density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CycLiqCP_Material_(Cyclic_ElasticPlasticity)','CycLiqCP Material (Cyclic ElasticPlasticity)')+'<br/>') +
		html_end()
		)
	#at_rho.dimension = u.M/u.L**3
	
	xom = MpcXObjectMetaData()
	xom.name = 'CycLiqCP'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_G0)
	xom.addAttribute(at_kappa)
	xom.addAttribute(at_h)
	xom.addAttribute(at_Mfc)
	xom.addAttribute(at_dre1)
	xom.addAttribute(at_Mdc)
	xom.addAttribute(at_dre2)
	xom.addAttribute(at_rdr)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_dir)
	xom.addAttribute(at_ein)
	xom.addAttribute(at_use_rho)
	xom.addAttribute(at_rho)
	
	#use_rho-dep
	xom.setVisibilityDependency(at_use_rho, at_rho)
	
	return xom

def writeTcl(pinfo):
	
	#nDmaterial CycLiqCP $matTag $G0 $kappa $h $Mfc $dre1 $Mdc $dre2 $rdr $alpha $dir $ein <$rho>
	xobj = pinfo.phys_prop.XObject
	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	G0_at = xobj.getAttribute('G0')
	if(G0_at is None):
		raise Exception('Error: cannot find "G0" attribute')
	G0 = G0_at.quantityScalar
	
	kappa_at = xobj.getAttribute('kappa')
	if(kappa_at is None):
		raise Exception('Error: cannot find "kappa" attribute')
	kappa = kappa_at.quantityScalar
	
	h_at = xobj.getAttribute('h')
	if(h_at is None):
		raise Exception('Error: cannot find "h" attribute')
	h = h_at.real
	
	Mfc_at = xobj.getAttribute('Mfc')
	if(Mfc_at is None):
		raise Exception('Error: cannot find "Mfc" attribute')
	Mfc = Mfc_at.real
	
	dre1_at = xobj.getAttribute('dre1')
	if(dre1_at is None):
		raise Exception('Error: cannot find "dre1" attribute')
	dre1 = dre1_at.real
	
	Mdc_at = xobj.getAttribute('Mdc')
	if(Mdc_at is None):
		raise Exception('Error: cannot find "Mdc" attribute')
	Mdc = Mdc_at.real
	
	dre2_at = xobj.getAttribute('dre2')
	if(dre2_at is None):
		raise Exception('Error: cannot find "dre2" attribute')
	dre2 = dre2_at.real
	
	rdr_at = xobj.getAttribute('rdr')
	if(rdr_at is None):
		raise Exception('Error: cannot find "rdr" attribute')
	rdr = rdr_at.quantityScalar
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	dir_at = xobj.getAttribute('dir')
	if(dir_at is None):
		raise Exception('Error: cannot find "dir" attribute')
	dir = dir_at.real
	
	ein_at = xobj.getAttribute('ein')
	if(ein_at is None):
		raise Exception('Error: cannot find "ein" attribute')
	ein = ein_at.real
	
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
	
	str_tcl = '{}nDMaterial CycLiqCP {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, G0.value, kappa.value, h, Mfc, dre1, Mdc, dre2, rdr.value, alpha, dir, ein, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)