import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = 'Group'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') + 
		html_par('tolerance for convergence of the element state. Suggested value: E-12 to E-10. OpenSees will warn if convergence is not achieved, however this usually does not prevent global convergence.') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/3188.htm','Isolator2spring Section')+'<br/>') +
		html_end()
		)
	
	# k1
	at_k1 = MpcAttributeMetaData()
	at_k1.type = MpcAttributeType.QuantityScalar
	at_k1.name = 'k1'
	at_k1.group = 'Group'
	at_k1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k1')+'<br/>') + 
		html_par('initial stiffness for lateral force-deformation') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/3188.htm','Isolator2spring Section')+'<br/>') +
		html_end()
		)
	at_k1.dimension = u.F/u.L
	
	# Fyo
	at_Fyo = MpcAttributeMetaData()
	at_Fyo.type = MpcAttributeType.QuantityScalar
	at_Fyo.name = 'Fyo'
	at_Fyo.group = 'Group'
	at_Fyo.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fyo')+'<br/>') + 
		html_par('nominal yield strength for lateral force-deformation') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/3188.htm','Isolator2spring Section')+'<br/>') +
		html_end()
		)
	at_Fyo.dimension = u.F/u.L**2
	
	# k2o
	at_k2o = MpcAttributeMetaData()
	at_k2o.type = MpcAttributeType.QuantityScalar
	at_k2o.name = 'k2o'
	at_k2o.group = 'Group'
	at_k2o.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k2o')+'<br/>') + 
		html_par('nominal postyield stiffness for lateral force-deformation') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/3188.htm','Isolator2spring Section')+'<br/>') +
		html_end()
		)
	at_k2o.dimension = u.F/u.L
	
	# kvo
	at_kvo = MpcAttributeMetaData()
	at_kvo.type = MpcAttributeType.QuantityScalar
	at_kvo.name = 'kvo'
	at_kvo.group = 'Group'
	at_kvo.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kvo')+'<br/>') + 
		html_par('nominal stiffness in the vertical direction') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/3188.htm','Isolator2spring Section')+'<br/>') +
		html_end()
		)
	at_kvo.dimension = u.F/u.L
	
	# hb
	at_hb = MpcAttributeMetaData()
	at_hb.type = MpcAttributeType.QuantityScalar
	at_hb.name = 'hb'
	at_hb.group = 'Group'
	at_hb.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('hb')+'<br/>') + 
		html_par('total height of elastomeric bearing') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/3188.htm','Isolator2spring Section')+'<br/>') +
		html_end()
		)
	at_hb.dimension = u.L
	
	# PE
	at_PE = MpcAttributeMetaData()
	at_PE.type = MpcAttributeType.QuantityScalar
	at_PE.name = 'PE'
	at_PE.group = 'Group'
	at_PE.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('PE')+'<br/>') + 
		html_par('Euler Buckling load for the bearing') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/3188.htm','Isolator2spring Section')+'<br/>') +
		html_end()
		)
	at_PE.dimension = u.F
	
	# use_Po
	at_use_Po = MpcAttributeMetaData()
	at_use_Po.type = MpcAttributeType.Boolean
	at_use_Po.name = 'use_Po'
	at_use_Po.group = 'Group'
	at_use_Po.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_Po')+'<br/>') + 
		html_par('axial load at which nominal yield strength is achieved (optional, default = 0.0, i.e. no strength degradation)') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/3188.htm','Isolator2spring Section')+'<br/>') +
		html_end()
		)
	
	# Po
	at_Po = MpcAttributeMetaData()
	at_Po.type = MpcAttributeType.QuantityScalar
	at_Po.name = 'Po'
	at_Po.group = 'Optional parameters'
	at_Po.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Po')+'<br/>') + 
		html_par('axial load at which nominal yield strength is achieved (optional, default = 0.0, i.e. no strength degradation)') +
		html_par(html_href('http://opensees.berkeley.edu/OpenSees/manuals/usermanual/3188.htm','Isolator2spring Section')+'<br/>') +
		html_end()
		)
	at_Po.dimension = u.F
	
	xom = MpcXObjectMetaData()
	xom.name = 'Iso2spring'
	xom.addAttribute(at_tol)
	xom.addAttribute(at_k1)
	xom.addAttribute(at_Fyo)
	xom.addAttribute(at_k2o)
	xom.addAttribute(at_kvo)
	xom.addAttribute(at_hb)
	xom.addAttribute(at_PE)
	xom.addAttribute(at_use_Po)
	xom.addAttribute(at_Po)
	
	
	# use_Po-dep
	xom.setVisibilityDependency(at_use_Po, at_Po)
	
	return xom

def writeTcl(pinfo):
	
	#section Iso2spring $matTag $tol $k1 $Fyo $k2o $kvo $hb $PE <$Po>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	tol_at = xobj.getAttribute('tol')
	if(tol_at is None):
		raise Exception('Error: cannot find "tol" attribute')
	tol = tol_at.real
	
	k1_at = xobj.getAttribute('k1')
	if(k1_at is None):
		raise Exception('Error: cannot find "k1" attribute')
	k1 = k1_at.quantityScalar
	
	Fyo_at = xobj.getAttribute('Fyo')
	if(Fyo_at is None):
		raise Exception('Error: cannot find "Fyo" attribute')
	Fyo = Fyo_at.quantityScalar
	
	k2o_at = xobj.getAttribute('k2o')
	if(k2o_at is None):
		raise Exception('Error: cannot find "k2o" attribute')
	k2o = k2o_at.quantityScalar
	
	kvo_at = xobj.getAttribute('kvo')
	if(kvo_at is None):
		raise Exception('Error: cannot find "kvo" attribute')
	kvo = kvo_at.quantityScalar
	
	hb_at = xobj.getAttribute('hb')
	if(hb_at is None):
		raise Exception('Error: cannot find "hb" attribute')
	hb = hb_at.quantityScalar
	
	PE_at = xobj.getAttribute('PE')
	if(PE_at is None):
		raise Exception('Error: cannot find "PE" attribute')
	PE = PE_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	use_Po_at = xobj.getAttribute('use_Po')
	if(use_Po_at is None):
		raise Exception('Error: cannot find "use_Po" attribute')
	use_Po = use_Po_at.boolean
	if use_Po:
		Po_at = xobj.getAttribute('Po')
		if(Po_at is None):
			raise Exception('Error: cannot find "Po" attribute')
		Po = Po_at.quantityScalar
		
		sopt += '{}'.format(Po.value)
	
	
	str_tcl = '{}section Iso2spring {} {} {} {} {} {} {} {}{}\n'.format(
			pinfo.indent, tag, tol, k1.value, Fyo.value, k2o.value, kvo.value, hb.value, PE.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)