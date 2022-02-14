import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# massDensity
	at_massDensity = MpcAttributeMetaData()
	at_massDensity.type = MpcAttributeType.QuantityScalar
	at_massDensity.name = 'massDensity'
	at_massDensity.group = 'Non-linear'
	at_massDensity.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('massDensity')+'<br/>') + 
		html_par('mass density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bounding_Cam_Clay','Bounding Cam Clay')+'<br/>') +
		html_end()
		)
	#at_massDensity.dimension = u.M/u.L**3
	
	# C
	at_C = MpcAttributeMetaData()
	at_C.type = MpcAttributeType.Real
	at_C.name = 'C'
	at_C.group = 'Non-linear'
	at_C.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('C')+'<br/>') + 
		html_par('ellipsoidal axis ratio (defines shape of ellipsoidal loading/bounding surfaces)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bounding_Cam_Clay','Bounding Cam Clay')+'<br/>') +
		html_end()
		)
	
	# bulkMod
	at_bulkMod = MpcAttributeMetaData()
	at_bulkMod.type = MpcAttributeType.Real
	at_bulkMod.name = 'bulkMod'
	at_bulkMod.group = 'Non-linear'
	at_bulkMod.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bulkMod')+'<br/>') + 
		html_par('initial bulk modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bounding_Cam_Clay','Bounding Cam Clay')+'<br/>') +
		html_end()
		)
	
	# OCR
	at_OCR = MpcAttributeMetaData()
	at_OCR.type = MpcAttributeType.Real
	at_OCR.name = 'OCR'
	at_OCR.group = 'Non-linear'
	at_OCR.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OCR')+'<br/>') + 
		html_par('overconsolidation ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bounding_Cam_Clay','Bounding Cam Clay')+'<br/>') +
		html_end()
		)
	
	# mu_o
	at_mu_o = MpcAttributeMetaData()
	at_mu_o.type = MpcAttributeType.QuantityScalar
	at_mu_o.name = 'mu_o'
	at_mu_o.group = 'Non-linear'
	at_mu_o.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu_o')+'<br/>') + 
		html_par('initial shear modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bounding_Cam_Clay','Bounding Cam Clay')+'<br/>') +
		html_end()
		)
	at_mu_o.dimension = u.F/u.L**2
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Non-linear'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') + 
		html_par('pressure-dependency parameter for modulii (greater than or equal to zero)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bounding_Cam_Clay','Bounding Cam Clay')+'<br/>') +
		html_end()
		)
	
	# lambda
	at_lambda = MpcAttributeMetaData()
	at_lambda.type = MpcAttributeType.Real
	at_lambda.name = 'lambda'
	at_lambda.group = 'Non-linear'
	at_lambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lambda')+'<br/>') + 
		html_par('soil compressibility index for virgin loading') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bounding_Cam_Clay','Bounding Cam Clay')+'<br/>') +
		html_end()
		)
	
	# h
	at_h = MpcAttributeMetaData()
	at_h.type = MpcAttributeType.Real
	at_h.name = 'h'
	at_h.group = 'Non-linear'
	at_h.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('h')+'<br/>') + 
		html_par('hardening parameter for plastic response inside of bounding surface (if h = 0, no hardening)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bounding_Cam_Clay','Bounding Cam Clay')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.Real
	at_m.name = 'm'
	at_m.group = 'Non-linear'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') + 
		html_par('hardening parameter (exponent) for plastic response inside of bounding surface (if m = 0, only linear hardening)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bounding_Cam_Clay','Bounding Cam Clay')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'BoundingCamClay'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_massDensity)
	xom.addAttribute(at_C)
	xom.addAttribute(at_bulkMod)
	xom.addAttribute(at_OCR)
	xom.addAttribute(at_mu_o)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_lambda)
	xom.addAttribute(at_h)
	xom.addAttribute(at_m)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial BoundingCamClay $matTag $massDensity $C $bulkMod $OCR $mu_o $alpha $lambda $h $m
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	massDensity_at = xobj.getAttribute('massDensity')
	if(massDensity_at is None):
		raise Exception('Error: cannot find "massDensity" attribute')
	massDensity = massDensity_at.quantityScalar
	
	C_at = xobj.getAttribute('C')
	if(C_at is None):
		raise Exception('Error: cannot find "C" attribute')
	C = C_at.real
	
	bulkMod_at = xobj.getAttribute('bulkMod')
	if(bulkMod_at is None):
		raise Exception('Error: cannot find "bulkMod" attribute')
	bulkMod = bulkMod_at.real
	
	OCR_at = xobj.getAttribute('OCR')
	if(OCR_at is None):
		raise Exception('Error: cannot find "OCR" attribute')
	OCR = OCR_at.real
	
	mu_o_at = xobj.getAttribute('mu_o')
	if(mu_o_at is None):
		raise Exception('Error: cannot find "mu_o" attribute')
	mu_o = mu_o_at.quantityScalar
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
	lambda_at = xobj.getAttribute('lambda')
	if(lambda_at is None):
		raise Exception('Error: cannot find "lambda" attribute')
	lambd = lambda_at.real
	
	h_at = xobj.getAttribute('h')
	if(h_at is None):
		raise Exception('Error: cannot find "h" attribute')
	h = h_at.real
	
	m_at = xobj.getAttribute('m')
	if(m_at is None):
		raise Exception('Error: cannot find "m" attribute')
	m = m_at.real
	
	str_tcl = '{}nDMaterial BoundingCamClay {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, massDensity.value, C, bulkMod, OCR, mu_o.value, alpha, lambd, h, m)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)