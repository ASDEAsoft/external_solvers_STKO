import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fc
	at_fc = MpcAttributeMetaData()
	at_fc.type = MpcAttributeType.QuantityScalar
	at_fc.name = 'fc'
	at_fc.group = 'Non linear'
	at_fc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fc')+'<br/>') + 
		html_par('concrete compressive strength at 28 days (positive)') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional concrete model')+'<br/>') +
		html_end()
		)
	at_fc.dimension = u.F/u.L**2
	
	# ft
	at_ft = MpcAttributeMetaData()
	at_ft.type = MpcAttributeType.QuantityScalar
	at_ft.name = 'ft'
	at_ft.group = 'Non linear'
	at_ft.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ft')+'<br/>') + 
		html_par('concrete tensile strength (positive)') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional concrete model')+'<br/>') +
		html_end()
		)
	at_ft.dimension = u.F/u.L**2
	
	# fcu
	at_fcu = MpcAttributeMetaData()
	at_fcu.type = MpcAttributeType.QuantityScalar
	at_fcu.name = 'fcu'
	at_fcu.group = 'Non linear'
	at_fcu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fcu')+'<br/>') + 
		html_par('concrete crushing strength (negative)') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional concrete model')+'<br/>') +
		html_end()
		)
	at_fcu.dimension = u.F/u.L**2
	
	# epsc0
	at_epsc0 = MpcAttributeMetaData()
	at_epsc0.type = MpcAttributeType.Real
	at_epsc0.name = 'epsc0'
	at_epsc0.group = 'Non linear'
	at_epsc0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsc0')+'<br/>') + 
		html_par('concrete strain at maximum strength (negative)') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional concrete model')+'<br/>') +
		html_end()
		)
	
	# epscu
	at_epscu = MpcAttributeMetaData()
	at_epscu.type = MpcAttributeType.Real
	at_epscu.name = 'epscu'
	at_epscu.group = 'Non linear'
	at_epscu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epscu')+'<br/>') + 
		html_par('concrete strain at crushing strength (negative)') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional concrete model')+'<br/>') +
		html_end()
		)
	
	# epstu
	at_epstu = MpcAttributeMetaData()
	at_epstu.type = MpcAttributeType.Real
	at_epstu.name = 'epstu'
	at_epstu.group = 'Non linear'
	at_epstu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epstu')+'<br/>') + 
		html_par('ultimate tensile strain (positive)') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional concrete model')+'<br/>') +
		html_end()
		)
	
	# stc
	at_stc = MpcAttributeMetaData()
	at_stc.type = MpcAttributeType.Real
	at_stc.name = 'stc'
	at_stc.group = 'Non linear'
	at_stc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('stc')+'<br/>') + 
		html_par('shear retention factor') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional concrete model')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'PlaneStressUserMaterial'
	xom.Xgroup = 'Materials for Modeling Concrete Walls'
	xom.addAttribute(at_fc)
	xom.addAttribute(at_ft)
	xom.addAttribute(at_fcu)
	xom.addAttribute(at_epsc0)
	xom.addAttribute(at_epscu)
	xom.addAttribute(at_epstu)
	xom.addAttribute(at_stc)
	
	return xom

def writeTcl(pinfo):
	
	#nDmaterial PlaneStressUserMaterial $matTag 40 7 $fc $ft $fcu $epsc0 $epscu $epstu $stc
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fc_at = xobj.getAttribute('fc')
	if(fc_at is None):
		raise Exception('Error: cannot find "fc" attribute')
	fc = fc_at.quantityScalar
	
	ft_at = xobj.getAttribute('ft')
	if(ft_at is None):
		raise Exception('Error: cannot find "ft" attribute')
	ft = ft_at.quantityScalar
	
	fcu_at = xobj.getAttribute('fcu')
	if(fcu_at is None):
		raise Exception('Error: cannot find "fcu" attribute')
	fcu = fcu_at.quantityScalar
	
	epsc0_at = xobj.getAttribute('epsc0')
	if(epsc0_at is None):
		raise Exception('Error: cannot find "epsc0" attribute')
	epsc0 = epsc0_at.real
	
	epscu_at = xobj.getAttribute('epscu')
	if(epscu_at is None):
		raise Exception('Error: cannot find "epscu" attribute')
	epscu = epscu_at.real
	
	epstu_at = xobj.getAttribute('epstu')
	if(epstu_at is None):
		raise Exception('Error: cannot find "epstu" attribute')
	epstu = epstu_at.real
	
	stc_at = xobj.getAttribute('stc')
	if(stc_at is None):
		raise Exception('Error: cannot find "stc" attribute')
	stc = stc_at.real
	
	str_tcl = '{}nDMaterial PlaneStressUserMaterial {} 40 7 {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fc.value, ft.value, fcu.value, epsc0, epscu, epstu, stc)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)