# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

####################################################################################
# Utilities
####################################################################################

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def _description(title, body):
	return (
		html_par(html_begin()) +
		html_par(html_boldtext(title)+'<br/>') + 
		html_par(body) +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/ConcretewBeta_Material','ConcretewBeta Material')) +
		html_end()
		)

# A simple class that collects all the material parameters 
# obtained from the XObject
class ConcretewBetaParameters:
	
	class Beta:
		def __init__(self, xobj):
			self.bint = _get_xobj_attribute(xobj, 'bint').real
			self.ebint = _get_xobj_attribute(xobj, 'ebint').real
			self.bres = _get_xobj_attribute(xobj, 'bres').real
			self.ebres = _get_xobj_attribute(xobj, 'ebres').real
	
	class Conf:
		def __init__(self, xobj):
			self.fcc = _get_xobj_attribute(xobj, 'fcc').quantityScalar.value
			self.ecc = _get_xobj_attribute(xobj, 'ecc').real
	
	def __init__(self, xobj):
		
		# tag
		self.tag = xobj.parent.componentId
		
		# mandatory parameters
		self.fpc = _get_xobj_attribute(xobj, 'fpc').quantityScalar.value
		self.ec0 = _get_xobj_attribute(xobj, 'ec0').real
		self.fcint = _get_xobj_attribute(xobj, 'fcint').quantityScalar.value
		self.ecint = _get_xobj_attribute(xobj, 'ecint').real
		self.fcres = _get_xobj_attribute(xobj, 'fcres').quantityScalar.value
		self.ecres = _get_xobj_attribute(xobj, 'ecres').real
		self.ft = _get_xobj_attribute(xobj, 'ft').quantityScalar.value
		self.ftint = _get_xobj_attribute(xobj, 'ftint').quantityScalar.value
		self.etint = _get_xobj_attribute(xobj, 'etint').real
		self.ftres = _get_xobj_attribute(xobj, 'ftres').quantityScalar.value
		self.etres = _get_xobj_attribute(xobj, 'etres').real
		self.LR = _get_xobj_attribute(xobj, 'LR').quantityScalar.value
		
		# optional parameters
		if _get_xobj_attribute(xobj, '-lambda').boolean:
			self.lambda_ = _get_xobj_attribute(xobj, 'lambda').real
		else:
			self.lambda_ = None
		if _get_xobj_attribute(xobj, '-alpha').boolean:
			self.alpha = _get_xobj_attribute(xobj, 'alpha').real
		else:
			self.alpha = None
		if _get_xobj_attribute(xobj, '-beta').boolean:
			self.beta = ConcretewBetaParameters.Beta(xobj)
		else:
			self.beta = None
		if _get_xobj_attribute(xobj, '-M').boolean:
			self.M = _get_xobj_attribute(xobj, 'M').real
		else:
			self.M = None
		if _get_xobj_attribute(xobj, '-E').boolean:
			self.Ec = _get_xobj_attribute(xobj, 'Ec').quantityScalar.value
		else:
			self.Ec = None
		if _get_xobj_attribute(xobj, '-conf').boolean:
			self.conf = ConcretewBetaParameters.Conf(xobj)
		else:
			self.conf = None

# Writes the tcl command for the ConcretewBeta material from the ConcretewBetaParameters p.
# In this way external scripts like RCTrussModel2DElement can get ConcretewBetaParameters p,
# modify some parameters, for example to apply fracture energy regularization, and then
# write the tcl command for the modified material
def writeTclInternal(pinfo, p):
	#uniaxialMaterial ConcretewBeta $matTag $fpc $ec0 $fcint $ecint $fcres $ecres $ft $ftint $etint $ftres $etres <-lambda $lambda> <-alpha $alpha> <-beta $bint $ebint $bres $ebres> <-M $M> <-E $Ec> <-conf $fcc $ecc>
	
	# build strings for optional parameters
	if p.lambda_ is not None:
		str_lambda = '   -lambda {}'.format(p.lambda_)
	else:
		str_lambda = ''
	if p.alpha is not None:
		str_alpha = '   -alpha {}'.format(p.alpha)
	else:
		str_alpha = ''
	if p.beta is not None:
		str_beta = '   -beta {} {} {} {}'.format(p.beta.bint, p.beta.ebint, p.beta.bres, p.beta.ebres)
	else:
		str_beta = ''
	if p.M is not None:
		str_M = '   -M {}'.format(p.M)
	else:
		str_M = ''
	if p.Ec is not None:
		str_E = '   -E {}'.format(p.Ec)
	else:
		str_E = ''
	if p.conf is not None:
		str_conf = '   -conf {} {}'.format(p.conf.fcc, p.conf.ecc)
	else:
		str_conf = ''
	
	# build the tcl command
	str_tcl = '{}uniaxialMaterial ConcretewBeta {}   {} {} {} {} {} {}   {} {} {} {} {}{}{}{}{}{}{}\n'.format(
		pinfo.indent, p.tag, 
		p.fpc, p.ec0, p.fcint, p.ecint, p.fcres, p.ecres,
		p.ft, p.ftint, p.etint, p.ftres, p.etres,
		str_lambda, str_alpha, str_beta, str_M, str_E, str_conf
		)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)

####################################################################################
# Main methods
####################################################################################

def makeXObjectMetaData():
	
	####################################################################################
	# Compression attributes
	####################################################################################
	
	# fpc
	at_fpc = MpcAttributeMetaData()
	at_fpc.type = MpcAttributeType.QuantityScalar
	at_fpc.name = 'fpc'
	at_fpc.group = 'Compression'
	at_fpc.description = _description('fpc', 'peak unconfined concrete compressive strength (negative)')
	at_fpc.dimension = u.F/u.L**2
	
	# ec0
	at_ec0 = MpcAttributeMetaData()
	at_ec0.type = MpcAttributeType.Real
	at_ec0.name = 'ec0'
	at_ec0.group = 'Compression'
	at_ec0.description = _description('ec0', 'compressive strain corresponding to unconfined concrete compressive strength (negative)')
	
	# fcint
	at_fcint = MpcAttributeMetaData()
	at_fcint.type = MpcAttributeType.QuantityScalar
	at_fcint.name = 'fcint'
	at_fcint.group = 'Compression'
	at_fcint.description = _description('fcint', 'stress of intermediate stress-strain point for compression post-peak envelope (negative)')
	at_fcint.dimension = u.F/u.L**2
	
	# ecint
	at_ecint = MpcAttributeMetaData()
	at_ecint.type = MpcAttributeType.Real
	at_ecint.name = 'ecint'
	at_ecint.group = 'Compression'
	at_ecint.description = _description('ecint', 'strain of intermediate stress-strain point for compression post-peak envelope (negative)')
	
	# fcres
	at_fcres = MpcAttributeMetaData()
	at_fcres.type = MpcAttributeType.QuantityScalar
	at_fcres.name = 'fcres'
	at_fcres.group = 'Compression'
	at_fcres.description = _description('fcres', 'stress of residual stress-strain point for compression post-peak envelope (negative)')
	at_fcres.dimension = u.F/u.L**2
	
	# ecres
	at_ecres = MpcAttributeMetaData()
	at_ecres.type = MpcAttributeType.Real
	at_ecres.name = 'ecres'
	at_ecres.group = 'Compression'
	at_ecres.description = _description('ecres', 'strain of residual stress-strain point for compression post-peak envelope (negative)')
	
	####################################################################################
	# Tension attributes
	####################################################################################
	
	# ft
	at_ft = MpcAttributeMetaData()
	at_ft.type = MpcAttributeType.QuantityScalar
	at_ft.name = 'ft'
	at_ft.group = 'Tension'
	at_ft.description = _description('ft', 'tensile strength of concrete (positive)')
	at_ft.dimension = u.F/u.L**2
	
	# ftint
	at_ftint = MpcAttributeMetaData()
	at_ftint.type = MpcAttributeType.QuantityScalar
	at_ftint.name = 'ftint'
	at_ftint.group = 'Tension'
	at_ftint.description = _description('ftint', 'stress of intermediate stress-strain point for tension softening envelope (positive)')
	at_ftint.dimension = u.F/u.L**2
	
	# etint
	at_etint = MpcAttributeMetaData()
	at_etint.type = MpcAttributeType.Real
	at_etint.name = 'etint'
	at_etint.group = 'Tension'
	at_etint.description = _description('etint', 'strain of intermediate stress-strain point for tension softening envelope (positive)')
	
	# ftres
	at_ftres = MpcAttributeMetaData()
	at_ftres.type = MpcAttributeType.QuantityScalar
	at_ftres.name = 'ftres'
	at_ftres.group = 'Tension'
	at_ftres.description = _description('ftres', 'stress of residual stress-strain point for tension softening envelope (positive)')
	at_ftres.dimension = u.F/u.L**2
	
	# etres
	at_etres = MpcAttributeMetaData()
	at_etres.type = MpcAttributeType.Real
	at_etres.name = 'etres'
	at_etres.group = 'Tension'
	at_etres.description = _description('etres', 'strain of residual stress-strain point for tension softening envelope (positive)')
	
	####################################################################################
	# Misc attributes
	####################################################################################
	
	# LR
	at_LR = MpcAttributeMetaData()
	at_LR.type = MpcAttributeType.QuantityScalar
	at_LR.name = 'LR'
	at_LR.group = 'Misc'
	at_LR.description = _description('LR', (
		'Characteristic size of the specimen used to obtain the stress-strain curve.<br/>'
		'This parameter is used for fracture energy regularization in order to obtain mesh-size objectivity.<br/>'
		'In the examples provided in the OpenSEES documentation a reference size of 600 mm was used.'))
	at_LR.dimension = u.L
	at_LR.setDefault(1.0)
	
	####################################################################################
	# Optional parameters attributes
	####################################################################################
	
	# -lambda
	at_use_lambda = MpcAttributeMetaData()
	at_use_lambda.type = MpcAttributeType.Boolean
	at_use_lambda.name = '-lambda'
	at_use_lambda.group = 'Optional'
	at_use_lambda.description = _description('-lambda', 'input optional parameter: lambda')
	
	# lambda
	at_lambda = MpcAttributeMetaData()
	at_lambda.type = MpcAttributeType.Real
	at_lambda.name = 'lambda'
	at_lambda.group = 'Optional'
	at_lambda.description = _description('lambda', 'controls the path of unloading from compression strain (default 0.5)')
	at_lambda.setDefault(0.5)
	
	# -alpha
	at_use_alpha = MpcAttributeMetaData()
	at_use_alpha.type = MpcAttributeType.Boolean
	at_use_alpha.name = '-alpha'
	at_use_alpha.group = 'Optional'
	at_use_alpha.description = _description('-alpha', 'input optional parameter: alpha')
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Optional'
	at_alpha.description = _description('alpha', 'controls the path of unloading from tensile strain (default 1)')
	at_alpha.setDefault(1.0)
	
	# -beta
	at_use_beta = MpcAttributeMetaData()
	at_use_beta.type = MpcAttributeType.Boolean
	at_use_beta.name = '-beta'
	at_use_beta.group = 'Optional'
	at_use_beta.description = _description('-beta', 'input optional parameters: bint, ebint, bres, ebres')
	
	# bint
	at_bint = MpcAttributeMetaData()
	at_bint.type = MpcAttributeType.Real
	at_bint.name = 'bint'
	at_bint.group = 'Optional'
	at_bint.description = _description('bint', '&beta; of intermediate &beta;-strain point for for biaxial effect (default 1)')
	at_bint.setDefault(1.0)
	
	# ebint
	at_ebint = MpcAttributeMetaData()
	at_ebint.type = MpcAttributeType.Real
	at_ebint.name = 'ebint'
	at_ebint.group = 'Optional'
	at_ebint.description = _description('ebint', 'strain of intermediate &beta;-strain point for for biaxial effect (default 0)')
	at_ebint.setDefault(0.0)
	
	# bres
	at_bres = MpcAttributeMetaData()
	at_bres.type = MpcAttributeType.Real
	at_bres.name = 'bres'
	at_bres.group = 'Optional'
	at_bres.description = _description('bres', '&beta; of residual &beta;-strain point for for biaxial effect (default 1)')
	at_bres.setDefault(1.0)
	
	# ebres
	at_ebres = MpcAttributeMetaData()
	at_ebres.type = MpcAttributeType.Real
	at_ebres.name = 'ebres'
	at_ebres.group = 'Optional'
	at_ebres.description = _description('ebres', 'strain of residual &beta;-strain point for for biaxial effect (default 0)')
	at_ebres.setDefault(0.0)
	
	# -M
	at_use_M = MpcAttributeMetaData()
	at_use_M.type = MpcAttributeType.Boolean
	at_use_M.name = '-M'
	at_use_M.group = 'Optional'
	at_use_M.description = _description('-M', 'input optional parameter: M')
	
	# M
	at_M = MpcAttributeMetaData()
	at_M.type = MpcAttributeType.Real
	at_M.name = 'M'
	at_M.group = 'Optional'
	at_M.description = _description('M', ('factor for Stevens et al. (1991) tension stiffening (default 0)<br/>'
		'For non-zero $M, the tension stiffening behavior will govern the post-peak tension envelope.<br/>'
		'Tri-linear tension softening parameters $ftint, $etint, $ftres, $etres will have no effect, but dummy values must be specified.'))
	at_M.setDefault(0.0)
	
	# -E
	at_use_E = MpcAttributeMetaData()
	at_use_E.type = MpcAttributeType.Boolean
	at_use_E.name = '-E'
	at_use_E.group = 'Optional'
	at_use_E.description = _description('-E', 'input optional parameter: Ec')
	
	# Ec
	at_Ec = MpcAttributeMetaData()
	at_Ec.type = MpcAttributeType.QuantityScalar
	at_Ec.name = 'Ec'
	at_Ec.group = 'Optional'
	at_Ec.description = _description('Ec', ('initial stiffness (default 2*$fpc/$ec0)<br/>'
		'Value of $Ec must be between $fpc/$ec0 and 2*$fpc/$ec0 otherwise the closest value will be assigned.'))
	at_Ec.dimension = u.F/u.L**2
	
	# -conf
	at_use_conf = MpcAttributeMetaData()
	at_use_conf.type = MpcAttributeType.Boolean
	at_use_conf.name = '-conf'
	at_use_conf.group = 'Optional'
	at_use_conf.description = _description('-conf', 'input optional parameters: fcc, ecc')
	
	# fcc
	at_fcc = MpcAttributeMetaData()
	at_fcc.type = MpcAttributeType.QuantityScalar
	at_fcc.name = 'fcc'
	at_fcc.group = 'Optional'
	at_fcc.description = _description('fcc', 'confined concrete peak compressive stress')
	at_fcc.dimension = u.F/u.L**2
	
	# ecc
	at_ecc = MpcAttributeMetaData()
	at_ecc.type = MpcAttributeType.Real
	at_ecc.name = 'ecc'
	at_ecc.group = 'Optional'
	at_ecc.description = _description('ecc', 'confined concrete peak compressive strain')
	
	####################################################################################
	# Create XObject Meta Data and add all attributes
	####################################################################################
	
	xom = MpcXObjectMetaData()
	xom.name = 'ConcretewBeta'
	xom.Xgroup = 'Concrete Materials'
	# Elasticity
	# Compression
	xom.addAttribute(at_fpc)
	xom.addAttribute(at_ec0)
	xom.addAttribute(at_fcint)
	xom.addAttribute(at_ecint)
	xom.addAttribute(at_fcres)
	xom.addAttribute(at_ecres)
	# Tension
	xom.addAttribute(at_ft)
	xom.addAttribute(at_ftint)
	xom.addAttribute(at_etint)
	xom.addAttribute(at_ftres)
	xom.addAttribute(at_etres)
	# Misc
	xom.addAttribute(at_LR)
	# Optional
	xom.addAttribute(at_use_lambda)
	xom.addAttribute(at_lambda)
	xom.addAttribute(at_use_alpha)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_use_beta)
	xom.addAttribute(at_bint)
	xom.addAttribute(at_ebint)
	xom.addAttribute(at_bres)
	xom.addAttribute(at_ebres)
	xom.addAttribute(at_use_M)
	xom.addAttribute(at_M)
	xom.addAttribute(at_use_E)
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_use_conf)
	xom.addAttribute(at_fcc)
	xom.addAttribute(at_ecc)
	
	# boolean dependencies
	xom.setVisibilityDependency(at_use_lambda, at_lambda)
	xom.setVisibilityDependency(at_use_alpha, at_alpha)
	xom.setVisibilityDependency(at_use_beta, at_bint)
	xom.setVisibilityDependency(at_use_beta, at_ebint)
	xom.setVisibilityDependency(at_use_beta, at_bres)
	xom.setVisibilityDependency(at_use_beta, at_ebres)
	xom.setVisibilityDependency(at_use_M, at_M)
	xom.setVisibilityDependency(at_use_E, at_Ec)
	xom.setVisibilityDependency(at_use_conf, at_fcc)
	xom.setVisibilityDependency(at_use_conf, at_ecc)
	
	return xom

def writeTcl(pinfo):
	# get parameters
	p = ConcretewBetaParameters(pinfo.phys_prop.XObject)
	# write
	writeTclInternal(pinfo, p)

